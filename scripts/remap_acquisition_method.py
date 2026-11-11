#!/usr/bin/env python3
"""Remap comment[proteomics data acquisition method] to PRIDE:0000659 policy.

Rules (see issue #31 / design 2026-08-10):
- Wrong/foreign AC → map by recognized method to recommended PRIDE NT+AC
- Valid known AC with casing/order drift → normalize to NT=<lowercase>;AC=<accession>
- Plain free-text descendant labels → leave as-is (allowed; validator warns)
- Empty cells → leave and report

Usage:
    python scripts/remap_acquisition_method.py [--dry-run] [REPO_DIR]
"""

from __future__ import annotations

import argparse
import csv
import glob
import re
from collections import Counter
from pathlib import Path

COLUMN = "comment[proteomics data acquisition method]"

# Known valid descendants we normalize in place (AC -> lowercase NT label + AC).
KNOWN_TERMS: dict[str, tuple[str, str]] = {
    "pride:0000627": (
        "data-dependent acquisition",
        "NT=data-dependent acquisition;AC=PRIDE:0000627",
    ),
    "pride:0000450": (
        "data-independent acquisition",
        "NT=data-independent acquisition;AC=PRIDE:0000450",
    ),
    "pride:0000629": (
        "parallel reaction monitoring",
        "NT=parallel reaction monitoring;AC=PRIDE:0000629",
    ),
    "pride:0000630": (
        "selected reaction monitoring",
        "NT=selected reaction monitoring;AC=PRIDE:0000630",
    ),
    "pride:0000650": ("diapasef", "NT=diaPASEF;AC=PRIDE:0000650"),
    "pride:0000447": ("swath ms", "NT=SWATH MS;AC=PRIDE:0000447"),
}

METHOD_CANONICAL = {
    "DDA": "NT=data-dependent acquisition;AC=PRIDE:0000627",
    "DIA": "NT=data-independent acquisition;AC=PRIDE:0000450",
    "PRM": "NT=parallel reaction monitoring;AC=PRIDE:0000629",
    "SRM": "NT=selected reaction monitoring;AC=PRIDE:0000630",
    "diaPASEF": "NT=diaPASEF;AC=PRIDE:0000650",
    "SWATH": "NT=SWATH MS;AC=PRIDE:0000447",
}

DIA_FAMILY = {"DIA", "diaPASEF", "SWATH"}

_AC_RE = re.compile(r"AC=([A-Za-z]+:[0-9A-Za-z]+)", re.IGNORECASE)
_NT_RE = re.compile(r"NT=([^;]+)", re.IGNORECASE)


def methods_compatible(nt_method: str | None, ac_method: str | None) -> bool:
    if not nt_method or not ac_method:
        return False
    if nt_method == ac_method:
        return True
    return nt_method in DIA_FAMILY and ac_method in DIA_FAMILY


def classify_method(text: str) -> str | None:
    low = text.lower()
    if "diapasef" in low:
        return "diaPASEF"
    if "swath" in low:
        return "SWATH"
    if "independent" in low:
        return "DIA"
    if "dependent" in low:
        return "DDA"
    if "parallel reaction" in low or re.search(r"\bprm\b", low):
        return "PRM"
    if "selected reaction" in low or re.search(r"\bsrm\b", low):
        return "SRM"
    return None


def parse_cell(value: str) -> tuple[str | None, str | None, bool]:
    """Return (nt, ac, is_plain)."""
    raw = value.strip()
    if not raw:
        return None, None, False
    if "=" not in raw:
        return raw, None, True
    nt_m = _NT_RE.search(raw)
    ac_m = _AC_RE.search(raw)
    nt = nt_m.group(1).strip() if nt_m else None
    ac = ac_m.group(1).strip() if ac_m else None
    return nt, ac, False


