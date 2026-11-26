# PXD076578 SDRF annotation report

## Study
Curcuminoid Supplementation Modulates Neuroinflammatory and One-Carbon Metabolic Pathways in Canine Primary Epilepsy: A Proteomic and Clinical Study.
Chantong B, Prakaikowit N, Sangapol W, Chatampaiwong S, Ploypetch S, Phochantachinda S, Chatchaisak D. *Curcuminoid supplementation alters proteomic profiles and clinical outcomes in canine primary epilepsy: A pilot study.* Vet Anim Sci 2026;34:100906. doi:10.1016/j.vas.2026.100906, PMID 42959793, PMC13718403. The full text was read on pmc.ncbi.nlm.nih.gov.

The study is label-free serum proteomics of client-owned dogs (*Canis lupus familiaris*) on a Bruker compact Q-TOF (Mahidol University, Bangkok). Dogs with primary epilepsy syndrome (PES) were sampled at baseline and after 60 days of oral curcuminoid; healthy adult dogs were sampled once as a reference.

## Status: sandbox
The SDRF validates, and every run maps to a sample code stated in its file name. It is not `annotated` because three material points are unresolved:
1. **The sample counts conflict with the paper.** The deposit has 6 PES codes (`2A, 2B, 2C, 3A, 3B, 3C`) × D0/D60 and 6 healthy codes (`Adult-A..F`). The paper describes 8 PES dogs and "five healthy adult dogs". It never states the n used in proteomics and never uses these codes.
2. **What a code means is INFERRED.** Each code is taken to be one dog, or possibly one pool. The paper does not mention pooling, but the sibling dataset from the same lab, PXD055138, used the same naming scheme for 2-dog pools. No code can be linked to Table 1 (Dog 1-8), so breed, sex and age stay `not available`.
3. **Acquisition mode (DDA) and dissociation (CID) are INFERRED**, as in PXD055138. The modification and tolerance columns follow the paper, because the deposited Mascot `.dat` files could not be read (see Conflicts).

## Scope: deposited vs annotated
The PROXI record (`proteomecentral.proteomexchange.org/api/proxi/v0.1/datasets/PXD076578?resultType=full`, accession verified) lists 126 files:

| Prefix | Raw `.d.zip` | `.mgf` + `.dat` | Annotated rows |
|---|---|---|---|
| `Adult-{A..F}-{1..3}` | 18 | 18 + 18 | 18 |
| `Siezure-2{A,B,C}-{D0,D60}-{1..3}` | 18 | 18 + 18 | 18 |
| `Siezure-3{A,B,C}-{D0,D60}-{1..3}` | 18 | 0 + 0 | 18 |
| **Total** | **54** | 72 | **54** |

- **Rows.** There is one row per raw `.d.zip` (label-free, one channel). `comment[data file]` holds the deposited `.d.zip` name, as in PXD040999. `assay name` is the same name without `.d.zip`.
- **Exclusions.** No raw run is excluded. The `.mgf` and `.dat` files are derived files and get no rows of their own.
- **Missing derived files.** Group 3 (`3A/3B/3C`) has raw data only.
- **Typo in the deposit.** One file is spelled `Seizure-2A-D0-1_BB5_01_8711.d.zip`; the other 35 PES runs use `Siezure`. Names are kept exactly as deposited.
- **Name check.** The file names were transcribed from the PROXI JSON into `scratch/PXD076578/raw_files.txt`. They give 54 unique names, 3 per sample code, and the SDRF `comment[data file]` set matches that list exactly.
- **Not cross-checked.** PRIDE `files/all` and the FTP index could not be reached today (EBI upstream connect errors), so the list was not cross-checked against them.

## Decisions and evidence
**Groups and time points are STATED by the file names and the paper.**
- `Siezure-…-D0` = PES dogs at baseline (paper "C0").
- `Siezure-…-D60` = PES dogs after 60 days of curcuminoid (paper "C60").
- `Adult-X` = healthy adult control dogs (paper "adults"), sampled once with no supplement.
- Disease is `epilepsy` (MONDO:0005027) for PES dogs and `normal` (PATO:0000461) for controls. The paper's term is primary epilepsy syndrome (IVETF), which has no more specific MONDO term, so the general term is used.

**Sources and biological replicates (INFERRED).**
- Each code is one source. The same code at D0 and D60 is assumed to be the same dog: both rows get the same `biological replicate` (1-6 by code) but separate source names (`PES_dog2A_D0` / `PES_dog2A_D60`), because each is a different blood draw.
- Controls are numbered 1-6 (`healthy_adult_A..F`).
- `characteristics[pooled sample]` = `not available`. The paper does not say whether samples were pooled, and the sibling dataset PXD055138 used the identical `Adult-A..F` / `<n>{A,B,C}` scheme for pools of 2 dogs.

**Technical replicates (INFERRED, strongly supported).**
- The `-1/-2/-3` suffix is taken as repeat injections of the same vial: all three runs of a code share one autosampler position (for example `2A-D0` → `BB5` for runs 8711, 8719 and 8727).
- The run numbers step in cycles: in each batch every sample is injected once before the next round starts.
- The paper does not mention replicate injections.

**Treatment.** D60 = `curcuminoid 100 mg oral daily for 60 days`; D0 and controls = `no curcuminoid`. Factor values are `disease` and `treatment`. All PES dogs also stayed on phenobarbital throughout; this is not encoded and is noted here instead.

**Sampling time.** `0 day` / `60 day` for PES dogs. For controls it is `not applicable`, because they had a single draw that was not on the supplementation timeline.

