# PXD016016 SDRF annotation report

## Study
Structural insights into a HECT-type E3 ligase AREL1 and its ubiquitination activities in vitro. Lab of J. Sivaraman, Department of Biological Sciences, National University of Singapore. Paper: Singh S, Ng J, Nayak D, Sivaraman J., J Biol Chem 2019;294(52):19934-19949, PMID 31732561, DOI 10.1074/jbc.RA119.010327, PMC6937569. The paper's data-availability footnote cites PXD016016, so the PX record links the right paper.

## Scope, evidence and decisions
Status: sandbox. The file has 4 rows (4 MS runs, label-free) and 33 columns. Templates: ms-proteomics and human (v1.1.0).

- **Is this mappable proteomics?** Yes, but it is small. The analytes are not cells or tissue. They are SDS-PAGE bands of purified recombinant human proteins after an in vitro ubiquitination reaction, cut out and digested with trypsin to map ubiquitination sites (GG-Lys). There are two kinds of sample: (a) autoubiquitinated extended AREL1 HECT domain (aa 436-823), and (b) SMAC ubiquitinated by that AREL1 domain. Each run maps to one of these two kinds from its file name, and the Results confirm both experiments (STATED). This follows the campaign's precedents for purified recombinant proteins (PXD019082, PXD003132, PXD009095).
- **Deposited vs annotated.** The ProteomeCentral PROXI record (rev 2, 2024-10-22) lists 12 files:
  - 4 `.mzML` files, each tagged "Associated raw file URI".
  - 4 ProteinPilot `.group` files.
  - 4 `.group.xml` files.

  No `.wiff` or `.wiff.scan` file is listed. The campaign cache said "4 RAW / 12 files". The 4 "RAW" files are the 4 mzML files, so the cache counted them correctly but typed them wrongly, and the expectation that `.wiff` plus `.wiff.scan` make one run does not apply. Each mzML is one run, and all 4 are annotated (4/4). The `.group` and `.group.xml` files are search outputs and get no rows. The PRIDE FTP folder and the PRIDE v3 API were unreachable all session (upstream connect error, 5 tries), so I could not read the FTP listing, a README or the mzML headers. The file list comes from PROXI only. The PX record carries the "Unsupported dataset by repository" (partial submission) term.
- **Run → sample.**
  - `AREL1Ubiquitination-WXH_Spl36_Digant_4.mzML`: autoubiquitination bands of wild-type extended AREL1 HECT. Stated: Results, "TripleTOF 5600 MS analysis of these bands identified ~11 lysine residues".
  - `SmacUbiquitination-WXH_Spl37_Digant_5`, `SmacUbiquitination2-WXH_Spl35_Digant_3` and `SmacUbiquitination3-WXH_sp7__SMOE_H9`: ubiquitinated SMAC bands (Results: K62, K191, K207 found). Wild-type SMAC and AREL1 are INFERRED from the order of work: the K→R mutants were made only after the MS identified the sites.
- **INFERRED, and the reason for sandbox: what the 3 SMAC runs are.** The paper says only "Ubiquitinated SMAC bands were analyzed by MS". It does not say whether the 3 SMAC files are repeat reactions, different gel bands of one reaction (for example mono- vs poly-Ub), or re-injections. The file names carry different submission sample IDs (Spl37, Spl35, and sp7/SMOE_H9 from a different naming batch). This suggests separately prepared samples, so I annotated them as `SMAC_ubiquitination_1..3` with biological replicate 1/2/3 and technical replicate 1. That reading is not stated. They could equally be bands or technical repeats. Table S5 and Fig. S5 (JBC supplement) were not read.
- **Prep (stated).**
  - Proteins expressed in *E. coli* BL21(DE3) and affinity- or gel-filtration-purified. Tags were cleaved (SUMO protease or PreScission).
  - Reaction: 0.05 uM UBA1, 1 uM UbcH7, 3 uM extended AREL1 HECT, 10 uM ubiquitin, 10 uM SMAC (SMAC runs only). Buffer: 50 mM HEPES pH 7.5, 100 mM NaCl, 5 mM ATP, 10 mM MgCl2, 1 mM DTT. Incubated 120 min at 37 C.
  - 12.5% SDS-PAGE, band excision, then "exhaustive trypsin digestion" and Sep-Pak tC18 desalting.
  - The `characteristics[treatment]` text summarises the reaction. The SMAC runs also contain SMAC, which is the substrate factor.
