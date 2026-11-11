# PXD082596: sample mapping recovered; digestion record missing

Reviewed on 2026-09-28 using the [PRIDE project](https://www.ebi.ac.uk/pride/archive/projects/PXD082596)
and its [deposited files](https://ftp.pride.ebi.ac.uk/pride/data/archive/2026/09/PXD082596/).

`metadata.xlsx` maps all 24 RAWs to 12 female mice, aged 18 weeks, with two
sequential protein-extraction fractions from each tail-tendon sample. The
four groups are wild type and oim/oim on C57BL/6J, and wild type and Col1a2
null (tm1b) on C57BL/6N. Fraction 2 combines two extracts from the same
individual; it is not a pool of different mice.

Source names identify each sample/fraction extract. Shared individual IDs
and biological-replicate numbers retain the 12 sample relationships across
fractions. In group D, author replicate numbers 1 and 2 switch between
fractions for sample IDs 156.4 and 156.2. The explicit sample IDs determine
the pairing; the original replicate numbers are retained separately.

All 24 RAW headers identify Orbitrap Exploris 480. Both result archives
contain identical `fragger.params` files and workflows that differ only in
their output directory. Those configurations support 20 ppm precursor and
fragment tolerances, fixed cysteine carbamidomethylation, variable methionine
oxidation and protein N-terminal acetylation, and fully specific K/R cleavage
without proline exclusion. The generated SDRFs contain inconsistent 40/10 ppm
tolerances; the actual configurations and PRIDE protocol agree on 20/20 ppm.

The public preparation protocol stops after extraction and protein
quantification. It does not identify the physical digestion enzyme. The
FragPipe search-specificity setting cannot establish that preparation step.
`comment[cleavage agent details]` therefore remains unavailable. This required
field blocks ms-proteomics validation and promotion to `datasets/`.

The complete mapping and supported settings are retained in the sandbox
SDRF. Resolving the digestion record is required before promotion.

With sdrf-pipelines `701356bd5309f352b499846dcb4c31709b65bf8a`, the vertebrates
template passes and ms-proteomics fails only on the unavailable cleavage
agent. Source reconciliation also reports the unavailable enzyme value as
unsupported. These findings are retained; no placeholder enzyme is supplied.
