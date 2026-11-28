# PXD002202 annotation blocked (dimethyl duplex labels not supported by the SDRF builder)

PXD002202 is a reductive dimethyl duplex study of His-tagged ubiquitin pulldowns from *S. cerevisiae* BY4742.

**The design is resolved. Only tool support blocks the SDRF.**

- **Three RAW files.** All three are genuine Thermo files. The raw headers give the instrument as an LTQ Orbitrap Velos: FTMS 60k MS1 at 300–1500 m/z, then top-20 ion-trap CID at NCE 35 (DDA).
- **Correct SDRF.** It has two rows per RAW file:
  - the WT His-ubiquitin pulldown as heavy `DIMETHYL6` (PRIDE:0000851);
  - the comparison sample as light `DIMETHYL0`. The light sample is the no-bait control (05824), His-ubiquitin S65A (05830) or His-ubiquitin S65E (05831).
- **Channel map evidence:**
  - The paper's Methods and the PRIDE protocol both say WT was labelled heavy.
  - The MaxQuant experiment names (WTvsCtrl / WTvs65A / WTvs65E) and the sample names stored in the raw headers agree with this.
  - The H/L ratios in the deposited `proteinGroups.txt` reproduce the paper's Table 1 log2(WT/x) values.
- **Why it cannot be built.** The SDRF builder used for agent-assisted annotation (sdrf-skills `sdrf-tools build`) recognises only TMT, iTRAQ and SILAC labels as channels. It therefore refuses one data file claimed by two samples. The same limitation blocks PXD006337 and 15N metabolic-label datasets.
- **Already checked once the builder supports dimethyl.** A build with dimethyl channel support patched in locally passes `parse_sdrf validate-sdrf` (ms-proteomics), `sdrf-tools structure` and `reconcile`.

**Other notes**
- **Heavy label.** The measured mass spacing per label site is 6.0376 Da, which is Dimethyl:2H(6) (CD2O + NaCNBD3, as in the paper), i.e. `DIMETHYL6`.
  - The PRIDE protocol's "(13C,2H) formaldehyde" would give +8 Da and does not fit the data.
  - PRIDE's "SILAC" quantification field is also inaccurate.
- **Search settings** come from the deposited MaxQuant 1.5 output:
  - no fixed modifications;
  - variable Oxidation (M), plus the Dimethyl / Dimethyl:2H(6) labels on K and N-term;
  - fragment tolerance 0.5 Da;
  - precursor tolerance not recorded.
- **Enzyme.** Trypsin, per the paper and the protocol.
- **Open question.** It is not known whether the three WT heavy pulldowns are separate pulldowns or aliquots of one, so each run would get its own WT source name.

**To unblock:** builder support for `DIMETHYL0`/`DIMETHYL4`/`DIMETHYL6` (and 15N) channels in sdrf-skills, or a hand-curated SDRF using the layout above.
