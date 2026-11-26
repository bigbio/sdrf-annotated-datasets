# PXD053297 annotation blocked (out of scope: nucleoside LC-MS/MS)

**Status:** blocked. This dataset is outside SDRF-proteomics scope.

PXD053297 (tRNA modification profile of a P. aeruginosa UCBPP-PA14 transposon insertion mutant library; Sun et al., Nucleic Acids Res 2025;53(14):gkaf696, doi:10.1093/nar/gkaf696, PMID 40716780, PMC12300143) holds no protein or peptide mass spectrometry. The paper's Data availability statement cites PXD053297 explicitly. The MS data come from a high-throughput ribonucleoside screen of the 5,746/5,764-strain library:
- tRNA was purified by robotic magnetic-bead size selection.
- It was hydrolysed with benzonase, CIAP and phosphodiesterase I ([15N]5-dA internal standard).
- Runs used a UHPLC (Waters BEH C18, Agilent 1290 Infinity II) with an Agilent 6495 triple quadrupole, in dynamic MRM mode for 63 modified ribonucleosides plus neutral-loss scans (132/146 Da).
- Processing used MassHunter Qual/Quant and R. Peak areas were normalised to the canonical-nucleoside UV signal.

The SDRF-proteomics templates assume protein/peptide samples, with cleavage agent, peptide modification parameters and so on. None of that applies to RNA hydrolysates measured by nucleoside MRM. The study also has thousands of mutant strains, but the deposit offers no per-run sample key: one `Raw.zip` and one `results_peak_area.xlsx`.

**Evidence checked:**
- **ProteomeCentral PROXI record** (`resultType=full`): instrument MS:1000937 6495C Triple Quadrupole LC/MS. Keywords: tRNA modification, UCBPP-PA14, MRM, LCMS. Modifications: "No PTMs are included in the dataset". Summary term: MS:1002857 "Unsupported dataset by repository".
- **Deposited files:** `Raw.zip` (the only raw file, so the campaign cache of 1 RAW is confirmed), `results_peak_area.xlsx` and `checksums.txt`. The archive contents could not be listed: the PRIDE v3 API was rate-limited and the PRIDE FTP mirror was unreachable.
- **PMC12300143 Methods** (RNA hydrolysis, Dynamic MRM, Neutral loss scan, LC-MS data processing) **and Data availability:** no protein digestion or peptide MS. "Protein" appears only in the STRING/bioinformatics network context.
- **Scratch:** `/home/claude/singapore1/scratch/PXD053297/`.

**To unblock:** not applicable under the proteomics templates. A future SDRF template for small-molecule or nucleoside (epitranscriptomics) MS would be needed.
