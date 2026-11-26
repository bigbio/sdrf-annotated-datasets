# PXD070374 — under repair
`PXD070374-celllines.sdrf.tsv` is held in `sandbox/` because it does not pass the repository review gate.
## Blocker
16 coordinate collisions, including groups of 10 and 12. The deposit is a fragmentation-method benchmark: each sample is acquired under CID, EAD and ExCID, and ExCID is repeated across kinetic-energy (KE3/KE6/KE9) and reaction-time (10/20 ms) settings. `comment[dissociation method]` separates 10 of 16 groups; the KE and reaction-time axes have no column, and the review gate accepts only a single separating column, so no split on one axis clears groups of this size.
## What would resolve it
Submitter or publication evidence naming the dimension that separates the colliding runs, or a template column able to carry it. The annotation is otherwise complete and passes `parse_sdrf validate-sdrf`.

The other sheets for this accession are gate-clean and live in `datasets/PXD070374/`: `PXD070374-synthetic.sdrf.tsv`.
