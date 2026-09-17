#!/usr/bin/env python3
"""Collect findings that external AI review bots posted on a PR and attach them to datasets.

Bots such as Qodo and CodeRabbit post findings as numbered items in summary comments and as
inline comments on files. Each finding is mapped to the datasets it concerns (inline comment
path, or dataset accessions mentioned anywhere in the finding) so the change report can quote
it next to that dataset. Findings are quoted, never interpreted: the text is untrusted and is
escaped by the renderer. A note is marked as confirmed when this report flags the same
column or kind of change for that dataset.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sdrf_change_report import parse_table  # noqa: E402

REVIEWERS = ("qodo-code-review[bot]", "coderabbitai[bot]", "copilot-pull-request-reviewer[bot]")
MAX_NOTES_PER_DATASET = 5
MAX_TITLE_CHARS = 120
MAX_DETAIL_CHARS = 260

# A numbered finding line carrying a category badge, e.g. Qodo's
# "<summary>  3.  Eight yeast datasets use animal terms <code>📘 Rule violation</code>"
# or inline "1\. Reverted changes keep stale warnings <code>🐞 Bug</code>".
FINDING_START = re.compile(r"(?m)^[ \t]*(?:<summary>[ \t]*)?\d+\\?\.[ \t]+(?=.*<code>)")
DATASET_PATH = re.compile(r"datasets/([^/\s]+)/")
NON_ANIMAL_GENERA = {"saccharomyces", "schizosaccharomyces", "candida", "pichia", "komagataella",
                     "escherichia", "bacillus", "mycobacterium", "streptomyces", "synechocystis",
                     "arabidopsis", "oryza", "zea", "chlamydomonas", "plasmodium", "trypanosoma"}
TEMPLATE_CLAIM = re.compile(r"\b(templates?|layers?|animal terms|classified as an animal)\b")
ORGANISM_KIND = re.compile(r"\b(yeast|fung\w*|bacteri\w*|plants?|human|animals?|invertebrates?|vertebrates?)\b")
FILE_CLAIM = re.compile(r"\b(checksums?|archives?|reports|outputs?|results?|spreadsheets?|tables|"
                        r"(support|auxiliary|utility|analysis) files?)\b")
RUN_WORDS = re.compile(r"\b(runs?|assays?|measurements?|acquisitions?)\b")
ACQUISITION = re.compile(r"\.(raw|wiff2?|wiff\.scan|d|baf|tdf|yep|lcd|mzml|mzxml|mgf|ms2|dat)"
                         r"(\.(zip|gz|bz2|tar|7z))?$")


def clean(text: str) -> str:
    s = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    s = re.sub(r"<details>.*?</details>", " ", s, flags=re.S)
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    s = re.sub(r"<code>.*?</code>", " ", s, flags=re.S)
    s = re.sub(r"<img[^>]*>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\\([.\-*_#\[\]()])", r"\1", s)
    s = re.sub(r"\*\*|__|`", "", s)
    # Single-character emphasis only around words, so identifiers_with_underscores survive.
    s = re.sub(r"(?<!\w)[*_](\S(?:.*?\S)?)[*_](?!\w)", r"\1", s)
    s = re.sub(r"(?m)^[ \t]*(?:&gt;|>)[ \t]?", "", s)
    return " ".join(html.unescape(s).split())


def _shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit]
    end = cut.rfind(". ")
    if end > limit // 2:
        return cut[: end + 1]
    return cut[: limit - 1].rstrip(" .;,") + "…"


def split_findings(body: str) -> list[str]:
    body = body or ""
    fences = [m.span() for m in re.finditer(r"```.*?(?:```|\Z)", body, flags=re.S)]
    starts = [m.start() for m in FINDING_START.finditer(body)
              if not any(a <= m.start() < b for a, b in fences)]
    return [body[a:b] for a, b in zip(starts, starts[1:] + [len(body)])]


def is_resolved(raw: str) -> bool:
    first = raw.strip().splitlines()[0] if raw.strip() else ""
    return "✓ Resolved" in raw[:500] or "<s>" in first


def title_of(raw: str) -> str:
    lines = raw.strip().splitlines()
    for line in lines[:6]:
        if FINDING_START.match(line):
            head = re.sub(r"^[ \t]*(?:<summary>[ \t]*)?\d+\\?\.[ \t]+", "", line)
            return _shorten(clean(head.split("<code>")[0]), MAX_TITLE_CHARS)
    body = re.sub(r"<details>.*?</details>", " ", raw, flags=re.S)
    bold = [m.group(1).strip() for m in re.finditer(r"(?m)^\*\*(.+?)\*\*\s*$", body)]
    titled = [b for b in bold if b.endswith(".")] or bold
    if titled:
        return _shorten(clean(titled[0]), MAX_TITLE_CHARS)
    for line in lines:
        text = clean(line)
        if len(text) > 3:
            return _shorten(text, MAX_TITLE_CHARS)
    return ""


def detail_of(raw: str, title: str) -> str:
    pre = re.search(r"<pre>(.*?)</pre>", raw, flags=re.S)
    if pre:
        return _shorten(clean(pre.group(1)), MAX_DETAIL_CHARS)
    body = re.sub(r"<details>.*?</details>", " ", raw, flags=re.S)
    for para in re.split(r"\n\s*\n", body):
        text = clean(para)
        if (len(text) > 40 and text != title and not para.lstrip().startswith(("**", "_", "<img"))):
            return _shorten(text, MAX_DETAIL_CHARS)
    return ""


def _column(header, rows, name) -> set[str]:
    idx = [i for i, h in enumerate(header) if h == name]
    return {r[i].strip() for r in rows for i in idx if i < len(r) and r[i].strip()}


def check_finding(title: str, sdrf_text: str) -> str | None:
    """Return why the data confirms a finding, or None when it is not checked or not confirmed.

    Only two recurring issue types are checked, recognised from the finding's title, and only
    confirmations are reported: a rule that finds nothing says nothing, so a correct finding is
    never marked as wrong.
    """
    header, rows = parse_table(sdrf_text)
    title = title.lower()
    if TEMPLATE_CLAIM.search(title) and ORGANISM_KIND.search(title):
        templates = {re.sub(r"^nt=|;.*$", "", t.lower()) for t in _column(header, rows, "comment[sdrf template]")}
        organisms = {o.lower() for o in _column(header, rows, "characteristics[organism]")}
        genera = {o.split()[0] for o in organisms}
        if (("human" in templates and organisms - {"homo sapiens"})
                or ({"invertebrates", "vertebrates"} & templates and genera & NON_ANIMAL_GENERA)
                or ("vertebrates" in templates and "homo sapiens" in organisms)):
            return "organism does not fit the declared template"
    if FILE_CLAIM.search(title) and RUN_WORDS.search(title):
        bad = sorted(f for f in _column(header, rows, "comment[data file]") if not ACQUISITION.search(f.lower()))
        if bad:
            return "non-acquisition data files: " + ", ".join(bad[:3])
    return None


def _paged(gh, path: str):
    sep = "&" if "?" in path else "?"
    for page in range(1, 11):
        items = gh.request("GET", f"{path}{sep}per_page=100&page={page}") or []
        yield from items
        if len(items) < 100:
            return


def _confirming_terms(ds: dict) -> dict[str, str]:
    """Words a reviewer would use for what this report flagged, mapped to what was flagged."""
    terms: dict[str, str] = {}
    for c in ds.get("changes") or []:
        if c.get("risk") in ("medium", "high"):
            col = str(c.get("column", ""))
            inner = re.sub(r"^[a-z ]+\[(.*)\]$", r"\1", col)
            terms[inner.lower()] = col
    for f in ds.get("findings") or []:
        msg = str(f.get("message", ""))
        m = re.match(r"Column (?:removed|added): (.+)$", msg)
        if m:
            terms[re.sub(r"^[a-z ]+\[(.*)\]$", r"\1", m.group(1)).lower()] = m.group(1)
        elif "deleted" in msg.lower():
            terms["delet"] = msg
        elif "rows removed" in msg or "data files" in msg:
            terms["removed"] = msg
        elif msg.startswith("Label set changed"):
            terms["label"] = "comment[label]"
    for key in (ds.get("quality") or {}).get("defects_head") or {}:
        terms[str(key).replace("_", " ")] = str(key)
    return {t: v for t, v in terms.items() if len(t) >= 4}


def collect_notes(gh, repo: str, pr_number: int, report: dict,
                  reviewers=REVIEWERS, read_file=None) -> dict[str, list[dict]]:
    datasets = {d["id"]: d for d in report["datasets"] if isinstance(d.get("id"), str)}
    path_ids = {d.get("path"): d["id"] for d in datasets.values()}
    # (reviewer, url, finding text, text searched for accessions, datasets fixed by file path)
    items = []
    for c in _paged(gh, f"/repos/{repo}/issues/{pr_number}/comments"):
        if (c.get("user") or {}).get("login") in reviewers:
            items += [(c["user"]["login"], c.get("html_url"), unit, unit, set())
                      for unit in split_findings(c.get("body") or "")]
    for r in _paged(gh, f"/repos/{repo}/pulls/{pr_number}/reviews"):
        if (r.get("user") or {}).get("login") in reviewers:
            items += [(r["user"]["login"], r.get("html_url"), unit, unit, set())
                      for unit in split_findings(r.get("body") or "")]
    for rc in _paged(gh, f"/repos/{repo}/pulls/{pr_number}/comments"):
        if (rc.get("user") or {}).get("login") not in reviewers:
            continue
        path = rc.get("path") or ""
        m = DATASET_PATH.match(path)
        forced = {path_ids[path]} if path in path_ids else ({m.group(1)} if m else set())
        body = rc.get("body") or ""
        # Inline comments collapse tool output into <details>; accessions there are noise.
        visible = re.sub(r"<details>.*?</details>", " ", body, flags=re.S)
        items.append((rc["user"]["login"], rc.get("html_url"), body, visible, forced))

    def key_of(raw: str) -> str:
        return re.sub(r"\W+", " ", title_of(raw).lower()).strip()[:80]

    # Bots mark a finding resolved in their summary but often leave the inline copy untouched.
    resolved = {(login, key_of(raw)) for login, _, raw, _, _ in items if raw.strip() and is_resolved(raw)}
    notes: dict[str, list[dict]] = {}
    for login, url, raw, searched, forced in items:
        if not raw.strip() or is_resolved(raw) or (login, key_of(raw)) in resolved:
            continue
        mentioned = {i for i in datasets
                     if re.search(rf"(?<![A-Za-z0-9]){re.escape(i)}(?![0-9])", searched)}
        targets = sorted((forced | mentioned) & set(datasets))
        if not targets:
            continue
        title = title_of(raw)
        detail = detail_of(raw, title)
        key = key_of(raw)
        for target in targets:
            bucket = notes.setdefault(target, [])
            if len(bucket) >= MAX_NOTES_PER_DATASET or any(n["key"] == key for n in bucket):
                continue
            text = f"{title} {detail}".lower()
            confirmed = sorted({flag for term, flag in _confirming_terms(datasets[target]).items()
                                if term in text})
            sdrf_text = read_file(datasets[target].get("path")) if read_file else None
            bucket.append({"reviewer": login, "url": url, "title": title, "detail": detail,
                           "confirmed_by": confirmed, "key": key,
                           "data_check": check_finding(title, sdrf_text) if sdrf_text else None})
    for bucket in notes.values():
        for n in bucket:
            n.pop("key")
    return notes
