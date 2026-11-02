# PXD002214

Sandbox: the file fails `parse_sdrf validate-sdrf` for the ms-proteomics template.

## Why this is in sandbox
- `characteristics[sample type]` uses `study sample` in 1284 rows, which `parse_sdrf validate-sdrf` rejects for the ms-proteomics template (not in the PRIDE list it checks). Separately, the iTRAQ 8-plex channel map is assumed to be the same for all 10 mixes; the paper (Preil et al., Circ Cardiovasc Genet 2015) is not open access and was not read.

## Return criteria
- Replace `study sample` with an accepted PRIDE sample-type term or drop the column, confirm the per-mix iTRAQ channel map against the paper's Methods, then re-validate.
