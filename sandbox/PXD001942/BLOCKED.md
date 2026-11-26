BLOCKED: SILAC channel -> construct map of the APP 48 h whole-proteome runs is not recoverable.

Affected runs (20 of 122 deposited RAW): `Tiffy_20120213_FPH_APP_48h_{III,IV}_slice1-5_{01,02}.raw`
(two experiments, Exp III and Exp IV, 5 slices x 2 injections each).

The other 102 runs (the qAP-MS interaction experiments for APP, PSEN1, HTT, PARK2 and ATXN1) are
annotated in `datasets/PXD001942/PXD001942-interaction.sdrf.tsv`.

Why blocked: Hosp et al. 2015 (Cell Rep, PMID 25959826, PMC9014711) and its Supplemental
Information state that the whole-proteome experiments compared HEK293T cells expressing APP, APPsw
or APPsw + LRPPRC, but no source says which construct was SILAC light or heavy in Exp III / Exp IV.
There is no label swap, and the deposited `proteome_changes_APPsw.zip` search output has an
`experimentalDesignTemplate.txt` that lists Exp3/Exp4 but names no channels. Ratios in that output (e.g. LRPPRC H/L 0.49 / 0.46,
APP 0.27 / 0.18) do not identify the constructs without assuming the design.

Unblock: an author statement, a deposited MaxQuant mqpar/experimentalDesign, or a sample sheet that
names the construct per channel for Exp III and Exp IV. Do not infer the map from the ratios.

Note for whoever unblocks these runs: the supplement names both an LTQ-Orbitrap Velos and a Q Exactive
for the whole-proteome runs, while the raw-file headers say LTQ Orbitrap Velos.

No SDRF is provided here for these runs.
