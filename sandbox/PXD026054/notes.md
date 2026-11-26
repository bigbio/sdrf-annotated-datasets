# PXD026054

BLOCKED: not a SILAC dataset. This deposit holds only the label-free UBE2D3-TULIP2 pull-downs in HeLa cells. The study's SILAC diGly data are in a separate deposit, PXD035045. The label-free SDRF here passes `parse_sdrf validate-sdrf`. A curator should decide whether to promote it to `datasets/` as a label-free annotation.

## Evidence
- PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD026054. Quantification is "Label free". The instrument is an Orbitrap Exploris 480. There are 24 RAW files.
- Paper: Yalçin et al., Mol Cell Proteomics 2023;22(6):100548. PMID 37059365, PMC10209342, doi:10.1016/j.mcpro.2023.100548.
  - The Data Availability section names PXD026054 for TULIP2 and PXD035045 for the SILAC-based and LFQ diGly proteomics.
- Deposited MaxQuant files:
  - `txt.zip`: `summary.txt` and `parameters.txt`.
  - `MQ_search_files.zip`: `mqpar - Copy.xml`, with multiplicity 1 and lfqMode 1.
  - These give the raw file → experiment map used for the source names.

## Design
| construct (factor value[genetic modification]) | MG132 (factor value[treatment]) | runs |
|---|---|---|
| UBE2D3 wild type TULIP2 | control / Proteasome Inhibitor MG-132 | 4 / 4 |
| UBE2D3 wild type TULIP2deltaGG (negative control) | control / Proteasome Inhibitor MG-132 | 4 / 4 |
| UBE2D3 C85A TULIP2 (catalytically inactive) | control / Proteasome Inhibitor MG-132 | 4 / 4 |

## Open points
- The passage number is not stated, so it is set to `not available`.
- Biological replicates 1-4 are taken from the experiment-name suffixes. The deposit does not say whether replicates are paired across conditions.

## Return criteria
- A curator accepts this as a label-free annotation. Then `git mv sandbox/PXD026054 datasets/PXD026054`.
