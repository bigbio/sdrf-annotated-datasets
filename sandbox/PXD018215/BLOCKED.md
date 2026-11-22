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
| Organism / cells | Homo sapiens; MRC5VA (SV40-transformed MRC-5) parental and CRISPR DDI2 KO | Paper, STAR Methods "Cell lines and culture conditions", "Generation of cell lines" |
| Quantification | SILAC, two channels (MaxQuant `Ratio H/L`) | PRIDE `quantificationMethods`; deposited `*proteinGroups.txt` headers |
| Workflow | Affinity purification on immobilized catalytically inactive FLAG-DDI2(D→N); elution by SDS buffer or by DDI2 proteolysis; forward + reverse SILAC mixtures; SDS-PAGE; in-gel trypsin digestion | PRIDE sample protocol; paper "Mass spectrometry analysis" |
| Instrument | Orbitrap Fusion Lumos (MS:1002732), Ultimate3000 HPLC, DDA | PRIDE record; paper |
| Search | MaxQuant 1.6.0.1, UniProt human canonical (Nov 2017); tryptic and semi-tryptic searches; Oxidation (M) and Acetyl (Protein N-term) variable | PRIDE data protocol; `modificationSpecificPeptides.txt` headers |
| Raw files | 48 Thermo `.raw` (MGE9284A3–A28, A51–A72) | PRIDE files API |

### Run-to-experiment map that *is* recoverable

`shortgelmodificationSpecificPeptides.txt` (column `Raw file` vs `Experiment *`):

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
   names `U`/`US` is not defined.
2. **Table S1 does not describe these runs.** Table S1 (mmc2.xlsx, "data from
   proteins in Figure 3C, lanes 5-8") reports Mix1–Mix4 × Slice01–Slice20
   (80 slice ratios), which matches neither the 22-slice long gel nor the short-gel
   runs deposited here (submission is PARTIAL).
3. **Long-gel raw file → slice order is not deposited.** The A-number sequence
   suggests an order, but run serial numbers in A51–A72 are non-monotonic and no
   MaxQuant table carrying `Raw file` for the long-gel search is deposited
   (`longgelmodificationSpecificPeptides.txt` has the same size and header as the
   short-gel file).
4. **SILAC isotopes are unspecified** ("heavy Arginine and/or Lysine"); no
   `mqpar.xml` or `parameters.txt` is deposited, so the heavy label modifications
   (e.g. Arg10/Lys8 vs Arg6/Lys4) cannot be stated.

## Sources checked

- PRIDE project record and files API (48 raw + 4 MaxQuant txt)
- Deposited MaxQuant tables: `shortgelproteinGroups.txt`, `longgelshiftproteinGroups.txt`,
  `shortgelmodificationSpecificPeptides.txt`, `longgelmodificationSpecificPeptides.txt` (headers;
  short-gel `Raw file` × `Experiment` cross-tab)
- Europe PMC full text (PMC7369636) and supplementary files (mmc1 Figures S1–S6, mmc2
  Table S1, mmc3 Table S2, mmc4 article PDF): no channel legend
- Data availability statement: cites only PXD018215 and PXD019152 (no other repository)

## What would unblock it

- The authors' `mqpar.xml` / `parameters.txt` and `summary.txt` for both searches
  (gives raw file → experiment and the label modifications), and
- a statement of which condition is heavy in each mixture (forward vs reverse) and
  what `1U`, `1US`, `2U`, `2US` denote.
