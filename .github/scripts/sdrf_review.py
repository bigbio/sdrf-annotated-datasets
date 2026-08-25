#!/usr/bin/env python3
"""Self-contained SDRF review gate for CI.

Runs the checks parse_sdrf is blind to -- coordinate collisions, ragged rows,
reserved-word casing, characteristics value encoding, hollow/missing factor values,
pandas artifact headers and peak-list data files -- plus parse_sdrf validation itself,
over the SDRF files given as arguments.
Canonical logic lives in the sdrf-harness package (validator.py); this is a
vendored, dependency-light copy so CI needs only sdrf-pipelines.

Usage: python sdrf_review.py [--baseline <dir>] <file.sdrf.tsv> [more...]
Exit 0 if all clean (warnings allowed), 1 if any defect.

With --baseline <dir>, structural and content defects are
reported only when the file INTRODUCES them: a file that already had N collisions on
the base branch (a copy of which lives at <dir>/<path>) and still has <= N is not
flagged, so a change that never touches the coordinate columns is not blocked by a
pre-existing defect. parse_sdrf validity is always checked in full.
"""
import re
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
    # comment[label] is part of the identity: in multiplexed data (TMT/SILAC) the same
    # sample+replicate+fraction legitimately repeats once per label channel of one raw
    # file. Excluding the label flags every correct SILAC/TMT annotation as a collision.
    lb = col("comment[label]")
    collisions = 0
    if None not in (bi, ti, fr):
        need = max(x for x in (bi, ti, fr, lb) if x is not None)
        groups = {}
        for r in rows:
            if len(r) <= need:
                continue
            k = (r[0], r[bi], r[ti], r[fr]) + ((r[lb],) if lb is not None else ())
            groups.setdefault(k, []).append(r)
        dup = [v for v in groups.values() if len(v) > 1]
        # A collision is only a defect if the file does not record the distinction
        # anywhere. Multi-dimensional designs (a second fractionation scheme, an
        # enrichment arm, a preparation batch) repeat the coordinate legitimately and
        # carry the distinguishing value in another column, so a group that some
        # descriptive column separates completely is annotated, not colliding.
        # Identity columns are excluded: comment[data file] differing IS the collision,
        # and assay name/source name are derived run labels, not sample description.
        if dup:
            ignore = {"source name", "assay name", "comment[data file]", "comment[file uri]"}
            explainers = [i for i, name in enumerate(h)
                          if name.strip().lower() not in ignore
                          and (name.strip().lower().startswith(("characteristics[", "comment["))
                               or name.strip().lower().startswith("factor value["))]
            explained = any(
                all(len({r[i] if i < len(r) else "" for r in v}) == len(v) for v in dup)
                for i in explainers)
            collisions = 0 if explained else len(dup)
    return ragged, collisions


SENTINELS = {"not available", "not applicable"}
RESERVED = SENTINELS | {"pooled", "normal"}
PEAK_LIST = (".mgf", ".mzml", ".mzxml")


def _baseline_path(baseline, f):
    """Map a reviewed file to its copy under <baseline>.

    Path(baseline) / "/abs/path" returns "/abs/path" -- an absolute argument would
    silently make the baseline the file itself and disable every check, so strip the
    anchor first and always resolve inside the baseline tree.
    """
    p = Path(f)
    rel = p.relative_to(p.anchor) if p.is_absolute() else p
    return Path(baseline) / rel


def content_check(path):
    """Defects parse_sdrf does not catch. Returns {defect_name: count}."""
    lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
    if not lines:
        return {}
    hdr = lines[0].split("\t")
    H = [c.strip().lower() for c in hdr]
    rows = [ln.split("\t") for ln in lines[1:] if ln.strip()]
    d = Counter()

    # header mangled by pandas: comment[x].1 is NOT the same column as comment[x]
    d["artifact_headers"] = sum(1 for c in hdr if re.search(r"\]\.\d+$", c.strip()))

    if not rows:
        return {k: v for k, v in d.items() if v}

    def cell(r, i):
        return r[i].strip() if i < len(r) else ""

    for i, name in enumerate(H):
        for r in rows:
            v = cell(r, i)
            if not v:
                continue
            # reserved words MUST be lowercase (spec); parse_sdrf does not check this
            if v.lower() in RESERVED and v != v.lower():
                d["reserved_word_case"] += 1
            # characteristics take the bare ontology label, not NT=;AC=
            elif name.startswith("characteristics[") and "=" in v:
                parts = [p for p in v.split(";") if p.strip()]
                keys = set()
                pure = True
                for p in parts:
                    if "=" not in p:
                        pure = False
                        break
                    keys.add(p.split("=", 1)[0].strip().upper())
                if pure and keys == {"NT", "AC"}:
                    d["characteristics_not_bare_label"] += 1
        # vendor RAW, not peak lists
        if name == "comment[data file]":
            d["peak_list_data_file"] += sum(
                1 for r in rows if cell(r, i).lower().endswith(PEAK_LIST))

    # factor value: must exist and must encode an actual contrast
    fi = [i for i, c in enumerate(H) if c.startswith("factor value[")]
    if not fi:
        d["no_factor_value"] = 1
    elif all(cell(r, i).lower() in SENTINELS or not cell(r, i)
             for i in fi for r in rows):
        d["hollow_factor_value"] = 1

    return {k: v for k, v in d.items() if v}


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
            bpath = _baseline_path(baseline, f)
            if bpath.exists() and bpath.stat().st_size > 0:
                base_ragged, base_collisions = structural_check(bpath)
        new_collisions = max(0, collisions - base_collisions)
        new_ragged = max(0, ragged - base_ragged)
        cont = content_check(f)
        base_cont = {}
        if baseline:
            bp = _baseline_path(baseline, f)
            if bp.exists() and bp.stat().st_size > 0:
                base_cont = content_check(bp)
        new_cont = {k: v - base_cont.get(k, 0) for k, v in cont.items()
                    if v - base_cont.get(k, 0) > 0}
        ok, last = parse_sdrf_ok(f)
        problems = []
        if new_collisions:
            pre = f" (base had {base_collisions})" if base_collisions else ""
            problems.append(f"{new_collisions} new coordinate collisions{pre}")
        if new_ragged:
            problems.append(f"{new_ragged} new ragged rows")
        for k, v in sorted(new_cont.items()):
            problems.append(f"{v} {k}")
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
