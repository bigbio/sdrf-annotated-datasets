# PXD023270 annotation blocked (TMT channel-to-sample map not public)

PXD023270 has one genuine Thermo RAW file, a single TMT6plex anti-crotonyllysine (Kcro) enrichment run. It compares 3 control and 3 PaACLB1-B2-silenced petunia corollas.

**Why it is blocked.** No public source ties any TMT channel to the silenced or control group:
- The paper (Physiol Plant 2022, PMID 36193016) is closed access, and its supplementary files could not be retrieved.
- The deposited MaxQuant output names the channels only "Reporter intensity 0..5", and `mqpar.xml` has no experiment names.
- The related J Exp Bot 2020 study (PXD015480) gives a table column order for different runs, not a channel map for this run.
- The data do not settle it either. ATP-citrate synthase crotonyl-site signal is higher in 126–128 than in 129–131, but channels 127 and 130 do not cluster cleanly with either group across all sites.

**Technical values verified** (ready for a future SDRF):
- **Instrument:** Q Exactive HF-X (MS:1002877), from the raw header. PRIDE and the protocol say Q Exactive Plus.
- **Search settings:** from the deposited MaxQuant search:
  - Trypsin/P;
  - 4.5 ppm precursor and 0.02 Da fragment tolerance;
  - TMT6plex fixed on K and peptide N-term, and Carbamidomethyl (C) fixed;
  - Crotonyl (K) (UNIMOD:1363; +68.026 Da confirmed from peptide masses), Acetyl (protein N-term) and Oxidation (M) variable.
- **Acquisition:** HCD at NCE 28, DDA.
- **Sample characteristics:** *Petunia x hybrida* corolla, study sample.

**To unblock:** the channel layout for TMT126–131, from the paper's supplementary site table or from the authors / service provider.
