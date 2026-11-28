# PXD019542 SDRF annotation report

## Study
A primary human T-cell spectral library to facilitate large scale quantitative T-cell proteomics. Weerakoon H et al., Sci Data 2020;7:412, DOI 10.1038/s41597-020-00744-3, PMID 33230158, PMC7683684. PX record links PMID 33230158; the paper's Data Records name PXD019542 as "raw SWATH-MS files from the CD4+ T-cell activation time series, plus PeakView results/quantification". The library DDA data (OFFGEL-fractionated) are PXD019446 (same paper, handled by another agent; not touched here).

## Scope, evidence and decisions
- Deposited (PROXI, re-derived): 18 `.wiff` (+18 `.wiff.scan`) = `CD4 REP {1,2,3} {0HR,6HR,12HR,24HR,3D,7D}.wiff`; plus 2 `.swath`, 2 `_QUANT.xlsx`, `Human_Tcell_peakview_new.txt` (results, not runs). Annotated 18/18 runs, one row each (label free). File list in scratch/PXD019542/files.txt.
- Templates: ms-proteomics, human, dia-acquisition (whole file). Primary cells, so no cell-lines template.
- Samples (paper, stated): CD4+ T cells purified from buffy-coat PBMCs of three donors; 0 h = ex vivo, then anti-CD3/CD28 Dynabeads (1:1) for 6 h, 12 h, 24 h, 3 d, 7 d. Time point taken from file names (stated). REP n -> donor n is INFERRED (paper says three donors; REP 1-3 assumed to be the donors) -> biological replicate and `characteristics[individual]` = donor1-3.
- Prep for validation samples (stated): TCEP reduction, 2-chloroacetamide alkylation, trypsin 1:50, no fractionation for the SWATH runs (OFFGEL applies only to library, PXD019446; hence no SDS-PAGE/OFFGEL term here).
- MS (stated): TripleTOF 5600 (paper = PX), Eksigent nanoLC, SWATH 100 variable windows across 400-1250 m/z (scan window 400/1250), 25 ms accumulation. Dissociation: beam-type CID (TripleTOF CID), INFERRED from instrument class.
- Modifications: PeakView extraction against the library searched with Carbamidomethyl C fixed, Oxidation M variable (stated for library search). Chloroacetamide gives the same +57.021 carbamidomethyl. PX record lists MOD:00397/00425, consistent.

## Values not available / not applicable
- age, sex, ancestry: not available (paper: anonymous Red Cross buffy coats, not reported).
- precursor/fragment mass tolerance: not available for SWATH extraction (PeakView 75 ppm XIC width is an extraction window, not a search tolerance; library search 50 ppm/0.05 Da belongs to PXD019446).
- isolation window width: not available (variable windows; per-window widths not stated).

## Conflicts / caveats
- None between PX and paper on instrument.
- Ontology accessions in this file reuse values already used in validated campaign files (PRIDE:0000450, 0000578, 0000609, 0000600; MS:1000932, 1001251, 1002038, 1000422; UNIMOD 4/35). Live OLS check of the CL cell type label failed today (OLS returned an unrelated result), so `CD4-positive, alpha-beta T cell` (CL:0000624) is unverified live; validation ran with --use_ols_cache_only (ontology layer not installed).
- figshare metadata (10.6084/m9.figshare.12991619) could not be fetched (rate limit); it may hold the explicit REP->donor key.

## Validation
parse_sdrf (human, dia-acquisition, ms-proteomics): no errors. sdrf_review.py: [OK]. 18 rows x 39 cols.

## Review status
pending
