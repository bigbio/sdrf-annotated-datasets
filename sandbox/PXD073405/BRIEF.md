# PXD073405

## Evidence and coverage

See the evidence and parameter audit in `datasets/PXD073405/README.md`, based
on [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD073405), the
[paper](https://doi.org/10.1021/acs.jproteome.5c00972), 46 RAW headers, four
original Proteome Discoverer configurations and three Skyline documents.

The 36 HeLa digest runs are represented by three canonical subsets.
The sandbox subset represents ten Jurkat sets, each containing 15 single cells
in TMT channels 126 through 133C, for 150 rows. RAW and Skyline names map
bijectively. Cell identifiers combine the author's set and tag identifiers;
original plate-well identifiers are not available. Cell-line lineage is
[Jurkat CVCL_0065](https://www.cellosaurus.org/CVCL_0065), without assigning an
unreported Jurkat subclone. Cells were sorted and processed with cellenONE.
Physical trypsin digestion is explicit in the paper.

## Remaining gaps and corrections

The number and identity of independently cultured preparations are not
specified. Biological replicate stays unavailable; 150 cells are not declared
150 independent cultures. Each labeled cell has one deposited acquisition.
No carrier or reference channel is introduced: the shTMTpro synthetic peptides
serve as trigger standards, and the authors explicitly note the absence of a
reference channel. The previous 46-row draft incorrectly called every RAW a
single HeLa cell, omitted channel expansion and used an incorrect PRM accession
and collision energy. It is replaced by the separate subsets.

## Local validation

Reviewed 2026-09-28 with sdrf-pipelines `701356bd5309`. Jurkat remains in
sandbox because the biological-replicate field cannot be supported. The old
draft's successful parser result did not establish correct cell types or
sample/channel relationships.
