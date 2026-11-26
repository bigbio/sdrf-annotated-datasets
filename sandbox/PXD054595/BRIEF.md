# PXD054595: sandbox brief

**Dataset:** Human squamous cell carcinoma HSC-4 betaine treatment. Bangkok (bangkok-2).

**Status:** draft, not reviewed. It is in `sandbox/` because: No vendor RAW data is deposited. The files PRIDE classes as RAW are Mascot .dat result files, so the data files in this draft are the deposited .mgf peak lists. Bruker .d data would be needed to promote it.

## Evidence and decisions
annotated 18/18.

HSC-4 (CVCL_1289; male, tongue SCC) betaine 500 mM 24 h (T) vs untreated (C); C/T X-Y: X = biological, Y = technical (INFERRED from names). No vendor RAW deposited: PRIDE "RAW" files are Mascot .dat result files; data file = deposited .mgf peak lists. Instrument Bruker compact (mgf header "Instrument: compact"). Mascot params from .dat: TOL 1.6 Da, ITOL 0.8 Da, carbamidomethyl C fixed, ox M var, Trypsin/P, 1 missed, charge 2-4, ESI-QUAD-TOF. IJMS 2024 PMC11476985 (no MS methods in paper).

SDRF file(s): . Built with `sdrf-tools build` and validated with `parse_sdrf validate-sdrf`; warnings are free-text values only.
