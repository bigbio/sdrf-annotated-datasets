# PXD015512 SDRF annotation report

## Study
Different osteogenic differentiation behavior of canine mesenchymal stem cells derived from bone marrow and dental pulp: the proteomics profile.
Publication: Nantavisai S et al., "Systems biology analysis of osteogenic differentiation behavior by canine mesenchymal stem cells derived from bone marrow and dental pulp", Sci Rep 2020;10:20703, doi:10.1038/s41598-020-77656-0, PMID 33244029, PMCID PMC7692528. The full Methods were read on the PMC HTML page.

## Scope, evidence and decisions
Status: **sandbox**. 270 rows (90 RAW x 3 dimethyl labels) x 37 columns. Templates: ms-proteomics v1.1.0 and vertebrates v1.1.0.

**Deposited vs annotated.** The ProteomeCentral PROXI record (Page URL and JSON checked for PXD015512) lists 200 files:
- 90 `.raw` and 90 `.mgf` with the same stems;
- 10 `.pdResult` and 10 `.msf`, one per set.

The 90 RAW files are `Bone_Set{1,3,4,5}_F1-F9`, `bone_Set2_F1-F9` (lower-case b in the deposit) and `Pulp_Set{1-5}_F1-F9`. Some names carry instrument timestamps: `Pulp_Set4_F*_1806xxxxxxxx` and `Pulp_Set5_F7_180606143457`. All 90 RAW files are annotated and none are excluded. The `.mgf`, `.msf` and `.pdResult` files are processed outputs and do not appear in the SDRF. The PRIDE v3 API was down ("upstream connect error"), so the file list comes from PROXI only. The cached count of 90 RAW / 200 files matches.

**Design (STATED, paper Methods).**
- Five healthy dogs per cell type, aged 3-10 years. Bone marrow and dental pulp came from different dogs.
- Cells were used at passage 2-5. cBM-MSCs came from bone-marrow aspirate; cDPSCs came from pulp-tissue explants.
- Osteogenic medium was ascorbic acid, dexamethasone and beta-glycerophosphate, for up to 14 days. Cells in growth medium were the undifferentiated control (day 0).
- Label map, quoted verbatim: "control group ... and osteogenic induction groups ... at day 7 and 14 were labeled with ... light ..., medium ..., and heavy ..., respectively". So day 0 = DIMETHYL0 (light), day 7 = DIMETHYL4 (medium, formaldehyde-d2 + NaBH3CN), day 14 = DIMETHYL8 (heavy, 13CD2O + NaBD3CN). "Three labeled-peptide samples were mixed", then fractionated with the Pierce high-pH RP kit.
- "Five biological replicates were used for analyzing of proteomics data."

**Mapping.**
- Each deposited set is one triplex (day 0/7/14) from one dog of one cell type.
- `Set N` -> `characteristics[biological replicate]` = N. Source names are `cBM-MSC_dogN_dayX` / `cDPSC_dogN_dayX`. The prefix keeps them distinct because the dogs differ by cell type.
- `F1-F9` -> `comment[fraction identifier]` 1-9.

**Instrument and search.**
- LC-MS: EASY-nLC1000; MS1 at 70,000 and MS2 at 17,500; 350-1400 m/z (`comment[ms1 scan range]`).
- Search: PD 2.1, trypsin, 2 missed cleavages, Carbamidomethyl C fixed (UNIMOD:4), Oxidation M variable (UNIMOD:35).
- Dimethyl N-term/K at +28.0313 / +32.056407 / +36.07567 Da maps to UNIMOD:36 / 199 / 330. These masses were checked live on unimod.org for 199 and 330, and in the bundled unimod.xml for all three. Each label row carries its own channel's dimethyl mod as `Fixed` on K and `PP=Any N-term`, as in the same lab's PXD046383/PXD034530 files.
- Reduction: TCEP (PRIDE:0000609). Alkylation: IAA (PRIDE:0000599).

