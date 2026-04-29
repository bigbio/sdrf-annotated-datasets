# Sandbox (work in progress)

This folder holds **ProteomeXchange (or related) accessions that are not yet ready**
for the canonical `datasets/` tree: empty placeholders, drafts, or files that
**do not pass** `parse_sdrf validate-sdrf` with the current
[`sdrf-pipelines`](https://github.com/bigbio/sdrf-pipelines) `main` branch.

See the [root README](../README.md#sandbox-under-preparation) for the full
explanation of what `sandbox/` is for and why it exists.

## Rules

- **`datasets/`** — Only SDRF files that pass CI validation belong here.
- **`sandbox/`** — Anything under active curation, repair, or migration. Fix the
  SDRF here, validate locally, then **promote** the accession folder into
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

## Promoting a sandbox accession to `datasets/`

When a sandbox SDRF finally passes validation, move it with `git mv` so history
follows the file:

```bash
# 1. Validate locally
pip install git+https://github.com/bigbio/sdrf-pipelines@main
parse_sdrf validate-sdrf --sdrf_file sandbox/{ACC}/{ACC}.sdrf.tsv

# 2. Move and commit
git mv sandbox/{ACC} datasets/{ACC}
git commit -m "Promote {ACC} from sandbox/ to datasets/."

# 3. Push and open a PR
git push -u origin promote/{ACC}
```

Keep the diff scoped to the rename plus any small fixes made in the same pass.
CI will then validate the file on the canonical path. Merge once the `validate`
job is green.
