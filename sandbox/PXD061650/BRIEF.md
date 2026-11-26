# PXD061650: sandbox status (not ready for datasets/)

**Why it is in sandbox:** the SDRF is complete and independently reviewed (two rounds; all 48 RAW files match PRIDE and all 696 channel assignments match the deposited pdResult StudyInformation), but it has two template/identity problems that cannot be resolved from public sources:
1. The 48 pool-channel rows have `pooled` in `characteristics[cell line]` and `factor value[cell line]`. The template forbids `pooled`, `not available` and `not applicable` there, and a pool across several lines has no compliant value (the validator only warns).
2. The 72 KOLF2-SF rows (set 1 channels 133N/133C/134N) are annotated as KOLF2 by inference. The meaning of "SF" is not stated anywhere, and the paper says these samples were excluded.

## To resume
- Find out what "KOLF2-SF" is (ask the submitters, or check the paper's supplement); fix the cell line, treatment and organoid competence of those 72 rows accordingly, or drop them.
- Decide how to encode the 48 pool rows (a compliant cell-line value, or a template change upstream), or drop them and accept an incomplete channel-to-file map.
- Optional: add `characteristics[ancestry category]` (Cellosaurus: Caucasian for the HPSI lines); the cell line column mixes Cellosaurus (HPSI...) and BTO-style (`WA-01 cell`) labels, which do not resolve in CLO/BTO/EFO.
- Then promote to `datasets/` in a dedicated PR after a fresh adversarial review.

Files here: `PXD061650.sdrf.tsv` (current draft), `PXD061650.evidence.json` (evidence manifest). The annotation report follows, from the NordicSDRF campaign (Odense/SDU datasets); its 'Review status' section is the review log.

---

## PXD061650 SDRF annotation report

## Study
"Optimizing PSC culture for generating neural organoids" (Sutcliffe, Jensen, Tan, Morris, Fazakerley, Larsen, Lancaster; Stem Cell Reports 2026, doi:10.1016/j.stemcr.2025.102724, PMID 41349536). Six human pluripotent stem cell lines (H9, H1, kolf2 = organoid-competent; sojd3, burb1, fiaj1 = non-competent), 4 biological repeats each, cultured in E8 on vitronectin. SDC lysis, DTT/iodoacetamide, methylated trypsin, TMTpro 16-plex (two sets, one pooled reference channel each), TiO2 phosphopeptide enrichment, high-pH fractionation (12 fractions) of the phospho and non-modified (TiO2 flow-through) peptides, Orbitrap Eclipse DDA. Submitter Pia Jensen, SDU (Larsen lab).

## Templates
ms-proteomics v1.1.0 + human v1.1.0 + cell-lines v1.1.0. Not clinical/oncology (no patient or disease). TMT plex handled by comment[label] channels.

## Scope: deposited vs annotated
PRIDE file list read over all pages (page 0 = 50 files, page 1+ empty): 48 RAW (Eclips_01864..01911_LAJ.raw) and 2 .pdResult search files. All 48 RAW annotated: each RAW x 16 TMTpro channels, minus 3 unused channels in set 2 = 696 rows x 51 columns. The 2 pdResult files are not annotated as data rows.
- RAW headers (HTTP range): sample name "Madeline Lancaster 1/2 [NON] modified A1..A12" gives set and enrichment: 01864-01875 phospho set 1, 01876-01887 non-modified set 1, 01888-01899 phospho set 2, 01900-01911 non-modified set 2.

## Key decisions
- Channel map read from the StudyInformation table of the deposited pdResult files (identical in the non-modified and phospho searches): set 1 = BURB1 x4, FIAJ1 x4, KOLF2 x4, Mix (132C), KOLF2-SF x3 (133N, 133C, 134N); set 2 = H1A x2, H1B x2, H9 x4, SOJD3 x4, Mix (132C), NO x3 (133N, 133C, 134N). Consistent with the PRIDE processing protocol text (3 KOLF2-SF excluded, 3 NO channels unused, H1A/H1B replicates).
- NO channels: rows with empty source (no row emitted). KOLF2-SF and Mix channels kept as rows (acquired, labelled).
- Source name = line_repN_{nonmodified|phospho}: the TiO2 eluate and flow-through are separate injection series of the same TMT set, so each has its own source; characteristics[enrichment process] = enrichment of phosphorylated protein (EFO:0010806) for phospho, not applicable for the flow-through.
- Cell lines from the supplement's Cell lines section (sex) and Cellosaurus: H9 = WA09 CVCL_9773 (female), H1 = WA01 CVCL_9771 (male), kolf2 = HPSI0114i-kolf_2 CVCL_AE29 (male), sojd3 = HPSI0314i-sojd_3 CVCL_AE87 (female), burb1 = HPSI0714i-burb_1 CVCL_AG74 (male), fiaj1 = HPSI0514i-fiaj_1 CVCL_AF79 (male). Cell type: embryonic stem cell (CL:0002322) for H9/H1, pluripotent stem cell (CL:0002248) for the iPSC lines (PRIDE record).
- Factors: cell line and organoid competence (competent/non-competent per paper).
- Acquisition DDA (PRIDE:0000627), Orbitrap Eclipse (MS:1003029), Trypsin, DTT (PRIDE:0000608), iodoacetamide (PRIDE:0000599), hpHRP (PRIDE:0000564), 10 ppm.
- Non-modified runs: MS2 CID 35 NCE in ion trap, fragment tolerance 0.8 Da, SPS-MS3 HCD NCE 55 (protocol). Phospho runs: HCD 36 NCE, Orbitrap 50K (RAW header of 01864), fragment tolerance 0.05 Da (Sequest HT workflow in the phospho pdResult).
- Modifications from the pdResult Sequest HT workflows: Carbamidomethyl C, TMTpro K and N-term fixed (all rows); Phospho STY and Deamidated N variable (phospho rows only; blank cells in the flow-through rows). The blanking of those two repeated columns was done by a post-build script (build cannot vary repeated columns per row).

## Not available values
disease, age, ancestry, individual, passage number (<50 + <25 stated only as bounds), culture medium (Essential 8 has no NCIT term), storage temperature, developmental stage, organism part (no anatomical source stated for cultured cells), phospho/non-modified acquisition date and scan ranges (omitted).

## Conflicts / overrides
- tools check "hallucinated" for the HPSI cell line names (8 groups of rows): iPSC HPSI lines are not in CLO/BTO/EFO; WA01/WA09 written as BTO labels "WA-01 cell"/"WA-09 cell". Cellosaurus accessions are the identity. The bundled curated cell line DB maps "H9" to a Sezary T-cell line; not used.
- PRIDE protocol describes only the SPS-MS3 method; the phospho acquisition (OTOT 120 min HCD MS2) comes from RAW headers.

## Inferred vs stated
Stated: lines, sex, TMTpro, enrichment, fractionation, instrument, tolerances, modifications, channel map (deposited PD study definition). Inferred: biological replicate numbering within a line by ascending channel order (Table S2 column names H1A.1,H1A.2,H1B.3,H1B.4 give numbers but no channels); KOLF2-SF annotated as kolf2 (meaning of SF not stated); phospho acquisition settings from header of 01864 applied to all 24 phospho runs; pooled reference = mix of all samples of the set; dissociation of non-modified rows recorded as CID (MS2), the MS3 HCD step is not representable.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` (ms-proteomics + human + cell-lines, 2 rounds): remaining error is the known cache artifact "study sample" (PRIDE:0001013, valid live); round 1 also flagged age value "pooled" for the pool channels (changed to not available, sample type pooled instead) and culture medium Essential 8 (changed to not available). Remaining warnings: cell line names not in CLO/BTO/EFO (cache-only). `tools structure` OK; `tools score` 100/100; `tools reconcile` clean after organism part set to not available; `tools check` reports the cell line names above. Live OLS4 resolution of all NT/AC terms succeeded.

SDRF: 696 rows x 51 columns, sha256 f3c3e656617fe8854b4e2b5f2d0e21d16ee029cb1055007c4f54b89a04f6bc74

## Review status
Independent round 1 (fresh-context reviewer, sha256 f3c3e656617fe8854b4e2b5f2d0e21d16ee029cb1055007c4f54b89a04f6bc74) = FAIL, 3 important, 5 minor. No review-gate receipt was written. Verified: 48/48 RAW files match PRIDE (all pages); all 696 channel assignments match both deposited pdResult StudyInformation tables with 0 mismatches (set 2 channels 133N/133C/134N are 'NO' and correctly absent); phospho acquisition (HCD 36 NCE, Orbitrap 50K) confirmed in the headers of 01864, 01870, 01875, 01888 and 01899; Cellosaurus accessions and sex match; `tools score` 100; `tools check` flags only the HPSI cell-line names (Cellosaurus confirms them). Fixes: (1) `characteristics[culture medium]` set to `Essential 8 medium` on the 648 non-pool rows (paper Results: all lines cultured in E8 on vitronectin), `not applicable` on pool rows; (2) `characteristics[cellosaurus name]` for WA01/WA09 rows corrected from the BTO labels to the Cellosaurus names `WA01` and `WA09`; (3) pool rows: sex set to `not applicable`. NOT applied: for the KOLF2-SF rows (72 rows) the reviewer suggested `not available` for biological replicate, and for pool rows `not applicable` for cell line, but the ms-proteomics/cell-lines templates reject both values (`allow_not_available`/`allow_not_applicable` false), so the KOLF2-SF rows keep replicates 1-3 within their own group (the meaning of 'SF' is unknown; the paper excluded these samples) and pool rows keep `pooled`. Minor: replicate numbers inferred from channel order; ancestry (Caucasian, Cellosaurus) not added; the same TMT sample appears as two sources (`_nonmodified` / `_phospho`); MS3 HCD not representable in the dissociation column. Round 2 (fresh-context, targeted reviewer, sha256 b8cea85885cf54789ea60f41aaea74a57802db6167f62703d2c829e9b2a99079) = verdict PASS, 0 blocker / 1 important not treated as blocking / 3 minor. No review-gate receipt was written. Verified: culture medium `Essential 8 medium` stated in the paper (Results and Methods); Cellosaurus names WA01/WA09 and the four HPSI accessions consistent on every row; 333 (file, channel) pairs from one pdResult StudyInformation (all 24 non-modified files, both sets) match the SDRF with 0 mismatches (phospho files 01864-01875 and 01888-01899 not re-checked in round 2, but covered by round 1); 48/48 RAW files match PRIDE. Important (documented deviation, accepted by the reviewer as non-blocking): `characteristics[cell line]` and `factor value[cell line]` are `pooled` on the 48 pool rows, which the template forbids (`allow_pooled` false for cell line; the validator reports only an unresolved-ontology warning); no compliant value exists for a pool across several lines, and dropping the pool rows would leave the channel-to-file mapping incomplete. Note: under the strict review contract an important finding means FAIL, so this file should be treated as 'passed with one documented template deviation', not as a clean pass. Minor: KOLF2-SF rows (72) are treated as KOLF2 by inference, `factor value[organoid competence]` is `not available` and nothing marks the SF condition; cell line column mixes Cellosaurus (HPSI...) and BTO-style (`WA-01 cell`, `WA-09 cell`) labels, unresolved in CLO/BTO/EFO.
