# PXD055138 SDRF annotation report

## Study
Plasma-based proteomics analysis of molecular pathways in canine diabetes mellitus after astaxanthin supplementation. Phochantachinda S et al., PLoS One 2025;20(5):e0321509, doi:10.1371/journal.pone.0321509, PMC12057883 (CC-BY; full text read on journals.plos.org). Bruker compact Q-TOF, label-free, client-owned dogs (*Canis lupus familiaris*), Mahidol University (Bangkok).

## Status: sandbox
The SDRF validates, but two material points stop it from being `annotated`:
- **No vendor raw data is deposited.** The 90 files that PRIDE/PROXI class as "Associated raw file" are Bruker `.baf_idx` index files (4.3-6.9 MB), which hold no spectra. No `.baf` or `.d` is deposited. `comment[data file]` therefore points to the deposited `.mgf` peak lists, as in the bangkok-2 precedent PXD054595.
- **A third of the runs (the "Aging" series, 54 runs) are not described by the linked paper** and are left out (see Scope).

The pool and replicate structure is INFERRED from one sentence plus the file names (see Decisions).

## Scope: deposited vs annotated
The deposit has 258 files, counted on the PRIDE FTP HTTPS index (`ftp.pride.ebi.ac.uk/pride/data/archive/2025/03/PXD055138/`) and cross-checked against the PROXI `datasetFiles` list:

| Prefix | Runs | Files | Annotated |
|---|---|---|---|
| `Adult-{A..F}-{1..3}` | 18 | 54 (.baf_idx/.dat/.mgf) | 18 |
| `DM-3{A,B,C}-{D0,D90}-{1..3}` | 18 | 54 | 18 |
| `Aging-{1,2,3}{A,B,C}-{D0,D135}-{1..3}` | 54 | 150 (54 .baf_idx; .dat/.mgf for 48 runs; `Aging-2C-*` has only .baf_idx) | 0 |
| **Total** | 90 | 258 | **36 rows** |

**The "Aging" runs are excluded.** The paper and the PX description cover only 18 dogs:
- 6 diabetic (DM) dogs, sampled on day 0 and day 90.
- 12 clinically healthy adult dogs, sampled on day 0 only.

The paper never mentions an aging, senior or geriatric cohort, or a day-135 time point, and it mentions no third group. A web search found no other publication describing these runs. Their dog identity, disease state, intervention and age are therefore unknown, and annotating them would mean inventing a treatment and cohort from the strings "Aging" and "D135".

All 108 Adult/DM file names were read directly from the FTP index. The Aging names are listed in `scratch/PXD055138/file_names.txt`, reconstructed from the naming pattern and verified by per-prefix counts.

## Decisions and evidence
**Pools (INFERRED).** The paper says only "All plasma samples were combined in a 2:1 ratio within each group. These pooled samples were then processed…". The deposit holds 6 Adult pools (A-F) and 3 DM pools (3A-3C), which is consistent with 2 dogs per pool: 12 healthy dogs → 6 pools, 6 DM dogs → 3 pools. So:
- Each pool is one source.
- `characteristics[pooled sample]` = `pooled`. Member dogs are unnamed, so no `SN=` list is given.
- `biological replicate` = pool index within the group.
- DM pool *X* at D0 and at D90 is assumed to be the same pair of dogs. It gets the same replicate number but a different source name per time point, because it is a different blood draw.

**Injections (INFERRED).** The suffix `-1/-2/-3` is taken as technical replicate injections. The paper does not mention replicate injections.

**Groups and factors.** Group, disease and time point are STATED via the names and the paper:
- `Adult` = clinically healthy dogs, `normal` (PATO), day 0.
- `DM-…-D0` / `DM-…-D90` = diabetes mellitus (MONDO:0005015) before and after astaxanthin. The supplement was 12 mg/day oral (1.5-2.4 mg/kg) for 90 days, given on top of the dogs' regular DM treatment.
- `characteristics[sampling time]` = `0 day` / `90 day`.
- Factor values: `disease` and `treatment` (`astaxanthin` vs `no astaxanthin`, free text). NCIT:C63653 "Astaxanthin" exists, but the column is kept as a plain label.

