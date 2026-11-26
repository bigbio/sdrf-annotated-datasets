# PXD048805 annotation blocked (out of scope: nucleoside LC-MS/MS)

**Status:** blocked. This dataset is outside SDRF-proteomics scope.

PXD048805 (Bartonella henselae Houston I and B. quintana Toulouse tRNA modification mapping; Quaiyum, Sun et al., Front Microbiol 2024;15:1369018, doi:10.3389/fmicb.2024.1369018, PMID 38544857, PMC10965804) holds no protein or peptide mass spectrometry. The MS data are targeted LC-MS/MS of ribonucleosides. Small RNA was extracted with Trizol and the PureLink miRNA kit, then hydrolysed to nucleosides with benzonase, CIAP and phosphodiesterase I (with a [15N]5-dA internal standard). It was run on an Agilent 1290 and Agilent 6495 triple quadrupole in MRM mode. Signals were normalised to the UV of the four canonical ribonucleosides (paper section 2.3). The paper states "The MS data was deposited in the PRIDE database with the accession number PXD048805", so the PX record links the correct paper.

The SDRF-proteomics templates assume proteins/peptides, with cleavage agent, peptide modification parameters and protein-level sample metadata. None of that applies to enzymatic RNA hydrolysates measured by nucleoside MRM. Writing one would require fabricating or mis-using required fields.

**Evidence checked:**
- **ProteomeCentral PROXI record** (`resultType=full`): instrument MS:1000937 6495C Triple Quadrupole LC/MS. Modifications: "No PTMs are included in the dataset". Summary term: MS:1002857 "Unsupported dataset by repository". Keywords: tRNA modification, mass spectrometry, NGS. Publication shown as "pending".
- **Deposited files:** `BH_LC-MS_data.zip` (the only raw file, so the campaign cache of 1 RAW is confirmed) and `BH_BQ_LC-MS.txt` (results). The archive contents could not be listed: the PRIDE v3 API was rate-limited and the PRIDE FTP/HTTPS mirror timed out.
- **PMC10965804 Methods 2.2–2.3 and Data availability:** no protein digestion, peptide LC-MS or proteomics. "Protein families" appear only in the bioinformatics section.
- **Scratch:** `/home/claude/singapore1/scratch/PXD048805/`.

**To unblock:** not applicable under the proteomics templates. Two things would change this: a future SDRF template for small-molecule or nucleoside (epitranscriptomics) MS, or evidence that `BH_LC-MS_data.zip` contains peptide runs (contradicted by the paper and the PX record).
