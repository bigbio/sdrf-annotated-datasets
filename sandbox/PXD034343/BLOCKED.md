BLOCKED: no public TMT channel → sample map (treatment, time point, replicate) for either TMTpro-16 plex.

Dataset: [PXD034343](https://www.ebi.ac.uk/pride/archive/projects/PXD034343). It is a TMT-pulsed SILAC
(TMT-pSILAC) study in MCF7 cells: eIF4A1 inhibition with 150 nM hippuristanol vs DMSO, sampled at
0, 2, 4 and 8 h after the switch to heavy medium.
Publication: Schmidt T et al., *Nucleic Acids Res* 2023;51(4):1859-1879, doi:10.1093/nar/gkad030,
PMID 36727461, [PMC9976904](https://europepmc.org/article/PMC/PMC9976904).

## What the public record establishes

- Cells: MCF7 (Cellosaurus CVCL_0031; EFO:0001203), *Homo sapiens*, from PRIDE `sampleProcessingProtocol`
  and the paper's Methods ("TMT-pulsed SILAC").
- Design (PRIDE protocol and paper Methods): light-adapted cells (Lys0/Arg0) are switched to heavy medium
  (Lys8 = Lys-13C6-15N2, Arg10 = Arg-13C6-15N4) with either 150 nM hippuristanol or DMSO. Samples were taken
  at 0, 2, 4 and 8 h. "For all time points a biological quadruplet was generated."
- Labels: TMTpro 16plex (kit A44522). SILAC heavy is a pulse inside every sample, not a separate
  sample channel. MaxQuant 1.6.14.0 searched with TMT16plex at the MS2 level, with SILAC Arg10 and Lys8 as
  **variable modifications** (PRIDE `dataProcessingProtocol`). The deposited `parameters.txt` holds only
  MaxQuant global settings; it confirms version 1.6.14.0 and MS/MS tolerance 20 ppm, and implies the Arg10 /
  Lys8 search through its `SILAC Arg10Sites.txt;SILAC Lys8Sites.txt` site tables.
- Two plexes, each high-pH reversed-phase fractionated into 21 fractions. There are 46 deposited RAW files:
  - `..._TMT16_pH10_Group1_*`: 25 RAW files. `20210611_*` f001–f016 (fraction 13 is deposited as
    `f013_b`) plus `20210708_*` f013–f021, so fractions 13–16 were acquired twice.
  - `..._TMT16_pH10_Group2_*`: 21 RAW files, `20210708_*` f001–f021.
- Deposited `Light_IDs_out.txt` / `Heavy_IDs_out.txt` hold 32 reporter columns, `G1_..._1..16` and
  `G2_..._1..16`. All 32 carry non-zero summed intensity, which fits 4 time points × 2 treatments × 4
  replicates = 32 samples. That count is consistent but **not** a map. Their `Experiment` /
  `Experiment_` columns read `Group1` / `Group2`, which confirms G1/G2 = the Group1/Group2 plexes. Their
  `Raw file` column names `20210611` f001–f012 and `20210708` f013–f021 of Group1 only. No Group2
  raw-file provenance is deposited.
- Technical metadata confirmed from the record: Orbitrap Fusion Lumos (MS:1002732), DDA, HCD, Lys-C +
  trypsin, Carbamidomethyl C fixed (UNIMOD:4), Oxidation M (UNIMOD:35) and Acetyl protein N-term (UNIMOD:1)
  variable, Label:13C(6)15N(2) K (UNIMOD:259) and Label:13C(6)15N(4) R (UNIMOD:267) variable, TMTpro
  (UNIMOD:2016), precursor tolerance 4.5 ppm (main search), MS/MS tolerance 20 ppm. All UNIMOD accessions
  were checked against OLS.

## Why it is blocked

No public source says which TMT channel of which plex (Group1/Group2) holds which treatment × time point
× replicate. The SDRF needs one row per (raw file, TMT channel) with that identity, and it cannot be
written without inventing it. Sources checked (channel-map ladder):

1. Paper full text (PMC9976904 via NCBI efetch; Europe PMC full-text returned HTTP 500): Methods and
   Fig. 2A give the design but no channel layout.
2. Supplementary (`gkad030_supplemental_files.zip`): `supplementary_information_compiled.pdf` (Suppl.
   Fig. S2A shows replicate correlations labelled `DMSO_1..4`, `hipp_1..4` only),
   `Supplementary_Table_2_pSILAC_results.csv` (per-gene slopes only), `Supplementary_Table_3_*.csv`
   (sequences). None has a channel layout.
3. Deposited PRIDE files: `parameters.txt` (MaxQuant global parameters, no experimental design),
   `Light_IDs_out.txt` / `Heavy_IDs_out.txt` (reporter channels numbered 1–16 per group, with no sample
   names), `Rscript.R` (aggregation only).
4. Europe PMC `supplementaryFiles`: the same zip as in 2.
5. External repositories in Data Availability: Zenodo 10.5281/zenodo.7515807. This is a snapshot of the
   GitHub repository `Joseph-Waldron/Structure-seq2-with-hippuristanol-treatment-in-MCF7-cells`, also
   cited as Bushell-lab. It holds RNA Structure-seq2 code and data only, with no proteomics layout.
6. Not checkable or empty: the OUP article page returns HTTP 403 to automated access, and
   `bigbio/proteomics-sample-metadata` has no PXD034343 annotation.

Secondary open point: no source says how the time-0 samples are distributed over treatments. The
per-channel heavy/(heavy+light) fraction from the deposited tables is near 1% only in channels 1 and 8
of each plex, and the per-channel pattern is nearly identical in G1 and G2. This is inference only. It
cannot assign treatment or replicate and does not lift the block.

## Unblock

An author-provided table, or the MaxQuant `mqpar.xml` / experimental design plus a channel sheet, that maps
Group1/Group2 × TMTpro channel (126–134N) to treatment (hippuristanol / DMSO), time point (0/2/4/8 h) and
biological replicate. The point to settle as well is which acquisition of Group1 fractions 13–16 was used
(`20210611` vs `20210708`); the deposited tables point to `20210708`.

No SDRF is provided here, because every row would need an invented channel identity.
