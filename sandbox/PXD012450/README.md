BLOCKED: the SILAC channel orientation of the two ZC3H40 conditional over-expression (cOE) experiments, AT-BSF and AT-PCF (16 raw files), rests only on the authors' published supplementary tables. No deposited search output or public text confirms it.

PXD012450-cOE.sdrf.tsv in this folder is a DRAFT covering those 16 raw files (32 rows). The other two experiments of this project (3940DKO and 40RNAi) are evidenced from the deposited MaxQuant output and the text, and are submitted separately in `datasets/PXD012450/`.

What the draft assumes:
- **Orientation:** light = tetracycline withdrawn (cOE off), heavy = induced, in both the BSF and the PCF experiment.
- **BSF basis:** Supplementary Sheet S8. ZC3H40 itself is absent from S8, so the call rests on ZC3H39 as a proxy (H/L 5.36) and on ATP-synthase subunits (median H/L about 1.18).
- **PCF basis:** Supplementary Sheet S10 (ZC3H40 H/L 6.03).

Sources checked for a direct statement:
1. **Paper, Methods:** names the light and heavy channels only for the knockout experiment.
2. **PRIDE sample processing protocol:** calls the "knockdown" lines light, which does not cover the over-expression lines.
3. **Figure 7:** its axes are labelled "Log2 Fold Change H/L" but plot -log2(H/L), so they cannot settle the orientation.
4. **Deposited cOEBSF.zip:** an unrelated single-run search (TREU927 database, written 2016-08-30, before the AT-BSF raws were acquired). It shares no protein IDs with Sheet S8.
5. **Deposited cOEPCF.zip:** does not match Sheet S10.

What would unblock it: the MaxQuant output that produced Sheets S8 and S10, or a statement from the authors of which channel was the induced line.

Other notes:
- The PCF uninduced duration is not stated, so its source name carries no duration.
- The precursor tolerance is `not available`, because no mqpar.xml was deposited.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the channel orientation of the files above has no public evidence other than the published tables. Merge these rows into `datasets/PXD012450/` only once the orientation is resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Working files (evidence/, validation output, scripts, tables) are not part of this submission.
