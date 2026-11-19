# PXD022056: sandbox status (not ready for datasets/)

**Why it is in sandbox:** Independent review round 1 = FAIL (2 important). Lys-C was added afterwards, but the modification set for the MPO/control runs (rows 13-27) was never checked.

## To resume
- Open `P07_E01_Progenesis-_2_.msf` (the search for the MPO, control and protein-control runs) and set `comment[modification parameters]` for rows 13-27 from it; the HOCl runs (rows 1-12) were read from `P03_E04`.
- Reconcile with the paper/PRIDE list: chlorination/dichlorination on Y and W, oxidation on M, H, C and W (His oxidation and Trp chlorination are currently missing); Deamidated N/Q appears only in the msf.
- Consider `negative control` for sample type on control rows, `not applicable` organism part, shorter treatment text, and the QEHF3 vs QHF2 batch confound note.
- Re-run `parse_sdrf` with live OLS and request a fresh adversarial review (round 2).

Files here: `PXD022056.sdrf.tsv` (current draft), `PXD022056.evidence.json` (evidence manifest: claim, source, confidence per field). The annotation report follows, written by the annotator from the NordicSDRF campaign (Odense/SDU datasets). Its 'Review status' section is the review log.

---

## PXD022056 SDRF annotation report

## Study
Label-free MS of murine laminin-111 (Sigma) oxidised/chlorinated by HOCl (0, 100, 500 uM, 4 biological replicates each; 1 h, 21 C) or the MPO/H2O2/NaCl system (3 replicates) with controls omitting H2O2, MPO or NaCl and an untreated protein control (Nybo et al., Redox Biol 2019, PMID 30476874, PMC6260226). Q Exactive HF, DDA, HCD NCE 28, 60 min gradient.

## Templates
ms-proteomics v1.1.0 + vertebrates v1.1.0 (mouse protein; no clinical, cell-line or crosslinking templates apply).

## Scope: deposited vs annotated
PRIDE lists 34 files (one page of 100 returned all; page 1 empty): 27 RAW, 2 .msf, 2 .mgf, 2 FASTA, 1 xlsx. Annotated all 27 RAW files = 27 rows x 38 columns. Search outputs (msf, mgf, fasta) are not annotated as rows.

## Key decisions
- Run-to-sample map: deposited PRIDE_files_Lamini.xlsx (treatment, concentration, replicate, RAW name). RAW names in the xlsx lack the `_0` suffix present in the archive for QEHF3_02443-02452; matched by stem to the real archive file names.
- Single factor value[treatment] (condition string, also in characteristics[treatment]).
- Instrument Q Exactive HF (RAW headers of QEHF3_02443, QEHF3_02453, QHF2_03505, QHF2_03508: "Q Exactive HF - Orbitrap MS", method NCE28 HCD) matches PRIDE.
- Modifications read from deposited P03_E04-(2).msf (HOCl search, via search-params): custom PD mods mapped by delta mass/residue to Unimod: -O1 (C,M) and oxidation(W) -> Oxidation; -O2(C,M) -> Dioxidation; -O3(C) -> Trioxidation; -Cl(Y) -> Chlorination (+33.961); -Cl2(Y) -> dichlorination; Deamidated N,Q variable. No fixed modification (a dummy MascotXValue substitution is not a real modification).
- No reduction/alkylation (paper: digestion without them): reduction and alkylation reagent = not applicable.
- Cleavage agent Trypsin (paper/PRIDE search "trypsin, 2 missed cleavages"); the deposited msf names semiTrypsin.
- Treatment sampling: HOCl 1 h/21 C and MPO 37 C stated; MPO incubation duration not stated for the MS samples, so no sampling time column.

## Values not available / not applicable
organism part, strain or breed: not available (Sigma laminin-111 source tissue/strain not stated in the deposit; PRIDE lists no organism part). disease, cell type, sex, developmental stage: not applicable (purified protein). reduction/alkylation reagent: not applicable.

## Conflicts
- Paper: chlorination at Y and W, oxidation also on H, and Trp dichlorination; deposited P03 msf: chlorination only Y, oxidation C/M/W, plus Deamidated N,Q. msf used (deposit), applied to all rows.
- Only the HOCl msf (P03_E04) was fully parsed; the MPO msf (P07_E01, 1.3 GB) was not opened; the PRIDE/paper text gives the same search for both.
- Cleavage: msf semiTrypsin vs paper Trypsin; Lys-C step (two-step LysC then trypsin) cannot be expressed because the cleavage agent column is single-valued; reconcile flags this (cleavage_agent_incomplete, Lys-C missing) and it is a known template limitation.

## Inferred vs stated
Stated: organism, treatments, replicates, run map (xlsx), instrument, NCE 28, tolerances 4 ppm / 0.1 Da, top-12 DDA. Inferred: HCD (paper states HCD collision energy 28), Orbitrap MS2 (15,000 resolution on QE HF), source names, technical replicate 1, fraction 1 (unfractionated; single run per sample), sample type `study sample` for all rows including controls, treatment string wording.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` (one round): the lone error "study sample ... not found in pride" (cache artifact; PRIDE:0001013 valid live) and 8 warnings that characteristics[treatment] free text is not in NCIT/EFO. `structure` OK. All NT=;AC= terms resolved live in OLS4 (MS:1001251, MS:1000422, MS:1002523, MS:1000484, PRIDE:0000627, UNIMOD:7/35/345/425/936/937).

## Review status
Independent round 1 (fresh-context reviewer, sha256 d184eafeafa4df4d79703140aa4a889b3d6fb236aae884d0a69d1df9fe24b40b) = FAIL, 2 important + 1 incomplete validation. (1) Lys-C omitted: fixed, second `comment[cleavage agent details]` column `NT=Lys-C;AC=MS:1001309` on all 27 rows. (2) Modification set was parsed only from the HOCl search file (P03_E04); the MPO/control runs (rows 13-27, search P07_E01) were not checked, and His oxidation / Trp chlorination from the paper are absent while Deamidated N/Q appears only in the msf: NOT fixed, needs a read of P07_E01_Progenesis-_2_.msf. (3) The reviewer's venv lacked OLS extras so `tools check` flagged 4 UNIMOD terms (425, 345, 936, 937) that it resolved live. Minor: negative-control sample type, organism part, free-text treatment, batch confound between QEHF3 and QHF2 series. Round 2: pending
