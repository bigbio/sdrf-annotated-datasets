# sdrf-annotated-datasets

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![llms.txt](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/llms-txt.json)](llms.txt)
![Datasets](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/datasets.json)
![Sandbox](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/.github/badges/sandbox.json)
[![Validate SDRF datasets](https://github.com/bigbio/sdrf-annotated-datasets/actions/workflows/validate-sdrf.yml/badge.svg?branch=main)](https://github.com/bigbio/sdrf-annotated-datasets/actions/workflows/validate-sdrf.yml)

Community **SDRF** annotations for public proteomics datasets (ProteomeXchange and related accessions).
The SDRF specification lives in [`bigbio/proteomics-sample-metadata`](https://github.com/bigbio/proteomics-sample-metadata).

**License:** [Apache 2.0](LICENSE) · **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md) · **Agent context:** [llms.txt](llms.txt), [AGENTS.md](AGENTS.md)

<!-- STATS:START -->
## Resource at a glance

_Auto-generated from curated `datasets/` on 2026-11-26T10:52:20Z. Sandbox drafts are excluded._

| Metric | Count |
| --- | ---: |
| Accessions | 19,149 |
| SDRF files | 20,377 |
| Accessions with a declared template | 19,124 |
| Samples (unique `source name` per file) | 1,053,714 |
| Runs (unique `comment[data file]` per file) | 1,350,153 |
| Assay rows | 1,831,372 |
| Merged PRs that changed curated datasets | 3,411 |
| ... adding new datasets | 3,127 (92%) |
| ... modifying existing datasets | 284 (8%) |
| Human contributors | 43 |
| AI agents (named fingerprints) | 10 |
| Foundation models identified | 23 |
| AI-assisted accessions | 19,149 |
| Unidentified agent | 1,313 |
| Multi-agent accessions | 6,005 |
| Distinct instruments | 241 |
| Median runs per accession | 14 |
| Accessions with modification parameters | 12,640 |
| ProteomeXchange coverage | 19,078 / 58,669 (32.5%) |
| PRIDE coverage | 17,520 / 42,963 (40.8%) |
| MassIVE coverage | 212 / 3,794 (5.6%) |
| iProX coverage | 1,671 / 8,561 (19.5%) |

**Highlights:** most common organism is **Homo sapiens**; **283,588** DIA assay rows; **372,248** TMT and **1,171,665** LFQ assay rows; **86** single-cell, **3,052** cell-line, and **653** metaproteomics accessions; sample-field completeness (applicable samples): disease 37%, age 10%; all **19,149** accessions are AI-assisted (**43** human contributors, **10** named AI agents); identified fingerprints are mostly **Cursor**; **1,313** accessions have no vendor fingerprint (typical of Claude Code committed as the reviewer); **552** accessions have Codex evidence (`codex/` PR branches); **6,005** accessions were touched by more than one agent (most common handoff **Cursor → Codex**); **3,411** merged PRs have changed curated datasets — **3,127** (92%) added brand-new datasets and **284** (8%) refined existing annotations; most common instrument is **Q Exactive**; most common modification is **Carbamidomethyl**; **32.5%** of public ProteomeXchange datasets have a curated SDRF here; **40.8%** of PRIDE projects are annotated.

![How much of public proteomics is annotated](docs/stats/plots/coverage.png)

![Organisms in curated annotations](docs/stats/plots/organisms.png)

![Disease annotations](docs/stats/plots/diseases.png)

![Quantification and acquisition methods](docs/stats/plots/methods.png)

![Instruments, runs, and modifications](docs/stats/plots/analytical.png)

![Annotation completeness](docs/stats/plots/completeness.png)

![Templates and specialized collections](docs/stats/plots/templates.png)

![AI-assisted annotation](docs/stats/plots/contributions.png)

![Foundation models used in annotation](docs/stats/plots/models.png)

<!-- STATS:END -->

## Gold standard datasets

Looking for a known-good SDRF to point a pipeline at? A short curated list is kept for
exactly that. Each entry passes both CI gates, maps every row to a real deposited run, and
carries enough sample metadata to exercise what usually breaks first — TMT channel maps,
cell-line identity, phospho-enrichment metadata and factor-value driven designs. Between
them they span five organisms, DDA and DIA, label-free, TMT and SILAC, and 112 to 5,798
rows. The standout is `PXD030304`: 949 cell lines with per-line sex, age, ancestry and
Cellosaurus accession across 5,798 individually mapped runs.

See **[docs/gold-standard-datasets.md](docs/gold-standard-datasets.md)** for the list,
what each one is good for testing, and how to fetch and validate them.

## Known issues

Some deposits have problems that annotation alone cannot fix. Examples are a 2 KB
metadata stub named `.raw`, or a PRIDE instrument field that contradicts the raw file.
These SDRFs are kept, not deleted, and are listed in
**[docs/known-issues.md](docs/known-issues.md)** by severity (critical, major, moderate,
minor), with the evidence for each, so pipelines can skip them and curators can follow up.

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

Work-in-progress annotations live under [`sandbox/`](sandbox/README.md).
Move a folder to `datasets/` and open a PR once it passes `parse_sdrf validate-sdrf`.
CI only validates `datasets/`; `sandbox/` is exempt so drafts don't block merges.

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

## How to cite

- Dai C, Füllgrabe A, Pfeuffer J, Solovyeva EM, Deng J, Moreno P, Kamatchinathan S, Kundu DJ, George N, Fexova S, Grüning B, Föll MC, Griss J, Vaudel M, Audain E, Locard-Paulet M, Turewicz M, Eisenacher M, Uszkoreit J, Van Den Bossche T, Schwämmle V, Webel H, Schulze S, Bouyssié D, Jayaram S, Duggineni VK, Samaras P, Wilhelm M, Choi M, Wang M, Kohlbacher O, Brazma A, Papatheodorou I, Bandeira N, Deutsch EW, Vizcaíno JA, Bai M, Sachsenberg T, Levitsky LI, Perez-Riverol Y. A proteomics sample metadata representation for multiomics integration and big data analysis. Nat Commun. 2021 Oct 6;12(1):5854. doi: 10.1038/s41467-021-26111-3. PMID: 34615866; PMCID: PMC8494749. [Manuscript](https://www.nature.com/articles/s41467-021-26111-3)
- Perez-Riverol, Yasset, European Bioinformatics Community for Mass Spectrometry. "Towards a sample metadata standard in public proteomics repositories." Journal of Proteome Research (2020) [Manuscript](https://pubs.acs.org/doi/abs/10.1021/acs.jproteome.0c00376).
