# PXD000642

BLOCKED: independent review failed. Do not promote to `datasets/` until the channel usage is mapped.

## Why this is in sandbox
- The deposited ProteinPilot searches flag only two of the four iTRAQ channels as used per search set.
- The runs were not mapped to those flags, so some of the 176 rows may be empty channels.
- This is recorded in the annotation manifest.

## Return criteria
- Map each run to the search set and drop unused channels.
- Re-review, then move to `datasets/PXD000642/`.
