# PXD024983 SDRF annotation report

## Study
Bifunctional dehalogenases in Dehalococcoides mediate complete debromination of penta- and tetra-brominated diphenyl ethers (NUS, Singapore; submitter Siyan Zhao, lab head Jianzhong He).

Paper: Zhao S, Rogers MJ, Cao L, Ding C, He J. *Identification of Reductive Dehalogenases That Mediate Complete Debromination of Penta- and Tetrabrominated Diphenyl Ethers in Dehalococcoides spp.* Appl Environ Microbiol 2021;87(17):e00602-21. doi:10.1128/AEM.00602-21, PMC8357287, PMID 34160266. The PX record says "publication pending", but the paper's Data availability statement cites PXD024983, so the link is verified. Its MS method refers to ref. 43: Seidel K, Kuhnert J, Adrian L. Front Microbiol 2018;9:1130 (PMC6005880).

## Scope, evidence and decisions
Status: **sandbox**. The file has 4 rows (4 RAW, label-free) and 29 columns, with template `ms-proteomics` v1.1.0.

**Deposited vs annotated.**
- The PRIDE FTP holds 10 files: 4 `.raw`, the PD 2.2 result set (`2019_TZ50_new_database.msf` 3.6 GB, `.msfView`, `.pdResult`, `.pdResultView`), `checksum.txt` and `README.txt`.
- The PX record lists 9 of them; `README.txt` is not in it.
- All 4 RAW are annotated, so no run is left out.
- The cached "4 RAW / 9 files" figure is correct for the PX record.
- RAW names on the FTP use underscores, for example `PCE_enriched_TZ50_proteomics.raw`. PRIDE renamed them on 2023-05-07. The PX record, README and checksum use the original names with spaces. `comment[data file]` uses the current FTP names.

**Samples.** Paper Results: "Prior to obtaining the isolate of strain TZ50, protein profiles of the TZ50 enrichment culture amended with different electron acceptors (PCE, TCE, or the penta- and tetra-BDE mixture) were elicited". Methods give the cultures:
- penta-/tetra-BDE mixture (BDE-47/99/100 1:1:1), 1.5 uM, 500 ml culture
- PCE 0.6 mM, 300 ml
- TCE 0.6 mM, 300 ml

All were grown in DCB-1 medium with acetate (10 mM) and H2 (0.3 atm), each after at least six transfers on that substrate. File names map one to one to the substrate (PBDE / PCE / TCE), so the run-to-condition map is STATED by file name plus paper. Each substrate is one `source name`. The substrate is recorded in `characteristics[treatment]` and `factor value[treatment]` as free text.

**Organism / strain.**
- Organism: `Dehalococcoides mccartyi` (NCBITaxon:61435). PX species, the BioProject PRJNA564712 TaxId and NCBI taxonomy (checked live) agree. TZ50 has no strain-level taxon (NCBI taxonomy search returned 0 hits).
- `characteristics[strain or breed]` = `TZ50`.
- Material type: `whole organism` (cultured cells; PXD002912 precedent).
- Organism part, cell type and disease: `not applicable`.
- **Caveat:** the proteomes come from the TZ50 *enrichment culture*, not from the later pure isolate. Earlier 16S data show other taxa (Proteiniclasticum, Clostridiales fam. IX, Veillonellaceae, Coriobacteriaceae, Rikenellaceae; Dehalococcoides 20.9%). The later metagenome is 99.06% Dehalococcoides. The search database was only the D. mccartyi metagenome bin, so a single organism matches what was identified. It does not cover the full biomass. I did not use the metaproteomics template: its required environmental fields do not fit a lab enrichment, and the search was single-organism.

**Technical.**
- Instrument: Orbitrap Fusion (MS:1002416). The paper ("Orbitrap Fusion Tribrid") and the PX record agree. The RAW header was not read: these are multi-GB binaries and the shell has no network.
- Trypsin: stated in the paper.
- DDA (PRIDE:0000627): INFERRED from PD 2.2 Sequest HT + Minora LFQ and from the cited method (top-2 data-dependent).
- Label free sample (MS:1002038): stated ("label-free quantification").
- Precursor tolerance 3 ppm, fragment tolerance 0.6 Da, Carbamidomethyl C fixed (UNIMOD:4), Oxidation M variable (UNIMOD:35): **INFERRED** from ref. 43's Proteome Discoverer 2.2 settings, cited as "as previously described". That method was applied to gel slices of strain CBDB1. The deposited `.msf`, which is authoritative, was not read: 3.6 GB, and no HTTP range access was available from this environment.
- Fraction identifier: 1, since there is no fractionation.

## Values left not available / not applicable
- `comment[dissociation method]` = not available. Ref. 43 says precursors were "subjected either to" HCD 30% or CID 35%, so the activation used in these runs is not determinable without the RAW/msf.
- `comment[reduction reagent]`, `comment[alkylation reagent]` = not available. The TZ50 paper names neither. Ref. 43 mentions only "cysteine derivatization", and its search uses fixed carbamidomethyl. The step is assumed to have happened, so the value is `not available`, not `not applicable`.
- Organism part / cell type / disease = not applicable: a cultured bacterium, no host tissue or disease.

## Stated vs INFERRED
- STATED: run to substrate (file names + paper Methods), organism, strain TZ50 (enrichment population), trypsin, Orbitrap Fusion, label-free, PD 2.2 Sequest HT / Minora.
- INFERRED:
  1. The two PBDE runs (`-proteomics`, `-proteomics-2`) are technical replicates 1/2 of one culture (biological replicate 1). The paper describes a single 500-ml PBDE culture and gives no replicate statement.
  2. DDA.
  3. Tolerances and modifications from ref. 43.

## Conflicts
- The PX `modifications` field says "No PTMs are included in the dataset", which disagrees with the cited search (fixed CAM, variable Met-ox). The cited method was used, flagged as inferred.
- The PX record shows the publication as pending, but it is published (AEM 2021).
- FTP file names have underscores while the PX record names have spaces. The FTP names were used.
- The PX record does not list `README.txt`.

## Validation
- `parse_sdrf validate-sdrf --use_ols_cache_only` with and without `--template ms-proteomics`: "Everything seems to be fine". Structural only: the OLS cache dependencies are not installed.
- `sdrf_review.py`: [OK].
- Accessions were verified live via NCBI eutils, ontobee (MS), unimod.org and the PRIDE CV obo on GitHub. OLS4 and Europe PMC were down today.
- `characteristics[strain or breed]` is not licensed by `ms-proteomics`. No bacterial template licenses it. It was kept as in campaign precedents PXD001373 / PXD002912 / PXD006630, because the strain matters for this dataset.

Evidence: `/home/claude/singapore1/scratch/PXD024983/`.

## Review status
pending
