# PXD031243 — draft SDRF (sandbox)

**BLOCKED: the raw-file → SILAC experiment/condition map is not public.**

- Dataset: [PXD031243](https://www.ebi.ac.uk/pride/archive/projects/PXD031243) —
  "From incision to excision: active DNA damage eviction by HLTF stimulates repair"
- Publication: van Toorn M *et al.* Active DNA damage eviction by HLTF stimulates
  nucleotide excision repair. *Mol Cell* 2022;82(7):1343-1358.e8.
  PMID [35271816](https://pubmed.ncbi.nlm.nih.gov/35271816/), PMC9473497,
  doi:[10.1016/j.molcel.2022.02.020](https://doi.org/10.1016/j.molcel.2022.02.020)
- Samples: Xpb-YFP knock-in mouse dermal fibroblasts, SILAC 2-plex
  (light Lys0/Arg0, heavy Lys6/Arg10), XPB/TFIIH GFP-Trap pull-downs analysed on
  an Orbitrap Fusion (DDA, HCD, ion-trap MS2).

## What is known

The deposited `1645_1686_proteinGroups.txt` (MaxQuant 1.5.3.8) names six SILAC
experiments:

| MaxQuant experiment | light (K0R0) | heavy (K6R10) |
|---|---|---|
| Exp_K0R0_BCbeads_K6R10_GFP_FW | binding-control beads | GFP-Trap |
| Exp_K0R0_GFP_K6R10_BCbeads_REV | GFP-Trap | binding-control beads |
| Exp_K0R0_mock_K6R10_UV_FW | mock | UV (16 J/m², 1 h) |
| Exp_K0R0_UV_K6R10_mock_REV | UV | mock |
| Exp_1686_K0R0_mock_K6R10_UV_FW | mock | UV |
| Exp_1686_K0R0_UV_K6R10_mock_REV | UV | mock |

The 52 RAW files are `1645_F_YaseminTurkyilmaz_01..28` (60-min method) and
`1686_F_YaseminTurkyilmaz__01..16` plus `1686_F_YaseminTurkyilmaz_least_int_01..08`
(90-min methods). The Thermo headers of the `least_int_NN` files carry the sample
name `1686_F_YaseminTurkyilmaz__NN` and the same tray position, so they are
re-injections of samples `__01..__08` with a "least intense precursor first" DDA
method. The draft encodes them as technical replicate 2 of those samples.

## What is missing

No file in PRIDE, the paper, its Mendeley Data deposit (images only) or the
reachable supplementary material says which raw files belong to which of the six
experiments, or how many gel slices make up one lane. Without that, the condition
of each light/heavy channel cannot be assigned. The draft therefore writes
`characteristics[treatment]` and `factor value[treatment]` as `not available`, and
gives each `1645_*` file its own source name.

Supplementary Table S1 (`NIHMS1817677-supplement-Table_S1.xlsx`) could not be
retrieved automatically. Its caption describes protein-level results.

## To unblock

Deposit or share the MaxQuant `mqpar.xml` or `experimentalDesign.txt` (or
`summary.txt`/`evidence.txt`) for this search. Then fill in the treatment and
pull-down per channel, merge gel-slice files into their lane sources with
`comment[fraction identifier]`, and promote this folder to `datasets/`.
