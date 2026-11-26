# PXD050755 SDRF annotation report

## Study
Secretome analysis of HSPD1 knockdown in A549 lung cancer cells (PRIDE, announced 2024-04-13; Mae Fah Luang University). The PX record still says "Dataset with its publication pending". The publication was found in PubMed: Aluksanasuwan S, Somsuan K, Ngoenkam J, Chiangjong W, Rongjumnong A, Morchang A, Chutipongtanate S, Pongcharoen S. "Knockdown of heat shock protein family D member 1 (HSPD1) in lung cancer cell altered secretome profile and cancer-associated fibroblast induction". Biochim Biophys Acta Mol Cell Res 2024;1871(5):119736. doi:10.1016/j.bbamcr.2024.119736, PMID 38663552, no PMCID (Elsevier bronze OA).
- The match rests on title, abstract, submitter and timing. The abstract reports a targeted label-free secretome comparison of shHSPD1-A549 vs shControl-A549, with lentiviral shRNA. The paper is by the same lab head as the PX contact, and its Epub (2024-04-24) is 11 days after the dataset was announced.
- **The paper's full text could not be read.** ScienceDirect showed a captcha (not bypassed), europepmc.org showed a Cloudflare challenge, and the www.ebi.ac.uk services (Europe PMC REST, PRIDE v3, OLS4) all returned "upstream connect error". Unpaywall lists only the publisher location.
- So the methods below come from the **submitter's PRIDE sample/data processing protocols**, read from the OmicsDI mirror (`omicsdi.org/ws/dataset/pride/PXD050755.json`; its accession and file list match).
- A second paper from the same lab was checked and is not this dataset's paper: Somsuan et al., Biomed Rep 2025;22:77, doi:10.3892/br.2025.1955. It has no MS work and no PXD (data "on request"). Its Methods describe the same knockdown model: pLKO.1-puro lentiviral shRNA, scrambled shRNA control, serum-free DMEM for 24 h.

## Scope, evidence and decisions
annotated 18 rows (18 .wiff runs x label free); 18 x 36; templates ms-proteomics, human, cell-lines.

**Deposited vs annotated.** The PX `datasetFiles` and the FTP listing agree on 55 files:
- 18 `.wiff` with 18 matching `.wiff.scan`: one run per pair, and `comment[data file]` = the `.wiff`.
- 18 mzXML conversions. These are not separate runs; some names differ from their wiff (`sup_shHSP60_2_IDA..mzXML`, `sup_shHSP60_3_IDA1`, `*_SWATH1`, `*_SWATH3`).
- 1 ProteinPilot `.group` (2.3 GB, not read).

All 18 runs are annotated; none are excluded. `.wiff.scan` is not listed in its own column because `comment[associated data file]` is not licensed by the declared templates.

**Design (stated).** The PRIDE description has two groups: A549 with HSPD1 knockdown by shRNA (file token `shHSP60`; HSP60 = HSPD1), and shControl. The data protocol gives "3 biological replicates per group". File tokens `_1/_2/_3` and `1/2/3` give `biological replicate` 1-3 within each group. Each sample has 1 SWATH run and 2 IDA runs (`_IDA`, `_IDA2`).
- `factor value[treatment]` = `HSPD1 shRNA knockdown` / `control shRNA`.
- `characteristics[genetic modification]` was not used: only `clinical-metadata` licenses it, and that template does not fit here.

**Samples.** A549 = Cellosaurus `A-549`, CVCL_0023, checked live at api.cellosaurus.org: male, 58Y, lung adenocarcinoma (NCIt C3512), derived from lung.
- `organism part` = lung and `cell type` = epithelial cell.
- `material type` = cell line, because the fixed vocabulary has no "conditioned medium" value. The analysed material is the concentrated serum-free conditioned medium (3-kDa cut-off), i.e. the secretome. Reviewers may prefer a different representation.

