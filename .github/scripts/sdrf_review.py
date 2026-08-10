#!/usr/bin/env python3
"""Self-contained SDRF review gate for CI.

Runs the two checks parse_sdrf is blind to (coordinate collisions, ragged rows)
plus parse_sdrf validation itself, over the SDRF files given as arguments.
Canonical logic lives in the sdrf-harness package (validator.py); this is a
vendored, dependency-light copy so CI needs only sdrf-pipelines.

Usage: python sdrf_review.py [--baseline <dir>] <file.sdrf.tsv> [more...]
Exit 0 if all clean (warnings allowed), 1 if any defect.

With --baseline <dir>, structural defects (coordinate collisions, ragged rows) are
reported only when the file INTRODUCES them: a file that already had N collisions on
the base branch (a copy of which lives at <dir>/<path>) and still has <= N is not
flagged, so a change that never touches the coordinate columns is not blocked by a
pre-existing defect. parse_sdrf validity is always checked in full.
"""
import subprocess
import sys
from collections import Counter
from pathlib import Path


def structural_check(path):
    lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
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
           "-t", "ms-proteomics", "--use_ols_cache_only"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    tail = (out.stdout + out.stderr).strip().splitlines()
    last = tail[-1] if tail else ""
    ok = ("Well done" in last) or ("only warnings" in last)
    return ok, last[:200]


def main(argv):
    baseline = None
    if "--baseline" in argv:
        i = argv.index("--baseline")
        baseline = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    files = [a for a in argv if a.endswith((".sdrf.tsv", ".sdrf"))]
    if not files:
        print("no SDRF files to review")
        return 0
    failures = []
    for f in files:
        ragged, collisions = structural_check(f)
        # Baseline: subtract defects that already existed on the base branch so a change
        # that does not touch the coordinate columns is not blocked by a pre-existing defect.
        base_ragged = base_collisions = 0
        if baseline:
            bpath = Path(baseline) / f
            if bpath.exists() and bpath.stat().st_size > 0:
                base_ragged, base_collisions = structural_check(bpath)
        new_collisions = max(0, collisions - base_collisions)
        new_ragged = max(0, ragged - base_ragged)
        ok, last = parse_sdrf_ok(f)
        problems = []
        if new_collisions:
            pre = f" (base had {base_collisions})" if base_collisions else ""
            problems.append(f"{new_collisions} new coordinate collisions{pre}")
        if new_ragged:
            problems.append(f"{new_ragged} new ragged rows")
        if not ok:
            problems.append(f"parse_sdrf: {last}")
        status = "OK" if not problems else "FAIL"
        note = ""
        if not problems and (collisions or ragged):
            note = f" — pre-existing {collisions} collisions/{ragged} ragged (not introduced here)"
        print(f"[{status}] {f}" + (" — " + "; ".join(problems) if problems else note))
        if problems:
            failures.append(f)
    print(f"\n{len(files) - len(failures)}/{len(files)} clean, {len(failures)} with defects")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
