# PXD051720 - BLOCKED: SILAC raw file → experiment → channel map not public

BLOCKED: no SDRF is committed because the per-file sample identities and the light/heavy channel
assignment cannot be resolved from public evidence. Writing them would mean inventing sample → file /
channel relationships.

## Dataset
- PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD051720
  ("STK19 drives transcription-coupled nucleotide excision repair by stimulating Pol II ubiquitylation
  and TFIIH recruitment"; PARTIAL submission; disease field: Cockayne syndrome, DOID:2962)
- Primary publication: Ramadhin AR, Lee S-H, Zhou D, … Marteijn JA. *Mol Cell* 2024,
  PMID 39547223, doi:10.1016/j.molcel.2024.10.030. Preprint: bioRxiv doi:10.1101/2024.07.22.604556
  (full text used as evidence; the Mol Cell version has no open PMC copy).
- PRIDE currently links a later paper that reanalyses the Pol II data: Blom CMA et al., *Nucleic Acids Res*
  2026, PMID 42965289, PMC13722877, doi:10.1093/nar/gkag1068 (Fig. 1A,B).
- Organism: *Homo sapiens*. Cell lines: HCT116 (WT, STK19-/-, CSA-/-, CSB-mScarlet-I KI, STK19-GFP).
  These are TC-NER knockout models of Cockayne syndrome biology, not patient material.

## What the evidence does establish
- Quantification: SILAC, 2-plex. MaxQuant "multiplicity=2, K8/R10"; heavy = [13C6,15N2]-lysine
  (Label:13C(6)15N(2), UNIMOD:259) and [13C6,15N4]-arginine (Label:13C(6)15N(4), UNIMOD:267). Light =
  unlabelled Lys/Arg. (The preprint's diGly methods write heavy lysine as "[13C6]-lysine", which
  contradicts the K8 search setting. That is one more open point.)
- Interactome runs (2304_*, 2307_*, 2350_*; 92 files): Orbitrap Fusion Lumos (raw headers), EASY-nLC
  1200, in-gel tryptic digest of SDS-PAGE gel slices, DDA, HCD with ion-trap MS2. Fixed mods: carbamidomethyl C.
  (The PRIDE protocol says iodoacetamide; the papers say chloroacetamide.)
- diGly runs (2373_E_*; 6 files): Orbitrap Eclipse (raw headers), Vanquish Neo per paper; in-solution
  trypsin; K-ε-GG immunoaffinity enrichment; 3 high-pH fractions each for "WT_CSA_KO" and "WT_STK19_KO".
- Experiments described in the papers (each FW + label-swap REV):
  1. STK19-GFP chromatin IP, mock vs UV (16 J/m², 1 h) (Fig. 2A), plus an unperturbed STK19-GFP IP (Supp. Fig. 2);
  2. pSer2-RPB1 (Pol II) IP, HCT116 WT vs STK19-/-, UV (20 J/m², 1 h) (Fig. 5B; NAR 2026 Fig. 1A);
  3. CSB-mScarlet ("RFP") IP (methods; `RFP_IP_FW/REV` in the deposited proteinGroups);
  4. diGly ubiquitinome, WT vs CSA-/- and WT vs STK19-/-, UV 20 J/m², 30 min (Fig. 6A).

## Why it is blocked
1. **No raw file → experiment map for the 92 interactome files.** File names carry only a batch number,
   a date and a slice index (`2304_…_11MAY_01..20`, `2307_…_01JUNE21_01..20`, `2350_…_01nov2021_01,02,11..60`).
   No mqpar.xml, summary.txt or experimental-design file is deposited. The only search output,
   `Marteijn_et_al_proteingroups.xlsx`, covers just 4 MaxQuant experiments (`POLII_IP_plusUV_FW/REV`,
   `RFP_IP_FW/REV`, 10 fractions) and does not name raw files. The papers do not list files. Raw
   headers hold no sample name or comment, only the method and file name.
2. **The light/heavy → sample assignment is not stated** for any experiment, the diGly runs
   included: the paper says only that each cell line was grown in light or heavy medium, with a label swap.
   The `POLII_IP_plusUV_FW` ratios in the proteinGroups (UVSSA, ERCC3, GTF2H1, CUL4A H/L ≈ 2; CSA/CSB/DDB1
   ≈ 1) fit WT = heavy in FW. That is an inference from results, not a stated design, and it still
   does not say which raw files make up that experiment.

3. **Other inconsistencies found in the public record:**
   - In `RFP_IP_FW/REV` the bait CSB (ERCC6) has raw H/L 0.49 (FW) and 0.66 (REV), but normalized H/L
     0.32 (FW) and 2.09 (REV) in the deposited proteinGroups. The papers do not say which conditions
     this CSB-mScarlet IP compares (the preprint text suggests WT vs STK19-/-), so its sample identities
     cannot be pinned down from the data alone.
   - The diGly file names encode three high-pH fractions (F1-F3). The methods state "a single LC-MS/MS run
     was performed for all immunoprecipitated peptide material from one sample".
   - The 2350 batch skips slice numbers `_03` to `_10`. No public source explains this.

## Independent check
A fresh-context reviewer tried to disprove the block from public sources only. Verdict: **BLOCK_CONFIRMED**.
- Only the 6 diGly files can be tied to an experiment, from their file names, and not to a channel.
- Not reachable: the Mol Cell STAR Methods and Table S1 (cell.com / sciencedirect returned HTTP 403; no PMC
  copy). The bioRxiv supplements (media-1.pdf with Suppl. Fig. 8C/9A, and media-2.xlsx) were rate-limited
  (HTTP 429). A curator with browser access should check these before treating the block as final.

## What would unblock
- The submitters depositing the MaxQuant `mqpar.xml` (or `summary.txt` / experimental design template)
  for each search, or a table that maps raw file to experiment, FW/REV and the heavy/light condition. With that,
  every interactome file becomes 2 rows (SILAC light / SILAC heavy) with known sources, and the 6 diGly
  files likewise.
- Or the authors (Marteijn / Demmers labs, Erasmus MC) giving the map, cited publicly (for example in a
  corrigendum or the PRIDE description).

## Evidence checked
PRIDE v3 project + files API (99 files: 98 RAW, 1 SEARCH); `Marteijn_et_al_proteingroups.xlsx` (all
122 columns); raw file headers (first MB of one or more files per batch); bioRxiv full text of
10.1101/2024.07.22.604556 (Methods: IP, diGly, quantitative proteomics, data availability; Fig. 2, 5, 6
legends); Europe PMC full text of PMC13722877 (Methods > Proteomics; Fig. 1 legend; data availability).
The Mol Cell full text and supplementary tables were not reachable (paywalled, HTTP 403).
