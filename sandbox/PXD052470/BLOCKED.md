# PXD052470 annotation blocked (TMT channel-to-sample map not public; partial fraction deposit)

PXD052470 is a TMT multiplex of 12 samples: 4 fetal stages × 3 fetuses.

**Why it is blocked.** No public source maps TMT channels to samples:
- The paper and its supplementary files do not give the map.
- The PRIDE files and the Europe PMC supplementary material do not give it either.
- The Data Availability statement names only PRIDE.

**The deposited files are also misleading.** The 4 RAW files are genuine Thermo files (the raw headers give Q Exactive, MS:1001911). They are named 75d/85d/95d/105d, but most likely they are high-pH fractions 4–7 of one TMT mixture, not one file per stage:
- **Original names in the raw headers:** `140375-4` to `140375-7`, vials GB4–GB7, all acquired on 2014-08-28 in one sequence.
- **LC method:** the gradient changes from RP1 to RP2 between "85d" and "95d", as is usual between early and late fractions.
- **Peptide overlap:** in the deposited MaxQuant results, only adjacent files share peptides (24/28/12), and "75d" and "105d" share none.

So the file names do not identify stage samples. About 16 of the 20 fractions are not deposited (PRIDE marks the submission PARTIAL).

The deposited MaxQuant 2.5.2 search used no TMT label and identified only about 1–2% of spectra. The paper and PRIDE describe a Proteome Discoverer 1.4 search instead.

**To unblock:** deposit all fraction RAW files together with a channel-to-sample table, or a Proteome Discoverer study file with sample annotations.
