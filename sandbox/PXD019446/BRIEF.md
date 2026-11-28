# PXD019446 SDRF annotation report

## Study
A primary human T-cell spectral library to facilitate large scale quantitative T-cell proteomics. Weerakoon et al., Sci Data 2020;7:412, DOI 10.1038/s41597-020-00744-3, PMID 33230158 (the paper cites PXD019446 and PXD019542 by name). Submitter affiliation: Rajarata University of Sri Lanka, with QIMR Berghofer, Brisbane.

## Scope, evidence and decisions
- Deposited files (PROXI resultType=full plus the PRIDE FTP index, both re-derived in this run): 96 `.wiff` (+96 `.wiff.scan`), 96 mzML, 96 pepXML, iProphet pep/prot.xml x4, the consensus `.splib`, `Human_Tcell_peakview.tsv`, README.txt and `Dataset_annotation_spectral_library.txt`. Annotated: 96/96 `.wiff` runs, one row each. Label-free, so there is one channel per run.
- The run-to-sample key is STATED. The deposited `Dataset_annotation_spectral_library.txt` maps SPLib1_HuTcell to Activated_human_T-cells and SPLib2/3/4_HuTcell to Exvivo samples 1/2/3. The paper says SpLib_1 is one in-vitro-activated CD3+ T-cell sample and SpLib_2-4 are ex vivo, each from a different buffy coat ("four genetically unrelated individuals"). This gives individuals donor1-4.
- Fractions: off-gel IEF (Agilent 3100, 24 cm pH 3-10 IPG strip). The paper says 96 samples were analysed; the files run _1.._24 per library, so 4 x 24 fractions. Fraction identifier = the file suffix. Fractionation is annotated as Off-gel electrophoresis PRIDE:0000552, NOT SDS-PAGE. The coordinator note about PRIDE:0000568 does not apply: the paper uses SDS only in the lysis buffer.
- MS: TripleTOF 5600 (paper and PX agree), DDA top10 (SpLib_4: top12), MS1 300-2000 m/z. TPP search: 50 ppm / 0.05 Da, trypsin with 2 missed cleavages, Carbamidomethyl C fixed, Oxidation M variable. Reduction with DTT, alkylation with IAA (stated).
- Treatment / factor: "in vitro activated with anti-CD3/CD28 Dynabeads 7 days" vs "ex vivo (unstimulated)".
- PXD019542 (the SWATH validation set from the same paper) was not touched.

## Values left not available / INFERRED
- age, sex, ancestry: not available. These are anonymous Red Cross buffy coats and the paper states none of them.
- dissociation method CID (MS:1000133): INFERRED from the TripleTOF 5600 (beam-type CID); the paper does not state it. Collision energy is omitted (rolling CE assumed, not stated).
- organism part blood: the cells are PBMC-derived, so this is stated in substance. Disease "normal": blood-bank donors, inferred.
- PRIDE:0000552 could not be checked live because OLS4 was unreachable (WebFetch permission timeout, browser upstream error). The accession is taken from 457 prior curated rows in sdrf-annotated-datasets. The local OLS cache was also unusable because fastparquet is missing, so parse_sdrf ran structural checks only.

## Validation
`parse_sdrf validate-sdrf --template ms-proteomics --template human`: no errors (ontology checks skipped). `sdrf_review.py`: [OK].

## Review status
pending
