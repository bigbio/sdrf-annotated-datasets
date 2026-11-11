# PXD001354

BLOCKED: deposited files are MALDI `.t2d.mzxml` peak lists, not vendor RAW, and the MS is identification of DIGE spots from a preparative gel so treatment (control / acetaminophen / atenolol / carbamazepine) cannot be mapped to files.

## Why this is in sandbox
- `comment[data file]` must be vendor RAW (`.raw` / `.d` / `.wiff`). PRIDE lists 290 "RAW" entries that are converted mzXML.
- Spot-level rows collapse to one source name unless uniqueness is assigned per spot; even then the experimental factor is not recoverable from the deposit.
- Independent review FAIL: uniqueness collision, peak-list data files.

## Return criteria
- Vendor 4800 `.t2d` or equivalent RAW deposited, or an explicit exception for MALDI peak lists.
- A cited map from gel spots or DIGE images to the four exposure groups.
