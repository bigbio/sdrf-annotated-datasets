# PXD043908

Sandbox: the heavy-peptide row has filler values for required columns, and the AML patient-to-file mapping is unresolved.

`datasets/PXD043908/PXD043908.sdrf.tsv` already exists. This pull request does not replace it.

## Why this is in sandbox
- The immunopeptidomics template requires MHC and enrichment columns. The heavy-peptide standard was not immunopurified, so those cells are fillers.
- Patients 1 and 3 cannot be assigned to `H222724PBMC.raw` and `H224278.raw`.

## Return criteria
- A patient-to-file map, and a template choice that does not force immunopeptidomics values onto the heavy-peptide standard.
- Re-review before any move into `datasets/`.
