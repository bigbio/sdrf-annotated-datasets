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

### Validation

GitHub Actions runs `parse_sdrf validate-sdrf` on every pull request and push that
touches `datasets/**`. The workflow installs the latest
[`bigbio/sdrf-pipelines`](https://github.com/bigbio/sdrf-pipelines) from GitHub on
each run so validators stay current. You can re-run checks manually from the
Actions tab (`workflow_dispatch`); that job validates all tracked
`datasets/**/*.sdrf.tsv` files.
