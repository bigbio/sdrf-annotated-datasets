# PXD008090 SDRF annotation report

## Study
Proteomic Profiling of Barley Spent Grains (PRIDE PXD008090; Bioprocessing Technology Institute, A*STAR, Singapore).
Paper: Bi X et al., "Proteomic profiling of barley spent grains guides enzymatic solubilization of the remaining proteins", Appl Microbiol Biotechnol 2018;102(9):4159-4170, doi 10.1007/s00253-018-8886-8, PMID 29550991, no PMCID. The paper is closed access (Unpaywall: closed); I read the full text from the A*STAR OAR repository PDF (record 15627). The paper's Data availability section and its Europe PMC abstract cite PXD008090, so the PX link is correct.

Status: **sandbox** (6/6 RAW mapped; the replicate index is INFERRED from the file-name suffix; RAW headers and MaxQuant txt.zip unread because the PRIDE FTP timed out).

## Scope, evidence and decisions
6 rows x 36 cols, label-free DDA, one row per RAW file, no fractions. Templates: `ms-proteomics` v1.1.0 + `plants` v1.1.0, both declared on every row.

**Deposited vs annotated.** I took the file list from ProteomeCentral PROXI (`resultType=full`; the page URL and accession were checked). It lists 17 files, 6 of them RAW, so the campaign cache count is confirmed:
- 6 RAW, all annotated: `SGA-SDS-FASP-20150115-1`, `SGA-SDS-FASP-20150212-2`, `SGA-SDS-FASP-20150212-3`, and the same three names for SGB.
- 11 non-RAW files, not rows: 2 mzid.gz, 4 MGF/mgf.gz, 2 mztab.gz (one combined "3Replicates" search per grain), `txt.zip` and `andromeda.zip` (MaxQuant), and `NCBInr_Hordeumvulgare20170206.fasta`.
- No gel-band or 2D-spot runs are deposited, although the paper analysed them by LC-MS/MS. Only the shotgun FASP arm is in PRIDE.

The saved file list is in scratch/PXD008090/proxi_filelist.txt.

**Sample mapping:**
- **Grain (stated).** The `SGA`/`SGB` prefix comes from the paper. SGA is spent grain from malted barley. SGB is spent grain from non-malted barley mashed with a proprietary mix of exogenous enzymes (Nestle R&D Singapore). The paper states 3 biological replicates for shotgun.
- **Replicate number (INFERRED).** I took it from the `-1/-2/-3` file suffix and set biological replicate 1-3 and technical replicate 1. Replicate 1 was run on 20150115 and replicates 2-3 on 20150212. No source says per file that each suffix is a separate biological replicate rather than a re-injection.
- **Factor.** `factor value[treatment]` is "malted barley" vs "raw barley plus exogenous enzymes" (my wording).

**Technical values (paper Methods; PROXI agrees where it has the field):**
- Instrument: LTQ Orbitrap Elite (MS:1001910; the PROXI instrument term and the paper agree; RAW header not read).
- nanoAcquity with a BEH130 C18 column, 75 um x 200 mm, 105 min gradient.
- Top-15 DDA, 120,000 resolution, m/z 350-1800; CID at NCE 35.
- Trypsin, by FASP on a 30 kDa cut-off filter.
- Sequest HT (PD 1.4) and PEAKS 8.0: 10 ppm precursor / 0.6 Da fragment tolerance, Carbamidomethyl C fixed, Oxidation M and Deamidated N/Q variable. MaxQuant 1.5.2.8 LFQ used the same modifications. The PROXI modification list (UNIMOD:4/7/35) matches.
- Organism: Hordeum vulgare, NCBITaxon:4513 (PROXI TaxID).
- Organism part: seed (PO:0009010, checked live in OLS). Spent grain is the mashed grain residue.

## Values left not available / not applicable
- `reduction reagent`, `alkylation reagent`: **not available**. The FASP prep says only "reduced, alkylated". The 20 mM DTT / 55 mM IAA values belong to the in-gel protocol, whose runs are not deposited, so I did not carry them over.
- `developmental stage`, `strain or breed`: **not available**. The cultivar and the malting/mashing stage are not stated.
- `growth condition`: **not applicable**. This is a processed brewing by-product, not a grown plant.
- `disease`: **not applicable**.
- `fractionation method`: **not applicable** (no fractionation).
- `ms2 mass analyzer`: column omitted. The ion trap is only implied by CID with a 0.6 Da fragment tolerance and is not stated.

## Conflicts and unread sources
- The paper names the search database inconsistently: "NCBI barley, 38,557 entries" in one place and "NCBInr" restricted to barley in another. The deposited fasta name (`NCBInr_Hordeumvulgare20170206`) fits both. This does not affect SDRF columns.
- The PRIDE FTP folder (2018/03/PXD008090) timed out, so the RAW headers and MaxQuant `txt.zip` (`parameters.txt`, `summary.txt`) were not read. They could confirm the instrument, the modifications and the replicate naming used in the experimental design.
- The OLS API was unreachable for NCBITaxon:4513 and MS:1001910. I relied on the PROXI CV terms and on the same accessions already reviewed in earlier campaign files.

## Validation
- `parse_sdrf validate-sdrf --use_ols_cache_only`, run with ms-proteomics, with plants, and with both: no errors. Ontology lookup is not installed, so this was a structural check only.
- `sdrf_review.py`: [OK].

## Review status
pending
