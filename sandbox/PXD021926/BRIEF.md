# PXD021926 SDRF annotation report

## Study
A novel enzyme-mediated method for covalent surface modification of extracellular vesicles to achieve targeted drug delivery.
Pham et al. 2021, J Extracell Vesicles 10(4):e12057, doi:10.1002/jev2.12057, PMID 33643546, PMC7886705. The paper's Data availability section gives "PDX021926", a typo for PXD021926. The submitter (Kappei) is a co-author, and the title and abstract match, so the link is accepted.

## Scope, evidence and decisions
Status: **sandbox**. 12 rows x 35 cols: 12 RAW files, label-free, 1 row per file. Templates: ms-proteomics, human.

Deposited vs annotated: ProteomeCentral PROXI (2026-11-27) lists 14 files: 12 .raw files and 2 MaxQuant output zips (`..._biotin_peptide_pulldown.zip`, `..._RBCEVs.zip`). All 12 RAW files are annotated. The zips are search outputs, not runs. This matches the campaign cache (12 RAW / 14 files). The PRIDE FTP listing timed out, so the file list comes from PROXI only, and neither the zips nor the RAW headers were read.

Three groups (paper section 4.8 and Fig 2d; group identity STATED by the file names):
- `EVs_biotin_peptide_01-04`: RBCEVs ligated to biotinylated TR5 peptide by OaAEP1 ligase, lysed in RIPA, then streptavidin magnetic-bead pulldown.
- `EVs_unligated_01-04`: control. Uncoated RBCEVs incubated with biotinylated TR5 without ligase, then the same pulldown.
- `RBCEVs_01-04`: total RBCEV proteome, 100 ug lysate. The paper states these come from "4 separate donors".
  - Mapping file _0n to donor n is INFERRED from the file order.
  - Files 03/04 say "SoN" where 01/02 say "SoM". This looks like a submitter typo; the names are kept verbatim.

Pulldown replicates: biological replicate 1-4 is taken from the file suffix. The donor for each pulldown replicate is not stated, so `individual` = not available. Whether ligated_0n and unligated_0n are paired (same EV batch) is also not stated.

Sample:
- Human RBC-derived EVs from Hong Kong Red Cross healthy O-group donors. EV release was induced with calcium ionophore; EVs were purified by ultracentrifugation.
- Values used: organism part = blood, cell type = erythrocyte (CL:0000232, checked live in OLS), disease = normal.
- material type = cell. This is a judgement call: the allowed list has no EV term. The EVs come from isolated primary RBCs.

Protocol (Methods 4.8, STATED):
- Sample prep: 12% NuPAGE gel run for only 10 min (cleanup, not fractionation, so fractionation = not applicable). Reduction with 10 mM DTT, alkylation with 55 mM IAA, in-gel trypsin digestion (Promega), StageTips.
- LC-MS: EASY-nLC 1200 coupled to a Q Exactive HF. TOP20 DDA, so dissociation = HCD. Gradient 105 min for the pulldowns, 215 min for the RBCEV proteomes; the run dates (0913 vs 1007) are consistent with this split.
- Search: MaxQuant 1.5.2.8. Carbamidomethyl C fixed; Oxidation M and protein N-term Acetyl variable.
- Instrument: Q Exactive HF in both the PX record and the paper. Not confirmed from the RAW headers (FTP unreachable).

## Values left not available / not applicable
- age, sex, ancestry, developmental stage: not available. Anonymous Red Cross donors; the paper gives nothing.
- individual for the pulldown rows: not available. The donor is unstated.
- fractionation method: not applicable (single short gel lane).
- Mass tolerances and MS1 scan range: omitted. MaxQuant "standard settings" were used but the values are not stated, and mqpar.xml was unread because the zips are on FTP.
- Mods: taken from the Methods, not from mqpar.xml. The PX record's "No PTMs" is contradicted by the paper, and the paper wins.

## Conflicts
None material. The paper's Data availability gives PDX021926 (typo); the PX record gives "No PTMs" but the paper's Methods list modifications.

## Validation
- `parse_sdrf validate-sdrf --template ms-proteomics --template human --use_ols_cache_only`: no errors. The OLS ontology plugin is not installed here, so only the structure was checked.
- `sdrf_review.py`: [OK].

## Why sandbox
Three points are INFERRED or unverified:
- The RBCEV file to donor order.
- Pulldown replicate pairing and donors.
- RAW headers and mqpar.xml were unread (FTP down).

These would unblock it:
- mqpar.xml from the two zips: modifications, tolerances, experiment names.
- RAW headers.

## Review status
pending
