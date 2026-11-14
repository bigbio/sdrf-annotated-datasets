# PXD065223 - BLOCKED subset: SILAC virion mixtures with no channel -> sample map (Q Exactive)

Annotated in [`datasets/PXD065223/`](../../datasets/PXD065223/):
`PXD065223-individual-virion-preps.sdrf.tsv` (35 .raw runs - the six individually analysed,
single-channel HCMV Merlin virion preparations). **Coverage: 35 of the 59 deposited vendor .raw files
are annotated; the 24 listed below are not.**

Study: "Virion proteomics of genetically intact HCMV reveals a regulator of envelope glycoprotein
composition that protects against humoral immunity", PNAS 2025, doi:10.1073/pnas.2425622122
(PMC12478159). SILAC (light / medium 13C6 / heavy 13C6-15N4 Arg + 13C6-15N2 Lys), in-gel trypsin
digest of six gel bands per preparation, Thermo Q Exactive, MaxQuant 2.4.8.0.

## Affected files (24, from PRIDE files/all; all are vendor Thermo .raw)

Group A - triple-SILAC virion mixtures (12):
- `RS_3_1_070514_run1.raw`
- `RS_3_2_070514_run1.raw`
- `RS_3_3_070514_run1.raw`
- `RS_3_4_070514_run1.raw`
- `RS_3_5_070514_run1.raw`
- `RS_3_6_070514_run1.raw`
- `RS_1_triple_1_290714_run1.raw`
- `RS_1_triple_2_290714_run1.raw`
- `RS_1_triple_3_290714_run1.raw`
- `RS_1_triple_4_290714_run1.raw`
- `RS_1_triple_5_290714_run1.raw`
- `RS_1_triple_6_290714_run1.raw`

Group B - runs absent from every deposited search output (12):
- `RS_2_triple_1_280714_run1.raw`
- `RS_2_triple_2_280714_run1.raw`
- `RS_2_triple_3_280714_run1.raw`
- `RS_2_triple_4_280714_run1.raw`
- `RS_2_triple_5_280714_run1.raw`
- `RS_2_triple_6_280714_run1.raw`
- `RS_4_triple_1_310714_run1.raw`
- `RS_4_triple_2_310714_run1.raw`
- `RS_4_triple_3_310714_run1.raw`
- `RS_4_triple_4_310714_run1.raw`
- `RS_4_triple_5_310714_run1.raw`
- `RS_4_triple_6_310714_run1.raw`

Associated (not runs): `peptides.txt`, `media-2.txt` (= Dataset S1, virion proteinGroups),
`media-4.txt` (= Dataset S3, gpUL141 SILAC-IP).

## Why

- **The file format is not the problem here.** Unlike
  [`sandbox/PXD065538/BLOCKED.md`](../PXD065538/BLOCKED.md), where the runs existed only as converted
  mzML, all 24 files above are deposited vendor Thermo `.raw` and are therefore eligible for
  `comment[data file]` under both the SDRF specification and the curation convention this annotation
  follows (bigbio/sdrf-skills: `comment[data file]` references the vendor raw file, never a converted
  peak list). What is missing is the **SILAC channel -> sample map**, so they were left out rather than
  annotated against an invented channel identity.
- **Group A** are the only multi-channel experiments in the deposited search output. Of the eight
  experiments in `peptides.txt` / Dataset S1, only `RS_3` and `RS1` carry per-channel columns
  (`Intensity L RS_3`, `Intensity M RS_3`, `Intensity H RS_3`, and the same for `RS1`) together with
  `Ratio M/L`, `Ratio H/L` and `Ratio H/M`; `RS1` matches the `RS_1_triple_*` stem by elimination.
  The paper says quantitative comparisons were made "as two groups of three variants" and SI Fig. S1
  names the variants compared in each group - group 1: dRL13, dRL13+dUL128L, dRL13/UL128int; group 2:
  dRL13, dRL13+dUL128L, wild-type. Main-text Fig. 1A partitions the variants differently (mix 1:
  wild-type, dRL13, dUL128+dRL13; mix 2: wild-type, intermediate-UL128L dRL13, dUL128 dRL13), so even
  the group membership is not consistent between sources - and **no source states which isotope
  channel (light / medium / heavy) each variant occupied**. Three variants per run leave six possible assignments and no evidence
  to choose between them. Annotating these 12 runs as three channel rows each would raise coverage to
  47/59, and they are otherwise fully annotatable (same instrument, same method, same gel-band
  fractionation as the 35 annotated runs), so this is the single change that would most improve the
  dataset - but only once the map is stated. It is not inferred here.
