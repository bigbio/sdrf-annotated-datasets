# PXD030613 SDRF annotation report

## Study
Venomics analysis of Thai Daboia siamensis using integrated omics data (PX title). Paper: Saethang T, Somparn P, et al. "Identification of Daboia siamensis venome using integrated multi-omics data", Sci Rep 2022;12:13140, doi:10.1038/s41598-022-17300-1, PMC9338987, PMID 35907887. The PX record still says "publication pending"; the paper was matched by title, submitter (Somparn, Chulalongkorn) and its Data availability statement, which cites PXD030613.

## Scope, evidence and decisions
Status: **sandbox**. 36 rows (36 RAW, label-free) x 34 columns. Templates: ms-proteomics v1.1.0 + vertebrates v1.1.0.

- **Organism (PX record is wrong).** The PX/PRIDE species field says *Arabidopsis thaliana* (3702). The title, keywords, paper and every file name show the sample is crude venom of *Daboia siamensis* (eastern Russell's viper). I used `Daboia siamensis`, NCBITaxon:343250, checked live with NCBI eutils taxonomy.
- **Sample.** There is one biological source: crude venom from one adult male snake. It came from the QSMI snake farm (Thai Red Cross) and was caught in Sakaew province, Thailand. All rows use `source name` = `Daboia_siamensis_crude_venom_male1` with biological replicate 1. The female snake was used only for genome and transcriptome work. organism part = `venom` (UBERON:0007113, a secretion of an exocrine gland). sex = `male` and developmental stage = `adult` are STATED. disease = `normal`, because the snake was a healthy captive animal.
- **Deposited vs annotated runs.** 36/36 RAW are annotated and no run is excluded. The 20 files that are not RAW are not data rows: 17 MGF (peak lists for Gel_Venom1-13 and S_Venom1, 2, 3, 10 only), checksum.txt, protein-peptides.xlsx (PEAKS export) and Snake_smsnet_m-mod_fdr5_final_report.tsv. The set check between the PX file list and the SDRF `comment[data file]` values passes, with no missing and no invented runs.
  - `Gel_Venom1_20200627142538.raw` and `Gel_Venom2..13.raw` are in-gel set 1, fractions 1-13. The paper STATES that the SDS-PAGE lane was "cut into 13 fractions from top to bottom". Gel slice N = file N is INFERRED from the numbering.
  - `Venomset2_1..13.raw` are in-gel set 2, fractions 1-13, with technical replicate 2. **INFERRED**: the paper never mentions a second gel or lane. The 13-file series matches the 13 gel slices, so I took it as a repeat of the in-gel workflow on the same venom. It could instead be a second lane, a re-injection, or a different venom aliquot. I could not check Supplementary Table S6 or Fig. S1 (gel image), and the deposited search outputs were unreachable.
  - `S_Venom1..10.raw` are in-solution digests fractionated with the Pierce high-pH RP kit, fractions 1-10. The paper does not state the fraction count. The kit nominally gives 8 fractions, and 10 files were deposited (perhaps flow-through or wash fractions added). Fraction N = file N is INFERRED.
- **Instrument (conflict, unresolved).** The PX record says Q Exactive HF (MS:1002523). The paper Methods say "Q Exactive Plus Hybrid Quadrupole-Orbitrap". I used **Q Exactive Plus (MS:1002634)**, following the precedence paper > PX fields. The stated 70,000 / 17,500 resolution settings are typical of a Q Exactive Plus (the HF uses 60k/15k), which supports this choice. The RAW headers could NOT be read: the shell has no internet, and on 2026-11-25 both PRIDE FTP-over-https and the PRIDE v3 API returned upstream connect errors in the cloud browser. This is the main reason for sandbox status.
- **Acquisition and search (paper Methods, STATED).** DDA top-10, HCD at 28% NCE, MS1 200-2000 m/z. Search in PEAKS Studio 8.5 with trypsin, at most 1 missed cleavage, parent and fragment tolerance both 10 ppm (as stated, even though 10 ppm fragment is unusual for PEAKS). Modifications: Carbamidomethyl C fixed (UNIMOD:4); variable Oxidation M (UNIMOD:35), Acetyl protein N-term (UNIMOD:1, PP=), Phospho S/T/Y (UNIMOD:21) and Deamidated N/Q (UNIMOD:7). The deposited files hold no search-parameter file, and the two result tables were unreachable today. The modifications therefore come from Methods, not from deposited search settings. PX `modifications` lists only MOD:00397 (iodoacetamide derivatized residue), which agrees with the fixed modification. Reduction was DTT and alkylation IAA in both workflows (stated).
- **Fractionation method.** In-gel rows use `SDS PAGE` (PRIDE:0000568). In-solution rows use `High-pH reversed-phase chromatography (hpHRP)` (PRIDE:0000564).
- **No factor value column.** The dataset is one sample characterised two ways; there is no experimental variable. The prep workflow appears in assay names and in `comment[fractionation method]`.
- **Accession checks.** OLS4 was down, so terms were checked live elsewhere:
  - ontobee: UBERON_0007113 venom, MS_1002634, MS_1000422 (beam-type CID; exact synonym HCD), MS_1001251 Trypsin, EFO_0001272 adult, PATO_0000461 normal.
  - PRIDE CV obo on GitHub (release 2026-11-23): PRIDE:0000568, 0000564, 0000627, 0000608 "Dithiothreitol (DTT)", 0000599 "Iodoacetamide (IAA)".
  - unimod.org records 1, 4, 7, 21 and 35.
  - NCBI eutils for taxon 343250.

## Values left not available / not applicable
- `characteristics[strain or breed]` = `not applicable`: the snake was wild-caught and has no strain or breed. Geographic origin (Sakaew, Thailand) has no licensed column under these templates, so it is recorded only here.
- `characteristics[material type]` is omitted (optional). None of the fixed values (tissue, cell, organism part, ...) cleanly describes a secretion.
- No value had to be set to `not available`.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only`, run without a template and again with `--template ms-proteomics` and `--template vertebrates`: no errors. Ontology validation did not run because the OLS extras are not installed, so this proves well-formedness only. A mutation test with `BOGUS999` as the organism also passed. Every accession above was therefore checked by hand.

## Stated vs INFERRED
- STATED: organism; venom source; one adult male donor; 13 gel fractions; in-solution hpH fractionation; instrument per paper; DDA/HCD/NCE; scan range; tolerances; modifications; reagents.
- INFERRED: file number = fraction number; Venomset2 = second in-gel set of the same venom (technical replicate 2); 10 hpH fractions; disease `normal`.

## Conflicts
- PX species *Arabidopsis thaliana* vs actual *Daboia siamensis*. Resolved to *Daboia siamensis* (title, keywords, paper, files).
- PX instrument Q Exactive HF vs paper Q Exactive Plus. Paper used; not verified against RAW.
- Paper Results say "venom gland" proteins; Methods say crude venom. Methods used (organism part = venom).

## Review status
pending