**Developmental stage.** `adult` is STATED: PES dogs were 3-10 years old and controls were "healthy adult dogs" aged 1-6 years.

**Sample preparation (STATED).**
- Serum (UBERON:0001977). The paper's Introduction says "plasma", but Methods say serum.
- Pierce albumin/IgG depletion, encoded as `characteristics[depletion]` = `depletion`.
- Urea; 30 µg protein per sample.
- DTT reduction and iodoacetamide alkylation in TEAB.
- Trypsin Gold (Promega) at 37 °C for 16 h; 1 µg injected.

**Instrument (STATED).** `compact` (MS:1002280) is given by both the PX record and the paper ("quadrupole time-of-flight compact mass spectrometer (Bruker)"), with a Dionex UltiMate 3000 RSLCnano. The raw `.d` headers were not read (no network from the shell, and the EBI FTP was down).

**Search parameters (paper).**
- MaxQuant 1.6.2.10 / Andromeda, UniProt *Canis lupus familiaris*.
- Carbamidomethyl C fixed; Oxidation M variable.
- N-terminal acetylation variable, encoded as `PP=Protein N-term`. That position is INFERRED from the MaxQuant default; the paper says "N-terminal acetylation".
- Fragment tolerance "TOF MS/MS match tolerance of 0.5 Da".
- The PX record's single modification ("acetylated residue", MOD:00394) is consistent with this.

**MS1 scan range (STATED).** 150-2200 m/z.

**Acquisition and dissociation (INFERRED).** DDA (PRIDE:0000627) and CID (MS:1000133), from the compact's AutoMSMS mode and the MaxQuant DDA search. The paper states neither.

## Values left not available / not applicable
- `characteristics[strain or breed]` and `characteristics[sex]` = `not available`. Table 1 gives breed and sex for Dog 1-8, but no code links to a Table 1 dog, and the control dogs are not described individually.
- `characteristics[pooled sample]` = `not available` (see above).
- `characteristics[cell type]` = `not applicable` (serum).
- `characteristics[sampling time]` = `not applicable` for the healthy controls.
- `comment[precursor mass tolerance]` = `not available`: not stated in the paper, and the deposited search output was not readable.
- `comment[fractionation method]` = `not applicable`: one unfractionated run per injection; `fraction identifier` = 1.
- `characteristics[age]` is omitted: there is no per-code age.

## Conflicts and open points
1. **8 PES dogs (paper) vs 6 PES codes (deposit); 5 controls (paper) vs 6 `Adult` codes (deposit).** It is unknown whether 2 dogs were dropped from proteomics, whether the codes are pools, or whether the controls are a different set. This needs an author sample sheet mapping each code to a dog.
2. **Possible reuse of control runs from PXD055138.** The same submitter (Phochantachinda, Mahidol) deposited `Adult-A..F-{1..3}` runs (`.baf_idx/.mgf/.dat`) in PXD055138 (canine diabetes and astaxanthin). There they are pools of 12 healthy dogs. Here the paper describes 5 single healthy dogs. Whether these are byte-identical data could not be checked: the EBI FTP was unreachable and PXD055138 has no `.d` files to compare. If they turn out to be the same runs, the control rows describe pools, not individuals.
3. **The deposited search output contradicts the paper.** Mascot `.dat` files are deposited, but the paper reports MaxQuant/Andromeda. The `.dat` parameter headers (TOL, ITOL, MODS, IT_MODS, CLE) were **not read**: the shell has no internet and `ftp.pride.ebi.ac.uk` returned upstream errors in the browser. Contrary to the usual precedence, the modification and tolerance columns therefore follow the paper. Reading the first ~10 KB of any `Adult-A-1.dat` would settle this, including the precursor tolerance.
4. **The dose is inconsistent within the paper.** Methods say 10-20 mg/kg/day; Results, the abstract and the PX description say 100 mg/day. 100 mg/day is encoded because three sources agree on it.
5. **Batches.** Run numbers show two acquisition batches for PES: 87xx holds 2A/2B/2C (D0 and D60) plus 3A-D0, and 131xx holds 3B-D0, 3C-D0 and 3A/3B/3C-D60. The controls run in between (129xx). No `lc batch` column was added, because batch is not stated, only visible in the run numbers.

## Ontology verification (live, 2026-11-26)
- Checked on Ontobee: MONDO:0005027 epilepsy, UBERON:0001977 blood serum, NCBITaxon:9615 *Canis lupus familiaris*, PATO:0000461 normal, MS:1002280 compact, MS:1000133 collision-induced dissociation, MS:1001251 Trypsin.
- Checked on unimod.org: UNIMOD:1 Acetyl, UNIMOD:4 Carbamidomethyl, UNIMOD:35 Oxidation.
- Checked in `pride_cv.obo` (GitHub master): PRIDE:0000627, PRIDE:0000608 and PRIDE:0000599.
- OLS4 was rate-limited or down today.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` passes clean with no template, with `--template ms-proteomics` and with `--template vertebrates` ("Everything seems to be fine"). Ontology lookups were structural only, because OLS extras are not installed. The SDRF has 54 rows × 39 columns; templates ms-proteomics v1.1.0 and vertebrates v1.1.0.

Evidence files are in `/home/claude/bangkok3/scratch/PXD076578/`: `raw_files.txt`, `peak_and_dat_files.txt`, `px_record_notes.txt`, `paper_notes.txt`, `ontology_checks.txt`. The build script is `/home/claude/bangkok3/scripts_PXD076578/build.py`.

## Review status
pending