**Developmental stage.** `adult` is STATED: the DM dogs were 5-11 years old, and the healthy group was "adult dogs… age-matched".

**Sample-prep reagents.** STATED in the paper: reduction 100 mM DTT and alkylation 100 mM iodoacetamide (both in 100 mM TEAB), digestion with trypsin gold (Promega) for 16 h.

**Instrument.** `compact` (MS:1002280) is STATED by both the PX record and the paper ("Q-ToF Compact, Bruker"). The raw headers could not be checked because there are no raw files.

**Search parameters** come from the paper (MaxQuant 1.6.2.10 / Andromeda, UniProt *Canis lupus familiaris*):
- Carbamidomethyl C fixed; Oxidation M variable; N-terminal acetylation variable (encoded as `PP=Protein N-term`, the MaxQuant default "Acetyl (Protein N-term)" — the position is INFERRED from "acetylation of the N-terminus").
- Fragment tolerance: "TOF MS/MS match tolerance 0.5 Da".
- The PX record's modification list (acetylated residue, iodoacetamide-derivatized residue) is consistent with this.

**MS1 scan range.** 150-2200 m/z, STATED.

**Acquisition and dissociation (INFERRED).** DDA (PRIDE:0000627) and CID (MS:1000133) are inferred: the Bruker compact AutoMSMS acquisition is CID-based DDA, and a MaxQuant DDA search was used. The paper states neither.

## Values left not available / not applicable
- `characteristics[sex]` and `characteristics[strain or breed]` = `not available`. Each pool mixes 2 client-owned dogs "of any breed or sex", and per-dog data would only be in S1 Table (DM dogs only, not read). Pool membership is unknown anyway.
- `characteristics[age]` is omitted: there is no per-pool age.
- `characteristics[cell type]` = `not applicable` (plasma).
- `comment[precursor mass tolerance]` = `not available`: not stated, and the MaxQuant/Mascot settings could not be read.
- `comment[fractionation method]` = `not applicable`: no fractionation, 1 run per injection.

## Conflicts and open points
1. **Deposited search output ≠ paper.** The deposited search files are Mascot `.dat` (145-519 MB), but the paper reports MaxQuant/Andromeda. The `.dat` headers (the Mascot TOL/ITOL/MODS/CLE parameters) were **not read**: the shell has no internet, and the browser would download multi-hundred-MB files. The modification and tolerance columns therefore follow the paper, not the deposited search, contrary to the usual precedence. Reading the first ~10 KB of one `.dat` (for example `DM-3C-D0-2.dat`) would settle this.
2. **No vendor raw data**, only `.baf_idx`, as described above. Promoting the dataset out of the sandbox needs the original Bruker `.d` folders.
3. **The "Aging" series (54 runs) is unexplained.** It needs a publication or author sample sheet stating the cohort, intervention, and what D135 means.
4. **Pool composition and replicate semantics are inferred** from the "2:1 ratio" sentence and the file-name counts.

## Ontology verification (live, 2026-11-25)
- NCBITaxon:9615, MONDO:0005015, PATO:0000461 and MS:1002280 were checked on Ontobee.
- UBERON:0001969 and EFO:0001272 were checked on OLS4.
- MS:1001251 was checked on Ontobee and MS:1000133 in the psi-ms.obo file on GitHub.
- PRIDE:0000627, PRIDE:0000608 and PRIDE:0000599 were checked in pride_cv.obo, release 2026-11-23. The reagent labels use that release's capitalisation.
- UNIMOD:1, 4 and 35 were checked on unimod.org.

EBI OLS was rate-limited for part of the session, so some lookups went through Ontobee and GitHub instead.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` passed (exit 0) once per template, for `ms-proteomics` and for `vertebrates` (v1.1.0). In this environment `parse_sdrf` 0.1.7 lacks its OLS dependencies, so the run was **structural only**; terms were checked by hand as listed above. Factor-value columns are last, and the row coordinate (source name, biological replicate, technical replicate, fraction) is unique.

SDRF: `PXD055138.sdrf.tsv`, 36 rows × 38 columns. Templates: ms-proteomics, vertebrates.

## Review status
pending
