# PXD005873 — SILAC, recessive dystrophic epidermolysis bullosa (draft)

BLOCKED: which donor is in which SILAC channel (medium or heavy) of each MaxQuant
experiment is not published in any source I could reach, so disease, age, sex and
individual are `not available` on every medium/heavy row.

- Dataset: https://www.ebi.ac.uk/pride/archive/projects/PXD005873
- Publication: Thriene K. et al., *Mol Cell Proteomics* 2018;17(4):565-579,
  PMID 29326176, PMC5880109, doi:10.1074/mcp.RA117.000437

## What the evidence supports (and is annotated)

- 163 RAW files (LTQ Orbitrap XL, ion-trap CID, DDA). Each file has 3 rows, one per
  SILAC channel, so the file has 489 rows.
- Triple SILAC. MaxQuant `summary.txt` gives light = Arg0/Lys0, medium = Arg6/Lys4
  (Label:13C(6) UNIMOD:188 on R, Label:2H(4) UNIMOD:481 on K) and heavy = Arg10/Lys8
  (Label:13C(6)15N(4) UNIMOD:267 on R, Label:13C(6)15N(2) UNIMOD:259 on K).
- Mixtures come from the deposited MaxQuant `experimentalDesign` files:
  - extracellular matrix (ECM): ECM1, ECM2, ECM2_2, ECM3, ECM4
  - intracellular lysate: intr5 to intr8
  - Fractions are gel slices.
  - Repeat injections of the same slice are numbered as technical replicates.
- The light channel of the ECM mixtures is a super-SILAC standard pooled "from all four
  donors" (paper, Results), so it is annotated as `pooled`.

## What is missing

- The paper names the donors: 2 DEB (DEB1, DEB2) and 2 control (Ctrl1, Ctrl2)
  populations, each measured in two biological replicates "using swapped labels".
- It does not say which donor (or disease state) was medium and which was heavy in each
  experiment. Fig. 3C shows only the generic scheme (DEB = Arg6/Lys4, Ctrl = Arg10/Lys8).
- The supplementary tables would probably resolve the map, but I could not retrieve them:
  - PMC serves them behind a bot check.
  - Europe PMC lists the article as not open access.
  - The publisher site returned 403.

## Hypothesis from the deposited data (NOT written into the SDRF)

The `proteinGroups.txt` ratios follow the published DEB direction: S100A8/A9 and CTSB
up, ITGB4/LAMB3/COL17A1 down. That pattern fits this layout:

- DEB = heavy in ECM1, ECM2, ECM2_2, intr5 and intr6
- DEB = medium in ECM3, ECM4, intr7 and intr8

Donor identity (DEB1 vs DEB2, Ctrl1 vs Ctrl2) and replicate a/b cannot be inferred from
the data.

## To promote to `datasets/`

1. Get the channel-to-donor map: from supplementary Table S3/S6 column headers, or from
   the authors.
2. Fill in disease, individual, age and sex per channel source. Age and sex are in the
   paper's Tables I and II:
   - DEB1 8Y male
   - DEB2 1M female
   - Ctrl1 2Y male
   - Ctrl2 4Y male
3. Set `factor value[disease]`.
4. Re-validate.

Other open points:

- Whether ECM2_2 is a second gel of the ECM2 mixture is not stated.
- What the light lysate standard contains is not described.
