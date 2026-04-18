#!/usr/bin/env python3
"""Run parse_sdrf validate-sdrf on every datasets/*/*.sdrf.tsv; write a TSV report."""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATASETS = REPO_ROOT / "datasets"
REPORT = REPO_ROOT / ".validation-full-run.log"
TIMEOUT = 300


def main() -> int:
    files = sorted(DATASETS.glob("*/*.sdrf.tsv"))
    REPORT.write_text("", encoding="utf-8")

    def log(msg: str) -> None:
        line = f"{datetime.now(timezone.utc).isoformat()} {msg}\n"
        print(line, end="")
        with REPORT.open("a", encoding="utf-8") as fh:
            fh.write(line)

    log(f"START count={len(files)}")
    failures: list[tuple[str, str]] = []

    for idx, path in enumerate(files, start=1):
        rel = path.relative_to(REPO_ROOT)
        if path.stat().st_size == 0:
            log(f"EMPTY [{idx}/{len(files)}] {rel}")
            failures.append((str(rel), "empty file"))
            continue
        log(f"RUN [{idx}/{len(files)}] {rel}")
        try:
            proc = subprocess.run(
                [
                    "parse_sdrf",
                    "validate-sdrf",
                    "--sdrf_file",
                    str(path),
                    "--use_ols_cache_only",
                ],
                capture_output=True,
                text=True,
                timeout=TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            log(f"TIMEOUT [{idx}/{len(files)}] {rel}")
            failures.append((str(rel), f"timeout >{TIMEOUT}s"))
            continue
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout or "").strip().splitlines()
            snippet = " | ".join(tail[-5:]) if tail else f"exit {proc.returncode}"
            log(f"FAIL [{idx}/{len(files)}] {rel} :: {snippet[:500]}")
            failures.append((str(rel), snippet[:2000]))
        else:
            log(f"OK [{idx}/{len(files)}] {rel}")

    log(f"SUMMARY ok={len(files) - len(failures)} fail={len(failures)}")
    for rel, reason in failures:
        log(f"FAILED_FILE\t{rel}\t{reason.replace(chr(9), ' ')}")

    summary_path = REPO_ROOT / ".validation-summary.tsv"
    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write("status\tpath\treason\n")
        for rel, reason in failures:
            fh.write(f"fail\t{rel}\t{reason.replace(chr(9), ' ').replace(chr(10), ' ')}\n")
        for path in files:
            rel = str(path.relative_to(REPO_ROOT))
            if not any(r == rel for r, _ in failures):
                fh.write(f"ok\t{rel}\t\n")

    log("DONE")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
