# Sandbox (work in progress)

This folder holds **ProteomeXchange (or related) accessions that are not yet ready**
for the canonical `datasets/` tree: empty placeholders, drafts, or files that
**do not pass** `parse_sdrf validate-sdrf` with the current
[`sdrf-pipelines`](https://github.com/bigbio/sdrf-pipelines) `main` branch.

## Rules

- **`datasets/`** — Only SDRF files that pass CI validation belong here.
- **`sandbox/`** — Anything under active curation, repair, or migration. Fix the
  SDRF here, validate locally, then **move** the accession folder into
  `datasets/` in a dedicated pull request.

## Layout

Use the same folder pattern as `datasets/`:

`sandbox/{ACCESSION}/{ACCESSION}.sdrf.tsv` (and additional `.sdrf.tsv` files in that
folder if needed).

## CI

GitHub Actions **does not** require `sandbox/**/*.sdrf.tsv` to pass validation. It
only enforces checks on paths under `datasets/`. Pushes that touch only `sandbox/`
still trigger the workflow so the job can validate `datasets/` when both areas
change in one PR.
