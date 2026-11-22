BLOCKED: the raw-file -> sample map (cell type, fraction or gel band, SILAC timepoint, replicate) is not public. 192 of the 198 deposited sample IDs cannot be placed at all, and the remaining 6 lack a replicate number.

Dataset: PXD028963, "Identification of long-lived proteins in the mitochondria reveals increased
stability of the electron transport chain". Krishna et al. 2021, Dev Cell 56(21):2952-2965,
PMID 34715012, PMC8664086, doi:10.1016/j.devcel.2021.10.008.

## What the deposit holds

- 398 Thermo `.raw` files (Orbitrap Fusion Lumos), plus an `.mzXML` for each.
- 198 IP2 result pairs (`MHSK-<n>_DTASelect-filter.mzid.gz`, `MHSK-<n>_census-out.txt`), one per
  sample ID `MHSK-82` ... `MHSK-343`.
- Nearly every sample ID has two raw files. The injection suffixes are not regular (`_1/_2`, `_1/_3`,
  `_2/_3`, `_3/_4`, `-1/-2`), and `MHSK-170` has four. The files were acquired on 11 dates from
  2019-04-14 to 2021-04-06.
- File names carry only an acquisition date and the MHSK ID. They name no cell type, fraction,
  day or replicate.

## What the paper says about the design (STAR Methods)

- This is pulsed SILAC. Light medium is switched to heavy Lys-13C6 (Lys6) + Arg-13C6,15N4 (Arg10)
  medium. All timepoints are harvested on day 8. The timepoints are days 0, 1, 2, 4, 6 and 8
  (Mendeley `Proteomics Data Analysis.Rmd`: `Time_d = c(0,1,2,4,6,8)`).
- There are two systems: H9 hESC-derived induced neurons (human), fractionated into nuclear,
  mitochondrial and cytosolic fractions; and C2C12 myotubes (mouse), as whole cell or nuclear and
  mitochondrial fractions. Each system has 3 independent biological replicates.
- BN-PAGE gel bands from myotube mitochondria were cut into 5 samples (SCI,IIIn,IVn; SCIII2,IV;
  CIII2,CIV2; CI+CII; CIV). These were run on an Orbitrap Fusion (not Lumos) with an nLC 1000.
  The PRIDE record lists only the Lumos, and the file names do not say which runs are gel bands.
- Search: ProLUCID / DTASelect / Census2 in IP2 6.0.5. Fixed modification: carbamidomethyl C
  (+57; the alkylant is chloroacetamide). Heavy labels: K +6.0201 and R +10.0083. Precursor
  tolerance 50 ppm. Enzyme: trypsin, fully and half-tryptic.

## Sources checked for the map, and what each gave

1. Paper full text (PMC8664086, author manuscript via NCBI BioC). No sample-to-file table. Data
   availability gives only the PXD and Mendeley Data 10.17632/b3hww8ng7w.1.
2. Supplementary Tables S1 and S2 (NIHMS1753680-supplement-3/4.xlsx). By their captions they hold
   "mass spectrometry data" per fraction and per gel band. The PMC download is behind a reCAPTCHA,
   so they were not read, and Europe PMC `supplementaryFiles` refuses the article as not open
   access. They are protein-level result tables. Whether they name MHSK IDs is unverified.
3. PRIDE files. The Census `H` header lines and the mzid headers name no sample. The mzid protein
   descriptions show the search database (for example, MHSK-136 is mouse) but give no day, fraction
   or replicate.
4. Mendeley Data b3hww8ng7w (code deposit). Its example input is `MHSK-Day0-136`,
   `MHSK-Day1-137`, `MHSK-Day2-138`, `MHSK-Day4-139`, `MHSK-Day6-140` and `MHSK-Day8-141`, in a
   folder named "Myotube Whole Cell". This maps only these 6 IDs (12 raw files) to C2C12 myotube
   whole cell, days 0 to 8. Even for these 6, it does not say which of the 3 replicates they are.
5. PRIDE structured fields. `diseases = Severe acute respiratory syndrome (DOID:2945)` is a
   submitter dropdown artefact. Nothing in the paper involves SARS or any disease: the samples are
   healthy cell lines (H9 hESC-derived neurons and C2C12 myotubes). A future SDRF must not carry
   SARS. The disease should be `normal`.

The block-like runs of consecutive IDs in the numbering (for example, 6 IDs per timecourse) suggest
a layout. Using them would be inference, not evidence, so they were not used.

## What would unblock this dataset

- An author-provided sample sheet mapping each MHSK ID to system (neuron or myotube),
  fraction or gel band, day and replicate.
- Or a readable copy of Tables S1 and S2, if they turn out to name the MHSK IDs. Only then
  would the map be verifiable.

With such a map, the SDRF would be `ms-proteomics` + `human` + `vertebrates` + `cell-lines` (split
per organism if needed). It would have two rows per raw file (`SILAC light`, `SILAC heavy`), heavy
modifications Label:13C(6) (UNIMOD:188) on K and Label:13C(6)15N(4) (UNIMOD:267) on R, and
`factor value[time]` (days of heavy pulse) plus the fraction.

No SDRF is provided here.
