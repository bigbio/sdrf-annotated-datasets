# PXD033191 — sandbox draft (one value missing)

*Drosophila melanogaster* head and intestine, wild type vs *lgl* mutant vs *lgl* + melatonin, sampled
at 0/6/12/18 h (6-h intervals over 24 h); label-free, Orbitrap Fusion. Arch Insect Biochem Physiol
2023 113:e22008 (not open access).

`PXD033191.sdrf.tsv` maps all 72 RAW from the file names
(`{H,INS}{00,06,12,18}{WT,LGL,LGLM}_{1-3}.raw` = tissue × time × group × replicate; full 2×4×3×3
factorial confirmed against the ProteomeCentral list).

**Update (same day): enzyme and mods resolved.** The deposited MaxQuant `Head_summary.txt`
(PRIDE FTP) lists, for every head run: Trypsin (specific, ≤2 missed cleavages), fixed
Carbamidomethyl (C), variable Oxidation (M) and Acetyl (Protein N-term); each RAW is its own
MaxQuant experiment (`00LGLM_1` … `18WT_3`), consistent with `_1–_3` being separate samples.
`Intestine_parameters.txt` (MaxQuant 2.0.1.0) quantifies the same two variable mods. The file now
passes `parse_sdrf validate-sdrf --use_ols_cache_only` and can be promoted to `datasets/`.

Still to confirm: fly stage/strain (`not available`), whether 0/6/12/18 are ZT hours, and that the
intestine search used the same fixed mod (only its parameters.txt, not its summary, was read).
