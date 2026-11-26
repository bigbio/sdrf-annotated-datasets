# PXD004879

BLOCKED: the SILAC channel -> cell line map is not recoverable from the public record
available to the annotator. No SDRF is provided. Do not write one until the map is known.

- PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD004879
- Publication: Mathieu AA, Ohl-Séguy E, Dubois ML, Jean D, Jones C, Boudreau F, Boisvert FM.
  *Subcellular proteomics analysis of different stages of colorectal cancer cell lines.*
  Proteomics 2016;16(23):3009-3018. PMID 27689624, doi:10.1002/pmic.201600314
  (no open full text in Europe PMC; Unpaywall reports no OA copy).
- Organism: Homo sapiens. Disease: colorectal cancer (seven CRC cell lines) plus normal colon
  fibroblasts and normal intestinal epithelial cells (abstract).

## What the deposit settles

Deposit: 136 Thermo `.raw` files and one MaxQuant output, `combined.zip` (25 GB). Its
`combined/mqpar_final.xml` and `combined/txt/parameters.txt` give:

- Triplex SILAC (`multiplicity` 3): light / `Arg6;Lys4` (medium) / `Arg10;Lys8` (heavy).
- Trypsin/P with 2 missed cleavages. Fixed: Carbamidomethyl (C). Variable: Acetyl (Protein N-term), Oxidation (M).
- Main search tolerance 4.5 ppm, first search 20 ppm, FTMS MS/MS tolerance 20 ppm. MaxQuant 1.4.1.2.
  The PRIDE data protocol says 1.5.2.8 and 7 ppm.
- Instrument: Q Exactive (`summary.txt`, PRIDE). DDA top-10 (PRIDE sample protocol).
- 36 MaxQuant experiments: 9 cell-line codes x subcellular fractions `_F1`-`_F4`. The codes are
  `HIEC`, `1459`, `CACO`, `HT`, `DLD`, `HCT`, `227`, `228`, `233`. The fraction names behind
  F1-F4 are not stated in any source available here.
- 224 file entries over the 136 deposited raw files. Many raw files were loaded several times
  under `" - Copy"` names, each time with a different experiment. So one raw file carries 2 or 3
  cell lines, one per SILAC channel. From the experiment assignments:

| raw files (deposited) | n | experiments assigned (cell-line codes) |
|---|---|---|
| `76AAM_HIEC_HCT_{A,B,C,D}{1-8}` | 32 | HIEC (only one experiment, although the file name also says HCT) |
| `17Emma{1-4}_{1-8}` | 32 | DLD, CACO |
| `20Emma{5-8}_{1-8}` | 32 | HT |
| `80AAM_HCT_DLD_F{1-4}` | 4 | HT, DLD, HCT |
| `87AAM_B_F{1-4}` | 4 | 228, 227, HCT |
| `87AAM_H_F{1-4}` | 4 | HIEC, CACO |
| `87AAM_J_F{1-4}` | 4 | HIEC, 228 |
| `87AAM_M_F{1-4}` | 4 | HT, 227 |
| `103AAM_C{1-4}` | 4 | 233, 1459, HCT |
| `103AAM_F{1-4}` | 4 | 233, 227 |
| `103AAM_G{1-4}` | 4 | 228, 1459 |
| `103AAM_K{1-4}` | 4 | 233, DLD |
| `103AAM_L{1-4}` | 4 | CACO, 1459, HCT |

The trailing digit (`A1`-`D8`, `_1`-`_8`) of the 8-file sets looks like eight LC-MS fractions
(gel slices; PRIDE lists "Gel-based experiment") of one subcellular fraction. The letter or Emma
number (A-D, 1-4, 5-8) maps to `_F1`-`_F4`. The 4-file sets are one run per subcellular fraction.
The mqpar `fractions` values (1-10) are run counters inside an experiment, not real fraction numbers.

## Why blocked

1. **Channel identity.** The MaxQuant output reports ratios M/L, H/L and H/M per experiment.
   No deposited file says which cell line was grown in light, medium or heavy medium in any raw
   file. The experiment names say which lines share a file, but not which channel each line is in.
   For the files with only one or two experiments (for example `76AAM_HIEC_HCT_*`,
   `20Emma*`), the remaining channels are not identified at all. They could be a reference,
   another line, or empty.
2. **Cell-line codes.** `227`, `228`, `233` and `1459` look like ATCC catalogue numbers:
   CCL-227 SW620, CCL-228 SW480, CCL-233 SW1116, and CRL-1459 CCD-18Co (normal colon
   fibroblast). That would match "seven CRC lines + fibroblasts + epithelial cells" (CACO, HT,
   DLD, HCT, SW620, SW480, SW1116 + CCD-18Co + HIEC). No source available here confirms it.
   This is a hypothesis, not evidence.
3. **Subcellular fractions.** The names of compartments F1-F4 are not in PRIDE or in the abstract.
4. The full paper (Wiley, not open access) was not readable in this pass. Its Methods, figures or
   supplementary material probably hold the labelling and mixing scheme.

## Unblock

Read the Materials and Methods and the supplementary information of PMID 27689624, or the
companion protocol (Methods Mol Biol 2018, PMID 29589306), or get an author statement. You need:

- the SILAC label of each cell line in each raw-file group above, and what fills any channel
  not named by an experiment;
- the names of subcellular fractions F1-F4;
- confirmation of the cell-line identities behind `227`, `228`, `233`, `1459`, `CACO`, `HT`,
  `DLD`, `HCT` and `HIEC`.

Then annotate one row per raw file per SILAC channel (136 files x 3 channels = 408 rows if every
channel is used). Use templates `ms-proteomics`, `human`, `cell-lines` and probably
`oncology-metadata`. Add `comment[fraction identifier]` from the slice index and a
subcellular-fraction characteristic. Do not infer the channel map from ratios or from file names.
