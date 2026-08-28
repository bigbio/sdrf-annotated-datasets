# Single-cell PRIDE autoresearch drafts

Generated with the sdrf:autoresearch workflow for target `all PRIDE single-cell datasets`, using PRIDE Archive project/file APIs, Europe PMC accession searches, and the `ms-proteomics` + `single-cell` SDRF templates.

This folder contains the campaign manifest. Accession-specific draft SDRFs are staged under `sandbox/{ACCESSION}/{ACCESSION}.sdrf.tsv` unless an annotation already existed in `datasets/`. These sandbox drafts are evidence-backed scaffolds, not finished curator-reviewed submissions. In particular, TMT/channel-level single-cell mappings often require publication supplements or deposited sample maps before promotion to `datasets/`.

Summary:

- Confirmed candidate accessions: 109
- Existing dataset updated directly: 1
- New sandbox draft SDRFs: 108
- Templates applied to drafts: `NT=ms-proteomics;VV=v1.1.0` and `NT=single-cell;VV=v1.0.0`
- Organism templates applied where the local v1.1.0 template manifest has a biological match: 84 human, 18 vertebrate, and 1 plant draft. The 5 yeast drafts were not forced into an organism layer because the current manifest has no fungal/yeast template.
- Round 2 enrichment applied to all 108 sandbox drafts using PRIDE project metadata, complete PRIDE file lists, and Europe PMC accession evidence.
- Round 2 added richer method fields where evidence supported them: acquisition mode, dissociation method, collision energy, precursor/fragment tolerances, digestion enzymes, modification parameters, sample-preparation batch, FACS/LCM/microfluidics/nanoPOTS metadata, and inferred cell-line hints.
- Round 3 validation updated all 108 sandbox drafts to pass `parse_sdrf validate-sdrf --skip-ontology` for `ms-proteomics`, `single-cell`, and each applicable organism template.

Validation notes:

- `datasets/PXD043473/PXD043473.sdrf.tsv` passes `parse_sdrf validate-sdrf --skip-ontology` for `ms-proteomics` and `single-cell`.
- `sandbox/PXD016921/PXD016921.sdrf.tsv` passes the same structural/template check as a representative label-free draft.
- All 108 sandbox drafts now pass structural/template validation with `--skip-ontology`.
- For 21 multiplexed drafts, `comment[label]` was filled from the PRIDE quantification mode so the required label field is structurally valid. Exact sample-to-channel mapping remains lower confidence until supplement-backed channel maps are curated.

See `manifest.tsv` for PRIDE URLs, Europe PMC hits, publication identifiers, evidence terms, file counts, and draft paths. See `autoresearch-round2.tsv` for per-accession enrichment status, unresolved high-value gaps, and validation status. See `validation-round3.tsv` for per-template validator results.
