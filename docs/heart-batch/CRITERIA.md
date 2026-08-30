# Cardiac SDRF batch — criteria (v2, rebuilt after adversarial review)

## Why there is a v2

The first build of this batch (390 files) read PRIDE's structured fields — `instruments[0]`,
`diseases`, `organismParts`, `organisms[0]` — as ground truth. Ten independent adversarial
reviewers, working from fresh context against the deposits and their publications, found those
dropdowns wrong or incomplete often enough to produce false claims that **every validator
passed**: `parse_sdrf`, this repository's review gate, and CodeRabbit all returned clean on
files asserting mouse heart for human HeLa QC injections, `heart` for epicardial adipose tissue,
`Trypsin` for a study that digested nothing, and a patient diagnosis for wild-type controls.

Those files were never merged. This is the rebuild.

## The rule that changed

**PRIDE's dropdown is one witness, not the record.** Every value is now reconciled against the
deposit's own title, protocol prose, run names and — where the paper is open access — its
methods section. Any disagreement resolves to a sentinel. `not available` is a result, not a
failure; a wrong specific value is worse for reuse than an honest blank.

Publication evidence was resolved through Europe PMC for every accession: **full text for 185,
abstract for 104, and nothing for 101**. Where there is no paper, a claim that rests only on
PRIDE is treated as unverified.

## What each check does now

| Field | v1 | v2 |
|---|---|---|
| **organism** | `organisms[0]` | flagged when the prose names exactly one species and never the declared one — deposit skipped |
| **organism part** | `organismParts[0]` | dropped to a sentinel when the title names a different tissue (epicardial adipose, aortic arch, carotid plaque), when the material is cultured/immortalised/recombinant, or when run names name another organ or a cell line |
| **disease** | `diseases[0]` on every row | written only when PRIDE registers exactly one, it is not the generic `cardiovascular system disease` bucket, it is a real disease-ontology term, and neither the run names nor the record nor the paper indicate a control arm |
| **instrument** | `instruments[0]` | taken from the paper first, then the protocol prose, then PRIDE; rejected outright when the vendor could not have written the deposited file format |
| **acquisition mode** | one value per file | per run, from the run's own `DDA`/`IDA`/`DDALib`/`SWATH`/`PRM` token; a deposit that interleaves library and DIA runs no longer declares `dia-acquisition`, which requires a single value |
| **cleavage agent** | first pattern to match anywhere | every protease named **in a sentence that also carries a digest cue** and does not read as a measurement of the enzyme; a Lys-C→trypsin double digest now gets two columns |
| **modifications** | carbamidomethyl + oxidation only | plus phospho, acetyl, GlyGly and deamidation where the protocol states them |
| **run selection** | one format by preference order | a deposit holding two real acquisition formats is skipped rather than half-annotated |

Two specific bugs from v1, both of the same shape — a pattern matching a word playing a
different role:

- `\bicat\b` unanchored matched inside "quantifi**cat**ion", dropping label-free deposits as
  labelled. (Found and fixed before v1 shipped; noted here because the class recurred.)
- `\btrypsin` did not match `tryptic`, while `\bchymotrypsin` matched *"the UPS showed a higher
  **chymotrypsin-like activity**"* — a proteasome assay. One deposit therefore lost its real
  enzyme and gained a fabricated one. Protease detection is now sentence-scoped and requires a
  digest cue.

## Scope

16 accessions the review confirmed are **not cardiac at all** were removed — the keyword sweep
matched a pathway, an application or an anatomical homonym rather than a sample. `PXD034890`
is medulloblastoma ("ventricular zone" is a *neural* structure); `PXD068560` deposits liver and
HeLa QC runs and no heart runs at all despite its title.

## Result

**294 files, 21,082 rows, 294/294 clean** through `.github/scripts/sdrf_review.py` on
`sdrf-pipelines` 0.1.6. v1 produced 390 files from the same candidate pool; the 96-file
difference is deposits the stricter screens could not annotate faithfully, which is the
intended direction.

Every value still comes from the archive record, the run names or the publication. Nothing about
sample grouping is inferred: each deposited run is its own `source name`
(`<ACCESSION>-Sample-<n>`), with `assay name` carrying the run stem and biological replicate,
technical replicate and fraction all `1`. `comment[sdrf annotation tool]` is
`NT=sdrf-skeleton-gen;VV=v2.0.0`.
