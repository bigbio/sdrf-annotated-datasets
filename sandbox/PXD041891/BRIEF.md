# PXD041891: glucocorticoid and CSK-inhibition SILAC proteomics in aggressive B-cell lymphoma lines

**BLOCKED:** two SILAC channel identities cannot be resolved from public evidence (details below). The file validates, but it stays in `sandbox/` until they are resolved.

Sources:
- [PRIDE PXD041891](https://www.ebi.ac.uk/pride/archive/projects/PXD041891)
- the submitter's [`File_assignment.txt`](https://ftp.pride.ebi.ac.uk/pride/data/archive/2024/05/PXD041891/File_assignment.txt)
- the deposited MaxQuant zips (`mqpar.xml`, `summary.txt`, `proteinGroups.txt`)
- the instrument model in the header of each of the 186 RAW files
- Choi et al., *Cancer Cell* 2024, [doi:10.1016/j.ccell.2024.04.007](https://doi.org/10.1016/j.ccell.2024.04.007), PMID 38701792, PMC11168741
- Cellosaurus records for the 7 cell lines

## What is annotated

The SDRF has 558 rows and 44 columns: 186 RAW files × 3 SILAC channels (light, medium and heavy). Templates are ms-proteomics, human and cell-lines (v1.1.0).

| Set | Type | Cell line | Files | L / M / H |
|---|---|---|---|---|
| 66, 69, 72, 81, 87, 90 | global proteome, SDS-PAGE, 23 slices | TMD8, FL-318, HBL-1, SU-DHL-5, BL-60, Ramos | 23 each | DMSO / prednisolone 24 h / **? (see blocker 1)** |
| 162 | pTyr IP | TMD8 CSK-T266G | R1-R2 | DMSO / 3-IB-PP1 15 min / 3-IB-PP1 2 h |
| 165 | global proteome, E1-E8 | TMD8 CSK-T266G | R1-R2 × 8 | DMSO / 3-IB-PP1 **? / ?** (see blocker 2) |
| 168 | diGly IP | TMD8 | R1-R2 | DMSO / CSKi 5 min / CSKi 15 min |
| 171 | global proteome, E1-E8 | TMD8 | R1-R2 × 8 | DMSO / CSKi **? / ?** (see blocker 2) |
| 698, 701, 707 | pTyr IP | HBL-1, TMD8, DoHH2 | R1-R3 | DMSO / CSKi 15 min / CSKi 2 h |
| 897 | diGly IP | TMD8 CSK-T266G | R1-R3 | DMSO / 3-IB-PP1 5 min / 3-IB-PP1 15 min |

SILAC states come from `mqpar.xml`, which is triplex in every search:
- Light: unlabelled
- Medium: Arg6 = Label:13C(6) R (UNIMOD:188) and Lys4 = Label:2H(4) K (UNIMOD:481)
- Heavy: Arg10 = Label:13C(6)15N(4) R (UNIMOD:267) and Lys8 = Label:13C(6)15N(2) K (UNIMOD:259)

Instruments, from the RAW headers:
- Q Exactive HF: all files except set 897
- Q Exactive HF-X: set 897

PRIDE's "Q Exactive" entry is contradicted by these headers.

## Blockers

1. **Heavy channel of the prednisolone sets 66-90 is undocumented (138 rows).**
   - `File_assignment.txt` lists only L = DMSO and M = prednisolone.
   - The paper and the PRIDE protocol describe only DMSO vs prednisolone, but say the lysates were mixed 1:1:1, and the MaxQuant search is triplex.
   - In `proteinGroups.txt`, the H channel has the same intensity scale as L and M. Its H/L ratios show induction of GR targets (FKBP5, LAPTM5), which suggests a second glucocorticoid condition, but its dose or time point is not stated anywhere public.
   - These rows are written with treatment and exposure duration `not available`.
2. **Time points of the global proteomes 165 and 171 conflict.**
   - `File_assignment.txt` gives 165 = 3-IB-PP1 15 min / 2 h and 171 = CSKi 5 min / 15 min.
   - The PRIDE protocol and the paper's Methods say global proteomes were taken after CSKi or 3-IB-PP1 treatment "for 6h and 24h".
   - The Src-family kinase loss in `proteinGroups.txt` (165, H/L log2 HCK −1.38) fits hours better than minutes.
   - Both channels are written as `not available`, so M and H cannot be told apart.

To unblock, find Table S2 or S4 of the paper, or ask the submitter for:
- the H-channel condition of sets 66-90
- the M and H time points of sets 165 and 171

Then edit those rows and promote the file to `datasets/`. The supplementary tables could not be retrieved here: PMC returned a bot challenge, and Europe PMC says the article is not open access for supplementary files.

## Other open points

- **Replicates:** R1/R2/R3 are encoded as biological replicates. The deposit does not say whether they are biological or technical.
- **Prednisolone dose:** the PRIDE protocol and the paper disagree (PRIDE: 10 µM, 25 µM for SU-DHL-5; paper: 10 nm, 30 nm for SU-DHL-5). No dose column was written.
- **FL-318 disease:** written as follicular lymphoma, following Cellosaurus. The paper groups FL-318 with the GCB-DLBCL lines.
- **Compounds without ontology terms:** 3-IB-PP1 and the CSK inhibitor (compound 13 of the paper's reference 63) have no NCIT or EFO term. These are validator warnings only.

## Validation and review

- **`parse_sdrf validate-sdrf` (sdrf-pipelines main):** run with ms-proteomics + human + cell-lines together, with each template alone, and with online OLS. Every run exits 0 with warnings only.
- **Other local checks:** `sdrf-tools structure` and `parse_sdrf convert-openms` pass.
- **Independent adversarial review: FAIL.** The two important findings are exactly blockers 1 and 2. All 186 RAW files are mapped, and all ontology terms resolve and are current.
- Checked 2026-11-21.
