BLOCKED: TMT channel -> sample map of every PXD015438 run is not recoverable from public evidence.

Affected runs (9 of 9 deposited RAW):

- `20190905_KKL_Revision_Tg_Torin_F1.raw` ... `_F8.raw` (one TMT plex, 8 high-pH fractions;
  RAW header: Q Exactive HF, method `TMT10_190min(200min)_45000_Top20_35ce_1Th_HF.meth`)
- `20190822_KKL_CHX_revision_Test.raw` (one unfractionated TMT plex; RAW header: Orbitrap Fusion
  Lumos, method `mePROD_MS2_120(142)min`)

What the dataset is: Klann, Tascher & Muench 2020 (Mol Cell 77:913, doi:10.1016/j.molcel.2019.11.010,
PMID 31812349, PMC7033560) - revision data for mePROD, i.e. pulsed SILAC (Lys8/Arg10) read out by
**TMT multiplexing**. Each plex holds pulse-labelled (heavy Lys8/Arg10 pulse) treated/control
samples, a light, non-SILAC-labelled "baseline/noise" channel (Figure 1E legend: "the non-SILAC
labeled channel") and a fully heavy "booster" channel (cells grown two weeks in Arg10/Lys8 medium).
Samples are distinguished only by TMT channel. An SDRF therefore needs one row per (RAW, TMT
channel), with the sample and its SILAC state per channel, which needs the channel map.

No AHA (azidohomoalanine) labelling is described in the paper, and PRIDE lists only SILAC and TMT as
quantification methods; the "AHA" in the request does not apply to this dataset.

Why blocked:

- Neither the paper, its STAR Methods, nor the figure legends assign samples to TMT channels.
  Methods name three TMT kits (Thermo 90111 TMT10plex, A37724 TMT11-131C, 90061 TMT6plex) without
  per-experiment channel layouts.
- Supplementary Tables S1-S5 (mmc2-mmc6) give condition columns per replicate (e.g. Table S4:
  Baseline, DMSO_9h x2, DMSO_2.5h x2, Torin1_9h x2, Tg_2.5h x2, Boost) but no channel names. The
  only channel name anywhere is the booster of Table S1 (`Abundance: F1: 131C, Sample`; Table S1 is
  the Figure 3 UPR experiment, presumably the ERStress runs of PXD014377) and it carries Proteome
  Discoverer's generic `Sample` label.
- It is not stated which figure the `Revision_Tg_Torin` plex belongs to. Figure 5 (Table S4:
  DMSO/Torin1 9 h, DMSO/Tg 2.5 h, n = 2) was fractionated into 24 fractions per its panel A, while
  this deposit has 8, and its RAW method uses a 190 min gradient against Figure 5A's 24 x 120 min.
  Table S4 does have exactly 10 columns (Baseline, 8 samples, Boost), matching a TMT10 plex, so
  Figure 5 cannot be excluded either (PXD014377's `20190110_KKL_MePROD_TORIN1_02_F1..F24` fits Figure 5's 24
  fractions better); Figure 6A/B (DMSO x2, Tg 0.25/1/6 uM, Torin1 0.75/2 uM = 7 samples) has no
  supplementary table and does not fit 10 channels one-to-one either. Sample identities of the plex
  are therefore also uncertain, not only their channels.
- The CHX test plex is presumably the cycloheximide titration of Figure 2I, inferred from the file
  name only (its PD study is named `190823_Revision_Chx_Torin`). No concentration per channel is
  stated in the text; concentrations appear only as figure axis values, with no channel assignment.
- The deposited Proteome Discoverer search files hold no map either. In
  `20190822_KKL_CHX_revision_Test-1.msf` (1.1 GB, downloaded and opened), the embedded study
  definition (`190823_Revision_Chx_Torin`) names the 11 channels only generically
  (`20190822_KKL_CHX_revision_Test - [126]` ... `[131C]`, Sample Type `Sample`, no factor values).
  In `20190905_KKL_Revision_Tg_Torin_F.msf` (10 GB; its first 4 MiB, which hold the study
  definition, were read by HTTP range request) the study `190906_KKL_Revision_final` uses PD method
  `TMT10_CM_Beta` and names the 10 channels only as `20190905_KKL_Revision_Tg_Torin_F - [126]` ...
  `[131]`, Sample Type `Sample`, with empty factor values.
- Ordering the supplementary columns onto TMT channels (Baseline = 126 ... Boost = 131) would be an
  assumption, not evidence; it is not done here.

Unblock: an author statement, a PD `.pdStudy` / study-design export, or a sample sheet that names
the sample (condition, dose, time, replicate, baseline, booster) for each TMT channel of
`Revision_Tg_Torin` and `CHX_revision_Test`. Do not infer the map from supplementary column order or
from reporter intensities.

Sister dataset: PXD014377 (same paper; the paper's Data Availability lists both accessions). Its 8
SILAC-only RAW files are being contributed separately (`datasets/PXD014377/`, separate pull
request); its TMT mePROD runs have the same blocker.

No SDRF is provided here for these runs. Checked: 2026-11-22.
