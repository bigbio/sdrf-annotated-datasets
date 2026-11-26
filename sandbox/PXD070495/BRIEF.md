# PXD070495

## Evidence and coverage

The [paper](https://doi.org/10.1038/s41467-026-71418-8), author RAW description
spreadsheet and completed DIA-NN logs map 107 acquisitions: 18 cultured pools,
80 single tissue-neuron contours and nine tissue pools. The spreadsheet note
explicitly defines experiment IDs as different experimental batches. For
57 culture/NF200 acquisitions, complete native RAR membership is verified and
separate canonical files are described in `datasets/PXD070495/README.md`.

## Remaining gaps

The peptidergic/non-peptidergic raw RAR request returned HTTP 403; its member
listing was not verified. Fifty named acquisitions are supported independently
by both the author spreadsheet and DIA-NN statistics, and retained in two
sandbox files: 44 tissue-neuron contours and six pools. Their file URIs point
to the recorded RAR; the member-verification field is explicitly unavailable.
Technical-replicate identity remains unavailable in these drafts. The author
mouse codes here are mouse1, mouse3 and mouse5, not an invented renumbering to
mouse1-mouse3. The identifiers are local to experiment 2.

The peptidergic DIA-NN statistics contain 114 acquisitions, of which 64 are
not covered by the author RAW description table. They are not silently assigned
cell classes or exclusion reasons. The two explicitly named outlier exclusions,
ending 6944 and 7041, are retained as acquisitions with the published exclusion
status where present. Inclusion in the annotation is not inclusion in every
published statistical comparison.

The old three-row archive placeholder is retired. It mislabeled compressed
archives as assays, conflated the two instruments and used PRIDE:0000628
for DIA. Canonical/draft rows now use native acquisition directories and the
current diaPASEF term PRIDE:0000650.

## Local validation

Reviewed 2026-09-28 with sdrf-pipelines `701356bd5309`. Sandbox files retain
the unresolved technical-replicate requirement and explicit archive-verification
gap. The old draft's parser success did not validate its assay granularity.
