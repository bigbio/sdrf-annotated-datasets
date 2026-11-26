# PXD032030: BLOCKED (no SDRF yet)

**BLOCKED:** this dataset is **not SILAC**. It is one TMT10plex shotgun experiment
(AMO1-BtzR cells, 5 drug conditions), so a SILAC annotation would be wrong. The
TMT10plex reporter → sample map is also not in any public evidence I could reach,
so a TMT SDRF cannot be written without inventing channel identities either.
There is no `.sdrf.tsv` here. Nothing below was invented. Each fact cites its source.

- Dataset: <https://www.ebi.ac.uk/pride/archive/projects/PXD032030>
  ("Allosteric HSP70 inhibitors in Proteasome Inhibitor Resistant Multiple Myeloma",
  submitted 2022-03-03, published 2022-05-27)
- Publication: Ferguson ID *et al.*, "Allosteric HSP70 inhibitors perturb mitochondrial
  proteostasis and overcome proteasome inhibitor resistance in multiple myeloma",
  *Cell Chem Biol* 2022. PMID 35853457, PMC9434701, DOI 10.1016/j.chembiol.2022.06.010.
  The Data Availability statement lists PXD018617, PXD018387 and PXD032030.
- In the paper this dataset is the AMO1-BtzR TMT experiment: Fig. S3D, Dataset S4
  ("TMT Proteomics PI-resistant cells … TMT shotgun proteomics experiments in AMO1-BtzR cells").
- Sister datasets: PXD018617 (TMT10plex, MM.1S / KMS34 / RPMI-8226, Fig. 3A, also not
  SILAC, see `sandbox/PXD018617/`), PXD018387 (the only pulsed-SILAC × TMT part of the
  study, BLOCKED in `sandbox/PXD018387/`).

## Why it is not SILAC

| Evidence | What it says | Source |
|---|---|---|
| PRIDE `quantificationMethods` | TMT (PRIDE:0000314); no SILAC entry | PRIDE project record |
| PRIDE sample protocol | "Miniaturized TMT labeling … 50 µg TMT reagent"; no SILAC media, no isotope-labelled amino acids | PRIDE project record |
| Deposited sample sheet | every file is "AMO1 BtzR **10plex** Fraction 1…8" | `Sample_List.xlsx` |
| MaxQuant `summary.txt` | `Multiplicity` = 1 (no SILAC label partners), LC-MS run type `Reporter ion MS2`, one experiment `AMO1` | `summary.txt` |
| MaxQuant `proteinGroups.txt` | `Reporter intensity corrected 1 … 10 AMO1` (10 reporters); no H/L ratio or intensity columns | `proteinGroups.txt` header |
| Paper | SILAC appears only for the MM.1S pulsed-SILAC-TMT 7-plex (Fig. 4A, Dataset S3, Fusion Lumos) = PXD018387 | PMC9434701 Methods, figure legends |

## What the public evidence settles (for a later TMT annotation)

| Item | Value | Source |
|---|---|---|
| Organism | Homo sapiens | PRIDE record |
| Cell line | AMO1-BtzR, a bortezomib-resistant derivative of AMO-1 (Besse et al., 2018; Soriano et al., 2016). Parental AMO-1 is Cellosaurus CVCL_1806; whether Cellosaurus has an entry for the BtzR derivative was not checked. | PRIDE protocol, paper Results |
| Disease | plasma cell myeloma (PRIDE: DOID:9538 multiple myeloma). All channels are the same cell line, so there is no healthy control arm. | PRIDE, paper |
| Design | AMO1-BtzR treated 22 h with 800 nM JG98, 400 nM JG342, 200 nM DMAG, 800 nM CB-5083 or DMSO; one TMT10plex; high-pH reversed-phase kit fractionation (Pierce 84868) into 8 fractions (the protocol lists only 7 acetonitrile steps, but 8 raw files carry MaxQuant `Fraction` 1–8). The paper says "two biological replicates per condition" for TMT proteomics in general, which fits 5 × 2 = 10, but it does not say so for this plex specifically. | PRIDE sample protocol, paper Methods / Quantification |
| Raw files → fraction | Q20210823-04 … -11 = fractions 1 … 8 (8 raw files) | `Sample_List.xlsx`, `summary.txt` `Fraction` column |
| Instrument | Q Exactive Plus (MS:1002634), DDA top 15, MS1 70k, MS2 35k, NCE 32 | PRIDE record and protocol, paper Methods |
| Digest | Trypsin (Pierce 90057) per the protocol. **Note:** the MaxQuant search used `Trypsin/P;LysC`. | PRIDE protocol, `summary.txt` |
| Search | MaxQuant (`parameters.txt` says version 2.0.2.0; the PRIDE data-processing text says 1.6.2.1), fixed Carbamidomethyl (C), variable Oxidation (M) and Acetyl (Protein N-term), max. 2 missed cleavages, MS/MS tolerance (FTMS) 20 ppm, PSM/protein FDR 0.01. **Note:** `parameters.txt` has `Match between runs False`; the PRIDE text says match between runs was used. | `parameters.txt`, `summary.txt`, PRIDE |

## What blocks a TMT SDRF

1. **The reporter → condition map is missing.** MaxQuant reports reporters 1–10 for
   the single experiment `AMO1` without naming them. The PRIDE protocol, the deposited
   `Sample_List.xlsx` (file → fraction only) and the paper text do not say which
   TMT10plex channel (126 … 131) holds which drug or replicate.
   - The map is most likely in **Dataset S4** (`NIHMS1825533-supplement-4.xlsx` on PMC).
     The Europe PMC supplementaryFiles endpoint answered "Article with id PMC9434701 is
     not open access one" (on a later try it refused the connection), and the PMC `bin/` URLs return a bot challenge page instead of
     the file. It is unread, not known to lack the map.
2. **Scope.** The request was for a SILAC annotation. A TMT annotation belongs in a
   separate task once the map is available.

## To unblock

- Read Dataset S4 (or ask the authors / Wiita lab) for the TMT10plex channel →
  (JG98 | JG342 | DMAG | CB-5083 | DMSO, replicate) assignment.
- Then annotate as TMT10plex (`ms-proteomics`, `human`, `cell-lines`), 8 files × 10
  channels = 80 rows, with `factor value[compound]` (and dose), run the adversarial
  review, and promote to `datasets/`.
