# PXD076093 annotation blocked (out of scope: nucleoside LC-MS/MS)

**Status:** blocked. This dataset is outside SDRF-proteomics scope.

PXD076093 (PLP-dependent biosynthesis of aminovaleramide by AvaS in tRNA; Sun et al., Nat Chem Biol 2026, doi:10.1038/s41589-026-02303-0, open access) holds no protein or peptide mass spectrometry. The paper's Data availability statement cites PXD076093 for the MS data generated in that study. It also points to PXD053297 for the earlier PA14 library screen. The MS data are ribonucleoside analyses of tRNA hydrolysates:
- **LC-QQQ MRM:** k2C m/z 372→240 and ava2C m/z 342→210, normalised to rC UV. Samples were PA14 WT and ΔavaS, E. coli K12 ± pET21b-avaS, purified tRNA^Ile2/Met/fMet/Ile, AvaS site-directed mutants, the in vitro AvaS/PLP assay and the dual-reporter assay.
- **High-resolution LC-QTOF MS1/MS2:** used to identify the N341 nucleoside against synthetic ava2C and inm5U standards (Fig. 1b, Extended Data Fig. 1).

The SDRF-proteomics templates (cleavage agent, peptide modification parameters, protein-level samples) do not apply.

**Evidence checked:**
- **ProteomeCentral PROXI record** (`resultType=full`): instrument MS:1000937 6495C Triple Quadrupole LC/MS. Keywords: QQQ, ava2C, RNA modification, avaS, tRNA. Modifications: "No PTMs are included in the dataset". Summary term: MS:1002857 "Unsupported dataset by repository". The species is given as E. coli (562), although the study is mainly on P. aeruginosa PA14 (AvaS was expressed in E. coli K12).
- **Deposited files:** 4 raw zips, so the campaign cache of 4 RAW is confirmed: `Raw_avaS_mutagenesis.zip`, `Raw_QQQ.zip`, `Raw_dula_reporter_assy.zip` (sic) and `RAW_HRM_QTOF.zip`. There are also 2 results files: `Results_peakarea_avaS_mutagenesis.xlsx` and `Results_peakarea_dual_reporter_assay.xlsx`. The archive contents could not be listed: the PRIDE v3 API was rate-limited and the PRIDE FTP/HTTPS mirror timed out.
- **Nature Chem Biol full text** (nature.com): searching the page for "trypsin" returns 0 hits. "proteom" appears only in the ProteomeXchange data statement. The QTOF data are nucleoside high-resolution MS, not intact or peptide protein MS.
- **Scratch:** `/home/claude/singapore1/scratch/PXD076093/`.

**To unblock:** not applicable under the proteomics templates. Either a future SDRF template for small-molecule or nucleoside MS is needed, or proof that `RAW_HRM_QTOF.zip` contains protein/peptide runs (the paper indicates otherwise).
