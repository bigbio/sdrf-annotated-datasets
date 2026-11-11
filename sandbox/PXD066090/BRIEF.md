# PXD066090: one Flag-Lck/SUMO1-T95R immunoprecipitate

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD066090), `NON-1.raw`, bounded metadata reads from `NON-1.msf` and [HEK293T CVCL_0063](https://www.cellosaurus.org/CVCL_0063).

The author describes HEK293T expressing Flag-Lck and c-Myc-SUMO1 T95R, followed by anti-Flag immunoprecipitation and in-gel tryptic digestion. The filename `NON-1` does not establish an untreated control. Biological preparations and pooling remain unavailable; technical identifier 1 denotes the single deposited acquisition.

The RAW identifies Orbitrap Elite, a 350–1800 m/z FTMS survey and CID 35 NCE ion-trap fragments for the top **16** precursors. The method filename contains Top15, but the embedded scan-event definition specifies 16. The MSF input filename matches `NON-1.raw`.

The MSF `SchemaInfo` records Proteome Discoverer **1.3.0.339**. SEQUEST uses 10 ppm precursor/0.8 Da fragment tolerance, two missed cleavages, `SP_Human_201711.fasta`, fixed C carbamidomethylation and variable M oxidation/K GlyGly. The hidden X-to-leucine mass mapping is a search representation setting, not an additional chemical modification. Physical reduction and alkylation reagents are not established by the fixed search modification.

Keep the one-row draft in `sandbox/` until its preparation and replicate history can be established. A GlyGly search setting does not by itself establish a separate modified sample or a validated site result.

## Local validation

The ms-proteomics, human and cell-lines templates, and repository review, fail only on unavailable biological replicate. Deposit-record reconciliation passes. The retained ontology-cache warnings do not supply the missing experimental design.
