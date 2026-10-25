# PXD012771 — under repair

17 coordinate collisions remain. Within one isolation arm, runs of the same sample differ only by the submitter's aliquot codes (`C9-W1-1a`, `-1b`, `-2a`, `-2b`, `-3`). The deposit records both isolation arms (mild acid elution and MHC immunoaffinity chromatography) in `characteristics[immunopeptidome enrichment method]`, but neither the deposit's protocol text nor the publication defines these codes: the full text of Sturm et al., J Proteome Res 2021;20:289-304 (10.1021/acs.jproteome.0c00386) contains no occurrence of `C9`, `W1` or 'aliquot', and reports only triplicate 5 µL LC-MS injections per sample. Whether the codes denote separate immunoprecipitations, wash fractions or repeat injections therefore cannot be established; encoding them as `comment[fraction identifier]`, `comment[sample preparation batch]` or `characteristics[biological replicate]` would be a guess, and each choice changes what the file asserts.

Affected file(s): `PXD012771.sdrf.tsv`.

The other defect classes from the first submission (ontology-invalid `characteristics[sample type]`, `NT=`/`AC=` characteristics cells, pandas artifact headers) are fixed in the file above; the coordinate collisions described here are the only remaining blocker.
