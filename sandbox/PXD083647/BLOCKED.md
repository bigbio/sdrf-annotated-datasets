# PXD083647 annotation blocked (deposited files contain only zero bytes)

**Why it is blocked.** Both deposited files are entirely zero-filled, so no acquisition metadata can be read:
- `Q3_CWIPAS1488_AU.raw` (755,602,767 bytes) is the only RAW file. It was read end to end in 16 range requests, and it has no Thermo "Finnigan" header and no non-zero byte at all.
- `Q3_CWIPAS1488_AU.msf` (455,524,352 bytes) was read in one full stream. It has no SQLite header and no non-zero byte.
- HTTPS and plain HTTP returned identical bytes.
- PRIDE lists no checksums, no publication is linked, and Europe PMC has no record citing the accession.

As a result, the instrument (PRIDE says LTQ Orbitrap Elite) cannot be confirmed from the raw file, and the search settings cannot be read from the .msf.

**Expected SDRF once real files are available:** one label-free DDA row for the in-vitro PGK1 / KAT2A / Aurora B reaction, with no cell-lines template and no factor value.

**To unblock:** a re-upload of valid copies of both files by the submitter or PRIDE.
