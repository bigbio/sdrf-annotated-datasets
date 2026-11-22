# PXD027739

BLOCKED: 48 of 283 raw files (MaxQuant experiments X1, X2, X3; ELITE-RSLC016247 to ELITE-RSLC016303) have no sample identity in any public source. The other 235 files are fully annotated and checked against the evidence.

## What is annotated (235 raw files, 470 rows)
SILAC (Arg10/Lys8 heavy vs Arg0/Lys0 light), *T. brucei* procyclic strain 29-13, Orbitrap Elite, ms-proteomics v1.1.0. One row per raw file per SILAC channel.

| MaxQuant experiments | Line | Sample |
|---|---|---|
| X4, X6, X8 | ATOM40 RNAi | mitochondria-enriched |
| ATOM19_76h_1-3 | ATOM19 RNAi | mitochondria-enriched |
| A4, A6, A9 | ATOM14 RNAi | mitochondria-enriched |
| Y4, Y6, Y8 | ATOM12 RNAi | mitochondria-enriched |
| H4, H6, H8 | ATOM11 conditional knockout | mitochondria-enriched |
| ATOM46_1-3 | ATOM46 RNAi | mitochondria-enriched |
| D4, D6, D8 | ATOM69 RNAi | mitochondria-enriched |
| D1, D2, D3 | ATOM69 RNAi | whole cells |

How the experiments and channels were mapped:
- Each replicate column of Supplementary Data 1a (Dewar et al. 2022, Nat Commun 13:3084, PMC9163028) was matched against the per-experiment ratios in the deposited `txt.zip/proteinGroups.txt`. Every column matches exactly one MaxQuant experiment, for 100% of its quantified values.
- The "+/- Tet" ratio equals MaxQuant H/L for replicates 1 and 2 and L/H for replicate 3, which is the label switch.
- Each targeted ATOM subunit is depleted in the expected channel.
- An independent reviewer confirmed both the experiment map and the channel map.
- Files map to experiments and fractions through `txt.zip/summary.txt`.

## Why this is in sandbox
- X1, X2 and X3 are 16-fraction SILAC experiments in the joint MaxQuant search. No column of Supplementary Data 1a matches them, and neither the paper nor the PRIDE record describes them.
- Their ratios resemble an ATOM40 knockdown, and X3 is label-switched. Nothing public states the targeted line, the induction state or the sample type.
- Their rows therefore carry `not available` for genotype, compound, cellular component, strain, fractionation and factor values. Their source names are the deposited MaxQuant experiment names.
- The replicate numbers for X1-X3 (1/2/3) follow only the MaxQuant experiment index.

## Other open points
- `characteristics[cellular component]` is not a TERMS.tsv column (the validator accepts it). It separates the mitochondria-enriched pellets from the ATOM69 whole cells.
- ATOM11 is a conditional knockout. For that line, `tetracycline` marks the control channel and the depleted channel has none.
- Induction times (Fig. 1 legend) are not encoded.
- CID and ion-trap MS2 come from a sample of `msms.txt` covering 40 raw files.
- ELITE-RSLC002555 has the same experiment and fraction as ELITE-RSLC002541 (X6, fraction 2), so it is encoded as technical replicate 2.

## Return criteria
- Get the authors' identification of MaxQuant experiments X1-X3 (target line, which channel was induced, whole cells or mito).
- Or a maintainer decision to drop or accept those rows.
- Then re-review and move the folder to `datasets/PXD027739/`.