- **LC-MS (stated).**
  - Eksigent nanoLC Ultra / cHiPLC trap-elute, 75 um x 150 mm column, about 30 min gradient at 300 nl/min.
  - TripleTOF 5600 in information-dependent acquisition mode (DDA), MS1 400-1800 m/z, top 20, rolling collision energy. The paper and the PX record agree on the instrument (MS:1000932).
  - Dissociation is written as beam-type CID (MS:1000422). This is the collision-cell CID of a Q-TOF, as in PXD000588. It comes from the instrument type, not from a stated value.
- **Search.**
  - Stated: ProteinPilot 5.0 (Paragon 5.0.0.0.4767) against UniProt Swiss-Prot 2018_06 (40,698 entries); trypsin; ID focus "biological modifications"; special factor "ubiquitin/SUMO enrichment"; thorough effort; 95% confidence.
  - Modification parameters: GG (UNIMOD:121) on K, Variable. This is STATED: the paper's whole aim is Ub sites, and the PX record has MOD:00492.
  - Carbamidomethyl (UNIMOD:4) on C, Fixed. This is INFERRED from the PX term MOD:00397 "iodoacetamide derivatized residue". The paper names no reduction or alkylation step, and Paragon has no explicit fixed/variable list.
  - Oxidation (UNIMOD:35) on M, Variable. This is INFERRED from the PX term MOD:00425 "monohydroxylated residue".
  - The PX term MOD:00394 (acetylated residue) is not annotated because its target residue or position is unknown. Paragon's "biological modifications" mode searches hundreds of PTMs that are not listed.

## Values left not available / not applicable
- `organism part`, `cell type`, `disease`, `ancestry category`, `sex`, `individual`: not applicable. These are purified recombinant proteins, not biological specimens.
- `age`: not available. The human template does not accept `not applicable` here (PXD019082 precedent).
- `organism` = Homo sapiens: the PX record and the constructs are human AREL1 and SMAC. The expression host (*E. coli* BL21(DE3), stated) has no column; it is recorded here.
- `precursor/fragment mass tolerance`: not available. Paragon takes no user tolerances, and none are stated.
- Reduction and alkylation reagent columns are omitted because they are not stated (see the carbamidomethyl note above).

## Conflicts
- The cache said "4 RAW" on a SCIEX instrument, but the deposit is mzML only (advisory `peak_list_data_file` x4). No native `.wiff` is listed.
- The Results heading says "Lys61 and Lys191", but the text and abstract say Lys62 and Lys191. This does not affect the SDRF.

## Verification
- Accessions checked live today:
  - UNIMOD:121 GG: unimod.org.
  - MS:1000932, MS:1000422 and MS:1001251: Ontobee.
  - UNIMOD:1, 4 and 35: names checked against the unimod.xml bundled with sdrf-pipelines.
  - PRIDE:0000627: the campaign precedent (PXD000588).
  - EBI OLS4 was down today (upstream connect error).
- `parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics --template human`: "Everything seems to be fine". Ontology checks were skipped because the OLS dependencies are not installed.
- `sdrf_review.py`: [OK], with the advisory "4 peak_list_data_file".
- Evidence is saved in `/home/claude/singapore2/scratch/PXD016016/`: `proxi_summary.txt`, `file_list.txt`, `paper_PMC6937569_excerpts.txt` and `accession_checks.txt`.

**To upgrade to annotated:** the PRIDE FTP README/listing, or Table S5 / Fig. S5, stating what each of the 3 SMAC runs is. A readable mzML header or `.group.xml` would also confirm the run-to-band mapping.

## Review status
pending
