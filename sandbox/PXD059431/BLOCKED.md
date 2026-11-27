# PXD059431 annotation blocked (TMTpro channel-to-sample map not public)

PXD059431 is a TMTpro 16-plex TurboID proximity-labelling experiment in mouse beige adipocytes. It compares empty vector with TurboID-ALN, and Fig. S3B adds a norepinephrine-treated arm.

**Why it is blocked.** No public source gives the TMTpro channel-to-sample map:
- The paper (PMC12137002) and its supplements contain no layout. mmc1 holds Figures S1–S6, and Fig. S3B lists peptides only. mmc2 is RNA-seq. mmc3 is figure source data with no Fig. 3B / S3B sheet.
- The deposited mzIdentML files are PSM lists only, with no reporter-ion or sample-group information.
- The only external repository the paper cites is GEO GSE268770, which is unrelated RNA-seq.

Writing SDRF rows would therefore mean inventing sample identities.

**Technical values already verified** (ready for a future SDRF):
- **Raw files:** two genuine Thermo files.
  - The raw headers give the instrument as Orbitrap Eclipse (MS:1003029). PRIDE lists Orbitrap Fusion.
  - The methods are "60min_Pro16_hrMS2_FAIMS" and "150min_Pro16…".
  - Both files carry the same facility sample ID, tc-1034 (suffixes RC and QIP), so they may be two injections of one plex.
- **Labels and modifications**, from the mzIdentML search parameters:
  - TMTpro (UNIMOD:2016) on K and peptide N-term, fixed
  - Carbamidomethyl (C), fixed
  - Oxidation (M), variable
- **Search and acquisition:** Trypsin; 50 ppm precursor and 0.02 Da fragment tolerance; HCD at 36% NCE with Orbitrap MS2; DDA.

**To unblock:** the submitters' TMTpro layout for tc-1034, i.e. which of the 16 channels hold empty-vector or TurboID-ALN cells, basal or NE treatment, replicate numbers and unused channels. Also needed: whether the two raw files are re-injections of the same plex.
