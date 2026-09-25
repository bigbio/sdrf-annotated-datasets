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

## Major: labelled experiment annotated as a single label-free sample

Category: `collapsed-multiplex`. Each SDRF has one row labelled `label free sample`,
but the deposit is a multiplexed run: several labelled samples were pooled and measured
in the one raw file. Quantification with these SDRFs would treat the pool as one
sample. Each needs one row per label channel, with its channel-to-sample map.

| Dataset | Labelling | Evidence |
|---|---|---|
| PXD027232 | TMT10plex, 6 samples | Raw header method `Fusion_TMT10_PTM_60min...`; deposited `LC-MS data.xlsx` quantifies Sirt7KD1-3 and Sirt7ctr1-3. Which channel carries which sample is not stated anywhere |
| PXD044020 | TMTpro, plex not stated | Protocol sets TMTpro on K and peptide N-termini; the paper (Cell 2024, PMC11145561) pools three conditions (empty vector, MBC-TurboID, BCAT2-TurboID) in one run. No sample sheet or channel map is deposited or published |

How this was checked: each SDRF's `comment[label]` was compared with PRIDE's
quantification method, the sample and data processing protocols, and the deposited
file names.

Resolution: re-annotate with one row per channel from the channel-to-sample map.

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

## Moderate: deposited SDRF is internally inconsistent

Category: `deposited-sdrf-inconsistent`. The SDRF was deposited by the submitter and is
kept as deposited. The deposit does not show which of the conflicting values is right.

| Dataset | Problem |
|---|---|
| PXD006439 | Sample 14 (2 rows) is cell line B16-F10 with disease `low metastatic potential`; the other 30 B16-F10 rows say `high metastatic potential`, and all B16-F1 rows say `low`. Either the cell line or the disease value is wrong for Sample 14. |

Resolution: confirm with the submitter.
