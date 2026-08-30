# Zebrafish and yeast recovery — deposits an earlier screen wrongly excluded

## What went wrong in #274

PR #274 annotated 360 zebrafish and yeast deposits. Its pool screen rejected labelled
quantification with this pattern:

```python
QLAB = re.compile(r"silac|tmt|itraq|dimethyl|icat|isobaric|tandem mass tag", re.I)
```

`icat` is unanchored, and **"quantifi(cat)ion" contains "icat"**. Every deposit whose only
registered quantification method was *label-free*, *relative* or *absolute quantification*
was therefore dropped as "labelled quantification" — the exact opposite of what it is.

99 zebrafish and yeast deposits were excluded by that single missing `\b`. The triggering
strings were `MS1 intensity based label-free quantification method` (61),
`Relative quantification` (19), `label-free quantification` (9) and `Absolute quantification`.

The same class of bug — a pattern matching a word playing a different role — has now been
found three times in this tooling, so the screens here are word-anchored throughout.

## What this PR adds

Of those 99, **21 are no longer eligible** (already annotated since, out-of-template
experiment type, several instruments, or labelling genuinely stated in the protocol), leaving
78 candidates. **52 could be annotated faithfully.**

| Organism group | Datasets |
|---|---:|
| *Saccharomyces cerevisiae* | 33 |
| *Danio rerio* | 5 |
| *Schizosaccharomyces pombe* | 5 |
| *Candida albicans* | 3 |
| *Cryptococcus neoformans* | 3 |
| *Nakaseomyces glabratus* | 2 |
| *Clavispora lusitaniae* | 1 |

The 26 that could not be annotated: 10 name no protease anywhere in the record, 6 are
genuinely labelled, 5 do not state a recoverable acquisition mode, 4 deposit no usable run
format, and 1 declares an instrument that cannot have written its files.

## How these differ from #274

Same run-level skeleton — one row per deposited run, `source name` = `<ACCESSION>-Sample-<n>`,
no sample grouping invented — but generated with the **reconciling** generator built after an
adversarial review of a later batch found that reading the archive's structured fields as
ground truth produces well-formed false claims. Every value here is checked against the
deposit's title, protocol prose, run names and open-access publication, and any disagreement
resolves to a sentinel.

Publication evidence was resolved through Europe PMC: **full text for 37, abstract for 12, and
nothing for 29** of the 78 candidates.

Concretely, relative to #274's generator:

- **Labelling** is detected from PRIDE's `quantificationMethods`, the protocol *and* the
  paper. It caught 6 genuinely labelled deposits here, including spellings #274's pattern
  missed.
- **Instrument** is taken from the publication first, then the protocol, then PRIDE — and
  rejected outright when the vendor could not have written the deposited file format. That
  caught 1 deposit declaring a Bruker timsTOF over Thermo `.raw` files.
- **Acquisition mode** is per run, from the run's own `DDA`/`IDA`/`SWATH`/`PRM` token, so the
  DDA library runs inside a DIA deposit are not mislabelled.
- **Cleavage agent** lists every protease the record names *as a digest reagent*, scoped to
  the sentence, so a Lys-C→trypsin double digest gets two columns.
- **Organism part and cell type** are decided by the ontology prefix OLS returns for the
  PRIDE label — UBERON to organism part, CL to cell type, anything else to a sentinel.
  48 of 52 carry `not available`, which is correct: for a yeast culture there is no
  anatomical part, and PRIDE registers only container terms like `Cell culture`.

Two false positives in the new checks were found and fixed while building this batch, both
caught by applying them to yeast rather than to the mammalian batch they were written for:
the organism check treated "declared species absent from the text" as evidence even when the
species was outside its vocabulary, and `\bporcine\b` matched **"modified porcine trypsin"** —
a reagent, not the study organism.

## Validation

**52/52 clean** through `.github/scripts/sdrf_review.py` on `sdrf-pipelines` 0.1.6.

Independently verified after generation: every `comment[data file]` is a file PRIDE lists
under the `RAW` category for that accession; no deposited run of the selected acquisition
format is left unannotated; `source name` is unique and matches `<ACCESSION>-Sample-<n>`; the
`(source name, fraction identifier, technical replicate, label)` coordinate is unique; no
empty cells; and none of the 52 is already present under `datasets/`.

`comment[sdrf annotation tool]` is `NT=sdrf-skeleton-gen;VV=v2.0.0`.
