# Known issues

Datasets whose SDRF is kept in the repository but describes a deposit that cannot be
reprocessed as annotated. They are not removed: SDRFs here sync to PRIDE, and each entry
states what is wrong so that pipelines can skip them and curators can follow up.

## Data file is not instrument data

Each of these SDRFs references a `.raw` file that exists in the PRIDE deposit, but the file
contains no spectra. A Thermo `.raw` file is typically tens of megabytes to gigabytes.

| Dataset | `comment[data file]` | Size | What the file actually is | Other files in the deposit |
|---|---|---|---|---|
| PXD024341 | `P8_2_.raw` | 2,239 B | PRIDE submission metadata (MTD) text | `PEPTIDES.TXT`, `PROTEIN_GROUP.TXT` |
| PXD024362 | `P6_2_.raw` | 2,234 B | PRIDE submission metadata (MTD) text | `PEPTIDES.TXT`, `PROTEIN_GROUP.TXT` |
| PXD024365 | `P8_1_.raw` | 2,236 B | PRIDE submission metadata (MTD) text | `PEPTIDES.TXT`, `PROTEIN_GROUP.TXT` |
| PXD038474 | `DWJ_20210318_Rpb3.raw` | 3,707 B | PRIDE submission metadata (MTD) text | `DWJ_20210318_Rpb3_GG_M.xlsx` |
| PXD043396 | `peptides2.raw` | 14,333 B | Excel workbook (`.xlsx`) renamed to `.raw` | `proteins.xlsx` |

How this was checked: file sizes from the PRIDE Archive file listing
(`/pride/ws/archive/v3/projects/<PXD>/files/all`), and the first bytes of each file read
over HTTP from the PRIDE FTP mirror. None of these deposits contains another raw or
peak-list file that the SDRF could point to instead.

What would resolve them: the submitters re-depositing the instrument files through PRIDE.
Until then, the sample and protocol annotation in these SDRFs is still accurate, but there
is no run to reprocess.
