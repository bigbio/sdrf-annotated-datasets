# Known issues

Datasets where the deposit itself, or PRIDE's record of it, has a problem that annotation
alone cannot fix. The SDRFs stay in the repository: they sync to PRIDE, and each entry
states what is wrong and how it was checked, so pipelines can skip or adjust and
curators can follow up with the submitters.

## Severity

| Severity | Meaning | What a pipeline should do |
|---|---|---|
| **Critical** | The deposit cannot be reprocessed as annotated: the referenced data file holds no spectra. | Skip the dataset. |
| **Major** | Reprocessing runs but gives wrong or misleading results unless corrected. For example, the wrong labelling design or the wrong organism. | Do not use until resolved. |
| **Moderate** | Repository metadata contradicts the deposited files. The SDRF follows the files. | Use the SDRF, and treat PRIDE's field as unreliable. |
| **Minor** | Metadata is incomplete but not wrong. For example, a sample property that is not recoverable. | Use as is. |

## Critical: data file is not instrument data

Category: `data-file-not-spectra`. Each SDRF references a `.raw` file that exists in the
PRIDE deposit but contains no spectra. A Thermo `.raw` file is typically tens of
megabytes to gigabytes.

| Dataset | `comment[data file]` | Size | What the file actually is | Other files in the deposit |
|---|---|---|---|---|
| PXD024341 | `P8_2_.raw` | 2,239 B | PRIDE submission metadata (MTD) text | `PEPTIDES.TXT`, `PROTEIN_GROUP.TXT` |
| PXD024362 | `P6_2_.raw` | 2,234 B | PRIDE submission metadata (MTD) text | `PEPTIDES.TXT`, `PROTEIN_GROUP.TXT` |
| PXD024365 | `P8_1_.raw` | 2,236 B | PRIDE submission metadata (MTD) text | `PEPTIDES.TXT`, `PROTEIN_GROUP.TXT` |
| PXD038474 | `DWJ_20210318_Rpb3.raw` | 3,707 B | PRIDE submission metadata (MTD) text | `DWJ_20210318_Rpb3_GG_M.xlsx` |
| PXD043396 | `peptides2.raw` | 14,333 B | Excel workbook (`.xlsx`) renamed to `.raw` | `proteins.xlsx` |

How this was checked: file sizes come from the PRIDE Archive file listing
(`/pride/ws/archive/v3/projects/<PXD>/files/all`). The first bytes of each file were read
over HTTP from the PRIDE FTP mirror. None of these deposits contains another raw or
peak-list file that the SDRF could point to instead.

Resolution: the submitters re-deposit the instrument files.

## Moderate: PRIDE instrument field contradicts the raw file

Category: `repository-instrument-mismatch`. PRIDE's project-level instrument names a
different model from the one recorded in the header of the deposited `.raw` file. The
SDRF records the model in the header.

| Dataset | PRIDE instrument | Model in `.raw` header | Evidence file | Note |
|---|---|---|---|---|
| PXD044136 | Q Exactive HF | Q Exactive Plus | `P20180400209_PP.raw` | Header states the full model field (`Q Exactive Plus - Orbitrap MS`) |
| PXD047407 | Q Exactive HF | Q Exactive Plus | `21082002_YYM_LASV-Z.raw` | Header states the full model field (`Q Exactive Plus - Orbitrap MS`) |
| PXD051024 | Q Exactive HF | Orbitrap Fusion Lumos | `20220810_ZKhan_sample_C.raw.raw` | The paper also states Q Exactive HF; needs confirmation by the submitter |

How this was checked: the first 256 KB of each `.raw` file was read over HTTP from the
PRIDE FTP mirror and decoded as UTF-16-LE. The instrument model is written in the
file header.

Resolution: correct PRIDE's instrument field, or confirm with the submitter where
the header and the paper disagree.
