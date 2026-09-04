# Adversarial review of the heart SDRF corpus

Every heart-annotated SDRF in `datasets/` was re-derived from primary evidence by an
independent reviewer that never saw the annotation it was judging. The brief was to
falsify each file, not to polish it: a value survives only if the deposit's own text or
its publication says so.

The review covers **252 SDRF files / 248 accessions**. It produced **323 evidence-backed
values** and **273 defects** in existing annotation (25 blocker, 70 important, 178 minor).

## Why this pass exists

`parse_sdrf` and this repository's review gate check *form*. They cannot see a value that
is a well-formed ontology term making a false statement — `disease = heart failure` on a
sham-operated mouse passes every check we run. That is the failure mode this pass targets,
and it is the reason the largest defect class below was invisible until now.

## Method

1. **Evidence harvest.** The PRIDE Archive v3 record for each accession, its linked PubMed
   IDs, and the Europe PMC full text of every open-access publication (101 of 141 linked
   papers were retrievable).
2. **Independent review.** 25 reviewer contexts, one per batch of ten accessions. Each saw
   only an evidence bundle — PRIDE title, description, sample-processing protocol, the
   submitter's dropdown fields, cue-filtered publication text, and the current SDRF — and
   worked under three standing rules:
   - PRIDE's `diseases` / `organismParts` / `organisms` fields are submitter-entered
     dropdowns. They are one witness, never evidence on their own.
   - A value may be written only if it holds for **every** row of the deposit.
   - Where the deposit publishes no run-to-sample key, a per-row assignment may not be
     invented. `not available` is the correct answer.
3. **Mechanical quote verification.** Every proposal and finding carries a quote, and each
   quote was re-checked as a verbatim substring of the evidence file it cites. A claim whose
   quote did not verify was discarded rather than trusted. All 323 proposals and 273
   findings in this directory passed that check.
4. **Application.** Two separate passes, so that filling a gap and contradicting an existing
   value are never confused: the first only ever writes into a sentinel cell or a column the
   file lacks; the second overwrites, and every one of its edits is listed individually in
   `applied.tsv` and traceable to a blocker/important finding.

## What changed

| column | files with a real value | annotated rows |
|---|---|---|
| `characteristics[disease]` | 84 → 102 (+18) | 18,043 → 22,536 (+4,493) |
| `characteristics[sex]` | 26 → 64 (+38) | 14,342 → 18,053 (+3,711) |
| `characteristics[developmental stage]` | 54 → 127 (+73) | 16,342 → 20,174 (+3,832) |
| `characteristics[age]` | 22 → 48 (+26) | 11,923 → 15,173 (+3,250) |
| `characteristics[strain or breed]` | 11 → 64 (+53) | 4,111 → 6,987 (+2,876) |
| `characteristics[cell type]` | 24 → 29 (+5) | 3,871 → 1,879 (**−1,992**) |
| files declaring an organism-layer template | 91 → 242 (+151) | |

`cell type` is the one column that loses rows, and that is the point: 1,992 of its rows
asserted a cell type that the deposit's own protocol contradicts (see below).

**The organism-layer template was missing from most of the corpus.** 151 heart files
declared only `ms-proteomics` and no `human` / `vertebrates` / `invertebrates` layer — the
layer that makes `disease` and `developmental stage` required in the first place. Declaring
it is what turns these fields from optional into part of the file's contract; where the
evidence supports no value, the column is now present and honestly `not available`.

## The four recurring defect classes

**1. A project-level diagnosis broadcast onto control rows.** The most common false claim
in the corpus. A deposit's disease written into every row of a design that also contains
sham, wild-type, vehicle or donor-control material — so the controls carry a diagnosis they
do not have, and the column that should encode the study's contrast encodes nothing.
Fifteen accessions, e.g. `restrictive cardiomyopathy` on all 48 rows of a
transgenic-vs-control mouse deposit (PXD021165), `heart failure` on all 150 rows of a
takotsubo model that compares stressed against unstressed animals (PXD032667).

