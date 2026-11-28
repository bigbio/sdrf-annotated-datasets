# PXD050744 annotation blocked (no acquisition files deposited)

PXD050744 is the PD-1/CD80+ small extracellular vesicle study (Zhang LZ et al., Nat Commun 2024;15:3884; PMC11079016; PMID 38719909; doi:10.1038/s41467-024-48200-9). PRIDE marks the submission as `PARTIAL`.

**The two files PRIDE classes as RAW are Excel workbooks**, not acquisitions:

| file | PRIDE category | actual content |
|---|---|---|
| `WCL.RAW` | RAW | xlsx (PK zip magic): Spectronaut pivot `Report_Protein Quant (Pivot)`, 4,403 protein groups × 7 conditions |
| `sEVs.RAW` | RAW | xlsx, same layout: 1,153 protein groups × 7 conditions |
| `WCL.txt`, `sEVs.txt` | SEARCH | the same protein matrices as text |

This was confirmed independently by two downloads of the file bytes. Mapping these tables as runs in `comment[data file]` would fabricate data files, so no SDRF is emitted.

**To unblock:**
1. Real acquisitions: the timsTOF Pro `.d` folders, one per sample. That is CAL27 whole-cell lysate and CAL27 sEVs for each condition (Control, IFN-γ, aT-sEVs, cT-sEVs, Liposome, aT-sEV-IgG, aT-sEV-PD-1/CD80-Ab), plus any replicates.
2. The search settings behind the tables: enzyme, modifications, tolerances (e.g. a Spectronaut setup overview or log).
3. The acquisition mode (DDA vs diaPASEF), e.g. from `analysis.tdf`.
