# PXD019716: draft (BLOCKED)

**BLOCKED: no public source says which SILAC channel holds which differentiation state in each raw file.**
This draft SDRF has all run-level metadata, but `characteristics[cell type]` and
`factor value[cell type]` are `not available` on every row. Do not promote it to `datasets/`
until the map is known.

- **Dataset:** [PXD019716](https://www.ebi.ac.uk/pride/archive/projects/PXD019716): SILAC
  (Arg10/Lys8) proteome of 3T3-L1 preadipocytes compared with day-10 adipocytes.
- **Publication:** Choi S, Goswami N, Schmidt F. *J Proteome Res* 2020, PMID 32991178,
  doi:10.1021/acs.jproteome.0c00475. The full text is paywalled, so only the abstract was used.
  The ACS supporting information on figshare was also used:
  [SI PDF](https://acs.figshare.com/articles/journal_contribution/13070318) and
  [SI xlsx](https://acs.figshare.com/articles/dataset/13070321).
- **Disease relevance:** adipogenesis model for obesity and type 2 diabetes. The cells
  themselves are written as `normal`, because 3T3-L1 is a non-disease line.

## What is known (from public evidence)

- **Design.** This is SILAC duplex with a label swap. The PRIDE protocol says "SILAC culture
  (R-10, K-8)". SI Fig. 2 shows both heavy-labelled preadipocytes and heavy-labelled adipocytes.
- **Runs.** There are 48 Thermo RAW files in 4 groups of 12: `1_H_L`, `1_L_H`, `2_HL` and `2_LH`.
  - Each group has 4 ACN step fractions (ACN10, ACN15, ACN20, ACN40) × suffixes `_1`/`_2`/`_3`.
  - The raw headers name a fraction-specific LC method (`…_ACN10_…`, `ACN15`, `ACN20`). The
    ACN40 files were run with the `…_ACN30_…` method; their fraction number (4) comes from the
    file name.
  - Set 1 (`1_*`) was acquired on a **Q Exactive HF-X**, set 2 (`2_*`) on a **Q Exactive HF**.
    This comes from the raw-file headers. PRIDE lists only Q Exactive HF.
- **Search.** The deposited search output is `proteinGroups.txt` (MaxQuant). It has 6
  experiments × 8 fractions.
  - In experiments 1-3, heavy = adipocyte: FABP4 Ratio H/L normalized is about 50.
  - In experiments 4-6, heavy = preadipocyte: the ratio is about 0.005.
  - The SI xlsx sheet "Proteins" agrees. It relabels Intensity L 1-3 and H 4-6 as
    `Before_diff_1-6`, and Intensity H 1-3 and L 4-6 as `After_diff_1-6`.
- **Settings.** The digest is trypsin. Modifications are Carbamidomethyl (C, fixed),
  Oxidation (M, variable), Label:13C(6)15N(4) (R, UNIMOD:267) and Label:13C(6)15N(2)
  (K, UNIMOD:259). Acquisition is HCD DDA.

## What is missing: how to unblock

The 48 raw files cannot be assigned to MaxQuant experiments 1-6. No `mqpar.xml`,
`summary.txt` or `experimentalDesign.txt` was deposited. The tokens `H_L`/`L_H`/`HL`/`LH` in
the file names are not defined in any public source, so they could mean "heavy = preadipocyte"
or "heavy = adipocyte". These sources were checked:

| Source | Result |
|---|---|
| PRIDE project record and protocols | SILAC R10/K8 and fractionation, but no channel assignment |
| PRIDE file list | 48 RAW files + `proteinGroups.txt` only |
| `proteinGroups.txt` | orientation per MaxQuant experiment, but no file → experiment map |
| Paper full text | paywalled; Europe PMC, Unpaywall and Semantic Scholar have no OA copy |
| ACS SI PDF and xlsx (figshare) | label swap confirmed; no per-file layout |
| RAW headers | instrument, original file names, LC methods; no sample names |

To unblock, do one of the following:

1. Read the paper's Experimental Procedures, which may define the `H_L`/`L_H` naming.
2. Ask the submitter (Sunkyu Choi, Weill Cornell Medicine-Qatar) for the `mqpar.xml`.
3. Convert one file per group (e.g. `*_ACN10_1.raw`) and compare light vs heavy intensities
   of FABP4/ADIPOQ peptides. The adipocyte channel is about 50× higher.

Then set `characteristics[cell type]` and `factor value[cell type]` per channel: `preadipocyte`
(CL:0002334) or `adipocyte` (CL:0000136). After that, validate and promote.

## Sample structure is also unresolved

MaxQuant combined the 48 files into **6 experiments × 8 fractions** (`proteinGroups.txt`
columns `Fraction 1`..`Fraction 8`). Fractions 1-4 and 5-8 show the same peptide-count pattern
across the ACN steps. So each experiment most likely joined the 4 ACN fractions of one set-1
(HF-X) group with the 4 fractions of one set-2 (HF) group.

If that is right, the deposit holds **12 distinct samples** (2 orientations × 3 replicates ×
2 channels), not the 24 sources written here. Which groups were paired is not public.

The 24 source names, one per (file group, suffix `_1`/`_2`/`_3`, channel), and the replicate
numbers are therefore **placeholders**. They do not claim that set 1 and set 2 are independent
samples. Merge or renumber them when the file → experiment map is known. The deposit also does
not say whether `_1`/`_2`/`_3` are biological or technical replicates.

## Other open points
- **Tolerances.** Precursor and fragment tolerances are not recorded anywhere public, so they
  are written as `not available`. Because of that, `parse_sdrf convert-openms` stops on this file.
- **Fractionation method.** The ACN step elution is probably high-pH reversed phase, but no
  source names it, so `comment[fractionation method]` is left out.
- **Protein N-terminal acetylation** (a MaxQuant default) is not in the data-processing
  protocol and was not added.
