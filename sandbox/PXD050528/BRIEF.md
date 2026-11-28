# PXD050528 SDRF annotation report

## Study
Comprehensive Proteomic Profiling of Converted Adipocyte-like Cells from Normal Human Dermal Fibroblasts Using Data-Independent Acquisition Mass Spectrometry. Choi S et al., ACS Omega 2024 9(38):40034-40050, DOI 10.1021/acsomega.4c05852, PMID 39346858, PMC11425921. Weill Cornell Medicine - Qatar (Doha). The paper's Data Availability names PXD050528, so the PX-linked paper is correct.

## Scope, evidence and decisions
Status: **sandbox**. 48/48 deposited RAW annotated (24 DDA + 24 DIA), label-free, one row per file.

- Files: PROXI `resultType=full` record (PRIDE FTP and PRIDE API were unreachable today). 48 `.raw` files plus search outputs `Lysates_/Secretome_DDA_exclude_single.xls/.params` and `Lysates_/Secretome_DIA_exclude_single.tsv` (not opened: FTP down). Name pattern `<date>_Exploris_<DDA|DIA>_<180|120>min_iRT_<C|S>_<D|ND>_<1-6>.raw`, a full 2 x 2 x 2 x 6 grid.
- Split into `PXD050528-dda.sdrf.tsv` (ms-proteomics, human) and `PXD050528-dia.sdrf.tsv` (ms-proteomics, human, dia-acquisition), so that dia-acquisition is declared on the whole file only. Each sample's DDA and DIA runs share a source name and are told apart by file, not by technical replicate.
- Design (STATED): NHDF (Lonza CC-2511) in DMEM/10% FBS, converted with IBMX, dexamethasone, insulin and rosiglitazone (2 d), then insulin and rosiglitazone (2 d), then rosiglitazone until lipid droplets formed (Results: 28 days). Secretome came from 24 h serum-free conditioned medium. Six interday biological replicates for both the intracellular and the extracellular proteome.
- Filename decoding (INFERRED, the main open point): C = cell lysate, S = secretome (matches the deposited `Lysates_`/`Secretome_` outputs and the 2 acquisition dates); D = adipocyte-like (differentiated), ND = NHDF (not differentiated); suffix 1-6 = biological replicate. The paper never spells out these codes.
- Source names are `<NHDF|adipocyte-like>_<lysate|secretome>_<n>`. Whether lysate n and secretome n come from the same culture is not stated, so they are kept as separate sources.
- Instrument: Orbitrap Exploris 480 (MS:1003028), from the paper and the filenames. The PX record says Q Exactive. RAW headers were not read (no network for range reads).
- LC: Vanquish Neo; DIA 120 min / DDA 180 min gradients. DIA: MS1 350-1200 m/z, 35 m/z isolation windows, HCD 30%. DDA: MS1 400-1650 m/z, HCD 28%. 500 ng injected.
- Digestion: PreOmics iST kit, Lys-C and trypsin (both listed).
- Search: Spectronaut 18 directDIA and SpectroMine (DDA), 20 ppm MS/MS2. Carbamidomethyl C is Fixed, Oxidation M is Variable. The paper writes "acetylation ... of methionine" and N-terminal acetylation; this is annotated as Acetyl at Protein N-term (Spectronaut default), an INFERRED reading. The deposited `.params` files were not readable and should be checked.
- Disease: normal (commercial normal fibroblasts). Cell type: fibroblast of dermis (CL:0002551, verified live in OLS) for both arms; the conversion is carried in treatment/factor value. Organism part: dermis.

## Values left not available / not applicable
- age, sex: donor not stated in the paper (vendor lot unknown) -> not available.
- reduction/alkylation reagent: iST LYSE contains both, but the paper does not name them -> not available. The PX record lists MOD:00397 (iodoacetamide derivatized), but PX fields rank lowest, so this was not used.
- material type for secretome = `conditioned medium`: this triggers a validator WARNING (not in the enum). It was kept because `cell` would be false for the secretome.

## Conflicts
- PX instrument Q Exactive vs paper/filenames Exploris 480 -> Exploris 480.
- Figure 1 legend says 0.25 uM dexamethasone, Methods say 1 uM. Concentrations are not encoded.

## Verification and validation
- Checked live in OLS this run: CL:0002551, MS:1003028. EBI was rate-limiting or down (OLS, Europe PMC, PRIDE FTP and API all failing). The remaining accessions (UNIMOD:4/35/1, MS:1001251, MS:1001309, MS:1000422, PRIDE:0000450/0000627) were reused from accepted campaign files and were not re-checked live.
- parse_sdrf: run once per template, warnings only (material type), 0 errors. sdrf_review.py gives [OK] for both files. The OLS cache could not be read (no pyarrow), so this was a structural check only.
- Scratch: /home/claude/mideast1/scratch/PXD050528/ (files_from_proxi.txt, proxi_summary.txt). Builder script: /home/claude/mideast1/scripts_PXD050528/build.py.

## To lift to annotated
Open the PRIDE FTP and read `*_DIA_exclude_single.tsv` (condition/run columns) and `*.params` (mods) to confirm C/S/D/ND, the replicate mapping and the acetyl site. Range-read one RAW header to confirm the instrument.

## Review status
pending
