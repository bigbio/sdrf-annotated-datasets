# PXD078629

Sandbox: The file fails `parse_sdrf validate-sdrf` for every declared template: `characteristics[sample type]` uses `study sample`, which is not in the PRIDE ontology list CI checks. Separately, the specific stimuli per perifusion chamber are not in the deposit, so treatment is recorded generically as `perifusion`.

## Return criteria
- Replace `study sample` with an accepted PRIDE sample-type term or drop the column, then re-validate.
- Re-review, then move to `datasets/PXD078629/`.
