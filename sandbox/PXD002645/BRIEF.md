# PXD002645 SDRF annotation report

## Study
Proteomic profiling of ubiquitylated proteins in urinary exosomes. Huebner AR, Cheng L, Somparn P, Knepper MA, Fenton RA, Pisitkun T. Deubiquitylation of Protein Cargo Is Not an Essential Step in Exosome Formation. Mol Cell Proteomics 2016;15(5):1556-1571. doi:10.1074/mcp.M115.054965, PMID 26884507, PMC4858939 (full text read on PMC).

## Status: sandbox
The SDRF validates and every deposited RAW is in it, but three run-to-design mappings are INFERRED, not stated (see Conflicts / inferred).

## Scope, evidence and decisions
72 rows x 43 columns, one row per deposited Thermo RAW file (label-free, 1 file = 1 row). Templates: ms-proteomics v1.1.0 + human v1.1.0 (human extends sample-metadata, which licenses `pooled sample` and `enrichment process`).

**Campaign cache was wrong.** It said "mgf/msf only, no RAW listed". The PX record (proxi full) lists 72 `Associated raw file URI` entries, and the FTP directory listing shows them at 1.0-1.4 GB each, with the RAW files next to the mgf files. Deposited files: 72 RAW + 72 mgf (same basenames), 8 PD 1.4 `.msf` (IP runs only), 4 MaxQuant `msms.txt` + `apl.zip` pairs (`Exo_1st_run`, `Exo_Rerun`, `Exo_Rerun_Miss2`, `Exo_UbiRemIP`), and about 150 GPM X!Tandem `*_peptides.xls`.

**Deposited vs annotated:** all 72 RAW files are annotated. Nothing was excluded.
- `Exo01-32.raw` (32): SDS-PAGE gel slices 1-32, technical replicate 1. Paper: "fractionated into 32 pieces".
- `ReExo02-32.raw` (31): gel slices 2-32, technical replicate 2. Paper: "two technical replicates for all samples".
- `Exo01_105min.raw` (1): gel slice 1, technical replicate 2 (INFERRED; see below).
- `Exo_UbiRemIP_01-04.raw` (4) and `R2Exo_UbiRemIP_01-04.raw` (4): K-epsilon-GG immunoaffinity-purified peptides, runs 1-4, technical replicates 1 and 2.
- The AQUA runs (5 biological replicates) are not identifiable among the deposited files and are not annotated.

