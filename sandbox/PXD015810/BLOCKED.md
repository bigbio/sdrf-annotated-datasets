# PXD015810 annotation blocked (no public TMT channel-to-sample map)

PXD015810 compares early (15 min) and late (60 min) phagosomes from oyster (*Crassostrea gigas*) hemocytes, with 3 biological replicates each (Mao et al., Sci Rep 2020, PMC7171069).

**The design cannot be resolved from public sources.**

- **Six samples, one pool, two runs.** The 6 samples were TMT6-labelled and pooled, and the pool was run twice as technical replicates. Those 2 RAW files are the only data deposited. Both are genuine Thermo files (Orbitrap Elite).
- **Labelling confirmed, map missing.** The deposited peak lists show six strong reporter ions at the TMT6 masses, but nothing says which channel holds which sample. Sources checked:
  - the paper (full text, Table 1, Table S1 and the S1 pdf), which says only "TMT";
  - the two deposited `.msf` files, which are peak-list exports with empty quantification tables and no channel names;
  - the Europe PMC supplementary files;
  - external repositories (none are cited).
- **No guessing from the file name.** The file name `LP1-3&EP1-3` hints at a channel order, but that is an inference, not evidence.

**Other notes (ready for a future SDRF)**
- Acquisition was top-5 DDA, with each precursor fragmented by both CID and HCD.
- Search settings come from the paper: trypsin, Carbamidomethyl C fixed, Oxidation M and Deamidated N/Q variable, 5 ppm precursor tolerance.
- Dissociation method and fragment tolerance would be not available, because the runs mix CID and HCD.
- The SCX fractions described in the paper were not deposited (PARTIAL submission).

**To unblock:** a per-channel table from the authors, or a deposited search or quantification output that names the channels. The SDRF would then have 12 rows (6 samples × 2 technical replicates).
