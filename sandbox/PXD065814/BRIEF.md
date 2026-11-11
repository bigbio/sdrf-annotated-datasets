# PXD065814: mucus-type and replicate mapping missing

The 10-row draft was checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD065814), all ten RAW headers, deposited `mqpar.xml`, both deposited protein tables and the [author preprint](https://doi.org/10.26434/chemrxiv-2025-jx7gt) ([institutional copy](https://pure.mpg.de/rest/items/item_3682661_1/component/file_3682663/content)). The [published paper](https://doi.org/10.1126/science.adx7367) and its supplementary PDF could not be retrieved. The preprint is explicitly distinguished from the published version.

## Supported annotations

All ten RAWs identify Q Exactive HF, HCD at 28 NCE and 300–1750 m/z MS1 scans. Their exact basenames match `mqpar.xml` experiments 01–10. This parameter file confirms MaxQuant 2.2.0.0, Trypsin/P search specificity, 4.5 ppm main-search tolerance, 20 ppm FTMS fragment tolerance, fixed carbamidomethylation, and variable methionine oxidation/protein N-terminal acetylation. Physical preparation used Lys-C followed by trypsin, with TCEP/chloroacetamide. SCX StageTips are peptide cleanup; no separate SCX fractions are inferred.

## Remaining limitations

The deposition names the runs only `Sample01`–`Sample10`. Neither MaxQuant nor the protein tables maps these identifiers to lubricant, adhesive, epiphragm, yellow or bubbly mucus. The protein table column **`Snail_IDs` contains protein identifiers such as `Cnem001132-RA_True_0`, not individual snail identifiers**.

The preprint describes collection from 5–8 animals and two samples per mucus type, plus a repeated experiment. It does not provide a direct 01–10 crosswalk or establish whether the deposited pairs are independent pools, preparations or repeated injections. Therefore mucus type, biological replicate, technical replicate, individual and per-run pooling remain unknown. The C981 isolate is the search-genome source, not a demonstrated strain of the sampled animals.

Both templates fail on unresolved biological/technical replicates, and the review gate additionally reports the empty mucus-type factor. The record-reconciliation enzyme warning is a repeated-column parsing issue: passing both declared enzymes separately to the same reconciliation check yields no discrepancy. This draft remains in `sandbox/` pending a sample-to-RAW crosswalk and replicate/pool definition.
