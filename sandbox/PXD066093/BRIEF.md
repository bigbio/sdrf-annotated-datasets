# PXD066093: one Lck immunoprecipitate with separate CID and ETD scans

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD066093), the deposited `S3.raw` header, the original `s3.msf` Proteome Discoverer project metadata and [HEK293T CVCL_0063](https://www.cellosaurus.org/CVCL_0063).

The archive reports Flag-Lck immunoprecipitation from HEK293T, followed by SDS-PAGE and in-gel tryptic digestion. The RAW header identifies Orbitrap Elite. Both the RAW and the MSF internally identify the acquisition as **sumo-3.raw**, establishing the deposited filename alias rather than assuming that unrelated names refer to the same sample.

The method acquires a 350–1800 m/z FTMS survey, followed by separate CID and ETD ion-trap spectra for each of the top eight precursors. The 35 NCE field refers to CID. This is not a combined EThcD activation event. The MSF has three SEQUEST branches: CID uses 0.7 Da fragment tolerance, while both ETD charge-selection branches use 1.2 Da. Those values are recorded separately; a single common fragment tolerance remains unavailable. All branches use 10 ppm precursor tolerance, two missed cleavages, `SP_Human_201711.fasta`, fixed C carbamidomethylation and variable M oxidation/K GlyGly.

An additional read of the original MSF `SchemaInfo` table establishes Proteome Discoverer **1.3.0.339**. This application version is now recorded; workflow node versions were not used as a substitute. Physical reduction/alkylation reagents, the number of underlying preparations and pooling relationships are also not established. Technical identifier 1 denotes the one deposited acquisition; biological replicate remains unavailable. No acute treatment or separate SUMO-modified sample is inferred from the internal filename or the GlyGly search setting. Keep this one-row draft in `sandbox/` pending preparation evidence.

## Local validation

The ms-proteomics, human and cell-lines templates, and consequently repository review, fail only because biological replicate is unavailable. Both separately declared fragmentation methods are retained. Deposit-record reconciliation passes; this does not establish the missing preparation or pool history. Offline ontology warnings remain in the stored logs.
