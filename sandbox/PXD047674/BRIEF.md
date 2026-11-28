# PXD047674 SDRF annotation report

## Study
Mass spectrometry-based proteomic profiling of exosomal (extracellular vesicle) proteins in diabetic and non-diabetic ischemic stroke patients: a case-control study (Weill Cornell Medicine-Qatar / Hamad Medical Corporation, Doha). Paper: Front Mol Biosci 2024, doi:10.3389/fmolb.2024.1387859, PMC11211575. Its Data Availability names PXD047674, so the link is verified. The PX record still says "publication pending".

## Scope, evidence and decisions
- **Deposited:** 40 RAW files plus `P003_exosome_p_and_ES.xlsx` (search output). The list comes from PROXI `resultType=full` and is cross-checked against the PRIDE FTP listing. No sample-metadata, mqpar or README files are deposited. The file list is in scratch `raw_files.txt`.
- **Annotated:** 40 rows, one per RAW file, label-free.
  - Control_01-12 become HC_01-12 (12 rows).
  - Group1_Stroke_NonDiabeteic01-14 become nDS_01-14 (14 rows).
  - nDS_01 has an extra file, `NonDiabeteic01_repeat.raw` (technical replicate 2). The first nDS01 file is only 408 MB; the repeat is 628 MB.
  - Group2_Stroke_Diabeteic01-13 become DS_01-13 (13 rows).
  - The counts 12/14/13 match the paper and PX description (HC=12, nDS=14, DS=13). Group membership is STATED in the file names.
- **Groups encoded as:**
  - disease = normal (HC) or ischemic stroke (nDS, DS).
  - phenotype = diabetic / non-diabetic, using HbA1c of at least 6 versus below 6 as in the paper.
  - The clinical-metadata template is declared to license phenotype. Both disease and phenotype are factor values.
- **Sample:** serum (`blood serum`). EVs were isolated by differential ultracentrifugation (100,000 g twice). 10 ug of protein was run briefly into a NuPAGE gel as a single band and digested in-gel with trypsin. Reduction was DTT.
- **LC-MS (paper):** Easy nLC 1200, 120 min gradient, DDA top-15, MS1 at 70,000 resolution. Processed with Genedata Refiner MS and Mascot 2.6 (SwissProt human). Tolerances are 20 ppm precursor and 0.05 Da fragment (STATED).
- **Dissociation:** HCD is INFERRED (Q Exactive family).

## Instrument conflict (main open point, INFERRED)
The three sources disagree:
- PX record: Q Exactive HF.
- Paper: "Q-Exactive HFX" with Easy nLC 1200.
- RAW file names: `QEP_LC1000`, i.e. Q Exactive Plus with nLC 1000, acquired 2019-08-07.

I chose **Q Exactive Plus (MS:1002634)**. The reasons are that the file names are the closest thing to raw data available, and that 70,000 resolution is a QE/QE Plus setting, not an HF/HF-X one (60k/120k). The RAW headers could NOT be read: the shell has no network and the files are 0.4-1.6 GB. A reviewer with network should range-read the first ~256 KB of one RAW file and fix the instrument.

## Values left not available / not applicable
- **age, sex, ancestry category: not available.** The paper gives only group medians and sex counts (HC 8M/4F; nDS 13M/1F; DS 12M/1F). There is no per-subject key.
- **developmental stage = adult (INFERRED).** Group median ages are 45-53.
- **alkylation reagent: not available.** No alkylation step is described, but silence is not evidence that none was done.
- **modification parameters: not available.** The paper does not state the modifications, the PX record says "No PTMs", and the xlsx search output was not opened. Carbamidomethyl was deliberately NOT asserted.
- **collision energy: not available.** Not reported.
- **fractionation method: not applicable.** The sample was a single gel band, not fractionated.
- **biological replicate = 1 per subject; individual = source name.** The paper says "each sample was run in triplicate", but only one run per subject is deposited (two for nDS_01).

## Conflicts / caveats
- **Triplicates:** the stated triplicate runs are not deposited.
- **Genedata version:** the paper gives v13.0.1 in Methods and 7.5 in Results.
- **LC system:** nLC 1000 (file names) versus nLC 1200 (paper).
- **Ontology terms:** OLS was unreachable today (the WebFetch rate limit and the browser upstream both failed). Terms are labels already used in prior campaign files (PRIDE:0000627, MS:1002634, MS:1001251, MS:1000422, PRIDE:0000608). The disease labels ("ischemic stroke", "normal") were not live-verified against MONDO/PATO in this run.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics --template human --template clinical-metadata` reports clean. The OLS ontology check is unavailable in this environment, so only the structure was validated. `sdrf_review.py` reports [OK]. The file has 40 rows × 37 columns.

## Status
sandbox: the instrument is inferred from the file-name tag against both the paper and the PX record, modifications are unknown, and the ontology terms were not live-verified.

## Review status
pending