def remap_value(value: str) -> tuple[str, str]:
    """Return (new_value, action)."""
    raw = value.strip()
    if not raw:
        return value, "empty"

    nt, ac, is_plain = parse_cell(raw)
    ac_key = ac.lower() if ac else None
    nt_method = classify_method(nt or "") if nt else None

    # Prefer a clear NT method when it disagrees with AC (DIA mis-accession bug).
    if nt_method and ac_key:
        # Generic DIA NT with any AC → always the DIA parent. Avoids keeping
        # accidental child ACs (e.g. PRIDE:0000650) from the row-varying AC bug.
        if nt and nt.lower() == "data-independent acquisition":
            canonical = METHOD_CANONICAL["DIA"]
            if raw == canonical:
                return value, "unchanged"
            return canonical, "fix-ac" if ac_key not in {"pride:0000450"} else "normalize"

        if ac_key in KNOWN_TERMS:
            ac_method = classify_method(KNOWN_TERMS[ac_key][0])
            if methods_compatible(nt_method, ac_method):
                canonical = KNOWN_TERMS[ac_key][1]
                if raw == canonical:
                    return value, "unchanged"
                return canonical, "normalize"
            return METHOD_CANONICAL[nt_method], "fix-ac"
        return METHOD_CANONICAL[nt_method], "fix-ac"

    if ac_key and ac_key in KNOWN_TERMS:
        canonical = KNOWN_TERMS[ac_key][1]
        if raw == canonical:
            return value, "unchanged"
        return canonical, "normalize"

    if ac_key:
        method = classify_method(raw)
        if method and method in METHOD_CANONICAL:
            return METHOD_CANONICAL[method], "fix-ac"
        return value, "unmapped-ac"

    if is_plain:
        # Short aliases → recommended form; full OLS labels left as-is.
        alias = raw.strip().upper()
        if alias in {"DDA", "DIA", "PRM", "SRM"}:
            return METHOD_CANONICAL[alias], "upgrade-alias"
        return value, "plain-kept"

    # NT-only (or malformed without AC): upgrade recognizable methods.
    method = classify_method(nt or raw)
    if method and method in METHOD_CANONICAL:
        return METHOD_CANONICAL[method], "upgrade-nt-only"
    return value, "unmapped"


def process_file(path: Path, dry_run: bool) -> tuple[Counter[str], list[str]]:
    actions: Counter[str] = Counter()
    notes: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        notes.append(f"{path}: read failed ({exc})")
        return actions, notes

    # Preserve final newline behaviour.
    had_trailing_newline = text.endswith("\n")
    rows = list(csv.reader(text.splitlines(), delimiter="\t"))
    if len(rows) < 2:
        return actions, notes

    header = [c.strip().lower() for c in rows[0]]
    idxs = [i for i, c in enumerate(header) if c == COLUMN]
    if not idxs:
        return actions, notes

    changed = False
    for ridx in range(1, len(rows)):
        row = rows[ridx]
        for i in idxs:
            if i >= len(row):
                continue
            old = row[i]
            new, action = remap_value(old)
            actions[action] += 1
            if action == "empty":
                notes.append(f"{path}: empty acquisition method at data row {ridx}")
            elif action.startswith("unmapped"):
                notes.append(f"{path}: {action} value={old!r}")
            if new != old:
                row[i] = new
                changed = True

    if changed and not dry_run:
        out_lines = ["\t".join(row) for row in rows]
        out = "\n".join(out_lines)
        if had_trailing_newline:
            out += "\n"
        path.write_text(out, encoding="utf-8")

    return actions, notes


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("repo", nargs="?", default=".", help="repo root with datasets/")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.repo)
    files = sorted(glob.glob(str(root / "datasets" / "*" / "*.sdrf.tsv")))
    total = Counter()
    all_notes: list[str] = []
    files_changed = 0

    for f in files:
        path = Path(f)
        before = path.read_bytes() if path.exists() else b""
        actions, notes = process_file(path, dry_run=args.dry_run)
        if not actions:
            continue
        total.update(actions)
        all_notes.extend(notes)
        if args.dry_run:
            # approximate change detection
            if any(a in actions for a in ("normalize", "fix-ac", "upgrade-nt-only")):
                files_changed += 1
        elif path.read_bytes() != before:
            files_changed += 1

    print(f"files scanned: {len(files)}")
    print(f"files changed: {files_changed}{' (dry-run estimate)' if args.dry_run else ''}")
    print("actions:")
    for k, n in total.most_common():
        print(f"  {n:6d}  {k}")
    if all_notes:
        print(f"\nnotes ({len(all_notes)}):")
        for note in all_notes[:50]:
            print(f"  {note}")
        if len(all_notes) > 50:
            print(f"  ... {len(all_notes) - 50} more")


if __name__ == "__main__":
    main()
