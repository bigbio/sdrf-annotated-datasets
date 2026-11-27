# PXD059385 SDRF annotation report

## Study
Microbial Cooperative Molecular Strategies Enabling 1,2-Dichloroethane Detoxification in Low pH Aquifers (NUS, Singapore; submitter Siyan Zhao, lab head Jianzhong He). This is label-free comparative proteomics of the organohalide-respiring *Desulfitobacterium* sp. strain AusDCA, grown at pH 5.5 and pH 7.0 while dechlorinating 1,2-DCA.

**Paper:** Zhao S, Rogers MJ, Xu G, Low A, Ding C, He J. *Environ Sci Technol* 2025;59(33):17655-17665. doi:10.1021/acs.est.5c03012, PMID 40788676. There is no PMC copy and the ACS licence is not OA.
- The PX record links this DOI, and the title, authors and NUS lab match.
- The full text could not be read. pubs.acs.org served a Cloudflare human-verification challenge, which was not attempted. Europe PMC, Unpaywall and Semantic Scholar were down, rate-limited or blocked today.
- So the paper's Methods, SI and data-availability statement were NOT read. The PXD citation inside the paper is unverified, although the DOI, the PX record and the PubMed abstract (PMID 40788676) are consistent.
- The evidence used is the PubMed abstract, the PRIDE sample/data protocols (via the OmicsDI mirror, since the PRIDE API was down) and the deposited Proteome Discoverer files on the PRIDE FTP.

## Scope, evidence and decisions
Status: **sandbox**. The file has 8 rows (8 RAW, label-free) and 30 columns, with template `ms-proteomics` v1.1.0.

**Deposited vs annotated.**
- The PRIDE FTP listing (re-derived) holds 29 files, matching the PX record and the campaign cache:
  - 8 RAW: `AT_pH5.5_R1-R4.raw` and `AT_pH7_R1-R4.raw`, 1.3-1.6 GB each.
  - The PD result set: `AUSDCA_Acid.msf` 1.1 GB, `.msfDetails` 5 GB, the views, `.pdResult*`, `AUSDCAA.pdStudy` and `.pdStudy.bak`.
  - 11 PD text exports.
- No README or checksum file is present.
- All 8 RAW are annotated, so no run is left out.

**Run to condition.**
- The deposited file names state pH (5.5 or 7) and replicate (R1-R4).
- The PRIDE sample protocol states "Proteomic expression profiles under pH 5.5 and pH 7.0 by strains AusDCA". The abstract names pH 5.5 as the acid-stress condition.
- The map is therefore STATED by file name. `characteristics[growth condition]` / `factor value[growth condition]` = `pH 5.5` / `pH 7.0`.

**Discrepancy in the deposited search (important).**
- The PD study (`AUSDCAA.pdStudy`, `AUSDCA_InputFiles.txt`, `AUSDCA_StudyInformation.txt`, `AUSDCA_ResultStatistics.txt`) searched **10** RAW, named `AT11.raw`-`AT20.raw`. They were acquired on an Orbitrap Fusion, 23-24 Oct 2023, PD 3.1.0.638.
- Only 8 RAW were deposited, all renamed. The PD study has no sample groups or factors (`<Factors />`, empty Sample Group). Nothing in the deposit maps `AT1x` to `AT_pHx_Ry`. Two searched runs were not deposited, and which two is unknown.
- This does not affect the SDRF rows, which use the deposited names. It does mean the deposited `.msf`/text exports cannot be tied to SDRF rows file-by-file.
- The exact byte sizes of AT11-AT20 are recorded in the pdStudy, but the FTP listing gives only rounded sizes, so I could not match them. With exact FTP sizes (PRIDE files API, down today) or the RAW headers, the AT1x key could be recovered.

**Organism / strain.**
- The PX species is `Desulfitobacterium sp. enrichment culture clone AusDCA-54` (NEWT/NCBITaxon:1145230). NCBI shows this is a 16S clone taxon under "Desulfitobacterium environmental samples" (parent 244201), so it is not the strain itself.
- The data protocol says the search used "the protein database annotated from complete genome of strain AusDCA". NCBI holds exactly that genome:
  - assembly GCA_051122385.1 / GCF_051122385.1, "Desulfitobacterium sp. AusDCA", strain AusDCA
  - complete genome, 1 chromosome, 4.54 Mb, submitted by NUS
  - BioProject PRJNA1143094, BioSample SAMN42994840, isolation source "acidic aquifer", Botany Industrial Park, Sydney
  - taxon NCBITaxon:3240383, rank species, verified live via the NCBI Datasets API
- I therefore used `characteristics[organism]` = `Desulfitobacterium sp. AusDCA` (NCBITaxon:3240383) and `characteristics[strain or breed]` = `AusDCA`, rather than the PX clone taxon.
- The search FASTA is `AUSDCA_Cluster1_aa.fasta`, a single-organism database. Material type is `whole organism` (cultured bacterial cells, following the PXD024983 / PXD002912 precedents). Organism part, cell type and disease are `not applicable`.

**Pure culture vs co-culture (open point).**
- The paper title says "Microbial Cooperative", which may imply a partner organism or the enrichment.
- The abstract, the PRIDE protocols ("cells of strain AusDCA were harvested ... from 30 ml cultures amended with 1,2-DCA (0.43 mM)") and the single-genome search all describe strain AusDCA alone.
- I annotated a single-strain culture. This is INFERRED, because the Methods could not be read.
- Unlike PXD024983, a complete isolate genome exists here, which supports a pure isolate.

