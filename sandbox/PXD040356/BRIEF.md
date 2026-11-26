# PXD040356 — S. pneumoniae D39 wild type vs Δ3UTR vs Δ3UTR CEP:3UTR, TMT10plex, 20 fractions

Source: [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD040356); Pettersen et al., NAR 2026, doi:10.1093/nar/gkag481 (PMC13173289).

## Why this is in sandbox/
The assignment of the PD study-definition **Conditions A/B/C to strains is partly inferred**. The deposited .msf gives Replicate 1-3 and Condition A/B/C per channel (126-130C; A = rep1 126, B = rep1 127N, C = rep1 127C, and so on) and flags channel 126 (A) as Control, which supports A = wild type. It carries no strain names; B = Δ3UTR and C = Δ3UTR CEP:3UTR follows only the order in which the paper's Methods list the strains. No source checked (.msf, PRIDE, paper, supplementary docx and Tables S1/S2) resolves B vs C. A swap would invert `characteristics[genotype]` / `factor value[genotype]` on 6 of the 9 samples (120 of 180 rows). Author confirmation (corresponding author at SDU) would settle it.

Two independent review rounds: round 1 fixed (HCD term, Orbitrap analyzer); round 2 failed conditionally only because the B/C caveat was not carried with the artifact. Everything else was verified against the .msf (9 channels, fractions 1-20, 20 RAW files, modifications).

## Other notes
Lys-C predigest is not representable in the single-valued cleavage agent column (Trypsin recorded). Modification list follows the PRIDE protocol (TMT variable per the paper), Mascot node parameters not read.

Move to `datasets/` once the B/C strain assignment is confirmed.
