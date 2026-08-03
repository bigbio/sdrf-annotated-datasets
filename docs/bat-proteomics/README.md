# Bat proteomics SDRF annotation pack

Branch: `annotate/bat-proteomics`  
Worktree: isolated from other WIP on `ci/sdrf-review-gate`.

## Screening

| File | Purpose |
|------|---------|
| `metascreen.tsv` | Inclusion screen of PRIDE bat / Chiroptera candidates |
| `taxonomy-map.tsv` | Verified NCBITaxon accessions for bat species used in SDRFs |

**Discovery note:** Keyword `bat` alone is unusable in PRIDE (~3000 hits). Candidates were found via scientific names (`Desmodus`, `Rousettus`, `Pteropus`, `Myotis`, `Artibeus`, `Eptesicus`, `Carollia`, `Hipposideros`, `Rhinolophus`) and the keyword `bats`, then filtered by organism/sample evidence.

## Include summary (17)

Vampire bat serum, Egyptian fruit bat serum, black flying fox cells/tissue/MHC, little brown bat plasma/MHC, Rickett's bat liver, Jamaican fruit bat organoids, big brown bat cells, Seba's short-tailed bat forelimb RIME, horseshoe bat brain/cells, great roundleaf bat heart.

## Exclude summary (11)

Keyword false positives (ocean metaproteomics, human/mouse-only studies), shrew/mole troponin study without bat samples, and multi-species tick blood-meal library (`PXD000170`).
