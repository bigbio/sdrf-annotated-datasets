# PXD043828 SDRF annotation report

## Study
Proteomic analysis of the neurotoxic effects of chronic methamphetamine self-administration on cognition, and of melatonin's role in recovery during methamphetamine withdrawal (mouse prefrontal cortex).
Polvat T et al., J Proteome Res 2023;22(10):3348-3359, doi:10.1021/acs.jproteome.3c00502, PMID 37676068, PMC10563163 (ACS AuthorChoice; full text read on PMC).

## Scope, evidence and decisions
**Status: sandbox.** All 108 runs are mapped to a sample, but the mouse/injection mapping is inferred from file names (F2), and the search parameters come from paper prose rather than the deposited `.dat` files (F3).

SDRF files (round 1 split the original single file by acquisition mode):
- `PXD043828-dda.sdrf.tsv`: 54 rows x 35 columns. Templates ms-proteomics and vertebrates. Data-dependent acquisition (PRIDE:0000627).
- `PXD043828-swath.sdrf.tsv`: 54 rows x 39 columns. Templates ms-proteomics, vertebrates and dia-acquisition. `NT=SWATH MS;AC=PRIDE:0000447`. Adds `comment[scan window lower/upper limit]` = not available (the paper's range is a typo) and `comment[isolation window width]` = 25.

Within each file the coordinate tuple (source name, biological replicate, technical replicate, fraction) is unique (54/54).

**Deposited vs annotated.** The PX record (ProteomeCentral PROXI, revision 3) lists 217 files: 108 Bruker `.d.rar` raw archives, 54 `.mgf`, 54 `.dat` search outputs, and `checksum.txt`. The PRIDE FTP directory listing agrees with this. All 108 raw archives are annotated. `.mgf`/`.dat` are derived files (one pair per DDA run) and are not rows. The raw names form a complete grid with no gaps or extras:
- DDA "screening" runs: `<group>-0<n>-rep<r>-<phase>-NT.d.rar` (54)
- SWATH runs: `SWATH-<group>-0<n>-rep<r>-<phase>.d.rar` (54)
- phase SA has groups control and METH; phase WD has control, METH, mel and METH_mel
- n = 1-3, r = 1-3

This gives 6 groups x 3 mice x 3 injections x 2 acquisition modes.

**Sample design (STATED, paper Methods).**
- Adult male ICR mice (6-8 weeks, 20-30 g; National Laboratory Animal Center, Mahidol University).
- Self-administration (SA) phase: 21 days oral two-bottle self-administration of METH HCl (0.05 mg/mL on days 1-9, then 0.1 mg/mL on days 10-21) or water only.
- 5 mice per group were killed after the SA phase. The rest went into the withdrawal (WD) phase: 14 days on water, with daily s.c. vehicle (2.5% ethanol in saline) or melatonin 10 mg/kg. This gave the groups control, METH-WD, METH-WD/mel and mel (N = 5 each).
- Whole PFC from each mouse was profiled. The paper says "protein levels from the PFC of individual mice", and that SWATH used "the same samples as the screening phase".
- File group codes map one-to-one to the paper's groups: `METH` in WD = METH-WD; `METH_mel` = METH-WD/mel.
- `factor value[treatment]` holds the paper's group label, with the phase where a label is shared (control (SA), METH (SA), control (WD), METH-WD, METH-WD/mel, mel).

**INFERRED (not stated anywhere).**
1. `-0<n>-` = individual mouse n (biological replicate 1-3 within each group), and `rep<r>` = repeated injection of the same digest (technical replicate). Only 3 of the 5 mice per group were run, and the paper never states the proteomics N or which mice were used. Western blots used N = 3/group.
2. DDA mouse n and SWATH mouse n are the same animal, so they share a source name (`PFC_<phase>_<group>_mouse<n>`). This rests on the "same samples" sentence and the identical numbering.
3. The meaning of the `-NT` suffix on the DDA files is unknown. It is not used for annotation.

**Instrument.** PRIDE lists `compact` (MS:1002280). The paper says "Q-ToF Compact, Bruker" with a Dionex UltiMate 3000 RSLCnano and CaptiveSpray source. They agree. The `.d` headers were not read: these are RAR archives of 0.7-3.4 GB, and the shell has no network access.

**Dissociation.** CID (MS:1000133) is INFERRED from the instrument: the compact Q-TOF fragments only in its collision cell. The paper does not name it.

**Acquisition.** DDA file: Data-dependent acquisition (PRIDE:0000627). SWATH file: SWATH MS (PRIDE:0000447). The paper reports "SWATH mode" with 25 Da isolation windows, 32 overlapping windows, 100 ms accumulation and a 3.0 s cycle, analysed in Skyline 19.1.0.193. Only the SWATH file declares `dia-acquisition`.

**Sample prep (STATED).** Lysis in urea/thiourea/CHAPS. 50 ug protein reduced with 100 mM DTT and alkylated with 100 mM iodoacetamide. Digested with Trypsin Gold (Promega), 16 h at 37 C. C18 ZipTip clean-up. 1 ug injected.

**Search (DDA rows, STATED in the paper).** MaxQuant/Andromeda against the Mus musculus UniProt database:
- Carbamidomethyl C fixed; N-terminal acetylation and Met oxidation variable. The paper says only "N-terminal acetylation"; it is encoded as Protein N-term (`PP=`), the MaxQuant default (INFERRED position).
- Trypsin/P, 2 missed cleavages, 1% protein FDR.
- ToF MS/MS match tolerance 0.5 Da, used as the fragment tolerance.
- MS1 m/z 150-2200.

PRIDE's modification list (acetylated residue, iodoacetamide-derivatized residue) agrees with this.

## Values left not available / not applicable
- `comment[precursor mass tolerance]` = not available on all rows. The paper gives "0.5 and 0.25 for the first and main searches" with no unit, and MaxQuant's default unit is ppm.
- SWATH rows:
  - `comment[fragment mass tolerance]`, `comment[modification parameters]` x3 and `comment[ms1 scan range]` = not available. The Skyline settings are unpublished.
  - The SWATH scan range is printed as "150-22,000 m/z", an evident typo, and 32 x 25 Da windows do not span 150-2200 either. It was therefore not copied.
- `characteristics[cell type]` = not applicable (whole-tissue PFC homogenate).
- `comment[fractionation method]` = not applicable (single-shot runs, fraction 1).
- `characteristics[disease]` = normal: these are healthy animals given drug treatments, with no disease model.
- Age (6-8 weeks at purchase, plus about 5-6 weeks of protocol) is not encoded because the declared templates do not license `characteristics[age]`. `developmental stage` = adult (stated).

## Conflicts
- The deposited search outputs are Mascot-style `.dat` files (one per DDA run), but the paper reports MaxQuant/Andromeda. The `.dat` headers (MODS/IT_MODS/TOL/ITOL/CLE) could not be read. Each is 0.26-0.72 GB, the shell has no internet, and the shared browser cannot do HTTP range reads. Search parameters therefore come from paper prose, against the brief's precedence rule. **This is the main open point.** If a reviewer can range-read one `.dat` header, it should override the modification and tolerance columns.
- Raw `.d` instrument metadata could not be checked, for the same reason.
- PRIDE's own v3 API was not used (down per brief). The Europe PMC REST endpoint returned upstream errors; PubMed and PMC were used instead.

## Ontology verification
- Verified live in OLS (WebFetch) this run: UBERON:0000451 prefrontal cortex; MS:1002280 compact (definition: Bruker Daltonics compact ESI Q-TOF, CaptiveSpray).
- Further live OLS lookups were rate-limited or failed with upstream errors. EBI was unreachable from the cloud browser.
- These terms are the standard campaign terms already present in reviewed files and were not re-verified this run: PRIDE:0000627/0000450/0000608/0000599, MS:1000133, MS:1001251, UNIMOD:4/1/35, NCBITaxon:10090.
- `parse_sdrf` ran structure-only, because its OLS dependencies are not installed.

## Validation
- `sdrf_review.py`: [OK] for both files.
- `parse_sdrf validate-sdrf --use_ols_cache_only`, run once per declared template: no errors. The DDA file was checked against ms-proteomics and vertebrates; the SWATH file against ms-proteomics, vertebrates and dia-acquisition. This was structure-only validation, because the OLS dependencies are not installed.

## Round-1 review (FAIL, recommended sandbox) and response
- **F1** (DDA and SWATH rows shared coordinate tuples on 54 pairs): fixed by splitting into `-dda`/`-swath` files. The old `PXD043828.sdrf.tsv` was deleted.
- **F2** (mouse/injection mapping inferred from file names): **open**. Recorded as INFERRED points 1-2 above. It would be resolved by an author statement, PRIDE sample metadata or `.d` headers.
- **F3** (search parameters from the paper's MaxQuant search; deposited `.dat` headers unread): **open**. See Conflicts.
- **F4** (`PP=Protein N-term` on Acetyl is the MaxQuant default, not stated): kept and documented as INFERRED. It depends on F3.
- **F5** (CID inferred from the instrument): kept and documented.
- **F6**: SWATH rows now use `NT=SWATH MS;AC=PRIDE:0000447`.
- **F7** (factor value vs characteristic wording): the factor is the paper's short group label, mapped one-to-one to the 6 `characteristics[treatment]` strings:
  - control (SA) = water 21 d
  - METH (SA) = METH self-administration 21 d
  - control (WD) = water + vehicle
  - METH-WD = METH + vehicle withdrawal
  - METH-WD/mel = METH + melatonin withdrawal
  - mel = water + melatonin
- **F8**: reagent labels are now capitalised to the OBO names "Dithiothreitol (DTT)" and "Iodoacetamide (IAA)".
- The reviewer resolved PRIDE:0000627/0000450/0000447/0000608/0000599 and MS:1000133 against pride_cv.obo/psi-ms.obo, and UBERON:0000451 against Ontobee.

Evidence files are in `scratch/PXD043828/`: `raw_files.txt`, `filelist_note.txt`, `paper_methods_PMC10563163.txt` and `py/build_PXD043828.py`.

## Review status
Round 1 (independent reviewer): FAIL, recommended sandbox. F1, F6 and F8 are fixed; F2 and F3 stay open (sandbox). Round 2: pending.
