BLOCKED: in `PXD007995-scaffold-silac.sdrf.tsv`, the `comment[fraction identifier]` does not mean the same extraction in every scaffold.

This is a DRAFT of the SILAC scaffold experiment (lung fibroblasts cultured in decellularized human lung scaffolds, days 6/9/12/25, 3 scaffolds per day, 3 raw files per scaffold; 72 rows). The project's label-free monolayer SDRF is submitted separately to `datasets/PXD007995/`.

## What is settled
- **Sampling day per raw file:** comes from an exact-equality join, accepted by the maintainer. The summed deposited MaxQuant per-experiment intensities equal the per-day values in the paper's Supplementary Table S3, to the 5 significant figures printed, and no alternative grouping scores above 2 exact matches.
- **Light/heavy orientation:** light = old scaffold protein, heavy = new fibroblast-made protein (heavy lysine). It is stated in the paper's Methods.

## Why it is blocked
Each scaffold was extracted into three fractions, one raw file each (soluble, SDS-released, ECM-enriched). Nothing public says which raw file holds which fraction, and the draft numbers them 1-3 by file-name order.

An independent reviewer profiled each raw file in the deposited `evidence.txt`:
- **The three classes:** every scaffold has exactly one file of each class. Class A has about 1% collagen intensity. Class B has 15-35%. Class C has 56-76% collagen, almost no heavy signal, and is clearly the ECM-enriched fraction.
- **Inconsistent numbering:** file-name order gives A/B/C = 1/2/3 in most scaffolds, but A/C/B in experiments 1, 4 and 6 and C/B/A in experiment 12, which is 16 of 72 rows.

## What would unblock it
A public statement of which file is which fraction. Alternatively, the maintainers can accept numbering by the profile above (ECM-enriched = 3). Even then, which of A and B is the soluble fraction and which is SDS-released stays open.

## Sandbox notes
- This is a blocked draft. Promote it to `datasets/` only once the fraction identity is resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Review status: an independent fresh-context adversarial review FAILED this draft on the fraction numbering only.
