# PXD033714 — under repair
`PXD033714-human.sdrf.tsv` is held in `sandbox/` because it does not pass the repository review gate.
## Blocker
1 coordinate collision. `20190820_EZ_FedeIMR90_NoC18_11_1.raw` and `20190820_EZ_FedeIMR90_NoC18_11_4ug_1.raw` differ only by the loaded peptide amount (4 µg), and no template column carries sample load. Encoding it in `source name` would make the two runs different samples, which they are not.
## What would resolve it
Submitter or publication evidence naming the dimension that separates the colliding runs, or a template column able to carry it. The annotation is otherwise complete and passes `parse_sdrf validate-sdrf`.

The other sheets for this accession are gate-clean and live in `datasets/PXD033714/`: `PXD033714-mouse.sdrf.tsv`.
