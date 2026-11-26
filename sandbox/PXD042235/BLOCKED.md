# PXD042235: annotation blocked

## Dataset

- **Title:** Secreted dengue virus NS1 is predominantly dimeric and in complex with high-density lipoprotein (HDX-MS part)
- **PRIDE record:** PXD042235 (PX instrument "Synapt MS"; species Dengue virus 2; "No PTMs")
- **Publication:** Chew BLA et al., eLife 12:RP90762 (2024), DOI [10.7554/eLife.90762.3](https://doi.org/10.7554/eLife.90762.3). The PX record links version .2. Its Data availability section cites PXD042235 as the HDX-MS deposit, so the link is correct.

## What is deposited (FTP listing, 13 files; matches the campaign cache of "3 RAW / 13 files")

- **3 "RAW"-category files:** `NS1c.DnX` (1.0 GB), `Heavy_562.DnX` (404 MB) and `Light_562.DnX` (424 MB). These are Waters DynamX 3.0 project files: processed HDX projects with one per protein/chain, each pooling every state, labelling time and replicate. They are not acquisition files.
- **10 PLGS `*_IA_final_peptide*.csv` peptide lists:** one per non-deuterated identification run (NS1c UnD1/2/4; Fab562 UnD1–3 split into heavy- and light-chain lists, dated 24 and 28 Feb 2023).
- **No Waters `.raw` run folders** are deposited, and no other per-run acquisition files either.

## What the paper says (Methods, "HDXMS")

- **States:** recombinant NS1c alone, Fab56.2 alone, and the NS1c–Fab56.2 complex (purified by SEC). This is epitope/paratope mapping. It is not the NS1:HDL complex named in the title.
- **Labelling and quench:** 90% D2O for 1, 10 and 100 min at 25 °C, plus non-deuterated controls. Quench at pH 2.5 and 0 °C.
- **Digestion and acquisition:** online immobilized pepsin, then a Synapt G2-Si in HDMSE with ion mobility.
- **Software and replication:** PLGS 3.0, DynamX 3.0 and Deuteros 2.0; triplicates.
- The paper says "Raw files are accessible via JPOST". However, jPOST JPST001925 (= PXD038097) holds only the 6 Thermo DSSO cross-linking runs of sNS1 + bovine ApoA1. It has no HDX or Waters files.

## Why no SDRF was emitted

An ms-proteomics SDRF needs one row per deposited raw run, each mapped to a sample state (and here a labelling time). The deuterated HDX runs (3 states × 3 times × triplicate, plus controls) are not deposited as runs in PRIDE or jPOST. They exist only inside the three DynamX `.DnX` projects. Run names, states and times cannot be read from those projects without downloading 1.8 GB of proprietary binaries; the cloud browser can only download them, and the shell has no network.

The only per-run objects are the 10 PLGS CSVs of non-deuterated identification runs. Those are search outputs, not raw data. Annotating them as if they were the dataset would present an HDX study as label-free identification. This follows the PXD013750 (data only in containers) and PXD021266 (HDX MS1 runs) precedents. It differs from PXD013841, which was annotatable only because an overview sheet mapped every run to state and time.

## Evidence checked

- ProteomeCentral PROXI record (`resultType=full`).
- PRIDE FTP directory listing (13 files; the CSV contents could not be opened because the browser forces a download).
- eLife full text: HDX Methods and Data availability.
- jPOST JPST001925 file list.
- Not reachable: the PRIDE v3 API and the Europe PMC REST search (connection failure / rate limit).
- Scratch copies are in `/home/claude/singapore1/scratch/PXD042235/`.

## To unblock

Any one of the following would unblock it:
- Deposit the Waters `.raw` HDX run folders, with a run → state (NS1c / Fab562 / complex) × labelling time (0/1/10/100 min) × replicate table.
- Export the DynamX state/run list from the `.DnX` projects.
- Reach a bigbio decision that HDX-MS project files (`.DnX`) may serve as `comment[data file]`. Even then, an HDX acquisition term and a labelling-time column would be needed.
