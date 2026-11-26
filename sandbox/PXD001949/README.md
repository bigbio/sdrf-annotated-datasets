BLOCKED: 8 of 48 raw files (MB-A1.raw .. MB-A8.raw) cannot be mapped to SILAC channel samples from public evidence.

PXD001949.sdrf.tsv in this folder is a DRAFT. It covers the 40 raw files whose channel map is evidenced: MCM2a, MCM2b and the E15min/E60min/E240min time course, 104 rows. It leaves out the MB-A series.

What is known about MB-A1..8:
- The deposited MaxQuant output (MCM2.zip, combined/txt/evidence.txt) assigns them to experiment "MCM2c".
- The raw headers say Orbitrap Velos Pro. The other series ran on LTQ Orbitrap XL or LTQ Orbitrap Velos.
- The deposited search uses multiplicity 3 (L / Arg6Lys4 / Arg10Lys8) for every file, so it gives no channel contents.

Rungs checked for the MCM2c channel map:
1. Paper (PMC4587322, full text): it reports only "two independent experiments" for GFP-MCM2 (Fig. 3) plus the 3 time points (Fig. 4). MCM2c is not mentioned.
2. Supplementary (Europe PMC supplementaryFiles zip, evidence/supp/): Suppl Table 2 has MCM2a, MCM2b, MCM5_a and MCM5_b only. Suppl Tables 3 and 4 cover E15min/E1h/E4h. Nothing covers MCM2c.
3. Deposited PRIDE files: MCM2.zip (truncated archive, read by range requests). The experimentalDesignTemplate.txt lists only the 40 mapped files. summary.txt and evidence.txt name the experiment MCM2c but give no condition per channel.
4. No external repository is cited in the paper's data statement.

What would unblock it: the authors confirming what MCM2c is and the sample in each SILAC channel. It may be a third GFP-MCM2 L/M experiment, or an unreported GFP-MCM5 or other experiment. Once that is known, add rows for MB-A1..8 to samples.tsv (instrument NT=Orbitrap Velos Pro;AC=MS:1003096) and rebuild.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above as blocked have no public sample/channel map. Promote to `datasets/` only once they are resolved, or once a maintainer accepts the partial coverage.
- Working files mentioned above (evidence/, validation.txt, scripts, tables) are not part of this submission.
- Review status: no independent adversarial review has been run on this draft yet.
