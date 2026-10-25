# PXD041154

Sandbox: The file fails `parse_sdrf validate-sdrf` for every declared template: `characteristics[sample type]` uses `study sample`, which is not in the PRIDE ontology list CI checks. Separately, the run-to-buffer mapping (odd runs K+, even runs Li+) is inferred from nucleolin abundance in proteinGroups, not stated in the deposit.

## Return criteria
- Replace `study sample` with an accepted PRIDE sample-type term or drop the column, then re-validate.
- Re-review, then move to `datasets/PXD041154/`.
