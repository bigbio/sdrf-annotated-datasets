# PXD040361 annotation blocked (TMT channel orientation unresolved)

PXD040361 has one genuine Thermo RAW file. It is a TMT10plex SPS-MS3 run on an Orbitrap Fusion Lumos, according to the raw header. The run holds small extracellular vesicles from five paired HCT116 cultures, each grown glutamine-replete (2 mM) or glutamine-depleted (0.15 mM). No public sample sheet gives the channel map.

**What is established.** Fitting the deposited Proteome Discoverer ratios to the paper's supplementary fold changes gives one unique **pairing**. It was checked over all 945 pairings × 32 orientations:
- 126/127N, 127C/128N, 128C/129N, 129C/130N, 130C/131.

This pairing reproduces all 135 published median and mean fold changes exactly. It also matches the "# Unique Peptides" column for all 135 proteins. No alternative pairing matches more than 2.

**Why it is blocked.** The **orientation** (which channel of each pair is glutamine-depleted) cannot be confirmed:
- The only support is the paper's "depleted versus replete" definition of fold change and its 48 increased / 87 decreased counts.
- Under that orientation, CHMP1A, CHMP1B, CHMP5 and IST1 come out lower in the depleted channels (median ratios 0.55–0.82). The paper's western blots (n = 5) show CHMP1A, CHMP1B and IST1 increased in depleted sEVs. The blots are normalised per cell rather than per equal peptide load, which may explain part of the gap, but no public source resolves it.
- In the supplementary tables, the protein-name and accession columns are a permutation of the same 135 proteins relative to the numeric columns. The paper's headline TMT claim and GO table may therefore come from mislabelled rows, and they cannot settle the orientation.
- "Control" in the Proteome Discoverer export is the software's default ratio denominator, not a sample annotation.

In a two-condition single-plex design, an inverted orientation flips every differential result, so the orientation cannot be guessed.

**Already verified** (ready for a future SDRF):
- Instrument and method from the raw header: MS1 380–1600, CID 35% ion-trap MS2, SPS-MS3 HCD 65%.
- Search settings from the deposited MSF, including variable phospho.
- Cell-line metadata from Cellosaurus CVCL_0291.

**To unblock:** an author-confirmed channel-to-condition list, a corrected supplementary table or erratum, or a sample sheet deposited in PRIDE.
