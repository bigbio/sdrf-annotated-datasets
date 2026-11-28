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
| PXD004372 | TMT6plex, 6 E. coli secretome samples | PRIDE `sampleProcessingProtocol` labels the seven ATCC strains (O111:H8, O145, O26:H11, O103:H11, O45:H2, O121:H19, K12 MG1655) with tandem-mass-tag reagents, pools them, and fractionates to 12 high-pH RP fractions run as technical replicates. The paper (Proteomics 2017, PMID 28070933) quantifies the six "big-six" strains against K12 but never states which reporter (126-131) carries which strain; the deposited `pep.xml`/`prot.xml` show only TMT6plex modifications with no per-channel sample names. The raw filenames say `7TMT` (7 strains in the `Ecoli_Seven_nr` search database) while the registered label is TMT6plex (6 reporters), so the seventh strain does not correspond to a distinct label channel; the channel-to-strain map is not stated anywhere |
| PXD044020 | TMTpro, plex not stated | Protocol sets TMTpro on K and peptide N-termini; the paper (Cell 2024, PMC11145561) pools three conditions (empty vector, MBC-TurboID, BCAT2-TurboID) in one run. No sample sheet or channel map is deposited or published |
| PXD005236 | TMT10plex, 10 samples | Protocol labels 10 samples with TMT 10-plex, pools them and fractionates into 8 high-pH RP fractions, each analysed on Orbitrap Fusion, so every `.raw` is a pooled 10-plex slice. Paper Table 3 / GEO GSE92601 name the 10 samples (WT1/2(DA50289), ORF1(DA50290) 1/2 ±IPTG, SVI3-3(DA50288) 1/2 ±IPTG) but assign **no reporter channel to any sample**; the deposit (8 `.raw` + one `.msf`, no design sheet) states the exact reporter→sample map nowhere |
| PXD005894 | TMT6plex, 6 final pooled samples | Protocol pools biological replicates into 6 TMT sixplex-labelled samples but assigns **no reporter channel to any sample**; the SDRF keeps run-level sources (`Gustavo-Vega_TMT_TPV1A/B` … CID/HCD pairs) with no per-channel map. c-di-GMP/BCG pellicle strains WT, ΔPDE, ΔDGC are never tied to a channel |
| PXD055203 | TMTpro 16-plex, cervical cancer | Protocol labels 16-plex TMTpro and pools each TMT set for high-pH fractionation; the SDRF source names are acquired `_GroupNN.tar`/DIA archive names, not samples, and assign **no channel to any of the 139 patients**. Channel→patient map appears only in the paper's extended data, not in the deposit |
| PXD009495 | TMT10plex thermal proteome profiling, E. coli + HepG2 | Thermal proteome profiling (meltome, 2D-TPP, TPP-CCR, ΔtolC mutants). Each `.raw` is one SEC fraction of a pooled TMT10plex run (10 channels = 10 temperatures or drug concentrations), but the SDRF has one row per `.raw` with `comment[label]=TMT10plex` and no channel. The paper (PMC6056769, PMID 29980614) defines per-experiment channel schemes in Dataset EV1/3/4/5 (meltome temperatures), EV8 (TPP-CCR concentrations), EV9–12 (2D-TPP concentrations × temperatures), but the SDRF's generic `Sample_N` sources never record which experiment/replicate each run belongs to, and the ΔtolC `Ecoli_mutants_170405` run (52 files) has no published channel map in any EV. PRIDE holds only `.raw`/`.dat` plus the SDRF — no design sheet |
| IPX0002466000 | iTRAQ (phospho + proteome), OSCC | One row per pooled iTRAQ run: sources are pool names (`OSCC_7779TPSY01` …) each spanning up to 24 fraction files, with **no channel/reporter column** and no per-channel sample map anywhere |
| IPX0003183000 (renamed from PXD043263) | TMTpro per SDRF; paper states TMT 6-plex or 10-plex | One row per fraction `.raw` in the TMT families (`20161022-Group1-TMT-R1/R2F*`, `20170418_Group3_TMT_R1/R2E*`, `20200826_ANTICANCER-TMT10-TOP-F*`), `comment[label]` is the bare `TMTpro` with **no channel**, and no reporter channel is assigned to any sample. The accompanying paper (J Pharm Anal 2024, PMC10859532) quantifies the MCF7 78-drug panel with TMT (6-plex or 10-plex, channels 126–131) and never states which channel carries which sample |
| PXD000752 | iTRAQ 8-plex, 2 pools × 36 IPG fractions | PRIDE `sampleProcessingProtocol` labels samples with 8plex iTRAQ then separates by IEF; each `.raw` fraction is one slice of a pooled 8-plex, so it holds all 8 channels. The only source names are the pools (`alveolar macrophage iTRAQ plex 1/2`); which reporter carries which subject is not recorded |
| PXD000928 | iTRAQ 8-plex, 2 pools × IPG fractions | PRIDE `sampleProcessingProtocol` labels with 8plex iTRAQ and isoelectric focusing; each `.raw` is a pooled 8-plex slice. Source names collapse to `melanoma lymph-node metastasis iTRAQ plex I/II` with no per-channel sample map |
| PXD000996 | iTRAQ 8-plex, 2 pools × 72 IPG fractions | Same Karolinska HiRIEF iTRAQ 8-plex design; PRIDE `sampleProcessingProtocol` states 8plex iTRAQ + isoelectric focusing. Rows use only pool-level sources (`thyroid cyst fluid iTRAQ plex 1/2`), no channel map |
| PXD001808 | iTRAQ 8-plex, 3 pools (15 cases + 5 controls) | `sampleProcessingProtocol` describes three 8-plex experiments "each with one reference pool (113 reporter), two controls … and five cases", but the SDRF keeps only pool-level sources (`BALF exosome iTRAQ plex 1-3`); the exact channel→subject assignment is not recorded and not recoverable from file names |
| PXD003702 | iTRAQ 8-plex, 6 pools × IPG fractions | PRIDE `sampleProcessingProtocol`: "processed using FASP with trypsin, iTRAQ and HiRIEF". Each fraction `.raw` is a pooled 8-plex slice; sources are named only by pool (`ascending aorta tissue iTRAQ 2013apr23_pool1_pool1` …), no channel map |
| PXD031800 | TMT16plex, PISA (16 temperature points pooled per run) | PISA / thermal-proteome study: the deposit protocol pools the 16 temperature points (43–59 °C) of each gradient into a single TMT16-labelled sample that is then fractionated into the 12 deposited `.raw` (a24572–a24583). The SDRF keeps one row per `.raw`, all labelled only with the reagent `TMT16plex` and **no reporter channel**. The paper (Proteomics 2022; PMID 36082775, DOI 10.1002/pmic.202100254) states the per-experiment layout only in prose/figures (E. coli: 4×PISA + 4×abundance per growth phase; Hek293T: 5×PISA + 3×abundance) with no channel-number→temperature/condition table, and the accessions it cites in Data Availability (PXD031756, PXD031754) are not in PRIDE, so no per-file channel→sample map is recoverable |
| IPX0005271000 | TMT10plex, colon cancer (proteome/phospho) | iProX-hosted, renamed from PXD038081. One row per acquisition (`0709-TMT2-N.raw` …): intrinsically label runs are pool-level `MMDD-TMTk-n` injection names that match the paper's CRC-Proteome batch numbering (PRO-1,2,3,4,6,…,19) and its 15 high-pH fractions, but the SDRF's 270 TMT rows carry `comment[label] = TMT` with **no reporter channel**. The paper (MCP 2023, PMID 36934880, DOI 10.1016/j.mcpro.2023.100532) gives per-batch TMT-126..131→sample maps in its supplementary `mmc1.xlsx`, keyed to clinical T#/N#/IS/NA IDs, but the iProX deposit is login-walled with no sample/design sheet tying a `.raw` to a specific channel, and the deposit's own label-free sample names (`ZR-P*`, `ZR-PHOS*`, `ZR1-18`, `CCY1/2`) do not appear in the paper. Which reporter carries which tissue/patient within each run is therefore not stated anywhere recoverable from the deposit |
| PXD030690 | iTRAQ 8-plex, 10 runs | The E. coli PeptideAtlas build (Jachmann et al., bioRxiv 2025.09.11.675345) lists PXD030690 as its only iTRAQ experiment, tagged `K12_DMP_0mg-80mg_itraq` (10 runs, Q Exactive, K-12): a two-condition (0 vs 80 mg/L dimethyl phthalate) comparison. Every `.raw` is annotated with the bare label `ITRAQ` and the iTRAQ8plex (`UNIMOD:730`) modification but collapses the multiplex to one row of identical "biological replicate 1" characteristics — a pooled iTRAQ run treated as one sample with no channel→sample map. Source: Chen et al., *Environ Sci Pollut Res* 30:13702 (2023), PMID 36136186; PRIDE project PXD030690 returns 404, so the channel map is not recoverable |
| PXD037434 | TMT, plex not resolvable (10 high-pH fractions of one pooled run) | PRIDE `sampleProcessingProtocol`: "labeled using Tandem Mass Tags (TMT)… Labeled peptides from different culture samples were mixed, and fractionated by High pH Reversed-Phase Peptide Fractionation Kit". The 10 `.raw` (P20210201029_F1..F10.raw / P20210101029_F5,F10.raw) fed one Proteome Discoverer result (`01029_F.msf`) and are slices of the pooled TMT run; the paper (Biotechnol Biofuels Bioprod 2023, PMC9854199) quantifies 5 conditions × 3 biological replicates = 15 samples (T7-d3, T7, T15, T15-LN, T25). Which reporter carries which condition is stated nowhere (no design table in the paper, its figures-only supplementary, or the deposit), and the plex is not resolvable (10 fractions vs the 15 described samples) |

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

