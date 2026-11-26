# PXD031111 SDRF annotation report

## Study
Pythium insidiosum protein identification. The paper is Krajaejun et al., "Secretome Profiling by Proteogenomic Analysis Shows Species-Specific, Temperature-Dependent, and Putative Virulence Proteins of *Pythium insidiosum*", J Fungi 2022 8(5):527, doi:10.3390/jof8050527, PMID 35628782, PMC9144242.

## Scope, evidence and decisions
**Status: sandbox.** 60 rows (60 mgf; one row per gel slice per sample); 30 columns; template ms-proteomics.

**What the deposit holds (PROXI, 124 files):**
- 60 "Associated raw file" entries, all Bruker `.baf_idx` index files. These hold no spectra.
- 60 `.mgf` peak lists.
- 4 Mascot `.dat` files (`CFA25 rep2/rep3`, `CFA37 rep2/rep3`).
- No `.d`/`.baf` bundles are deposited. Like PXD054595, `comment[data file]` therefore uses the deposited `.mgf` files.

**Reconciliation:** 60 mgf = 4 samples x 15 gel slices, each sample with slices 1-15 exactly once (checked in the build). The 60 `.baf_idx` files split the same way: `CFA25_N_rep2`, `CFA25_N_rep3`, `CFA37_N` and `CFA37rep3_N`, N = 1-15. One is misnamed `CFA25_4._rep2baf_idx`. All 60 runs are annotated; none are excluded.

**Samples:** cell-free culture filtrate antigens (CFA, the secretome) of *P. insidiosum* strain Pi-S, a Thai vascular pythiosis isolate. It was grown 7 days in SD broth at 25 °C or 37 °C, giving factor value[treatment] = `culture at 25/37 degree Celsius`. The paper states 2 biological replicates per temperature (CFA25-1/-2, CFA37-1/-2).

**Wet lab and search (all from Methods; the `.dat` files were not readable):**
- SDS-PAGE 12% gel; lanes cut into blocks (the count is not stated, and the deposit gives 15).
- DTT 10 mM, IAA 55 mM, trypsin.
- Ultimate 3000, 45 min gradient, MicrOTOF-Q II; MS1 m/z 400-2500, MS2 m/z 50-1500.
- Mascot 2.3.0 against the Pi-S predicted proteome: 0.6 Da / 0.8 Da, 1 missed cleavage, carbamidomethyl C and oxidation M both **variable** (as stated).

**Inferred, not stated:**
1. **mgf to replicate split.** The mgf names carry no rep tag. I assigned acquisition batch 7085-7123 (tray R*) to rep2 and batch 7500-7538 to rep3. This is consistent with the `.baf_idx` naming (`CFA37_N` without a tag versus `CFA37rep3_N`), but not proven, because the `.dat` FILE= lines were unread.
2. **Replicate numbering.** Deposited rep2/rep3 were taken as paper biological replicates 1/2.
3. **Fraction order.** Fraction identifier = slice number N from the file names; the paper gives no slice order or count.
4. **Instrument model.** micrOTOF-Q II comes from the paper. PX says only "micrOTOF series" (the parent term), and no `.baf` header exists to confirm it.
5. **Dissociation.** CID was not stated; it is the Q-TOF default, as in PXD032081.

**Conflicts:**
- PX species is `Pythium sp. PV So7` (TaxID 528135). The paper's organism, *Pythium insidiosum* (NCBITaxon:114742), was used.
- PX modifications list MOD:00425 (hydroxylation) and MOD:00397 (iodoacetamide). These are consistent with the paper's oxidation and carbamidomethyl, kept as variable per Methods.

**Values left as reserved words:**
- organism part, cell type and disease are `not applicable`: this is a secreted-protein fraction of a pathogen culture, with no anatomy, cell type or disease state of the sample.
- material type is omitted: none of its fixed values fits a culture filtrate.
- Strain Pi-S is recorded in the source name only, because `characteristics[strain or breed]` is licensed only by vertebrates/invertebrates/plants, and an oomycete fits none of these.

**Accession checks:** EBI OLS rate-limited every request today, so the checks used other sources (scratch `verify_terms.txt`):
- NCBITaxon 114742: UniProt taxonomy.
- MS:1000704 and MS:1001251: ontobee.
- MS:1000133: psi-ms.obo.
- PRIDE:0000568/0599/0608/0627: pride_cv.obo.
- UNIMOD:4/35: bundled unimod.xml.

**Validation:** `parse_sdrf validate-sdrf --template ms-proteomics --use_ols_cache_only` reported "Everything seems to be fine". Its ontology checks were unavailable (OLS deps not installed), so this is a structural pass only.

**To promote to annotated:** read the 4 `.dat` files (Mascot parameters and FILE= mgf lists) to confirm the rep split and the search mods. The vendor `.d`/`.baf` data would also need to be deposited.

SDRF file(s): PXD031111.sdrf.tsv. Built with a scripted manual build (`/home/claude/bangkok3/scripts_PXD031111/build.py`).

## Review status
pending
