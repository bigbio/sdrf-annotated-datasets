# PXD064974: mixed PRM/DIA experiments with incomplete DIA preparation metadata

The evidence-complete ten-file PRM subset is now represented at
`datasets/PXD064974/PXD064974-prm.sdrf.tsv`. The two DIA subsets remain here
because their physical digestion and search metadata are unresolved.

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD064974), deposited `DesignPRIDE_solene_methyl_all.xlsx`, `22072024-2.sky`, the three Spectronaut project headers, all 65 Thermo RAW headers and the [author preprint](https://zenodo.org/records/18759911/files/2025.07.06.663356v1.full.pdf?download=1).

## File and sample coverage

The author workbook explicitly describes 65 immunoprecipitation samples. Only its actual merged cell ranges were expanded. Each condition has five author-labelled biological replicates. The drafts preserve those original replicate numbers separately; globally unique biological identifiers distinguish the 65 samples without asserting matched donors or pairing between conditions.

| Draft | RAW files | Cell line | Experiment blocks |
| --- | ---: | --- | --- |
| `PXD064974-prm.sdrf.tsv` | 10 | HeLa | DMSO and EZM2302, five replicates each |
| `PXD064974-dia-hela.sdrf.tsv` | 40 | HeLa | Four inhibitor conditions and four siRNA conditions, five replicates each |
| `PXD064974-dia-hek.sdrf.tsv` | 15 | HEK-ALIX-KO, exact parent unresolved | ALIX EV, ALIX CARM1 ED and ALIX CARM1 WT, five replicates each |

The archive's HeLa-only description and Exploris-only instrument selector do not cover the expanded deposit. All ten PRM acquisitions identify Orbitrap Exploris 480. All 55 DIA acquisitions identify Orbitrap Astral, 380–980 m/z MS1, 4 m/z DIA windows and HCD at 25 NCE. The first overexpression RAW sample descriptions explicitly say `HEK-ALIX-KO_pALIX_EV`, `HEK-ALIX-KO_pALIX_pCARM1_ED` and `HEK-ALIX-KO_pALIX_pCARM1_WT`; the workbook links their subsequent replicates. They are not annotated as HeLa or assigned an unverified HEK293/HEK293T accession.

## Resolved deposited-name discrepancies

The workbook lists eight PRM files with `VM` suffixes, while the deposited acquisitions and Skyline sample paths use `LD`. Skyline independently names their conditions and replicate numbers:

| Workbook names | Actual deposited names | Condition and author replicate |
| --- | --- | --- |
| X8648VM, X8650VM, X8652VM, X8654VM | X8648LD, X8650LD, X8652LD, X8654LD | EZM2302, replicates 2–5 |
| X8649VM, X8651VM, X8653VM, X8655VM | X8649LD, X8651LD, X8653LD, X8655LD | DMSO, replicates 2–5 |

All names above carry `.raw`. Original workbook names remain in `comment[author data file]`. The two first replicates, X8504VM and X8603VM, already match. Two other Skyline entries, X2479VM and X8472VM, are absent from the workbook and deposited RAW inventory; no extra SDRF rows are created for them. The workbook's `Manip 3.sne` spacing discrepancy is resolved by the actual `Manip3.sne` run list, which contains the same 20 siRNA acquisitions.

## Supported methods and remaining gaps

The PRM-specific physical protocol reports LysargiNase, with DTT in lysis buffer. Figure 3d describes 1 uM EZM2302 or 0.01% DMSO for 48 hours. The actual Skyline 22.2.0.527 project uses LysArginase specificity, fixed C carbamidomethylation, and variable M oxidation, R methylation/dimethylation and N-terminal acetylation. Skyline's precursor extraction resolution and m/z matching tolerance are not represented as database search tolerances. An alkylation reagent is not inferred from the configured carbamidomethyl modification.

The 55 newer DIA acquisitions have author sample mappings and explicit biological replicate labels, but their physical digestion protocol and search settings have not been established. The project-level LysargiNase/Skyline description is specifically about the older PRM experiment. It is not copied to the Astral rows. Spectronaut version, modifications, search tolerances and treatment doses/durations for the added experiments remain unavailable. The exact parent and clone of HEK-ALIX-KO also remain unresolved.

Keep both DIA subsets in `sandbox/` pending those clarifications. The PRM subset can be checked independently; a passing structural check does not establish completeness of the accession. HeLa donor metadata come from [Cellosaurus CVCL_0030](https://www.cellosaurus.org/CVCL_0030), and describe the cell-line donor rather than the age of the cultures.

## Validation

The PRM subset passes `ms-proteomics`, `human`, `cell-lines` and the repository review gate. Both DIA subsets fail the mass-spectrometry/DIA templates and review gate solely on the unavailable physical cleavage agent; their human and cell-line checks pass. Record reconciliation flags the missing DIA enzyme against the project-level PRM protocol, reflecting the unresolved scope of that protocol. Existing ontology-cache warnings for free-text treatments, sample type and acquisition ancestry are retained. No check result overrides the missing physical evidence.
