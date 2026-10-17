# PXD009428

Sandbox: the file fails `parse_sdrf validate-sdrf` for the ms-proteomics and human templates.

## Why this is in sandbox
- `characteristics[sample type]` uses `study sample`, which is not in the PRIDE ontology list that CI checks.
- Separately, ultracentrifugation vs kit isolation cannot be assigned to file-name groups G and S, so the isolation method is not annotated.

## Return criteria
- Replace `study sample` with a PRIDE sample-type term, or drop the column if no honest term fits.
- Re-run `parse_sdrf validate-sdrf --use_ols_cache_only` for ms-proteomics and human, re-review, then move to `datasets/PXD009428/`.