**Ontology checks.** OLS4 was down all session (EBI upstream error; WebFetch was also rate-limited), so terms were checked live on Ontobee, the PRIDE CV obo (GitHub) and unimod.org:
- CL:0002540 mesenchymal stem cell of the bone marrow; CL:4030035 dental pulp stem cell (definition checked: "dental pulp cell that possesses stem-cell-like qualities").
- UBERON:0002371 bone marrow; UBERON:0001754 dental pulp.
- MS:1002634 Q Exactive Plus (and MS:1001911 Q Exactive); MS:1000422 HCD; MS:1001251 Trypsin.
- PRIDE:0000564 hpHRP; 0000599 IAA; 0000609 TCEP; 0000627 DDA.
- NCBITaxon 9615 comes from the PX record.

**Factors.** `factor value[cell type]` (BM-MSC vs DPSC) and `factor value[treatment]` (day 0 control / 7 d / 14 d osteogenic induction). These two columns are last.

## Values left not available / not applicable
- `characteristics[sex]`, `characteristics[strain or breed]`: **not available**. The paper does not report them.
- `comment[precursor mass tolerance]`, `comment[fragment mass tolerance]`: **not available**. They are not reported, and the `.msf` could not be read (see below).
- Collision energy, database and FDR are not reported, so those columns are omitted.

## Stated vs INFERRED
- STATED: the label-to-timepoint order ("respectively"), the cell types and sources, 5 biological replicates, the fractionation kit, PD 2.1 parameters, the reagents, MS1 range and the resolutions.
- INFERRED:
  - (1) `Set N` = dog N = biological replicate N. Five sets per cell type match "five dogs" and "five biological replicates", but no table names the dogs.
  - (2) Instrument = Q Exactive Plus (see conflicts).
  - (3) DDA acquisition, and HCD from the Q Exactive platform; neither is stated.
  - (4) `developmental stage` = adult, from age 3-10 years.
  - (5) Dimethyl labels as `MT=Fixed`. The paper lists dimethyl between "fixed modification" and "variable modifications" without saying which.
  - (6) Fraction ids 1-9 for 9 deposited fractions, while the paper says "10 fractions". F10 is either not deposited or was not acquired.

## Conflicts
- **Instrument:** the PX/PRIDE record says Q Exactive (MS:1001911). The paper Methods say "Q-Exactive Orbitrap Plus". The shell has no internet (proxy 403), so the RAW header could not be range-read. By the precedence rule (paper Methods > PX record), Q Exactive Plus (MS:1002634) is annotated. Other RAW headers from the same Chulalongkorn core (PXD034530, PXD046383) read Q Exactive Plus, which supports this circumstantially. **This is the main reason for sandbox status.**
- **Modifications:** the PX record lists "acetylated residue" (MOD:00394), "monohydroxylated residue" and "iodoacetamide derivatized residue". The last two match Oxidation and Carbamidomethyl. Acetylation is not in the paper. Its residue/position and fixed/variable status could not be checked against the deposited PD `.msf` (no shell network; the browser cannot range-read SQLite). It is therefore **omitted** rather than guessed; a reviewer with network access should read `Bone_Set1_F.msf` (Workflows node) and add it if it is a search parameter.
- Methods list alkylation (IAA) before reduction (TCEP). Both reagents are annotated as stated.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only`, run with no template, with `--template ms-proteomics` and with `--template vertebrates`: "Everything seems to be fine" each time (exit 0). The OLS ontology layer is unavailable in this environment (dependency missing), so this is **structural validation only**. The accessions were checked by hand as listed above.

## Evidence files
`/home/claude/bangkok3/scratch/PXD015512/`: `proxi_summary.txt`, `raw_files.txt`, `all_files.txt`, `paper_methods_PMC7692528.txt`, `scripts/build_PXD015512.py`.

## Review status
pending
