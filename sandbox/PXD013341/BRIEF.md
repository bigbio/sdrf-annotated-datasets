# PXD013341: WT/K3 sample map recovered from the author figure

Checked on 2026-09-29 against the [PRIDE project](https://www.ebi.ac.uk/pride/archive/projects/PXD013341), all ten deposited SWATH `.wiff` names, the [primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6600635/) and its Expanded View Figure 2 / supporting data.

The project protocol states that one brain hemisphere was taken from each mouse and that the SWATH experiment contains five WT and five K3 samples. Expanded View Figure 2 labels the ten individual heatmap columns as `WT-1191`, `WT-1196`, `WT-1194`, `WT-1202`, `WT-1200`, `K3-1192`, `K3-1193`, `K3-1203`, `K3-1204` and `K3-1201`. Those suffixes match the ten deposited RAW basenames exactly:

| Author label | Deposited RAW |
| --- | --- |
| WT-1191 | `180323_P21492_1191_SWATH.wiff` |
| WT-1196 | `180322_P21324_1196_SWATH.wiff` |
| WT-1194 | `180323_P21492_1194_SWATH.wiff` |
| WT-1202 | `180323_P21492_1202_SWATH.wiff` |
| WT-1200 | `180326_P21492_1200_SWATH.wiff` |
| K3-1192 | `180323_P21492_1192_SWATH.wiff` |
| K3-1193 | `180323_P21492_1193_SWATH.wiff` |
| K3-1203 | `180322_P21324_1203_SWATH.wiff` |
| K3-1204 | `180323_P21492_1204_SWATH.wiff` |
| K3-1201 | `180326_P21492_1201_SWATH.wiff` |

The draft now uses the author label as `source name`, its numeric suffix as the biological-replicate identifier, and records `WT` or `K3` in `factor value[genotype]`, while leaving sample-level disease as `not available` rather than converting a tauopathy model into a clinical diagnosis. Each deposited acquisition has technical replicate 1 and fraction 1. The project and article directly support mouse brain, SWATH/DIA, and trypsin digestion; no additional fractions or technical injections are created.

## Local validation

The revised draft has ten rows with exact one-to-one coverage of the ten deposited SWATH RAW files and no `FILL` placeholders. Search/quantification settings remain those reported by PRIDE and the article: ProteinPilot 5.0 for IDA search, PeakView 2.1 ion-library/SWATH extraction, and fixed cysteine carbamidomethylation with methionine oxidation retained in the ion library. The article reports DTT reduction and iodoacetamide alkylation before trypsin digestion. A separate workflow or raw-file alias is not inferred from the larger `.wiff.scan` representations. The pinned `ms-proteomics` and `dia-acquisition` validators, repository review, and deposit reconciliation all pass; the validator retains only the existing advisory that the plain acquisition label could use an ontology accession.
