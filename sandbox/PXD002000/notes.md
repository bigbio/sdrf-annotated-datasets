# PXD002000

BLOCKED: deposited “RAW” files are `.zip` / `.mgf.gz`, not vendor `.raw` / MALDI `.baf`.

## Why this is in sandbox
- 24 nLC-MSE files are `VG_CTRL*_*.raw.zip` / `VG_Coli*_*.raw.zip` (Waters Q-Tof Premier).
- Remaining RAW entries are numeric MALDI `*.zip` plus `sample*.zip` peak exports; PRIDE also lists `.pride.mgf.gz`.
- `comment[data file]` must be vendor RAW. CTRL vs 10 µg/ml enrofloxacin mapping is recoverable from the Waters zip names (3 biological replicates × 4 injections).

## Return criteria
- Unpacked Waters `.raw` folders and Bruker MALDI vendor files deposited under those names.
