#!/usr/bin/env python3
"""Render an SDRF change report (report.json) as a GitHub PR comment.

Every string in the report derives from files in an untrusted pull request, so all of it is
escaped: no raw HTML, no working links, no @-mentions.

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
RANK = {"low": 1, "medium": 2, "high": 3}
KIND_NOTE = {"format": " (format only)", "filled": " (value filled in)",
             "emptied": " (value removed)", "replaced": ""}


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
    return obj


def escape(text, limit: int = 120) -> str:
    s = " ".join(str(text).split())
    if len(s) > limit:
        s = s[: limit - 1] + "…"
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"([\\|`*_\[\]])", r"\\\1", s)
    return s.replace("@", "@​")


def _rank(ds) -> int:
    return RANK.get(ds.get("risk") or "", 0)


def _rows(ds) -> str:
    rows = ds.get("rows") or {}
    old, new = rows.get("old"), rows.get("new")
    return f"{'-' if old is None else old} → {'-' if new is None else new}"


def _quality(q) -> str:
    if not q:
        return "-"
    ps = q.get("parse_sdrf") or {}
    parse = f"{ps['base']} → {ps.get('head')}" if ps.get("base") else str(ps.get("head") or "-")
    return f"{q.get('fixed', 0)} fixed / {q.get('introduced', 0)} introduced; parse_sdrf {escape(parse)}"


def _value(v) -> str:
    return escape(v) if str(v).strip() else "(empty)"


def _dataset_block(ds) -> str:
    risk = ds.get("risk") or "-"
    lines = [f"<details{' open' if ds.get('risk') == 'high' else ''}>",
             f"<summary><b>{escape(ds['id'], 60)}</b> · {escape(ds['status'], 20)} · risk {escape(risk, 10)}</summary>",
             ""]
    if ds.get("error"):
        lines.append(f"- Could not analyse this file: {escape(ds['error'], 200)}")
    for f in ds.get("findings", []):
        lines.append(f"- **{escape(f['risk'], 10)}** · {escape(f['message'], 300)}")
    changes = ds.get("changes", [])
    for c in changes[:MAX_GROUPS]:
        rel = f" \\[{escape(c['relation'], 20)}\\]" if c.get("relation") else ""
        lines.append(
            f"- **{escape(c.get('risk', '-'), 10)}** · {escape(c['column'])}: {_value(c['old'])} → "
            f"{_value(c['new'])} ({c['rows']}/{c['total_rows']} rows){rel}"
            f"{KIND_NOTE.get(c['kind'], '')}")
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
             "| Dataset | Rows | parse_sdrf | Defects |", "|---|---|---|---|"]
    for ds in new:
        q = ds.get("quality") or {}
        defects = ", ".join(f"{escape(k, 60)}: {v}" for k, v in sorted((q.get("defects_head") or {}).items()))
        parse = (q.get("parse_sdrf") or {}).get("head") or "-"
        rows = (ds.get("rows") or {}).get("new")
        if ds.get("error"):
            defects = f"could not analyse: {escape(ds['error'], 120)}"
        lines.append(f"| {escape(ds['id'], 60)} | {'-' if rows is None else rows} | {escape(parse, 10)} | "
                     f"{defects or 'none'} |")
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def render(report: dict, max_chars: int = MAX_CHARS) -> str:
    s = report["summary"]
    datasets = report["datasets"]
    changed = sorted((d for d in datasets if d["status"] in ("modified", "deleted")),
                     key=lambda d: (-_rank(d), d["id"]))
    head = [MARKER, "### SDRF change report", "",
            f"{s.get('new', 0)} new · {s.get('modified', 0)} modified · {s.get('deleted', 0)} deleted"
            f" · highest risk: {escape(s.get('risk') or 'none', 10)}", ""]
    if changed:
        head += ["Changes to datasets that already exist in the repository:", "",
                 "| Dataset | Change | Risk | Rows old → new | Quality |", "|---|---|---|---|---|"]
        head += [f"| {escape(d['id'], 60)} | {escape(d['status'], 20)} | {escape(d.get('risk') or '-', 10)} | "
                 f"{_rows(d)} | {_quality(d.get('quality'))} |" for d in changed]
        head.append("")
    blocks = [_dataset_block(d) for d in changed]
    new_block = _new_block([d for d in datasets if d["status"] == "new"])
    footer = (f"<sub>Advisory report built from {escape(report.get('head_sha', '')[:12], 20)}. "
              "Risk labels do not block merging.</sub>\n")

    def assemble(kept, dropped):
        note = ""
        if dropped:
            note = (f"_{dropped} dataset details omitted for size (lowest risk first); "
                    "the workflow job summary has the full report._\n\n")
        return "\n".join(head) + "\n" + "".join(kept) + note + new_block + "\n" + footer

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
