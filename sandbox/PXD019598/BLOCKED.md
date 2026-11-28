# PXD019598 annotation blocked

PXD019598 (TMEM147/TMEM129 co-IP interactomes in HeLa Kyoto cells; Christodoulou et al., J Cell Sci 2020 133(16):jcs245357, doi:10.1242/jcs.245357, PMID 32694168, which cites PXD019598) is a single TMT6plex experiment. Six RAW files (`Zelda_200514_P1264_MR_NS_IP_TMT6_fr1..fr6.raw`, one high-pH RP fraction each, Orbitrap Fusion Lumos) carry six IP samples: TMEM147-GFP, TMEM129-GFP and GFP-only (control), each from 2 independent experiments.

The channel → sample map could not be obtained:
- **Paper:** it states 3 IP types x 2 experiments, SP3 and TMT6plex, but gives no channel table (read via a scispace PDF copy; the journal site is behind a Cloudflare bot challenge).
- **isobarQuant `..._proteins.txt`:** read via the cloud browser. It has the 10-column layout `signal_sum_126 ... 131L`, but only 126/127L/128H/129L/130H/131L hold signal, which fits TMT6plex. Reference label is 126. No sample names.
- **`..._summary.txt`:** read. It maps 6 RAW files to sample_id 1-6 (one per fraction, not per channel) and lists pyMSsafe/quantifyProteins parameters. No conditions.
- **`metadata.csv` (918 bytes, deposited):** this is almost certainly the isobarQuant channel/condition sheet. It could not be read: the cloud browser treats it as a download and never renders it (both the ftp.pride.ebi.ac.uk and ftp.ebi.ac.uk/pride-archive paths), and a text proxy timed out. The shell has no network.
- **Europe PMC and PRIDE v3 API:** both gave an upstream connection error today.

Any channel assignment would be a guess (for example 126 = GFP control), so no SDRF is emitted.

**Deposited files (PROXI + FTP listing, re-derived 2026-11-27):** 6 RAW, 6 Mascot `.dat` (F095263/64/67/71/73/83, mapped 1:1 to fr1-fr6 in README.txt), `fractionated_merged_results_20200518_1847_{peptides,proteins,summary}.txt`, `metadata.csv`, `README.txt`.

**Recoverable once the map is known:** Homo sapiens, HeLa Kyoto (verify the Cellosaurus accession), co-IP with GFP-Trap_A; SP3; TMT6plex; high-pH RP fractionation (Gemini C18; this is not SDS-PAGE); Orbitrap Fusion Lumos (paper; PX also lists Q Exactive, but the RAW header was not read); MS1 375-1500 m/z; HCD NCE 36; Mascot 2.2.07 / isobarQuant against UP000005640. The search modifications and enzyme are not in the paper and must be read from a `.dat` header (`MODS=`, `IT_MODS=`, `CLE=`, `TOL=`, `ITOL=`).

**To unblock:** read `https://ftp.pride.ebi.ac.uk/pride/data/archive/2020/08/PXD019598/metadata.csv` with any non-browser HTTP client (918 bytes). If it maps the TMT channels to conditions/replicates, the dataset can be annotated at 36 rows (6 RAW x 6 channels). Also range-read the first ~10 KB of `F095263.dat` for the search parameters.

## Review status
pending
