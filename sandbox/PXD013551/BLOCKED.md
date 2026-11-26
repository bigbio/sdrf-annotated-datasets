# PXD013551 annotation blocked

PXD013551 is the *Gnathostoma spinigerum* L3 excretory-secretory proteome (Parasite 2019, PMC6550564): 12% SDS-PAGE cut into 18 slices, on a Bruker micrOTOF.

**No vendor raw data is deposited.** The 19 files PRIDE classes as RAW are `.baf_idx` index files, which hold no spectra; the rest are Mascot `.dat` results and small `.mgf` peak lists.

**The run set is irregular:**
- There are two acquisition series with different run numbers (`GS*_1_*_18xx` and `GS*_B*_22xx/23xx`).
- Slices are duplicated (GS2, GS4 ×3, GS5, GS8, GS9) and missing (GS12, 13, 15, 17, 18).
- So the slice → fraction order cannot be reconstructed from the names.

No SDRF is emitted.

**To unblock:** the original Bruker `.d`/`.baf` data, plus a slice/run sheet.
