# PXD071719 annotation blocked (no public TMT channel and crosslinker map)

PXD071719 is a crosslinking-MS study of a human Hb:GAPDH:Band3(1-395) mixture under normoxia and hypoxia (paper full text: PMC12923992).

**The design cannot be resolved from public sources.**

- **One RAW file.** It is a genuine Thermo file (Orbitrap Fusion Lumos, EASY-nLC).
- **Six pooled conditions.** The paper describes 3 normoxia and 3 hypoxia aliquots, each crosslinked with "either" DSSO or DMTMM, then pooled into one TMTsixplex run. The deposited mzid contains both DSSO and zero-length (DMTMM-type) crosslinks.
- **No map anywhere.** Nothing public says which TMT channel (126–131) holds which condition, or which crosslinker each channel received. The crosslinker column is required, so it cannot be left out. Sources checked:
  - the Methods and the Fig. 5G legend (no channel layout);
  - Data S1 (supplement-2.xlsx), which could not be retrieved: PMC serves it behind a proof-of-work challenge and Europe PMC returned 403;
  - the PRIDE files (raw, mzid, mzML, mgf only, with no sample sheet or quantification file);
  - Europe PMC supplementary files ("not open access").
- **No reconstruction.** Assigning channels from reporter-ion ratios was not attempted, because the result would not be public evidence.

**To unblock:** Data S1 of the paper, or a channel map from the submitters giving the condition and crosslinker for each TMT channel.
