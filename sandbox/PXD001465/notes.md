# PXD001465

Sandbox: The file fails `parse_sdrf validate-sdrf` for the ms-proteomics and vertebrates templates: `characteristics[sample type]` uses `study sample`, which is not in the PRIDE ontology list CI checks. Separately, the file-to-plex/fraction assignment is inferred from file names inside the single deposited zip.

## Return criteria
- Replace `study sample` with an accepted PRIDE sample-type term or drop the column, then re-validate.
- Re-review, then move to `datasets/PXD001465/`.
