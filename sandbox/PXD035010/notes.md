# PXD035010

BLOCKED: two deposited RAW files look like copies of other runs, so their sample identity is unresolved.

`datasets/PXD035010/PXD035010.sdrf.tsv` already exists. This pull request does not replace it.

## Why this is in sandbox
- `191220_Hanson_P2.raw` and `191220_Hanson_P3.raw` carry embedded paths of the S2/S3 runs and are same-size copies.
- Treating them as technical replicates of P2/P3 would present S-labelled data as P samples.
- P/S meaning is still undecoded.

## Return criteria
- Confirmation of which files are the real P2 and P3 acquisitions.
- Re-review before any change to the file in `datasets/`.
