PARTIAL: `PXD016334-chpk-apms.sdrf.tsv` covers 19 of the 25 HEK293T herpesvirus-kinase AP-MS raw files. The two NIH 3T3 M97 SDRFs of this project are submitted separately to `datasets/PXD016334/`.

Unmapped files (6 HHV6-U69 / HHV7-U69 runs):
- Statler_20161214_BB_HS_U69_IP1.raw
- Statler_20161214_BB_HS_U69_IP2.raw
- Statler_20170306_BB_HS_betaKinasesU69_3.raw
- Animal_20180222_BB_HS_U69HHV7_1.raw
- Animal_20180222_BB_HS_U69HHV7_2.raw
- Animal_20180222_BB_HS_U69HHV7_3.raw

## What is known about the six U69 runs
- **Public sources:** the file names carry no H/L code. ExperimentalDesign.txt says only "double SILAC U69_HHV7 versus vector control" (the same for HHV6). The mqpar experiment names (U69_HHV6_n, U69_HHV7_n) carry no channel, and the paper says only "including label-swaps".
- **Supplementary Data 1:** it does not join exactly to the deposited proteinGroups.txt (residual SD 0.06-0.17 log2), so it seems to come from a different MaxQuant run.
- **Reviewer's bait check:** in the deposited `txt_HHVKinases` proteinGroups.txt, the HA-U69 bait protein sits mostly in one channel per run:

  | run | bait H/L | bait channel |
  |---|---|---|
  | U69_IP1 | 220.8 | heavy |
  | U69_IP2 | 0.018 | light |
  | betaKinasesU69_3 | 138.1 | heavy |
  | U69HHV7_1 | 18.6 | heavy |
  | U69HHV7_2 | 12.9 | heavy |
  | U69HHV7_3 | 0.030 | light |

  The same bait check reproduces the channel of all 15 annotated files that carry H/L codes in their names. Two caveats: the HHV7 bait protein group also contains an HA-U69 LF/AA mutant sequence, and Supp. Fig. 5 describes further HHV6-U69 WT vs R37A/L39A runs.
- This data-derived assignment is documented here but not applied.

## What would unblock it
An author statement, or a deposited table, that gives the heavy/light assignment and the construct (WT or mutant) of each U69 run.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above have no public channel map. Promote it to `datasets/` only once they are resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Review status: an independent fresh-context adversarial review found no issues in the 19 annotated files. It failed the file only on the six excluded U69 runs.
