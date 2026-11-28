# PXD043818: annotation blocked

## Dataset

- **Title:** Defining neutralization and allostery by antibodies against COVID-19 variants
- **PRIDE record:** PXD043818 (PX instrument "Synapt MS"; species Homo sapiens; "No PTMs"; publication marked pending)
- **Publication:** Tulsian NK et al., Nat Commun 14:6967 (2023), DOI [10.1038/s41467-023-42408-x](https://doi.org/10.1038/s41467-023-42408-x). Its Data availability section names PXD043818 as the HDXMS deposit, so the link is correct. The PX record still says the publication is pending.

## What is deposited (PROXI file list, 38 files; matches the campaign cache of "9 RAW / 38 files")

- **9 "RAW"-category files:** all Waters DynamX `.DnX` projects: `RBD_Wuhan`, `RBD-Delta`, `RBD-O-1`, `RBD_O-2`, `Spike-Delta`, `Spike-O2`, `Spike_Wuhan_NTDbinders`, `Spike_Wuhan_strongneutralizers` and `Spike_Wuhan_IgGs-141516`. Each is a processed project for one protein/variant (or antibody panel) that pools every state, labelling time and replicate. They are not acquisition files.
- **28 `*_UnD*.zip` "search engine output" files:** PLGS outputs of the non-deuterated identification runs (Spike/RBD Wuhan, Delta and Omicron BA.1/BA.2, 2020-12 to 2022-03, mostly 1–3 per construct).
- **`checksum.txt`.**
- **No Waters `.raw` run folders** are deposited. The deuterated runs are not deposited as separate files either. The paper itself says raw MS data are "available from the corresponding author upon request".

## What the paper says (Methods, HDXMS)

- **States:** apo Spike trimer and isolated RBD (Wuhan, Delta, Omicron BA.1/BA.2); antibody complexes (Spike:IgG 1:3, RBD:IgG 1:1); ACE2 complexes.
- **Labelling and acquisition:** 90% D2O at 37 °C for 1, 10 and 100 min (Spike) or 1 and 10 min (RBD). Online pepsin digestion on a nanoACQUITY HDX manager, then a Synapt G2-Si.
- **Software and replication:** PLGS 3.0, DynamX 3.0 and Deuteros 2.0; n = 3, with triplicate measurements per time point.

## Why no SDRF was emitted

This is the same situation as PXD042235 and PXD054896. An SDRF needs one row per deposited raw run, mapped to its state (protein variant × antibody/ACE2 × labelling time). The deuterated HDX runs exist only inside the nine proprietary DynamX projects. Their run names, states and times cannot be read without downloading those large binaries, and the shell has no network. The only per-run objects are the 28 zipped PLGS outputs of undeuterated controls. These are search outputs, not raw data, and annotating them alone would misrepresent an HDX study as label-free identification.

## Evidence checked

- ProteomeCentral PROXI record (`resultType=full`), which gives the file list.
- PRIDE FTP directory: two attempts, both "upstream connect error / connection timeout" (2026-11-27). The listing and file sizes come from PROXI only.
- Nat Commun paper PDF: HDXMS Methods and Data availability.
- Scratch copies are in `/home/claude/singapore3/scratch/PXD043818/`.

## To unblock

Any one of the following would unblock it:
- Deposit the Waters `.raw` HDX run folders, with a run → construct/variant × binder × labelling time × replicate table.
- Export the DynamX state/run lists from the nine `.DnX` projects.
- Reach a bigbio decision that `.DnX` projects may serve as `comment[data file]` (an HDX labelling-time column would also be needed).
