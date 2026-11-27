# PXD040218 annotation blocked (no public TMT channel-to-sample map)

PXD040218 is a lysine 2-hydroxyisobutyrylation (Khib) study of PBMCs in systemic lupus erythematosus (SLE).

**The design cannot be resolved from public sources.**

- **One RAW file.** `Z8207TP2O.raw` is a genuine Thermo file (Q Exactive Plus, created 2018-09-26). It is a single TMT10plex run of Khib-enriched PBMC peptides.
- **No channel map anywhere.** These sources were checked, and none says which sample or pool is in which TMT channel:
  - the paper and its supplement, which has clinical data for 8 patients only;
  - the deposited MaxQuant `txt/` output, which names the channels generically (Reporter intensity 0–9);
  - the Europe PMC supplementary files;
  - the Data Availability statement, which cites only PXD040218;
  - the cited cohort paper (Xie 2022, PMC9652266).
- **Reconstruction rejected.** Every SLE-vs-control split of the six main channels was tested against the paper's site directions and its 865 up / 630 down counts. None reproduces them (best 44 of 60 directions).
- **Pooling is undescribed.** The same raw and txt files are also deposited under PXD015351, whose paper describes 8 SLE + 20 healthy donors; this paper says 8 SLE + 8 controls. Either way, more donors than channels means pooling that neither paper describes. Only about 6 channels carry real signal.
- **Existing PXD015351 SDRF.** It fills all 10 channels with placeholder samples and disease `not available`, so it is not evidence of a map.

**Other notes**
- The raw method (60 min at 400 nL/min, MS2 at 35,000) disagrees with the paper's LC-MS settings (40 min at 800 nL/min, MS2 at 17,500); the raw file is taken as correct.
- PRIDE lists the PTM as "acetylated residue"; the enriched modification is 2-hydroxyisobutyrylation (UNIMOD:1849).
- Run-level values are prepared and verified in OLS4: Q Exactive Plus, DDA, Trypsin/P, HCD at NCE 30, Orbitrap MS2, 5 ppm / 0.02 Da; Carbamidomethyl, TMT6plex (K, N-term), 2-hydroxyisobutyryl, Acetyl, Deamidated, Oxidation.

**To unblock:** the authors' TMT channel assignment (per donor, or per pool with its make-up and group), or a deposited sample sheet or `mqpar.xml` that names the channels.
