BLOCKED: partial channel map. 330 of 370 raw files (33 of 37 triple-SILAC experiments) have an evidenced
sample per channel and are annotated in `PXD002065.sdrf.tsv` (990 rows). The remaining 40 raw files cannot be
annotated from public evidence:

- **GR1-10, GR11-20, GR21-30** (GR-1..GR-30.raw, acquired 2014-11-24): replicate experiments named in
  Supplemental Table S2 "(replicate) EGFR-RYK", "(replicate) EPHA1-MST1R", "(replicate) EPHA4-NTRK3".
  The TK pair is known and light = siControl, but **which TK is medium and which is heavy is not evidenced**:
  - Table S4 per-TK values do not match these runs' deposited ratios (they match the original runs exactly).
  - The replicate block names are alphabetical. The medium-heavy naming convention, which holds in all 31
    exactly testable original blocks, would imply a label swap. Approximate similarity of the ratios
    suggests the opposite. Choosing either would mean inferring from the data, which is not public evidence.
- **GT31-40** (GT-31..GT-40.raw, acquisition names DCP-GS31..40): the MaxQuant archive's results file is
  "Analysis Results Sample 34". Sample 34 is not named in the paper, Tables S1-S5 or the PRIDE record,
  so its siRNA targets are unknown. It may be the EPHA2 replicate mentioned in Fig. 1E/F, but no source says so.

Rungs checked (channel-map.md ladder, plus SILAC addendum item 5):
1. Paper (PMC4563730) methods and Fig. 1: light = R0K0 = control siRNA, medium = R6K4, heavy = R10K8. They give
   no per-experiment TK-to-channel assignment.
2. Supplementary Tables S1-S5 (PMC OA S3 bucket): S3 gives the TK pair per experiment and S2 gives the pair
   plus the Sample number. S4 gives per-TK protein ratios, which match the deposited Ratio M/L or Ratio H/L
   exactly (constant quotient, CV about 1e-15) for 31 experiments (`evidence/orientation_match.tsv`). S5 lists
   the MS-Viewer result files and adds no channel information.
3. Deposited PRIDE files: all 37 MaxQuant txt archives (summary.txt, parameters.txt, proteinGroups.txt,
   Analysis Results xlsx). These give raw-file-to-experiment, labels per state and Sample numbers, but no TK
   names per channel. The raw headers (first 8 KB) give acquisition names, the instrument and no sample names.
4. Europe PMC supplementary endpoint returned errors (connection refused). The PMC copies of the same files
   were used. The paper cites no external repository other than PRIDE and MS-Viewer.
5. Cross-check: the orientation of the 33 annotated experiments was checked as described in
   `PXD002065.evidence.json`. For GA1-10, GA21-30 and the FER channel of GB51-60, the orientation rests on
   the naming convention only.

To unblock: ask the authors (Giamas lab, Imperial College) for the GR orientation and the identity of
Sample 34. Alternatively, accept the 330-file subset as the annotation.

Files: `PXD002065.sdrf.tsv` (subset draft), `PXD002065.evidence.json`, `validation.txt`, `PR_BODY.md`,
`channel_map.tsv`, `samples.tsv`, `technical.tsv`, `scripts/`, `evidence/`.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above as blocked have no public sample/channel map. Promote to `datasets/` only once they are resolved, or once a maintainer accepts the partial coverage.
- Working files mentioned above (evidence/, validation.txt, scripts, tables) are not part of this submission.
- Review status: no independent adversarial review has been run on this draft yet.
- Caveat: for 31 of the 33 annotated blocks, the medium/heavy orientation follows the naming convention of Supplemental Tables S2/S3 and was confirmed by an exact join of Table S4 ratios with the deposited MaxQuant ratios. Three orientations (GA1-10, GA21-30 and the FER channel of GB51-60) rest on the naming convention alone.
