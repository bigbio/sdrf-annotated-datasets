# PXD063183 — sandbox draft

LX-2 hepatic stellate cells + TGF-β1 10 ng/mL ± 7-octenoic acid, 3 + 3 RAW.
Publication: Usuwanthim K et al., Sci Rep 2025;15:45609, doi:10.1038/s41598-025-29722-8 (published 28 Nov 2025).

Paper methods: trypsin 1:40, 37 °C, 6 h; 1 mM TCEP; 5 mM iodoacetamide; EASY-nLC1000, DDA top 15, HCD 29; Proteome Discoverer 2.4. `comment[cleavage agent details]` is now Trypsin.

**Open:** instrument — paper says HF-X, PX record says Q Exactive HF (draft keeps the PX value). Search mods/tolerances not stated in the paper.

Validation: `parse_sdrf validate-sdrf --use_ols_cache_only` (with ontology checks) passes; warnings only for free-text treatment values.
