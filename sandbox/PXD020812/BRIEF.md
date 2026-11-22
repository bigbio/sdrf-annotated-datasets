# PXD020812 — sandbox brief (partial)

**Dataset:** Adipose MDM2 regulates systemic insulin sensitivity (Hallenborg et al., Sci Rep 2021 11:21839, PMID 34750429). Odense (B. Blagoev lab).

**Status:** partial. It annotates 124 of 191 RAW files (248 rows): the in vivo SILAC epiWAT proteome. It passes `parse_sdrf validate-sdrf` (ms-proteomics + vertebrates v1.1.0) and `sdrf_review.py`.

## Annotated

- **64 runs:** `20170920SSR_QexXn2_091425cmr_{WT,HET}{1-8}{,_2,_3,_4}.raw`. These are 8 wild-type and 8 *Mdm2* Adi+/- epiWAT lysates (light), each mixed 1:1 with a Lys6 SILAC reference (heavy) and each run with 4 methods. The MaxQuant groups (Sens / Fast / SuperFast / Slow) come from the deposited `*_evidence.txt` `Experiment` and `Raw file` columns and are recorded as technical replicates 1–4. Instrument: Q Exactive HF-X (RAW header).
- **60 runs:** `20171013_SSR_{20,80}{WT,HET}{1-14,flowthrough}.raw` (MaxQuant group "Opt"). These are high-pH fractions of WT and HET material; flow-through is fraction 15, and `20HET3_171016181238` is a re-injection (technical replicate 2). Instrument: Q Exactive HF.

## Not yet annotated (67 files)

- **45 runs, MDM2 co-IP:** three antibodies (4B2 = `IP_Cyt_*`, 2A10, SMP14), 15 gel bands each, SILAC Arg6/Lys4 vs Arg10/Lys8. Which SILAC state is IgG and which is anti-MDM2 is not stated in the paper, PRIDE or the evidence files.
- **12 runs, MORC2 IP** (`IP_MORC2_*`), and **10 runs, MORC2 RIME** (`IP_MORC2_RIME_*`). These are triple SILAC (L/M/H): IgG, siGFP and siMdm2 by the figure legend, but the label → condition order is not stated. The RIME raw names in the evidence file (`1st`, `1stUrea`, `1ststar`) do not match the PRIDE file names one-to-one.
- **To unblock:** the SILAC label → condition map, from the authors or the MaxQuant `mqpar.xml` if it can be obtained.

## Open points for a reviewer

- The meaning of the "20" and "80" prefixes is not stated. They are recorded as two fraction sets, each with *pooled* WT/HET material. Whether these are pools or single mice is not stated.
- **Sex and age are `not available`.** The paper's metabolic cohort is male mice on high-fat diet, but the proteomics has 8 HET mice while the reported male HET cohort is N = 7, so the cohort match is not assumed.
- The run group MaxQuant calls "Slow" (`_4`) uses a method file named `Olsen_FAST_Top20`. Both names are recorded.
- The paper says CID, but the instrument is a Q Exactive. HCD is recorded, and fragment tolerance is 0.5 Da as stated.

## Update (odense-tromso-1): MDM2 co-IP annotated → `PXD020812-ip.sdrf.tsv`

There are 45 runs: 3 antibodies (4B2 = `IP_Cyt_*`, 2A10, SMP14) × 15 SDS-PAGE gel bands. The file has 90 rows (2 SILAC channels per run) and passes `parse_sdrf` (ms-proteomics + vertebrates + cell-lines) with no warnings. The specimen is 3T3-L1 adipocytes (CVCL_0123; male, embryo-derived, per Cellosaurus).

- **Label → condition.** The PRIDE data protocol states double labels Arg6/Lys4 and Arg10/Lys8, recorded as SILAC medium and SILAC heavy. In the deposited `MDM2_proteinGroups.txt`, the bait Mdm2 has H/L = 1419 (4B2), 269 (2A10) and 28 (SMP14), against a global median of about 1. So heavy (Arg10/Lys8) is anti-MDM2 and medium (Arg6/Lys4) is nonspecific IgG.
  - The MaxQuant L state is taken as Arg6/Lys4, following the label order in the protocol. Evidence-file masses could not confirm this, because MaxQuant `Mass` excludes the label.
- **Raw files → experiments.** The `Raw file` / `Experiment` columns of `MDM2_evidence.txt` match all 45 deposited file names one-to-one.
- **Digestion.** Trypsin: the evidence contains many R-terminal peptides. The other technical values follow the stated search parameters (20 ppm / 0.5 Da, carbamidomethyl C, oxidation M, protein N-term acetyl, SILAC label modifications).

### MORC2 IP / RIME (22 RAW files): still blocked, but the label map is now known

- **Label map, from the paper's Table S3** (`41598_2021_1240_MOESM3_ESM.xlsx`) against `MORC2_proteinGroups.txt`:
  - `aMORC2/IgG` tracks the MaxQuant M/L ratio (r = 0.95 Regular, 0.96 RIME).
  - `siMdm2/siGFP` tracks the H/M ratio (r = 0.98 on the Regular/RIME average).
  - So L (Arg0/Lys0) = IgG, M (Arg6/Lys4) = anti-MORC2 in siGFP cells, and H (Arg10/Lys8) = anti-MORC2 in siMdm2 cells.
- **Why it stays blocked.** The deposited raws (`20180525_..._IP_MORC2_1-12`, `20180611_..._IP_MORC2_RIME_1-10`) are not the runs in the deposited search. `MORC2_evidence.txt` lists `20170705_PH_MORC2IP_1-15` (Reg) and `20180130/20180202_..._MORC2_RIME_1st*` (RIME) instead, and none of those files are in PRIDE. So the deposited MORC2 files cannot be tied to a search or a label layout. They stay unannotated.
