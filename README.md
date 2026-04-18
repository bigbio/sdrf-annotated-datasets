# sdrf-annotated-datasets

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

Work-in-progress or **not-yet-valid** annotations live under **`sandbox/`** (see
[`sandbox/README.md`](sandbox/README.md)). Typical reasons include empty
placeholders, drafts, or files that **fail** `parse_sdrf validate-sdrf` until they
are repaired. **CI only enforces validation on `datasets/`**; `sandbox/` is
exempt so contributors can iterate without blocking merges on known-broken rows.
When an accession is ready, **move** its folder from `sandbox/` into `datasets/`
and open a pull request so checks run on the canonical path.

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
