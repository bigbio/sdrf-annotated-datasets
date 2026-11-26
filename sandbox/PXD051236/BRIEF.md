# PXD051236 SDRF annotation report

## Study
Placenta-derived Extracellular Vesicles in Maternal Plasma of Hb Bart's Fetuses. The paper is Chaemsaithong P et al., Sci Rep 2025;15:41140, DOI 10.1038/s41598-025-24900-0, PMID 41266492. No PMCID was shown on the publisher page. The preprint is Research Square rs-4163008/v1 (17 Apr 2024).

## Scope, evidence and decisions
**Status: sandbox.** The SDRF has 139 rows: 139 `.wiff` runs from 24 maternal-plasma EV donors, label-free, with 1 row per run.

**Deposited vs annotated.** The ProteomeCentral PROXI record (`resultType=full`, accession checked in the payload) lists 407 files. The OmicsDI PRIDE mirror lists the same set.
- 139 `.wiff` + 139 `.wiff.scan` = 278 RAW. Each pair counts as one run, and `comment[data file]` is the `.wiff`. Every `.wiff` has its `.wiff.scan`.
- 127 `.mzXML` peak lists are not annotated (vendor RAW only).
- 2 ProteinPilot `.group` search results are not annotated: `All_3_gr_add_PLAP.group` and `allcontrolBartNonbart_IDA1234.group`.
- Annotated = 139/139 `.wiff`. None were excluded.

**Runs per donor.** The file names encode group, donor number and run (`<Group><n>_<IDA|SWATH><k>.wiff`). There are 3 groups of 8 donors:
- Bart: 3, 7, 20, 23, 24, 26, 33, 55
- NonBart: 2, 4, 10, 13, 19, 25, 34, 36
- Control: 16, 17, 18, 21, 22, 28, 29, 43

Each donor has SWATH1-2 and IDA1-4, with three exceptions: Bart20 has IDA1-3 only, and Bart23 and Bart24 have IDA1-2 only. That gives 91 IDA (DDA) and 48 SWATH (DIA) runs.

**Encoding.**
- `source name` and `individual` = donor code (e.g. `Bart3`). Biological replicate = 1 (one donor per source).
- `comment[technical replicate]` is numbered sequentially per donor: IDA1-4 → 1-4 and SWATH1-2 → next numbers. This keeps the (source, bio rep, tech rep, fraction) key unique, following PXD005749/PXD029805. The acquisition-method column separates DDA from DIA.

**Group and disease (INFERRED; the main open point).** The group labels Bart / NonBart / Control are STATED only in the file names. No source defines "NonBart" or "Control", or maps the donor numbers to clinical data.
- Bart → `characteristics[disease]` = Hb Bart's hydrops fetalis (MONDO:0015579). This is the fetal condition carried by the pregnancy; the plasma is maternal. The Bart group may include fetuses without hydrops (the paper has both subgroups), and this cannot be split.
- Control → `normal`. This is INFERRED from the study design.
- NonBart → `not available`. In the preprint, Group 1 ("control") is defined as at-risk couples whose fetus proved non-Bart. In the paper, Group 5 is non-Bart hydrops. "NonBart" could be either, so it was not guessed.
- The literal group label is carried in `characteristics[phenotype]` and `factor value[phenotype]`. That column is licensed by clinical-metadata.

**Deposit does not match the publication (conflict, unresolved).** The paper and the PRIDE data-processing protocol describe:
- 18 women in 5 groups: normal 6, Bart hydropic 3, Bart non-hydropic 4, disease comparator 3, non-Bart hydrops 2;
- 2 technical replicates each;
- 36 IDA and 36 DIA files.

The deposit has 24 donors in 3 groups, up to 4 IDA runs each, and 48 SWATH runs. The `.group` file names ("allcontrolBartNonbart", "All_3_gr") also point to a 3-group analysis. The deposit appears to be a different or earlier sample set than the one published. All deposited runs were annotated as deposited.

The mzXML names `X_IDA3-X_IDA1.mzXML` and `X_IDA4-X_IDA2.mzXML` suggest that IDA3/4 may be re-injections of IDA1/2. Because this is not documented, they are kept as separate technical replicates.

**Instrument (conflict).** The PX structured field and the campaign cache say TripleTOF 5600 (MS:1000932). The PRIDE sample protocol, the paper and the preprint all say TripleTOF 6600+. The SDRF uses NT=TripleTOF 6600+;AC=MS:1003456, following the precedence paper > PX field.
- The `.wiff` headers could not be read: the shell has no network, and the FTP/HTTPS mzXML fetch was blocked (robots).
- The protocol's "resolution 35,000/30,000" and 157 variable windows are consistent with a 6600+.

**Acquisition and search.**
- IDA: top-30, TOF-MS 350-1250 m/z. SWATH: 157 variable windows of 7 m/z (1 m/z overlap) over 350-1500 m/z, with TOF-MS 100-1500 m/z.
- Rolling CE with 15 eV spread. Dissociation is beam-type CID (MS:1000422) and the MS2 analyzer is TOF.
- Trypsin. ProteinPilot 5.0.2.0 with Cys alkylation by iodoacetamide → Carbamidomethyl C (UNIMOD:4), entered as Fixed. Alkylation reagent = IAA (PRIDE:0000599).
- Sample: maternal EDTA plasma → EVs by ultrafiltration + SEC. `organism part` = blood plasma (UBERON:0001969). `sex` = female.
- `developmental stage` = adult, from the stated inclusion of women aged 18 or older.

**Values left not available / not applicable.**
- `cell type` = not applicable (acellular plasma EVs).
- `age` and `ancestry category` = not available: no per-donor data.
- `disease` for NonBart = not available (see above).
- `reduction reagent` = not available. Samples were "reduced" with no reagent named. The Laemmli lysis buffer contains beta-mercaptoethanol, but it is not stated as the reduction step.
- Precursor and fragment tolerances were omitted: ProteinPilot has no user tolerance, and "100 ppm" is an acquisition setting.
- Gestational age at sampling: per-donor values were not available.

**Ontology accessions checked live.** EBI OLS returned upstream errors throughout this session, so terms were checked elsewhere:
- Ontobee: MS:1003456, MS:1000932, MS:1000422, MS:1001251, MONDO:0015579, UBERON:0001969.
- HUPO-PSI psi-ms.obo: MS:1000084.
- PRIDE-Utilities pride_cv.obo: PRIDE:0000450, PRIDE:0000599, PRIDE:0000627.
- UNIMOD:4 from the sdrf-pipelines unimod.xml.

**Validation.** `parse_sdrf validate-sdrf --use_ols_cache_only` passed with templates ms-proteomics, human and clinical-metadata (each separately and as a union). The ontology cache is not installed, so this is a structural check only.

**Files.**
- SDRF: PXD051236.sdrf.tsv (139 × 33).
- Built by `/home/claude/bangkok3/scratch/PXD051236/scripts/build_PXD051236.py` from `px_files_ordered.txt`. The 407 names were transcribed from the PROXI payload and cross-checked by the pair and extension counts.

## Review status
pending
