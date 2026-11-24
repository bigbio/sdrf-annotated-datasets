# PXD054693 — sandbox draft (enzyme missing)

Secretome (conditioned medium) of PDAC lines Capan-2 and PANC-1, benign hTERT-HPNE and normal duct
H6c7, collected at 0/6/12/18 h over 24 h; label-free, Orbitrap Fusion. Vellan CJ et al. *Expert Rev
Proteomics* 2026 (PMID 41711676; not read). Universiti Malaya.

`PXD054693.sdrf.tsv` maps all 48 RAW: `<line>_<t>H_<ddmmyy>_R<n>.raw` = 4 lines × 4 time points ×
3 replicates (the ddmmyy acquisition-date token is ignored for mapping).

| Line | Cellosaurus | Source of the accession | disease | age / sex |
|---|---|---|---|---|
| Capan-2 | CVCL_0026 | sdrf-skills curated `cl-annotations-db.tsv` | pancreatic ductal adenocarcinoma | 56Y / male (same DB) |
| PANC-1 | CVCL_0480 | same | pancreatic ductal adenocarcinoma | 56Y / male (same DB) |
| hTERT-HPNE | CVCL_C466 | EFO xref (EFO_0022415) | normal | not available |
| H6c7 | not available | not in EFO or the local DB; Cellosaurus unreachable | normal | not available |

**Why sandbox:** digestion enzyme not stated in any reachable source (`comment[cleavage agent
details]` = `not available`, forbidden by `ms-proteomics`). To finish: PRIDE sample protocol →
enzyme; Cellosaurus → H6c7 accession and hTERT-HPNE donor age/sex; confirm R1–R3 are biological
replicates and that the sample is conditioned medium (`material type` is set to `cell line`, the
closest allowed value). Validates cleanly against `human` and `cell-lines` apart from that.
