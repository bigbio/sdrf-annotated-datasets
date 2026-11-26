PARTIAL: 8 of 12 raw files annotated. These 4 runs are not mapped because no public evidence gives their channel->sample identity:
- Statler_20150223_CHS_Veltel_E-H.raw
- Statler_20150223_CHS_Veltel_E-L.raw
- Statler_20150223_CHS_Veltel_F-H.raw
- Statler_20150223_CHS_Veltel_F-L.raw

The mapped runs (experiments A-D) come from a PUBLISHED_TABLE_JOIN: the authors' Supplementary Table 1
(41556_2021_767_MOESM4_ESM.xls), joined exactly to the deposited MaxQuant proteinGroups.txt
'Ratio H/L normalized <experiment>' columns. A human decides whether
this route is acceptable; the maintainer accepted it (see below).

Rungs checked for E/F: the paper's full text (PMC7617174) and Extended Data legends, Supplementary Table 1
(only 4 comparisons = 8 runs), the Nature ESM files (MOESM1 supplementary information = flow-cytometry gating only; MOESM2 reporting summary; MOESM3 peer-review file, which repeats the 4 comparisons a-d; MOESM4 = Supplementary Table 1; MOESM5-10 videos), the PRIDE record and
protocol (mentions an unreported Rab21 D135N mutant), MaxQuant summary.txt/parameters.txt (experiment names
A-H..F-L only, no condition names), and the Zenodo records cited in Code Availability (4812018 and 4811213:
cell-tracking code and a StarDist model, not proteomics). No mqpar.xml or experimentalDesign file is deposited.


## Channel map (accepted by the maintainer)
An independent reviewer redid the join and confirmed it is exact:
- Each Supplementary Table 1 log10 forward/reverse column equals ±log10 of one experiment's deposited `Ratio H/L normalized` for every resolvable gene, with a maximum deviation of 5e-15.
- The next-best experiment matches at most 1 gene.

Read as log10(X/Y), the columns give:

| Run | Heavy | Light |
|---|---|---|
| A-L | WT | DN |
| A-H | DN | WT |
| B-L | GFP | CA |
| B-H | CA | GFP |
| C-L | WT | CA |
| C-H | CA | WT |
| D-L | GFP | WT |
| D-H | WT | GFP |

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the E/F files listed above have no public sample/channel map. Promote it to `datasets/` only once they are resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Working files (scripts, evidence/, validation output) are not part of this submission.
- Review status: an independent fresh-context adversarial review confirmed every annotated run and failed the file only on the missing E/F coverage.
