# PXD002757 annotation blocked

PXD002757 (Fatima et al., "CD5 molecule-like and transthyretin as putative biomarkers of chronic myeloid leukemia", Sci Rep 2017 7:40943, doi:10.1038/srep40943, PMID 28117336; the paper cites PXD002757 in its Abstract and Results) is a gel-based plasma study. Plasma from 50 healthy controls and 32 chronic-phase CML patients was run on 2DE (IPG pH 4-7, 12% SDS-PAGE, colloidal Coomassie). Spots were digested in-gel with trypsin (TCEP/IAA) and identified by MALDI-TOF PMF on a Bruker Ultraflex III. The search was Mascot with carbamidomethyl C fixed, oxidation M variable, and 50-100 ppm tolerance. According to the paper, about 1300 spots were analysed "from the pooled control and the individual CP-CML samples".

**Deposited (FTP listing and README.txt, re-derived; PROXI agrees):** 8 single-spot MALDI acquisitions. Seven are flexAnalysis/Bruker raw zips (`SAMPLE10529-9-12.zip`, `SAMPLE11129-9-12.zip`, `SAMPLE11429-9-12.zip`, `SAMPLE14429-9-12.zip`, `SAMPLE14929-9-12.zip`, `SAMPLE15629-9-12.zip`, `SAMPLE2337-10-12.zip`, i.e. spots 105/111/114/144/149/156 of 29-9-12 and spot 233 of 7-10-12) and one is `Spectrum.mzXML` (spot 83). Each has a peaklist (`peaklist*.xml`), `Spectrum_<spot>.mgf/.tsv`, a Mascot `.dat` and a one-protein FASTA. The FASTAs cover the 8 proteins the paper validated: AACT, A1AT, CD5L, STIP1, TTR, VDBP, FGG and HP (`sequence.fasta`, INFERRED). There are also two gel images: `CPCML.png` and `normal healthy control.png`.

**Why blocked: the run → sample/condition key is unknown.**
- In README.txt, the MAPPINGS column links each of the 8 Mascot searches to BOTH gel images (IDs 0 and 1). So the submission does not say whether a spot was cut from the pooled-control gel or from a CP-CML patient's gel. If it came from a patient gel, it also does not say which patient.
- Paper Table 3 and Fig. 1 label spots as N1a-d / L1a-g, etc. These labels do not correspond to the deposited Dymension spot numbers (83, 105, ...). No table in the paper links the two numbering schemes.
- The 8 runs are therefore spot identifications of one protein each, with no defensible disease, individual or pool status. Every `characteristics[disease]`/source value would have to be guessed. `not available` for disease across all rows would give an SDRF with no biological content.
- `peaklist.xml` header (flexAnalysis 3.3.80.0, 2012-09-11) carries no sample name.
- I did not open the raw zips or the Mascot `.dat` files (the browser downloads them instead of rendering them). A `.dat` COM/title line could hold a sample name. That is the first thing to check if someone can read them.

**Evidence checked:** PROXI full record (2024-10-22 revision); PRIDE FTP directory listing and README.txt; `peaklist.xml`; Nature article full text and Table 3 (cloud browser). I did not reach Europe PMC (rate-limited), and the PRIDE v3 API was not used (down).

**To unblock:** the spot-number → gel (pooled control vs CP-CML patient ID) mapping, either from the authors or from the Mascot `.dat` headers / raw `.zip` acquisition metadata. With it, an 8-row SDRF (MALDI PMF, ultraflex III, SDS-PAGE fractionation `PRIDE:0000568`, trypsin, CAM C fixed / Ox M variable) is straightforward.

**Status:** blocked. Review status: pending.
