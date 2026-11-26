# PXD001256

BLOCKED: `comment[label]` uses free-text diethyl 13C/2H light/heavy values that `parse_sdrf` rejects.

`datasets/PXD001256/PXD001256.sdrf.tsv` already exists. This pull request does not replace it.

## Why this is in sandbox
- No diethyl-labeling term exists in the PRIDE/MS vocabularies.
- `PRIDE:0000513` Dimethyl Labeling would validate but names the wrong chemistry.
- The diethyl mass shifts (+56.063 / +60.076 Da) are not in the modification column.

## Return criteria
- A controlled label term for diethyl labeling, or a template that allows this chemistry honestly.
- Re-review before any change to the file in `datasets/`.
