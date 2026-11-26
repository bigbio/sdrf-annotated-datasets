# PXD034081: draft (BLOCKED)

**BLOCKED: the TMTpro-18 channel → sample/treatment map is not public.** This draft SDRF
has all run-level metadata, but every channel's sample identity, cell type, disease and
treatment is `not available`. Do not promote it to `datasets/` until the map is known.

- **Dataset:** [PXD034081](https://www.ebi.ac.uk/pride/archive/projects/PXD034081): translatome
  proteomics (mePROD) of primary human FLT3-ITD+ AML cells treated with quizartinib,
  crenolanib or gilteritinib.
- **Publication:** Koschade SE *et al.*, Leukemia 2022, PMID 35999260,
  doi:10.1038/s41375-022-01678-y (PMC9522593). The dataset is in Supplementary Fig. 2.

## What is known (from public evidence)

- **Design** (Supp. Fig. 2A and its legend): one newly diagnosed, untreated FLT3-ITD+ AML patient
  sample (leukapheresis, Ficoll). Cells were treated for 6 h with 10 nM quizartinib, crenolanib,
  gilteritinib or DMSO in Lys8/Arg10 SILAC-heavy medium, n = 4 per condition (16 channels).
- **Extra channels** (Supp. Methods): one SILAC-heavy HeLa digest (booster channel) and one
  SILAC-light HeLa digest (noise/baseline channel). 16 + 2 = 18 channels, which matches TMTpro-18
  (PD quan method `TMTpro18_CM_Gamma`, channels 126–135N).
- **Runs:** one plex, high-pH RP fractionated (96 fractions concatenated to 24).
  `20220123_KKL_SK_T6_F1..F24.raw` on a Q Exactive HF, top-20 DDA, HCD with 35% NCE.
- **Search** (read from the deposited PD 2.4 `.msf`): two Sequest HT nodes, a light search
  (TMTpro on K) and a heavy search (TMTpro+K8 on K, Arg10 on R). Both used static TMTpro on the
  N-term and Carbamidomethyl on C. Variable mods: Oxidation (M), and Acetyl, Met-loss and
  Met-loss+Acetyl on the protein N-term. Tolerances 10 ppm / 0.02 Da, trypsin, 2 missed cleavages.

## What is missing: how to unblock

Each of the 18 TMTpro channels must be assigned to one of: DMSO, quizartinib, crenolanib or
gilteritinib (replicates 1–4), HeLa heavy booster, or HeLa light noise. These sources were
checked and none holds that assignment:

| Source | Result |
|---|---|
| Paper and Supplementary PDF (MOESM1) | design only, no per-channel layout |
| Supplementary tables (MOESM2/3 xlsx) | per-condition log2FC/q values for the cell lines only |
| Europe PMC `supplementaryFiles` | same files as above |
| PRIDE file list | 24 raw files and 1 `.msf`, no sample sheet |
| PD `.msf` StudyDefinition | generic `20220123_KKL_SK_T6_F - [126]`…`[135N]`, `<Factors />` empty |
| Data Availability | PRIDE accessions only, no external repository |

To unblock, get the channel layout from the authors (submitter S. Koschade, PI C. Münch,
Goethe University Frankfurt). Then fill `source name`, `characteristics[biological replicate]`,
the sample characteristics and `factor value[treatment]` per channel. Mark the booster and noise
channels as HeLa (`characteristics[cell line]`, `cell-lines` template). Consider adding
`comment[carrier channel]` for the booster.

## Label design note

This is mePROD, a pulsed SILAC label inside a TMTpro multiplex. It is not a light/heavy
SILAC-channel design. For that reason `comment[label]` holds the TMTpro channels, and the SILAC
pulse is written as variable `Label:13C(6)15N(2)+TMTpro` (UNIMOD:2123, the search's TMTpro+K8,
+312.221 Da) on K, next to variable TMTpro (UNIMOD:2016) on K, and `Label:13C(6)15N(4)` (UNIMOD:267) on R.
These merge the deposit's two Sequest searches (light and heavy), which set the labels as static.
