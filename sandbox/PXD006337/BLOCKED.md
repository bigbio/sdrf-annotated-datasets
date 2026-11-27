# PXD006337 annotation blocked (dimethyl duplex labels not supported by the SDRF builder)

PXD006337 is a reductive dimethyl duplex study of human platelets. In each run, the saline control is the light label and the thrombin-stimulated sample is the heavy label.

**The design is resolved. Only tool support blocks the SDRF.**

- **Two RAW files.** Both are genuine Thermo files (Orbitrap Elite ETD, from the raw headers; this agrees with PRIDE and the protocol). They are two runs of the same light/heavy mixture: one unenriched and one TiO2 phospho-enriched.
- **Correct SDRF.** It has two rows per RAW file:
  - the saline control as `DIMETHYL0` (PRIDE:0000848);
  - the thrombin sample as `DIMETHYL6` (PRIDE:0000851).
- **Why it cannot be built.** The SDRF builder used for agent-assisted annotation (sdrf-skills `sdrf-tools build`) recognises only TMT, iTRAQ and SILAC labels as channels. It therefore refuses one data file claimed by two samples. This is the same limitation that blocks 15N metabolic-label datasets.
- **Already checked once the builder supports dimethyl.** A build with dimethyl channel support patched in locally passes `parse_sdrf validate-sdrf` (ms-proteomics + human), `sdrf-tools structure` and `reconcile`.

**Other notes**
- Search settings come from the deposited pep.xml (Proteome Discoverer 1.4 / Mascot):
  - Carbamidomethyl fixed;
  - variable Acetyl (protein N-term), Gln->pyro-Glu, Oxidation, Dimethyl and Dimethyl:2H(4)13C(2) (K and N-term), and Phospho (S/T/Y);
  - 10 ppm precursor and 0.7 Da fragment tolerance.
- CID at NCE 35 and ion-trap MS2 come from the raw method and the protocol.
- DIMETHYL6 is used for the 13C2D4 heavy label (+6.0318 Da), following the curated corpus; PRIDE defines it as +6.0377 Da.
- The paper's full text could not be retrieved, so disease, age, sex, ancestry and individual would be not available.

**To unblock:** builder support for `DIMETHYL0`/`DIMETHYL4`/`DIMETHYL6` (and 15N) channels in sdrf-skills, or a hand-curated SDRF using the layout above.
