# PXD027901 — TMT6plex phosphoproteomics of mouse cortical astrocytes (2-OHE vs DMSO)

Source: [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD027901); Glia 2021, doi:10.1002/glia.24072 (full text not accessible; PRIDE protocol text used).

## Why this is in sandbox/
`comment[fraction identifier]` (1-14) is a **file-order placeholder**, not an established run-to-fraction map. The protocol states 12 concatenated high-pH fractions, but 14 RAW files (QEHFX_00334-00347) are deposited and nothing in the deposit (PRIDE, mzid, mgf) links runs to fractions. RAW header timestamps confirm the file numbers follow acquisition order only. The deposited .msf input-file table and RAW header sample-name fields were not read and might settle it.

Two independent review rounds both failed on this single finding; everything else was verified (channel map TMT126-128 control / 129-131 2-OHE per the protocol, instrument Q Exactive HF-X per protocol vs HF in PRIDE's structured field, modifications, tolerances, 84 rows = 6 channels x 14 files).

## Other notes
Treatment is free text (`2-OHE 50 uM, 6 min`, abbreviation not expanded); organism part `cerebral cortex` inferred from "cortical astrocytes"; developmental stage not available.

Move to `datasets/` once the run-to-fraction map is established.
