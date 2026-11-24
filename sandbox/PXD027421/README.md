BLOCKED: 12 of 82 raw files (the Figure 1 ChIP-SICAP label-swap runs) have no public per-file SILAC channel orientation. The other 70 files are annotated in two draft SDRFs. Review is pending.

# PXD027421: working notes

## What is annotated (draft, REVIEW_PENDING)
- `PXD027421.sdrf.tsv`: SILAC, 150 rows covering 50 raw files
  - gamma-H2AX time-course ChIP-SICAP (Fig. 3): 10 Orbitrap Fusion files x 3 channels. Light = IgG, medium = H2A, heavy = gamma-H2AX ChIP.
  - Fractionated chromatin input: 2 triple-SILAC experiments x 8 fractions on the Q Exactive HF. Exp 1: light UT / medium 0.5 h / heavy 1 h. Exp 2: light UT / medium 4 h / heavy 8 h.
  - iPOC: 3 experiments (1 h, 4 h and 8 h), each 2 replicates x 4 fractions, on the Q Exactive HF. Light = UT without EdU, medium = UT with EdU, heavy = IR with EdU.
- `PXD027421-nchrop.sdrf.tsv`: label-free N-ChroP histone PTMs, 20 rows covering 20 files. This part is split into its own file because `parse_sdrf convert-openms` refuses SILAC and label-free runs in one SDRF.

## Blocked files (not annotated)
- 20171022_GS_Rad50_ON_Fwd_1, Fwd_2, Rev_1, Rev_2
- 20171022_GS_Rpa_ON_Fwd_1, Fwd_2, Rev_1, Rev_2
- 20180731_FS1_GS_53BP1_ChIP-SICAP_Triple_ON_Fwd, Rev
- 20180731_FS1_GS_MDC1_ChIP-SICAP_Triple_ON_Fwd, Rev

The run names mark forward and reverse (label-swap) runs. The paper describes only one orientation: light = IgG control of a 1:1 UT:IR mix, medium = UT, heavy = 1 h IR.

## Evidence ladder checked for these files
1. Paper Methods, Fig. 1A, Table 1 (PMC9881138): one orientation only, and no swap is mentioned.
2. Supplementary (PMC OA package): the Suppl. Fig. S1 legend gives L/M/H = control/UT/IR. Suppl. Item 1 reports ratios already re-oriented (UT/Ctr, IR/Ctr) for RPA/RAD50/MDC1 `_ON_F1`/`_F2` only. It does not map the 4 RPA or RAD50 files to F1/F2, and it has no 53BP1 sheet.
3. Deposited PRIDE files, ChIP-SICAP.zip (read with HTTP range requests): mqpar.xml, experimentalDesignTemplate.txt, summary.txt and parameters.txt. These give the experiment name per run (for example Rpa_ON_Rev_1) and labelMods Arg6;Lys4 / Arg10;Lys8. They give no condition per channel.
4. Europe PMC supplementary endpoint (HTTP 500). The paper names no external repository apart from protocols.io (the protocol only).

What would unblock them: the authors confirming the channel layout of the Rev runs, or a deposited per-run condition table.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above as blocked have no public sample/channel map. Promote to `datasets/` only once they are resolved, or once a maintainer accepts the partial coverage.
- Working files mentioned above (evidence/, validation.txt, scripts, tables) are not part of this submission.
- Review status: no independent adversarial review has been run on this draft yet.
