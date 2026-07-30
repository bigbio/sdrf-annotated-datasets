# PXD010402

Status: parked in `sandbox/` during `annotate/ecoli-batch-1`.

## Why this is in sandbox
- Free-text chemistry still mentions SILAC / 13C15N labeling that cannot be safely normalized without stronger evidence.

## Return criteria
- Recover the missing evidence needed for a spec-complete SDRF.
- Re-run `parse_sdrf validate-sdrf --use_ols_cache_only` with the declared templates.
- Move back to `datasets/PXD010402/` only after the unresolved issue is fixed.
