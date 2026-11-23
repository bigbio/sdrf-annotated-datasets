# PXD048931 — BLOCKED (sandbox draft)

**BLOCKED:** two parts of this dataset cannot be resolved from the public evidence
read. Both SDRFs therefore fail `cell-lines@1.1.0`, where `characteristics[cell line]`
is required and permits no reserved word. The whole-proteome file also fails
`ms-proteomics@1.1.0` (`comment[label]`, `comment[cleavage agent details]`).

1. **JAC45A / GTD12 arms** (`PXD048931-silac.sdrf.tsv`, sources `JAC45A_13h_*`,
   `GTD12_13h_*`, 144 rows). The preprint characterises one previously disclosed
   degrader, "compound 1" (Jurkat, 5 µM, 13 h, Fig 4b). The deposit holds two 13 h
   arms under lab codes JAC45A and GTD12
   (`Annotation_raw_data_and_searches.xlsx`: "211217 13h Degradation by JAC45A and
   GTD12"). No public source says which code is compound 1, or which cell line and
   dose the other arm used. Cell line and dose are `not available` on these rows.
2. **2024 whole-proteome runs** (`PXD048931-wholeproteome.sdrf.tsv`, 12
   `20240523_FS1_LMW55_dCEMM2_WP_*` files, dCeMM2/DMSO 2 h/4 h). They were acquired
   after the preprint and are not in the PRIDE protocol or the xlsx. Only file names
   and raw headers describe them (Orbitrap Fusion, DIA, HCD, Orbitrap MS2). Cell
   line, label, digestion, reduction/alkylation and dose are `not available`.

## Evidence

- Dataset: https://www.ebi.ac.uk/pride/archive/projects/PXD048931
- Preprint (read): Jochem et al., bioRxiv doi:10.1101/2024.01.28.577572 v1
  (Data availability cites PXD048931)
- Published version (not read, no open full text reachable): Cell Chem Biol 2025,
  doi:10.1016/j.chembiol.2024.10.007, PMID 39536762
- Search outputs: `mqpar.xml` in each deposited MaxQuant zip (file → replicate and
  fraction, labels, modifications, tolerances)
- Raw-file headers: instrument, acquisition mode, MS2 analyzer, HCD

## Files

| file | rows | content |
|---|---|---|
| `PXD048931-silac.sdrf.tsv` | 764 | 382 SILAC DDA raw files (Orbitrap Fusion, 12 or 8 high-pH RP fractions) × 2 channels: `SILAC light` = DMSO, `SILAC heavy` = drug |
| `PXD048931-wholeproteome.sdrf.tsv` | 18 | label-free DIA: 6 Jurkat CC-885 100 nM or DMSO, 8 h (Q Exactive HF); 12 dCeMM2 or DMSO, 2 h/4 h (Orbitrap Fusion, BLOCKED) |

Resolved SILAC design (preprint Fig 1–3 and Methods):
- KBM-7: dCeMM2 2.5 µM for 0, 0.5, 1, 2, 4, 8 and 12 h; dCeMM4 3.5 µM for 12 h.
- Jurkat: CC-885 100 nM for 8 h, in both the degradome and the translatome
  (nascent proteome).
- 3 biological replicates per experiment.

## To unblock

- Have the submitters (or the Cell Chem Biol STAR Methods) confirm which of
  JAC45A/GTD12 is compound 1, plus the cell line and dose of both arms.
- Get the sample preparation (cell line, label, digestion) for the 2024 LMW55
  dCeMM2 whole-proteome runs.

## Annotation choice to confirm

The SILAC-intermediate state (Lys4/Arg6) is present in the raw files. It marks
protein synthesized before or after the pulse in both combined cultures; it is not
a sample. Only the light and heavy pulse channels are annotated, matching the
heavy/light ratios used in the paper. Most deposited MaxQuant searches are 2-plex
(light | Arg10;Lys8). The t0/t30 files, however, are covered only by the deposited
3-plex `20211028_..._0_30_fractions_includeM` search: the xlsx lists a `0_30`
"newdatabase" search, but it is not in the PRIDE file list. A curator should decide
whether to add the Lys4/Arg6 modifications (UNIMOD:481, UNIMOD:188) or a
`SILAC medium` channel for those rows.

## Other open review points

- All whole-proteome runs are DIA: declare `dia-acquisition` and add window
  columns. Rows 1–6, per the preprint: 400–1200 m/z, 34 × 24.3 m/z windows.
- Consider `characteristics[exposure duration]` (TERMS.tsv) instead of
  `characteristics[time]`, and whether to declare `clinical-metadata` for the
  compound and dose columns.
- The CC-885 degradome (drug after the pulse) and translatome (drug during the
  pulse) rows differ only in source name and file. Consider a column that tells
  the two assays apart.

Independent review (three fresh-context rounds): **FAIL**. The only blockers are
the two BLOCKED items above; no review receipt was issued.
