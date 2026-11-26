# PXD062512: sandbox brief

**Dataset:** Effect of sacha inchi  shell extract treatment on colorectal cancer cell for proteomic. Bangkok (bangkok-2).

**Status:** draft, not reviewed. It is in `sandbox/` because: Only SCIEX mzML files (converted from WIFF) and .timeseries.data are deposited. The original .wiff files are not, so there is no vendor RAW data file. The untreated controls analysed in the paper are also not deposited.

## Evidence and decisions
annotated 6/6.

HCT116 (100 ug/mL) and HT29 (450 ug/mL) treated 24 h with sacha inchi shell extract, triplicates SII-HCT1-3 / SII-HT1-3. Untreated controls analysed in paper but NOT deposited. Only mzML + .timeseries.data deposited (WIFF not deposited); mzML used as data file. Instrument X500R QTOF per mzML header (PRIDE TripleTOF 5600 overridden). PEAKS 5 ppm/0.1 Da (paper; PRIDE says 50 ppm), carbamidomethyl fixed, acetyl K, deamidation NQ, ox M, pyro-glu var. DTT/IAA. IJMS 2026 PMC12785288. Factor: cell line (only treated arms deposited).

SDRF file(s): . Built with `sdrf-tools build` and validated with `parse_sdrf validate-sdrf`; warnings are free-text values only.
