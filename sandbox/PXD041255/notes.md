# PXD041255

Sandbox: no file-to-sample map. Disease group and biopsy site cannot be assigned per run.

## Why this is in sandbox
- The study has 15 participants (5 INR, 5 IR, 5 HC) with two biopsy sites each = 30 files.
- Neither PRIDE, MaxQuant (`01`..`30`), RAW headers nor the paper text identifies which file is which participant, group or site.
- Organism part, disease and age are `not available`. No factor value column was declared.

## Return criteria
- A run-to-participant, disease-group and tissue-site map.
- Re-review, then move to `datasets/PXD041255/`.
