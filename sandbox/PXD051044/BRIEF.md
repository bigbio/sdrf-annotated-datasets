# PXD051044 SDRF annotation report

## Study
Enhancing CAR T-cell efficacy against neuroblastoma through MIF inhibition (PRIDE). Paper: Strijker JGM et al., "Blocking MIF secretion enhances CAR T-cell efficacy against neuroblastoma", Eur J Cancer 2025;218:115263, doi:10.1016/j.ejca.2025.115263, PMID 39908652, PMC11884407. The paper's Data availability statement cites PXD051044 (with PXD051208, which holds the whole-tumoroid lysate data and is not annotated here).

## Scope, evidence and decisions
- Deposited: 14 files from PROXI (12 .raw, proteinGroups.txt, checksum.txt), which matches the campaign cache. Annotated: 12/12 RAW. The PRIDE FTP listing timed out, so the file names come from PROXI only.
- Files: `PXD051044-tumoroid.sdrf.tsv` has 9 rows (templates ms-proteomics, human, oncology-metadata). `PXD051044-blank.sdrf.tsv` has 3 rows (ms-proteomics only). I split the file because the blank-medium runs have no donor: the human template requires age and sex, and age does not allow `not applicable`.
- Run to sample (STATED): the file tokens 039, 691B and 772 match the three tumoroids in Suppl. Fig. 3b ("three chosen tumoroids for secretome analysis"): NB039, AMC691B and AMC772. DMEM is the empty DMEM GlutaMAX. The supplementary methods state that proteins found in that medium were excluded, which shows it was measured as a blank. Suffixes _1/_2/_3 = technical replicates. The supplementary methods say "analyzed in triplicates", and each model was conditioned from one expansion of two T175 flasks, so biological replicate = 1. The mapping of a suffix to an injection rather than a separate conditioning is INFERRED from that wording.
- Label-free. There is no channel map to state.
- Sample characteristics (Suppl. Fig. 3b, STATED): NB039 relapse, MYCN amplified, ATRX WT, 1p/11q loss, 17q gain. AMC691B diagnosis, MYCN amplified, ATRX WT, 1p loss, 17q gain. AMC772 diagnosis, MYCN non-amplified, ATRX homozygous deletion, 11q loss, 17q gain. I put these in genotype and clinical history (licensed via oncology-metadata, which extends clinical-metadata).
- Treatment: 45 mL empty DMEM GlutaMAX conditioned for 24 h, then 3 kDa MWCO concentration. Tumoroid growth medium (DMEM low glucose GlutaMAX + 20% F-12, B27, N2, IGF, FGF, EGF, PDGFaa/bb) is stated, but `characteristics[culture medium]` is licensed only by cell-lines. That template cannot be declared because the tumoroids are not in Cellosaurus (API search for AMC691B, AMC772 and NB039 returned 0 hits). The medium is recorded here instead.
- MS (supplementary methods, STATED): Orbitrap Exploris 480 (matches PX), UltiMate 3000, DDA, MS1 375-1600 m/z, HCD 28% NCE. Prep: urea, 10 mM DTT, 20 mM IAA, Lys-C then trypsin. Search: MaxQuant 1.6.10.0, Trypsin/P, fixed carbamidomethyl C, variable M oxidation and protein N-term acetyl, precursor 20 ppm first search / 4.5 ppm main, fragment 20 ppm, LFQ + MBR. The PX record says "No PTMs", which is overridden by the Methods.
- RAW headers and mqpar.xml were not read (no shell network, PRIDE FTP timed out). The modifications therefore come from the Methods prose, not from the deposited search parameters.

## Values left not available / not applicable
- Tumoroid rows: organism part, age and sex are `not available` (not in the paper). Material type `cell`: "organoid" is not an allowed value, and the conditioned medium is from cells.
- Blank rows: organism, organism part, disease and material type are `not applicable` (no biological material).

## Ontology verification
EBI (OLS, Europe PMC, FTP) returned upstream connect errors throughout the session. Accessions reuse values in already-reviewed campaign files (MS:1003028, MS:1001309, MS:1001251, MS:1002038, MS:1000422, PRIDE:0000627/0000608/0000599, UNIMOD:4/35/1). Disease is the bare label "neuroblastoma". These were not re-verified live; re-check them when OLS is back.

## Status: sandbox
Every run is mapped from stated evidence. The open points are: suffix = technical replicate is inferred; raw headers, mqpar and the FTP listing are unread; accessions are not re-verified live.

## Review status
pending
