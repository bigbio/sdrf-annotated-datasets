# PXD023086

BLOCKED: the SILAC channel-to-condition map is not in the public record, so the compared
variable (`factor value[treatment]`) is `not available` on every row. Everything else in the
file is taken from the deposit, the paper (PMC7771050) and Cellosaurus. The file passes
`parse_sdrf validate-sdrf` for ms-proteomics, human and cell-lines.

## What is known
- Flag-UBCv1 (ASFV I215L) affinity-purification SILAC in HEK293T cells, with three replicates
  (`290617_Rep1/2/3.raw`) on an Orbitrap Fusion. The raw-file header confirms the Orbitrap
  Fusion; the PRIDE dropdown says "LTQ Orbitrap Elite", which is wrong.
- Each run is triple SILAC. The Proteome Discoverer workbook `UBCv1SILACData.xlsx` reports
  Heavy/Light, Medium/Heavy and Medium/Light ratios, and the search used Arg+6/Arg+10 and
  Lys+4/Lys+8 labels. That gives 9 rows: 3 files x 3 channels.
- No virus infection was involved. The samples are human cells transfected with a viral gene,
  so the organism is *Homo sapiens* only.

## Why this is in sandbox
- The paper says the eluates were "combined on a 1:1 ratio", but each run has three channels.
  Neither the paper, its only supplementary file (Figure S1, western blots), the PRIDE record
  nor the workbook says which construct or control each label carries.
- In the workbook the bait sits in the medium channel for Replicates 1-2 but in the heavy
  (and medium) channels for Replicate 3. The layout seems to change between replicates, and
  this cannot be reconstructed without guessing.

## Return criteria
- A sample sheet or author statement mapping each SILAC label in each replicate to its
  transfection (for example empty vector, Flag-UBCv1 or Flag-UBCv1 C85A).
- Fill `characteristics[treatment]` / `factor value[treatment]`, re-review, then move the
  folder to `datasets/PXD023086/`.
