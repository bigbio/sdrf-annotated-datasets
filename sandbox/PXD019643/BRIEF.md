# PXD019643 — held back from `datasets/`

Both class sheets pass the review gate, but a coverage comparison against the deposit shows our
annotation is **less complete than the one already in `datasets/PXD019643/`**, so that stays canonical
and ours is parked here.

Checked against the PRIDE file list for PXD019643 (3,426 files; 1,470 `.raw`, 1,471 `.mzML`):

- **56 deposited runs are annotated upstream but missing from ours** (26 class I, 30 class II). All
  56 exist in the deposit as both `.raw` and `.mzML`, so they are real gaps, not a naming artefact.
- **14 rows in ours reference files that are not in the deposit at all** (12 class I, 2 class II; e.g.
  `160409_DK_AUT01-DN16_Liver_W6-32_20_DDA_3_400-650mz_msms14_TS8h.raw`,
  `191118_AM_OVA01-DN278_Ovary_W6-32_20_DDA_1_400-650mz_msms6_TS0h_directinject.raw`) — neither as
  `.raw` nor as `.mzML`.
- The remaining difference is convention only: upstream points at the `.mzML` peak lists, ours at the
  vendor `.raw` files (726 of 752 class I and 686 of 716 class II rows match after normalising).

Ours does carry metadata the upstream annotation lacks — per-donor four-digit HLA typing in
`characteristics[mhc typing]`, antibody/enrichment columns and the MS acquisition settings — so
merging is worthwhile, but only after the 14 phantom references are resolved and the 56 missing runs
are annotated. Until then overwriting would lose deposited coverage.
