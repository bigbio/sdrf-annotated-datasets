# PXD084819: experimental replicate type unresolved

The 34-row draft was checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD084819), deposited `PRIDE_RF_CNC_Proteomics_Sample_Mapping.xlsx`, all 34 Waters archive headers/method files and the directory of `RF_CNC_Proteomics_PEAKS_Analysis_Files.zip`. The deposited [paper DOI](https://doi.org/10.1073/pnas.2626934123) was not retrievable.

## Supported mapping

The author workbook maps RF435–RF439 to TCPP-CNC, mPEG-CNC, POEGMA-CNC, PSBMA-CNC and PHEAA-CNC, with 1-hour/3-hour incubations and three experimental replicate identifiers. Three FBS controls are also included. RF435, 3 hours, experimental replicate 1 has two explicitly linked injections of 3 and 5 uL: these share a source name and receive technical identifiers 1 and 2. The remaining single acquisitions receive technical identifier 1 within their author sample identifier. All 34 archives are represented, yielding 33 author sample/replicate combinations; their mutual preparation independence is unresolved.

`comment[data file]` records the actual Waters `.raw` directory inside each archive, including spaces. Archive names and author spreadsheet names are separate provenance fields. The workbook's `20250711_PMA_FBS_1_1uL.raw.zip` differs only in case from deposited `20250711_PMA_FBS_1_1ul.raw.zip`; the exact deposited name is used in the URI and archive column.

Every `_HEADER.TXT` identifies Xevo G2-XS QTof, and every `_extern.inf` contains a DDA method with 200–2000 m/z survey range. Archive protocols support trypsin, DTT/IAA, PEAKS Studio X Plus, fixed carbamidomethylation, 0.1 Da precursor and 0.2 Da fragment tolerances. The separate 20 ppm LFQ mass-matching setting is not substituted for precursor search tolerance. Unreported variable modifications remain unknown.

## Remaining limitation

The workbook calls these experimental replicates but does not establish independent FBS lots/donors or independent preparations versus repeated analyses. Donor and pooling relationships are unknown. Author replicate numbers are preserved separately, and biological replicate remains `not available`. In particular, three serum-derived replicates are not annotated as three calves.

Both templates and the review gate fail on the missing biological-replicate values. Record reconciliation passes. This draft stays in `sandbox/` until the replicate basis is documented.
