# PXD014755: BLOCKED (no SDRF yet)

**BLOCKED:** I could not resolve the raw file → sample (SW48 KRAS genotype × cetuximab
treatment) map from public evidence I could reach. The design is also **not SILAC**:
PRIDE lists `SILAC` (PRIDE:0000315), but the protocol describes synthetic heavy-isotope
peptides spiked into digests of unlabelled cells (AQUA-style targeted quantification in
Skyline). So there is no `.sdrf.tsv` here yet. Nothing below was invented. Each fact
cites its source.

- Dataset: <https://www.ebi.ac.uk/pride/archive/projects/PXD014755>
- Publication: McFall T *et al.*, "A systems mechanism for KRAS mutant allele-specific
  responses to targeted therapy", *Sci Signal* 2019;12(600):eaaw8288.
  PMID 31551296, PMC6864030 (NIH author manuscript NIHMS1053977), DOI 10.1126/scisignal.aaw8288.

## What the public evidence settles

| Item | Value | Source |
|---|---|---|
| Organism | Homo sapiens | PRIDE record |
| Cell line | SW48 (Cellosaurus CVCL_1724) and isogenic KRAS-knock-in derivatives | paper, "Cell Line Models and Culture Method" and Results |
| KRAS genotypes (as published) | G12D/WT, G12V/WT, G13D/WT, WT/WT. The MS figure (Fig. 2D) reports **G12V/WT and G13D/WT** cells; whether WT/WT cells were also injected is not stated. | paper Results, Fig. 2D legend |
| Disease | colorectal cancer (paper); PRIDE lists DOID:219 "colon cancer". All MS samples are SW48-derived, so no control arm. | paper, PRIDE |
| Treatment | cetuximab 20 µg/ml for 48 h vs untreated | PRIDE sample protocol, paper Methods, Fig. 2D legend |
| Sample | active (GTP-bound) Ras pulled down with RAF-RBD (Thermo Active Ras Pull-Down kit), methanol/chloroform precipitated | PRIDE protocol, paper Methods |
| Digest / mods | trypsin, overnight 37 °C; TCEP reduction, chloroacetamide alkylation (Carbamidomethyl C, UNIMOD:4 in the Skyline document) | PRIDE protocol; `20180614_Edpeptides-7-12.sky` |
| Heavy standards | 500 fmol per injection of synthetic peptides SFEDIHQYR (HRAS), SFADINLYR (NRAS), SFEDIHHYR (KRAS), LVVVGAGGVGK (WT H/N/KRAS), LVVVGAGDVGK (G13D), LVVVGAVGVGK (G12V). Skyline heavy mods: Label:13C(6)15N(4) C-term R (UNIMOD:267), Label:13C(6)15N(2) C-term K (UNIMOD:259). | PRIDE protocol; both deposited `.sky` files |
| Instrument | Orbitrap Fusion (MS:1002416), nLC 1200, 140 min gradient, DDA, MS1 120k Orbitrap, CID MS/MS in ion trap, 3 s cycle | PRIDE protocol, paper Methods |
| Quantification | Skyline peak areas, light endogenous vs heavy standard; normalised to mutant Ras within each sample | PRIDE data processing protocol |
| Replication | "Mass spectrometry was performed twice"; Fig. 2D shows "two independent experiments" | paper Statistical Analysis, Fig. 2D legend |
| Raw files | 12: `20180420_ESTM-07…12_w500fmol.raw` (Skyline doc `20180614_Edpeptides-7-12.sky`) and `20180515_ESTM-13…16,18_w500fmol.raw` + `20180515_ESTM-17_w500fmol_2.raw` (Skyline doc `20180614_Edpeptides-13-18_v2.sky`) | PRIDE files API |

## What blocks the SDRF

1. **The file → sample map is missing.** The 12 runs fall into two acquisition batches of
   six (ESTM-07…12 in April, ESTM-13…18 in May 2018), consistent with the two independent
   experiments. But two genotypes × ± cetuximab is only four samples per experiment, so
   six runs per batch implies either a third genotype (e.g. WT/WT) or repeat injections.
   Neither the PRIDE record, the PMC author-manuscript text, nor the Skyline documents
   (replicate names are only `ESTM-nn`; no replicate annotations) say which ESTM number is
   which genotype/treatment.
   - The map is most likely in **Data file S1** ("Mass spectrometry data and analysis of
     untreated and cetuximab-treated isogenic SW48 cells",
     `NIHMS1053977-supplement-Supp_Data.xlsx`). The Europe PMC supplementaryFiles endpoint
     answers "not open access" for this article, and PMC served a captcha page instead of
     the file in this session. It is unread, not known to lack the map.
   - Genotype could in principle be inferred per run from which light mutant peptide
     (LVVVGAGDVGK vs LVVVGAVGVGK) is detected, but treatment cannot, and an inferred map is
     not public evidence.
2. **Deposit oddities to resolve with the map.** The `13-18_v2` Skyline document also
   contains `20180505_ESTM-13…18` and `20180515_ESTM-17` / `_1` runs that are not deposited;
   only `20180515_ESTM-17_w500fmol_2.raw` is, so ESTM-17 was re-injected and only the third
   injection was shared.
3. **Label encoding.** This is not metabolic SILAC; the heavy channel is a synthetic
   peptide standard, not a sample. An SDRF would need one row per raw file for the
   endogenous (light) sample plus a heavy row whose source is the spiked peptide standard
   (its own `source name`, with `characteristics[spiked compound]`), or the light row only
   with the standard described in `characteristics[spiked compound]`. A maintainer
   decision on which representation the repository prefers would help.

## To unblock

- Read Data file S1 (or ask the authors / Stites lab, Salk) for the ESTM-nn → (KRAS
  genotype, cetuximab yes/no, experiment) assignment.
- Then: `sdrf-tools build` with one row per raw file (and label channel, if the heavy
  standard gets its own row), validate with `-t ms-proteomics -t human -t cell-lines`
  (optionally `-t oncology-metadata`), run the adversarial review, and promote to
  `datasets/`. Factor values: `genetic modification`/KRAS genotype and `compound`
  (cetuximab vs none).
