# PXD024501 annotation blocked (iTRAQ channel-to-sample map not public)

PXD024501 has one genuine Thermo RAW file, `Hackam_ITRAQ.raw`. The instrument strings give a Q Exactive (MS:1001911), which agrees with PRIDE and the paper. It is a single iTRAQ 8-plex run of 8 rd10 mice: 4 treated with a MyD88 inhibitor and 4 with a control peptide. All 8 reporter channels (113–119, 121) carry signal.

**Why it is blocked.** No public source says which channel holds which mouse or treatment group:
- The paper (PMC8505828) gives no channel map, and Supplementary Table S1 has only group averages and ratios.
- The deposited mzid and mzML headers carry no sample or channel information, and no study or experimental-design file was deposited.
- Neither the Europe PMC supplementary files nor the Data Availability statement add one.

The map could be reconstructed by fitting per-channel reporter abundances to the Table S1 group averages. That would be an inference, not a public map, so it was not done.

**Already prepared** (for a future SDRF):
- Technical values, with every term verified in OLS4:
  - Q Exactive, DDA;
  - iTRAQ 8-plex labels;
  - search settings from the deposited mzid.
- Note that the paper gives carbamidomethyl as "+52.021 Da", which is a typo for 57.021.
- The raw method shows a 240 ms MS1 maximum injection time and a 350 nl/min flow, against the paper's 100 ms and 450 nl/min.

**To unblock:** the authors' channel-to-treatment list, or their original Proteome Discoverer result or study file.
