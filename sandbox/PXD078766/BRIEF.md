# PXD078766 SDRF annotation report

## Study
MLKL confers ferroptosis resistance in colorectal cancer cells via impaired ESCRT-III-mediated membrane repair.
Sonkaew S et al., Biol Direct 2026;21:184. DOI 10.1186/s13062-026-00887-0, PMID 42401932. The paper is open access; no PMCID was resolvable today because Europe PMC returned a server error. Lab head Siriporn Jitkaew, Chulalongkorn University, Bangkok.

## Scope, evidence and decisions
Status **sandbox**. The file has 36 rows (36 SWATH runs, label-free) and 48 columns. Templates: ms-proteomics, human, cell-lines, clinical-metadata (v1.0.0) and dia-acquisition.

**Deposited vs annotated.** The PROXI record lists 73 files: 36 `.wiff`, 36 `.wiff.scan` and 1 `Library.group`. The FTP directory also holds `checksum.txt`.
- Every `.wiff` has a matching `.wiff.scan`; the sets are identical when checked in code. Each pair is one run, and `comment[data file]` is the `.wiff`.
- 36/36 runs are annotated.
- The names fit a full grid: `Swath_{NT|shMLKL}_{Control|RSL3}_{01-03}_{01-03}.wiff`, 9 runs per group.
- `Library.group` is the ProteinPilot search output of the spectral library. The DDA library runs behind it are NOT deposited, so they have no rows.

**Design (stated).** Paper Methods and Results (Fig. 5, Supplementary Fig. S5):
- Cells: HT-29 colorectal cancer cells, MLKL knockdown (shMLKL) vs non-targeting control (shNT, pLKO.1-puro).
- Conditions: basal ("Control" in the file names) vs 8 h RSL3.
- The S5 PCA shows the groups shNT_Basal, shNT_RSL3, shMLKL_Basal and shMLKL_RSL3, with 3 points each.
- File tokens map to groups: NT→shNT, shMLKL→shMLKL, Control→untreated/basal, RSL3→RSL3.

**Replicate structure (INFERRED).** Methods state that single injections were performed for each of the biological triplicates. The deposit has 9 runs per group, which contradicts this. I read the first index (`_01_`..`_03_`) as the biological replicate and the second as a repeat injection (`comment[technical replicate]`). The evidence: `.wiff.scan` sizes cluster by the first index. For example, NT_Control_02_* are all 2.6G, shMLKL_RSL3_02_* are all 2.3G and NT_RSL3_02_* are 3.3–3.4G (see `scratch/PXD078766/ftp_listing_sizes.tsv`). This fits one digest injected three times. No sample sheet or result table confirms it.

**Cell line.** HT-29, CVCL_0320 (paper gives the RRID; obtained from ATCC). Cellosaurus gives: female, 44Y, colon adenocarcinoma (NCIt C4349 = MONDO:0002271), derived from colon (UBERON:0001155). Culture medium was DMEM + 10% FBS (stated).

**Acquisition (paper Methods; instrument agrees with the PX record).**
- Sciex TripleTOF 6600+ (MS:1003456) with EASY-nLC 1000, 95 min gradient.
- SWATH-MS DIA with variable Q1 windows from the SWATH Variable Window Calculator. The collision energy "was different for each window". MS1 range 400–1500 m/z.
- Dissociation is recorded as CID (MS:1000133). This is the TripleTOF convention; the paper does not name it.

**Prep and search (paper Methods).**
- Preparation: 10 mM DTT, 12 mM IAA, trypsin 1:40 for 6 h.
- Search: ProteinPilot Paragon against human UniProt with "IAA alkylation", 1% FDR.
- Modifications: Carbamidomethyl C as Fixed (UNIMOD:4). Paragon's "IAA alkylation" setting = Cys carbamidomethyl. No other modifications are stated, and Paragon's variable (ID-focus) settings are not given. `Library.group` was not parsed: it is 523 MB and the shell has no internet.
- Tolerances: 25 ppm / 50 ppm are the PeakView MS / MS/MS extraction tolerances as stated. Paragon has no user-set search tolerance.

**Genotype / treatment encoding.**
- `characteristics[genotype]` holds shNT vs shMLKL. It is licensed by clinical-metadata, which also licenses compound, dose and exposure duration.
- `characteristics[treatment]` holds untreated vs RSL3.
- RSL3 rows: compound = RSL3, exposure duration = 8 hour.
- Factor values: genotype and treatment.

## Values left not available / not applicable
- `characteristics[dose]` = not available for RSL3 rows. No RSL3 concentration is stated in the Methods, the Results, the Fig. 3 and Fig. 5 legends, or the Supplementary S4–S7 legends. It is not applicable for untreated rows.
- `comment[collision energy]` = not available: rolling CE per window, no values given.
- `comment[scan window lower/upper limit]` and `comment[isolation window width]` = not available: variable windows, and the window table is not given.
- `comment[fractionation method]` = not applicable: single-shot runs.
- Which shMLKL construct (#1 TRCN0000194846 or #2 TRCN0000003227) was used for proteomics is not stated. The genotype says "MLKL knockdown (shMLKL)" without a number.
- Passage number, storage temperature and ancestry were left out (optional/recommended; not stated).

## Conflicts
- The paper says "single injections ... for each of the biological triplicates", but the deposit has 3 runs per biological sample. I kept all 36 runs and resolved the conflict as described above (INFERRED).
- PX `modifications` says "No PTMs are included in the dataset", but the paper states IAA alkylation. Carbamidomethyl is annotated as Fixed.

## Validation
- `parse_sdrf validate-sdrf --use_ols_cache_only` passes. I ran it with all five templates together and with each template on its own: "Everything seems to be fine".
- Ontology validation did not run (the OLS extras are not installed). I checked accessions live instead:
  - Ontobee: MS:1003456, MS:1000133, MS:1001251, MONDO:0002271.
  - Cellosaurus: CVCL_0320.
  - pride_cv.obo, GitHub release 2026-11-23: PRIDE:0000447, PRIDE:0000608, PRIDE:0000599.
  - The bundled unimod.xml: UNIMOD:4.
- EBI OLS4 and the PRIDE v3 API were down or rate-limited all day.

## Reviewer attack points
1. The `_BB_RR` = biological/technical reading, given that the paper says single injections per biological replicate.
2. Whether 25/50 ppm belong in the precursor/fragment tolerance columns: they are PeakView extraction tolerances, not search tolerances.
3. The RSL3 dose is missing, and the shMLKL construct is unnamed.
4. Possible unstated Paragon variable modifications. `Library.group` was not read.

## Review status
pending
