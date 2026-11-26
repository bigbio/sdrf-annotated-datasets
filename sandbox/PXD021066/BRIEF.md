# PXD021066 — sandbox draft

*P. aeruginosa* PAO1 envelope proteins, pMfs1 / pMfs2 overexpression vs empty vector. 8 RAW mapped from names; `PAO1_p_Rep3` has an msf but no RAW.
Publication: Dulyayangkul P et al., Front Microbiol 2020;11:592153, doi:10.3389/fmicb.2020.592153, PMC7835679.

Paper methods: envelope fraction, 11% SDS-PAGE, in-gel tryptic digestion; Ultimate 3000 + LTQ-Orbitrap Velos; Proteome Discoverer 1.2 / SEQUEST, PAO1 database; 3 biological replicates. `comment[cleavage agent details]` is now Trypsin.

**Open:** search mods, missed cleavages and tolerances not reported in the paper.

Validation: `parse_sdrf validate-sdrf --use_ols_cache_only` (with ontology checks) passes; warning only for free-text `cell envelope` organism part.
