# PXD037898 annotation blocked (TMT channel-to-sample map not public)

PXD037898 has one genuine Thermo RAW file: Orbitrap Fusion Lumos, DDA, HCD 38%, MS2 in the Orbitrap at 15K, according to the raw header. That one run is a single TMT6plex, and all six reporter channels carry signal in the deposited MaxQuant 1.6.0.1 output.

**Why it is blocked.** The study describes 13 participants: 1 cTTP patient, 4 healthy pregnant controls, 4 gestational hypertension and 4 preeclampsia. No public source maps any participant, pool or group to TMT126–131. Writing an SDRF would mean inventing channel identities.

**Where the map was looked for:**
- The paper and its Europe PMC supplementary material: only the Figure 1 image, no tables.
- The deposited MaxQuant output: channels are named only "Reporter intensity 0..5". There is no `mqpar.xml` and no experimental design file.
- The Data/Code Availability statement: cites only the PXD; R code is "on request".
- The ProteomeCentral record and a Europe PMC search on the accession: nothing further.
- The related cohort study PXD031278 (Cells 2022): it holds different, earlier raw files. Its labelling-scheme Table S1 could not be retrieved.

**Other notes for a future curator:**
- Deamidation (NQ) was searched but is mentioned in neither the protocol nor the paper.
- PRIDE gives the organism part as "blood plasma", but the protocol describes platelet-rich plasma plus buffy coat.
- The precursor tolerance was not deposited.

**To unblock:** the submitters' per-channel table for TMT126–131 (participant or pool, and group).
