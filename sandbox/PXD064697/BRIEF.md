# PXD064697: SILAC label-swap mapping recovered; culture independence unresolved

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD064697), the deposited `txt.zip` members `summary.txt` and `parameters.txt`, all six RAW headers, and the [author preprint](https://zenodo.org/records/18759911/files/2025.07.06.663356v1.full.pdf?download=1). Only the ZIP directory and small metadata members were read; the entire result archive was not required.

## Verified channel and bait mapping

Each RAW contains one two-channel SILAC mixture, giving 12 SDRF rows. The PRIDE protocol explicitly defines the swap: in forward experiments, unmethylated bait captures light extract and asymmetrically dimethylated bait captures heavy extract; reverse experiments swap those associations. MaxQuant records light/unlabelled and heavy Arg10/Lys8 channels.

| RAW | MaxQuant experiment | Bait residue in biological description | Light channel | Heavy channel |
| --- | --- | --- | --- | --- |
| Asc_001456.raw | For-750 | R745 | unmodified | asymmetric dimethylation |
| Asc_001458.raw | Rev-750 | R745 | asymmetric dimethylation | unmodified |
| Asc_001461.raw | For-762 | R757 | unmodified | asymmetric dimethylation |
| Asc_001463.raw | Rev-762 | R757 | asymmetric dimethylation | unmodified |
| Asc_001466.raw | For-767 | R767 | unmodified | asymmetric dimethylation |
| Asc_001468.raw | Rev-767 | R767 | asymmetric dimethylation | unmodified |

The 750→745 and 762→757 residue crosswalk is explicitly stated in the deposited preparation protocol. Both numberings are retained. Bait methylation is an experimental factor; it is not added as a variable modification searched across the captured proteome.

Paired pulldowns were combined before digestion of one stacked gel band. Each mixture is assigned physical fraction identifier 1. MaxQuant's deposited `Fraction` values 1, 5 and 10 are preserved in a separate comment; they do not establish ten physical fractions.

All six files identify Orbitrap Ascend, DDA, HCD at 30 NCE and 400–1600 m/z MS1. Physical in-gel trypsin digestion is reported. The actual MaxQuant 2.4.2.0 metadata specify Trypsin/P search specificity, two missed cleavages, fixed C carbamidomethylation, variable M oxidation/protein N-terminal acetylation and 20 ppm FTMS fragment tolerance. A precursor search tolerance is not supplied; the RAW's dynamic exclusion tolerance is not substituted. Reduction and alkylation reagents also remain unknown.

[Cellosaurus CVCL_0062](https://www.cellosaurus.org/CVCL_0062) establishes MDA-MB-231 donor metadata and its metastatic pleural-effusion origin. These are characteristics of the cell line, not twelve separate donors.

## Remaining limitation

Forward/reverse label swaps do not establish independent biological cultures or exclude shared or pooled extracts across bait comparisons. Biological replicate and pooling values remain `not available`. Source identifiers distinguish each documented bait/channel preparation without asserting culture independence; both channels share the corresponding RAW/assay. Missing biological replication is an expected validation blocker, so the draft remains in `sandbox/`.

## Validation

The mass-spectrometry, human and cell-line templates and repository review gate reject the unavailable biological replicate value. Record reconciliation reports no conflicting values. Ontology-cache warnings about sample type and acquisition ancestry are retained. These checks do not establish independence of the underlying cultures.
