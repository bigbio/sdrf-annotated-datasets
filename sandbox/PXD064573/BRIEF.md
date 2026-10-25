# PXD064573 — under repair

The two files here are an acquisition-method benchmark (Orbitrap Excedion Pro EThcD study): runs of one digest differ along several orthogonal dimensions at once — supplemental activation 0-35 %, precursor range 350-800 vs 350-1500 m/z, RF settings, HCD vs ETD, and column age. The review gate excuses a repeated coordinate only when a *single* column separates every colliding run, which no one standard column can do for an 8-way method matrix (`comment[collision energy]` covers the activation series, `comment[ms min mz]`/`[ms max mz]` the range variant, `comment[lc batch]` the column age — none covers all). Porting needs a decision: split per method family, or introduce a composite method-variant column.

Affected file(s): `PXD064573-elastase-benchmark.sdrf.tsv`, `PXD064573-immunopeptidomics.sdrf.tsv`.

The other defect classes from the first submission (ontology-invalid `characteristics[sample type]`, `NT=`/`AC=` characteristics cells, pandas artifact headers) are fixed in the file above; the coordinate collisions described here are the only remaining blocker.
