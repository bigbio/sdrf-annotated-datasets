# sdrf-annotated-datasets

This repository is the canonical home for ProteomeXchange datasets annotated in SDRF.

The annotated projects were moved out of the SDRF specification repository to keep
the specification lifecycle stable while allowing annotated datasets to evolve
continuously.

## Dataset layout

Each dataset is stored under:

`datasets/{ACCESSION}/{ACCESSION}.sdrf.tsv`

Examples:

- `datasets/PXD000070/PXD000070.sdrf.tsv`
- `datasets/MSV000078494/MSV000078494.sdrf.tsv`

## Migration context

- Source repository: `bigbio/proteomics-sample-metadata`
- Migration discussion: https://github.com/bigbio/proteomics-sample-metadata/issues/817

## Contributing

Submit pull requests against this repository to add or improve annotated SDRF files.
