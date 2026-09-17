#!/usr/bin/env python3
"""Render an SDRF change report (report.json) as a GitHub PR comment.

Every string in the report derives from files in an untrusted pull request, and external
reviewer notes quote bot comments, so all of it is escaped: no raw HTML, no links except to
comments in this repository, no @-mentions. Numeric fields are rendered only if they are
integers.

Usage: sdrf_change_render.py report.json > comment.md
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "<!-- sdrf-change-report -->"
MAX_CHARS = 60000
MAX_GROUPS = 30
MAX_NOTES = 60
RANK = {"low": 1, "medium": 2, "high": 3}
STATUSES = {"new", "modified", "deleted"}
KIND_NOTE = {"format": " (format only)", "filled": " (value filled in)",
             "emptied": " (value removed)", "replaced": "",
             "renamed": " (identifiers renamed; first example shown)"}
COMMENT_URL = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+/pull/\d+#[\w-]+$")


def validate_report(obj):
    if not isinstance(obj, dict) or obj.get("schema_version") != 1:
        raise ValueError("unsupported report schema")
    pr = obj.get("pr_number")
    if isinstance(pr, bool) or not isinstance(pr, int) or pr <= 0:
        raise ValueError("pr_number must be a positive integer")
    if not isinstance(obj.get("datasets"), list) or not isinstance(obj.get("summary"), dict):
        raise ValueError("report must contain a datasets list and a summary")
    if not isinstance(obj.get("head_sha"), str):
        raise ValueError("head_sha must be a string")
    for ds in obj["datasets"]:
        if (not isinstance(ds, dict) or not isinstance(ds.get("id"), str)
                or ds.get("status") not in STATUSES):
            raise ValueError("each dataset needs a string id and a known status")
        for key in ("changes", "findings"):
            if not isinstance(ds.get(key, []), list) or not all(isinstance(x, dict) for x in ds.get(key, [])):
                raise ValueError(f"dataset {key} must be a list of objects")
    return obj


def escape(text, limit: int = 120) -> str:
    s = " ".join(str(text).split())
    if len(s) > limit:
        s = s[: limit - 1] + "…"
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"([\\|`*_\[\]])", r"\\\1", s)
    return s.replace("@", "@​")


def _num(value) -> str:
    return str(value) if isinstance(value, int) and not isinstance(value, bool) else "-"


def _rank(ds) -> int:
    return RANK.get(ds.get("risk") if isinstance(ds.get("risk"), str) else "", 0)


def _label(ds) -> str:
    name = Path(str(ds.get("path") or "")).name
    default = {f"{ds['id']}.sdrf.tsv", f"{ds['id']}.sdrf"}
    return escape(ds["id"], 60) + ("" if not name or name in default else f" ({escape(name, 80)})")


def _rows(ds) -> str:
    rows = ds.get("rows") if isinstance(ds.get("rows"), dict) else {}
    return f"{_num(rows.get('old'))} → {_num(rows.get('new'))}"


def _quality(q) -> str:
    if not isinstance(q, dict):
        return "-"
    ps = q.get("parse_sdrf") if isinstance(q.get("parse_sdrf"), dict) else {}
    parse = f"{ps['base']} → {ps.get('head')}" if ps.get("base") else str(ps.get("head") or "-")
    return (f"{_num(q.get('fixed'))} fixed / {_num(q.get('introduced'))} introduced; "
            f"parse\\_sdrf {escape(parse, 30)}")


def _value(v) -> str:
    return escape(v) if str(v).strip() else "(empty)"


def _dataset_block(ds) -> str:
    risk = ds.get("risk") or "-"
    lines = [f"<details{' open' if ds.get('risk') == 'high' else ''}>",
             f"<summary><b>{_label(ds)}</b> · {escape(ds['status'], 20)} · risk {escape(risk, 10)}</summary>",
             ""]
    if ds.get("error"):
        lines.append(f"- Could not analyse this file: {escape(ds['error'], 200)}")
    for f in ds.get("findings", []):
        lines.append(f"- **{escape(f.get('risk', '-'), 10)}** · {escape(f.get('message', ''), 300)}")
    changes = ds.get("changes", [])
    for c in changes[:MAX_GROUPS]:
        rel = f" \\[{escape(c['relation'], 20)}\\]" if c.get("relation") else ""
        lines.append(
            f"- **{escape(c.get('risk', '-'), 10)}** · {escape(c.get('column', ''))}: "
            f"{_value(c.get('old', ''))} → {_value(c.get('new', ''))} "
            f"({_num(c.get('rows'))}/{_num(c.get('total_rows'))} rows){rel}"
            f"{KIND_NOTE.get(c.get('kind'), '')}")
    if len(changes) > MAX_GROUPS:
        lines.append(f"- … and {len(changes) - MAX_GROUPS} more change groups")
    if not ds.get("findings") and not changes and not ds.get("error"):
        lines.append("- No semantic changes detected (whitespace or ordering only).")
    if ds.get("summary"):
        lines += ["", "**AI-generated summary. Verify against the diff above.**", "",
                  f"> {escape(ds['summary'], 700)}"]
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def _new_block(new) -> str:
    if not new:
        return ""
    lines = ["<details>", f"<summary>New datasets ({len(new)})</summary>", "",
             "parse\\_sdrf validation of new datasets is reported by the SDRF review gate check.", "",
             "| Dataset | Rows | Defects |", "|---|---|---|"]
    for ds in new:
        q = ds.get("quality") if isinstance(ds.get("quality"), dict) else {}
        found = q.get("defects_head") if isinstance(q.get("defects_head"), dict) else {}
        defects = ", ".join(f"{escape(k, 60)}: {_num(v)}" for k, v in sorted(found.items()))
        rows = ds.get("rows") if isinstance(ds.get("rows"), dict) else {}
        if ds.get("error"):
            defects = f"could not analyse: {escape(ds['error'], 120)}"
        lines.append(f"| {_label(ds)} | {_num(rows.get('new'))} | {defects or 'none'} |")
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def _notes_block(datasets, external) -> str:
    if not external:
        return ""
    # One line per finding, listing every dataset it concerns (bots often name several).
    grouped: dict[tuple, dict] = {}
    for ds in datasets:
        for note in external.get(ds["id"]) or []:
            key = (note.get("reviewer"), note.get("title"), note.get("detail"), note.get("url"))
            entry = grouped.setdefault(key, {"note": note, "ids": [], "confirmed": []})
            entry["ids"].append(ds["id"])
            entry["confirmed"] += [(ds["id"], c) for c in note.get("confirmed_by") or []]
    lines = []
    for entry in list(grouped.values())[:MAX_NOTES]:
        note, ids = entry["note"], entry["ids"]
        shown = ", ".join(escape(i, 60) for i in ids[:8]) + (f" and {len(ids) - 8} more" if len(ids) > 8 else "")
        text = escape(note.get("title", ""), 120)
        detail = str(note.get("detail") or "")
        if detail:
            text += (". " if not text.endswith((".", "…", "!", "?")) else " ") + escape(detail, 260)
        url = str(note.get("url") or "")
        link = f" ([source]({url}))" if COMMENT_URL.match(url) else ""
        confirmed = entry["confirmed"]
        if confirmed and len(ids) == 1:
            also = " · also flagged by this report: " + ", ".join(escape(c, 60) for _, c in confirmed)
        elif confirmed:
            also = " · also flagged by this report: " + ", ".join(
                f"{escape(c, 60)} ({escape(i, 60)})" for i, c in confirmed)
        else:
            also = ""
        lines.append(f"- **{shown}** · {escape(note.get('reviewer', ''), 60)}: {text}{link}{also}")
    if not lines:
        return ""
    return "\n".join(["#### External reviewer notes", "",
                      "Quoted from AI review bots on this PR. Not verified by this report unless "
                      "marked as also flagged.", ""] + lines + [""])


def render(report: dict, max_chars: int = MAX_CHARS, external: dict | None = None) -> str:
    s = report["summary"]
    datasets = report["datasets"]
    changed = sorted((d for d in datasets if d["status"] in ("modified", "deleted")),
                     key=lambda d: (-_rank(d), d["id"]))
    new = [d for d in datasets if d["status"] == "new"]
    head = [MARKER, "### SDRF change report", "",
            f"{_num(s.get('new'))} new · {_num(s.get('modified'))} modified · "
            f"{_num(s.get('deleted'))} deleted · highest risk: {escape(s.get('risk') or 'none', 10)}", ""]
    if changed:
        head += ["Changes to datasets that already exist in the repository:", "",
                 "| Dataset | Change | Risk | Rows old → new | Quality |", "|---|---|---|---|---|"]
        head += [f"| {_label(d)} | {escape(d['status'], 20)} | {escape(d.get('risk') or '-', 10)} | "
                 f"{_rows(d)} | {_quality(d.get('quality'))} |" for d in changed]
        head.append("")
    notes = _notes_block(changed + new, external)
    blocks = [_dataset_block(d) for d in changed]
    new_block = _new_block(new)
    footer = (f"<sub>Advisory report built from {escape(str(report.get('head_sha', ''))[:12], 20)}. "
              "Risk labels do not block merging.</sub>\n")

    def assemble(kept, dropped):
        note = ""
        if dropped:
            note = (f"_{dropped} dataset details omitted for size (lowest risk first); "
                    "the workflow job summary has the full report._\n\n")
        return ("\n".join(head) + "\n" + (notes + "\n" if notes else "") + "".join(kept) + note
                + new_block + "\n" + footer)

    dropped = 0
    body = assemble(blocks, dropped)
    while len(body) > max_chars and blocks:
        blocks.pop()
        dropped += 1
        body = assemble(blocks, dropped)
    if len(body) > max_chars:
        body = body[: max_chars - 40] + "\n\n_… report truncated for size._\n"
    return body


def main(argv: list[str]) -> int:
    report = validate_report(json.loads(Path(argv[0]).read_text(encoding="utf-8")))
    sys.stdout.write(render(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
