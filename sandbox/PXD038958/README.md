# PXD038958 — BLOCKED: partial SDRF (6 of 30 raw files)

BLOCKED: the sample→file→SILAC-channel map for 24 of the 30 raw files cannot be
resolved from openly retrievable public evidence. Only the 6 runs whose label is
evident from the file name are annotated here.

- Dataset: https://www.ebi.ac.uk/pride/archive/projects/PXD038958 — "Spatial SILAC
  Regorafenib Treated Bottom-up Proteomic Analysis"
- Publication: Beller NC, Wang Y, Hummon AB. Anal Chem 2023;95(30):11263-11272.
  PMID 37462741, PMC10676637, doi:10.1021/acs.analchem.3c00905
- Organism / cell line: Homo sapiens, HCT 116 (CVCL_0291), colon carcinoma
- Templates: ms-proteomics v1.1.0, human v1.1.0, cell-lines v1.1.0

## What is annotated

`051122_Sample_Heavy1-3.raw` (SILAC heavy, Arg10/Lys8 = UNIMOD:267/259) and
`051122_Sample_Light1-3.raw` (SILAC light), one row per file, the unused channel
omitted. Treatment and culture format (2D monolayer label-incorporation check vs
singly labeled spheroid) are `not available` because no file-level statement exists.

## What is missing

`051122_Sample_{1,2,3,7,8,9,10,11,12,16,17,18,19,20,21,25,26,27,28,29,30,34,35,36}.raw`
— the regorafenib (9.05 µM, 48 h) vs control spheroids, singly labeled and duplex
(core vs outer label) in biological triplicate. The deposited MaxQuant parameters
(`05162022_duplex_regorafenib_spatial_SILAC_search_parameters.xml`) name the
experiments only by number, and the paper's main text does not list which number is
which condition. The map is described as being in Supplementary Figure 8 / Figure 3
(`NIHMS1942467-supplement-Supp_Materials_1.docx` / `_2.docx`), which could not be
retrieved: Europe PMC reports the article as not open access, and the PMC and ACS
copies are behind a browser challenge.

## To unblock

From the supplementary material (or the authors), get for each numbered run: treatment
(regorafenib / control), labelling scheme (singly labeled heavy, singly labeled light,
duplex heavy-core/light-outer, duplex light-core/heavy-outer), and replicate. Then add
one row per (file, occupied SILAC channel), with `characteristics[treatment]`, a
spatial region characteristic for duplex channels, and factor values for treatment and
region, re-validate, and promote this folder to `datasets/`.
