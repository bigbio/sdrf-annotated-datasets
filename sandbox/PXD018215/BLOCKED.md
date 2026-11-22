# PXD018215 — BLOCKED: SILAC channel-to-sample map not resolvable from public evidence

BLOCKED: no SDRF is provided because the heavy/light channel identity of every
SILAC mixture, and the raw-file-to-gel-slice order of the long-gel runs, cannot be
established from the PRIDE record, the deposited MaxQuant tables or the publication.
Writing those rows would mean inventing sample-to-channel relationships.

## Dataset

- PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD018215
  ("Human DDI2 is a ubiquitin-directed endo-protease"; submission type PARTIAL)
- Publication: Dirac-Svejstrup AB et al. *Mol Cell* 2020;79(2):332-341.e7,
  PMID [32521225](https://europepmc.org/article/MED/32521225), PMCID PMC7369636,
  doi:10.1016/j.molcel.2020.05.035
- Companion UbiSite dataset (not SILAC, not covered here): PXD019152

## What is established

| Item | Value | Evidence |
|---|---|---|
| Organism / cells | Homo sapiens; paper: "DDI2 KO cells" (PRIDE: "WT or DDI2 KO cells"). MRC5VA (SV40-transformed MRC-5) is an inference: SILAC media are described only under MRC5VA culture | Paper, STAR Methods "Cell lines and culture conditions", "Mass spectrometry analysis"; PRIDE sample protocol |
| Quantification | SILAC, two channels (MaxQuant `Ratio H/L`) | PRIDE `quantificationMethods`; deposited `*proteinGroups.txt` headers |
| Workflow | Affinity purification on immobilized catalytically inactive FLAG-DDI2(D→N); elution by SDS buffer or by DDI2 proteolysis; forward + reverse SILAC mixtures; SDS-PAGE; in-gel trypsin digestion | PRIDE sample protocol; paper "Mass spectrometry analysis" |
| Instrument | Orbitrap Fusion Lumos (MS:1002732), Ultimate3000 HPLC, DDA | PRIDE record; paper |
| Search | MaxQuant 1.6.0.1, UniProt human canonical (Nov 2017); tryptic and semi-tryptic searches; Oxidation (M) and Acetyl (Protein N-term) variable | PRIDE data protocol; `modificationSpecificPeptides.txt` headers |
| Raw files | 48 Thermo `.raw` (MGE9284A3–A28, A51–A72) | PRIDE files API |

### Run-to-experiment map that *is* recoverable

`shortgelmodificationSpecificPeptides.txt` (column `Raw file` vs `Experiment *` cross-tab; MaxQuant names such as `MGE9284A3RW3_A1` matched to deposited files on the `MGE9284A<n>` prefix):

| raw file | MaxQuant experiment |
|---|---|
| MGE9284A3RW3-40-563014.raw | 1U |
| MGE9284A4RW3-40-563015.raw | 2U |
| MGE9284A5RW3-40-563016.raw | 1US |
| MGE9284A6RW3-40-563017.raw | 2US |

`longgelshiftproteinGroups.txt` has experiments `S01_01`–`S01_22` and
`S02_01`–`S02_22` (2 lanes × 22 slices = 44), matching the 44 remaining raw files
(A7–A28 and A51–A72), but no deposited file maps raw file to slice.

## What blocks the SDRF

1. **Heavy vs light identity per mixture is not stated anywhere.** PRIDE says "WT or
   DDI2 KO cells were labelled either heavy or light"; the paper says "DDI2 KO cells
   were labeled either heavy or light" and that eluates (SDS vs DDI2 proteolysis)
   were mixed into forward and reverse mixtures. Neither says which condition
   (genotype or elution) carries the heavy label in which mixture, nor which of
   S01/S02 or 1U/1US/2U/2US is forward or reverse. The meaning of the experiment
   names `U`/`US` is not defined. The sources even disagree on the contrast:
   PRIDE implies WT vs KO; the paper's methods imply SDS elution vs DDI2-proteolysis
   elution of KO material; and Table S1 is said to come from Figure 3C lanes 5-8,
   which compares inactivated-DDI2 beads with an empty-bead control.
2. **Table S1 does not describe these runs.** Table S1 (mmc2.xlsx, "data from
   proteins in Figure 3C, lanes 5-8") reports Mix1–Mix4 × Slice01–Slice20
   (80 slice ratios), which matches neither the 22-slice long gel nor the short-gel
   runs deposited here (submission is PARTIAL).
3. **Long-gel raw file → slice order is not deposited.** The A-number sequence
   suggests an order, but run serial numbers are non-monotonic in both lanes
   (e.g. A10 = 563018 sits between A6 = 563017 and A11 = 563069; A7–A9 = 563075–77;
   A55 = 563399 precedes A51 = 563403; A59–A66 run 563414 down to 563407) and no
   MaxQuant table carrying `Raw file` for the long-gel search is deposited
   (`longgelmodificationSpecificPeptides.txt` is byte-identical to the short-gel
   file, and its `Raw file` column holds only A3–A6). The FTP `README.txt` groups
   files A7–A28 and A51–A72 with the long-gel search but gives no slice order.
4. **SILAC isotopes are unspecified** ("heavy Arginine and/or Lysine"); no
   `mqpar.xml` or `parameters.txt` is deposited, so the heavy label modifications
   (e.g. Arg10/Lys8 vs Arg6/Lys4) cannot be stated.

## Sources checked

- PRIDE project record and files API (48 raw + 4 MaxQuant txt), plus the FTP `README.txt` file-mapping table
- Deposited MaxQuant tables: `shortgelproteinGroups.txt`, `longgelshiftproteinGroups.txt`,
  `shortgelmodificationSpecificPeptides.txt`, `longgelmodificationSpecificPeptides.txt` (headers;
  short-gel `Raw file` × `Experiment` cross-tab)
- Europe PMC full text (PMC7369636) and supplementary files (mmc1 Figures S1–S6, mmc2
  Table S1, mmc3 Table S2, mmc4 article PDF): no channel legend
- Data availability statement: cites PXD018215, PXD019152 (label-free UbiSite/PRM, no SILAC map) and Mendeley Data
  doi:10.17632/cz336hbwy8.1, listed as figure source data (western blots, etc.); that DOI did not resolve
  (DOI Not Found) when checked, so it could not be inspected

## What would unblock it

- The authors' `mqpar.xml` / `parameters.txt` and `summary.txt` for both searches
  (gives raw file → experiment and the label modifications), and
- a statement of which condition is heavy in each mixture (forward vs reverse) and
  what `1U`, `1US`, `2U`, `2US` denote.
