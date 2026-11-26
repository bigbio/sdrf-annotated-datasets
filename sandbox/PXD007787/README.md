PARTIAL: 256 of 258 RAW files annotated. BLOCKED for PT5354-1.raw and PT5354-2.raw only (phospho TMT10, no public channel map).

# PXD007787 working notes

Final files:
- `PXD007787-silac.sdrf.tsv` (416 rows, 208 RAW): interphase SILAC (16 single-shot runs) + mitotic-subphase SILAC (2 reps x 4 subphases x 24 fractions)
- `PXD007787-tmt.sdrf.tsv` (288 rows, 48 RAW): mitotic-subphase TMT6plex, biological replicate 3, 24 fractions x 2 technical replicates
- `PXD007787-{silac,tmt}.evidence.json`, `validation.txt`, `PR_BODY.md`

Why split: `parse_sdrf convert-openms` refuses SILAC and TMT in one SDRF.

Rungs checked for the phospho TMT channel map (PT5354-1/-2): paper Methods/Results/figure legends
(only the mitotic TMT map is given), Supplementary file 3 (column names B1.G1..B2.M, no channels),
PRIDE project record, MQresults.zip `MQ results/phosphorylation/` (only txt/ output; no mqpar.xml or
experimental design; evidence.txt has anonymous "Reporter intensity 0-9"). Mapping channels from
column order or from the data would be inference, so these 2 runs are left out.

Regenerate: `python3 -I scripts/make_tables.py .` then `sdrf-tools build` per arm (see validation.txt),
`python3 -I scripts/make_manifest.py .`

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above as blocked have no public sample/channel map. Promote to `datasets/` only once they are resolved, or once a maintainer accepts the partial coverage.
- Working files mentioned above (evidence/, validation.txt, scripts, tables) are not part of this submission.
- Review status: an independent review PASSED `PXD007787-silac.sdrf.tsv`. It FAILED `PXD007787-tmt.sdrf.tsv` only for leaving out PT5354-1/-2. The reviewer showed that the phospho TMT reporter-channel map can be rebuilt by joining the deposited `Phospho (STY)Sites.txt` with Supplementary file 3 (a constant log-ratio offset across ~3,600 sites). Under this repository's annotation rules a map derived from the data is not public evidence, so the two runs stay out until the authors confirm the channel order or a maintainer accepts the data-derived map.
