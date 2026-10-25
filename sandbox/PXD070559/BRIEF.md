# PXD070559: 20 PYGL IP runs; animal and A/B relationships unresolved

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD070559), all 20 RAW headers, the `MaxQuant_Elaboration.zip` directory and its deposited `mqpar.xml`, `summary.txt` and `parameters.txt`.

The author describes anti-PYGL immunoprecipitation from mouse liver and preparation with iST Kit P.O.00001. The 20 RAW basenames match the MaxQuant input list exactly, including the timestamp suffix on the KO-1A file. RAW copies inside the results ZIP are not additional acquisitions.

MaxQuant groups A and B runs into ten experiments: WT_1–5 and KO_1–5. It configures B as fraction 1 and A as fraction 2. These are processing settings; neither the physical origin of A/B nor their animal/preparation relationships is provided. The draft retains the author experiment and WT/KO codes, leaving physical fraction, biological/technical replicate, individual and pooling unavailable. It does not assign a specific knockout allele or infer ten animals.

All RAW files identify Q Exactive HF, Top15 DDA, HCD 27 NCE and a 300–1650 m/z survey. The deposited processing version is **MaxQuant 2.6.7.0**, despite the PRIDE description naming 1.6.2.10. Actual settings are a 4.5 ppm main precursor tolerance, 20 ppm first-search tolerance, 20 ppm FTMS fragment tolerance, two missed cleavages and `uniprotkb_Mouse_2025.fasta`. Search specificity is LysC plus Trypsin; fixed C carbamidomethylation and variable M oxidation/protein N-terminal acetylation are recorded.

The preparation text only names the commercial kit. Search enzymes and fixed modifications do not establish the physical protease or reduction/alkylation reagents used, so those fields remain unavailable. The registered article DOI [10.1126/sciadv.aej6157](https://doi.org/10.1126/sciadv.aej6157) did not return a Crossref record at this audit; no methods from another PYGL study were substituted.

## Local validation

Keep the 20-row draft in `sandbox/`. The ms-proteomics check and repository review fail on unavailable biological replicate, technical replicate, physical cleavage agent and physical fraction identifier. The vertebrates check fails on the two replicate fields. Record reconciliation also flags the unavailable cleavage-agent value. That flag records an unresolved method gap; a kit name or the search configuration cannot resolve it. Remaining ontology-cache warnings are retained in the logs.
