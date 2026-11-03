# PXD025073 — under repair
`PXD025073-phosphotyrosine.sdrf.tsv` is held in `sandbox/` because it does not pass the repository review gate.
## Blocker
9 coordinate collisions. The colliding runs are TMT boost-channel variants of one sample — `A549_pTyr_noBoost.raw`, `A549_pTyr_9xEGFboost_250msIT.raw` and injection-time variants. The boost condition and the ion-injection time are the dimensions that separate them, and the declared templates have no column for either; `comment[acquisition date]` separates 8 of the 9 groups but not all, which the review gate requires.
## What would resolve it
Submitter or publication evidence naming the dimension that separates the colliding runs, or a template column able to carry it. The annotation is otherwise complete and passes `parse_sdrf validate-sdrf`.

The other sheets for this accession are gate-clean and live in `datasets/PXD025073/`: `PXD025073-immunopeptidome.sdrf.tsv`.
