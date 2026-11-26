"""Emit validator arguments from declared templates without losing duplicate columns."""
import csv
import re
import sys
from pathlib import Path


def template_args(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.reader(stream, delimiter="\t")
        header = next(rows)
        indices = [i for i, name in enumerate(header) if name == "comment[sdrf template]"]
        declared = set()
        for row in rows:
            if not row:
                continue
            for i in indices:
                value = row[i] if i < len(row) else ""
                match = re.fullmatch(r"NT=([a-z][a-z0-9-]*);VV=v?[0-9][a-zA-Z0-9.+-]*", value)
                if not match:
                    raise ValueError(f"Invalid template declaration: {value!r}")
                declared.add(match.group(1))
    if not declared:
        declared.add("affinity-proteomics" if Path(path).name.startswith("PAD") else "ms-proteomics")
    return [arg for name in sorted(declared) for arg in ("-t", name)]


if __name__ == "__main__":
    print("\n".join(template_args(sys.argv[1])))
