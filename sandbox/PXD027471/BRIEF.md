# PXD027471 SDRF annotation report

## Study
Exploration on survived mice after sepsis and proteomic analysis on LPS-activated macrophages supports the regulation of sepsis hyper-inflammation by intravenous immunoglobulin (PX title). Published as Makjaroen J et al., "A Comparison Between 1 Day versus 7 Days of Sepsis in Mice with the Experiments on LPS-Activated Macrophages Support the Use of Intravenous Immunoglobulin for Sepsis Attenuation", J Inflamm Res 2021;14:7243-7263, DOI 10.2147/JIR.S338383, PMID 35221705, PMC8866997. Its Data Availability statement cites PXD027471.

**Publication conflict:** the PX/PRIDE record links PMID 35163596 (Thim-Uam et al., IJMS 2022, DSS colitis in splenectomy mice). That is a different paper by the same lab. The PX title and abstract match the JIR 2021 paper, and the JIR paper cites PXD027471, so the JIR paper was used.

## Scope, evidence and decisions
Status: **sandbox**. The file has 60 rows (30 RAW x 2 TMT channels) and 40 columns. Templates: ms-proteomics, vertebrates, cell-lines (all v1.1.0).

- **Deposited files:** 66 files from the PX `datasetFiles`: 30 `.raw`, 30 `.mgf`, 3 `.msf` and 3 `.pdResult` (`Aof_Asada_Repeat_Set{1,2,3}_F`). All 30 RAW files are annotated. The MGF files are peak lists and are not used as data files. The Set3 fraction 7 RAW is named `Aof_Asada_Repeat_Set3_F7_20190810211447.raw` and is annotated with that exact name as fraction 7.
- **Samples (stated):** RAW264.7 macrophages (ATCC). The paper says "Stimulated RAW246.7 cells after 24 h of LPS or LPS + sHA-Ig" (the "246.7" is a typo in the paper). The Fig 7 title confirms RAW264.7. Treatments ran 24 h: 100 ng/mL LPS (E. coli O26:B6, Sigma), alone or with 100 ug/mL soluble heat-aggregated mouse IgG (sHA-Ig). The proteomics has no untreated arm.
- **Channel map (stated):** the paper says "Peptides derived from cells stimulated with LPS plus sHA-Ig or LPS were labeled with 128 and 130 TMT reagent, respectively." The kit was the TMTsixplex set. Channels 126, 127, 129 and 131 are not mentioned and get no rows.
- **Biological replicates (stated):** the Fig 7 legend says "Set 1-3 are the triplication of the protein expression experiments". So SetN = biological replicate N, and each set is one TMT plex.
- **Fractions:** Pierce high-pH RP gave "20 fractions concatenated into 10". F1-F10 map to `comment[fraction identifier]` 1-10.
- **Sample prep:** 8 M urea / TEAB lysis; 10 mM DTT; 40 mM IAA; trypsin 1:50.
- **Acquisition:** EASY-nLC1000; Full MS 70k; top-10 DDA at 35k; HCD NCE 32%; scan range 200-2000 m/z.
- **Search (from paper Methods):** PD 2.1.1.21 against Mouse SwissProt. Precursor 10 ppm, fragment 0.02 Da. Fixed: carbamidomethyl C, plus TMT6plex on K and N-term. Variable: oxidation M. Up to 2 missed cleavages.
- **Cell line:** RAW 264.7 = CVCL_0493. Cellosaurus (checked live) gives Mus musculus, male, adult, BALB/c, macrophage (CL:0000235), mouse leukemia (NCIt C21604), derived from ascites. `organism part` = not applicable (cell line), consistent with PXD046383.

## Values left not applicable / not available
- `characteristics[organism part]` = not applicable: this is a cultured cell line, same convention as the reviewed PXD046383.
- No `not available` values were used.
- Columns not emitted because no source states them: missed-cleavage count (2), dynamic exclusion and MS2 resolution. They are not template-required.

## Stated vs INFERRED
- **Stated (paper):** cell line, treatments, TMT128 = LPS+sHA-Ig, TMT130 = LPS, Set1-3 = triplicate experiments, fractionation, reagents, enzyme, tolerances, mods, NCE and scan range.
- **INFERRED:**
  - Fraction numbers come from the file-name token F1-F10.
  - Donor-level traits (sex, age stage, strain, disease) come from Cellosaurus, not the paper.

## Conflicts / unresolved (reasons for sandbox)
1. **Instrument.** PX/PRIDE says Q Exactive (MS:1001911). The paper says "Q-Exactive Orbitrap Plus". Following the precedence rule (paper > PX field), the SDRF uses Q Exactive Plus (MS:1002634). The RAW headers were **not** read because the shell has no internet and the PRIDE FTP timed out in the browser. So this choice is not confirmed from the raw data. The same lab's PXD046383 and PXD034530 were Q Exactive Plus from the RAW header and protocol.
2. **Search and channel settings.** The deposited `.msf`/`.pdResult` files (PD StudyDefinition and Workflows) were **not** read for the same network reason. The modifications and the 128/130 channel map rest on paper Methods only.
3. **Mislinked publication.** As above, the PX record links PMID 35163596.

## Accession verification
Checked live on 2026-11-25:
- OLS: MS:1002634 Q Exactive Plus.
- Cellosaurus: CVCL_0493.
- UNIMOD: 737 TMT6plex, 4 Carbamidomethyl, 35 Oxidation.
- pride_cv.obo: PRIDE:0000564 hpHRP, 0000608 DTT, 0000599 IAA, 0000627 DDA.
- psi-ms.obo: MS:1000422 beam-type CID (HCD).

MS:1001251 (Trypsin) was not re-checked: OLS was rate-limited or returning upstream errors. It is carried over unchanged from the reviewed PXD046383.

Evidence files are in `/home/claude/bangkok3/scratch/PXD027471/`.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` was run once per template (ms-proteomics, vertebrates, cell-lines) and all three passed. The OLS dependencies are not installed, so this was **structural validation only**. The column set and reserved-word use are identical to the reviewed PXD046383.

## Judgement calls to attack
- Q Exactive Plus (paper) over Q Exactive (PX), with no RAW-header check.
- Only two of six TMT channels are annotated. If the `.msf` shows other channels carrying samples, rows are missing.
- Set = biological replicate. "Triplication of the experiments" could instead mean technical repeats of one culture.
- Paper used: J Inflamm Res 2021, DOI 10.2147/JIR.S338383, PMC8866997, not the PX-linked PMID 35163596.

## Review status
pending
