# PXD019239 SDRF annotation report

## Study
STING mediates lupus via the activation of conventional dendritic cell maturation and plasmacytoid dendritic cell differentiation. Mouse bone-marrow-derived dendritic cells (BMDC) from WT, Fcgr2b-/- (lupus-prone) and Fcgr2b-/-.Sting gt/gt mice.

Thim-uam A et al., iScience 2020;23(9):101530. DOI 10.1016/j.isci.2020.101530, PMID 33083760, PMC7502826. The PX record still says "publication pending", but the paper's Transparent Methods name PXD019239. The correction (PMC7644739) only fixes an author name. For the proteomics, the Methods cite Makjaroen et al., Mol Cell Proteomics 2018;17:2197 (PMC6210224) as the dimethyl method.

**Status: sandbox.** All 77 RAW files are mapped from stated design and file names. Two things are open:
- The medium channel genotype conflicts between the Methods and the Figure 5I legend.
- For both arms, the search and acquisition parameters are inferred: from the cited 2018 paper for the dimethyl arm, and from the PX modification list for the co-IP arm.

## Scope, evidence and decisions
The SDRF has 149 rows x 41 columns, in two experimental arms.

**Deposited files** (ProteomeCentral PROXI, Page URL checked for PXD019239): 199 files, matching the campaign cache.
- 77 RAW, 77 mgf (one per RAW) and 45 pdResult. The pdResult files are `ArtySet1F`-`ArtySet4F` plus one per gel RAW.
- PRIDE v3 and Europe PMC supplementaryFiles both returned "upstream connect error".

**Deposited vs annotated:** 77/77 RAW annotated, none excluded. The mgf and pdResult files are derived files and get no rows. The gel grid {wt,R2KO} x {0,3,6} h x 7 bands would have 42 runs, but only 41 are deposited: `R2KO-6-30KD` is absent as raw, mgf and pdResult. Nothing is invented for it.

### Arm A: whole-proteome triplex dimethyl (36 RAW x 3 labels = 108 rows)
Files are `ArtySet{1-4}F{1-9}.raw`.
- **Design (STATED, Transparent Methods "Sample preparation for MS analysis"):**
  - BMDC were stimulated with 10 ug/mL DMXAA for 24 h, 300 ug protein per group, trypsin 1:50.
  - Peptides from "WT mice, Fcgr2b-/- mice, and Fcgr2b-/-.Sting gt/gt mice" were labelled light, medium and heavy, "respectively".
  - The heavy reagent is 13C-D2 formaldehyde + cyanoborodeuteride, so +36.0757 = UNIMOD:330, not 510.
  - Ratios are taken against WT "across all four biological replicates".
- **Mapping:**
  - ArtySet k = biological replicate k (4 sets = 4 stated replicates; the 1:1 match is INFERRED from the counts).
  - F1-F9 = fraction identifier.
  - Labels: DIMETHYL0 = WT, DIMETHYL4 = Fcgr2b-/-, DIMETHYL8 = Fcgr2b-/- Sting gt/gt.
- **Developmental stage:** adult. The Figure 5 legend says bone marrow came from 6-month-old mice. The vertebrates template has no age column, so the age is noted here only.
- **Parameters INFERRED from Makjaroen 2018** (the Methods say "using a dimethyl labeling method (Makjaroen et al., 2018)" and "The peptides were fractionated and subjected to LC-MS/MS (Thermo)"):
  - DTT/IAA; hpHRP fractionation (the 2018 paper used the Pierce kit with 10 fractions; 9 are deposited here).
  - HCD at 32% NCE; MS1 range 350-1400 m/z; 10 ppm / 0.02 Da.
  - Fixed: carbamidomethyl C and per-channel dimethyl on K and any N-term. Variable: oxidation M.
- **PX modification list:** MOD:00397 iodoacetamide derivatized and MOD:00425 monohydroxylated. This agrees with the above and lists no acetyl, so unlike PXD018652 no acetyl modification was added.

### Arm B: STING co-IP, SDS-PAGE gel bands, label-free (41 rows)
Files are `{wt,R2KO}-{0,3,6}-{30..100}kd.raw`.
- **Design:**
  - STATED (PX description + Methods "Immunoprecipitation of STING-interacting proteins"): DMXAA-stimulated BMDC; STING antibody (CUSB clone GTN-01) on Protein A SureBeads; 10% SDS-PAGE; in-gel digestion.
  - File names give genotype, time and band.
  - `R2KO` = Fcgr2b-/- (FcgammaRIIb). This is INFERRED from the name, but it is the only knockout besides Sting gt/gt in the PX description, and the PX description lists 3 and 6 h DMXAA.
  - 0 h is annotated as unstimulated ("no DMXAA (0 h)"). That is INFERRED.
