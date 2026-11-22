# PXD065538 - BLOCKED subset: label-free protein-abundance time course (Exploris 480)

Annotated in [`datasets/PXD065538/`](../../datasets/PXD065538/): `PXD065538-silac.sdrf.tsv` (288 SILAC .raw runs) and
`PXD065538-ubiquitin.sdrf.tsv` (18 ubiquitin .raw runs). Every deposited vendor .raw file is covered.

## Affected files (23, from PRIDE files/all; PRIDE files them under category RAW but they are mzML)
- `KossBS_031323_GPF6_1.mzML`
- `KossBS_031323_GPF6_2.mzML`
- `KossBS_031323_GPF6_3.mzML`
- `KossBS_031323_GPF6_5.mzML`
- `KossBS_031323_GPF6_6.mzML`
- `KossBS_031323_Sample_01_Day4_Acute_101C.mzML`
- `KossBS_031323_Sample_02_Day4_Acute_801C.mzML`
- `KossBS_031323_Sample_03_Day4_Acute_803C.mzML`
- `KossBS_031323_Sample_04_Day4_Chronic_101C.mzML`
- `KossBS_031323_Sample_05_Day4_Chronic_801C.mzML`
- `KossBS_031323_Sample_06_Day4_Chronic_803C.mzML`
- `KossBS_031323_Sample_07_Day6_Acute_101C.mzML`
- `KossBS_031323_Sample_08_Day6_Acute_801C.mzML`
- `KossBS_031323_Sample_09_Day6_Acute_803C.mzML`
- `KossBS_031323_Sample_10_Day6_Chronic_101C.mzML`
- `KossBS_031323_Sample_11_Day6_Chronic_801C.mzML`
- `KossBS_031323_Sample_12_Day6_Chronic_803C.mzML`
- `KossBS_031323_Sample_13_Day8_Acute_101C.mzML`
- `KossBS_031323_Sample_14_Day8_Acute_801C.mzML`
- `KossBS_031323_Sample_15_Day8_Acute_803C.mzML`
- `KossBS_031323_Sample_16_Day8_Chronic_101C.mzML`
- `KossBS_031323_Sample_17_Day8_Chronic_801C.mzML`
- `KossBS_031323_Sample_18_Day8_Chronic_803C.mzML`

Associated (not runs): `Timecourse_2023_01_UniProt_Homo_sapiens.fasta`, `Timecourse_KossBS_031323_Metadata.csv`, `Timecourse_MzTab_Report_KossBS_031323.mztab`, `Timecourse_Samples_Report_KossBS_031323.csv`.

## Why
- These runs exist only as mzML; no vendor .raw file is deposited for any `KossBS_031323_*` run. The
  SDRF specification itself allows mzML data files, but the curation convention this annotation follows
  (bigbio/sdrf-skills: `comment[data file]` references the vendor raw file, never a converted peak list)
  does not, so they were left out rather than annotated against the mzML. Nothing in the mzML content was
  found to prevent an annotation.
- The experiment is label-free (EncyclopeDIA/Scaffold DIA; Orbitrap Exploris 480), not SILAC, so it is
  also outside the SILAC campaign.
- The sample map itself IS recoverable: `Timecourse_KossBS_031323_Metadata.csv` gives Day 4/6/8,
  Acute/Chronic and donor IDs 101C/801C/803C per file; the 5 `GPF6_*` files are gas-phase-fractionated
  chromatogram-library runs (GPF6_4 is not deposited).

## What would unblock
- The submitters depositing the Thermo .raw files for the 18 samples and the GPF library runs, or
- a maintainer decision to accept the deposited mzML files as `comment[data file]`, in which case a
  label-free `PXD065538-timecourse.sdrf.tsv` can be built from the metadata CSV above.
