# PXD054682 — sandbox brief

**Dataset:** Enrichment of cysteine S-palmitoylated peptides using sodium deoxycholate acid precipitation (SDC-ACE). Mouse, Odense (M.R. Larsen lab). Paper: Mol Cell Proteomics 2026, PMID 41109480 / PMC12874130.

**Status:** draft for review. It covers all 93 of 93 deposited RAW files (501 rows). It passes `parse_sdrf validate-sdrf` (ms-proteomics + vertebrates v1.1.0; warnings only) and `sdrf_review.py` (no coordinate collisions). It sits in `sandbox/` because it came from a deferred batch item and has had no independent review. Promote with `git mv` once reviewed.

## Sub-experiments and evidence

| Runs | Experiment | Instrument (RAW header) | Sample map source |
|---|---|---|---|
| 27 | Brain S-palmitoylome mapping. C57BL/6J, day 21. Two preparations × 12 high-pH fractions + flow-through (fraction 13). Includes 1 unfractionated test run (rep1, technical replicate 2) | Orbitrap Eclipse (test run: Exploris 480) | file names + paper |
| 4 | Acyl-RAC, control vs 1 M hydroxylamine × 2 (pooled NMRI brain membranes) | Orbitrap Astral | `RAC_Control_vs_HA.msf` study factors + paper |
| 6 | SDC-ACE 500 µg, control (H2O) vs DTT × 3 | Orbitrap Astral | file names + paper |
| 12 | Membrane-buffer partitioning, control / HA / DTT × 4, label-free | Orbitrap Astral | `MembraneTreatment_LabelfreePD.msf` + paper |
| 20 × 13 ch | TMTpro tissue set: kidney, heart, brain, liver, BAT, WAT × 2, plus an all-tissue mixture in 134N | Exploris 480 | paper channel list, matching `.msf` study factors |
| 2 × 12 × 8 ch | WT vs db/db brain TMTpro (126–129N WT, 130N–133N db/db). Depalm and Non-Mod peptide sets | Exploris 480 | paper, matching both `.msf` files |

## Open points for a reviewer

- The paper writes the outbred strain as "NMR1". It is recorded here as **NMRI**.
- `MRL_dbdb_Brain_Non-Mod_*`: *enrichment process* is `not available`. Reading these runs as the SDC-soluble, non-palmitoylated peptide fraction is an inference, so treatment is also `not available`.
- db/db disease is recorded as `type 2 diabetes mellitus`; the strain is recorded as "C57BL/6J Lepr db/db", as the paper describes it.
- Sex is not stated anywhere, so it is `not available`.
- PRIDE lists *Acyrthosiphon pisum* as a second organism. Nothing in the files or the paper supports this, so it is ignored (likely a submission error).
- Alkylation is recorded as NEM (free Cys blocked before release) for all sets except membrane partitioning (DTT/IAA). The IAA used after the DTT release step is not a separate column.
- `Mousebrain_rep1_test.raw` (original name `05102022_MRL_MB_10percent_DTT_2.raw`) is not described in the paper.
