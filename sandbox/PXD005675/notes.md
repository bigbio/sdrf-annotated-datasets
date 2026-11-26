# PXD005675

Sandbox: the file fails `parse_sdrf validate-sdrf` for the ms-proteomics template.

## Why this is in sandbox
- Human stem-cell-derived neuron arm only (iTRAQ 8-plex; control, TNF-alpha, H2O2, CREB siRNAs). `characteristics[sample type]` uses `study sample` in all 408 rows, which `parse_sdrf validate-sdrf --use_ols_cache_only` rejects for the ms-proteomics template. The iTRAQ channel order is inferred from the positional order in supplementary tables S6-S11. The mouse HT22 arm (TMT10plex) is not included: its TMT channel order is unverified and failed independent review.

## Return criteria
- Replace `study sample` with an accepted PRIDE sample-type term or drop the column, then re-validate. The HT22 arm needs the authors' channel sheet before it can be contributed.
