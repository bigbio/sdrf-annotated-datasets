# PXD033191 — sandbox draft (one value missing)

*Drosophila melanogaster* head and intestine, wild type vs *lgl* mutant vs *lgl* + melatonin, sampled
at 0/6/12/18 h (6-h intervals over 24 h); label-free, Orbitrap Fusion. Arch Insect Biochem Physiol
2023 113:e22008 (not open access).

`PXD033191.sdrf.tsv` maps all 72 RAW from the file names
(`{H,INS}{00,06,12,18}{WT,LGL,LGLM}_{1-3}.raw` = tissue × time × group × replicate; full 2×4×3×3
factorial confirmed against the ProteomeCentral list).

**Why it is not in `annotations/`:** `comment[cleavage agent details]` is `not available`, which the
`ms-proteomics` template rejects — no reachable source states the enzyme (PRIDE protocol text was
unreachable this session; the paper is closed; OmicsDI carries no protocol). Everything else
validates.

To finish: read the PRIDE sample protocol, set the enzyme, and confirm
1. `_1–_3` are biological replicates (inferred);
2. fly stage / strain (`developmental stage`, `strain or breed` = `not available` for now);
3. whether 0/6/12/18 are ZT hours;
4. search modifications beyond Carbamidomethyl (PX lists only "iodoacetamide derivatized residue").
