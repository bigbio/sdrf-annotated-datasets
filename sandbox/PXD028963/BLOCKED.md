BLOCKED: the raw-file -> sample map (cell type, fraction or gel band, SILAC timepoint, replicate) is not public. For 192 of the 198 deposited sample IDs the biological sample identity cannot be placed at all, and the remaining 6 lack a replicate number. Only the organism (from the search database) and the instrument (from the mzXML headers) can be read per ID.

Dataset: PXD028963, "Identification of long-lived proteins in the mitochondria reveals increased
stability of the electron transport chain". Krishna et al. 2021, Dev Cell 56(21):2952-2965,
PMID 34715012, PMC8664086, doi:10.1016/j.devcel.2021.10.008.

## What the deposit holds

- 398 Thermo `.raw` files, plus an `.mzXML` for each. The `msModel` in the mzXML headers names three
  instruments:
  - Orbitrap Fusion Lumos: 206 files, 103 IDs.
  - Orbitrap Fusion: 180 files, 89 IDs.
  - Orbitrap Eclipse: 12 files, `MHSK-284` to `289`, acquired 2020-12-18.

  PRIDE lists only the Lumos, and the paper never mentions the Eclipse.
- 198 IP2 result pairs (`MHSK-<n>_DTASelect-filter.mzid.gz`, `MHSK-<n>_census-out.txt`), one per
  sample ID `MHSK-82` ... `MHSK-343`.
- 197 sample IDs have two raw files, and `MHSK-170` has four. Most names write the ID as `MHSK-<n>`.
  The 108 files acquired on 2021-04-06 (`MHSK_290` to `343`) write it as `MHSK_<n>`.
- The injection suffixes are not regular (`_1/_2`, `_1/_3`, `_2/_3`, `_3/_4`, `-1/-2`).
- The files were acquired on 11 dates from 2019-04-14 to 2021-04-06.
- File names carry only an acquisition date and the MHSK ID. They name no cell type, fraction,
  day or replicate.

## What the paper says about the design (STAR Methods)

- This is pulsed SILAC. Light medium is switched to heavy Lys-13C6 (Lys6) + Arg-13C6,15N4 (Arg10)
  medium. All timepoints are harvested on day 8. The timepoints are days 0, 1, 2, 4, 6 and 8
  (Mendeley `Proteomics Data Analysis.Rmd`: `Time_d = c(0,1,2,4,6,8)`).
- There are two systems, each with 3 independent biological replicates:
  - H9 hESC-derived induced neurons (human), fractionated into nuclear, mitochondrial and cytosolic
    fractions.
  - C2C12 myotubes (mouse), as whole cell or as nuclear and mitochondrial fractions.
- BN-PAGE gel bands from myotube mitochondria were cut into 5 samples: SCI,IIIn,IVn; SCIII2,IV;
  CIII2,CIV2; CI+CII; and CIV. These were run on an Orbitrap Fusion (not Lumos) with an nLC 1000.
  The 89 Orbitrap Fusion IDs come close to the 90 gel-band samples the paper implies, but do not
  equal them. The instrument therefore does not identify the gel-band runs.
- Search: ProLUCID / DTASelect / Census2 in IP2 6.0.5. Fixed modification: carbamidomethyl C
  (+57; the alkylant is chloroacetamide). Heavy labels: K +6.0201 and R +10.0083. Precursor
  tolerance 50 ppm. Enzyme: trypsin, fully and half-tryptic.

## Sources checked for the map, and what each gave

1. **Paper full text** (PMC8664086, author manuscript via NCBI BioC). No sample-to-file table. Data
   availability gives only the PXD and Mendeley Data 10.17632/b3hww8ng7w.1.
2. **Supplementary Tables S1 and S2** (NIHMS1753680-supplement-3/4.xlsx). By their captions they
   hold "mass spectrometry data" per fraction and per gel band. They were not read: the PMC download
   is behind a reCAPTCHA, and Europe PMC `supplementaryFiles` refuses the article as not open
   access. Their captions (PMC article page) describe protein-level tables with columns
   `Day 0-8_mean/SD/N`, alpha, Rsq and Thalf. The sheets are `Neu_AllFraction_Replicates`,
   `Myo_WholeCell_Replicates`, `Myo_NucFraction_Replicates` and `Myo_MitoFraction_Replicates`, plus
   Gel Bands 1-5 "pooled from 3 independent replicates". A per-run MHSK map is therefore unlikely,
   though it is unverified. The neuron whole-cell values are fractions pooled in the analysis, not
   separate runs. The supplementary figures PDF (NIHMS1753680-supplement-2.pdf) is behind the same
   reCAPTCHA and was not read.
3. **PRIDE files.** None of these headers names a sample: the Census `H` lines, the mzid headers,
   and the headers of all 398 mzXML files (`parentFile` is only `E:\mzid\<same name>.raw`). The mzid
   protein descriptions show the search database (for example, MHSK-136 is mouse), but give no day,
   fraction or replicate.
4. **Mendeley Data b3hww8ng7w** (code deposit). Its example input is `MHSK-Day0-136`,
   `MHSK-Day1-137`, `MHSK-Day2-138`, `MHSK-Day4-139`, `MHSK-Day6-140` and `MHSK-Day8-141`, in a
   folder named "Myotube Whole Cell". This maps only these 6 IDs (12 raw files) to C2C12 myotube
   whole cell, days 0 to 8. Even for these 6, it does not say which of the 3 replicates they are.
   All 12 of these files were acquired on the Orbitrap Fusion Lumos. That is further evidence that
   instrument does not separate whole-cell runs from gel-band runs.
5. **PRIDE structured fields.** These disagree with the paper in three places. Follow the paper:
   - `diseases = Severe acute respiratory syndrome (DOID:2945)` is a submitter dropdown artefact.
     Nothing in the paper involves SARS or any disease: the samples are healthy cell lines (H9
     hESC-derived neurons and C2C12 myotubes). A future SDRF must not carry SARS. The disease should
     be `normal`.
   - The PTMs list "iodoacetamide derivatized residue" (MOD:00397), but the paper's alkylant was
     chloroacetamide.
   - The PTMs list only "6x(13)C labeled residue" (MOD:00544), with no Arg +10 label.

The block-like runs of consecutive IDs in the numbering (for example, 6 IDs per timecourse) suggest
a layout. So does the paper's design arithmetic (3x6x3 + 3x6x3 + 5x6x3 = 198). Using either would
be inference, not evidence, so neither was used.

## What would unblock this dataset

- An author-provided sample sheet mapping each MHSK ID to system (neuron or myotube),
  fraction or gel band, day and replicate.
- Or a readable copy of Tables S1 and S2, if they turn out to name the MHSK IDs. Only then
  would the map be verifiable.

With such a map, the SDRF would use the templates `ms-proteomics` + `human` + `vertebrates` +
`cell-lines`, split per organism if needed. It would have:

- two rows per raw file, `SILAC light` and `SILAC heavy`;
- heavy modifications Label:13C(6) (UNIMOD:188) on K and Label:13C(6)15N(4) (UNIMOD:267) on R;
- `comment[instrument]` per file, taken from the mzXML `msModel`;
- `factor value[time]` (days of heavy pulse), plus the fraction.

No SDRF is provided here.
