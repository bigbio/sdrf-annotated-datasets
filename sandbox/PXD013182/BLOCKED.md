BLOCKED: TMT10 reporter (TMT126–TMT131) cannot be mapped to treatment.

The paper and SI (Gaetani et al., J Proteome Res 2019, DOI 10.1021/acs.jproteome.9b00500) give experiment identity and cell line, but not which reporter is DMSO vs drug, which of the nine drugs, or which 2D PISA channel is Sm / Sm′ / Sm″ / carrier proteome. Figure 1e/g is a cartoon only. SI Tables S3–S7 and S10 use DMSO1/MTX1-style analysis columns, not TMT channel IDs. PRIDE MaxQuant `parameters*.txt` files have no experimentalDesign table.

Do **not** promote this folder to `datasets/` until a channel map exists (author table, MaxQuant experimentalDesign.txt, or a figure that labels 126–131).

What *is* evidenced and encoded:

| PRIDE file prefix (24 fractions each) | Experiment (paper/SI) | Cell line |
|---|---|---|
| `pisaMTXcellsA549` | 1D PISA MTX, living cells (Table S3) | A549 / CVCL_0023 |
| `20180928_MTX_PISA_LYSATE` | 1D PISA MTX, lysate (Table S4) | A549 / CVCL_0023 |
| `pisa5FUcellsA498` | 1D PISA 5-FU, living cells (Table S5) | A498 / CVCL_1056 |
| `20181115mg_5FU_LYSATE_A498` | 1D PISA 5-FU, lysate (Table S6) | A498 / CVCL_1056 |
| `PISA_9drugs_set1/2/3` | 1D PISA 9-drug + DMSO, lysate (Table S7); sets = bio-reps 1–3 | A549 / CVCL_0023 |
| `20190121_PISA_MTX_C` | 2D PISA MTX dose series, lysate (Table S10) | A549 / CVCL_0023 |

Each RAW is one TMT10-plex × 24 concatenated high-pH fractions → 192 files × 10 channels = 1920 rows. `comment[label]` is the TMT channel name only.

1D assays used five biological replicates of treated and untreated samples in one TMT10 (paper). Those replicate numbers are **not** assigned per channel here. `characteristics[biological replicate]` is 1 except for the three 9-drug plexes.

Alkylation in the paper methods is 25 mM iodoacetamide (matches MaxQuant Carbamidomethyl / UNIMOD:4). The PRIDE sample-processing text saying iodoacetic acid is treated as a deposit typo.
