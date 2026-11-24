# PXD073738 — sandbox draft (enzyme missing)

*Hevea brasiliensis* latex, clones BPM24 / GT1 / PB260 / RRIC100, 10- vs 20-year-old trees;
LC-MS/MS, PX instrument "LTQ Orbitrap"; publication pending (USM Penang / RIKEN).

`PXD073738.sdrf.tsv` maps all 24 RAW: `KK1812-<n>_<year>-<clone>-<rep>.raw`
(2 year groups × 4 clones × 3 replicates, run numbers 19–42 contiguous by group).

Inferences to confirm:
1. `2010` = 10-year-old trees, `2001` = 20-year-old trees (planting year; the description names exactly
   two ages and the files exactly two years, younger ↔ later).
2. `-1/-2/-3` = biological replicates (separate trees).
3. Clone names recorded in `characteristics[strain or breed]` (factor together with age).

**Why sandbox:** `comment[cleavage agent details]` is `not available` (no protocol text reachable;
no paper yet), which `ms-proteomics` forbids. Instrument is PX's generic "LTQ Orbitrap"
(MS:1000449) — read a RAW header to get the actual model. PX says "No PTMs" — search mods unknown.

## Update (PRIDE FTP listing, same day)

The deposit contains `KK1812.pg_matrix.tsv` and `KK1812.tsv` — **DIA-NN** outputs — plus an mzML per
RAW. That strongly suggests **DIA** acquisition, while the draft says DDA (PRIDE:0000627). Confirm
from an mzML header or the DIA-NN log before promoting, and switch to DIA (PRIDE:0000450) if so.
No parameter file with the enzyme was deposited.