## Moderate: SCIEX run deposited without its `.wiff`

Category: `wiff-scan-without-wiff`. A SCIEX run is written as a `.wiff` file plus a
`.wiff.scan` companion holding the scan data. The companion cannot be read without the
`.wiff`. In these deposits some runs have only the `.wiff.scan`, so the SDRF lists the
complete runs and leaves these out.

| Dataset | Runs without `.wiff` | `.wiff` in deposit | Example |
|---|---|---|---|
| PXD028310 | 42 | 125 | `PVJ11_R2.wiff.scan`: every `PVJ*_R2` run |
| PXD023168 | 6 | 184 | `20150516_ZT_IDA_059.wiff.scan` |
| PXD017052 | 5 | 3,322 | `EXP19072_2019v1ms068X1_A.wiff.scan` |
| PXD011198 | 1 | 126 | `171205_LDC_Hist_SWATH_blanco_14.wiff.scan` |
| PXD014800 | 1 | 316 | `RCB_SALSW_TB_E00193_V2.3.wiff.scan` |
| PXD028078 | 1 | 57 | `20200628_SWATH_LC172.wiff.scan` |
| PXD030354 | 1 | 88 | `IDA_PreIP_APP23_5.wiff.scan` |
| PXD030947 | 1 | 64 | `Bobby_masto_18bobby_masto_18_2_10.wiff.scan` |
| PXD032299 | 1 | 448 | `20200128_OvCa_Lemba_ECA_PosControl_2.wiff.scan` |
| PXD038003 | 1 | 72 | `Pool_neuron-derived_EVs_from_rheumatoid_arthritid_patients_1..wiff.scan` |
| PXD050920 | 1 | 58 | `200403DDA-HC8-5uL-150min-50msec.wiff.scan` |
| PXD061811 | 1 | 65 | `HippocampalProteomics_WT_uncond_2.wiff.scan` |

How this was checked: every `.wiff.scan` in the PRIDE Archive file listing
(`/pride/ws/archive/v3/projects/<PXD>/files/all`) was matched to a `.wiff` with the same
name, without the `.scan` suffix.

Resolution: the submitters deposit the missing `.wiff` files.

## Moderate: deposited SDRF is internally inconsistent

Category: `deposited-sdrf-inconsistent`. The SDRF was deposited by the submitter and is
kept as deposited. The deposit does not show which of the conflicting values is right.

| Dataset | Problem |
|---|---|
| PXD006439 | Sample 14 (2 rows) is cell line B16-F10 with disease `low metastatic potential`; the other 30 B16-F10 rows say `high metastatic potential`, and all B16-F1 rows say `low`. Either the cell line or the disease value is wrong for Sample 14. |

Resolution: confirm with the submitter.
