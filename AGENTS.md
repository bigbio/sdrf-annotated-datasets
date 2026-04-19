# Agent instructions (Cursor, Copilot, and similar)

Use this file together with `llms.txt` and `CONTRIBUTING.md`.

## Primary toolkit (agentic SDRF)

Use **[sdrf-skills](https://github.com/bigbio/sdrf-skills)** as the **default**
setup for agent-assisted annotation and validation (skills + assistant rules +
workflows). Follow its setup docs, then apply changes in this repository under
`datasets/` and confirm with `parse_sdrf validate-sdrf` as below.

## Scope

- **In scope:** `datasets/**/*.sdrf.tsv`, `sandbox/**/*.sdrf.tsv` (WIP only), and
  doc/CI updates **only when asked**.
- **Canonical vs sandbox:** validated accessions belong in `datasets/`. If
  `parse_sdrf validate-sdrf` fails or the file is incomplete, use `sandbox/` (see
  `sandbox/README.md`) until it passes locally.
- **Out of scope:** Changing the SDRF specification or templates here; that belongs
  in [`bigbio/proteomics-sample-metadata`](https://github.com/bigbio/proteomics-sample-metadata).

## Required checks before suggesting a PR

1. Layout: `datasets/{ACCESSION}/{ACCESSION}.sdrf.tsv` (or same folder, extra
   `.sdrf.tsv` only when justified by the project).
2. Run validation:

   ```bash
   pip install --upgrade "git+https://github.com/bigbio/sdrf-pipelines.git@main"
   parse_sdrf validate-sdrf --sdrf_file "datasets/<ACCESSION>/<file>.sdrf.tsv" --use_ols_cache_only
   ```

3. PR description must include **public evidence** (PX / PMID / repository URL)
   for sample and file mappings.

## Agentic annotation — do / do not

- **Do** keep edits minimal, accession-scoped, and aligned with archive metadata.
- **Do** prefer ontology terms and template columns consistent with the chosen
  SDRF template (`ms-proteomics` unless the dataset clearly needs another layer).
- **Do not** fabricate raw file names, replicate IDs, or sample relationships.
- **Do not** bulk-reformat unrelated accessions.

If uncertain, leave a comment in the PR for human reviewers instead of guessing.
