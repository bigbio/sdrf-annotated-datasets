# PXD054896: annotation blocked

## Dataset

- **Title:** Insights into the regulation of CHIP E3 ligase-mediated ubiquitination of neuronal protein BNIP-H
- **PRIDE record:** PXD054896 (PX instrument "Synapt MS"; species Mus musculus; "No PTMs"; keywords E3-ligase, Ubiquitination, HDX-MS; announced 2025-05-07)
- **Publication:** Shankar S, Liu Y, Tulsian NK, Low BC, Lin Q, Sivaraman J. PNAS Nexus 3(12):pgae536 (2024), DOI [10.1093/pnasnexus/pgae536](https://doi.org/10.1093/pnasnexus/pgae536), PMID 39703232. Its Data availability section cites PXD054896 as the HDX-MS deposit, so the link is correct.

## What is deposited (PROXI file list, 16 files; matches the campaign cache of "4 RAW / 16 files")

- **4 "RAW"-category files:** `CHIPwt_NKT.DnX`, `CHIP-9M_NKT_Jun2021.DnX`, `BNIPwt_NKT.DnX` and `BNIP-4M_NKT_170122.DnX`. These are Waters DynamX project files. There is one per protein construct, and each pools all states, labelling times and replicates. They are processed HDX projects, not acquisition files.
- **11 PLGS `*_IA_final_*.csv` files:** these are search outputs of the non-deuterated (UnD) identification runs.
  - 10 peptide lists: CHIP-wt UnD1/UnD2, CHIP-9M UnD1/UnD3, BNIP-wt UnD1–3 and BNIP-4M UnD1–3.
  - 1 protein list: BNIP-4M UnD3.
  - They are dated 8, 11 and 19 Jun 2021.
- **`checksum.txt`.**
- **No Waters `.raw` run folders** are deposited, and no other per-run acquisition files either. The paper says "raw data" were deposited, but no PX-registered file is a raw run.

## What the paper says (Methods, HDX-MS)

- **Proteins and states:** recombinant mouse CHIP and BNIP-H, expressed in *E. coli* BL21. The HDX states are:
  - CHIP-WT alone, BNIP-H-WT alone, and the 1:1 WT complex (preincubated 30 min at 25 °C);
  - CHIP-9M (K2,4,7,23,31,42,126,222,256R) and BNIP-H-4M (K61,128,291,350R), each alone and as a preincubated complex.
- **Labelling and quench:** D2O PBS (pD 7.4) at 25 °C for 1, 10 and 100 min, plus non-deuterated controls. Quench at pD ~2.5 with 0.75 M GdnHCl and 0.06% TFA.
- **Digestion and acquisition:** online Enzymate BEH pepsin column at 12 °C; nanoAcquity M-class; Synapt G2-Si in HDMSE.
- **Software and replication:** PLGS 3.0 and DynamX 3.0; biological n = 2 × technical n = 3.

This design implies roughly 6 states × (3 labelling times + undeuterated) × replicates, which is on the order of 100+ acquisitions. Only the 4 DynamX containers and 10 undeuterated peptide lists represent them in PRIDE.

## Why no SDRF was emitted

An ms-proteomics SDRF needs one row per deposited raw run, each mapped to a sample state (here also a labelling time and a replicate). The deuterated HDX runs are not deposited as runs. They exist only inside the four `.DnX` projects. Run names, states, times and replicates cannot be read from those projects without downloading proprietary binaries. The cloud browser can only download them, and the shell has no network.

The only per-run objects are the PLGS CSVs of the undeuterated identification runs. Those are search outputs, not raw data. Annotating them would present an HDX study as label-free identification, and they would also leave the complex states and all deuterated runs out.

This follows the PXD042235 precedent (singapore-1: identical deposit pattern of DynamX `.DnX` plus PLGS UnD CSVs, same submitter). It also follows PXD013750 (data only in containers) and PXD021266 (HDX runs).

## Evidence checked

- **ProteomeCentral PROXI record** (`resultType=full`): page URL and accession verified. Saved to `/home/claude/singapore2/scratch/PXD054896/proxi_files.txt`.
- **Paper:** PNAS Nexus full text on academic.oup.com (title confirmed); HDX Methods and Data availability read. Saved to `paper_notes.txt` in the same scratch dir.
- **Not reachable today:**
  - the PRIDE FTP directory listing (connection timeout, 3 attempts), so file sizes were not confirmed;
  - the PRIDE v3 `files/all` API (remote connection failure);
  - the PMC article page (client error).
- **Europe PMC REST:** it returned a payload for an unrelated query, which was discarded.
- **Not done:** the supplementary HDX metadata (the paper says full HDX-MS metadata are in the SI) was not read. Even if it holds a state/time table, it cannot supply per-run files that were never deposited.

## To unblock

Any one of the following would unblock it:
- Deposit the Waters `.raw` HDX run folders, with a run → state (CHIP-WT / CHIP-9M / BNIP-H-WT / BNIP-H-4M / WT complex / mutant complex) × labelling time (0/1/10/100 min) × biological/technical replicate table.
- Export the DynamX state/run list from the four `.DnX` projects.
- Reach a bigbio decision that HDX-MS project files (`.DnX`) may serve as `comment[data file]`. Even then, an HDX acquisition term and a labelling-time column would be needed.
