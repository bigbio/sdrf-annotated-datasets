# PXD030765

BLOCKED: not a SILAC dataset. It is label-free AP-MS with spectral counting. No SDRF is committed yet, because the cell line and the infection details of the AP-MS samples conflict between sources or are missing from them.

- Dataset: https://www.ebi.ac.uk/pride/archive/projects/PXD030765
- Publication: Brugier et al., "RACK1 Associates with RNA-Binding Proteins Vigilin and SERBP1 to Facilitate Dengue Virus Replication", J Virol 2022;96(7):e01962-21. PMID 35266803, PMC9006918, doi:10.1128/jvi.01962-21. Preprint: doi:10.1101/2021.10.28.466260.

## Why this is in sandbox

1. **The labelling is not SILAC.** PRIDE lists `quantificationMethods = SILAC (PRIDE:0000315)`, but that is a submitter dropdown and the record contradicts it:
   - The PRIDE data-processing protocol and the paper analyse the data with SAINTexpress and MIST, which score spectral counts.
   - The deposited Taplin result workbooks (`*_HA-RACK1_IP{1,2,3}_.xlsx`) report only `Unique` / `Total` peptide counts and `Sum Intensity`. They have no heavy/light channels or H/L ratios.
   - PRIDE `identifiedPTMStrings` is "No PTMs are included in the dataset".
   - The paper's Methods describe no isotope labelling.

   The correct label is therefore `label free sample`. This is an inference from the evidence above, because the paper never says "label-free" explicitly.
2. **The cell line conflicts between sources.** The PRIDE protocol, the Results and the Fig. 2A legend say 293T. A Methods-section summary of the paper says "HAP1 cells (5 × 10^8)". The paper is internally inconsistent, so the submitter must confirm the cell line.
3. **The infection details are missing.** The workbooks label two of the three conditions per IP as `+DENV2`, and the viral-proteins sheet names DENV2-16681. The paper's AP-MS Methods give no virus strain, MOI or time post infection.

## Resolved file → condition map (from the deposited workbooks)

Each IP is 3 conditions × 3 SDS-PAGE gel regions (fractions). The conditions are:

- **untagged RACK1 + DENV2** (control, SAINT bait `x001` "CONTROL")
- **HA-RACK1, no virus** (SAINT bait `x002`)
- **HA-RACK1 + DENV2** (SAINT bait `x003`)

| IP (biological replicate) | RACK1 + DENV2 (control) | HA-RACK1 | HA-RACK1 + DENV2 | Evidence |
|---|---|---|---|---|
| IP1 | 62910 (A), 62911 (B), 62912 (C) | 62913 (D), 62914 (E), 62915 (F) | 62916 (G), 62917 (H), 62918 (I) | IP1 workbook, sheet `Liste siRNA` (explicit) |
| IP2 | 67543 (1), 67544 (2), 67545 (3) | 67546 (4), 67547 (5), 67548 (6) | 67549 (7), 67550 (8), 67551 (9) | IP2 workbook, sheet `Feuil1` (explicit) |
| IP3 | 68573–68575 (ABC) | 68576–68578 (DEF) | 68579–68581 (GHI) | **Inferred**: same ABC/DEF/GHI layout as IP1, but no per-file list in the IP3 workbook |

The group-to-condition assignment was cross-checked against the SAINT input sheets (`No Virus`, `+DENV`). Per-group total peptide counts match bait 1001/2001/3001 → ABC/123, 1002/2002/3002 → DEF/456 and 1003/2003/3003 → GHI/789, for 98–99% of genes in IP2 and IP3.

## Technical values known

- Instrument: LTQ Orbitrap Velos Pro (PRIDE dropdown says LTQ Orbitrap Velos).
- Digestion: in-gel trypsin.
- Acquisition: DDA.
- Search: Sequest, <2% peptide FDR.

Modifications and tolerances are not stated anywhere in the record.

## Return criteria

- Confirm the AP-MS cell line (293T vs HAP1) with the submitter. The published paper is internally inconsistent, so it cannot settle this on its own.
- Confirm the DENV2 strain, MOI and harvest time of the AP-MS infection, and the IP3 file order (ask the submitter or Taplin).
- Then build a label-free SDRF (`ms-proteomics` + `human` + `cell-lines`), with 27 rows and factor values for bait (HA-RACK1 vs untagged RACK1) and infection (DENV2 vs mock). Pass `parse_sdrf validate-sdrf` and independent review, and move the folder to `datasets/PXD030765/`.
