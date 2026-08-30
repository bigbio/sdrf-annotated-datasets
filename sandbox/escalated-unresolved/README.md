# Escalated easy-targets — unresolved (sandbox)

Skeleton SDRFs copied from the annotation pipeline. Biology columns remain `FILL:`
because no public run-to-condition mapping exists. See per-accession `BRIEF.md`
and blockers below.

- **PXD002306** — no generating publication is attached to this deposit (the 2021 Sci Rep prostate SWATH paper uses PXD027558), and the 313 files mix individual SWATH runs with 24-fraction pools without a public sample-to-subtype key.
- **PXD005077** — runs map to seven heterogeneous sick sheep plus pooled sick/healthy controls, but Additional file 1 diagnoses are not named in the paper, so a single disease factor would be hollow.
- **PXD003179** — all 21 runs are technical DIA/DDA window-size variants of one HeLa digest, so no biological factor discriminates among rows.
- **PXD003579** — the 10 SwathL files are technical injections of a single pooled seminal-plasma spectral library, not the ejaculate-portion comparison described in the paper.
- **PXD006102** — iTRAQ 8-plex labelled and split into 12 fractions; the one-row-per-run skeleton cannot represent multiplex channels.
- **PXD006550** — only two peak lists (HMW and LMW processing fractions) were deposited, so individual follicular-fluid donors cannot be mapped and HMW/LMW is not an allowed biological factor.
- **PXD007134** — filenames carry numeric sample IDs with no public table mapping them to heart-failure versus healthy (or NYHA class).
- **PXD001112** — 118 peak lists are numbered 1–118 with no public key to the five altitude sites (4350–5200 m).
- **PXD004108** — iTRAQ 8-plex liver-regeneration samples plus well-like file IDs; the one-row-per-run skeleton cannot represent multiplex channels.
- **PXD004642** — MUP_01–31 are individual mouse urine files with no public map to standard versus semi-natural housing.
- **PXD007038** — 189 files are SEC fractions of one HEK293 lysate; fraction identity is not a biological factor.
- **PXD007038** — SEC-fractionated (the deposit's own annotation file carries fraction_hplc and fraction_number columns), so the one-row-per-run DIA skeleton misrepresents it: every row hardcodes fraction identifier 1, and each biological sample spans many consecutive fractions that must share a source name.
- **PXD012044** — run names carry only injection numbers and internal case IDs (Inject002_SampleID_1-050115-20); A_SAMPLE_LIST.xlsx maps injections to ear tags but not to any experimental group, so no factor can be assigned without the unpublished animal table.
- **PXD008073** — files are HPLC/MARS fractions of one pooled follicular-fluid sample (HMW vs LMW processing); fraction identity is not an allowed biological factor.
- **PXD009223** — ten Run001–010 SWATH files of mrps-5/fzo-1/drp-1/eat-3 RNAi worms with no public table mapping run number to RNAi target.
- **PXD009619** — SWATH files are labelled with heifer IDs (P46–P64) and the paper does not publish which animals are pre- versus post-pubertal.
- **PXD010597** — six Lo_1/2/3 injections are technical pairs from one labelled-niche experiment; the paper’s niche-versus-distant comparison is not encoded in the files.
- **PXD013341** — ten SWATH files are labelled with mouse IDs (1191–1204) and the paper does not map them to K3 versus wild-type.
- **PXD017052** — 3436 files are internal nanoparticle-experiment IDs with no public map to NSCLC versus control or particle type.
- **PXD019334** — SWATH files carry internal sample numbers (1, 3, 6, …) with no public map to malignant versus benign breast tissue.
- **PXD019600** — TMT 9-plex plus concatenated bRPLC fractions of an EMT time course; the one-row-per-run skeleton cannot represent multiplex channels.
- **PXD020722** — 361 urine files are labelled sample10–sampleN with no public map to Parkinson’s versus control (or LRRK2/GBA status).
- **PXD021642** — 93 ATAG_02–94 files are sequential case IDs with no public map to monoamine-metabolism defect versus control.
- **PXD023297** — 30 files are numbered w-1–w-30 with no public map to tau-injected versus control brain.
- **PXD023316** — 75 files are well-like IDs (1-1 … 9-15) with no public map to T2D mild-cognitive-impairment versus control.
- **PXD025092** — S01–S44 are sequential biopsy IDs with no public map to HFpEF versus control.
- **PXD026228** — nine files cluster as J31–J33 / J41–J43 / J51–J53 matching n=3 at days 0, 3 and 5, but the paper does not state which J-group is which day.
- **PXD026491** — CSF files are numbered sample_1–114 (plus a second cohort) with no public map to Parkinson’s versus control.
- **PXD014800** — 316 raw files carry internal plate/run identifiers with no public sample-to-condition table in PRIDE or the generating publication.
- **PXD019902** — only one rapamycin dose-response run was deposited, so no factor can discriminate among rows.
- **PXD023077** — twelve DIA files share rep1-only filenames with no publication and no public map of runs to MDV versus OMM enrichments described in the PRIDE protocol.
- **PXD025752** — 307 runs use sequential internal IDs with no public map to the study’s experimental groups.
- **PXD027250** — eleven bML-labelled cell-culture files have no attached publication and no metadata mapping samples to JAK2 V617F status or drug treatments.
