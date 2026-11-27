# PXD060864: annotation blocked

PXD060864 accompanies Sun et al., "Hybrid hydrogel–extracellular matrix scaffolds identify biochemical and mechanical signatures of cardiac ageing", Nat Mater 24:1489–1501 (2025), doi:10.1038/s41563-025-02234-6, PMID 40506498, PMC12404999. The paper's Data availability section cites PXD060864. The study is a TMT-based quantitative proteomics comparison of decellularized cardiac ECM (SDC + DNase-I) from young (2 months) and aged (24 months) female C57BL/6J mice. Fig. 3d,e gives N = 3 biological replicates per condition. BGI Genomics did the extraction, TMT labelling, Shimadzu LC-20AB fractionation and LC-MS/MS. Search and analysis used BGI's Dr. Tom platform.

No defensible SDRF can be written, for four reasons:
- **No channel → sample map.** The Methods say only "labelled with a tandem mass tag". They name no plex (TMT6/10/16), no channel assignment and no sample names. The PX record is also silent: "No PTMs", and its description is only the abstract.
- **No raw file names.** The 5 "RAW" entries are bundles (`Rawdata_1.tar` … `Rawdata_5.tar`, 2.8–2.9 GB each). `Rawdata.md5` lists only the bundles, as `Rawdata_N.tar.gz`, not their members. The number and names of the Thermo `.raw` fractions inside could not be read, so `comment[data file]` cannot be filled without fabricating it.
- **Deposited outputs unreadable here.** `protein.tsv` (1.6 MB) is the only file that might carry sample or channel column names. In the cloud browser it starts a download and opens no page, and WebFetch is blocked by robots. `24NP0877_1_all.mgf` (3.0 GB, BGI project id 24NP0877) was not opened.
- **Search parameters unstated.** Tolerances, modifications (TMT and carbamidomethyl implied by DTT/IAA but not listed), missed cleavages and NCE are all absent.

**Conflict noted:** PX lists the instrument as `Q Exactive` (MS:1001911). The paper says "Thermo Scientific Q-Exactive HF X". The raw headers were not readable to settle it. The campaign cache ("5 RAW / 8 files, Q Exactive") has the right file count (8), but the 5 "RAW" are tar bundles, not runs, and its instrument comes from PX, which disagrees with the paper.

**Evidence checked:**
- ProteomeCentral PROXI `PXD060864?resultType=full`. The first response showed a different PXD (shared browser) and was discarded; the re-fetch was verified.
- PRIDE FTP directory listing and `Rawdata.md5` (http; the https endpoint timed out).
- PRIDE v3 `files/all` (down).
- Nature full text: Methods (tissue, decellularization, mass spectrometry, bioinformatics), Fig. 3 legend, Data availability.
- Nature Source Data Fig. 3 / Extended Data Fig. 1 xlsx: robots-blocked, download-only.
- PMC12404999: reCAPTCHA interstitial.
- Europe PMC REST: upstream error.

Payloads are saved in `/home/claude/singapore2/scratch/PXD060864/`.

**To unblock:**
1. List the members of each `Rawdata_N.tar` (HTTP-range read of the 512-byte tar headers) to get the `.raw` names and fraction count, and read a RAW header to settle QE vs QE HF-X.
2. Read the header row of `protein.tsv`, and Source Data Fig. 3 / Extended Data Fig. 1, for sample and channel column names.
3. Otherwise get the TMT plex and channel layout (3 young + 3 aged dECM) and the BGI search parameters from the authors (corresponding author J. L. Young, Mechanobiology Institute, NUS).

If (1) and (2) yield an explicit channel map, the dataset becomes annotatable: one TMT plex × N fractions, organism Mus musculus, organism part heart (decellularized ECM), female, C57BL/6J, age 2 months vs 24 months, DTT/IAA, trypsin.
