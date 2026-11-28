# PXD002231 annotation blocked (15N metabolic-label reference cannot be built)

PXD002231 is the PTSD mouse-model brain proteome study: "Fluoxetine Treatment Rescues Energy Metabolism Pathway Alterations in a Posttraumatic Stress Disorder Mouse Model" (PMID 27606320, doi:10.1159/000445377). PRIDE marks it as a `PARTIAL` submission.

**The design is resolved. Only the label encoding blocks the SDRF.**

- **Two RAW files.** Both are genuine Thermo LTQ Orbitrap files: `cyk_20140122_ACC_SV_cyto_01.RAW` and `_02.RAW`. They are two SDS-PAGE gel slices of one sample: ACC, shock + vehicle, cytosolic fraction, pooled from 5 male adult C57BL/6NCrl mice.
- **Two samples per run.** Every run mixes the 14N sample with an equal amount of a 15N-labelled mouse-brain internal reference. Quantification is the 14N/15N ratio.
- **Correct SDRF.** It has two rows per RAW file: the sample as `15N light` (PRIDE:0000885) and the reference as `15N heavy` (PRIDE:0000884).
- **Why it cannot be built.** The SDRF builder used for agent-assisted annotation (sdrf-skills `sdrf-tools build`) recognises only TMT, iTRAQ and SILAC labels as channels. It treats the 15N rows as two label-free sources claiming one file and refuses.
- **What is not done.** Dropping the reference row to force a build would misdescribe the experiment, so no SDRF is emitted.
- **What is ready.** The sample and technical model is prepared: 4 rows, ms-proteomics + vertebrates. Settings come from the raw headers (DDA top-5, Orbitrap MS1 at R=60000 over 380–1600 m/z, ion-trap CID at NCE 35) and the paper.

**Other notes**
- The two deposited `.srf` search files belong to RAW files that were never deposited; they were used only to corroborate the search settings.
- The 15N search's custom −0.9997 Da shift on K/R has no UNIMOD term.

**To unblock:** builder support for metabolic `15N (light|heavy)` channels, or a hand-curated SDRF using that layout.
