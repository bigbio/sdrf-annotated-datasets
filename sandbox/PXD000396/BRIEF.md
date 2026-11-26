# PXD000396: acquisition metadata repaired; biological grouping unresolved

Reviewed on 2026-09-28 using the [PRIDE project](https://www.ebi.ac.uk/pride/archive/projects/PXD000396),
the [associated article](https://doi.org/10.1002/pmic.201300418), and the
[deposited files](https://ftp.pride.ebi.ac.uk/pride/data/archive/2014/07/PXD000396/).

The complete two-page archive listing contains 40 RAWs and 40 pepXML search
exports. All RAW headers identify Q Exactive, HCD at 30 NCE, and an MS1 range
of 350–2000 m/z. Every pepXML header contains the same Mascot search settings:
trypsin, 5 ppm precursor tolerance, 50 mmu (0.05 Da) fragment tolerance, fixed
cysteine carbamidomethylation, variable methionine oxidation, and variable
asparagine/glutamine deamidation. The search-summary input paths link those
exports to all 40 RAWs.

The archived `sdrf.tsv` provides source names, BioSamples accessions, and
technical-replicate numbers but explicitly leaves biological replicate
unavailable in all 40 rows. The separate community SDRF assigns biological
replicate 1 throughout without adding a supporting preparation crosswalk.
The revision retains the original unavailable values, source/accession
mapping, and reported technical-replicate numbers. Independent culture and
digest preparation relationships remain unresolved.

The draft restores public file URIs, updates HeLa origin/donor metadata from
[Cellosaurus CVCL_0030](https://www.cellosaurus.org/CVCL_0030), and removes
the assignment of analytical HPLC as offline fractionation. Flow rates and
gradient lengths agree with both archive SDRFs and the RAW filename labels.
Genetic ancestry is not inferred from a race label.

The source-reconciliation tool flags trypsin because the project record's
preparation and analysis protocols are both `Not available`. The archived
SDRF explicitly names trypsin, and the article describes a tryptic HeLa
peptide mixture; this annotation is supported by those sources. The missing
biological-replicate mapping remains a validation blocker, so this revision
stays in `sandbox/`. The existing canonical SDRF has not been replaced.

All three declared templates were checked using sdrf-pipelines
`701356bd5309f352b499846dcb4c31709b65bf8a`; each fails only on the unavailable
biological-replicate field. No errors or warnings were suppressed.
