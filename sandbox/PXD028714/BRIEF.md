# PXD028714 SDRF annotation report

## Study
EIF5A hypusinaion in hepatic cells (PX title). Zhou J et al., "Spermidine-mediated hypusination of translation factor EIF5A improves mitochondrial fatty acid oxidation and prevents non-alcoholic steatohepatitis progression", Nat Commun 2022;13:5202, doi:10.1038/s41467-022-32788-x, PMID 36057633, PMC9440896. The paper's Methods cite PXD028714 (verified in the PMC full text), so the PX publication link is correct.

## Scope, evidence and decisions
Status: **sandbox**. 7 rows (7 RAW x label free), 38 columns; templates ms-proteomics + vertebrates + cell-lines (all declared on every row).

Deposited vs annotated: the ProteomeCentral PROXI record (Page URL checked for PXD028714) lists 9 files = 7 RAW (siCtrl, siDohh, sieIF5A, ctrl, FA, FA_sper, FASpersiD) + 2 Proteome Discoverer exports (HFX4_FPEP210000911-1A_PeptideGroups.txt, _Proteins.txt). This matches the campaign cache (7 RAW / 9 files). All 7 RAW are annotated; the 2 search outputs are not data files. The PRIDE FTP folder and the PRIDE v3 API returned upstream connection errors on three tries (2026-11-26/27), so no submitter metadata file, RAW header or PD export header could be read.

Samples (STATED, paper Methods, Results and Fig. 2/4 legends): AML12 mouse hepatocytes (ATCC CRL-2254) in DMEM:F12 + 10% FBS + insulin/transferrin/selenium/dexamethasone. Label-free LC-MS/MS by Novogene on "pooled (n = 2) cell pellets for each experimental condition", one run per condition ("lack of replicates from proteomics data"), so biological replicate = 1 and pooled sample = pooled on every row. Run -> condition mapping is from the file names, which match the paper's conditions one-to-one:
- siCtrl = negative control siRNA 20 nM 48 h; siDohh = Dohh siRNA s97895; sieIF5A = Eif5a siRNA s114771 (Fig. 2 legend, Methods).
- ctrl = no FA; FA = 0.5% BSA-conjugated 0.6 mM palmitic + 0.17 mM oleic acid 48 h; FA_sper = FA + 100 uM spermidine 48 h (Results, Fig. 3).
- FASpersiD = Dohh siRNA 24 h then FA + Spd 48 h (Fig. 4 legend, Fig. 4c "FA + Spd+siDohh vs FA + Spd").

Cell line metadata from Cellosaurus CVCL_0140 (verified live): liver (UBERON:0002107), hepatocyte (CL:0000182), male, CD-1 MT42 transgenic (TGFA transgene), age 5M -> developmental stage "adult" (INFERRED from 5 months), no disease line -> "normal" (non-transformed hepatocyte line).

Instrument: **Q Exactive HF-X (MS:1002877)** per paper Methods ("Q Exactive HF-X mass spectrometer") and the deposited search-output file prefix "HFX4" (Novogene instrument name); the PX record says Q Exactive HF (MS:1002523). RAW headers not read (FTP down) -> unresolved conflict, resolved in favour of the paper.

Prep (STATED): urea/SDS lysis, 10 mM DTT, iodoacetamide, acetone precipitation, trypsin, Proteome Discoverer 2.2, UniProt mouse 2021_3_9. Carbamidomethyl C fixed: IAA alkylation is stated and the PX record lists MOD:00397 (iodoacetamide derivatized residue); the PD search mods were NOT read (PD export headers unreachable) -> Fixed type INFERRED; no variable mods annotated because none are stated.

Accessions verified live: MS:1002877, MS:1001251, MS:1000422 (Ontobee), CL:0000182, UBERON:0002107 (Ontobee), UNIMOD:4 (unimod.org), CVCL_0140 (Cellosaurus). PRIDE:0000627/0000608/0000599 could not be checked live (EBI OLS down); they are the same NT/AC pairs as earlier reviewed campaign files.

## Values left not available / not applicable
- precursor / fragment mass tolerance: not available (not in paper; PD exports unreadable).
- passage number: not available (not stated).
- No LC gradient, MS1/MS2 settings or NCE are stated, so those columns are omitted.

## INFERRED (why sandbox)
1. Data acquisition = DDA and dissociation = HCD: not stated; inferred from label-free Q Exactive HF-X + PD 2.2 (Novogene standard).
2. Instrument HF-X vs PX HF: paper + file prefix vs PX record; RAW header unread.
3. Carbamidomethyl as a Fixed search modification; other search mods unknown.
4. Whether ctrl/FA/FA_sper cells also received siNeg (as in the Fig. 4e Seahorse design) is not stated for the proteomics; treatment text records only what is stated.
5. sieIF5A.raw is deposited but no siEif5a proteomics comparison is reported in the paper; it is annotated from the file name and the Fig. 2 siRNA description.
6. Developmental stage "adult" from Cellosaurus age 5M.

## Conflicts
- Instrument: PX Q Exactive HF vs paper Q Exactive HF-X (see above).
- PX modifications list only MOD:00397; consistent with IAA alkylation.

## Review status
pending
