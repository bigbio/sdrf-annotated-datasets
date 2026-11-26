# PXD032795 SDRF annotation report

## Study
Synechocystis-Hik28 stress response. Kurdrid P, Yutthanasirikul R, Saree S, Senachak J, Saelee M, Hongsthong A. "Hik28-dependent and Hik28-independent ABC transporters were revealed by proteome-wide analysis of ΔHik28 under combined stress." BMC Mol Cell Biol 2022;23:27. doi:10.1186/s12860-022-00421-w, PMID 35794554, PMC9258054. The paper's Data Availability names PXD032795. The study compares the proteomes of *Synechocystis* sp. PCC 6803 wild type (WT) and a Hik28 (sll0474) deletion mutant (MT). Both strains were grown in normal or nitrogen-free BG-11, at 16, 30 or 45 °C, and sampled at 0, 1 and 24 h.

## Scope, evidence and decisions
**Status: sandbox.** 106 rows (one per deposited mzXML); 34 columns; templates ms-proteomics + clinical-metadata.

**What the deposit holds (PROXI full record, 212 files; also checked against the FTP directory listing):**
- 106 `.mzXML` files, listed as "Associated raw file".
- 106 Spectrum Mill `tagSummary_*.tsv` search outputs.
- No Agilent `.d` bundles and no archives. The campaign cache said "106 RAW, Agilent .d", which is wrong: only converted peak lists are deposited.

**What the mzXML header shows** (No1_6803_0h_1.mzXML, read directly):
- Instrument: msManufacturer Agilent, msModel **G6545A**, HPLC-Chip/MS, Q-TOF, MassHunter acquisition 5.0.
- Parent file: `C:\SpectrumMill\msdataSM\PLEK_01_WT_0h_1\No1_6803_0h_1.d`.
- Converter: Spectrum Mill `xtractorAgilent` 6.0.201.
- Contents: MS2 scans only, merged .pkl, activationMethod CID.

These are therefore Spectrum Mill-extracted peak lists, not vendor raw data. `comment[data file]` uses the deposited `.mzXML` names, following the campaign precedent for peak-list-only deposits (PXD031111, PXD054595). This is the main reason for the sandbox status (sdrf-skills invariant 9).

**Run → sample key.** The key was parsed deterministically from the file names; the build script asserts every name.
- `<date>_<WT|MT>[_0474]_<16|30|45>_<1h|24h>_<[N]b>_<i>`
  - `N` = nitrogen-free.
  - `b` = biological replicate.
  - `i` = injection.
  - The 0 h files carry no temperature and were taken at 30 °C, before the temperature shift.
- `NoK_<6803|0474>[_30]_<0h|1h>[_N]_<i>` = replicate 1 of the 0 h and 30 °C/1 h arms. Strain 6803 = WT and 0474 = sll0474 mutant.
- Self-consistency check: injection 1 of replicate 1 was acquired on 2021-01-12/13 and injection 2 on 2021-01-13/14. Replicate 2 was acquired on 2021-01-14/15. No (sample, injection) key occurs twice.

**Reconciliation.** The full design is 2 genotypes × [0 h ± N, plus 3 temperatures × 2 times × ± N] × 2 biological replicates × 2 injections = 112 runs. 106 are deposited, and all 106 are annotated. The 6 absent runs are all at 0 h:
- WT −N rep1 inj1.
- WT −N rep2, both injections.
- MT +N rep1 inj1.
- MT −N rep2, both injections.

The 106 tagSummary tsv files map one-to-one onto the mzXML conditions. The exception is `tagSummary_WT_1h_N1_1.tsv`, whose name lacks the temperature; by elimination it is 20210112_WT_45_1h_N1_1.

**Samples:** 54 source names (genotype × medium × temperature × time × biological replicate). Encoding:
- `characteristics[genotype]`: `wild type` / `sll0474 (hik28) deletion mutant`.
- `characteristics[treatment]`: medium + temperature, e.g. `nitrogen-free BG-11 medium at 45 degree Celsius`.
- `characteristics[sampling time]`: `0/1/24 hour`.
- All three are repeated as factor values, which are the last columns.