**Technical**, from deposited PD files (authoritative) unless noted:
- Instrument: Orbitrap Fusion (MS:1002416). The PX record, the protocol ("Orbitrap Fusion Tribrid") and the PD InputFiles "Instrument Name" read from the RAW headers all agree.
- Trypsin (MS:1001251): from the PD Sequest HT node, "Trypsin (Full)", KR / not before P, up to 2 missed cleavages. Also stated in the protocol.
- Label-free (MS:1002038): stated as "label-free quantification ... Minora".
- DDA (PRIDE:0000627): INFERRED from the Sequest HT + Minora workflow on MS2 spectra.
- Precursor tolerance `3 ppm` and fragment tolerance `0.1 Da`: from the Sequest HT node in the pdStudy processing workflow `Common_Quan_Orbitrap`. (The 20 ppm / 0.5 Da values are only the Spectrum Files RC recalibration settings.) The PSM ΔM range is ±2.997 ppm, which agrees.
- Modifications, from the Sequest HT node:
  - `StaticModification1` = Carbamidomethyl C, UnimodAccession 4 -> MT=Fixed.
  - `DynamicModification1` = Oxidation M, UnimodAccession 35 -> MT=Variable.
  - No terminal modifications.
- Collision energy `30 NCE`: every PSM and MS/MS spectrum in the PD exports reports NCE 30%.
- Fraction identifier 1 (PD FractionNumber=1; no fractionation). Technical replicate 1.

## Values left not available / not applicable
- `comment[dissociation method]` = not available. The Spectrum Selector activation filter is "Any". The PD exports I could read (ResultStatistics) give NCE but not the activation type. The 0.1 Da fragment tolerance suggests Orbitrap-readout HCD, but on a Fusion CID is also possible, so I did not assert it. `AUSDCA_PSMs.txt` (27 MB) has an Activation Type column but was too large for the cloud browser.
- `comment[reduction reagent]`, `comment[alkylation reagent]` = not available. The PRIDE protocol names no reagent (freeze-thaw, sonication, trypsin, ZipTip). The deposited search sets Carbamidomethyl C as a static modification, so alkylation is assumed to have happened: `not available`, not `not applicable`. The paper Methods could not be read to check.
- Culture medium, temperature and incubation time: not recorded, because the paper Methods were unreadable. A reviewer with ACS access should add them if stated, for example as a medium in the growth condition text.
- Organism part / cell type / disease = not applicable (cultured bacterium).
- MS1 scan range: not recorded. The precursor m/z spans 350-2000 in the exports, but the instrument method was not read.

## Stated vs INFERRED
- **STATED:**
  - pH 5.5 vs 7.0 per file (file names + PRIDE protocol)
  - strain AusDCA, from the PRIDE protocols and the abstract
  - Orbitrap Fusion, trypsin, label-free / Minora, Sequest HT
  - tolerances, modifications and NCE 30 (deposited PD study/exports)
  - 1,2-DCA 0.43 mM in all cultures (PRIDE protocol)
- **INFERRED:**
  1. R1-R4 are four independent biological replicate cultures per pH (`characteristics[biological replicate]` 1-4). No document says whether they are separate cultures or repeated injections.
  2. A single-strain culture rather than a co-culture.
  3. DDA.
  4. NCBITaxon:3240383, chosen over the PX record's 1145230: inferred from the matching NUS complete genome and the "complete genome of strain AusDCA" search database.

## Conflicts
- **PX species vs organism used.** The PX record says clone AusDCA-54 (1145230). The protocol plus the NCBI genome point to strain AusDCA (3240383), and I used 3240383.
- **PD version.** The protocol says Proteome Discoverer v2.4. The deposited result files say 3.1.0.638. The deposited files win.
- **Run count.** 10 RAW (AT11-AT20) were searched, but 8 renamed RAW were deposited, and the PD study has no key between the two sets.
- **PTMs.** The PX `modifications` field says "No PTMs are included in the dataset". The search used fixed Carbamidomethyl C and variable Oxidation M, which were annotated.

## Validation
- `parse_sdrf validate-sdrf --use_ols_cache_only`, both without a template and with `--template ms-proteomics`: "Everything seems to be fine". This is structural validation only: the OLS dependencies are not installed, and OLS4 was down today.
- `sdrf_review.py`: [OK].
- Accessions:
  - The NCBITaxon IDs were verified live via the NCBI Datasets API.
  - UNIMOD 4 / 35 are confirmed by the PD `UnimodAccession` fields.
  - MS:1002416, MS:1001251, MS:1002038 and PRIDE:0000627 are identical to the campaign precedents (PXD024983) and were not re-checked live, because OLS was down.
- `characteristics[strain or breed]` and `characteristics[growth condition]` are not licensed by `ms-proteomics`. They were kept, following the bacterial precedents PXD002912 / PXD001373 / PXD024983.

Evidence: `/home/claude/singapore2/scratch/PXD059385/`:
- `px_record_summary.txt`
- `omicsdi_PXD059385.txt`
- `pubmed_40788676.txt`
- `ncbi_taxonomy_genome.txt`
- `ftp_listing.txt`
- `AUSDCA_InputFiles.txt`
- `AUSDCA_StudyInformation.txt`
- `AUSDCA_ResultStatistics_excerpt.txt`
- `AUSDCAA_pdStudy_excerpt.txt`

Build script: `/home/claude/singapore2/scripts_PXD059385/build.py`.

## Review status
pending
