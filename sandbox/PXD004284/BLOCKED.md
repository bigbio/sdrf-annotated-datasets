# PXD004284

BLOCKED: no public source says which of the 36 liver samples each raw file holds. The
fraction of every file is known, and the SILAC design is known. The sample (strain x
high-fat-diet duration x fed/fasted x replicate) behind each file is not in any source the
annotator could read. No SDRF is provided. Do not write one until the run -> sample map is known.

- PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD004284
  ("Mouse Liver LC-MSMS - System-wide quantitative proteomics of the metabolic syndrome in
  mice: genotypic and dietary effects"; submitted 2016-06-06, public 2016-12-22).
- Publication: Terfve C, Sabidó E, Wu Y, Gonçalves E, Choi M, Vaga S, Vitek O,
  Saez-Rodriguez J, Aebersold R. *System-wide quantitative proteomics of the metabolic syndrome
  in mice: genotypic and dietary effects.* J Proteome Res 2016. PMID 27936760,
  doi:10.1021/acs.jproteome.6b00815. Europe PMC has no full text. The open-access accepted
  manuscript (ETH Research Collection, hdl 20.500.11850/124881) returned HTTP 429 (rate limit)
  on every attempt. The ACS Supporting Information is paywalled and was not read.
- Preprint read in full: bioRxiv doi:10.1101/051508 (v posted 2016-05-12, CC-BY-NC).
- Organism: Mus musculus. Tissue: liver (PBS-perfused). Disease context: metabolic syndrome /
  diet-induced obesity model. PRIDE lists "type 2 diabetes mellitus" (DOID:9352). That is a
  submitter field and is not a per-sample fact: no mouse is reported as diabetic.
- Analysis code: https://github.com/saezlab/liverx (commit 34ad04e, 2017-02-09).

## What the evidence settles

**Design** (preprint, Results and Experimental Procedures; Figure 1):

> Liver samples from C57BL/6J and 129Sv mice (genetic background) fed with a high-fat rodent
> diet for 0, 6 and 12 weeks (time) were collected in biological triplicate either after ad
> libitum feeding or after overnight fasting (treatment), making a total of 36 samples for 12
> different experimental conditions

- Mice: "Three-weeks old C57Bl/6J and 129Sv mice were obtained from Charles River
  Laboratories". High-fat diet is "60 % fat content". Sex is not stated.
- Condition names used by the authors (liverx `data/result_sg_v2.3.7_protein_quant.tab`):
  `B6|S9` x `T0|T1|T2` (0, 6, 12 weeks) x `FED|FASTED`. That gives 12 conditions x 3
  biological replicates = 36 samples.

**SILAC design** (PRIDE sample protocol = preprint Methods): a spike-in reference, not a
pairwise comparison.

- Light channel: the mouse liver sample. 1 mg liver protein was mixed with 1 mg of reference.
- Heavy channel: Hepa1-6 mouse hepatoma cells (ATCC CRL-1830; Cellosaurus `Hepa 1-6`,
  CVCL_0327) grown in
  L-13C6 15N4-arginine and L-13C6 15N2-lysine, >95 % incorporation. The same reference was
  used "in all samples". It is its own source (for example `Hepa1-6 SILAC heavy reference`,
  cell-lines layer). The Figure 1 legend once says "HepG2". The Methods and the PRIDE
  protocol both say Hepa1-6 (ATCC CRL-1830). Hepa1-6 is the mouse line, so it is the correct one.
- Label modifications, OLS-verified: `Label:13C(6)15N(4)` UNIMOD:267 on R and
  `Label:13C(6)15N(2)` UNIMOD:259 on K. The deposited pep.xml search used
  R +10.0083 and K +8.0142 as variable modifications.
- Search (pep.xml `aminoacid_modification`, identical in all 6 searches): fixed
  Carbamidomethyl C (UNIMOD:4). Variable: Oxidation M (UNIMOD:35), the two SILAC labels, and
  Phospho S/T/Y (+79.9663, UNIMOD:21). The PRIDE data protocol mentions only Carbamidomethyl and
  Oxidation. The phospho variable modification appears only in the deposited search files.
  Sequest (Sorcerer 4.0.4), trypsin (MS:1001251), 2 missed cleavages, precursor tolerance
  50 ppm, PeptideProphet 1 % FDR, quantification with OpenMS 1.7 + MSstats 2.3.7.
- Instrument: LTQ FT (MS:1000448), confirmed in every mzXML header (`msModel` "LTQ FT",
  FTMS full scan 400-1600 m/z). Easy-nLC, 60 min 5-30 % B gradient, DDA.
- Files: 216 `.c.mzXML` (converted with ReAdW 4.0.2 from `.RAW`; no RAW files are deposited).

**Fraction of each file.** OFFGEL, 24 wells pooled into six fractions: A wells 1-2, B 3-4,
C 5-8, D 9-11, E 12-18, F 19-24. Each deposited `interactXtoY.pep.xml` lists the 36 runs it
searched. So every file has a known fraction:

| fraction (wells) | pep.xml | runs (36 each) |
|---|---|---|
| A (1-2) | `interact1to2.pep.xml` | `esabido_B1003_226` ... `esabido_B1003_272` |
| B (3-4) | `interact3to4.pep.xml` | `esabido_B1004_295` ... `esabido_B1004_341` |
| C (5-8) | `interact5to8.pep.xml` | `esabido_B1005_112` ... `esabido_B1005_172` |
| D (9-11) | `interact9to11.pep.xml` | `esabido_B1005_261` ... `esabido_B1005_312` |
| E (12-18) | `interact12to18.pep.xml` | `esabido_B1006_097` ... `esabido_B1006_143` |
| F (19-24) | `interact19to24.pep.xml` | `esabido_B1007_004` ... `esabido_B1007_056` |

This gives 36 samples x 6 fractions = 216 runs, which matches the design: one injection per
sample per fraction. The expected SDRF size is 216 files x 2 SILAC channels = 432 rows.

## Why blocked

1. **Sample identity of each run.** None of these sources names the mouse, condition or
   replicate behind any run: the file names (`esabido_B<batch>_<injection number>`), the mzXML
   headers (`parentFile` is only the RAW path), the pep.xml/prot.xml (only run base names), the
   PRIDE record, the preprint, and the liverx repository (condition-level results only, no run
   table).
2. The runs inside each fraction come in blocks of three consecutive injection numbers with a
   gap after each block (for example 226-228, 230-232, ...). This suggests triplicate blocks
   per condition, run in the same order in every fraction. That is a hypothesis from
   numbering, not evidence, and it does not say which block is which condition. The gaps are
   also irregular in fractions C, D and F. Do not use it to assign samples.
3. The published article and its Supporting Information (ACS) were not readable here. They
   may contain a run list.

## Unblock

Get a run -> sample table from the JPR Supporting Information, the ETH accepted manuscript,
or the authors (E. Sabidó, CRG; R. Aebersold, ETH). It must give each of the 216 files its
strain, HFD weeks (0/6/12), fed/fasted and biological replicate. Then annotate:

- templates `ms-proteomics`, `vertebrates`, plus `cell-lines` for the Hepa1-6 reference rows;
- per file, one `SILAC light` row (liver sample: `characteristics[strain/breed]` C57BL/6J or
  129Sv, organism part liver, diet / fasting / time characteristics, biological replicate) and
  one `SILAC heavy` row (source `Hepa1-6 SILAC heavy reference`, cell line `Hepa 1-6`,
  Cellosaurus CVCL_0327, which is ATCC CRL-1830 per the Cellosaurus API);
- `comment[fraction identifier]` 1-6 for A-F from the table above;
- `comment[modification parameters]`: Carbamidomethyl C fixed; Oxidation M, Phospho STY,
  Label:13C(6)15N(4) R and Label:13C(6)15N(2) K variable;
- factor values for strain, high-fat diet duration and fed/fasted.

Do not take the disease from the PRIDE dropdown, and do not take the sample order from the run
numbering.
