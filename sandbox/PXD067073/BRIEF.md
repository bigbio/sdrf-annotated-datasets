# PXD067073: 79 SWATH sample mappings; physical digest and pooled IDA design incomplete

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD067073), the complete 198-file inventory, deposited `SampleLegend.txt`, `DIANN_Report.log.txt` and `DIANN.pg_matrix.tsv`. Two representative WIFF prefixes were inspected; their available method descriptions support the distinction between IDA and SWATH, but the precise instrument model is taken from the reported protocol.

## Supported clinical sample mapping

The deposited legend explicitly defines the filename cohort tokens:

| Token | Clinical group | Deposited SWATH acquisitions |
| --- | --- | ---: |
| Dn | Type 2 diabetes without chronic kidney disease | 19 |
| He | Healthy control | 20 |
| Pr | Progressive diabetic kidney disease | 20 |
| St | Stable diabetic kidney disease | 20 |

All 79 SWATH files carry distinct PDN/SKI sample identifiers, and every one is present in the protein matrix. These identifiers, author sample numbers and cohort labels are preserved. Ages, sex, ancestry and a per-identifier biobank crosswalk are not supplied. Small and large vesicle fractions from each urine sample were combined; this is not treated as pooling different patients. The literal `_HALF` suffix on SKI1019 is recorded without inventing a dilution factor or another sample.

The archive also contains **12 IDA pool acquisitions** (four named cohort pools, i1–i3) and their WIFF scan companions. The pool membership, pool construction and replicate stage are not established, so they are not included in this SWATH draft. No role in the current DIA-NN analysis is assigned to them merely because they are DDA acquisitions.

## Results do not define extra deposited samples

The protein matrix and log additionally reference **24 `_DEP`, `_EV` and `_WU` files** from a separate acquisition batch that are absent from this accession's inventory. They are not added as RAW rows. The current draft therefore covers 79 of 91 deposited WIFF files. Every annotated `.wiff` has a verified `.wiff.scan` companion and both file locations are recorded.

The actual DIA-NN 1.8 log specifies `SwissProt_Human_June2021.fasta`, rather than the May date in the project description. It records K/R cleavage specificity, one missed cleavage, fixed C carbamidomethylation, variable M oxidation, and per-run optimisation of mass accuracy and scan windows. Individual optimisation messages are not replaced by one invented common search tolerance.

## Remaining limitations

The physical sample protocol names S-Trap micro preparation but does not name a protease, reduction reagent or alkylation reagent. A search cleavage rule does not establish the digestion enzyme used in the laboratory. Those values remain unavailable. Keep the 79-row subset in `sandbox/` until the physical preparation and the 12 pooled acquisitions are documented. A generic manufacturer's protocol or a similarly titled urine study would not resolve this accession's missing evidence.

## Local validation

The human template passes. The ms-proteomics and dia-acquisition templates, and consequently the repository review script, fail because the physical cleavage agent is unavailable. The separate record-reconciliation warning that every row has diabetes is incorrect: the draft contains 19 diabetes-without-CKD, 20 healthy-control and 40 diabetic-kidney-disease rows, matching the deposited legend. The absent physical enzyme remains a genuine evidence gap. Offline ontology warnings are retained in the validation logs.
