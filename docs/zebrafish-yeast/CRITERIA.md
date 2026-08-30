# Zebrafish and yeast metascreen criteria

## Goal

Give the two large model-organism corpora in PRIDE that this repository barely covers —
**zebrafish** (*Danio rerio*) and **yeast** — a validated, run-level SDRF baseline, so that
organism, instrument, acquisition mode and digest are machine-readable for every deposit
instead of only for the handful that have been curated by hand.

## Target organisms

- **Zebrafish**: *Danio rerio*
- **Budding yeast**: *Saccharomyces cerevisiae* (all strains and strain-qualified NEWT labels)
- **Fission yeast**: *Schizosaccharomyces pombe*
- **Other true yeasts**, kept as a clearly separated group: *Candida* (incl. *C. albicans*,
  *C. glabrata*, *C. auris*, *C. parapsilosis*, *C. tropicalis*), *Nakaseomyces*, *Yarrowia*,
  *Komagataella*/*Pichia*, *Kluyveromyces*, *Debaryomyces*, *Cryptococcus*, *Malassezia*,
  and the remaining Saccharomycetes genera.

*Candidatus* is a provisional-genus prefix for uncultured **bacteria and archaea**, not the
yeast genus *Candida*. Matching the genus as a substring pulled anammox bacteria and
Lokiarchaeota into an earlier draft of this screen; the classifier is word-anchored and
excludes *Candidatus* outright.

## Include when

- The deposit declares **exactly one** organism from the target list and is not already
  annotated under `datasets/` or `sandbox/`.
- The archive record names **one** instrument, and that instrument resolves to an MS
  ontology *model* (`MS:…`) via OLS4. `orbitrap` (MS:1000484) is an analyser type, not a
  model, and is rejected.
- The acquisition mode is recoverable from `experimentTypes` or stated in the protocol.
- The submitter's own record (sample-processing protocol, data-processing protocol, or
  project description) **names the protease**. `comment[cleavage agent details]` is a
  required, ontology-backed column: a sentinel fails validation and a default would be a
  guess, so an accession that never names one is skipped rather than given an assumed
  tryptic digest.
- At least one deposited file is a single acquisition in a format that can stand as a run
  (`.raw`, `.d.zip`/`.d.7z`, `.wiff`, `.dia`, `.mzML`/`.mzXML`, `.baf`, `.yep`, `.mgf`).

## Exclude when

- **Quantification is labelled** (SILAC, TMT, iTRAQ, dimethyl, ICAT, any isobaric tag),
  whether declared in `quantificationMethods` or stated in the methods text. A labelled
  run carries several samples in one file, and PRIDE deposits ship no channel-to-sample
  key; annotating one would mean inventing the assignment. This is the single largest
  exclusion in the screen.
- The experiment type falls outside the `ms-proteomics` template: chemical cross-linking,
  top-down, affinity proteomics, MS imaging, RNA MS.
- The record lists several instruments — the record gives no way to say which run came off
  which machine.
- Several organisms are declared, since `characteristics[organism]` is per row and the
  record gives no per-run mapping.
- Only archive bundles (`.zip`, `.rar`) are deposited, with no way to tell how many
  acquisitions they hold.

## What the resulting annotation asserts, and what it does not

Every value written comes from the PRIDE archive record for the accession — project
metadata, sample attributes, file listing — or from an explicit statement in the
submitter's own protocol text.

**Nothing is inferred about which run belongs to which biological sample.** Each raw file
is its own `source name`, with `characteristics[biological replicate]`,
`comment[technical replicate]` and `comment[fraction identifier]` all `1`. Where a
deposit really is fractionated, or really does contain replicate injections, that
structure is *not* encoded — it is left for a curator who has the publication in hand.
These files are a validated floor to build on, not a finished curation.

A `factor value[…]` column is written only where the archive record carries a real value
for it (a stated disease, or a single stated organism part). A placeholder factor would
assert a contrast the record does not support, so the column is omitted instead.

## Extract columns

`id`, `group`, `label` (include|skip), `reason`, `organism_taxname`, `pmid`,
`n_raw_files`, `n_sdrf_rows`, `instrument`, `quantification`, `experiment_types`, `title`
