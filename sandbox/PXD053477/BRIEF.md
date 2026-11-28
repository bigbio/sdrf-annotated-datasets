# PXD053477 SDRF annotation report

## Study
Stage-Specific Serum Proteomic Signatures Reveal Early Biomarkers and Molecular Pathways in Huntington's Disease Progression. Christodoulou, Demetriou, Zamba-Papanicolaou, Cells 2025, 14(15):1195, doi:10.3390/cells14151195. The paper's Data Availability statement cites PXD053477. PMCID not retrieved (Europe PMC rate-limited). Cyprus Institute of Neurology and Genetics, Nicosia.

## Scope, evidence and decisions
Status: **sandbox**. 72 rows x 37 cols, templates ms-proteomics + human + clinical-metadata.

- **Deposited vs annotated:** the PROXI record (saved file list: scratch `raw_files.txt`) lists 72 RAW files, numbered 1-72 with no gaps: 36 `-Control`, 18 `-Asym`, 10 `-Sym` and 8 `-SymAdv`. It also lists `Protein_Groups.prn`, `Peptides.prn` and `checksum.txt`. All 72 RAW files are annotated, one serum sample per file, label-free, with no fractionation.
- **Fractionation:** none. The paper describes depletion, then in-solution digestion, then a single 95 min LC-MS/MS run. It reports no SDS-PAGE, so `fraction identifier` is 1 and `fractionation method` is `not applicable`. The PRIDE:0000568 hint does not apply here.
- **Group mapping comes from the file names (stated):** Control maps to normal/control; Asym to HD asymptomatic; Sym to early symptomatic HD; SymAdv to symptomatic advanced HD. The disease stage is given in `characteristics[phenotype]` and in `factor value[phenotype]`. `characteristics[phenotype]` is licensed by clinical-metadata.
- **Sample prep (paper, stated):** spin-column depletion of albumin, IgG, transferrin, haptoglobin and myoglobin; reduction with DTT; alkylation with IAA; trypsin at 1:50.
- **MS (paper, stated):** Ultimate 3000 coupled to an Orbitrap Q Exactive HF; DDA top-20; MS1 m/z 300-1650; NCE 28%.
- **Search (paper, stated):** MaxQuant 1.6.2.6; 10 ppm precursor tolerance; 0.5 Da fragment tolerance; up to 2 missed cleavages; carbamidomethyl (C) fixed; oxidation (M) variable.

## Values left not available / not applicable
- `age`, `sex`: not available. They are per group only, in the paper's Table 1 and Supplementary Tables S1/S2, which were not read, and they cannot be linked to individual file numbers.
- `cell type`: not applicable (serum).
- `fractionation method`: not applicable.
- `individual`: given as P<n>, the file number (INFERRED to be a participant code).

## Conflicts and inferred points (why sandbox)
1. **Stage counts conflict.** The paper's Methods and Results give 8 early symptomatic and 10 advanced. The PX description and the deposited files give 10 `Sym` and 8 `SymAdv`. I followed the file names, which matches the PX description. The paper may have the two counts swapped, or `Sym` may not mean "early symptomatic". This is unresolved.
2. **Instrument conflict.** PX says Q Exactive; the paper says Q Exactive HF. I used the paper's value. The RAW headers were not read: the PRIDE FTP timed out and the shell has no network.
3. **Modifications.** The paper also lists oxidation as "fixed", which contradicts it being listed as variable. I annotated oxidation as variable only. No `mqpar.xml` is deposited to settle this.
4. **Ontology check.** OLS (EBI) was unreachable today. The terms used were not re-verified live, and the validator ran structure-only because the OLS dependencies are missing. All accessions are standard and match prior campaign files: MS:1002523, MS:1001251, MS:1000422, PRIDE:0000627/0000608/0000599, UNIMOD:4/35.
5. **Dissociation.** HCD is INFERRED from "NCE" on a Q Exactive HF.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` with the 3 templates: no errors. `sdrf_review.py`: [OK].

## Review status
pending
