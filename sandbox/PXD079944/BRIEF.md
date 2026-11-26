# PXD079944: RAW/MSF mapping recovered; biological and fraction crosswalk unresolved

Checked on 2026-09-29 against the [PRIDE deposit](https://www.ebi.ac.uk/pride/archive/projects/PXD079944), all 18 RAW/MSF file records, the embedded SQLite metadata in the deposited MSF files, and the associated [iScience article](https://doi.org/10.1016/j.isci.2026.116975).

The article reports 18 LC-MS/MS samples: three non-targeting (NT) controls and three Wnt10b-siRNA knockdown samples, each measured in three technical replicates. The project protocol identifies P12 C57BL/6J organotypic cerebellar slices, 10 nM siRNA, overnight trypsin digestion, C18 desalting and high-pH reversed-phase fractionation into eight fractions.

Every deposited MSF contains a one-to-one internal workflow and RAW path. The six filename families are:

| archive RAW family | MSF workflow families | study file IDs |
| --- | --- | --- |
| `20230415_NT_siRNA_1..3.raw` | `20230415_Control_1..3` | F1–F3 |
| `20230415_Wnt10b_siRNA_1..3.raw` | `20230415_KO_1..3` | F4–F6 |
| `20230416_NT_siRNA_1..3.raw` | `20230416_Control_1..3` | F7–F9 |
| `20230416_Wnt10b_siRNA_1..3.raw` | `20230416_KO_1..3` | F10–F12 |
| `20230417_NT_siRNA_1..3.raw` | `20230417_Control_1..3` | F13–F15 |
| `20230417_Wnt10b_siRNA_1..3.raw` | `20230417_KO_1..3` | F16–F18 |

The MSF metadata independently records Orbitrap Fusion Lumos, Proteome Discoverer 2.4.1.15, Sequest HT with Percolator validation, Trypsin (full), two missed cleavages, 10 ppm precursor tolerance, 0.02 Da fragment tolerance, and the UniProtKB mouse database (`UP000000589`, FASTA dated 2024-10-28). The embedded workflow lists oxidation and carbamidomethylation as **dynamic** modifications, N-terminal acetylation as dynamic, and a custom static `MappingL` J→L substitution (+113.08406 Da). This directly conflicts with the PRIDE prose that calls carbamidomethylation static; the draft records the deposited MSF setting and retains the discrepancy here.

The draft SDRF records all 18 RAWs and the explicit NT/Wnt10b condition labels. It does not assign biological replicate, technical replicate, or fraction identifiers: the paper does not provide a file-level crosswalk from the date/workflow names to the three biological samples or to the eight fraction numbers. The `comment[author sample identifier]` column preserves the embedded workflow name. No fraction numbers or replicate relationships are inferred. Keep this annotation in `sandbox/` until the authors or a deposited sample sheet resolve those relationships.

## Local validation

The draft has 18 rows and a one-to-one RAW list. `git diff --check` is clean and the repository review finds no ragged rows, duplicate coordinates or vendor/file contradiction. The pinned `validate-sdrf` gate still fails on the deliberately unavailable biological replicate, technical replicate, fraction identifier and acquisition-method columns; it also emits offline ontology warnings for the free-text treatment and fractionation labels. Those failures reflect the unresolved crosswalk and are retained rather than filled with guessed values. The unresolved record is a curation boundary, not a reason to fabricate sample relationships.
