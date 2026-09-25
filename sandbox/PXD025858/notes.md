# PXD025858

Status: parked in `sandbox/` because current `parse_sdrf validate-sdrf` rejects the sample-type terms.

## Why this is in sandbox
- `characteristics[sample type]` values `cell lysate` and `phospho-enriched cell lysate` are not in the PRIDE ontology list used by CI.
- The cell-lines template also requires `characteristics[cellosaurus accession]`; Cellosaurus IDs were omitted because the deposit does not verify all three D492 model labels.

## Return criteria
- Replace sample-type values with PRIDE ontology terms while keeping the total-proteome vs phospho-enriched distinction.
- Re-run `parse_sdrf validate-sdrf --use_ols_cache_only` for ms-proteomics, human, and cell-lines.
- Move to `datasets/PXD025858/` only after validation is clean.
