# PXD003724 SDRF annotation report

## Study
"Potential salivary biomarkers with diabetic retinopathy, part 2" (PRIDE/ProteomeXchange, submitter Mun Fai Loke, NUS / University of Malaya). This is part 2 of 3 sister deposits (PXD003724 and PXD003723, PXD003725). All three are covered by one paper: Chee CS, Chang KM, Loke MF, Loo VPA, Subrayan V. *Association of potential salivary biomarkers with diabetic retinopathy and its severity in type-2 diabetes mellitus: a proteomic analysis by mass spectrometry.* PeerJ 2016;4:e2022, doi:10.7717/peerj.2022, PMC4893325. The paper's data statement cites PXD003723-PXD003725, so the paper link is verified. The PX record itself still says "publication pending".

Design: saliva from 45 type-2 diabetes patients at the UMMC eye clinic, in 3 groups of 15: XDR (diabetes without retinopathy, the control), NPDR and PDR. The groups were labelled iTRAQ 8-plex 113/114/115 and run on an Orbitrap Fusion with "3 technical replications".

## Scope, evidence and decisions
**Status: sandbox.** 3 rows x 41 columns: 1 RAW x 3 iTRAQ channels.

- **Deposited vs annotated.** The PX record (ProteomeCentral PROXI, full) lists 1 RAW (`iTRAQ8plex10ul_2.raw`), 1 MGF (`iTRAQ8plex10ul_2.mgf`) and 1 mzid (`peptides_1_1_0_2.mzid`). The campaign cache said "1 RAW / 3 files, Orbitrap Fusion", which this confirms. The RAW is annotated with 3 rows (113/114/115). The MGF and mzid are a peak list and search output, not runs. The PRIDE v3 `files/all` API and the PRIDE FTP over https were both unreachable (upstream connect error / timeout), so the file list comes from PROXI only.
- **Channel map (STATED, paper Methods):** XDR, NPDR and PDR peptides were labelled with tags 113-115 respectively; ratios were 114/113 and 115/113. Channels 116-121 of the 8-plex kit are not mentioned and are not annotated. With this map, the single multiplexed RAW is annotatable, not blocked.
- **Run -> technical replicate (INFERRED):** the paper reports 3 technical replications. The three sister deposits each hold one RAW, suffixed `_1`, `_2`, `_3`, so this file is annotated as `comment[technical replicate]` = 2. The paper does not say which deposit is which replicate, or whether the replicates were re-injections of one labelled mix or separate labellings. Source names are identical across the three PXDs so they can be merged.
- **Pooling (INFERRED):** 45 patients but only 3 reporter channels, so each channel must hold the saliva of a whole group, pooled before or after digestion. The paper does not describe pooling, the per-patient amount, or whether all 15 patients contributed. Encoded as `biological replicate` / `pooled sample` / `sample type` / `age` / `sex` / `individual` = `pooled`.
- **Disease:** XDR = `type 2 diabetes mellitus` (MONDO:0005148; diabetic with no retinopathy). NPDR = `non-proliferative diabetic retinopathy` (EFO:0009760). PDR = `proliferative diabetic retinopathy` (MONDO:0001660). `pre-existing condition` = `type 2 diabetes mellitus` on every row (all subjects are T2DM; clinical-metadata template). `factor value[disease]` copies disease.
- **Sample:** organism part `saliva` (UBERON:0001836; unstimulated, fasting, 9-10 am, 8000 g supernatant). Material type `organism part`. Developmental stage `adult` (all subjects >45 y).
- **Instrument:** Orbitrap Fusion (MS:1002416), the same in paper and PX record. The RAW header was NOT read (no download possible).
- **Protocol (STATED, paper):** TCEP reduction (10 mM, 60 C) and iodoacetamide alkylation (20 mM). Trypsin (porcine). HCD at 35% NCE. MS1 380-2000 m/z. DDA (top-speed; precursor z 2-7, dynamic exclusion 70 s). No fractionation (one 225-min gradient per run), so fraction identifier = 1.
- **Search modifications (paper, PD 1.4 SEQUEST):** Carbamidomethyl C fixed; Oxidation M, iTRAQ8plex K and iTRAQ8plex N-term **variable** (as the paper states, not the usual fixed). Tolerances 10 ppm / 0.02 Da. The deposited mzid was not readable (PRIDE down), so these are unverified against the search output.

## Values left not available / not applicable
- `cell type` = not applicable (cell-free body fluid).
- `ancestry category` = not applicable: each channel is a mixed-ancestry pool (Table 1, Malay/Indian/Chinese). The column does not allow `pooled`.
- `age`, `sex`, `individual` = pooled. Group means are in Table 1 (XDR 5M/10F, NPDR 7M/8F, PDR 8M/7F; mean age ~59-62 y), but per-channel composition is not stated.
- Omitted: fractionation method (none), enrichment/depletion (none described), ms2 scan range (not stated).

## Conflicts
- **PX modifications vs paper:** the PX record lists acetylated, monohydroxylated, iodoacetamide-derivatized and deamidated residues. The paper lists Carbamidomethyl + Oxidation + iTRAQ8plex (variable). The paper is used because it describes the search. The mzid, which would settle it, could not be read.
- PX record: publication pending, but the paper (2016) cites the PXDs. The paper abstract has a typo ("PX003725").
- PX titles of the three parts differ in wording ("Salivary biomarkers of diabetic retinopathy" vs "Potential salivary biomarkers with diabetic retinopathy" for part 2); the content is the same study.

## Stated vs INFERRED
Stated: channel -> group map, disease groups, 3 technical replicates, instrument, enzyme, reagents, HCD/NCE, MS1 range, tolerances, modifications.
INFERRED: (1) each channel is a pool of its group's patients; (2) deposit part 2 = technical replicate 2; (3) the same 113/114/115 layout in all three runs (not separately stated per run); (4) DDA.

## Reviewer, attack hardest
1. The pooled-group interpretation: the paper never says "pooled".
2. Part-number = technical-replicate mapping, and whether the parts are re-injections of one mix (then the SDRFs should be one file) or independent labellings.
3. Modifications from paper prose vs the PX list (acetyl, hydroxyl, deamidation; no phospho here): the mzid was unread.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` with `--template` ms-proteomics, human and clinical-metadata (each run separately): "Everything seems to be fine", no errors or warnings. Ontology validation was NOT run by the tool (OLS extras not installed). Terms were checked live instead: OLS4 search (EFO:0009760, MONDO:0001660), ontobee (UBERON:0001836, MONDO:0005148, MS:1002416) and unimod.org (UNIMOD:730). MS:1000422, MS:1001251, UNIMOD:4/35, PRIDE:0000609/0000599/0000627 were reused from validated campaign files; EBI OLS was rate-limited/down for them. `sdrf_review.py`: [OK].

## Review status
pending