**Sample:** urinary exosome fraction (200,000 x g low-density membrane pellet) from urine pooled from 20 healthy volunteers (10 male, 10 female, 19-45 y, "various ethnic backgrounds"; Denmark). Two source names split the two prep arms: `urinary_exosomes_pool20_SDS-PAGE` (in-gel arm) and `urinary_exosomes_pool20_KeGG-IP` (in-solution Lys-C + trypsin, PTMScan #5562 K-epsilon-GG IP). It is the same biological pool. organism part = urine (UBERON:0001088); material type = organism part; disease = normal; developmental stage = adult (from the stated 19-45 y). biological replicate / pooled sample / age / sex / individual = `pooled`.

**Technical values (paper Methods unless noted):** Q Exactive (MS:1001911; paper and PX agree; RAW header NOT read because the shell has no network); DDA top-10; HCD 35% NCE; MS1 70k, MS2 17.5k (Orbitrap). MS1 range: 200-2000 m/z for the gel arm, 300-1500 m/z for the IP arm. Tolerances: 10 ppm precursor and 10 ppm fragment. Cleavage: trypsin for the gel arm; Lys-C (1:100, 4 h) then trypsin (1:25, overnight) for the IP arm. Alkylation: chloroacetamide 55 mM for the IP arm (PRIDE:0000600). Fractionation: SDS PAGE (PRIDE:0000568) for the gel arm.

**Modifications:** Carbamidomethyl C fixed (UNIMOD:4), and variable Oxidation M (UNIMOD:35), GG K (UNIMOD:121) and LRGG K (UNIMOD:535) are from the paper ("X! Tandem, Andromeda, SEQUEST ... consensus"). Acetyl Protein N-term variable (UNIMOD:1) is from the deposited `Exo_UbiRemIP_MQ_msms.txt` header (variable-mod columns: Acetyl (Protein N-term), GlyGly (K), Oxidation (M)). The paper does not mention it. It is kept because the deposited search output outranks prose. That MQ search has no LRGG column, so LRGG comes from the other engines per the paper. Max 3 missed cleavages (paper; no SDRF column). The PD `.msf` workflows were NOT read (no HTTP-range from the shell; the browser cannot range-read SQLite).

## Values left not available / not applicable and why
- `comment[reduction reagent]` = not available (both arms). Gel arm: "reduced and alkylated as described (14)", reagent not named. IP arm: "Samples were reduced", reagent not named; DTT is named only as the quench after alkylation, so it was not entered as the reductant.
- `comment[alkylation reagent]` = not available for the gel arm (reference 14 not consulted; the PX `iodoacetamide derivatized residue` is a modification, not a reagent statement).
- `comment[fractionation method]` = not available for the IP runs, because what 01-04 denote is unknown.
- `comment[cleavage agent details]` (2nd column) = not applicable for gel rows (single enzyme).
- `characteristics[enrichment process]` = not applicable for the gel arm (no enrichment).
- `characteristics[ancestry category]` = not available ("various ethnic backgrounds", not itemised).
- `characteristics[cell type]` = not applicable (body-fluid vesicle fraction).

## Conflicts / INFERRED (reviewer: attack these)
1. **`Exo01_105min.raw` = gel slice 1, technical replicate 2 (INFERRED).** No `ReExo01.raw` exists. Slice 1 of the rerun series appears to have been run with a 105-min gradient instead. This rests on file naming and the gap in the ReExo series. Only the RAW size (1.4 GB vs 1.0-1.3 GB for the others) hints at a longer run. The 137 MB MQ `Exo_Rerun_MQ_msms.txt` was not read to confirm it.
2. **`*_UbiRemIP_01-04` encoded as fraction identifier 1-4 (INFERRED).** The paper describes one IP protocol (1 mg peptides, 4 uL beads) and never says why there are 4 runs. The mgf sizes fall steadily (16 / 12 / 8.4 / 8.3 MB), which fits serial IPs/elutions or fractions as well as replicate IPs.
3. **`R2Exo_UbiRemIP_01-04` = technical replicate 2 (INFERRED from the "R2" prefix).** The deposited MQ `Exo_UbiRemIP_MQ_msms.txt` lists Raw files `Exo_UbiRemIP_01-04` and `ReExo_UbiRemIP_01-02` only. It has no `R2Exo*` names and no ReExo_UbiRemIP_03/04. So the MQ names do not reconcile one-to-one with the deposited R2Exo files (renamed at deposition, or 03/04 were never searched in MQ).
4. **Trypsin for the in-gel arm** is from the cited in-gel protocol (ref 2) and the tryptic search, not from an explicit statement in this paper.
5. **Instrument model** not confirmed from the RAW header.
6. **Ontology checks:** EBI OLS, Europe PMC and the PRIDE API were unreachable or rate-limited today. Accessions were verified on unimod.org, Ontobee (UBERON/MS) and the PRIDE CV obo on GitHub (scratch `accession_checks.txt`). The local parse_sdrf has no OLS cache ("structural validation only").

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics --template human`: "Everything seems to be fine" (structural only; ontology validation unavailable in this install).

Evidence files: `/home/claude/bangkok3/scratch/PXD002645/` (px_record_notes.txt, raw_files.txt, paper_PMC4858939_methods.txt, mq_ubiremip_msms_notes.txt, accession_checks.txt, build.py).

## Review status
pending
