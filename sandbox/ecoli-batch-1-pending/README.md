# E. coli batch 1 pending datasets

These SDRFs were moved out of `datasets/` while improving `annotate/ecoli-batch-1`.
They still need curator follow-up before they should return to `datasets/`.

## Reasons

- `PXD002705`: TMT label remains plex-level without channel-to-sample mapping.
- `PXD014039`: TMT label remains plex-level without channel-to-sample mapping.
- `PXD016403`: TMT label remains plex-level without channel-to-sample mapping.
- `PXD029140`: TMT label remains plex-level without channel-to-sample mapping.
- `PXD035326`: TMT label remains plex-level without channel-to-sample mapping.
- `PXD040618`: TMT label remains plex-level without channel-to-sample mapping.
- `PXD045656`: TMT label remains plex-level without channel-to-sample mapping.
- `PXD002409`: Free-text chemistry still mentions dimethyl-like terms not safely recoverable into spec-complete PTM columns.
- `PXD010402`: Free-text chemistry still mentions SILAC / 13C15N labels not safely recoverable into spec-complete PTM columns.
- `PXD053317`: Free-text chemistry still mentions dimethyl-like terms not safely recoverable into spec-complete PTM columns.

## Return criteria

- TMT files: add defensible channel-to-sample mapping and replace plex-level `comment[label]` values with channel-level labels.
- Chemistry/PTM files: recover exact labeling / modification semantics from public evidence and encode them with valid SDRF `comment[modification parameters]` columns.
- Re-run `parse_sdrf validate-sdrf --use_ols_cache_only` with declared templates before promotion back into `datasets/`.
