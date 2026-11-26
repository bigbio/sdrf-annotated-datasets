# PXD043461 annotation blocked

PXD043461 is the oleamide / tumour-associated macrophage study (PeerJ 2024, PMC11416084), on a Q Exactive HF-X with DDA:
- **Samples:** primary human monocyte-derived macrophages from three blood donors (AB, O1, O2), each in three groups (macrophage control, TAMs, TAMs + oleamide).
- **Files:** 18 RAW files, `T1_01-03`, `T2_*`, `T3_*`, `T7_*`, `T8_*`, `T9_*`.

The code → donor/group key is missing:
- **Donor sheets:** the deposited `Donor-AB.xlsx` and `Donor-O2.xlsx` give PD abundances only by F-number (F40–F45 and F31–F36; "TAMs" ×3 and "TAMs and OLA" ×3).
- **Gaps:** they carry no RAW file names, no control group and no donor O1 sheet.
- **Code pattern:** the six T-codes × 3 injections do not match the 3 donors × 3 groups described.

No SDRF is emitted.

**To unblock:** a file → donor/group sheet, or the PD study file.
