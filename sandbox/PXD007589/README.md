BLOCKED: 48 of 211 deposited RAW files (Phospho_* x24, Proteome_Drug_* x24) have no publicly evidenced sample/replicate map. The SDRF here covers only the 163 SILAC runs whose channel-to-sample map is evidenced.

# PXD007589: annotation status

- Draft SDRF: `PXD007589.sdrf.tsv` (326 rows = 163 RAW files x 2 SILAC channels, 41 columns). It validates: parse_sdrf exit 0 with warnings only, structure OK, check CLEAN, reconcile clean, convert-openms OK (see `validation.txt`).
- Evidence: `PXD007589.evidence.json`, `evidence/`. Tables: `samples.tsv`, `technical.tsv` (built with `sdrf-tools build`; generator `scripts/make_tables.py`).
- Unmapped files: `files_unmapped.txt`.

## Why blocked (channel-map ladder, rungs checked)
1. Paper (PMC6527175 full text, Methods + Fig. 1 legend). Gives the orientation of the forward experiment (heavy = proliferating myoblasts, light = myotubes; 3 biological replicates) and the reverse experiment (light = myoblast control or drug-treated, heavy = drug-free myotube control). It does not describe the `Phospho_<cond>_01-04` files, nor `Control_2`. It does not say whether _01-_04 are fractions or replicates. The histone label-free runs are described as "six conditions (three biological replicates each)" on an LTQ-Orbitrap Elite.
2. PRIDE deposit. There is no mqpar.xml, experimental design or search output for the proteome runs. The only search result is a histone Mascot .dat (`0histone_F002262.dat`). The project description adds nothing.
3. Europe PMC / PMC supplementary (Tables S1-S5). Could not be downloaded: Europe PMC says the article is not open access, PMC served a reCAPTCHA page, and jbc.org returned 403. These are result tables, which are unlikely to hold a per-file map.
4. Raw-file headers (HTTP range requests). Show that `Proteome_Drug_*_103014_*` are Q Exactive histone runs (method `Histone_standard-20143010.meth`, propionylation exclusion list), with 4 files per condition, not 3. `Phospho_*` were acquired as `Phospho1_0N` (Control), `Phospho1_2_0N` (Control_2), `Phospho2_0N` (PD), `Phospho4_0N` (Rosco). These still do not resolve the replicate or fraction structure, or what Control_2 is.
5. Cross-validation would require inferring from the data, which is not public evidence.

What would unblock it: the authors' per-file design for the reverse-experiment phospho runs and the histone runs, or a deposited MaxQuant experimentalDesign / mqpar.xml.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above as blocked have no public sample/channel map. Promote to `datasets/` only once they are resolved, or once a maintainer accepts the partial coverage.
- Working files mentioned above (evidence/, validation.txt, scripts, tables) are not part of this submission.
- Review status: no independent adversarial review has been run on this draft yet.
