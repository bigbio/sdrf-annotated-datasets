# PXD036811 — under repair

9 coordinate collisions remain. Every group is a pair distinguished only by the submitter's `DR2a` / `DR2b` tokens. The deposit's protocol describes standard immunoaffinity chromatography without defining them, and the publication (Naghavian et al., Nature 2023, 10.1038/s41586-023-06081-w) describes one HLA class II isolation per sample using L243 and Tü39 mixed 1:1 with data-dependent acquisition in technical triplicates, with no occurrence of `DR2a` or `DR2b` in its full text. The tokens are thus undefined in both sources, and the paper's single 1:1 antibody mix argues against reading them as allotype-specific antibody arms — which leaves `characteristics[cell line]` plus distinct `source name`s, or `comment[fraction identifier]`, as untestable alternatives.

Affected file(s): `PXD036811.sdrf.tsv`.

The other defect classes from the first submission (ontology-invalid `characteristics[sample type]`, `NT=`/`AC=` characteristics cells, pandas artifact headers) are fixed in the file above; the coordinate collisions described here are the only remaining blocker.
