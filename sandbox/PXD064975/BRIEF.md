# PXD064975: antibody and cell-line mapping recovered; biological replication unresolved

The 22-row draft was checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD064975), deposited `DesignPRIDE_IP2.xlsx`, all 22 RAW headers and Figure 1/methods in the [author preprint](https://zenodo.org/records/18759911/files/2025.07.06.663356v1.full.pdf?download=1).

## Supported design

The archive title and protocol mention BT-549/HeLa ALIX immunoprecipitation. The deposited author table also includes HCC1187 and CARM1 antibody comparisons. Its explicitly merged cells establish the following mapping:

| Cell line and lysis condition | RAW files, in reagent order | Reagent order |
| --- | --- | --- |
| HCC1187, 0.1% NP40 | C8910FD, C8909FD, C8911FD, C8912FD, C8913FD | IgG rabbit, IgG mouse, CARM1 Ab1 mouse, Ab2 rabbit, Ab3 rabbit |
| HCC1187, 1% NP40 | C8915FD, C8914FD, C8916FD, C8917FD, C8918FD | IgG rabbit, IgG mouse, CARM1 Ab1 mouse, Ab2 rabbit, Ab3 rabbit |
| BT-549, 0.1% NP40 | X1210VM–X1215VM | Same first five reagents, followed by ALIX |
| HeLa, 0.1% NP40 | X1216VM–X1221VM | Same first five reagents, followed by ALIX |

All file names carry `.raw`, and every deposited RAW is represented once. Each author-named MSF counterpart exists. The ten HCC1187 RAW files identify Orbitrap Fusion and 400–1500 m/z MS1; the twelve BT-549/HeLa RAW files identify Orbitrap Exploris 480. Rabbit and mouse describe antibody hosts; all study cell lines are human.

The physical protocol reports on-bead Trypsin/Lys-C digestion and DTT-containing lysis buffer. The reported search uses Sequest HT in Proteome Discoverer 2.4, 10 ppm precursor/0.02 Da fragment tolerances, fixed C carbamidomethylation and variable M oxidation, protein N-terminal acetylation, initiator methionine loss and methionine loss plus acetylation. These are protocol-reported settings; no unverified MSF patch version is supplied. The protocol's statement that trypsin cleaves N-terminal to lysine/arginine is inconsistent and is not used to relabel the physical enzyme as LysargiNase. Carbamidomethylation does not establish an alkylation reagent.

Cell-line donor metadata are supported by [BT-549](https://www.cellosaurus.org/CVCL_1092), [HCC1187](https://www.cellosaurus.org/CVCL_1247) and [HeLa](https://www.cellosaurus.org/CVCL_0030). HCC1187 is not assigned an unreported histological subtype. Donor ages do not denote culture ages.

## Remaining limitation

The workbook gives no biological replicate column or culture/lysate pooling relationships. Western-blot replicate counts in the paper do not establish proteomics replication. Each RAW therefore has an acquisition-linked source identifier and technical identifier 1, while biological replication and pooling remain `not available`; no common lysate or independent culture relationship is invented. Keep the draft in `sandbox/`. Its missing biological replicate value is an expected validation blocker.

## Validation

All three templates and the repository review gate reject the unavailable biological replicate value, as expected. The record-reconciliation CLI also reports a missing Lys-C because it truncates the second of repeated enzyme columns after stripping an accession; checking the set of both declared enzyme values directly returns no enzyme findings. The draft retains both physically reported enzymes. Ontology-cache warnings are retained.
