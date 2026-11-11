# PXD057118: partial colorectal annotation; tonsil channel map unresolved

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD057118), the deposited `Metadata.xlsx`, all six ZIP directories, the colorectal result tables, all 33 included Astral RAW headers and all 14 included timsTOF TDF headers.

The previous single-row draft treated a tonsil protein matrix as one label-free single cell. Retire that placeholder. The author explicitly describes colorectal samples as label-free, while tonsil samples use three dimethyl channels with a bulk reference. Neither a protein matrix nor a pooled laser-dissection population establishes one cell per well.

## Covered acquisitions

| Draft | Files | Direct evidence |
| --- | ---: | --- |
| `PXD057118-colorectal-astral.sdrf.tsv` | 33 | 12 T-cell, 6 macrophage and 15 instrument-comparison RAW files; archive members and all RAW methods checked |
| `PXD057118-colorectal-timstof.sdrf.tsv` | 14 | All uploaded comparison `.d` directories; TDF instrument identities and mass ranges checked |

`Metadata.xlsx` defines CTLs as cytotoxic T lymphocytes and TH as helper T cells. The filenames identify spatial regions and repeat indices. They do not establish patient identities or whether repeated dissections constitute biological or technical replicates. Those fields, pooling and per-run cell counts remain unresolved. The Cell Ontology label `neoplastic cell` has the exact synonym `tumor cell` ([CL:0001063](https://www.ebi.ac.uk/ols4/ontologies/cl/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FCL_0001063)); no malignant subtype is inferred.

The Astral files use DIA, HCD 25 NCE, a 380–980 m/z survey and nominal 8 m/z isolation windows. The original 18 immune-cell runs have 75 scan events; the 15 comparison runs have 74. The 14 Bruker files identify timsTOF SCP and a 100–1700 m/z acquisition range. Their detailed DIA-window and collision-energy settings remain unavailable. Separate SDRFs retain the distinct DIA and diaPASEF terms required by the template's single-value acquisition rule.

The physical protocol names both Lys-C and trypsin. DIA-NN 1.8.1, Trypsin/P search specificity, one missed cleavage, variable oxidation/N-terminal acetylation, methionine excision and the 2023 human UniProt reference are reported. The prose gives both 15 ppm tolerances and automatic first-run inference; actual search tolerances remain unavailable. Reduction, alkylation and a complete fixed-modification configuration are not established for the included runs.

## Unresolved coverage

- `timsTOF_pg_matrix.txt` lists 15 runs, but its lamina-propria stromal repeat 2 (`..._2_S2-A7_1_4582.d`) is absent from the ZIP. Only the 14 uploaded runs are represented.
- The 24 tonsil multiplex runs lack a group/channel-to-cell-population map. Their matrix columns do not supply that crosswalk.
- The 48 library acquisitions are excluded. The metadata lists 48 fractions, while PRIDE prose describes five library single shots. That discrepancy is unresolved.
- AppleDouble `._*.raw` archive entries are filesystem metadata, not acquisitions. The six archives contain 119 actual RAW/`.d` acquisitions in total; these drafts cover 47.
- The primary research DOI is [10.1016/j.molcel.2024.12.023](https://doi.org/10.1016/j.molcel.2024.12.023). The linked protocol article, article indexes and author-repository landing pages were located, but full-text retrieval returned 403/429. No unavailable paper-level donor or cell-count mapping is claimed.

## Local validation

Both drafts remain in `sandbox/`. Final ms-proteomics, human and dia-acquisition checks, and repository review, still fail on unavailable biological and technical replicates. The old matrix placeholder passed repository review; that pass did not validate its sample interpretation. Ontology-cache warnings remain visible in the logs.

The record reconciler incorrectly applies the project-wide dimethyl tag to these explicitly label-free colorectal subsets and reads only the first of the two enzyme columns. Both enzymes pass a direct check of the actual column values. These reconciliation limitations do not resolve the remaining sample-map gaps.
