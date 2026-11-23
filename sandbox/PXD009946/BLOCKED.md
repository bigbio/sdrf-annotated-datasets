# BLOCKED: PXD009946 — no SDRF yet

**Dataset:** [PXD009946](https://www.ebi.ac.uk/pride/archive/projects/PXD009946), "Alternative digestion approaches improve histone modification mapping by mass spectrometry in clinical samples" (Restellini *et al.* 2019, *Proteomics Clin Appl* 13:e1700166, PMID 30471193, doi:10.1002/prca.201700166).
**Design:** super-SILAC (Arg10 heavy spike-in) histone PTM study, 49 RAW files, Q Exactive HF.

## Why this is blocked

The paper is **closed access**: Unpaywall reports `closed`, and Europe PMC holds only the abstract. The PRIDE protocol text describes the methods but contains no sample table. Of the 49 runs, only 16 can be tied to samples from public evidence. A complete SDRF for the other 33 runs would require guessing the sample → file map, which the curation rules forbid.

### Resolvable: frozen breast tissue, Arg-C in-solution (16 runs)
The deposited MaxQuant output `txtbreastcancerfrozen.rar` (`parameters.txt` and `summary.txt`) gives these settings for every `HF180425_RN_*` run:
- Enzyme: ArgC
- Variable modifications: Acetyl (K), Methyl (KR), Dimethyl (K), Trimethyl (K)
- Fixed modification: Carbamidomethyl (C)
- Labels: multiplicity 2, Labels1 = Arg10
- Tolerance: MS/MS 20 ppm (FTMS)

**Sample map.** The design is described in a later paper from the same lab, Noberini *et al.* 2021, *Clin Epigenetics* (PMC8317427), Fig 4f: "Luminal A-Like BC samples (n = 5, matched), triple-negative BC samples (n = 3, matched)". That matches these runs:
- 5 luminal A-like tumours: `Lu6`–`Lu9` and `LuA10`
- 5 matched normals: `N_Lu6`–`N_Lu10`
- 3 TNBC tumours: `TN6`–`TN8`
- 3 matched normals: `N_TN6`–`N_TN8`

`summary.txt` also lists `HF180425_RN_TN9`, but that run is not deposited.

**Still missing for this subset:** the composition of the super-SILAC mix for this study. It is very likely the MDA-MB-231/-468/-453/-361 mix used in PXD057150 and PXD024799, but this paper does not state it in any open source.

### Not resolvable from public evidence (33 runs)
- **Ovarian cancer runs (17):** `HF180503_RN_ov_FF_*`, `HF180503_RN_ov_frozen_*`, `HF180731_FF_*` and `HF180731_FR_*`.
  - `evidence.txt` in `txtovarian.rar` uses different run names, e.g. `HF180503_RN_ov_FF_1 (41405)` for the deposited `HF180503_RN_ov_FF_141405.raw`. The deposited names therefore concatenate a run index with a patient code.
  - The patient codes are inconsistent: `41505` vs `41405`, and `70346` vs `70746`.
  - Whether "FF" means FFPE or fresh-frozen is not stated. Tumour vs normal status, the digestion protocol per run, and the spike-in are not stated either.
- **NB4 cell line runs (16):** `HF180731_RN_C18_1-4`, `HF180731_RN_ac_1-4`, `HF180904_RN_C18_5-8` and `HF180904_RN_Ac_5-8`. The archive name `txtNB4acme1me2me3` suggests the NB4 cell line (acute promyelocytic leukemia). The meaning of `ac` vs `C18` (acetone precipitation vs C18 StageTip enrichment?), the replicate structure and the digestion per run are not described in any open source.

## What would unblock it
- Access to the full text or Supporting Information of doi:10.1002/prca.201700166: the figure legends and sample tables.
- Or confirmation from the submitters (Bonaldi lab, IEO Milan) of the ovarian and NB4 run → sample map.

With either one, the 16 breast runs can be annotated as above, following the house style of `datasets/PXD057150`: one `SILAC light` and one `SILAC heavy` row per run, and `NT=Arg-C;AC=MS:1001303`.
