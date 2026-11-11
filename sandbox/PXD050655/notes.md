# PXD050655

Sandbox: The file fails `parse_sdrf validate-sdrf` for the human and ms-proteomics templates: `characteristics[sample type]` uses `study sample`, which is not in the PRIDE ontology list CI checks.

## Return criteria
- Replace `study sample` with an accepted PRIDE sample-type term or drop the column, then re-validate.
- Re-review, then move to `datasets/PXD050655/`.
