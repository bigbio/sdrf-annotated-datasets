# PXD014215 — BLOCKED draft

**BLOCKED:** public evidence does not say which SILAC channel is the suramin-treated culture
in each run. Without that, the treatment factor cannot be annotated. The draft SDRF holds
everything that *is* evidenced. Channel-level `characteristics[treatment]` and
`factor value[treatment]` are `not available` on all 96 rows.

- Dataset: https://www.ebi.ac.uk/pride/archive/projects/PXD014215 ("Trypanosoma brucei global proteome changes upon suramin exposure")
- Publication: Zoltner M. et al., J Biol Chem 2020; 295(24):8331-8347, PMID 32354742, PMC7294092, doi:10.1074/jbc.RA120.012355
- Design (paper, *SILAC labeling*): bloodstream-form *T. b. brucei* grown in HMI-11 with R0K0 (light) or R6K4
  (Arg U-13C6, Lys 4,4,5,5-2H4; heavy). The cells were treated with 35 nM suramin or left untreated
  ("respectively"), mixed after 24 h or 48 h, and run on SDS-PAGE in 8 slices. The paper says
  "Samples were generated in triplicate, and one label swap was performed."

## What is resolved (and how)

| Run stem (×8 slices) | Instrument (raw header) | Timepoint | Evidence |
|---|---|---|---|
| `24-sur` | Orbitrap Velos Pro, CID/ITMS | 24 h, MaxQuant Exp. 1 | `24h_output.txt.zip` summary.txt |
| `MZ-SA` | Orbitrap Velos Pro, CID/ITMS | 24 h, MaxQuant Exp. 2 | `24h_output.txt.zip` summary.txt |
| `MZ-SB` | Orbitrap Velos Pro, CID/ITMS | 24 h, MaxQuant Exp. 3 | `24h_output.txt.zip` summary.txt |
| `mz-48sur` | Q Exactive HF, HCD/FTMS | 48 h | file name `MZ-48Sur`, QE HF (paper: only the 24 h set was on the Velos Pro) |
| `mz-sc` | Orbitrap Velos Pro, CID/ITMS | unknown | in neither deposited search |
| `mz-sd` | Orbitrap Velos Pro, CID/ITMS | unknown | in neither deposited search |

Search parameters come from the deposited MaxQuant `parameters.txt` and `summary.txt`
(MaxQuant 1.6.1.0): Trypsin/P with 2 missed cleavages, Carbamidomethyl (C) fixed, and
Oxidation (M) and Acetyl (Protein N-term) variable. Labels are Arg6;Lys4, written as
UNIMOD:188 and UNIMOD:481. The MS/MS tolerance is 20 ppm for FTMS and 0.5 Da for ITMS.

## What blocks promotion to `datasets/`

1. **Which 24 h replicate is label-swapped is not stated.** The normalized H/L ratios of the three
   24 h experiments are essentially uncorrelated (r = 0.05 to 0.17). This fits the paper's statement that
   the proteome is unchanged at 24 h, so the data cannot identify the swap either.
2. **Only one of the three 48 h runs is deposited.** The 48 h MaxQuant search used raw files named
   `sura`, `mz-surb` and `surc`, and none is in PRIDE under those names. Its ratios show that
   Experiment 3 (`surc`) is the swapped one (r = −0.55 and −0.67 against Experiments 1 and 2). The deposited
   `mz-48sur` run's header states "Method duration 94.00 min" (method file `100min-T20_60k-UDP-RedCO-ML.meth`). That matches the ~95-min retention range of `sura`/`surc` in `msmsscans.txt`, so it can be either `sura` (unswapped) or `surc`
   (swapped). `mz-surb` has a 140-min gradient, which rules it out.
3. **`mz-sc` and `mz-sd`** (Velos Pro, acquired 19 Jun 2015, the same day as `MZ-SA`/`MZ-SB`) are
   not described anywhere. Their timepoint, treatment and replicate identity are unknown.
   SILAC labelling is assumed from the project-level protocol. Being on the Velos Pro weakly suggests
   the 24 h series, but the 24 h search holds exactly three replicates (`24-sur`, `MZ-SA`, `MZ-SB`), so
   no timepoint is asserted for them.
4. The precursor mass tolerance was not deposited (there is no `mqpar.xml`), so that column is omitted.
   `parse_sdrf convert-openms` fails on the 32 `mz-sc`/`mz-sd` rows because their fragment mass
   tolerance is `not available`.

**To unblock it:** the submitters (Zoltner/Field, Dundee) would need to give the label orientation of each
replicate, say what `mz-sc`/`mz-sd` are, and say which 48 h search file `mz-48sur` corresponds to (or
deposit the missing 48 h raw files).