**Wet lab, acquisition and search** (paper Methods; the instrument is confirmed by the mzXML header):
- Reduction and alkylation: DTT, then 50 mM IAA.
- Digestion: trypsin 1:75, 37 °C, 16 h.
- LC-MS: Agilent 1260 HPLC-chip (ProtID-chip-150 II) + Agilent 6545 Q-TOF → MS:1002791 "6545 Q-TOF LC/MS". G6545A is the plain 6545, not 6545XT (MS:1003535).
- Acquisition: automatic MS/MS = DDA; MS/MS range 80–2000 m/z; CID (also in the mzXML header).
- Search: MassHunter B.06.01 / Spectrum Mill B.06.00.201HF1.
  - Carbamidomethyl C fixed.
  - Phospho S/T/Y variable (as stated).
  - Precursor ±20 ppm, product ±50 ppm, ≤2 missed cleavages.

The tagSummary files were not opened, so the search mods come from Methods and not from the deposited output.

**Inferred, not stated:**
1. **Replicate semantics.** The paper never states replicate numbers (it has no occurrence of "replicate"). That the file token `[N]b_i` means biological replicate b and injection i is inferred from the names and the acquisition dates.
2. **No-series replicate.** The `NoK_*` files were taken as biological replicate 1, because the dated files of the same arms carry replicate 2 only.
3. **0 h temperature.** The 0 h samples were assigned 30 °C, the pre-shift growth temperature stated in Methods.
4. **MT_0474 tokens.** `MT_0474_45` files were taken as MT 45 °C replicate 1, the same as `MT_45`.

**Conflicts:**
- The PX instrument field says only "Agilent MassHunter format" (a file format, not an instrument). The mzXML header and the paper agree on the 6545 Q-TOF, which was used.
- PX modifications say "No PTMs are included in the dataset", but the paper searched carbamidomethyl (fixed) and phospho (variable). The paper was followed.
- Methods "Protein preparation" mentions only 30 and 45 °C, yet 16 °C runs are deposited, and the paper itself reports 16 °C ("low temperature") results. All runs were annotated.
- The MS1 range is printed as "100-140 m/z", an evident typo, so `comment[ms1 scan range]` was omitted.

**Template choice.** `characteristics[genotype]` (WT vs ΔHik28, a primary factor) is licensed only by clinical-metadata, invertebrates and single-cell. clinical-metadata states it is "applicable to any organism", so it is declared solely to license genotype. A reviewer may prefer a different encoding.

**Values left as reserved words:**
- organism part, cell type and disease are `not applicable`: whole unicellular cyanobacterial cultures have no anatomy, cell-type ontology term or disease state.
- material type = `cell`, matching prior *Synechocystis* SDRFs in this collection.
- Collision energy was omitted: the mzXML shows rolling CE values of about 34–36 per scan, not a single setting.

**Accession checks.** EBI OLS4 returned upstream connection errors and rate limits today, so terms were checked against other sources (scratch `verify_terms.txt`):
- MS:1002791, MS:1000133, MS:1001251: psi-ms.obo 4.2.18 from GitHub.
- PRIDE:0000627/0608/0599: pride_cv.obo from GitHub.
- UNIMOD:4 and UNIMOD:21: bundled unimod.xml.
- NCBITaxon:1148 "Synechocystis sp. PCC 6803": NCBI eutils.

**Validation:** `parse_sdrf validate-sdrf --use_ols_cache_only`, run once with `--template ms-proteomics`, once with `--template clinical-metadata`, and once with no template. All three reported "Everything seems to be fine". OLS dependencies are not installed, so this is a structural pass only.

**To promote to annotated:**
- Deposit of the original `.d` bundles.
- Author confirmation of the replicate/injection naming and the 6 missing 0 h runs.
- Optionally, reading the tagSummary tsv files to confirm the search modifications.

SDRF file(s): PXD032795.sdrf.tsv. Built with a scripted manual build (`/home/claude/bangkok3/scripts_PXD032795/build.py`); evidence is in `/home/claude/bangkok3/scratch/PXD032795/`.

## Review status
pending