- **Group B** appear in no deposited or supplementary search output: no experiment of either name
  exists in `peptides.txt`, Dataset S1 or Dataset S3. Their names say "triple", yet Dataset S3 (the
  gpUL141 SILAC-IP) is a two-channel search (`Ratio H/L`, `Intensity L`, `Intensity H`, a single
  experiment) that names neither raw files nor experiments - even though the IP's channel identities
  *are* stated in Fig. 2A (Medium = gpUL141-V5 virions, Heavy = dUL141 virions). For these 12 runs the
  variant, the channel and the experiment they belong to are all unknown.
- **Also unresolved for the 35 annotated runs:** the six preparations are the six Merlin variants the
  paper analysed individually (wild-type; dRL13; dRL13+dUL128L; two UL128-intron point mutants;
  dUL141), but no source maps a variant to a preparation number (1111, 1149, 1178, 1502, 1780, 1864).
  The SDRF therefore asserts no genotype and carries `factor value[source name]` so that a reanalysis
  keeps the six preparations apart.
- Sources exhausted for all of the above: paper Results and Methods; SI Appendix Extended Methods,
  Fig. S1, Table S1; Datasets S1-S3; the PRIDE record and `files/all`; the deposited `peptides.txt`,
  `media-2.txt` and `media-4.txt`; the paper's Data Availability link (Zenodo
  10.5281/zenodo.16351176) and the corresponding Apollo record (10.17863/CAM.118380), both of which
  hold AlphaFold3 models only; and Europe PMC full-text searches for
  the lab's stock numbers (`RCMV1111` matches other papers of the same group, where it denotes the
  standard Merlin working stock; `RCMV1149`, `RCMV1502`, `RCMV1864` return no hits).

## Upstream metadata error in the PRIDE record

The PRIDE record's `instruments` CvParam for PXD065223 is **wrong**: it states
`MS:1002732 Orbitrap Fusion Lumos`, while the SI Extended Methods, the submitter's own
`sampleProcessingProtocol` and the header of every deposited `.raw` file (HTTP-range read: instrument
string `Q Exactive - Orbitrap MS`) all give a **Thermo Q Exactive** (`MS:1001911`), which is also the
only reading compatible with the 2014 acquisition timestamps in those headers. The annotated SDRF
follows the raw files. Anyone re-using this deposit's structured fields - for these 24 runs or the 35
annotated ones - should take the instrument from the raw headers, not from the record.

## What would unblock

- The MaxQuant run-to-experiment table from the original search - `mqpar.xml`,
  `experimentalDesignTemplate.txt`, `summary.txt` or `evidence.txt` (any file pairing a `Raw file`
  column with an `Experiment` column) - which would resolve the Group A run grouping and the Group B
  experiment membership, but not which variant occupied which channel (Group A still needs the
  channel statement below), or
- a statement from the authors (or an SI table) of which Merlin variant occupied the light, medium and
  heavy channel in each of the two triple-SILAC groups, which raw files belong to each group, and which
  raw files constitute the gpUL141 SILAC-IP. With that channel statement, Group A becomes a 36-row
  addition (12 runs x 3 channels) and coverage reaches 47/59.
- A variant-to-stock-number key for 1111 / 1149 / 1178 / 1502 / 1780 / 1864 would additionally add the
  genotype to the 35 annotated rows and give the study its real factor, replacing
  `factor value[source name]`.
