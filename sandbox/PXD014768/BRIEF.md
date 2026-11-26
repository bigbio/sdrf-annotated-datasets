# PXD014768 SDRF annotation report

## Study
Protective cellular mechanism of estrogen against kidney stone formation: A proteomics approach and functional validation (Thongboonkerd lab, Mahidol University).

Paper: Peerapen P, Thongboonkerd V. *Proteomics* 2019;19(19):e1900095. DOI 10.1002/pmic.201900095, PMID 31475403. No PMCID was found. The paper is closed access: Wiley returned a Cloudflare bot check, and Europe PMC was down. Only the abstract was read (PubMed and the OmicsDI mirror of PubMed).

## Scope, evidence and decisions
**Status: sandbox.** 58 rows (58 runs x label-free), 38 columns. Templates: ms-proteomics + vertebrates + cell-lines, all v1.1.0.

**Design (PRIDE submitter protocol, read through the OmicsDI mirror `omicsdi.org/ws/dataset/pride/PXD014768.json`; the PRIDE API was down):**
- MDCK cells were grown with or without 20 nM estradiol for 7 days, in 5 independent flasks per group.
- One 2-D gel was run per flask: 10 gels in total (IPG pH 3-10 NL, 7 cm; 12.5% SDS-PAGE; Deep Purple stain).
- Spots that were significantly different (p < 0.05) were excised and digested in-gel. Each excised spot was run on nanoLC-ESI-Q-TOF MS/MS.
- The abstract reports "58 differentially expressed proteins", which matches the 58 deposited runs, each named `SN<spot no.>_..._FR<nn>`.
- So **one run = one 2-DE spot**. `source name` = `MDCK_2DE_spot_SN<nnn>`, with fraction identifier 1 per spot and fractionation method PRIDE:0000122 (2-DE).

**Deposited vs annotated.** The PROXI `datasetFiles` list has 174 files:
- 58 `*.mzdata.xml` (class "Associated raw file URI")
- 58 `*.mgf`
- 58 `*.mzid.gz`

The stems run FR28-FR87 with FR44 and FR80 absent, and one is `FR39x`. All 58 `mzdata.xml` files are annotated as `comment[data file]`, with none missing and none extra. The `.mgf` and `.mzid.gz` files are not rows. OmicsDI also lists the PRIDE-generated `.pride.mgf.gz` and `.pride.mztab.gz` files for the same 58 stems. No Agilent `.d` vendor raw data is deposited: the protocol says the spectra "were converted into mzData.xml using MassHunter Qualitative Analysis". The mzData files are therefore the only possible data files, as with the mzML in PXD077525.

**Instrument.** NT=6550 iFunnel Q-TOF LC/MS, AC=MS:1002783. The PX instrument field and the protocol ("6550 Q-TOF, Agilent") agree. It could not be confirmed from the mzData headers because the PRIDE FTP was unreachable.

**Search parameters.** Taken from the PRIDE data protocol (Mascot; the deposited `.mzid` could not be read):
- trypsin, 1 missed cleavage
- peptide tolerance ±0.1 Da, MS/MS ±0.5 Da
- Carbamidomethyl (C) fixed, Oxidation (M) variable; PX lists the same two modifications
- charge 2+/3+
- "standard Mascot parameters for CID", so dissociation = CID (MS:1000133)

In-gel reduction and alkylation used 10 mM DTT and 55 mM iodoacetamide (both stated).

**Cell line.** MDCK, CVCL_0422 (Cellosaurus: Female, Adult, Cocker Spaniel, kidney UBERON:0002113, kidney epithelial cell CL:0002518). Organism part, cell type, sex, developmental stage and breed come from the Cellosaurus donor record.

## Values left not available / not applicable, and why
- `characteristics[treatment]` = **not available** on every row. This is the main open point. The protocol says the spots "were excised from 2-D gels" but not from which gel, so a spot's material may come from a control gel or an estradiol gel. The design is 5 control and 5 estradiol gels. For that reason there is no `factor value` column: no factor is known per run.
- `characteristics[biological replicate]` = 1 on every row. This is a placeholder: the template forbids both reserved words, and the source flask and gel of each spot are unknown.
- Omitted: culture medium, passage number, collision energy and MS1 range, because none is stated in the protocol, and the paper's Methods were not read.

## Stated vs INFERRED
**STATED** (protocol / PX):
- 20 nM estradiol for 7 days vs control, 5 flasks or gels per group
- 2-DE, spot excision, DTT/IAA, trypsin
- 6550 Q-TOF
- Mascot settings
- 58 differentially expressed proteins

**INFERRED:**
- One file = one excised spot. This rests on SN = spot number and on 58 files matching 58 proteins.
- The MDCK subline is parental MDCK (CVCL_0422), not MDCK-I or MDCK-II. The 2019 paper's cell source was not read. The same lab's PMC10697849 (CSBJ 2023) says "MDCK ... cells (ATCC; Manassas, VA)".
- Data acquisition is DDA (Q-TOF MS/MS product-ion spectra searched with Mascot).
- Donor attributes come from Cellosaurus.

## Conflicts / caveats
- No conflict between PX, the protocol and the abstract.
- What was not available:
  - **Paper and data files.** The paper full text (Table 1 of spot numbers, fold changes, and the gel the spots were excised from) could not be retrieved. The `.mzid` / mzData headers were not readable because the EBI FTP and API were down.
  - **Ontology checks.** OLS was down. Terms were checked as follows:
    - Ontobee: CL:0002518 "kidney epithelial cell", UBERON:0002113 "kidney"
    - pride_cv.obo (GitHub, 2026-11-23): PRIDE:0000122
    - unimod.xml bundled with sdrf_pipelines: UNIMOD:4 and UNIMOD:35
    - Cellosaurus: CVCL_0422
    - PX record: MS:1002783 and NCBITaxon:9615
    - PRIDE:0000627 / 0000608 / 0000599, MS:1000133 and MS:1001251 were not rechecked today. They are reused from validated campaign files (for example PXD045313, PXD063568).
- `parse_sdrf validate-sdrf --use_ols_cache_only` passed under the default and under each `--template` (ms-proteomics, vertebrates, cell-lines). The check is structural only, because the OLS extras are not installed.
- Evidence and the build script: `/home/claude/bangkok3/scratch/PXD014768/` (`proxi_summary.txt`, `omicsdi_protocols.txt`, `cellosaurus_CVCL_0422.txt`, `stems.txt`, `sources_tried.txt`, `build.py`).

**To upgrade to annotated:** the paper's Methods and Table 1, or the authors, stating which gel or group each spot was excised from. Re-reading the mzData/mzid headers would also confirm the instrument and search settings.

## Review status
pending
