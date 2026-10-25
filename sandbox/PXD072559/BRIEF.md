# PXD072559

## Evidence and coverage

- [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD072559),
  [publication](https://pmc.ncbi.nlm.nih.gov/articles/PMC13289816/),
  [demographics S7](https://doi.org/10.1158/2159-8290.32845512),
  [sample counts S8](https://doi.org/10.1158/2159-8290.32845509), and
  [supplementary methods](https://doi.org/10.1158/2159-8290.32845533).
- `Reference_File.csv` matches all 115 mzML members of `MS_mzML_FILES.zip`
  exactly. The same 115 files occur in the DIA-NN main-analysis statistics.
  Every mzML prefix identifies Orbitrap Astral, its original RAW basename and
  MS1 380–980 m/z. Original Thermo RAWs are named as provenance only; the
  deposited acquisition representation is mzML.
- All 42 sample-code/group/batch counts agree with S8. S7 resolves 24 sample
  codes to 20 individuals: ten organ donors and ten patients. Donor1 has
  S0204/S0229; Patient2 has S0101/S0110, Patient3 S0119/S0122, and Patient5
  S0115/S0116. These pairs share individual and biological-replicate IDs.
- The seven author histological groups contain 9 iADM, 26 LG-iPanIN,
  14 iNormal, 9 cNormal, 12 LG-cPanIN, 23 Tumor and 22 HG-cPanIN runs.
  NB1/NB2/NB3 processing batches are retained.

## Annotation decisions

- Sex, age and patient treatment/stage follow the linked S7 rows. Reported
  race is retained as reported race; it is not converted into genetic ancestry.
  Disease describes donor clinical context; histological group separately
  preserves normal ducts, metaplasia, precursor lesions and tumor. No sample
  genotype is inferred from the separate KRAS search library.
- These are FFPE microdissected tissue regions, not individually measured
  cells. No exact cells-per-sample count is asserted. Multiple sampled regions
  are not assigned arbitrary technical-replicate numbers; the well/aliquot/
  repeat-injection correspondence remains unavailable.
- Physical Lys-C/trypsin preparation and published 2 m/z DIA windows, 300
  events and HCD 25 NCE follow the supplementary methods. Main-analysis logs
  independently confirm DIA-NN 1.8.1, fixed 15 ppm MS1/MS2 accuracy and library
  FASTA `20250204_UP000005640_9606.fasta`. CAM and methionine excision are
  library settings; no unreported physical alkylation reagent is inferred.
- The old one-row `Reference_File.csv` placeholder is replaced by 115 actual
  acquisition rows. The URI points to the real ZIP and the member field gives
  the exact internal mzML path.

## Local validation

Reviewed 2026-09-28 using sdrf-pipelines `701356bd5309`. `ms-proteomics`,
`human`, `dia-acquisition` and repository review fail only the unresolved
technical-replicate requirement. The old CSV placeholder passed syntax checks;
it was not a valid representation of the experiment. This remains a sandbox
draft until the remaining sample-to-injection relationship is supported.

The source reconciler reads only the first of the duplicate enzyme columns.
A direct check of both columns confirms the declared Trypsin/Lys-C pair.