- **Bands:** the 30/37/40/50/70/90/100 kDa bands are mapped to fraction identifiers 1-7 in ascending molecular weight. Reading the numbers as gel-slice marker positions is INFERRED.
- **Other values:**
  - `characteristics[enrichment process]` = immunoprecipitation (CHMO:0001691, in the PRIDE ontology index); arm A is `not applicable`.
  - Fractionation method = SDS PAGE (PRIDE:0000568).
  - Biological replicate = 1 (one IP per genotype x time).
- **Search parameters:** Trypsin is INFERRED because the column cannot be `not available`, and the Methods only say "in-gel digestion". Carbamidomethyl C (fixed) and oxidation M (variable) come from the dataset-level PX modification list; the fixed/variable split is INFERRED. Alkylation = IAA, from the same PX entry.

### Common to both arms
- Mus musculus; bone marrow (UBERON:0002371); dendritic cell (CL:0000451; BMDC from IL-4 + GM-CSF culture for 5 days); material type cell.
- Instrument Q Exactive (MS:1001911, the PX record); DDA; HCD.
- **Genotype:** `characteristics[genotype]` + `factor value[genotype]`, licensed by declaring clinical-metadata. The second factor is `factor value[treatment]` (DMXAA time).
- **Strain:** Fcgr2b lines are "129/C57BL/6" (Methods: Fcgr2b-deficient mice on the 129/C57BL/6 background, crossed with Sting-deficient mice). WT mice were bought from the National Laboratory Animal Center, Thailand, with the strain unstated, so their value is `not available`.
- **Disease:** WT = normal (PATO:0000461). Fcgr2b-/- and the double mutant = systemic lupus erythematosus (MONDO:0007915), as the lupus model the study is about.

## Values left not available / not applicable
- `characteristics[sex]`: not available for all rows; not stated anywhere.
- `characteristics[strain or breed]`: not available for WT (source given, strain not).
- `characteristics[developmental stage]`: not available for arm B; the age of the co-IP donors is not stated.
- **Arm B parameters not available:** collision energy, precursor and fragment tolerance, reduction reagent and MS1 range. No source covers the co-IP acquisition or search, and the pdResult files could not be read.
- **Not applicable:**
  - The two dimethyl modification columns on arm B (label-free).
  - Enrichment process on arm A.

## Conflicts and open points (why sandbox)
1. **Medium channel genotype.** The Methods say the medium channel is "Fcgr2b-/- mice". The Figure 5I legend says the comparison is Fcgr2b-/-.Sting wt/gt vs Fcgr2b-/-.Sting gt/gt (N = 4). The medium donors may therefore be Sting-heterozygous littermates. I followed the Methods, which give the explicit label assignment. If the legend is right, the DIMETHYL4 genotype should read "Fcgr2b-/- Sting wt/gt".
2. **Instrument.** The PX record says Q Exactive. The cited 2018 protocol used a "Q-Exactive Orbitrap Plus". The 2020 paper only says "(Thermo)". The RAW headers could not be read (no shell network; the browser cannot range-read). I kept the deposit's declaration; this is unresolved, and the same issue applies to sibling PXD018652.
3. **Arm A parameters come from another paper.** They are taken from Makjaroen 2018 via citation. The deposited `ArtySet*F.pdResult` files would settle them but could not be read.
4. **Arm B parameters.** The enzyme, the modification fixed/variable split and the alkylation reagent are inferred. The band-to-fraction meaning is inferred.
5. **Disease for the double mutant.** Sting deficiency attenuates lupus in Fcgr2b-/- mice, which is the paper's thesis. Labelling Fcgr2b-/- Sting gt/gt donors "systemic lupus erythematosus" describes the model background, not a measured phenotype of those donors.
6. **Genotype discrepancy in arm B.** The Methods say the co-IP used WT, Fcgr2b-/- and Sting gt/gt BMDC at 3 h. The deposit holds only WT and R2KO at 0/3/6 h, so no Sting gt/gt IP runs were deposited.

## Term verification
Every accession was checked live on 2026-11-25. OLS4 rate-limited after one call, so I used other sources:
- ontobee for CL:0000451, UBERON:0002371, MONDO:0007915, PATO:0000461, MS:1001911/1002038/1001251/1000422 and NCBITaxon:10090
- unimod.org for UNIMOD 4/35/36/199/330
- GitHub `pride_cv.obo` for PRIDE:0000627/0000564/0000608/0000599/0000568/0000848/0000850/0000852
- OLS4 for CHMO:0001691

Evidence and the build script are in `/home/claude/bangkok3/scratch/PXD019239/`.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` passes with no errors for each of ms-proteomics, vertebrates and clinical-metadata, and with no template. Only structural validation ran: the OLS extras are not installed.

## Review status
pending
