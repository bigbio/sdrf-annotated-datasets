# PXD018387: BLOCKED (no SDRF yet)

**BLOCKED:** I could not resolve the TMT channel → sample (treatment × time point) map
from public evidence I could reach. The design is also a **pulsed-SILAC × TMT
hyperplex**, and SDRF 1.x has no agreed way to write one row for each (SILAC
channel, TMT channel) pair: `comment[label]` holds a single label per row. So there
is no `.sdrf.tsv` here yet. Nothing below was invented. Each fact cites its source.

- Dataset: <https://www.ebi.ac.uk/pride/archive/projects/PXD018387>
- Publication: Ferguson ID *et al.*, "Allosteric HSP70 inhibitors perturb mitochondrial
  proteostasis and overcome proteasome inhibitor resistance in multiple myeloma",
  *Cell Chem Biol* 2022. PMID 35853457, PMC9434701, DOI 10.1016/j.chembiol.2022.06.010.
  Preprint: bioRxiv 10.1101/2020.04.21.052456.
- PRIDE: "This dataset corresponds to … experiment outlined in figure 5a". The published
  version calls it Fig. 4A, Dataset S3.

## What the public evidence settles

| Item | Value | Source |
|---|---|---|
| Organism | Homo sapiens | PRIDE record |
| Cell line | MM.1S (Cellosaurus CVCL_8792) | PRIDE protocol, paper STAR Methods (ATCC CRL-2974) |
| Disease | plasma cell myeloma (MONDO:0009693) | PRIDE (DOID:9538), paper. All rows are the same cell line, so there is no control arm. |
| Design | Cells in light SILAC medium, switched at t = 0 to heavy medium with 350 nM JG342 or DMSO. Harvested at 16, 21 and 26 h. Combined in **7-plex** TMT experiments, high-pH fractionated. | PRIDE sample protocol, paper Fig. 4A legend |
| SILAC labels | light, and heavy = L-Lys-13C6,15N2 (UNIMOD:259 Label:13C(6)15N(2), K) + L-Arg-13C6,15N4 (UNIMOD:267 Label:13C(6)15N(4), R) | paper Methods (SILAC media), `mqpar.xml` (heavy group: fixed `Arg10sub`, custom `HLys…` TMT+Lys8 labels) |
| TMT | TMT10plex reagents, MaxQuant "Reporter ion MS2". Only reporters **0–6 carry signal** (summed corrected intensity ~1e10–8e10 in every L1/L2/H1/H2 group, against ≤6e8 for reporters 7–9). | `mqpar.xml`, `proteinGroups.txt` |
| Raw files → plex / fraction | Z20181031-15…24 = replicate 1, fractions 1–10. Z20181031-26…35 = replicate 2, fractions 1–10 (there is no -25). 20 raw files. | deposited `pSILACTMTmsmsdatafilesheet.xlsx`, `mqpar.xml` experiments L1/L2/H1/H2 |
| Instrument | Orbitrap Fusion Lumos (MS:1002732), HCD 38 %, MS2 in Orbitrap at 50k | PRIDE protocol |
| Search | MaxQuant 1.6.2.1, Trypsin/P, 2 missed cleavages, fixed Carbamidomethyl (C), variable Oxidation (M) and Acetyl (Protein N-term), main search 4.5 ppm, reporter tolerance 0.003 Da | `mqpar.xml`, `parameters.txt`, `summary.txt` |

## What blocks the SDRF

1. **The channel → sample map is missing.** Reporters 0–6 are 7 samples per plex, but
   3 time points × 2 treatments is only 6. The identity of the 7th channel is not stated
   anywhere I could read: the PRIDE protocol, the PMC author-manuscript text, or the
   deposited sample sheet (which only maps file → replicate/fraction). The order of the
   six known conditions across reporters 126–129C is not stated either.
   - The map is most likely in **Dataset S3** (`NIHMS1825533-supplement-3.xlsx` on PMC).
     The Europe PMC supplementaryFiles endpoint answers "not open access" for this
     article, and I could not download the file from PMC in this session. It is unread,
     not known to lack the map.
   - Note: in `mqpar.xml` the heavy parameter group lists the isobaric labels in a
     different order from the light group (126C, 127C, 127N, 128C, 128N…). Check how
     reporter index maps to channel in the heavy group before using MaxQuant indices.
   - I also could not confirm whether replicate 1 and replicate 2 are independent
     biological replicates or a repeated 7-plex of the same lysates. The paper states two
     biological replicates for TMT-proteomics and RNA-seq in general, but not for this
     experiment specifically.
2. **SILAC × TMT hyperplexing.** Each raw file holds 2 SILAC states × 7 TMT channels =
   14 quantified "channels" (280 rows for 20 files). `comment[label]` holds one label
   per row, and row identity is (source name, assay name, label). I need a maintainer
   decision on how to encode this (for example a second label column, or the TMT label
   plus a SILAC characteristic) before an SDRF can be written without loss.

## To unblock

- Read Dataset S3 (or ask the authors / Wiita lab) for the reporter → (JG342 | DMSO,
  16 | 21 | 26 h, 7th channel) assignment and the nature of replicates 1 and 2.
- Agree in `bigbio/proteomics-sample-metadata` on a representation for SILAC × TMT
  hyperplex rows.
- Then: `sdrf-tools build` with samples.tsv (one row per source × SILAC × TMT channel),
  validate with `-t ms-proteomics -t human -t cell-lines`, run the adversarial review,
  and promote to `datasets/`.
