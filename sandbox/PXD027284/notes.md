# PXD027284

BLOCKED: run-to-sample mapping is undecodable for both instrument series.

## Why this is in sandbox
- `mqpar.xml` experiments are numbered only; RAW headers carry no sample names.
- Cell line (primary NK / NK-92 / KHYG-1) and treatment (IL-15, IL-12/15/18, anti-CD16) are missing.
- Biological replicate = 1 is a placeholder that contradicts the triplicate design.
- Instrument split confirmed from RAW headers: E* = Q Exactive, EH* = Q Exactive HF.

## Return criteria
- A run-to-cell-line and treatment map for both series.
- Re-review, then move to `datasets/PXD027284/`.
