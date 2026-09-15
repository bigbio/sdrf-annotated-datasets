# PXD011628 — under repair

Immunopeptidomics/proteomics re-annotation held in `sandbox/` because the file(s) below do
not yet pass the repository's review gate (`.github/scripts/sdrf_review.py`) or
`parse_sdrf validate-sdrf` against `sdrf-pipelines` `main`. Row content, run-to-sample
mapping and ontology terms are otherwise complete.

## `PXD011628-celllines.sdrf.tsv`
- parse_sdrf validate-sdrf: `characteristics[sample type]` values are not in the validator's `pride` ontology list

## `PXD011628-donors.sdrf.tsv`
- parse_sdrf validate-sdrf: `characteristics[sample type]` values are not in the validator's `pride` ontology list

Sibling file(s) of this accession that pass the gate are already under `datasets/PXD011628/`: `PXD011628-syntheticpeptides.sdrf.tsv`.

Promotion to `datasets/` will follow the workflow in `sandbox/README.md` once the defects above are fixed.
