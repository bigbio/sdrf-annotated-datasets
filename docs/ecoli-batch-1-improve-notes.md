# E. coli batch 1 — spec-backed SDRF improvements

Applied to all 85 SDRFs on `annotate/ecoli-batch-1` (PR #51).

## Templates
- `ms-proteomics` v1.1.0 on all files
- `dia-acquisition` v1.1.0 where acquisition is DIA

## Required fixes applied
- Split free-text PTM blobs into separate `comment[modification parameters]` columns with UNIMOD accessions
- `comment[cleavage agent details]`: capitalize Trypsin / Lys-C; map Trypsin/P
- `comment[instrument]`: preferred PSI-MS labels from accessions (e.g. `q exactive` → `Q Exactive`)
- PXD042090: LC system wrongly stored as instrument → **Orbitrap Fusion Lumos** from Methods text
- Normalize DDA/DIA acquisition labels; label-free → `label free sample`
- Organism part `NT=` without AC → `not available` / `cell` where mapped
- Expand HCD/CID dissociation to PSI-MS preferred forms
- Add `comment[sdrf template]`

## Validation
- `parse_sdrf validate-sdrf --use_ols_cache_only` with declared templates: **85/85 PASS** after fixes

## Remaining limitations (not invented)
- **7 TMT files** still have plex-level `comment[label]` (e.g. `NT=TMT6plex`) without channel→sample maps: PXD002705, PXD014039, PXD016403, PXD029140, PXD035326, PXD040618, PXD045656
- Partial leftover chemistry not fully encoded when free text mentioned dimethyl / SILAC / 13C15N beyond recovered Carbamidomethyl/Oxidation/Acetyl: PXD002409, PXD010402, PXD053317
