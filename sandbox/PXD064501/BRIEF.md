# PXD064501

## Evidence and coverage

- [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD064501) and
  [primary publication](https://doi.org/10.1186/s13059-026-04110-1), including
  its supplementary document, describe adult male mouse cardiomyocytes.
- The complete archive inventory contains 14 RAW, 14 mzML and 14 mzIdentML
  files. All 14 native RAW headers identify Orbitrap Eclipse. Alternate
  representations are not extra acquisitions.
- Each multiplex has eight cell channels: 126, 127N, 127C, 128N, 128C, 129N,
  129C and 130C. 130N is explicitly empty. 131 contains a pool of 100 control
  and 100 Myc-overexpressing cardiomyocytes. The corrected draft therefore
  contains 112 cell rows and 14 carrier rows. Empty channels are not samples.
- Isolation was FACS. The paper specifies trypsin digestion, TMT10plex,
  RETICLE, CID for the real-time search and HCD for reporter quantification.
  The 30 and 38 NCE settings are kept with their corresponding scan events.
- [Figure 3 inputs](https://zenodo.org/records/19484833) and
  [analytical cell-to-TMT metadata](https://zenodo.org/records/20273639) were
  inspected. The latter distinguishes TMT70A and TMT70B as separate sets and
  contains 81 batch identifiers; one TMT6 cell is absent from the processed
  metadata. The [iSanXoT template](https://zenodo.org/records/19439667) provides
  explicit tag assignments for the separate pilot dataset, whose RAW names
  differ from these accessions. Those assignments are not transferred here.

## Remaining gaps

The publication uses two alternating tag designs. A per-channel genotype and
mouse mapping for this accession has not been established. Biological replicate,
individual and single-cell genotype remain unavailable. RAW/channel-derived cell
identifiers are annotation identifiers, not claimed author cell IDs. The two mice
per genotype reported in Methods do not supply a cell-to-mouse crosswalk.
Carrier isolation details also remain unavailable.

The paper reports Sequest HT in Proteome Discoverer 2.5, an initial precursor
search tolerance of 800 ppm, and a subsequent 15 ppm mass-error filter. The
representative deposited mzIdentML header instead declares X! Tandem and
ProteoWizard 3.0.22187. These branches are not reconciled: the general tolerance
fields remain unavailable, and the published parameters and modifications are
explicitly described as the reported analysis. A 15 ppm post-filter is not an
initial search tolerance. No reduction/alkylation step is borrowed from the
paper's separate bulk-heart workflow.

## Local validation

Reviewed 2026-09-28 with sdrf-pipelines `701356bd5309`. The corrected draft is
kept in sandbox because biological replicate and carrier isolation provenance
are unresolved. The previous draft parsed successfully despite treating the
empty 130N channel as a cell and giving all cells an unsupported biological
replicate of 1. Parsing success did not verify that experimental design.
