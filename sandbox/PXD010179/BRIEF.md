# PXD010179 — pSILAC-AHA spatiotemporal proteomics of RAW264.7 macrophages infected with *Salmonella* Typhimurium

BLOCKED: 8 of the 80 deposited raw files (`20151002_JS_111.raw` … `20151002_JS_118.raw`) cannot be mapped to a sample from public evidence. This SDRF annotates the other 72 files (144 rows) and stays in `sandbox/` until the 8 files are resolved, e.g. by the submitters.

Sources: [PRIDE PXD010179](https://www.ebi.ac.uk/pride/archive/projects/PXD010179); Selkrig et al., *Nat Microbiol* 2020, [doi:10.1038/s41564-020-0736-7](https://doi.org/10.1038/s41564-020-0736-7) (PMC7610801); the deposited `MaxQuant_Output.zip`, which contains `sample list for deposit.xlsx`, `summary.txt`, `parameters.txt`, `msScans.txt` and `proteinGroups.txt`.

## Why 8 files are unresolved

- The authors' sample list and MaxQuant `summary.txt` both name `20151002_JS_011`–`018` as the replicate-1 t0 lysatome (8 high-pH fractions). In `msScans.txt` those are 60-minute runs. They were **not deposited**.
- The deposited `20151002_JS_111`–`118` are in neither the sample list nor the search output. Their raw headers record their own file names and a different 120-minute method (`100min_grad_120min_run_Waters_Top15.meth`, vial 2:C,1). The replicate-2 lysatome `_021` used a 60-minute method at vial 2:B,1. So they are separate runs, not renamed copies of 011–018, and they are not annotated.

## What is resolved

- **Design:** RAW264.7 cells (CVCL_0493, ATCC TIB-71), mock or *S.* Typhimurium 14028s infection (MOI 100:1). Cells were pulse-labelled for 3 h with AHA plus SILAC medium (Arg6/Lys4, "intermediate") or heavy (Arg10/Lys8) amino acids, then mixed 1:1 infected:uninfected. Three compartments were collected: secretome (`extracellular region`), Tx-100-soluble lysatome (`cytoplasm`; 8 hpH fractions) and Tx-100-insoluble nucleome (`nucleus`). AHA-containing proteins were enriched by click chemistry.
- **Labels:** in replicate 1 uninfected = SILAC medium and infected = SILAC heavy; replicate 2 is swapped. This was verified independently: Supplementary Table 1 replicate log2(infected/uninfected) ratios correlate at r=+1.00 (rep 1) and r=−1.00 (rep 2) with MaxQuant `Ratio H/M normalized`. The light channel holds pre-existing protein and has no rows.
- **Time points:** sample-list codes t1/t2/t3 = 4/8/20 hpi, verified by the same correlation. **t0** is deposited and searched but not reported in the paper, so its `sampling time` is `not available` (24 rows).
- **Instrument:** Orbitrap Velos Pro, CID, ion-trap MS2, Top15 DDA, from raw headers and the paper. The PRIDE record's "Q Exactive" is wrong.

## Notes for reviewers

- `characteristics[cellular component]` and `characteristics[infectious agent]` are additions outside the declared templates. `cytoplasm` is an approximation: per the paper, the lysatome is nuclear-free lysate with cytoplasmic and organelle content.
- `sdrf-tools check` flags `NT=Met->Aha;AC=UNIMOD:896` as hallucinated. That is a false positive: it is the OLS label and MaxQuant's `Met->AHA`.
- There is no column for the AHA click-chemistry enrichment: no fitting EFO enrichment-process term exists.

Validated: `parse_sdrf validate-sdrf -t ms-proteomics -t vertebrates -t cell-lines` exits 0 with one warning (BALB/c strain is free text). Checked 2026-11-22.
