# PXD000998 SDRF annotation report

## Study
Gastric cancer_iTRAQ: tanshinone IIA (TIIA) vs DMSO in the AGS gastric adenocarcinoma cell line, iTRAQ 4-plex, Waters Synapt G2 HDMS.
Paper: Lin LL et al., "Integrating transcriptomics and proteomics to show that tanshinone IIA suppresses cell growth by blocking glucose metabolism in gastric cancer cells", BMC Genomics 2015;16:41. PMID 25652794, PMC4328042, DOI 10.1186/s12864-015-1230-0. The paper's Data Availability section cites PXD000998 and 10.6019/PXD000998, so the PX-to-paper link is verified. The lab is at National Taiwan University (the record is in the Singapore batch).

## Status: sandbox
The SDRF validates. The channel-to-condition map is STATED. The run-to-replicate structure (what the two RAW files are) is INFERRED (see below).

## Scope, evidence and decisions
- **Deposited files** (re-derived from the PRIDE FTP listing and README.txt; the PRIDE v3 API was down): 2 RAW (`iTRAQ_20121120.raw.zip` 598M, `20121130_iTRAQ.raw.zip` 655M), 2 MGF, 1 `MascotDAT.dat-pride.xml.gz`, plus `generated/` (mgf and mzTab converted by PRIDE). This matches the cache (2 RAW / 5 files). README maps the single Mascot result to both RAW files and both MGFs, so it was one merged search.
- **Annotated:** 8 rows = 2 RAW x 4 iTRAQ channels, so every RAW is annotated. MGFs and the result file are not data-file rows.
- **Channel map (STATED):** "control samples labeled by 114 or 115; TIIA-treated samples labeled by 116 or 117" (Methods). Additional file 5 legend: control peptides "equally divided into two parts, C1 and C2, and labeled with iTRAQ 114 and 115"; treatment peptides likewise split into T1/T2 (116/117). So 114/115 are a peptide-level split of ONE control sample, and 116/117 of ONE TIIA sample. I modelled these as two source names (`AGS_DMSO_control`, `AGS_TIIA`), biological replicate 1, with the label distinguishing the split portions. No biological replication exists in the proteomics arm.
- **Treatment (STATED):** 5.3 uM TIIA (IC50; Sigma T4952) or 0.1% DMSO for 48 h; RPMI 1640 + 10% FBS. Cell line: AGS (ATCC CRL-1739) = CVCL_0139. Cellosaurus (live) gives 54Y, female, gastric adenocarcinoma (NCIt C4004), and EFO_0002109.
- **Two RAW files = technical replicate 1/2 (INFERRED):** The Methods say "All labeled peptides were mixed and analyzed by LC-MS/MS" and never state the number of injections. The two RAW files (2012-11-20 and 2012-11-30) are searched together in one Mascot result. The most likely reading is two injections of the same pooled 4-plex mixture, but they could also be separately labelled preparations. Because of this, the file is `sandbox`, not `annotated`.
- **Instrument (STATED + consistent):** PX says Synapt G2 HDMS (MS:1001777, verified on ontobee), and the paper says "Waters SYNAPT G2 HDMS (LC-ESI-Q-TOF) with nanoACQUITY UPLC". The MGF (Mascot Distiller 2.3.2) references `F:\20121130_iTRAQ.raw`. Its spectra carry Waters function numbers f=2..4 (1 survey + 3 MS/MS functions = the stated top-3 DDA) and show 114-117 reporter ions. iTRAQ on a Synapt is unusual but consistent across all three sources. The RAW `_extern.inf`/`_HEADER.TXT` inside the zips was NOT read (no range access from the shell), and only the first ~44 KB of one MGF was read; the second MGF request timed out.
- **Dissociation:** CID (MS:1000133). Not stated in the paper; INFERRED from the instrument (Synapt fragments by trap/transfer CID only).
- **Search (paper; the Mascot .dat was not opened):** Mascot 2.3.02, Swiss-Prot human, trypsin with up to 2 missed cleavages, +-0.1 Da precursor and fragment. Variable modifications: deamidation (NQ), oxidation (M), iTRAQ (N-term, K), methylthio (C). The paper lists no fixed modifications, so all five are annotated as Variable, iTRAQ included, as stated. Accessions were checked live on unimod.org: UNIMOD:214 iTRAQ4plex, UNIMOD:7 Deamidated, UNIMOD:35 Oxidation, UNIMOD:39 Methylthio. The PX `modifications` field (MOD:00425, 01499, 01294, 01153) is consistent with these. Its "deamidation in presence of O18" is a PRIDE-XML mapping artefact.
- **MS1 range:** 350-1700 m/z (stated).

## Values left not available / not applicable
- `comment[reduction reagent]`, `comment[alkylation reagent]`: not available. The paper says only "reduction, alkylation". The Methylthio (C) search mod strongly suggests MMTS (the iTRAQ kit reagent), but that is not stated, so I did not assert it.
- `comment[fractionation method]`: not available. No fractionation is described. One RAW per injection, so fraction identifier = 1.
- Gradient, collision energy: not stated, so the columns are omitted.

## Conflicts
- None material. The paper's column dimensions read "180 mm x 2 cm" / "75 mm x 25 cm ... 1.7 mm" (sic, um intended); not used.
- The PX contact affiliation is NTU Taipei, not Singapore (batch placement only).

## Verification limits
- EBI OLS and the PRIDE API were down (upstream connect errors). WebFetch was rate-limited or out of quota for OLS. The local `parse_sdrf` OLS cache cannot load (fastparquet missing), so validation was structural only. A mutation test (dropping `comment[label]`) confirmed that the validator does fail on errors.
- Labels with no accession in the file (`stomach`, `epithelial cell`, `gastric adenocarcinoma`, `adult`, `female`) were not checked live against OLS today. The validator also confirmed nothing about ontology terms, so a reviewer must check these.
- Verified live: Cellosaurus CVCL_0139; MS:1001777 and MS:1001251 (ontobee); UNIMOD 214/7/35/39 (unimod.org). PRIDE:0000627 and MS:1000133 were not re-checked live; both are used widely in validated campaign files.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics --template human --template cell-lines`: "Everything seems to be fine" (structural only; OLS unavailable). `sdrf_review.py`: [OK].

## Review status
pending
