# PXD052180 annotation blocked (cell line unresolved; deposited raw file is reused)

PXD052180 deposits one genuine Thermo RAW file, `CON.raw`. The raw header gives a Q Exactive Plus, top-20 DDA, HCD at NCE 30, 300–1800 m/z, Orbitrap MS2 at 17,500. The file is an IgG negative-control co-IP run. The technical annotation is complete, but the sample identity cannot be resolved from public sources.

**Why it is blocked.** The cell-lines template requires a named cell line, and three candidates conflict:
- **A-172**: the PRIDE keyword.
- **HS683**: the CDKN3 paper (PMC11751337), which cites the sibling dataset PXD052182, not PXD052180. PRIDE links PXD052180 to an unrelated KIFC1 renal-carcinoma paper.
- **EC109 / Eca-109**: `CON.raw` is byte-identical to `PXD048886/109_HS_igG.raw` from the same submitter's METTL3/METTL14 study in EC109 esophageal cancer cells. All three files are 707,381,917 bytes, and four 1 MB ranges, including the first and last MB, have the same md5. The same holds for `PXD052182/CON.raw`.

These differ in sex, tissue and disease, so picking one would be a guess.

**Further evidence for curators:**
- `PXD052182/CDKN3.raw` is the same size as `PXD048886/109_HS_M3.raw` (the METTL3 IP), and an interior 1 MB range has the same md5; only the first MB differs. The "anti-CDKN3 vs IgG" pairing therefore appears to reuse METTL3/IgG data as well.
- The deposited `proteins.xlsx` has two intensity columns ("Intensity B" and "Intensity Q"), but only one raw file is deposited.
- No search settings were deposited. The enzyme is not stated anywhere (trypsin is only an inference).
- The raw gradient is 45–90% B over 52–55 min, then 90% B from 55 to 70 min.

**To unblock:** the submitter's confirmation of which cell line `CON.raw` was acquired from, and clarification of how PXD052180, PXD052182 and PXD048886 relate.
