# PXD007683: mixed-species LFQ and TMT benchmark

## Evidence and corrected coverage

The [deposit](https://www.ebi.ac.uk/pride/archive/projects/PXD007683),
[paper](https://doi.org/10.1021/acs.jproteome.8b00016), and publisher
[Table 1](https://doi.org/10.1021/acs.jproteome.8b00016.s002) and
[Table 2](https://doi.org/10.1021/acs.jproteome.8b00016.s003) were inspected.
All 22 native RAW headers identify Fusion Lumos and distinguish eleven
`jdoc_LFQ_` samples from eleven `jdoc_TMT11` fraction acquisitions.
LFQ native IDs include 01, 02 and 04-12; the missing 03 is not fabricated.

Table 1 supplies an explicit TMT tag-to-group key: 126/127N/127C are group 1
(10% yeast protein), 128N/128C/129N/129C group 2 (5%), and
130N/130C/131N/131C group 3 (3.3%). The TMT draft contains 121 rows.
Both proteomes were physically digested with Lys-C followed by trypsin.
Preparation aliquots from shared stocks are not asserted to be independently
cultured biological replicates. Native SPS-MS3 settings distinguish CID at
35 NCE from reporter HCD at 65 NCE.

## Remaining gaps

The eleven LFQ RAW-to-group assignments in the old draft are not independently
supported by the inspected files. The source tables name groups 1a-3d, while
native RAW metadata uses numerical LFQ IDs. Ordering alone is insufficient:
yeast fractions remain unavailable in the corrected eleven-row LFQ draft.

For TMT, eleven of 24 concatenated fractions were measured, but the inspected
sources do not map each RAW to its original fraction number. Fraction identifiers
remain unavailable. The deposited TGZ search archives were not inspected;
the paper's search tolerances are explicitly reported fields, and no original
MaxQuant configuration is claimed to have been read.

The existing 22-row canonical file remains outside this draft replacement;
its all-label-free, yeast-only representation does not describe the full mixed
LFQ/TMT design and must not be treated as validated by this review.

## Local validation

Reviewed 2026-09-28 with sdrf-pipelines `701356bd5309`. The LFQ draft passes
`ms-proteomics` and repository review, with a `no_factor_value` advisory because
the concentration groups cannot be assigned. TMT fails the required fraction
check and has eleven coordinate-collision groups caused by those unavailable
fraction identifiers. Both files remain in sandbox because of the
source-mapping gaps above. The deposit-only
TMT flag is too broad for its genuine LFQ subset; physical Lys-C/trypsin is
explicit in the paper although not recognized by the deposit-only heuristic.
