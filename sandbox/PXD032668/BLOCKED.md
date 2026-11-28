# PXD032668 annotation blocked (no genuine vendor run file deposited)

**Why it is blocked.** The deposit holds no mass spectrometry acquisition:
- **`All_protein.raw`** (759 MB) is plain-text nucleotide FASTA (`>geneNNN` headers followed by A/C/G/T/N sequence), not a Thermo acquisition. Range reads of the start, 20 evenly spaced blocks and the end all show FASTA text, and none of them has the Thermo `01 A1` / "Finnigan" signature.
- **`All_protein.txt`** is a processed ratio table (`Accession d30 d60 d90`) with no per-run or per-channel data.

With no run file, no SDRF rows can be mapped.

**Other notes for a future curator:**
- The paper (PMC8997108) says both "Proteomic data have not been submitted" and, in the next sentence, cites PXD032668. It names no other MS repository. PRJNA772802 holds only RNA-seq data.
- The PRIDE record lists SWATH and cross-linking as experiment types, but the study is iTRAQ DDA. It also gives the human UniProt proteome as the search database for a deer study.
- The paper describes iTRAQ 8-plex for 9 samples (3 time points × 3 deer) and gives no channel map.

**To unblock:** deposition of the actual Thermo `.raw` iTRAQ runs together with the channel-to-sample map.
