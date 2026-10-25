# PXD029320 — reconstructed, biological-replicate evidence incomplete

## Evidence

- [PRIDE project](https://www.ebi.ac.uk/pride/archive/projects/PXD029320)
  and [deposited files](https://ftp.pride.ebi.ac.uk/pride/data/archive/2022/03/PXD029320/).
- [Furtwangler et al., DOI 10.1016/j.mcpro.2022.100219](https://doi.org/10.1016/j.mcpro.2022.100219),
  including the sample-processing and analysis methods deposited in PRIDE.
- [Author RETICLE repository at commit 80bfd8e](https://github.com/bfurtwa/RETICLE/tree/80bfd8e337725b6e22779d060a330c92ccd37e0c):
  `results/scMS/*/meta.txt`, the plate/label/sort layouts under `data/`,
  `data/diluted_sample/{100x,200x}/mapping.csv`, and `code/diluted_sample.ipynb`.
- [Schoof et al., DOI 10.1038/s41467-021-23667-y](https://doi.org/10.1038/s41467-021-23667-y),
  the source of the bulk standard reused in the later study.
- Fourteen deposited `.pdStudy` files; parameters were read from their active
  `Sequest HT` nodes. Instrument identity was checked in all 97 RAW headers.

## Repaired mapping

The former 97-row draft assigned one cycling TMT channel and a new biological
replicate to each RAW. It also treated the diluted bulk standard as individual
cells. It has been replaced with two files covering every deposited RAW:

| Draft | RAW files | Rows | Material represented |
| --- | ---: | ---: | --- |
| `PXD029320-single-cell.sdrf.tsv` | 58 | 870 | 812 individual cells plus 58 carrier-channel rows |
| `PXD029320-diluted-standard.sdrf.tsv` | 39 | 390 | Nine diluted bulk channels plus a carrier in each acquisition |

### Single cells

All 812 cell/RAW/channel assignments match the author's metadata and were
cross-checked against the independent sort, sample, and balanced label
layouts. Plate/well combinations are unique across the six acquisition
groups. Source names retain those physical identities as
`PXD029320_P<plate>_<well>`. Each run contains four CD34-negative, five
CD34-positive/CD38-positive, and five CD34-positive/CD38-negative cells.
The phenotype labels describe populations within the OCI-AML8227 model.

TMT126 is the carrier channel and TMT127C is empty. Empty channels are
documented as comments and have no invented biological source rows.
The carrier was pooled separately; its source is distinct from the standard
experiment's carrier. The 200-cell equivalent describes the injected
carrier amount, so it is recorded at assay level. It is not copied into
`characteristics[cells per well]`, which is one for each true single cell.

The author's `MS2_500` acquisition F7 is retained and marked as excluded
from their analysis as a failed acquisition. The annotation covers deposited
loaded samples before cell-level quality filtering; its cell count is not
the count retained in the paper's final analysis.

### Diluted standard

The author's two mapping CSVs identify 36 runs. The three remaining
close-out experiments are explicitly named in the notebook and in
`RETICLE_closeout.pdStudy`. They use the 100-cell-equivalent carrier, with
close-out settings four, disabled, and ten.

| Author sample | TMT channel | Sorted population |
| --- | --- | --- |
| BLAST1 / BLAST2 / BLAST3 | 127N / 131N / 132C | CD34- |
| PROG1 / PROG2 / PROG3 | 129N / 131C / 133N | CD34+CD38+ |
| LSC1 / LSC2 / LSC3 | 128N / 130C / 133C | CD34+CD38- |

Each of these nine loaded channels contains 250 pg of diluted bulk peptides
per injection. The six unused channels are listed separately as empty.
The original bulk study explicitly calls the three reporter channels per
population **technical replicates**. Their identifiers are preserved as
`comment[bulk preparation replicate]`; they do not become three independent
biological replicates. Repeated injections retain the same prepared-sample
source names. Technical-run numbers enumerate acquisitions for each source.

The three loaded channels nearest the carrier remain annotated even though
the author's main diluted-standard comparison excludes them for carrier
contamination. Exclusion during analysis does not make a loaded channel empty.

## Method corrections

All 97 RAW headers identify Orbitrap Eclipse. The older standard's original
Orbitrap Fusion acquisitions and fractionation scheme are not transferred
to these later, unfractionated dilution runs.

The actual Sequest precursor tolerance is 10 ppm. Fragment tolerance is
0.02 Da for MS2/RETICLE and 0.6 Da for RTS-MS3. The `.pdStudy` files also
contain a separate recalibration node with different tolerances; those are
not substituted for the database-search parameters. Each row identifies
its deposited search-parameter file.

Search modifications include fixed TMTpro on lysine and peptide N-termini,
and variable methionine oxidation, protein N-terminal acetylation,
methionine loss, and combined methionine loss plus acetylation. Fixed
carbamidomethylation is present only in the diluted-standard search.
The local PD TMTpro definitions are resolved to
[UNIMOD:2016](https://www.unimod.org/modifications_view.php?editid1=2016)
by matching name, mass, composition, and modified sites. Reporter labels
use PRIDE's `TMT126` through `TMT134N` names; the modification columns retain
the distinct TMTpro chemistry. The unsupported uniform collision-energy
value in the old draft has been removed.

## Remaining gate

The public records identify individual cells, pooled carriers, physical
plate batches, and technical preparations. They do not resolve the
independent culture/biological-replicate relationships. The plate numbers
and RAW numbers are not substituted for that missing information.
Biological replicate therefore remains `not available` for the study cells
and standard preparations, and `pooled` for the carriers. Donor age, sex,
individual identity, and a Cellosaurus accession are also unavailable.

These are **sandbox drafts**, not validated canonical datasets. Checked
on 2026-09-28 with sdrf-pipelines main
`701356bd5309f352b499846dcb4c31709b65bf8a`; the required biological-replicate
field blocks parser acceptance. No fake replicate numbers, ignored checks,
or warning suppressions were added. To promote them, obtain a supported
culture/replicate crosswalk and rerun all declared templates. The verified
cell, channel, file, and technical-preparation mappings can be retained.
