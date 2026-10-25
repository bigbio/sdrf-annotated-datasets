# PXD057685

## Evidence and coverage

- [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD057685) and
  [publication](https://pmc.ncbi.nlm.nih.gov/articles/PMC11875174/).
- Three raw archives contain 35 native timsTOF Pro acquisitions: nine at
  500 pg HeLa digest, eight at 200 pg, and 18 Xenopus acquisitions. Converted
  mzML files inside native directories are alternate representations, not
  additional samples. Original TDF metadata was read for every acquisition.
- Deposited `experiment_annotation.tsv` files map every native acquisition
  to its processing branch after explicit filename alias reconciliation:
  date punctuation, `ddaPASEF_window`/`EcoddaPASEF`, and `Eco-MS`/`EcoMS`.
  The matching is bijective and preserves date, run number, cell/TR identifier
  and acquisition method. Both the deposited name and analysis alias are saved.

## Decisions and remaining gaps

- The 18 Xenopus runs represent nine individually isolated stage-8 animal-cap
  blastomeres, each measured under classical IMS and Eco-IMS. The same cell
  source is retained across both acquisitions. Technical IDs 1/2 distinguish
  classical/Eco measurements; they do not assert injection order. Embryo-to-cell
  relationships are unavailable, so nine cells are not declared nine
  independent animal biological replicates. Their biological replicate remains
  unavailable; this subset stays in sandbox.
- HeLa material is commercial Pierce digest, not isolated human cells.
  The [manufacturer's catalog 88329](https://www.thermofisher.com/order/catalog/product/cl/en/88329)
  identifies HeLa S3 and Lys-C/trypsin digestion; see also
  [HeLa S3](https://www.cellosaurus.org/CVCL_0058) and the
  [manufacturer's brochure](https://documents.thermofisher.com/TFS-Assets/BID/brochures/mass-spectrometry-core-essentials-brochure.pdf).
  The two digest subsets are documented separately in `datasets/PXD057685`.
- Actual logs identify FragPipe 20.0, MSFragger 3.8 and IonQuant 1.9.8. Original
  configurations use fixed CAM, variable oxidation and protein N-terminal
  acetylation, two missed cleavages, and ±20 ppm precursor/20 ppm fragment
  tolerance. Xenopus uses `stricttrypsin` without proline protection; the HeLa
  branches use trypsin and Lys-C with proline protection.
- All selected processing workflows and completed logs enable MBR, including
  HeLa, contrary to the paper's stated HeLa MBR setting. The rows describe the
  deposited processing configurations. Additional 200 pg `_MBR` directories
  introduce a 10 ng reference acquisition absent from the raw archives; those
  branches are not represented as extra deposited runs.
- The paper reports a 300–1500 m/z MS1 range. TDF global acquisition limits
  are 100–1700 for the 500 pg and Xenopus runs, and 300–1500 for 200 pg.
  Both observations are retained with their provenance; the generic MS1 range
  is left unavailable pending scan-level resolution of that discrepancy.

## Local validation

Reviewed 2026-09-28 with sdrf-pipelines `701356bd5309`. The two HeLa subsets
pass `ms-proteomics`, `human`, `cell-lines` and repository review. The Xenopus
subset fails only the biological-replicate requirement under `ms-proteomics`,
`vertebrates` and `single-cell`. Offline ontology warnings are
reported separately; current OLS resolves HeLa-S3 to EFO:0002791.

Source reconciliation flags the HeLa tissue-origin/disease fields because run
names contain `HeLa` and `control`. The source is a commercial HeLa S3 digest,
and `control` labels the acquisition scheme; Cellosaurus supports the recorded
lineage. These are manually resolved heuristic alerts, not healthy-donor data.