**2. PRIDE's `cell type` dropdown imported onto bulk tissue.** `cardiac muscle cell`,
`cardiocyte`, `regular cardiac myocyte`, `cardiac muscle myoblast` asserted on rows whose
protocol describes whole-heart or whole-ventricle homogenate. The tissue contains those
cells; the sample is not those cells.

**3. Cultured material annotated as an organ.** hiPSC-derived cardiomyocytes and cardiac
progenitors, immortalised lines, organoids and engineered tissue carrying
`organism part = heart` — or, worse, carrying a cell-type string (`Fetal cardiomyocyte`,
`Cardiomyocyte cell line`) in the anatomical column. Such material has an anatomical
*identity*, not an anatomical *source*. PXD076291 is the rat H9c2 cardiomyoblast line;
PXD022091 is hiPSC-derived progenitors plus HEK293.

**4. Organism part copied from a dropdown the deposit's own title contradicts.**
PXD033029 is titled "Mouse PolG Mutant Liver Proteome"; PXD038922 is carotid endarterectomy
tissue; PXD032157 is the *reproductive-tract* atrium and male accessory glands of
*Anopheles gambiae*, swept into a cardiac collection because the submitter picked BTO's
"Atrium".

## Keeping the two organism-part fields in step

A correction to `characteristics[organism part]` has to reach `factor value[organism part]`
as well, or the file asserts two different tissues at once. A post-pass enforces this: where
the characteristic carries a real value the factor is rewritten to match, and where the
characteristic became a sentinel the factor column is removed instead — a sentinel-only
factor is `hollow_factor_value`, a hard gate failure, while an absent one is only advisory.
This also repaired a pre-existing mismatch in PXD008722, whose factor column already
published a per-row LA/RA/LV key that the characteristic (`heart` on all 252 rows) was
throwing away.

A *constant* factor value is not by itself a defect in this repository — a sample of `main`
runs roughly 290 constant to 73 absent to 37 multi-level, and the gate only fails a factor
whose every cell is a sentinel. Factor columns were therefore synced, not deleted, except
where a correction emptied them.

## What was deliberately NOT written

`left-unset.tsv` records 480 field/accession pairs where a value exists in the world but
cannot be attached to a row: case/control designs with no published run-to-sample key,
mixed-sex cohorts, TMT pools that mix both arms into every fraction, pooled donors. Leaving
these blank is the finding, not a gap in the work.

The review also declined to strip values that are merely *unsourced* rather than
*contradicted* — `developmental stage = adult` on PXD058436, `sex = male` on PXD064499,
`strain = C57BL/6J` on PXD061609. Those are flagged in `findings.tsv` for a curator with
access to the closed-access paper; removing a claim that may well be true is not an
improvement.

## Two repository-level issues this pass surfaced but did not fix

- **568 files repo-wide declare `dia-acquisition` but write the acquisition method as
  `NT=Data-independent acquisition;AC=PRIDE:0000450`, which that template rejects** (it
  requires the bare value). 27 files of this heart corpus fail `parse_sdrf` on `main` for
  this reason; they were left untouched here so this change does not inherit a pre-existing
  failure. The gate is path-filtered to changed files, so these never get re-validated.
- **A false value is invisible to CI by construction.** The one mechanical check that does
  catch a class of these without judgement is the instrument-vs-file-format contradiction
  already in the gate. Nothing comparable exists for `disease`, and the honest answer is
  that only evidence review finds them.

## Files in this directory

| file | contents |
|---|---|
| `findings.tsv` | every defect: accession, severity, column, current value, what is wrong, the quote that shows it |
| `evidence.tsv` | every value proposed: accession, field, value, confidence, source, quote |
| `left-unset.tsv` | fields deliberately left blank, and why no value can be written |
| `applied.tsv` | the exact edits made to each file |
