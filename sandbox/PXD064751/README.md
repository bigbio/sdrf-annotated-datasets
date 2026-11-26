# PXD064751 — BLOCKED

**BLOCKED: not a SILAC dataset (TMT 6-plex), and the TMT channel → sample map is not
available from public evidence retrievable so far. No SDRF has been written, because
writing one would mean guessing which reporter channel holds which sample.**

## Dataset

- PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD064751
- Title: *Quantitative proteomics of MYDGF knockdown in lung adenocarcinoma cells* (published 2025-06-22)
- Publication: Myeloid-Derived Growth Factor-Regulated Oncogenesis in Lung Adenocarcinoma Is
  Associated with EGFR Status and Cancer Aggressiveness. *J Proteome Res* 2025.
  PMID [40752010](https://europepmc.org/article/MED/40752010), PMC12419241,
  DOI [10.1021/acs.jproteome.5c00385](https://doi.org/10.1021/acs.jproteome.5c00385)
  (Europe PMC links this PMID to PXD064751)
- Organism: *Homo sapiens* (NCBITaxon:9606)

## Why it is blocked

1. **Labelling is TMT, not SILAC.** PRIDE lists the quantification method as `TMT`
   (PRIDE:0000314). The sample protocol says "labeled with a 6-plex tandem mass tag (TMT)".
   All raw files are named `MYDGF_KD_TMT6_sNN.raw`. The SILAC part of this study is the
   related tissue dataset **PXD046807** (super-SILAC), not this one. This accession was
   picked up by a SILAC screen only because the PRIDE description mentions PXD046807.
2. **The channel map is unresolved.** The protocol names 6 samples: NC siRNA and MYDGF
   siRNA in WI-38 (normal lung fibroblast), CL1-5 (EGFR wild-type LUAD) and PE089 (EGFR-mutant
   LUAD). That is 3 × 2 = 6, which matches one TMT6plex. But neither PRIDE nor the abstract
   says which reporter (126–131) holds which sample. The full text and supplementary files
   could not be retrieved here (the Europe PMC fullTextXML call returned HTTP 500, PMC
   returned a CAPTCHA, and no supplementary bundle was available). The ladder in
   `sdrf-skills` `references/channel-map.md` therefore stops at step 1 without a map.

## Evidence already gathered (for whoever finishes this)

- Files: 72 RAW files `MYDGF_KD_TMT6_s01.raw` … `MYDGF_KD_TMT6_s72.raw`. These look like
  72 fractions of a single TMT6plex (2D LC-MS/MS, SCX then RP-C18). There is also one search
  result, `20220831_CJY_MYDGF_KD_TMT6.msf`.
- Instrument: Orbitrap Fusion Lumos (MS:1002732); LC: Dionex UltiMate 3000 nano-LC
- Enzyme: Trypsin, 1:100, 37 °C 16 h; up to 2 missed cleavages
- Reduction: TCEP, 60 °C 60 min. Alkylation: MMTS (fixed Methylthio on C)
- Fixed modifications: TMT6plex on K and peptide N-term; Methylthio on C
- Variable modifications: Oxidation (M), Acetyl (protein N-term), Gln->pyro-Glu (N-term Q)
- Tolerances: precursor 10 ppm, fragment 0.03 Da
- Search: Mascot v2.5 against Swiss-Prot human; quantification with Proteome Discoverer 1.4
- Probable factors: `factor value[genetic modification]` (NC siRNA vs MYDGF siRNA) and
  `factor value[cell line]` (WI-38 / CL1-5 / PE089)

## To unblock

- Get the TMT channel assignment (126–131 ↔ cell line × siRNA) from the J Proteome Res
  methods or supplementary tables, or from the submitters. The other way is to read the
  reporter-channel/sample labels stored in the deposited `.msf` (Proteome Discoverer study
  factors), which is 6.7 GB.
- Confirm that s01–s72 are fractions of one plex, not several plexes.
- Then annotate it as a **TMT** dataset (labels `TMT126` … `TMT131`, one row per raw file per
  channel = 432 rows), validate, and promote it to `datasets/`. It should not be filed as SILAC.
