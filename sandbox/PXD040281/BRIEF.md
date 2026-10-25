# PXD040281

## Evidence and coverage

- [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD040281) and the
  [publication](https://pmc.ncbi.nlm.nih.gov/articles/PMC10565769/).
- The deposited `Metadata_Glycerol_Nordmann_et_al.csv` maps 38 acquisition
  directories: eight skin DVP samples and 30 tonsil samples. Every name matches
  the archive inventories. `Bulk.zip` contains 30 stored nested `.d.zip` files;
  `DVP.zip` contains eight native `.d` directories. The small SQLite metadata
  prefixes were read for all 38 acquisitions, without downloading spectra.
- The invalid one-row `Bulk.zip` sandbox placeholder is replaced by separate
  eight-row skin and 30-row tonsil drafts. Existing canonical SDRFs are retained.
  Their numeric biological replicate fields are not independent donor evidence.

## Annotation decisions

- Skin basal/suprabasal groups follow the author CSV. Four author repeats per
  group each collect 700 segmentation contours; these are not single-cell runs.
  Donor identifiers and biological versus technical replication are unresolved.
- Skin uses Lys-C/trypsin and diaPASEF. All eight deposited DIA method databases
  contain 12 scan groups, 24 windows, and limits 300.49–1199.61 m/z. The method
  and TDF acquisition range is 100–1700 m/z. Variable window widths are not a
  single fixed width. The publication identifies timsTOF SCP; the TDF internal
  instrument name is `timsTOF nano`.
- The skin MBR search tolerances are 15.049 ppm precursor and 20.1046 ppm
  fragment, as reported in the paper. These are not independently confirmed
  configuration values. No modification defaults are invented.
- Tonsil conditions are six retrieval buffers, each with five acquisition
  files. All 30 also appear in the deposited MaxQuant LFQ header; the paper's
  28-sample PCA does not identify which two files to exclude. The paper reports
  timsTOF Pro 2; native metadata records `TIMS TOF PP`. TCEP and ClAA are
  explicit preparation reagents. Physical digestion is only referred to an
  earlier protocol; search `Trypsin/P` is kept separately and is not substituted
  for independently established physical proteases.

## Local validation

Reviewed 2026-09-28 with sdrf-pipelines `701356bd5309` and repository review.
The skin draft fails only biological/technical replicate requirements. The
tonsil draft additionally lacks an established physical cleavage agent. These
remain sandbox drafts. The former ZIP placeholder and existing canonical files
pass the parser; that does not resolve their scientific mapping limitations.

Source reconciliation reads only the first duplicate enzyme column; checking
all declared enzymes confirms the skin Trypsin/Lys-C pair. Its bulk instrument
and enzyme alerts also mix the separate skin protocol into the tonsil arm;
the actual unresolved bulk enzyme gap is retained explicitly.
