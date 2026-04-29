# sdrf-annotated-datasets

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![llms.txt](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/llms-txt.json)](llms.txt)
![Datasets](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/datasets.json)
![Sandbox](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/sandbox.json)
[![Validate SDRF datasets](https://github.com/bigbio/sdrf-annotated-datasets/actions/workflows/validate-sdrf.yml/badge.svg?branch=main)](https://github.com/bigbio/sdrf-annotated-datasets/actions/workflows/validate-sdrf.yml)

Community **SDRF** annotations for public proteomics datasets (ProteomeXchange and
related accessions). This repository exists so **annotation work can move quickly**
while the **SDRF specification** stays stable in
[`bigbio/proteomics-sample-metadata`](https://github.com/bigbio/proteomics-sample-metadata).

**License:** [Apache License 2.0](LICENSE) · **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md) · **LLM / agent context:** [llms.txt](llms.txt), [AGENTS.md](AGENTS.md)

## SDRF ecosystem (links)

- **This repository (annotated public datasets):** https://github.com/bigbio/sdrf-annotated-datasets
- **SDRF-Proteomics specification (source, AsciiDoc):** https://github.com/bigbio/proteomics-sample-metadata  
  - Main specification: https://github.com/bigbio/proteomics-sample-metadata/blob/master/sdrf-proteomics/README.adoc  
  - Public site (overview, tools, explorer): https://sdrf.quantms.org/
- **Templates (how to choose layers and columns):** https://github.com/bigbio/proteomics-sample-metadata/blob/master/sdrf-proteomics/TEMPLATES.adoc  
  - Machine-readable template YAML (**sdrf-templates**): https://github.com/bigbio/sdrf-templates
- **Validator / CLI (`parse_sdrf`, used in CI and locally):** https://github.com/bigbio/sdrf-pipelines
- **Agentic annotator toolkit (skills, rules, workflows):** https://github.com/bigbio/sdrf-skills

## Mission

The aim of this repository is to **advance annotations in a community-driven way**,
bringing together:

- **Community annotators** (individuals, groups, and computational workflows)
- The **SDRF core team** and broader **HUPO-PSI** metadata community
- **ProteomeXchange** members and resource providers invested in **re-annotation**
  of public proteomics data

Together, these efforts improve **sample-to-data** reporting so deposited experiments
are easier to interpret, integrate across studies, and reprocess with clear
experimental design and technology metadata.

## Dataset layout

Each dataset is stored under:

`datasets/{ACCESSION}/{ACCESSION}.sdrf.tsv`

Examples:

- `datasets/PXD000070/PXD000070.sdrf.tsv`
- `datasets/MSV000078494/MSV000078494.sdrf.tsv`

Some projects include additional `.sdrf.tsv` files in the same accession folder
when the public record genuinely requires split designs (see existing folders).

## Sandbox (under preparation)

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

Open pull requests against this repository to add or improve annotated SDRF files.
See [CONTRIBUTING.md](CONTRIBUTING.md) for branch expectations, layout rules, and
review etiquette.

### Agentic and LLM-assisted annotation — best practices

Automated and **agent-assisted** curation is welcome when the result is **accurate,
traceable, and reviewable**. Use **[sdrf-skills](https://github.com/bigbio/sdrf-skills)**
as the **primary toolkit** for agentic SDRF work (Cursor rules, skills, and
workflows for setup, annotation, validation, and fixes). Combine it with
`parse_sdrf validate-sdrf` so outputs stay aligned with current templates and
validators.

In practice:

- **Anchor every row in public evidence** (PX landing page, submitted metadata,
  publication supplementary material). Do not invent sample names, factors, or
  raw file names.
- **Prefer small pull requests** (one accession or a tightly related batch) so
  reviewers can verify mappings quickly.
- **Run `parse_sdrf validate-sdrf` locally** before opening a PR; fix structural and
  template issues early.
- **Declare assistance** in the PR description (for example, “draft produced with
  tool X, manually verified against the PX record”) so maintainers can calibrate
  review depth.
- **Use ontology terms and templates** consistent with the dataset type; when in
  doubt, document open questions for humans instead of guessing.

For concise instructions aimed at coding agents, see [AGENTS.md](AGENTS.md).

### Validation (CI)

GitHub Actions runs `parse_sdrf validate-sdrf` on every pull request and push that
touches `datasets/**` or `sandbox/**`. Only files under **`datasets/`** are
validated; **`sandbox/` is excluded** so work-in-progress accessions do not fail
the build (see [Sandbox](#sandbox-under-preparation)). The workflow installs
[`bigbio/sdrf-pipelines`](https://github.com/bigbio/sdrf-pipelines) **from GitHub
`main` via pip** (`git+https://…@main`), not from PyPI releases, so each run uses
the latest validator code on the default branch. You can re-run checks manually
from the Actions tab (`workflow_dispatch`); that job validates all tracked
`datasets/**/*.sdrf.tsv` files.