**Acquisition and search (stated in the PRIDE protocol).**
- Prep: 50 ug protein was reduced, alkylated and digested with trypsin at 1:50.
- LC-MS: Eksigent nanoLC ultra, Analyst TF 1.8.
- IDA: 350-1250 m/z TOF-MS, top 100 precursors (written as `ms1 scan range` 350m/z-1250m/z on IDA rows).
- SWATH: 157 variable windows of 7 m/z (1 m/z overlap) over 350-1500 m/z, cycle 3.08 s.
- Search: ProteinPilot 5.0.2 against Swiss-Prot human (2022_01) with "alkylation on cysteine by iodoacetamide" → Carbamidomethyl UNIMOD:4 TA=C MT=Fixed and alkylation reagent IAA. Trypsin with 1 missed cleavage, 1% FDR.
- Library and quantification: PeakView 2.2 SWATH MicroApp, 6 transitions per peptide, XIC 20 ppm.
- Dissociation is beam-type CID (MS:1000422); the MS2 analyzer is TOF.

**Accessions verified live** (OLS4 was down, so other sources were used):
- MS:1003456 TripleTOF 6600+, MS:1000422, MS:1002038 and MS:1001251: Ontobee.
- MS:1000084: psi-ms.obo on GitHub.
- PRIDE:0000627, PRIDE:0000450 and PRIDE:0000599: pride_cv.obo on GitHub.
- UNIMOD:4: unimod.org.
- CVCL_0023: Cellosaurus API.

Evidence is in `/home/claude/bangkok3/scratch/PXD050755/`: `px_files_raw.txt`, `ftp_listing_sizes.txt`, `omicsdi_PXD050755_protocols.txt`, `pubmed_38663552.txt`, `cellosaurus_CVCL_0023.txt`, `ontobee_tripletof.txt`, `build/build_PXD050755.py`.

## Values left not available / not applicable
- `precursor mass tolerance` and `fragment mass tolerance`: not available. ProteinPilot has no user tolerances. The "50 ppm" in the protocol is the IDA dynamic-exclusion window, and "20 ppm" is the SWATH XIC width; neither is a search tolerance.
- `reduction reagent`: not available. The protocol says only that proteins were "reduced".
- `ms1 scan range` on SWATH rows: not available. The protocol gives 350-1500 m/z for the precursor window range but "100-1500" for the TOF-MS scan, which is ambiguous.
- `collision energy`: column omitted. The protocol's "collision energy of 15 eV" for SWATH is almost certainly the collision energy *spread*, since SCIEX SWATH uses rolling CE. Writing "15 eV" as CE would mislead.
- Age and sex come from Cellosaurus. Ancestry was not written: Cellosaurus gives "Caucasian", which does not map cleanly to HANCESTRO.

## Conflicts and INFERRED points
1. **Instrument conflict (main sandbox reason).** The PX/PRIDE structured `instruments` field says TripleTOF 5600 (MS:1000932). The submitter's own sample-processing protocol says "TripleTOF 6600+ mass spectrometer (ABSciex)" and Analyst TF 1.8. The annotation uses **TripleTOF 6600+ (MS:1003456)**: the free-text protocol is specific and written by the submitter, while the dropdown field is known to be wrong in this campaign. The raw header could not be read, because the shell has no internet and the 31-54 MB `.wiff` (OLE) and the GB-sized mzXML (`msInstrument/msModel`) were not downloaded. The paper Methods could not be read either. **To resolve:** read the msModel from any mzXML header (HTTP range, first few KB), or read the instrument string in a `.wiff`.
2. **`_IDA` vs `_IDA2` = technical replicates 1/2 of the same secretome sample (INFERRED).** This rests on the file names and on the library `.group` name `..._IDA12_...` (12 IDA runs). The data protocol says only "6 IDA experiments". The IDA2 `.wiff.scan` files are 1.5-3.7x larger (348-794 MB vs 200-241 MB), so IDA2 may have used a different method or a longer run, not a plain re-injection.
3. The SWATH runs carry `technical replicate` 1. Biological replicate numbers 1-3 restart within each group (`source name` keeps them distinct).
4. "control shRNA" is written generically; "scrambled" is stated only in the Biomed Rep 2025 companion paper.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` with no template and with `--template` ms-proteomics, human and cell-lines: each run reports "Everything seems to be fine". This was **structural only**: this parse_sdrf install has no OLS dependencies or ontology cache, so the accessions were checked by hand (sources above). SHA-256 b9b28970faa21418b7c723970d334bb44dccdc14432351333bd4e0aace8e251f.

## Review status
pending
