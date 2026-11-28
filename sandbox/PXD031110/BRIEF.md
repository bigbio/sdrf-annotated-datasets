# PXD031110 SDRF annotation report

## Study
PLK1 inhibition selectively induces apoptosis in ARID1A deficient cells through uncoupling of oxygen consumption from ATP production. Srinivas US et al., Oncogene 2022, DOI 10.1038/s41388-022-02219-8, PMID 35236967 (PMCID: not found, Europe PMC unreachable). The paper's Data Availability section cites PXD031110 (checked on the Nature PDF). Submitter: Dennis Kappei, Cancer Science Institute of Singapore.

## Scope, evidence and decisions
Status: **sandbox**. 12 rows (12 RAW, label-free), 36 columns. Templates: ms-proteomics, human, cell-lines, clinical-metadata (needed for characteristics[genotype]).

- Deposited vs annotated: the PROXI record (read in the cloud browser on 2026-11-27) lists 13 files: 12 `.raw` files plus 1 search-output zip (`20210220_QPC_DK_CSI_ADJ_Sai_GES1_ARID1A_WTvsKO_mito.zip`, not a run). All 12 RAW files are annotated. This matches the campaign cache (12 RAW / 13 files). The PRIDE FTP folder listing timed out (upstream connect error), so `checksum.txt` could not be cross-checked.
- Design: GES-1 ARID1A WT vs ARID1A KO × DMSO vs volasertib × replicates 01-03, mitochondrial fraction. Taken from the file names (STATED in the names, but their meaning is INFERRED). Replicate numbers 01-03 are taken as biological replicates (INFERRED).
- Labelling: label-free (INFERRED). The file names carry no channel tags, PX lists no label modification (only MOD:00397, iodoacetamide-derivatized residue), and there is one RAW per sample. Because no multiplexing is evident, no channel map is needed.
- Cell line: GES-1, CVCL_EQ22 (verified live in Cellosaurus: human, fetal donor AG 9FM, sex unspecified, no problematic-line note). The KO was made by CRISPR-Cas9 (stated in the bioRxiv preprint Methods). Culture medium is RPMI1640 + 20% FBS + 1% Pen/Strep (stated in the bioRxiv preprint Methods). Organism part: stomach. Cell type: epithelial cell. Disease: normal (immortalized non-malignant gastric epithelium).
- Instrument: Q Exactive HF (MS:1002523), from the PX record only. RAW headers were not read, and the Methods were not readable to confirm it.
- Modifications: Carbamidomethyl C fixed, plus alkylation with IAA. Based on PX MOD:00397 only. The search zip was not opened.

## Values not available / not applicable
- age, sex: `not available`. Cellosaurus gives sex as unspecified. Its age of fetal 9 months is reflected as developmental stage `fetal`.
- Volasertib dose and duration: not stated in any source I could read, so the treatment value is just `volasertib`.
- Reduction reagent, enzyme detail, tolerances, NCE, scan range, LC settings: omitted. The proteomics Methods are in the Supplementary Methods DOCX (Springer static-content MOESM1), which robots.txt blocked for WebFetch. The browser download of it was not readable here.

## INFERRED (reason for sandbox)
- Trypsin as the enzyme (the column forbids `not available`), DDA acquisition, label-free, and replicate meaning: none of these is stated in a source I read.
- Instrument taken from the PX record alone (the campaign has seen PRIDE instrument errors before).
- WT/KO and DMSO/volasertib decoded from the file names only.

Unblock: read the Supplementary Methods DOCX and `proteinGroups`/`parameters.txt` (or equivalent) in the deposited search zip, plus one RAW header.

## Conflicts
None found. The PX record and the paper agree on the title, PMID and accession.

## Review status
pending
