# PXD016927 annotation blocked (channel map only in a closed-access table)

PXD016927 is a TMT6plex study of PRRSV-infected and mock-infected pig alveolar macrophages, pooled and split into 4 high-pH fractions (Proteomics 2020, PMID 33296138).

**The design cannot be resolved from public sources.**

- **Four RAW files.** All are genuine Thermo files (Orbitrap Fusion, from all four headers); they are the 4 fractions of one TMT6plex experiment.
- **The map is only in a closed-access table.** The channel-to-sample map is in the paper's Table 1, and the paper is closed access:
  - Unpaywall, OpenAlex and Semantic Scholar report it as closed;
  - Europe PMC has no full text or PMCID;
  - the publisher page returned 403;
  - Europe PMC has no hits for the accession and no preprint was found.
- **The deposit does not reveal it either.**
  - The MaxQuant `txt.zip` names the channels only as "Reporter intensity 0..5", with empty experiment names.
  - No viral protein groups were identified, so the data cannot even show which channels were infected.

**Other notes (ready for a future SDRF)**
- Run-level values are prepared and verified in OLS4: Orbitrap Fusion, DDA, Trypsin/P, high-pH reversed-phase fractionation, DTT and IAA, 0.02 Da fragment tolerance.
- Modifications from the MaxQuant summary and parameters: TMT6plex, Carbamidomethyl, Acetyl (K and protein N-term), Deamidated, Oxidation.
- HCD is 35% NCE in the RAW method; the protocol text says 28.

**To unblock:** Table 1 of the paper, or a sample sheet from the submitters naming the sample in each channel.
