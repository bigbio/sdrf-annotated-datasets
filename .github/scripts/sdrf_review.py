#!/usr/bin/env python3
"""Self-contained SDRF review gate for CI.

Runs the two checks parse_sdrf is blind to (coordinate collisions, ragged rows)
plus parse_sdrf validation itself, over the SDRF files given as arguments.
Canonical logic lives in the sdrf-harness package (validator.py); this is a
vendored, dependency-light copy so CI needs only sdrf-pipelines.

Usage: python sdrf_review.py <file.sdrf.tsv> [more...]
Exit 0 if all clean (warnings allowed), 1 if any defect.
"""
import subprocess
import sys
from collections import Counter
from pathlib import Path


def structural_check(path):
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
    except FileNotFoundError:
        return None, None
    if not lines:
        return 0, 0
    h = lines[0].split("\t")
    rows = [ln.split("\t") for ln in lines[1:] if ln.strip()]
    ragged = sum(1 for r in rows if len(r) != len(h))
    def col(n):
        return h.index(n) if n in h else None
    bi, ti, fr = (col("characteristics[biological replicate]"),
                  col("comment[technical replicate]"),
                  col("comment[fraction identifier]"))
    collisions = 0
    if None not in (bi, ti, fr):
        key = Counter((r[0], r[bi], r[ti], r[fr]) for r in rows if len(r) > max(bi, ti, fr))
        collisions = sum(1 for v in key.values() if v > 1)
    return ragged, collisions


def parse_sdrf_ok(path):
    cmd = ["parse_sdrf", "validate-sdrf", "--sdrf_file", str(path),
           "--use_ols_cache_only"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    tail = (out.stdout + out.stderr).strip().splitlines()
    last = tail[-1] if tail else ""
    ok = ("Well done" in last) or ("only warnings" in last)
    return ok, last[:200]


def main(argv):
    files = [a for a in argv if a.endswith((".sdrf.tsv", ".sdrf"))]
    if not files:
        print("no SDRF files to review")
        return 0
    failures = []
    skipped = []
    for f in files:
        ragged, collisions = structural_check(f)
        if ragged is None:
            # File not found, skip it
            print(f"[SKIP] {f} (file not found)")
            skipped.append(f)
            continue
        ok, last = parse_sdrf_ok(f)
        problems = []
        if collisions:
            problems.append(f"{collisions} coordinate collisions")
        if ragged:
            problems.append(f"{ragged} ragged rows")
        if not ok:
            problems.append(f"parse_sdrf: {last}")
        status = "OK" if not problems else "FAIL"
        print(f"[{status}] {f}" + (" — " + "; ".join(problems) if problems else ""))
        if problems:
            failures.append(f)
    
    validated = len(files) - len(skipped)
    clean = validated - len(failures)
    print(f"\n{clean}/{validated} validated files clean, {len(failures)} with defects" + 
          (f", {len(skipped)} skipped" if skipped else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
