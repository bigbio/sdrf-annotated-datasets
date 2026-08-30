# Cardiac sweep, tiers 2-4 — criteria

Tier 1 (heart / myocardium tissue) is covered by `docs/heart-tier1/`. This document covers
the three harder tiers of the same 979-candidate cardiac sweep of PRIDE.

| Tier | Candidates | Annotated | What defines it |
|---|---:|---:|---|
| **T2** cardiac cell / valve | 48 | 22 | Sample is cardiac but is a **cell type or a valve**, not myocardial tissue |
| **T3** multi-tissue | 203 | 66 | Heart appears **alongside other organs** (liver, kidney, brain, …) |
| **T4** cardiac by title only | 234 | 106 | Title/keywords/disease are cardiac but PRIDE records **no cardiac organism part** |

The include/exclude screens are identical to Tier 1 (see `docs/heart-tier1/CRITERIA.md`):
one organism, one MS-ontology instrument *model*, a recoverable acquisition mode, a protease
named somewhere in the record, and at least one deposited file that is a single acquisition.
Labelled quantification, out-of-template experiment types, multi-instrument and multi-organism
records, and archive-bundle-only deposits are excluded.

Two vendor family nodes are rejected alongside `orbitrap` (MS:1000484) for the same reason —
they name a manufacturer, not a model: `SCIEX instrument model` (MS:1000121) and
`Bruker Daltonics instrument model` (MS:1000122).

## How organism part and cell type are decided

Every distinct organism-part label across these tiers (228 of them) was resolved against OLS4.
**OLS returns a term's real ontology prefix regardless of which ontology is requested**, so the
prefix of the resolved accession — not any pattern matched from the label text — decides which
column the label belongs in:

- `UBERON:` → `characteristics[organism part]`
- `CL:` → `characteristics[cell type]`, plus an organism part **only** where the anatomical
  source is unambiguous: a cardiac cell type gives `heart`, a valve cell type gives
  `cardiac valve`. Any other cell type gets no organism part.
- `GO:` or unresolved → neither. 39 labels resolve nowhere; almost all are cell lines
  (`HeLa cell`, `HEK-293 cell`, `H9c2 cell`, `HL-1 cell`), which belong in
  `characteristics[cell line]` and are left out rather than forced into organism part.

Several parts on one deposit collapse to a single term **only** when every one of them is
heart-derived — the Tier-2 case (`Heart` + `Cardiac muscle cell`). Generic containers
(`Cell culture`, `Stem cell`, `Primary cell`) do not block that collapse. A mixed-organ
record — the whole of Tier 3 — keeps `not available`, because nothing in the archive record
says which run came off which organ.

**This is why 138 of the 194 files carry `characteristics[organism part] = not available`.**
That is the honest value for a multi-organ deposit annotated at run level. Organism,
instrument, acquisition mode, cleavage agent, modifications and the exact run set are still
asserted, and none of them is guessed.

## What Tier 4 does and does not claim

Tier 4 was selected because the **title, keywords or disease terms** are cardiac, not because
PRIDE records a cardiac sample. Many are plasma or serum biomarker studies where the cardiac
link is the clinical question rather than the tissue. **These files do not assert that the
sample is heart tissue** — they carry whatever organism part PRIDE actually records
(`blood plasma`, `blood serum`, …) or a sentinel. Confirming the cardiac context of any
individual Tier-4 deposit needs the paper, which is outside what this batch claims.

## Validation

All 194 files pass the repository's own review gate (`.github/scripts/sdrf_review.py`) clean —
zero defects. Independently verified after generation: every `comment[data file]` is a file
PRIDE lists under the `RAW` category for that accession; no deposited run of the selected
acquisition format is left unannotated; `source name` is unique and matches
`<ACCESSION>-Sample-<n>`; the `(source name, fraction identifier, technical replicate, label)`
coordinate is unique; no empty cells.

`metascreen-t2.tsv`, `metascreen-t3.tsv` and `metascreen-t4.tsv` list **all 485 candidates**
with keep/skip label, reason, the resolved organism part and cell type, and the metadata each
was judged on.
