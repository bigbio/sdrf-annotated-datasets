# PXD071196

`PXD071196-hf.sdrf.tsv` is in `datasets/`. These two files passed review and stay in `sandbox/` because the cell line and the sample behind each run cannot be linked to a mapping.

## Why qe and tims are in sandbox
- `PXD071196-qe.sdrf.tsv`: Q Exactive runs. Cell line identity is not assigned, and the run-to-sample link is not deposited.
- `PXD071196-tims.sdrf.tsv`: timsTOF Pro runs. Same gap: cell line and sample cannot be linked to a mapping.

## Return criteria
- A mapping from each Q Exactive and timsTOF run to cell line and sample.
- Re-review, then move these two files to `datasets/PXD071196/`.
