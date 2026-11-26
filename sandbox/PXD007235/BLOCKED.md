# BLOCKED: PXD007235 — no SDRF yet

**Dataset:** [PXD007235](https://www.ebi.ac.uk/pride/archive/projects/PXD007235), "Extensive and systematic rewiring of histone post-translational modifications in cancer model systems" (Noberini *et al.* 2018, *Nucleic Acids Res*, PMID 29618087, [PMC5934616](https://europepmc.org/article/PMC/PMC5934616)).
**Design:** super-SILAC histone PTM profiling, plus a label-free global proteome and a few gel-band runs.
- **Super-SILAC mix:** MDA-MB-231/-468/-453/-361 grown on Arg10 (paper Methods, "Super-SILAC"). The paper says the same standard was used for all samples.
- **Digestion:** in-gel D6-acetic anhydride or propionic anhydride derivatisation, then trypsin.
- **Runs and instrument:** 264 RAW files on a Q Exactive HF.

## What the public evidence resolves
The paper's Methods and the Supplementary PDF (`gky224_supp.zip`, Tables S1–S3) give these maps:
- **Breast cancer cell lines (Table S1):** subtypes and media for each line. They cover runs `H3_<line>_{1,2}` (in-gel) and `H4sol_<line>_{1,2}` for 231, 361, 415, 436, 453, 468, BT474, MCF7, SKBR3/SKRB3, SUM (SUM149) and T47D.
- **Breast primary samples, patients 1–10 (Table S2):** subtype, ER/PR/HER2 status, and which patients have frozen tissue and a 2D primary culture. They cover runs `H3_/H4_frozen<n>[_rep]` and `H3_/H4_prim<n>[_rep]`. Normal breast is `frozennormalbreast1-3`.
- **Glioblastoma patients 1–33 (Table S3):** diagnosis, sample type and culture passages. They cover:
  - `FFPE1-11` and `Frozen11-16` / `frozen12,14`
  - `Prim3D<pt>p<passage>` and `Prim2D<pt>p<passage>` (passage numbers match Table S3)
  - `Xeno1,3,4,22,23,24`: PDXs from 3D cells, human tumour in nu/nu CD1 mouse brain, FFPE
- **GBM cell lines:** U87, U118, U138, T98G and LN405, plus their xenografts `XenoU87`, `XenoU872`, `XenoU118` and `XenoLN405`.
- **Other cell lines:** ovarian A2780, CAOV3, HEY and OVCAR3; MCF10A; and HB100 (HBL-100).

## Why this is blocked
Each of the following has no public evidence for the run → sample map, or conflicts with it:
1. **Label-free global proteome (46 runs):** `p0_<a>_<b>` (21 runs), `p5_<a>_<b>` (18), `short_1-3` and `long_1-3`.
   - Dataset S3 (`proteinGroups`) has only `p0 1-3`, `p5 1-3` and `p20 1-3` triplicates.
   - The deposited names (`p0_1_1` … `p0_7_3`, `p5_1_1` … `p5_6_3`) cannot be matched to those columns. Which patient each run comes from and what `<a>` means are not stated.
   - These runs are also label-free, so they would need their own SDRF.
2. **Ovarian primary and frozen tissue:** `OvPrimary4-7` and `Ovfrozen1-4`. The text cites an ovarian sample table (mixed high-grade serous and mucinous borderline cystadenoma samples, with chemotherapy history), but it is not in the Supplementary PDF.
3. **`H3_546_*` / `H4sol_546_*`:** there is no "546" line in Table S1.
4. **`A172`:** this GBM line is not listed in the Methods.
5. **`Brain_1-3`:** the text says normal mouse brain tissue and murine neural stem cell neurospheres from C57BL/6 mice were both analysed. Which one these runs are, the organism, and the storage are not stated per run.
6. **`HF180109_RN_PRO_700142_*` (8 runs):** the SI describes gel bands at the NSD2/NSD3 or SETMAR molecular weights from sh-infected GBM patient #4 neurospheres. Whether these are SILAC or label-free, and the controls (`C`, `C2`), are not described.
7. **Derivatisation per run** (D3-acetyl vs propionyl), which sets the modification parameters per run: the paper describes both protocols but does not say which one each run used. The 15 MaxQuant `txt*.rar` archives may resolve this, but they have not been checked yet.

## What would unblock it
- **Run 3:** Recover the map for the label-free proteome runs, or split them out and annotate them separately.
- **Run 2:** Obtain the ovarian sample table.
- **Run 1:** Read `parameters.txt` / `summary.txt` in each MaxQuant archive for per-run labels and modifications.

After that, annotate as two SDRFs in one folder:
- `PXD007235.sdrf.tsv`: SILAC histone runs, following the house style of `datasets/PXD057150`.
- `PXD007235-proteome.sdrf.tsv`: label-free runs.

The organism, `human` vs `vertebrates`, has to be handled for the xenograft and mouse-brain runs.
