# PXD018652 SDRF annotation report

## Study
Protein expression of isolated B cells from splenocytes in the collagen-induced arthritis (CIA) model, wild type (C57BL/6) vs Sting gt/gt mice. Tansakul M et al., "Deficiency of STING Promotes Collagen-Specific Antibody Production and B Cell Survival in Collagen-Induced Arthritis", Front Immunol 2020;11:1101. DOI 10.3389/fimmu.2020.01101, PMID 32582187, PMC7283782. The Methods say the dimethyl labelling and LC-MS/MS were done "as described in" Makjaroen et al., Mol Cell Proteomics 2018;17:2197 (PMC6210224), the paper's reference 28.

**Status: sandbox.** All 48 runs are mapped from stated design. The instrument, fractionation method and search/acquisition parameters are taken from a cited protocol paper, not from this dataset's own files.

## Scope, evidence and decisions
The SDRF has 96 rows (48 RAW x 2 dimethyl labels).

- **Deposited files** (ProteomeCentral PROXI, Page URL checked for PXD018652): 108 files, matching the campaign cache.
  - `TotalSet{1-6}F{1-8}.raw` (48) and matching `.mgf` (48)
  - `TotalSet{1-6}F.msf` (6) and `TotalSet{1-6}F.pdResult` (6)
- **Deposited vs annotated:** 48/48 RAW annotated, none excluded. The mgf, msf and pdResult files are derived files and get no rows.
- **Design (STATED, paper):**
  - WT peptides were labelled light (formaldehyde + cyanoborohydride) and Sting gt/gt peptides medium (formaldehyde-d2 + cyanoborohydride).
  - Each pair was pooled and split into eight fractions.
  - The Figure 5 legend says "N = 6 samples per group, and each sample consist of 2 mice".
  - There are 6 deposited TotalSets x F1-F8. TotalSet k = WT pool k (DIMETHYL0, UNIMOD:36) + Sting gt/gt pool k (DIMETHYL4, UNIMOD:199, +32.056407 = CHD2).
  - Pools are numbered by set. Each set holds exactly one WT and one gt/gt sample, so no external key is needed. The pool index is an identifier only.
- **Samples:**
  - Mus musculus, spleen (UBERON:0002106), B cell (CL:0000236).
  - B cells isolated by negative selection with anti-CD43 (Miltenyi), up to 95% purity.
  - Collected 3 weeks after the first CII + CFA injection, at an immunization age of 10-14 weeks. Developmental stage = adult.
  - Strain C57BL/6 (PX title; gt/gt is an ENU allele on a C57BL/6 background). Fraction identifier = F number.
- **Genotype:** encoded as `characteristics[genotype]` plus `factor value[genotype]`, which is licensed by declaring `clinical-metadata` (same pattern as PXD002560).
- **Search and acquisition, INFERRED from reference 28 (Makjaroen 2018):**
  - DTT/IAA reduction and alkylation; trypsin.
  - Fractionation by hpHRP (Pierce kit; 10 fractions in the 2018 study, 8 here).
  - HCD at 32% NCE; MS1 range 350-1400 m/z.
  - PD 2.1 SEQUEST, 10 ppm / 0.02 Da.
  - Fixed: carbamidomethyl C, plus light or medium dimethyl on K and N-terminus per channel. Variable: oxidation M.
  - The PX modification list (MOD:00397 iodoacetamide derivatized, MOD:00425 monohydroxylated, MOD:00394 acetylated) agrees with this. It also implies an acetyl variable mod, which I added as `Acetyl PP=Protein N-term Variable`. **The site is INFERRED** (the usual PD default); no source states it.
- **Deposited search outputs not read:** the shell has no internet, so the msf/pdResult could not be read with HTTP range requests. They would settle the modifications and tolerances.

## Values left not available / not applicable
- `characteristics[sex]` = not available: sex is not stated in the paper or the PX record.

## Conflicts and open points (why sandbox)
1. **Instrument.** PX says Q Exactive (MS:1001911). The cited protocol (reference 28, a different 2018 experiment) used a "Q-Exactive Orbitrap Plus". The 2020 paper names no instrument, and the RAW header could not be read (no shell network). I kept the deposit's own declaration, Q Exactive; this is unresolved.
2. **Parameters from another paper.** Fractionation method, NCE, scan range, tolerances, reagents and modifications all come from reference 28, via "as described in". Mascot/MaxQuant are not involved; the 2020 paper mentions PD 2.1 and MaxQuant 1.4.1.0.
3. **Acetyl site.** Inferred (point above).
4. **Disease term.** I used rheumatoid arthritis (MONDO:0008383) as the disease the CIA model stands for. I could not check whether a dedicated CIA term exists because OLS was down. B cells were taken 3 weeks after the first immunization, before the booster, when the mice may not yet show clinical arthritis.

## Term verification
Every accession was checked live on 2026-11-25. EBI OLS4 and Europe PMC were unreachable or rate-limited all session, so I used other sources:
- ontobee for MS, UBERON, CL, NCBITaxon and MONDO
- unimod.org for UNIMOD 1/4/35/36/199
- PRIDE-Utilities `pride_cv.obo` for the PRIDE terms

Evidence files are in `/home/claude/bangkok3/scratch/PXD018652/`.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` passes for each of ms-proteomics, vertebrates and clinical-metadata with no errors. Only structural validation ran: the OLS extras are not installed, so ontology checks were skipped.

## Review status
pending
