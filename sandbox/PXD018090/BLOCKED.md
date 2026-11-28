# BLOCKED: PXD018090 (partial TMT channel map), draft only

**Dataset:** [PXD018090](https://www.ebi.ac.uk/pride/archive/projects/PXD018090), SRSF3 RNPome: TMT10plex IP-MS of GFP immunoprecipitates from mouse P19 cells
**Publication:** Schwich O.D. et al., Genome Biol 2021;22:82. PMID [33706811](https://europepmc.org/article/MED/33706811), [PMC7948361](https://europepmc.org/article/PMC/PMC7948361), doi:10.1186/s13059-021-02298-y

`PXD018090.sdrf.tsv` is a **partial draft**. It covers 6 of the 9 sample-bearing
channels of the only run, `RAW.raw`. It passes `parse_sdrf validate-sdrf` for
`ms-proteomics`, `vertebrates` and `cell-lines` (v1.1.0). It stays in `sandbox/`
because channels in use are missing.

## Annotated channels (6)

These come from the deposited `TMT-channels.txt` and agree with Table S3 (Additional
file 4, columns `NLS_1-3` / `SRSF3_1-3`) and the n = 3 in the Fig. S4A legend:

| channels | sample | sample type |
|---|---|---|
| TMT126, TMT127N, TMT127C | "NLS-GFP DMSO control", replicates 1-3 | negative control |
| TMT128N, TMT128C, TMT129N | "SRSF3-GFP 16h in DMSO", replicates 1-3 | study sample |

## Why it is blocked

1. **Three channels carry real SRSF3-GFP signal, but no source names them.** The
   deposited Proteome Discoverer `SEARCH.msf` uses a TMT10 quan method with all 10
   channels active.
   - Summed reporter heights for TMT129C, TMT130N and TMT130C are 1.15e11, 1.39e11
     and 1.31e11. That matches the SRSF3-GFP channels (1.03-1.24e11) and is well
     above NLS-GFP (3.2-3.8e10).
   - The bait SRSF3 (P84104) takes 13.1 / 16.5 / 16.6 % of its reporter signal in
     these channels, against 0.0-0.4 % in the NLS-GFP channels. GFP and CPSF5 follow
     the same pattern.
   - So these are bait IP samples. Their condition is not in `TMT-channels.txt`,
     Table S3, the paper, Additional file 1, the PD study definition (generic
     `Sample` names, no factors), or the Data Availability links (GEO GSE151724 and
     a GitHub motif-analysis repository).
   - They are omitted from the draft. They are **not** declared unused.
2. **TMT131 is unused.** Its summed signal is 2.7e9, about 2 % of 130C, which fits
   TMT isotopic-impurity spill-over.

## What would unblock it

- A public source that names the condition of TMT129C, TMT130N and TMT130C, for
  example an updated PRIDE sample sheet, a corrected deposit or a later publication.
  "SRSF3-GFP 16h in DMSO" suggests a drug-treated SRSF3-GFP arm against the DMSO
  vehicle, but nothing confirms that.
- Then add the three rows with source-backed characteristics and factor values,
  re-review, and move to `datasets/PXD018090/`.

## Other notes for reviewers

- The raw-file method (`TMT10_APEX_60min(75min)_Top15_35ce_08Th_HF`: 75 min, Top15,
  0.8 m/z isolation) disagrees with the paper (120 min gradient, top 20, 1 Th
  window). The raw file was followed, and only values that agree were written.
- Search parameters come from the Sequest HT node of `SEARCH.msf`: 10 ppm / 0.02 Da;
  TMT6plex K + N-term, Carbamidomethyl C fixed; Oxidation M, protein N-term Acetyl
  variable.
