BLOCKED: 14 runs of cohort P113 (TgCRND8 hippocampus) cannot be assigned to one mouse.

Affected runs (14 of 1186 deposited RAW): `MMD1780A147LC3_C7.raw` ... `MMD1780A160LC3_H8.raw`
(MMD1780A147LC3_C7, A148LC3_D7, A149LC3_E7, A150LC3_F7, A151LC3_G7, A152LC3_H7, A153LC3_A8,
A154LC3_B8, A155LC3_C8, A156LC3_D8, A157LC3_E8, A158LC3_F8, A159LC3_G8, A160LC3_H8).

The other 1172 runs (cohorts P113, P285 TgCRND8; P186, P548 App NL-F; P120 SOD1-G93A; brain or spinal
cord, and plasma) are annotated in `datasets/PXD010671/PXD010671-mapped.sdrf.tsv`.

Why blocked: the deposited P113 Lys6 MaxQuant searches (txt_K6_3, txt_K6_4) and the paper's
Supplemental Table S7 (PMID 34979241, PMC8816717) both assign these 14 runs, as fractions 3-16, to
two samples at once, 350-GDN-det and 352-tri-sol. Run order and plate wells suggest 350-GDN-det fractions 3-16, but no source states it,
so annotating them would fabricate a sample link.

Unblock: an author statement or a corrected search/design file that assigns each of the 14 runs to
exactly one mouse and detergent fraction.

No SDRF is provided here for these runs.
