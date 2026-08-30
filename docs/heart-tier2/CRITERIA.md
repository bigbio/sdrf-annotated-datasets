# Cardiac cells, cardiomyocyte models and heart valves — criteria

## Why this replaces #287

An earlier attempt at this tier (#287) was withdrawn. An independent adversarial review,
working from the linked publications, found that **only 2 of its 22 files measured heart
tissue as annotated**. The rest wrote `characteristics[organism part] = heart` over
hiPSC-derived cardiomyocytes, immortalised lines and purified recombinant protein.

The inference itself was the defect. An hiPSC-derived cardiomyocyte, an AC16 or an H9c2 has
an anatomical *identity* but no anatomical *source*; `UBERON:0000948` asserts the sample is
part of a heart, and it was not. That is not a per-file fix, so the PR was closed rather than
patched.

## What this batch does instead

**Classify the material first, then write only the columns that class supports.**

| Material | `organism part` | `cell type` | cell line columns |
|---|---|---|---|
| **tissue** — explanted leaflet, LV free wall, myocardium, or a subcellular fraction prepared from hearts | the UBERON term | — | — |
| **primary** — freshly dissociated NRVM/NRCM or primary cardiac cells | `heart` | `cardiac muscle cell` | — |
| **iPSC/hESC-derived** — cardiomyocytes, organoids, engineered heart tissue | *sentinel* | `cardiac muscle cell` | — |
| **cell line** — AC16, H9c2, HL-1, … | *sentinel* | — | line + Cellosaurus accession + name, and the `cell-lines` template |
| **purified** — recombinant or purified protein | skipped: there are no cells | | |
| **mixed** — two materials with no per-run key | skipped | | |

Freshly dissociated primary cardiomyocytes keep `heart`: they were physically part of one.
That distinction is the whole point of the tier.

## Cellosaurus accessions are pinned, not looked up

Every accession below was confirmed by fetching the accession itself, because name lookup is
actively dangerous here:

- an exact-identifier search for **`AC16`** returns **`CVCL_LJ81` "AC16 [Mouse mesothelioma]"**,
  not the human cardiomyocyte line;
- the curated cell-line database in `sdrf-skills` fuzzy-matches **`HL-1`** to **`HLC-1`**, a
  human *gastric* line, at 0.86 confidence.

| Name | Accession | Cellosaurus identifier | Organism |
|---|---|---|---|
| AC16 | CVCL_4U18 | AC16 [Human hybrid cardiomyocyte] | *Homo sapiens* |
| H9c2 | CVCL_0286 | H9c2(2-1) | *Rattus norvegicus* |
| HL-1 | CVCL_0303 | HL-1 | *Mus musculus* |
| HeLa | CVCL_0030 | HeLa | *Homo sapiens* |
| HCT 116 | CVCL_0291 | HCT 116 | *Homo sapiens* |

A deposit whose declared organism disagrees with the named line's species is skipped rather
than reconciled.

## Two materials in one deposit

A record naming several cultured lines, or a line alongside primary cells in its
*sample-processing protocol*, describes two materials with no key saying which run is which.
Those are skipped. **PXD014791** is the clearest case: 64 of its 381 runs are named `*_Hela*`,
matching the protocol's "64 HeLa control lysates", and #287 annotated all 381 as heart.

The test deliberately uses the sample-processing protocol, not the description: a description
that merely *discusses* primary cardiomyocytes ("since the use of isolated primary
cardiomyocytes is limited, immortalized lines may represent…") is background, not material.

## Everything else

The generator is the reconciling one from the cardiac rebuild: PRIDE's structured fields are
one witness, and the title, protocol prose, run names and open-access publication all get a
vote, with disagreement resolving to a sentinel. Publication evidence was resolved through
Europe PMC — **full text for 11, abstract for 11, nothing for 9** of the 31 candidates.

A disease is not written for engineered or cultured material whose record describes an
isogenic, CRISPR-corrected, wild-type or vehicle arm — that arm is the control, and asserting
the case diagnosis on it is false for half the file.

## Result

**15 files, 549 rows, 15/15 clean** through `.github/scripts/sdrf_review.py`.

Of 48 tier-2 candidates: 17 were screened out before generation (labelled quantification,
out-of-template experiment type, several organisms or instruments, already annotated), and of
the 31 remaining, 16 could not be annotated faithfully — 5 name no protease, 3 deposit no
usable run format, 3 have a material class the record does not establish, 3 name two
materials, 2 are purified protein.

Verified after generation: every `comment[data file]` is a PRIDE `RAW`-category file for that
accession; no deposited run of the selected format left unannotated; `source name` unique and
matching `<ACCESSION>-Sample-<n>`; coordinates unique; no empty cells; none already under
`datasets/`.
