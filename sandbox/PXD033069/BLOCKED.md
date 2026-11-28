# PXD033069 annotation blocked

PXD033069 ("Batten's Disease proteomics using iTRAQ LC-MS/MS", Sharaireh et al., Cell Death Dis 2025 16:772, DOI 10.1038/s41419-025-08063-4, PMID 41173878) is an iTRAQ 8-plex study of iPSC-derived neural progenitor cells. It covers CLN7 Batten disease lines BD1/BD2 and controls WT1/WT2, each treated with DMSO or bafilomycin A1, in triplicate. That gives 24 samples in three 8-plexes, fractionated by high-pH RP and analysed with ProteinPilot 5.0.1. The paper's Data Availability statement cites PXD033069.

**No raw data is deposited.** The PROXI record lists only 7 files:
- 3 ProteinPilot `.group` search results: `20190904_AS_iTRAQ_8_plex_2.group`, `20190830_AS_iTRAQ_8_plex_3.group` and `20190906_AS_8_PLEX_1B_01.group`.
- 4 seaMASS comparison tables: `Battens-C.M_v_BD.M.csv`, `Battens-C.P_v_BD.P.csv`, `Battens-C.M_v_C.P.csv` and `Battens-BD.M_v_BD.P.csv`. PROXI mislabels these as "Associated raw file URI".

No `.wiff`, `.wiff.scan`, mzML or MGF files are listed, and the record carries MS:1002857 "Unsupported dataset by repository". An SDRF needs one row per raw data file × channel, so no defensible SDRF can be written: `comment[data file]` would have to point at search outputs.

**Secondary issues, if raw files appear later:**
- **Channel map:** the iTRAQ channel → sample map was not found in the paper Methods text that was read. It may be in the `.group` files or the supplement, neither of which was read.
- **Instrument conflict:** PX says TripleTOF 5600, but the paper says TripleTOF 6600.
- **Treatment conflict:** the paper's Results give Baf A1 10 nM for 12 h, while its general Methods give 100 nM for 6 h.

**Evidence checked:**
- ProteomeCentral PROXI `resultType=full` (Page URL verified).
- PRIDE FTP folder `2025/11/PXD033069/`: 2 attempts, both returned upstream connection timeout.
- PRIDE v3 `files/all`: remote connection failure.
- Paper full text on nature.com, including Methods and Data availability.
- Europe PMC search: rate-limited, not read.

Scratch: `/home/claude/mideast1/scratch/PXD033069/` (`file_names.txt`, `proxi_summary.txt`).

**To unblock:**
1. Get a PRIDE FTP listing showing that `.wiff`/`.wiff.scan` files exist. PROXI may omit them, and the FTP listing was unreachable today. If the listing confirms they are missing, the submitters must deposit the raw files.
2. Get the iTRAQ 113–121 channel → sample layout for each of the three 8-plexes, from the `.group` files, the supplement or the authors.
