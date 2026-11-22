# PXD018617: BLOCKED (no SDRF yet)

**BLOCKED:** this dataset is **not SILAC**. It holds three TMT10plex shotgun
experiments (MM.1S, KMS34 and RPMI-8226 cells, 5 drug conditions × 2 biological
replicates each), so a SILAC annotation would be wrong. The TMT10plex reporter →
sample map is also not in any public evidence I could reach, so a TMT SDRF cannot be
written without inventing channel identities either. There is no `.sdrf.tsv` here.
Nothing below was invented. Each fact cites its source.

- Dataset: <https://www.ebi.ac.uk/pride/archive/projects/PXD018617>
  ("Allosteric HSP70 inhibitors perturb mitochondrial proteostasis and overcome
  proteasome inhibitor resistance in multiple myeloma, dataset 2", submitted 2020-04-17,
  published 2020-04-24)
- Publication: Ferguson ID *et al.*, *Cell Chem Biol* 2022. PMID 35853457, PMC9434701,
  DOI 10.1016/j.chembiol.2022.06.010. The Data Availability statement lists PXD018617,
  PXD018387 and PXD032030.
- PRIDE: "This dataset corresponds to experiment outlined in figure 4a". That is the
  preprint numbering; in the published paper it is **Fig. 3A**, Dataset S2
  ("TMT Proteomics PI-sensitive cells … MM.1S, KMS34, and RPMI-8226 cells").
- Sister datasets: PXD032030 (TMT10plex, AMO1-BtzR, also not SILAC, see
  `sandbox/PXD032030/`), PXD018387 (the only pulsed-SILAC × TMT part of the study,
  BLOCKED in `sandbox/PXD018387/`).

## Why it is not SILAC

| Evidence | What it says | Source |
|---|---|---|
| PRIDE `quantificationMethods` | TMT (PRIDE:0000314); no SILAC entry | PRIDE project record |
| PRIDE sample protocol | "multiplexed TMT drug experiments", "Miniaturized TMT labeling", "10-plex TMT shotgun experiments"; no SILAC media | PRIDE project record |
| MaxQuant `summary.txt` | `Multiplicity` = 1 for every file, LC-MS run type `Reporter ion MS2`, experiments `MM1S`, `KMS34`, `8226` | `summary.txt` |
| MaxQuant `proteinGroups.txt` | `Reporter intensity corrected 0 … 9` per experiment (10 reporters); no H/L ratio columns | `proteinGroups.txt` header |
| Paper, Fig. 3A legend | "Two biological replicates combined into TMT-10plex for each cell line" | PMC9434701 |

## What the public evidence settles (for a later TMT annotation)

| Item | Value | Source |
|---|---|---|
| Organism | Homo sapiens | PRIDE record |
| Cell lines | MM.1S (ATCC CRL-2974), RPMI-8226 (DSMZ ACC 402), KMS34 (JCRB1195) | PRIDE protocol, paper Key Resources Table |
| Disease | plasma cell myeloma (PRIDE: DOID:9538 multiple myeloma); all samples are myeloma cell lines, no control arm | PRIDE, paper |
| Design | 22 h treatment, then one TMT10plex per cell line (5 conditions × 2 biological replicates): MM.1S 1.75 µM JG98, 2.5 nM bortezomib, 1 µM CB-5083, 150 nM DMAG, DMSO; RPMI-8226 1.5 µM JG98, 7.5 nM bortezomib, 1 µM CB-5083, 200 nM DMAG, DMSO; KMS34 2 µM JG98, 7.5 nM bortezomib, 1 µM CB-5083, 500 nM DMAG, DMSO. High-pH kit fractionation (Pierce 84868). | PRIDE sample protocol, paper Fig. 3A legend |
| Raw files → plex / fraction (24 files) | KMS34 F1–F8 = Q20190528-03, -04, -05, **Q20190611-16**, Q20190528-07, -08, -09, **Q20190611-12** (there is no Q20190528-06). MM1S F1–F8 = Q20190521-**10, -09 … -03** (reverse run order). RPMI8226 F1–F8 = Q20190611-**10, -09 … -03** (reverse run order). | deposited `sample_list.xlsx`; experiment per file confirmed by `summary.txt` (which has no Fraction column) |
| Instrument | protocol: Thermo **Q Exactive Plus**, DDA top 15, MS1 70k, MS2 35k, NCE 32. **PRIDE's structured field says Q Exactive (MS:1001911)**; reconcile from the raw file headers before annotating. | PRIDE protocol vs. PRIDE `instruments` |
| Search | MaxQuant 1.6.2.1, Trypsin/P, max. 2 missed cleavages, fixed Carbamidomethyl (C), variable Oxidation (M) and Acetyl (Protein N-term), MS/MS tolerance (FTMS) 20 ppm, match between runs on | `parameters.txt`, `summary.txt` |

## What blocks a TMT SDRF

1. **The reporter → condition map is missing.** MaxQuant reports reporters 0–9 for
   each experiment without naming them. The PRIDE protocol, the deposited
   `sample_list.xlsx` (file → cell line / fraction only) and the paper text do not say
   which TMT10plex channel (126 … 131) holds which drug and replicate, nor whether the
   order is the same in all three plexes.
   - The map is most likely in **Dataset S2** (`NIHMS1825533-supplement-2.xlsx` on PMC).
     The Europe PMC supplementaryFiles endpoint answered "Article with id PMC9434701 is
     not open access one" (on a later try it refused the connection), and the PMC `bin/` URLs return a bot challenge page instead of
     the file. It is unread, not known to lack the map.
2. **Scope.** The request was for a SILAC annotation. A TMT annotation belongs in a
   separate task once the map is available.

## To unblock

- Read Dataset S2 (or ask the authors / Wiita lab) for each cell line's TMT10plex
  channel → (JG98 | bortezomib | CB-5083 | DMAG | DMSO, replicate 1 | 2) assignment.
- Confirm the instrument model from the raw files.
- Then annotate as TMT10plex (`ms-proteomics`, `human`, `cell-lines`),
  24 files × 10 channels = 240 rows, with `factor value[compound]` (and dose), run the
  adversarial review, and promote to `datasets/`.
