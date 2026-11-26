PARTIAL: 52 of 59 deposited raw files are annotated. BLOCKED for the 7 SPATA2-knockdown TNF-RSC pulldown runs (`20130329_QE4_LC6_SAW_A549_SILAC_TNFalpha_SPATA_siRNA_FLAG_Ingel_1..7.raw`, MaxQuant experiment "SPATA2 siRNA"): no public source says which SILAC channel holds siControl, siSPATA2 or a possible third state.

# PXD003627: SPATA2 / TNF-alpha receptor signalling complex (A549, triple SILAC)

- Publication: Wagner SA et al., EMBO J 2016;35(17):1868-1884. PMID 27307491, PMC5007551, doi:10.15252/embj.201694300
- Draft SDRF: `PXD003627.sdrf.tsv`, 156 rows (52 raw files x 3 SILAC channels) x 48 columns. Templates ms-proteomics, human and cell-lines v1.1.0.
- Arms annotated: phosphoproteome (TiO2/SCX, 2 x 12 fractions), di-Gly ubiquitylome (SCX, 2 x 6), TNF-RSC FLAG-TNF-alpha pulldown (in-gel, 2 x 8 slices). In every arm light = control, medium = TNF-alpha 5 min, heavy = TNF-alpha 15 min.

## Evidence
- Phospho and di-Gly arms: the Fig 1A legend ("The 'medium' and 'heavy' labeled cells were stimulated with TNF-alpha for 5 and 15 min, respectively, and mock-treated 'light' labeled cells served as control") and Fig 2A.
- Raw file -> replicate: file names and the MaxQuant `Experiment` column of the deposited `evidence.txt` files.

## Caveat for reviewers
- TNF-RSC pulldown orientation: the text does not state the label per condition. The assignment comes from matching the paper's Table 1 ratios ("5 min/control", "15 min/control") to the deposited `Ratio M/L` and `Ratio H/L` columns (all five Table 1 proteins match exactly). This repository's annotation rules count a map built that way as data-derived, which is a further reason this accession is in `sandbox/`.

## Rungs checked for the 7 blocked files
Main text (Fig 5A/B), PRIDE record, deposited MaxQuant output. Dataset EV1-EV3 and the Appendix could not be retrieved. Assigning channels from the ratios would be data-derived.

## Sandbox notes
- Kept in `sandbox/` until the blocked files and the pulldown orientation are resolved, or a maintainer accepts the partial coverage.
- Review status: no independent adversarial review has been run on this draft yet.
