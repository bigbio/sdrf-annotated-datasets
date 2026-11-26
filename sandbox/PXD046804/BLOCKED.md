# PXD046804 annotation blocked

PXD046804 is a proteomics dataset, not metabolomics or lipidomics. It is a TMT6plex time course of *Mycobacterium bovis* BCG str. Pasteur 1173P2 (NCBITaxon:410289) under PBS starvation. The paper is Davis et al., Commun Biol 2024;7:866, doi:10.1038/s42003-024-06562-2, PMC11250799, PMID 39009734. Its Data availability statement cites PXD046804 for the starvation proteomics. Its Methods paragraph still points to Chorus for the same data.

The deposit holds 12 files. Two are Thermo RAW files, `170302_390_ND_setA_6plex.raw` and `170302_390_ND_setB_6plex.raw`, with matching `.mgf` files. The rest are seven Scaffold `.sf3` files and one ratio table (`BCG_TMT_10Plex_B01_R01andR02_RAW_06202016.txt`). The cache count of 2 RAW / 12 files is correct.

## Why no SDRF

1. **The deposited raws are not the runs the paper describes.**
   - The Methods describe these runs: 5 states (Log, S4, S10, S20, S-R6) × biological triplicate, TMT6plex, 24 OFFGEL fractions, technical duplicate injections, all on an **Agilent 6550 iFunnel Q-TOF**. That is about 144 Agilent `.d` runs. None of them are deposited.
   - The only other instrument use mentioned is a label-check mix on a Q Exactive.
   - The two deposited Thermo files are dated 2017-03-02, after the `QTOF6550` Scaffold searches dated 2017-01. Their names say "set A" and "set B", which the paper never mentions. Nothing states what they are or how they relate to the three biological replicates.
2. **There is no channel → sample map.**
   - The paper gives no table that assigns TMT 126–131 to time points or replicates.
   - Five states fill six channels, and the sixth channel's identity is unstated.
   - The only readable deposited result (the `.txt`) labels its columns only as `126/126 … 131/126`.
   - The `.sf3` files are binary Scaffold files and could not be read here, because the shell has no internet.
   - Any mapping would be guessed, which violates the hard rule.
3. **The instrument is unresolved.**
   - The PX record lists "LTQ Orbitrap" and "6520A Q-TOF".
   - The paper says 6550 iFunnel Q-TOF, plus a Q Exactive for the label check.
   - The sf3 file names say `OrbitrapQE` and `QTOF6550`.
   - The RAW headers could not be read, so which Thermo instrument acquired setA/setB is unknown.

## Evidence checked

- ProteomeCentral PROXI record (rev 2, 2024-10-22).
- PRIDE FTP directory listing over HTTPS: 12 files, with sizes.
- `BCG_TMT_10Plex_B01_R01andR02_RAW_06202016.txt`: column header and leading rows.
- PMC11250799 full text (Methods: "BCG starvation proteomics" sections; Data availability).
- Not checked:
  - Supplementary Data 2 and the SI PDF. They were not downloaded, because a download needs user permission.
  - The publisher page at doi.org. The fetch was not permitted.
  - Europe PMC full text. The REST API was unreachable.
- Saved under `/home/claude/singapore1/scratch/PXD046804/`.

## To unblock

Either of these would unblock it:
- The authors confirm what `setA` and `setB` are (which biological replicates or time points) and give the TMT channel layout, plus the instrument for the two RAW files.
- The Scaffold `.sf3` sample/quant category names are read, if they name the channels, together with a RAW header read that identifies the instrument.

A SDRF of only 2 runs × 6 channels would also need the setA/setB → sample key. Without it, even a sandbox SDRF would rest on guessed mappings.
