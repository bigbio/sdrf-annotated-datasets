# PXD025469 annotation blocked (multi-sample SCIEX .wiff containers)

PXD025469 is an SRM quantification of Peptide 2 (RLLWENGNL) in mouse plasma on a QTRAP 6500 with Analyst 1.6.2. It is the companion of PXD025440 (Komeno et al., J Biol Chem 2021;296:100761; PMC8167299).

**The design is fully resolved; only the file layout blocks the SDRF.** Both deposited run files are multi-sample Analyst `.wiff` containers. The deposited Analyst reports (`shiga-1.pdf`, `shiga-2.pdf`) list their injections:

| data file | injections |
|---|---|
| `Mouse_plasma_assay.wiff` | 6 calibration standards, single and double blank, mice Sample01, 02, 04, 06–15 |
| `Mouse_plasma_assay-2nd.wiff` | 6 calibration standards, single and double blank, mice Sample16, 18 |

The groups come from the PRIDE data processing protocol, with 5 mice each:
- **Control, PBS-infused C57BL/6:** Samples 1, 2, 4, 16, 18.
- **db/db (BKS.Cg-+Leprdb/+Leprdb/Jcl) + PBS:** Samples 6–10.
- **db/db + dipeptidyl peptidase III:** Samples 11–15.

Every sample is spiked with stable-isotope-labelled Peptide 2.

A correct SDRF has 15 rows, one per mouse injection, with several label-free sources sharing one `comment[data file]` and distinguished by `assay name`. The SDRF builder used for agent-assisted annotation (sdrf-skills `sdrf-tools build`) rejects one vendor file claimed by several label-free sources. The only layout it accepts, one source per `.wiff`, would invent a single sample per file and merge control and diabetic mice. So no SDRF is emitted. The 15-row sample and technical model is prepared and can be built once this is supported.

**To unblock:** builder support for several label-free sources per multi-sample vendor file (one `assay name` per injection), or a hand-curated SDRF following that layout.
