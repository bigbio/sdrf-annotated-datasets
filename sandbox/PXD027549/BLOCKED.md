# PXD027549 annotation blocked

PXD027549 is a quantitative chemical-proteomics study of the HeLa O-GlcNAcome under amino-acid starvation. The paper is Wong YK et al., Proteomics 2022;22(9):e2100175, doi:10.1002/pmic.202100175, PMID 35083852, with no PMCID. Lab head is Shen Han-Ming, NUS / University of Macau. The protocol: HeLa cells are metabolically labelled, lysates are clicked to biotin tags and enriched, then labelled with iTRAQ 8-plex and analysed by LC-MS/MS on a TripleTOF 5600. Quantitation used ProteinPilot v5.

**Deposit:** there is exactly **one acquisition**. It consists of `181017_YK_8plex_5ul.wiff` (14 MB) and its companion `181017_YK_8plex_5ul.wiff.scan` (745 MB). Also deposited are one ProteinPilot result, `181017_YK_8plex_5ul.group` (314 MB), plus `checksum.txt` and `README.txt`. The campaign cache said "2 RAW / 4 files". The 2 "RAW" entries are the `.wiff`/`.wiff.scan` pair of a single run, so the SDRF would need 1 file × up to 8 iTRAQ channels.

The channel → sample map is not available:
- **PRIDE/PX protocol text** says only that lysates were "labelled with iTRAQ tags". It gives no reagent assignment, no list of conditions, and no replicate structure. The PX modification is iTRAQ8plex (MOD:01549).
- **Paper:** it is closed access (Unpaywall `closed`, no OA locations, no PMC/Europe PMC full text). Both Wiley hosts served a Cloudflare bot check, which was not bypassed. The abstract names only control vs starvation and gives no channel layout.
- **Thesis:** the PhD thesis behind this deposit is in ScholarBank@NUS. It is by Wong Yin Kwan, dated 2021-06-28, and has the same title as the deposit. Its access status is *Restricted*.
- **ProteinPilot `.group`:** it may carry the Paragon sample/reagent labels. It is a 314 MB binary that could not be read here: the shell has no internet, and the browser cannot range-read it.
- **Europe PMC** free-text search for the accession: 0 hits.

How many of the 8 reagents carry samples, and which reagents are starved vs fed, ±label or replicates, is unknown. Any map would be guessed.

**Also unverified:** the instrument, TripleTOF 5600 (PX field only; the `.wiff` header was not read), plus enzyme, alkylation and search tolerances (the paper Methods are unread).

**Evidence checked:** ProteomeCentral PROXI record; PRIDE FTP listing, `README.txt` and `checksum.txt`; OmicsDI PRIDE record; PubMed 35083852; Unpaywall; Wiley (blocked by bot check); Europe PMC search; ScholarBank@NUS search. The PRIDE v3 API was down. Saved payloads are in `/home/claude/singapore1/scratch/PXD027549/`.

**To unblock:** the iTRAQ reagent → sample table (113–121) from either of these:
- the paper's Methods, Figure 1 or Supporting Information (needs Wiley access);
- the Paragon sample/reagent names in `181017_YK_8plex_5ul.group`, read with ProteinPilot or PeakView on a machine with PRIDE FTP access.

The `.wiff` header would also confirm the instrument.
