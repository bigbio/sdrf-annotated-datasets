# PXD060886 — under repair

Immunopeptidomics/proteomics re-annotation held in `sandbox/` because the file(s) below do
not yet pass the repository's review gate (`.github/scripts/sdrf_review.py`) or
`parse_sdrf validate-sdrf` against `sdrf-pipelines` `main`. Row content, run-to-sample
mapping and ontology terms are otherwise complete.

## `PXD060886-proximity-proteome.sdrf.tsv`
- 18 `characteristics[...]` cells encoded as `NT=...;AC=...` instead of the bare ontology label

Promotion to `datasets/` will follow the workflow in `sandbox/README.md` once the defects above are fixed.
