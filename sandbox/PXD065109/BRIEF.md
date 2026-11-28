# PXD065109 SDRF annotation report

## Study
A sEH/COX-2 Dual Inhibitor PTUPB Reduces Endothelium-to-Mesenchymal Transition and Improves Doxorubicin-induced Vascular and Cardiac Toxicity (Qatar University, Doha). Paper: Dhulkifle H, Therachiyil L, Hasan MH, Younis SM, Al-Shar'i NA, Yalcin HC, Maayah ZH. Mol Med Rep 33:100 (2026), doi:10.3892/mmr.2026.13810. The paper's data availability statement cites PXD065109 (verified). The PX record still says "publication pending".

## Scope, evidence and decisions
Status: **sandbox**. There are 12 rows (12 runs, label-free) and 33 columns. Templates: ms-proteomics and vertebrates (v1.1.0).

- **Deposited vs annotated:** The PROXI record (`resultType=full`, 2026-11-27) lists 12 Bruker `.d.zip` raw files plus `Zebrafish_Full_dataset.xlsx` (the search output). All 12 raw files are annotated and none are excluded. The PRIDE FTP folder and the EBI services (PRIDE API, OLS, Europe PMC) timed out today, so the file list comes from PROXI alone.
- **Run to sample mapping (STATED):** The file names encode the group and replicate: 4 groups x replicate1-3. The paper states 4 groups and "three tubes per group, each with eight embryos", which matches 3 x 4 = 12 runs.
  - `characteristics[pooled sample]` = `pooled`: each tube holds 8 whole larvae.
  - Biological replicate = the replicate number in the file name.
- **Organism and sample (STATED):** Danio rerio, wild-type AB strain, whole larvae homogenised in RIPA buffer.
  - Organism part and material type = `whole organism`.
  - Embryos were randomized at 24 hpf and assessed at 72 hpf.
  - Developmental stage = `larval stage`. This is an EFO label. At 72 hpf the larvae are at the hatching/early larval boundary.
- **Treatment (STATED):** The groups are vehicle (0.1% DMSO), PTUPB 1 uM, doxorubicin 100 uM, and doxorubicin 100 uM + PTUPB 1 uM. Larvae were kept at 28.5 C.
  - Exposure duration is left out of the treatment value because the sources conflict (see Conflicts).
  - `factor value[treatment]` is the last column.
- **MS (STATED, paper):**
  - Instrument: timsTOF Pro (MS:1003005; this agrees with PROXI).
  - Acquisition: DDA, top-10 precursors, 400-1800 m/z, singly charged ions excluded, dynamic exclusion 25 s.
  - Search: MaxQuant 2.1.4.0 / Andromeda against Swiss-Prot zebrafish, with MaxLFQ.
  - The raw-file headers could not be read because the FTP was unreachable.
- **Cleavage agent (INFERRED):** Trypsin. The paper only says "previously described method" and cites Mol Biol Rep 51:859 (2024) and J Proteomics 295:105108 (2024). Neither fetched text names the enzyme; the J Proteomics full text was not reachable. Trypsin is assumed from the MaxQuant "standard workflow" and LFQ context. The column forbids `not available`.

## Values left not available / not applicable
- **Not available (unstated in the paper and the cited Mol Biol Rep method):** reduction reagent, alkylation reagent, modification parameters, precursor and fragment tolerances, and dissociation method.
  - The modifications were not filled with MaxQuant defaults because the brief requires them to come from the deposited search.
  - The deposited `Zebrafish_Full_dataset.xlsx` could not be opened (FTP down).
- **Not applicable:** sex and cell type. Larvae at 72 hpf are sexually undifferentiated, and the sample is whole organism.
- **Disease** = `normal` for all groups. The animals are wild type, and the DOX-induced toxicity is captured as a treatment, not a disease.

## Conflicts
- The Methods state a 72 h exposure, but treatment ran from 24 hpf to 72 hpf (48 h), and the Figure 3A legend says 48 h. Duration is therefore not encoded.
- PROXI `modifications` says "No PTMs"; this is not used.

## Validation
- `parse_sdrf validate-sdrf --template ms-proteomics --template vertebrates --use_ols_cache_only`: "Everything seems to be fine". Ontology validation was skipped because the OLS dependencies are not installed.
- `sdrf_review.py`: [OK].
- Accessions were NOT re-verified live today because OLS and the EBI services were unreachable. The accessions used are:
  - MS:1003005 (timsTOF Pro), copied from the PX record;
  - MS:1001251 (Trypsin);
  - PRIDE:0000627 (DDA), as used in prior campaign files.

## To upgrade to annotated
- The J Proteomics 295:105108 methods (enzyme, DTT/IAA).
- The MaxQuant parameters, from the deposited xlsx or an mqpar.

## Review status
pending
