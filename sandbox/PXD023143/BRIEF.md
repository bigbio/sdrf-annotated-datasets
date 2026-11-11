# PXD023143 — under repair

4 coordinate collisions remain. Each group is one donor sample measured at three hepatocyte input levels (100E6, 400E6 and 1800E6 cells — the tokens appear in the deposited filenames). That is a real experimental variable, but no column in the declared templates (`ms-proteomics`, `immunopeptidomics`, `sample-metadata`) carries an input amount or cell count: `characteristics[tissue mass]` is for tissue and there is no injected-amount column. Porting needs a decision — a non-standard `characteristics[input cell number]` column, or treating each input level as its own `source name`.

Affected file(s): `PXD023143.sdrf.tsv`.

The other defect classes from the first submission (ontology-invalid `characteristics[sample type]`, `NT=`/`AC=` characteristics cells, pandas artifact headers) are fixed in the file above; the coordinate collisions described here are the only remaining blocker.
