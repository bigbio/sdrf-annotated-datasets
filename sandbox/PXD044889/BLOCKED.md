# BLOCKED: donor/condition identity unresolved for 6 files

`PXD044889.sdrf.tsv` in this folder covers 6 raw files from PXD044889 that could not
be mapped to a donor or a stool/fermented condition:

- `Sample_11.zip`, `Sample_12.zip`, `Sample_13.zip`, `Sample_14.zip`,
  `Sampe_S13.zip` (typo in the original deposit, preserved verbatim), `Sample_S14.zip`

The paper (Mottawea/Hammami, *Microbiol Spectrum*, DOI 10.1128/spectrum.01368-24,
PMC11792502) states the cohort is 12 healthy donors, each contributing a stool (S)
and an ex-vivo-fermented (F) sample coded `D<n>S`/`D<n>F`. Those 18 D-coded files
are fully resolved and live in `datasets/PXD044889/PXD044889.sdrf.tsv`. These 6 files
do not follow that naming convention and their donor/condition mapping is not
recoverable from:
- PRIDE's file-list/project metadata (no donor field, no additional attributes)
- The paper's main text and methods
- The paper's supplementary tables (Table S14 has per-donor sex/age, but
  `spectrum.01368-24-s0002.xlsx` returned HTTP 403 on every fetch attempt — bot-blocked)

`characteristics[biological replicate]` is left `not available` here, which is
schema-illegal under `datasets/` validation (sample-metadata.yaml disallows it for
this column) — that is exactly why this lives in `sandbox/` rather than `datasets/`.
Assigning these 6 files distinct biological-replicate integers, however chosen,
asserts 6 additional confirmed-distinct donors beyond the paper's stated 12, which
the evidence does not support (flagged by independent review).

## To promote to datasets/

Resolve the true donor/condition mapping — e.g. from Table S14 (may require
institutional/library access or direct author contact) or embedded metadata in the
raw files themselves — then fill in `characteristics[host subject id]`,
`characteristics[host body site]`, `characteristics[sample collection method]`,
`factor value[sample collection method]`, and a real integer (reusing an existing
donor number, or a new one only if the source confirms >12 donors were actually
sampled) for `characteristics[biological replicate]`. Validate and `git mv` per
`sandbox/README.md`.
