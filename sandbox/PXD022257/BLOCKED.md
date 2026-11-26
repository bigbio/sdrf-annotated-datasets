# PXD022257 annotation blocked

PXD022257 (Graves' ophthalmopathy orbital fibroblasts, Front Endocrinol 2021, PMC7919747) is a TMT10plex study. It covers 14 primary fibroblast cultures (4 active GO, 5 inactive GO, 5 controls) in two TMT sets (`Sitaset1F1-9`, `Sitaset2F1-9`; 9 high-pH fractions each, 18 RAW files), on a Q Exactive Plus.

The channel → sample map is not available:
- **PD `.msf`:** the `Sitaset1F.msf` StudyDefinition (study "Sita TMT 8 plex") has an empty `<Factors />` block, and no sample names are attached to reporter channels. The deposited `Sitaset1F-01.msf` has the same size. No set-2 `.msf` is deposited.
- **Paper:** it names only "10-plex tandem mass tag" and gives no channel table.
- **Europe PMC supplementary:** the request returned an HTML error.

Search parameters are recoverable (PD: trypsin, 10 ppm / 0.02 Da, TMT6plex + carbamidomethyl fixed, oxidation + acetyl variable), but with no channel identities no SDRF is emitted.

**Evidence checked:** PRIDE v3 record and `files/all`; the full `Sitaset1F.msf` (SQLite `AnalysisDefinition`, `WorkflowInputFiles`); PMC7919747 full text.

**To unblock:** the TMT channel layout of both sets (from the authors or a deposited study design).
