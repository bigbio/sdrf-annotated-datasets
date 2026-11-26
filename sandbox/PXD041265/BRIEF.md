# PXD041265 SDRF annotation report

## Study
The regulatory roles of Ezh2 in response to lipopolysaccharide (LPS) in macrophages and mice with conditional Ezh2 deletion with LysM-Cre system (PRIDE/PX title).

Publication actually describing this dataset: Phuengmaung P, ... Makjaroen J, ... Leelahavanichkul A. "Less Severe Sepsis in Cecal Ligation and Puncture Models with and without Lipopolysaccharide in Mice with Conditional Ezh2-Deleted Macrophages (LysM-Cre System)". Int J Mol Sci 2023;24(10):8517, doi:10.3390/ijms24108517, PMID 37239864, PMCID PMC10218384. Its section 4.5 cites PXD041265 by accession.

## Status
**sandbox.** The SDRF validates and the channel → condition map is stated. Several material values are inferred or conflict between sources (see below).

## Scope, evidence and decisions
The SDRF has 375 rows (125 RAW × 3 dimethyl labels) and 38 columns. Templates: ms-proteomics, vertebrates, clinical-metadata. clinical-metadata is declared only to license `characteristics[genotype]`, and it adds no required columns.

- **Deposited vs annotated.** The PX record lists 268 files: 125 `.raw`, 125 `.mgf`, 17 PD `.msf` and `checksum.txt`. The `.raw` names were checked one by one against the PRIDE FTP `checksum.txt`:
  - `CM_Ezh2_KO_Set1-3_F1-5`: 15 runs
  - `CM_Ezh2_WT_Set1-6_F1-5`: 30 runs
  - `Cells_Ezh2_KO_Set1-3_F1-10`: 30 runs
  - `Cells_Ezh2_WT_Set1-5_F1-10`: 50 runs
  - All 125 RAW are annotated and none are excluded. The `.mgf` and `.msf` files are derived files and are not listed.
- **Design (STATED, paper 4.4/4.5).** Bone-marrow-derived macrophages (femur, L929-conditioned DMEM) come from Ezh2 control (Ezh2 fl/fl; LysM-Cre -/-) or Ezh2 null (Ezh2 fl/fl; LysM-Cre cre/-) littermates. Three protocols were used:
  - N/N: DMEM twice.
  - N/LPS: DMEM, then LPS 100 ng/mL 24 h later.
  - LPS/LPS: LPS 100 ng/mL twice.
- **Material split.** "Cells" files are the proteome (cell lysate, in-solution digestion). "CM" files are the secretome (culture medium concentrated on Amicon 3K, then in-solution digestion).
- **Label map (STATED).** N/N = light (CH2O/NaBH3CN) → DIMETHYL0. N/LPS = medium (CD2O/NaBH3CN) → DIMETHYL4. LPS/LPS = heavy (13CD2O/NaBD3CN) → DIMETHYL8. The same map applies to proteome and secretome.
- **Genotype.** WT/KO in the file names = Ezh2 control/null. This is INFERRED from the naming, but it is unambiguous.
- **Fractionation and search.** Pooled peptides were fractionated with the Thermo high-pH reversed-phase kit: 10 fractions for Cells, 5 for CM. The fraction identifier comes from the file-name `F` number. The paper's PD/Percolator search used:
  - Fixed: carbamidomethyl C, plus light/medium/heavy dimethyl on N-term and K (+28.031300 / +32.056407 / +36.075670).
  - Variable: oxidation M.
  - Each row carries the dimethyl modification of its own channel (UNIMOD:36 / 199 / 330), checked against unimod.org masses.
- **Biological replicate = Set number** within genotype × compartment (INFERRED). Source names: `<genotype>_BMDM_set<N>_<condition>_<cells|medium>` (51 sources). Cells SetN and CM SetN are not linked as the same culture, because nothing states that they are.
- **Instrument.** The paper says "Q-Exactive Orbitrap Plus" (EASY-nLC1000); the PX record says Q Exactive (MS:1001911). The paper Methods are used (Q Exactive Plus, MS:1002634) by the precedence rule. RAW headers could not be read because the shell has no internet, so this remains unresolved.
- **Accession checks.** EBI OLS4 and the PRIDE v3 API were down. Accessions were checked live via unimod.org, the GitHub psi-ms.obo (4.2.18) and pride_cv.obo (2026-11-23), and ontobee (CL:0000235, UBERON:0002371, PATO:0000461). Evidence is in `/home/claude/bangkok3/scratch/PXD041265/`.

## Stated vs INFERRED
- **STATED:** organism, BMDM, genotypes, the three protocols and the LPS dose, the label → condition map, proteome/secretome split, hpHRP fractionation, fixed/variable modifications, and Q Exactive Plus (paper).
- **INFERRED:**
  - **Trypsin.** The paper says only "in-solution digestion", so the enzyme is unstated. The cleavage agent column does not allow `not available`.
  - **HCD.** Fragmentation is not stated; it is the only fragmentation mode on a Q Exactive.
  - **DDA.** Acquisition mode is not stated; DDA is implied by the PD/Percolator workflow.
  - **Set = biological replicate.** The paper says "Macrophages were isolated from 3 different mice for the triplicate analysis", yet Cells WT has 5 sets and CM WT has 6. Which WT sets entered the published triplicates is unknown, so all are annotated as replicates 1–5/1–6.
  - **material type `cell` for the CM (secretome) rows.** The fixed vocabulary has no secretome/medium value. The compartment is carried in the source name (`_medium`) and the file name (`CM_`).

## Values left not available / not applicable
- `not available`:
  - developmental stage, sex and strain or breed: the age, sex and background of the transgenic BMDM donors are not stated. The 8-week C57BL/6 male mice in 4.1 are the separately purchased WT mice used for other experiments.
  - precursor/fragment mass tolerance, reduction reagent, alkylation reagent: not stated (the paper defers to refs 35/56/104). Carbamidomethyl-C is fixed in the stated search, so alkylation happened but the reagent is unknown.
- `normal` for disease: these are non-diseased mice. LPS exposure is the treatment, not a disease.
- No collision energy or scan-range columns were emitted because the values are unstated.

## Conflicts
1. **PX publication link is wrong.** The PX record links PMID 37373325 / 10.3390/ijms241210175 (Sae-Khow et al. 2023, an *mgmt*-deletion paper), and its description reuses the abstract of PMC10049283. PMC10049283 (IJMS 24(6):5363) has the same title as the PX record but contains no proteomics and no PXD mention. The data are from PMC10218384, which cites PXD041265 in 4.5.
2. **Instrument:** PX says Q Exactive; the paper says Q Exactive Plus (see above).
3. **PX `modifications`** says "No PTMs are included"; the paper lists carbamidomethyl, dimethyl ×3 and oxidation. The paper is used.

## Not done / what would upgrade to annotated
- RAW header read: an HTTP-range read of any `.raw` would settle the instrument.
- Deposited PD `.msf` read: a SQLite range read would give enzyme, tolerances, the modification list and the set ↔ replicate grouping. There was no internet from the shell, so neither could be done.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` was run once each with `--template ms-proteomics`, `vertebrates` and `clinical-metadata`. All three report "Everything seems to be fine." The ontology checks were skipped because the OLS dependencies are not installed, so this is a structural pass only. Factor value columns (genotype, treatment) are last.

## Review status
pending
