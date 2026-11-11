# PXD078925: Jurkat Lck immunoprecipitate acquired on Fusion Lumos

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD078925), the extended `LCK-Y.raw` method header, bounded `LCK-Y.msf` metadata, the `LCK-MS.xlsx` export and [Jurkat CVCL_0065](https://www.cellosaurus.org/CVCL_0065).

The author describes anti-Lck immunoprecipitation from Jurkat followed by SDS-PAGE and in-gel tryptic digestion. The generic Jurkat line is retained; no E6.1 subclone is inferred. Cellosaurus supplies male, age 14 years, blood origin and T-cell acute lymphoblastic leukemia. Biological preparation count and pooling remain unresolved; technical identifier 1 denotes the one deposited run.

Both the RAW and the MSF input table identify **Orbitrap Fusion Lumos**, contradicting the PRIDE Orbitrap Elite entry. The RAW method specifies a 350–1500 m/z survey, **12** dependent scans and HCD 30 NCE with Orbitrap fragment detection. The external method filename contains Top10; the scan-event definition is the source for the annotated count.

The original processing workflow and schema identify Proteome Discoverer **2.4.1.15**. The actual Sequest HT node uses 10 ppm precursor/0.02 Da fragment tolerance and two missed cleavages. Its modifications are fixed C carbamidomethylation, variable M oxidation, protein N-terminal acetylation, N-terminal Met-loss and Met-loss+Acetyl. Its database contains author CEP83 and Lck FASTA entries plus `uniprotkb_proteome_UP000005640_2024_06_24 82518.fasta`.

The preceding precursor-recalibration node uses 20 ppm/0.5 Da. Those settings are kept separate from the final search tolerances. Node/plugin versions are not substituted for the application release. Reduction/alkylation reagents and biological replicates remain unavailable, so keep this draft in `sandbox/`.

## Local validation

The ms-proteomics, human and cell-lines templates, and repository review, fail only on unavailable biological replicate. Deposit-record reconciliation passes, but does not detect the confirmed instrument discrepancy. Direct RAW/MSF evidence supports that correction. Ontology-cache warnings remain in the logs.
