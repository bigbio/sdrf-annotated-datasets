# PXD053974 annotation blocked

PXD053974, "CETSA with YLIU-06-026-1 on P. falciparum" (Pazicky / Bozdech, NTU), is the ITDR MS-CETSA dataset of Nardella et al., Cell Chem Biol 2025, 32:926-941 (doi:10.1016/j.chembiol.2025.06.003, PMID 40628257, PMC12406260). The paper's data availability statement cites PXD053974, although the PX record still says "publication pending". Compound 12 (YLIU-06-026-1) was tested in *P. falciparum* 3D7 trophozoite lysate and in intact trophozoites. Each arm had 10 samples per temperature: 9 drug concentrations (lysate 4-step series from 100 uM, intact cells 4-fold from 10 uM) plus DMSO. Peptides were TMT-labelled, with the plex not named, and fractionated by high-pH RP into 20 concatenated fractions. Runs were on a Q Exactive HF (DDA top 12) and searched in PD 2.5 with Mascot 2.6.1.

## Verified deposit (ProteomeCentral PROXI, read 2026-11-27, accession checked)
- The deposit has 16 files: 8 raw `.zip` archives and 8 Proteome Discoverer `.msf` files. The instrument is Q Exactive HF (MS:1002523) and the species is *P. falciparum* 3D7 (NCBITaxon 36329). The campaign cache (8 RAW / 16 files, Q Exactive HF) matches at archive level.
- Raw archives: `Lysate_YLIU_{37,50,55,60}.zip` and `SP4_incell_YLIU_{37,53,59,65}.zip`. That is one archive per arm x temperature, so one TMT set each.
- MSF files: `2022113x/1203_SP_lysate_YLIU_ITDR_{60,55,50,37}_F.msf` and `2023122x/202401xx_incell_YLIU_ITDR_{37,53,59,65}_F.msf`.
- **Conflict:** the lysate file names give 37/50/55/60 C, but the paper gives 37/53/59/65 C for both arms. This is unresolved.

## Why no SDRF
1. **The TMT channel -> concentration map is not stated anywhere I could read:**
   - Paper STAR Methods: no plex and no channel table.
   - PMC supplementary xlsx: blocked by reCAPTCHA. Europe PMC supplementaryFiles: server error.
   - Zenodo 15636573: the authors' ITDRMS v0.1 R package only, with no sample sheet.

   The package implies a layout only as a code default. `tubes = 10` "assuming TMT10 labeling". `ITDRMS.load` takes PD "Abundances (Grouped)" columns by position, with control tube last and concentrations decreasing. So channel 1 would be the top concentration and channel 10 DMSO. That is a generic default, not a dataset statement, and the code itself does not verify the column order. It would at best support a clearly flagged sandbox.
2. **The per-fraction RAW file names are unknown.** Each `.zip` should hold the ~20 fraction RAW files. The PRIDE FTP folder `https://ftp.pride.ebi.ac.uk/pride/data/archive/2025/06/PXD053974/` returned "upstream connect error ... connection timeout" 3 times (about 3 minutes apart), and PRIDE v3 `files/all` returned "remote connection failure". So I could not list the zip contents or read the `.msf` StudyDefinition/channel names. Writing per-fraction `comment[data file]` values would mean fabricating them. Using the `.zip` as the data file would hide the fraction structure.

## Recoverable if unblocked
Search settings from the Methods: LysC + trypsin, up to 3 missed cleavages, 30 ppm / 0.06 Da, Carbamidomethyl C fixed, Oxidation M / Deamidated NQ / Acetyl N-term variable. Reduction was TCEP and alkylation chloroacetamide. MS1 was 350-1550 m/z. Expected size: 8 sets x 10 channels x about 20 fractions, which is about 1600 rows.

**Evidence checked:** the PROXI record; the PRIDE FTP folder and PRIDE v3 `files/all` (both unreachable); paper full text (PMC12406260 and the author-manuscript copy); Europe PMC; the Zenodo record, plus the GitHub vignette and `ITDRMS.load.R`. Notes are in `/home/claude/singapore2/scratch/PXD053974/`.

**To unblock:** two things are needed:
- The contents of the 8 zips from the PRIDE FTP listing or a zip central-directory read.
- A stated channel map, from one of these:
  - the `.msf` StudyDefinition or the PD channel names, if the samples are named;
  - the Table S2 / Supplementary_file_2/3 headers;
  - the authors.

The lysate temperature discrepancy also needs resolving.
