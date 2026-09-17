#!/usr/bin/env python3
"""Build an advisory change report for the SDRF files a pull request touches.

For every added, modified or deleted datasets/**/*.sdrf(.tsv) file this compares the PR
version with the base-branch copy *semantically*: rows are matched by data file, label and
fraction; identical value transitions are grouped across rows; replaced ontology terms are
related through OLS (refinement, generalisation, sibling, unrelated); and every change gets a
risk level. The quality delta reuses the review gate's checks on both versions.

Usage:
  sdrf_change_report.py --name-status FILE --base-dir DIR --out FILE
                        --pr N --head-sha SHA --base-sha SHA [--no-ols]

--name-status is `git diff --name-status --no-renames` output; --base-dir holds base-branch
copies of modified and deleted files at their repository paths. No output file is written when
the PR touches no dataset SDRF.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path
from urllib.parse import quote, urlencode

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdrf_review as gate  # noqa: E402

SCHEMA_VERSION = 1
SENTINELS = {"", "not available", "not applicable"}
KEY_COLUMNS = ("comment[data file]", "comment[label]", "comment[fraction identifier]")
SDRF_PATH = re.compile(r"^datasets/.+\.sdrf(\.tsv)?$")
STATUS = {"A": "new", "M": "modified", "D": "deleted"}
RANK = {"low": 1, "medium": 2, "high": 3}

# Ordered by review priority: when the lookup budget runs out, later columns go unresolved.
ONTOLOGY_COLUMNS = {
    "characteristics[organism]": ("ncbitaxon",),
    "characteristics[organism part]": ("uberon", "bto"),
    "characteristics[disease]": ("mondo", "efo", "doid", "ncit"),
    "characteristics[cell type]": ("cl", "bto", "clo"),
    "characteristics[cell line]": ("clo", "bto", "efo"),
    "characteristics[developmental stage]": ("efo", "hsapdv", "mmusdv"),
    "comment[instrument]": ("ms",),
    "comment[cleavage agent details]": ("ms",),
    "comment[modification parameters]": ("unimod", "mod"),
}
SAMPLE_COLUMNS = {
    "characteristics[organism part]",
    "characteristics[disease]",
    "characteristics[cell type]",
    "characteristics[cell line]",
    "characteristics[developmental stage]",
}
OLS_BASE = "https://www.ebi.ac.uk/ols4/api"


# ---------------------------------------------------------------- semantic diff


def parse_table(text: str) -> tuple[list[str], list[list[str]]]:
    lines = text.splitlines()
    if not lines or not lines[0].strip():
        return [], []
    header = [h.strip().lower() for h in lines[0].split("\t")]
    rows = [ln.split("\t") for ln in lines[1:] if ln.strip()]
    return header, rows


def _column_index(header: list[str]) -> dict[str, list[int]]:
    cols: dict[str, list[int]] = {}
    for i, name in enumerate(header):
        cols.setdefault(name, []).append(i)
    return cols


def _cell(row: list[str], i: int) -> str:
    return row[i].strip() if i < len(row) else ""


def _values(row: list[str], idxs: list[int], multi: bool) -> tuple[str, ...]:
    # Repeated columns (modification parameters, ...) are one set per row: order is meaningless.
    if multi:
        return tuple(sorted({_cell(row, i) for i in idxs} - {""}))
    return (_cell(row, idxs[0]),)


def _display(values: tuple[str, ...]) -> str:
    return " | ".join(values)


def _norm(value: str):
    s = " ".join(value.strip().lower().split())
    if "=" in s:
        parts = {}
        for p in s.split(";"):
            if "=" in p:
                k, v = p.split("=", 1)
                parts[k.strip()] = v.strip()
        if "nt" in parts:
            return ("kv", parts["nt"], parts.get("ac"))
    return ("s", s)


def _equivalent(a: str, b: str) -> bool:
    na, nb = _norm(a), _norm(b)
    if na == nb:
        return True
    if na[0] == "kv" and nb[0] == "kv":
        return na[1] == nb[1] and (na[2] is None or nb[2] is None or na[2] == nb[2])
    return False


def _is_empty(values: tuple[str, ...]) -> bool:
    return all(v.strip().lower() in SENTINELS for v in values)


def _kind(old: tuple[str, ...], new: tuple[str, ...]) -> str | None:
    if old == new:
        return None
    if _is_empty(old) and _is_empty(new):
        return "format"
    if _is_empty(old):
        return "filled"
    if _is_empty(new):
        return "emptied"
    if len(old) == len(new) and all(_equivalent(a, b) for a, b in zip(old, new)):
        return "format"
    return "replaced"


def _canon(value: str) -> str:
    n = _norm(value)
    return n[1]


def _file_stem(name: str) -> str:
    # A peak list swapped for its vendor RAW (x.mzML -> x.raw) is the same run, not a new row.
    base = name.strip().replace("\\", "/").rsplit("/", 1)[-1].lower()
    base = re.sub(r"\.(gz|bz2|zip|xz)$", "", base)
    return re.sub(r"\.[a-z0-9]+$", "", base)


def _coordinates(rows, cols, key_columns):
    coords = []
    for r in rows:
        c = []
        for name in key_columns:
            v = _display(_values(r, cols[name], len(cols[name]) > 1))
            c.append(_file_stem(v) if name == "comment[data file]" else _canon(v))
        coords.append(tuple(c))
    return coords


def _match_rows(old_rows, old_c, new_rows, new_c) -> list[tuple[int, int]]:
    """Pair old and new rows. Returns (old index, new index) pairs.

    Pass 1 pairs rows with the same data file stem, fraction and label. Pass 2 pairs the
    leftovers by data file stem and fraction alone, in file order, so a corrected label shows
    up as a value change on the same row instead of a removed row plus an added one.
    """
    key_columns = [c for c in KEY_COLUMNS if c in old_c and c in new_c]
    if "comment[data file]" not in key_columns:
        key_columns = ["source name"] if "source name" in old_c and "source name" in new_c else []
    if not key_columns:
        return [(i, i) for i in range(min(len(old_rows), len(new_rows)))]
    old_k = _coordinates(old_rows, old_c, key_columns)
    new_k = _coordinates(new_rows, new_c, key_columns)
    label_pos = key_columns.index("comment[label]") if "comment[label]" in key_columns else None

    pairs: list[tuple[int, int]] = []
    free_old = set(range(len(old_rows)))
    free_new = set(range(len(new_rows)))
    passes = [lambda k: k]
    if label_pos is not None:
        passes.append(lambda k: k[:label_pos] + k[label_pos + 1:])
    for project in passes:
        pool: dict[tuple, list[int]] = {}
        for i in sorted(free_old):
            pool.setdefault(project(old_k[i]), []).append(i)
        for j in sorted(free_new):
            bucket = pool.get(project(new_k[j]))
            if bucket:
                i = bucket.pop(0)
                pairs.append((i, j))
                free_old.discard(i)
                free_new.discard(j)
    return sorted(pairs)


def _term_name(value: str) -> str:
    for part in value.split(";"):
        if part.strip().upper().startswith("NT="):
            return " ".join(part.split("=", 1)[1].split())
    return " ".join(value.split())


def _column_set(rows, cols, name) -> list[str]:
    if name not in cols:
        return []
    names: dict[str, str] = {}
    for r in rows:
        for v in _values(r, cols[name], True):
            names.setdefault(_canon(v), _term_name(v))
    return sorted(names.values())


def _removed_files(old_rows, old_c, new_rows, new_c) -> list[str]:
    name = "comment[data file]"
    if name not in old_c:
        return []
    old_files = {v for r in old_rows for v in _values(r, old_c[name], True)}
    new_stems = ({_file_stem(v) for r in new_rows for v in _values(r, new_c[name], True)}
                 if name in new_c else set())
    return sorted(f for f in old_files if _file_stem(f) not in new_stems)


def diff_tables(old_text: str, new_text: str) -> dict:
    old_h, old_rows = parse_table(old_text)
    new_h, new_rows = parse_table(new_text)
    if not old_h or not new_h:
        raise ValueError("SDRF file has no header")
    old_c, new_c = _column_index(old_h), _column_index(new_h)

    matched = _match_rows(old_rows, old_c, new_rows, new_c)

    result = {
        "rows": {"old": len(old_rows), "new": len(new_rows),
                 "added": len(new_rows) - len(matched), "removed": len(old_rows) - len(matched)},
        "columns": {"added": [c for c in new_c if c not in old_c],
                    "removed": [c for c in old_c if c not in new_c]},
        "restructured": False,
        "changes": [],
        "removed_data_files": _removed_files(old_rows, old_c, new_rows, new_c),
        "labels": {"old": _column_set(old_rows, old_c, "comment[label]"),
                   "new": _column_set(new_rows, new_c, "comment[label]")},
    }
    biggest = max(len(old_rows), len(new_rows))
    if biggest and len(matched) < biggest / 2:
        result["restructured"] = True
        return result

    groups: Counter = Counter()
    for name in new_c:
        if name not in old_c:
            continue
        multi = len(old_c[name]) > 1 or len(new_c[name]) > 1
        for i, j in matched:
            old_v = _values(old_rows[i], old_c[name], multi)
            new_v = _values(new_rows[j], new_c[name], multi)
            kind = _kind(old_v, new_v)
            if kind:
                groups[(name, _display(old_v), _display(new_v), kind)] += 1

    order = {name: i for i, name in enumerate(new_c)}
    for (name, old_s, new_s, kind), n in sorted(groups.items(),
                                                key=lambda kv: (order[kv[0][0]], -kv[1])):
        result["changes"].append({"column": name, "old": old_s, "new": new_s, "rows": n,
                                  "total_rows": len(matched), "kind": kind})
    return result


# ---------------------------------------------------------------- ontology relations


class OlsResolver:
    """Relate an old and a new ontology value through the OLS4 hierarchy.

    Every failure degrades to "unknown": the report must never fail because OLS is slow or down.
    """

    def __init__(self, fetch=None, base: str = OLS_BASE, timeout: float = 10.0, budget: int = 50):
        self._fetch = fetch or self._http
        self.base = base
        self.timeout = timeout
        self.budget = budget

    def _http(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.load(resp)

    def _resolve(self, value: str, ontologies: tuple[str, ...]) -> dict | None:
        fields = {}
        for part in value.split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                fields[k.strip().upper()] = v.strip()
        accession = fields.get("AC")
        label = fields.get("NT", value).strip()
        if accession:
            params = {"q": accession, "queryFields": "obo_id", "exact": "true"}
        else:
            params = {"q": label, "ontology": ",".join(ontologies), "queryFields": "label",
                      "exact": "true"}
        params.update({"rows": "25", "fieldList": "iri,label,obo_id,ontology_name,is_defining_ontology"})
        docs = self._fetch(f"{self.base}/search?{urlencode(params)}").get("response", {}).get("docs", [])
        hits = []
        for d in docs:
            if accession:
                ok = str(d.get("obo_id", "")).lower() == accession.lower()
            else:
                ok = (str(d.get("label", "")).lower() == label.lower()
                      and d.get("ontology_name") in ontologies)
            if ok and d.get("obo_id") and d.get("iri"):
                hits.append(d)
        if not hits:
            return None
        hits.sort(key=lambda d: not d.get("is_defining_ontology"))
        h = hits[0]
        return {"obo_id": h["obo_id"].lower(), "iri": h["iri"], "ontology": h["ontology_name"]}

    def _hierarchy(self, term: dict, kind: str) -> set[str]:
        iri = quote(quote(term["iri"], safe=""), safe="")
        url = f"{self.base}/ontologies/{term['ontology']}/terms/{iri}/{kind}?size=1000"
        terms = self._fetch(url).get("_embedded", {}).get("terms", [])
        return {str(t.get("obo_id", "")).lower() for t in terms if t.get("obo_id")}

    def relation(self, column: str, old: str, new: str) -> str | None:
        ontologies = ONTOLOGY_COLUMNS.get(column)
        if not ontologies:
            return None
        if self.budget <= 0:
            return "unknown"
        self.budget -= 1
        try:
            a = self._resolve(old, ontologies)
            b = self._resolve(new, ontologies)
            if not a or not b:
                return "unknown"
            if a["obo_id"] == b["obo_id"]:
                return "same"
            if a["ontology"] != b["ontology"]:
                return "unknown"
            if a["obo_id"] in self._hierarchy(b, "hierarchicalAncestors"):
                return "refinement"
            if b["obo_id"] in self._hierarchy(a, "hierarchicalAncestors"):
                return "generalisation"
            if self._hierarchy(a, "hierarchicalParents") & self._hierarchy(b, "hierarchicalParents"):
                return "sibling"
            return "unrelated"
        except Exception as exc:  # network, HTTP and payload errors all mean "unverifiable"
            print(f"OLS lookup failed for {column}: {exc}", file=sys.stderr)
            return "unknown"


def annotate_relations(changes: list[dict], resolver: OlsResolver | None) -> None:
    priority = list(ONTOLOGY_COLUMNS)
    candidates = [c for c in changes if c["kind"] == "replaced" and c["column"] in ONTOLOGY_COLUMNS]
    candidates.sort(key=lambda c: priority.index(c["column"]))
    cache: dict[tuple, str] = {}
    for c in candidates:
        key = (c["column"], c["old"], c["new"])
        if key not in cache:
            cache[key] = (resolver.relation(*key) if resolver else None) or "unknown"
        c["relation"] = cache[key]
        if cache[key] == "same":
            c["kind"] = "format"


# ---------------------------------------------------------------- risk


def _change_risk(c: dict) -> str:
    column, kind, relation = c["column"], c["kind"], c.get("relation")
    if kind in ("format", "filled"):
        return "low"
    if kind == "emptied":
        return "medium"
    if column == "characteristics[organism]":
        return "low" if relation == "refinement" else "high"
    if column == "comment[label]":
        return "high"
    if column in SAMPLE_COLUMNS:
        return "low" if relation == "refinement" else "medium"
    return "medium"


def classify(ds: dict) -> None:
    if ds["status"] == "new":
        ds["risk"] = None
        return
    findings = []
    if ds["status"] == "deleted":
        findings.append({"message": "Dataset deleted", "risk": "high"})
    elif ds.get("error"):
        findings.append({"message": "File could not be analysed", "risk": "high"})
    else:
        rows = ds.get("rows") or {}
        if ds.get("restructured"):
            findings.append({"message": "Table restructured: fewer than half of the rows could "
                                        "be matched to the base version", "risk": "high"})
        if rows.get("removed"):
            findings.append({"message": f"{rows['removed']} rows removed", "risk": "high"})
        if ds.get("removed_data_files"):
            findings.append({"message": f"{len(ds['removed_data_files'])} data files no longer "
                                        "referenced", "risk": "high"})
        labels = ds.get("labels") or {}
        if (labels.get("old") and labels.get("new")
                and {x.lower() for x in labels["old"]} != {x.lower() for x in labels["new"]}):
            findings.append({"message": "Label set changed: " + ", ".join(labels["old"])
                             + " → " + ", ".join(labels["new"]), "risk": "high"})
        for name in (ds.get("columns") or {}).get("removed", []):
            risk = "high" if name.startswith("factor value[") else "medium"
            findings.append({"message": f"Column removed: {name}", "risk": risk})
        for name in (ds.get("columns") or {}).get("added", []):
            findings.append({"message": f"Column added: {name}", "risk": "low"})
        if rows.get("added"):
            findings.append({"message": f"{rows['added']} rows added", "risk": "low"})
    for c in ds.get("changes", []):
        c["risk"] = _change_risk(c)
    ds.get("changes", []).sort(key=lambda c: (-RANK[c["risk"]], -c["rows"]))
    ds["findings"] = findings
    levels = [f["risk"] for f in findings] + [c["risk"] for c in ds.get("changes", [])]
    ds["risk"] = max(levels, key=RANK.__getitem__) if levels else "low"


# ---------------------------------------------------------------- quality delta


def default_parse(path):
    return gate.parse_sdrf_ok(path)


def _defects(path: Path) -> dict[str, int]:
    ragged, collisions = gate.structural_check(path)
    found = {"ragged_rows": ragged, "coordinate_collisions": collisions}
    found.update(gate.content_check(path))
    return {k: v for k, v in found.items() if v}


def _parse_status(path: Path, parse_fn) -> str:
    try:
        ok, _ = parse_fn(path)
    except Exception as exc:  # parse_sdrf missing or crashing is reported, not fatal
        print(f"parse_sdrf failed on {path}: {exc}", file=sys.stderr)
        return "error"
    return "pass" if ok else "fail"


def quality_delta(head: Path | None, base: Path | None, parse_fn=None,
                  run_parse: bool = True) -> dict:
    parse_fn = parse_fn or default_parse
    head_d = _defects(head) if head else {}
    base_d = _defects(base) if base else {}
    q = {"fixed": 0, "introduced": 0, "defects_head": head_d,
         "parse_sdrf": {"base": None, "head": None}}
    if head and run_parse:
        q["parse_sdrf"]["head"] = _parse_status(head, parse_fn)
    if head and base:
        if run_parse:
            q["parse_sdrf"]["base"] = _parse_status(base, parse_fn)
        keys = set(head_d) | set(base_d)
        q["fixed"] = sum(max(0, base_d.get(k, 0) - head_d.get(k, 0)) for k in keys)
        q["introduced"] = sum(max(0, head_d.get(k, 0) - base_d.get(k, 0)) for k in keys)
    return q


# ---------------------------------------------------------------- report


def read_name_status(text: str) -> list[tuple[str, str]]:
    entries = []
    for line in text.splitlines():
        parts = line.split("\t")
        if len(parts) == 2 and parts[0] in STATUS and SDRF_PATH.match(parts[1]):
            entries.append((STATUS[parts[0]], parts[1]))
    return entries


def build_dataset(status: str, path: str, base_dir: Path, resolver) -> dict:
    ds = {"id": Path(path).parent.name, "path": path, "status": status,
          "restructured": False, "rows": {"old": None, "new": None, "added": 0, "removed": 0},
          "columns": {"added": [], "removed": []}, "changes": [], "quality": None}
    head = Path(path) if status != "deleted" else None
    base = base_dir / path if status != "new" else None
    try:
        if status == "modified":
            ds.update(diff_tables(base.read_text(encoding="utf-8", errors="replace"),
                                  head.read_text(encoding="utf-8", errors="replace")))
            annotate_relations(ds["changes"], resolver)
        else:
            source = head or base
            header, rows = parse_table(source.read_text(encoding="utf-8", errors="replace"))
            if not header:
                raise ValueError("SDRF file has no header")
            ds["rows"]["new" if status == "new" else "old"] = len(rows)
        if head:
            # New files are already validated by the SDRF review gate; running parse_sdrf again
            # doubles CI time on large batch PRs. Only the before/after comparison is new here.
            ds["quality"] = quality_delta(head, base, run_parse=status == "modified")
    except Exception as exc:
        ds["error"] = f"{type(exc).__name__}: {exc}"
    classify(ds)
    return ds


def build_report(entries, base_dir: Path, pr_number: int, head_sha: str, base_sha: str,
                 resolver) -> dict:
    datasets = [build_dataset(status, path, base_dir, resolver) for status, path in entries]
    risks = [d["risk"] for d in datasets if d["risk"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "pr_number": pr_number,
        "head_sha": head_sha,
        "base_sha": base_sha,
        "summary": {
            "new": sum(d["status"] == "new" for d in datasets),
            "modified": sum(d["status"] == "modified" for d in datasets),
            "deleted": sum(d["status"] == "deleted" for d in datasets),
            "risk": max(risks, key=RANK.__getitem__) if risks else None,
        },
        "datasets": datasets,
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name-status", required=True)
    ap.add_argument("--base-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--head-sha", required=True)
    ap.add_argument("--base-sha", required=True)
    ap.add_argument("--no-ols", action="store_true", help="skip ontology relation lookups")
    args = ap.parse_args(argv)

    entries = read_name_status(Path(args.name_status).read_text(encoding="utf-8"))
    if not entries:
        print("No dataset SDRF changes; no report written.")
        return 0
    resolver = None if args.no_ols else OlsResolver()
    report = build_report(entries, Path(args.base_dir), args.pr, args.head_sha, args.base_sha,
                          resolver)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    s = report["summary"]
    print(f"Report written to {out}: {s['new']} new, {s['modified']} modified, "
          f"{s['deleted']} deleted, highest risk {s['risk']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
