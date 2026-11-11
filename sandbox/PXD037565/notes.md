# PXD037565

Sandbox: The file fails `parse_sdrf validate-sdrf` for ms-proteomics: organism `Ideonella sakaiensis` is not found in the NCBITaxon list CI checks. Separately, the deposit has no design file and MaxQuant experiment names are only 1-8, so the five carbon-source treatments (PET, terephthalic acid, ethylene glycol, ethyl glycolate, sodium glyoxylate) cannot be mapped to files. No factor value is declared and biological replicate is a placeholder.

## Return criteria
- Fix the organism term so it validates, and obtain a file-to-treatment map (paper is closed access).
- Re-review, then move to `datasets/PXD037565/`.
