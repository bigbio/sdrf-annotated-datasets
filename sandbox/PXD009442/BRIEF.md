# PXD009442: phenotype and search metadata repaired; pool/replicate description unresolved

The existing five-row sandbox draft was rechecked on 2026-09-28 using [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD009442), all five RAW headers, all five deposited pepXML workflow summaries, [the primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6356073/) and [Cellosaurus CVCL_0062](https://www.cellosaurus.org/CVCL_0062). The existing canonical SDRF is retained; it is not used as independent evidence for biological replication.

## Supported mapping and corrections

The five files represent parental MDA-MB-231, its cisplatin-, doxorubicin- and cyclophosphamide-resistant derivatives, and cancer stem-like cells. These are distinct phenotypes, not five parental samples. The drug-resistance labels are not acute linezolid treatments, despite the archive title. The factor is now explicitly linked to `characteristics[cell phenotype]`.

Every RAW identifies LTQ Orbitrap Elite and HCD at 32 NCE. The physical protocol supports FASP, trypsin, DTT and iodoacetamide. Cell-line donor metadata replace inappropriate generic cell-culture anatomy; the derived MDA-MB-231 populations are not assigned new unverified Cellosaurus accessions.

The pepXML summaries contain a multistage workflow. Their initial cRAP contaminant screen uses 7 ppm, 0.03 Da and two missed cleavages. The subsequent human Mascot and Sequest HT searches use **10 ppm, 0.05 Da and one missed cleavage**, matching the stated study protocol. The actual Mascot version is **2.6.1**. Fixed C carbamidomethylation and variable M oxidation, N/Q deamidation and protein N-terminal acetylation are preserved. A first search-summary element would give the wrong tolerances for the human search. Full source RAW basenames embedded in the headers and results identify the corresponding renamed deposited files.

## Remaining limitations

The paper describes pooled cell extracts and mentions 3–5 biological replicates, but does not connect those underlying preparations to the five deposited RAWs. It also mentions TMT in that design description, while PRIDE, the reported quantification method and the deposited processing workflow describe label-free analysis. No channel map or TMT search setting is supplied. The draft retains the directly reported label-free processing and records the unresolved discrepancy here; it does not invent multiplexed rows, pool members or independent cultures.

Biological replicate and pooling relationships therefore remain unavailable. Technical identifier 1 denotes one deposited acquisition for each phenotype-linked preparation. Keep this draft in `sandbox/`; the previous numeric biological-replicate values are not a substitute for a pool-to-file map.

## Local validation

The ms-proteomics, human and cell-lines templates, and consequently the repository review script, fail because biological replicate is unavailable. The pre-existing canonical and sandbox files both passed the review script; removing unsupported replicate assignments exposes this gap rather than proving a new experiment defect. The record-reconciliation control-name warning is not applicable: parental and cancer stem-like MDA-MB-231 populations remain malignant cell-line material. Offline ontology warnings are retained in the validation logs.
