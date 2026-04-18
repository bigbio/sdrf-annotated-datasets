# Contributing to sdrf-annotated-datasets

Thank you for helping improve public proteomics metadata. This repository holds
**SDRF annotations** for ProteomeXchange (and related) datasets. The **SDRF
specification** itself lives in
[`bigbio/proteomics-sample-metadata`](https://github.com/bigbio/proteomics-sample-metadata).

## Who this is for

Contributions are welcome from:

- Community annotators and tool authors
- Members of the **SDRF / HUPO-PSI** ecosystem
- **ProteomeXchange** partners and curators interested in **re-annotation** of
  public experiments

The goal is to advance **consistent, validated** sample-to-data metadata so
datasets can be reused, integrated, and reprocessed with less ambiguity.

## Repository layout

Add or update files under:

```text
datasets/{ACCESSION}/{ACCESSION}.sdrf.tsv
```

Use the public accession as the folder name (`PXD…`, `MSV…`, `PMID…`, etc.). If a
project needs more than one SDRF file, keep them under the same accession folder
and use descriptive suffixes (see existing examples).

## Pull request workflow

1. **Fork** this repository and create a branch from `dev` (or `main` if that is
   the integration branch you are targeting).
2. Add or edit SDRF files only under `datasets/`.
3. **Validate locally** before opening a PR (same command CI uses):

   ```bash
   pip install --upgrade "git+https://github.com/bigbio/sdrf-pipelines.git@main"
   parse_sdrf validate-sdrf --sdrf_file "datasets/YOUR_ACCESSION/YOUR_FILE.sdrf.tsv" --use_ols_cache_only
   ```

4. Open a **pull request** with a short summary of the dataset, what changed, and
   how you validated it (manual review, tool output, etc.).
5. CI will re-run validation on changed `.sdrf.tsv` files using **sdrf-pipelines
   from GitHub `main`**.

## Human and agentic contributions

Manual curation and automated or **agent-assisted** annotation are both welcome.
If a contribution was produced or assisted by an LLM or other agent:

- Prefer **small, reviewable** pull requests (one accession or a coherent batch).
- **Cite sources** in the PR description (repository record, publication, PX
  landing page) so reviewers can verify organism, condition, and file mapping.
- **Do not invent** sample identifiers or file names: align rows with the actual
  record in the public archive.
- Run **`parse_sdrf validate-sdrf`** locally and fix errors before opening the PR.
- If ontology or term choices are uncertain, say so explicitly and prefer terms
  that match the **published** experiment description.

See [README.md](README.md) for a concise “agentic annotation” checklist.

## Code of conduct

Be respectful and constructive. For substantive specification debates, use the
[proteomics-sample-metadata issue tracker](https://github.com/bigbio/proteomics-sample-metadata/issues).

## License

By contributing, you agree your contributions are licensed under the same terms
as this repository ([LICENSE](LICENSE)).
