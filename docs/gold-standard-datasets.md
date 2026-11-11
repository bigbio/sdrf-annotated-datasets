# Gold standard datasets

A short, curated list of annotations to point a pipeline at when you need one that is
known to work — quantms, FragPipe, DIA-NN wrappers, or your own parser.

Almost all of these were already in `datasets/`. The point of this page is not that they
are new, but that they are *findable*: among 9,000+ accessions there was previously no way
to tell which annotations are safe to build a test suite on.

Every file listed here passes both CI gates — `parse_sdrf validate-sdrf` and
`.github/scripts/sdrf_review.py` (coordinate collisions, ragged rows, reserved-word
casing, value encoding, hollow factor values) — and has complete file mapping: every row
resolves to a real deposited run.

## Pick by what you need to exercise

| Testing… | Start with |
|---|---|
| a smoke test that finishes in seconds | `PXD008012` (141 rows) or `PXD066101` (112) |
| cell-line identity and Cellosaurus resolution at scale | `PXD030304` — 949 lines |
| sex / age / ancestry propagation | `PXD030304`, `PXD040455`, `PXD044986` |
| TMT channel→sample mapping | `PXD040455` (human), `PXD018814-phospho` (plant) |
| SILAC / metabolic labelling | `PXD002870` |
| a wide factor-value design matrix | `PXD039859` — 4 varying factors |
| phospho-enrichment metadata | `PXD036826-phospho`, `PXD039859`, `PXD030983-tissues-phosphoproteome` |
| non-human organism templates | `PXD002870`, `PXD030983` (mouse), `PXD000136`, `PXD018814` (plant), `PXD066101` (chicken) |
| per-patient clinical metadata | `PXD005571` |
| ion mobility | `PXD044986` (timsTOF SCP) |
| quantification against a known ground truth | the spike-in benchmarks below |

## Human cell lines

| Accession | File | Rows | Lines | Acq. | Label | Instrument |
|---|---|---|---|---|---|---|
| PXD030304 | `PXD030304.sdrf.tsv` | 5,798 | **949** | DIA | label free | TripleTOF 6600 |
| PXD040455 | `PXD040455.sdrf.tsv` | 1,178 | 4 | DDA | TMT | Orbitrap Exploris 480 |
| PXD039859 | `PXD039859.sdrf.tsv` | 372 | 6 | DDA | label free | Orbitrap Fusion Lumos |
| PXD014058 | `PXD014058.sdrf.tsv` | 323 | 4 | DDA | label free | Orbitrap Fusion Lumos |
| PXD044986 | `PXD044986.sdrf.tsv` | 315 | 6 | DDA | label free | timsTOF SCP |
| PXD036826 | `PXD036826-phospho.sdrf.tsv` | 144 | 12 | DIA | label free | Orbitrap Fusion Lumos |
| PXD008012 | `PXD008012.sdrf.tsv` | 141 | 9 | DDA | label free | Orbitrap Elite |

**`PXD030304`** is the one to reach for first. It carries `sex`, `age`,
`ancestry category`, `developmental stage`, `disease` and a Cellosaurus accession on every
row, across 949 distinct lines and 5,798 individually mapped `.wiff` files — 18 ancestry
categories, 104 distinct ages, 201 distinct diseases. Nothing else in the repository
exercises cell-line handling at that scale.

**`PXD039859`** has the richest *design*: 12 populated characteristics and four factors
that genuinely vary (cell line, compound, sampling time, enrichment process) in only 372
rows, so it runs fast while still testing a real design matrix.

## Human clinical

| Accession | File | Rows | Acq. | Label | Instrument |
|---|---|---|---|---|---|
| PXD005571 | `PXD005571.sdrf.tsv` | 124 | DDA | label free | Q Exactive |

42 liver samples from 21 patients (tumoral / non-tumoral), with sex, age, disease,
phenotype and subtype verified as genuinely per-individual rather than cohort values
copied down every row.

## Non-human

| Accession | File | Rows | Organism | Acq. | Label | Instrument |
|---|---|---|---|---|---|---|
| PXD030983 | `PXD030983-tissues-proteome.sdrf.tsv` | 1,536 | *M. musculus* | DDA | label free | Q Exactive HF |
| PXD002870 | `PXD002870.sdrf.tsv` | 1,477 | *M. musculus* | DDA | **metabolic** | Orbitrap Elite |
| PXD030983 | `PXD030983-tissues-phosphoproteome.sdrf.tsv` | 328 | *M. musculus* | DDA | label free | Q Exactive HF |
| PXD018814 | `PXD018814-phospho.sdrf.tsv` | 216 | *A. thaliana* | DDA | TMT | Q Exactive HF |
| PXD042904 | `PXD042904.sdrf.tsv` | 192 | *M. musculus* | DDA | label free | LTQ Orbitrap XL |
| PXD000136 | `PXD000136.sdrf.tsv` | 144 | *A. thaliana* | DDA | label free | LTQ FT |
| PXD066101 | `PXD066101.sdrf.tsv` | 112 | *G. gallus* | DDA | label free | Q Exactive HF |

These cover the `vertebrates` and `plants` organism templates, and `PXD002870` is the
only entry using metabolic (SILAC) labelling — worth including in any test matrix that
otherwise only sees label-free and TMT.

## Quantification benchmarks

Reach for these when you need a *known answer* rather than rich sample metadata — spike-in
and defined-ratio designs where the expected fold changes are known in advance.

| Accession | Rows | Organism | Acq. | Design |
|---|---|---|---|---|
| PXD000279 | 151 | *H. sapiens* | DDA | UPS1 spike-in dilution series |
| PXD002952 | 48 | *H. sapiens* | SWATH-MS | two-condition SWATH benchmark |
| PXD026600 | 24 | *E. coli* | DIA | spike-in series |

## How to use one

```bash
curl -fsSLO https://raw.githubusercontent.com/bigbio/sdrf-annotated-datasets/main/datasets/PXD030304/PXD030304.sdrf.tsv

parse_sdrf validate-sdrf --sdrf_file PXD030304.sdrf.tsv --template human
```

Check `comment[sdrf template]` in the file for the templates it declares, and validate
once per declared template — `--template` is single-valued, so passing several flags
validates only against the last one.

## What "gold standard" does and does not mean here

- **Does mean:** passes both CI gates; every row maps to a deposited run; the sample
  metadata is populated rather than filled with reserved words.
- **Does not mean** every value is biologically correct. The gates check structure,
  ontology resolution and internal consistency — not whether a curator read the paper
  correctly. Most of these have been in the repository for some time and have survived
  CI and community use, which is evidence, not proof.
- **Known rough edges:** ancestry in `PXD030304` is free text inherited from Cellosaurus,
  so `Caucasian` and `White` coexist as distinct values; several files use title-case
  `Male`/`Female` where the spec documents lowercase (the validator lowercases before
  comparing, so it passes).

Found a wrong value? Open an issue or a PR — see [CONTRIBUTING.md](../CONTRIBUTING.md).
