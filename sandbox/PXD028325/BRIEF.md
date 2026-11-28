# PXD028325 SDRF annotation report

## Study
Identification of splicing legumain from Momordica cochinchinesis (PRIDE PXD028325). Paper: Liew HT et al., "The legumain McPAL1 from Momordica cochinchinensis is a highly stable Asx-specific splicing enzyme", J Biol Chem 2021;297(6):101325, doi:10.1016/j.jbc.2021.101325, PMID 34710371, PMC8600085. The paper's Data availability cites PXD028325 and PXD028327 (link verified, but it does not say which dataset holds what).

## Scope, evidence and decisions
Status: sandbox. 10 rows x 28 cols, templates ms-proteomics + plants (v1.1.0).

- Deposited files (PROXI record, re-derived; the PRIDE FTP and the EBI APIs timed out today): 12 = 10 MALDI `.t2d` spectra (`H1_MS_1.t2d` + 9 `H1_MSMS_<precursor m/z>_<n>.t2d`) + Mascot `F062367.dat` + `F062367.csv`. Campaign cache "10 RAW / 12 files" confirmed. All 10 `.t2d` are annotated (10/10), one row each; the .dat/.csv are search outputs, not runs.
- Sample: PX description = seed extract of M. cochinchinensis with legumain activity, analysed by MALDI-TOF MS/MS to identify the co-eluted lectin. Paper: "A galactose-specific lectin was identified in the fraction with McPAL activity" / "seed lectin coeluted with McPAL1 by MALDI-TOF-TOF MS/MS". All files share prefix `H1` -> one source (one spot/sample), biological replicate 1. Since (source, bio rep, tech rep, fraction) must be unique, the 10 spectra (1 MS + 9 MS/MS precursors of the same spot) get comment[technical replicate] 1-10 — a structural device, not real replicates.
- Organism Momordica cochinchinensis (NCBITaxon 3674, from PX record); organism part seed (fresh, decoated seeds, paper); disease normal; material type tissue.
- Tolerances 50 ppm MS / 0.5 Da MS/MS: stated for the MALDI-TOF-TOF Mascot Daemon searches (database = TransDecoder ORFs from the seed transcriptome).
- Dissociation CID, MS2 analyzer TOF: implied by TOF/TOF instrument (INFERRED, standard for this platform). Acquisition method "Data-dependent acquisition" is the nearest available term for manual precursor selection on MALDI TOF/TOF (judgement call).

## Conflicts / INFERRED
- Instrument: PX record says 5800 TOF/TOF (MS:1001482); paper Methods say "MALDI-TOF-TOF (Applied Biosystems, 4800)" (MS:1000140). Following precedence (paper > PX) I used 4800 Proteomics Analyzer. But the 4800 sentence describes McPAL1 preliminary sequencing, not explicitly the lectin run, and the .t2d/.dat headers could not be read (FTP down). Unresolved; reading `F062367.dat` header (Mascot INSTRUMENT / search params) would settle it.
- Cleavage agent: Trypsin is INFERRED. Paper describes in-gel digestion of McPAL1 bands with trypsin OR chymotrypsin; enzyme for the lectin sample is not stated. Column forbids reserved words. The Mascot .dat CLE= line would settle it.

## Values left not available / not applicable
- developmental stage, strain or breed: not stated (no cultivar/source/supplier given).
- reduction / alkylation reagent: DTT 5 mM / IAA 20 mM are stated only for McPAL1 gel bands; the lectin was identified "in the fraction", prep unstated -> not available.
- modification parameters: not stated in paper; PX says "No PTMs"; .dat unread -> not available.
- No factor value: single sample, no comparison (CI advisory no_factor_value).

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics --template plants`: no errors (ontology checks skipped: OLS deps not installed; OLS live was unreachable, so accessions MS:1000140, MS:1001251, MS:1000133, MS:1000084, MS:1002038, PRIDE:0000627 were NOT re-verified live this run). `sdrf_review.py`: [OK], advisory no_factor_value.

## Review status
pending
