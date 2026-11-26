# PXD014841: label-free draft (BLOCKED for the SILAC campaign)

**BLOCKED: not a SILAC dataset.** PXD014841 is label-free (MaxQuant LFQ, `multiplicity 1`,
`lfqMode 1` in the deposited `mqpar.xml`), so it is out of scope for the SILAC annotation
campaign that produced its sister dataset PXD014740 (Neuro2a pSILAC/BONCAT). The SDRF here is
complete and passes `parse_sdrf validate-sdrf` for `ms-proteomics` and `vertebrates`; a maintainer
can promote it to `datasets/` with `git mv` after checking the open points below.

- **Dataset:** [PXD014841](https://www.ebi.ac.uk/pride/archive/projects/PXD014841): mouse
  neocortex total lysate (input), 80S and polysome proteomes across five developmental stages.
- **Publication:** Kraushar ML *et al.*, Mol Cell 2021;81(2):304-322.e16, PMID 33357414,
  doi:10.1016/j.molcel.2020.11.037 (PMC8163098). Key Resources table: "Neocortex total lysate,
  80S, polysome mass spectrometry ... ProteomeXchange PXD014841".

## Design (45 rows = 45 raw files)

5 stages × 3 sample types (input, 80S, polysome) × 3 biological replicates, one label-free run
each. File → stage/type/replicate comes from the MaxQuant experiment names in the deposited
`mqpar.xml`/`summary.txt` (e.g. `Waldorf_20171109_KI_MM_E13_n1.raw` → `E13_input_rep1`).
Each biological replicate is a pool of 6-18 animals of both sexes (`sex = pooled`; PRIDE protocol
and paper), from timed-pregnant wild-type CD-1 mice. The factors are developmental time point and
sample fraction (input / 80S monosome / polysome), giving 15 conditions × 3 replicates. All 45 raw headers read Q Exactive Plus.

## Open points for reviewers

1. **Stage names.** The paper and PRIDE protocol give E12.5, E14, E15.5, E17 and P0. The file
   and MaxQuant names give E13, E14p5, E16, E17p5 and P0, a constant 0.5-day offset. The paper's
   labels are kept as free text in `characteristics[developmental time point]` (matched in order)
   and used as a factor. `characteristics[developmental stage]` uses the verified coarse EFO terms
   `mouse embryo stage` and `neonate`, because EFO has no exact terms for E14, E17 or P0.
2. Replicates with the same number (input / 80S / polysome) come from the same lysate per the
   paper, but they are modelled as separate sources.
3. The suffixes `_scx` (E13 polysome rep3) and `_re` (P0 polysome rep1) are not explained.
4. Precursor tolerance is 4.5 ppm, taken from `mqpar.xml` (the protocol text says 6 ppm).
