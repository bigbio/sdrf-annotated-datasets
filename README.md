# sdrf-annotated-datasets

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![llms.txt](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/llms-txt.json)](llms.txt)
![Datasets](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/datasets.json)
![Sandbox](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/sandbox.json)
[![Validate SDRF datasets](https://github.com/bigbio/sdrf-annotated-datasets/actions/workflows/validate-sdrf.yml/badge.svg?branch=main)](https://github.com/bigbio/sdrf-annotated-datasets/actions/workflows/validate-sdrf.yml)

Community **SDRF** annotations for public proteomics datasets (ProteomeXchange and related accessions).
The SDRF specification lives in [`bigbio/proteomics-sample-metadata`](https://github.com/bigbio/proteomics-sample-metadata).

**License:** [Apache 2.0](LICENSE) · **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md) · **Agent context:** [llms.txt](llms.txt), [AGENTS.md](AGENTS.md)

## Key links

| Resource | URL |
|---|---|
| Specification | https://github.com/bigbio/proteomics-sample-metadata/blob/master/sdrf-proteomics/README.adoc |
| Public site | https://sdrf.quantms.org/ |
| Templates | https://github.com/bigbio/sdrf-templates |
| Validator CLI (`parse_sdrf`) | https://github.com/bigbio/sdrf-pipelines |
| Agentic toolkit | https://github.com/bigbio/sdrf-skills |

## Dataset layout

Files follow the pattern `datasets/{ACCESSION}/{ACCESSION}.sdrf.tsv`:

```
datasets/PXD000070/PXD000070.sdrf.tsv
datasets/MSV000078494/MSV000078494.sdrf.tsv
```

Additional `.sdrf.tsv` files may appear in the same folder when a project requires split designs.

## Sandbox

### What `sandbox/` is for

`sandbox/` is a **staging area** for SDRFs that are not yet ready to live
alongside the production annotations in `datasets/`. Put an accession here when
any of the following is true:

- The file **fails** `parse_sdrf validate-sdrf` (structural errors, ontology
  mismatches, template-level violations).
- The file is an **empty placeholder** or stub reserving the accession while
  annotation is in progress.
- The annotation is a **draft** that still needs review against the PX landing
  page, the publication, or raw files.
- The file was migrated from an external source and has **known issues** a
  reviewer plans to repair.

If the SDRF already passes validation, **do not** put it in `sandbox/` — it
belongs in `datasets/`.

### Why this split exists

CI validation (`parse_sdrf validate-sdrf`, GitHub Actions) runs **only** on
files under `datasets/**`. Files under `sandbox/**` are deliberately **exempt**
so contributors can iterate on broken SDRFs and open PRs without blocking
merges on known-failing rows. The tradeoff: `sandbox/` files are not guaranteed
valid at any point in time, while anything under `datasets/` must pass CI.

Layout in both trees is identical:
`{datasets,sandbox}/{ACCESSION}/{ACCESSION}.sdrf.tsv` (additional
`*.sdrf.tsv` files in the same accession folder are allowed when the public
record requires split designs). See also [`sandbox/README.md`](sandbox/README.md).

### How to promote from `sandbox/` → `datasets/`

When a sandbox SDRF is finally clean, move it to `datasets/` in a **dedicated
pull request**:

1. **Validate locally** against the current validator:
   ```bash
   pip install git+https://github.com/bigbio/sdrf-pipelines@main
   parse_sdrf validate-sdrf --sdrf_file sandbox/{ACC}/{ACC}.sdrf.tsv
   ```
   Fix every error before continuing; warnings can be addressed in review.
2. **Move the folder** with `git mv` so file history is preserved:
   ```bash
   git mv sandbox/{ACC} datasets/{ACC}
   ```
3. **Commit** with a message that names the accession and states the promotion,
   e.g. `Promote {ACC} from sandbox/ to datasets/.`
4. **Open a PR** whose diff shows only the rename (and any small fixes made in
   the same pass). Keep unrelated edits out so review stays tight.
5. CI will now validate the file on the canonical path. Merge once the
   `validate` job is green.

If a file already under `datasets/` regresses later, move it back to `sandbox/`
the same way and open an issue or PR describing the regression.

## Migration context

- Source repository: `bigbio/proteomics-sample-metadata`
- Discussion: https://github.com/bigbio/proteomics-sample-metadata/issues/817

## Contributing

Open a pull request to add or improve annotated SDRF files.
See [CONTRIBUTING.md](CONTRIBUTING.md) for layout rules and review etiquette.

### Agent-assisted annotation

Use **[sdrf-skills](https://github.com/bigbio/sdrf-skills)** as the primary toolkit.
Key rules:

- **Anchor every row** in public evidence (PX page, submitted metadata, publication). Don't invent sample names or file names.
- **Keep PRs small** — one accession or a closely related batch.
- **Run validation locally** (`parse_sdrf validate-sdrf`) before opening a PR.
- **Declare assistance** in the PR description so reviewers can calibrate review depth.

For agent-specific instructions see [AGENTS.md](AGENTS.md).

### CI validation

GitHub Actions runs `parse_sdrf validate-sdrf` on every PR and push touching `datasets/**`.
The validator is installed from [`bigbio/sdrf-pipelines`](https://github.com/bigbio/sdrf-pipelines) `main` branch.
Re-run all checks manually via `workflow_dispatch` in the Actions tab.
