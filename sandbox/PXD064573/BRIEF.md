# PXD064573 — under repair

Immunopeptidomics/proteomics re-annotation held in `sandbox/` because the file(s) below do
not yet pass the repository's review gate (`.github/scripts/sdrf_review.py`) or
`parse_sdrf validate-sdrf` against `sdrf-pipelines` `main`. Row content, run-to-sample
mapping and ontology terms are otherwise complete.

## `PXD064573-elastase-benchmark.sdrf.tsv`
- 2 coordinate collisions (source name x biological replicate x technical replicate x fraction, no separating column)

## `PXD064573-immunopeptidomics.sdrf.tsv`
- 6 coordinate collisions (source name x biological replicate x technical replicate x fraction, no separating column)

Promotion to `datasets/` will follow the workflow in `sandbox/README.md` once the defects above are fixed.
