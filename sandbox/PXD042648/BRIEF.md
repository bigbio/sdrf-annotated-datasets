# PXD042648 SDRF annotation report

## Study
Deciphering the proteome of naturally released extracellular vesicles from Leptospira interrogans serovar Pomona in response to temperature and osmotic stresses.
Paper: Techawiwattanaboon T et al., Sci Rep 2023;13:18601, DOI 10.1038/s41598-023-45863-0, PMID 37903905 (open access; full Methods read on nature.com. Europe PMC was unreachable, so no PMCID was resolved).

## Scope, evidence and decisions
Status: **sandbox**. 180 rows (60 RAW x 3 dimethyl labels), 32 columns, template ms-proteomics v1.1.0.

- **Deposit.** The PX record (ProteomeCentral PROXI, `resultType=full`) lists 121 files: 60 RAW, 60 MGF with the same stems, and 1 `search-20230526T152332Z-001.zip` (204 MB, presumably MaxQuant output; not read). The RAW files are `ECV_Set1F1-F10` and `ECV_Set{2..6}_F1-F10`. The FTP directory listing confirms the same files.
  **Reconciliation:** all 60 RAW are annotated and every row references a RAW, never an MGF (60/60). The MGF and the zip are not data-file rows.
- **Design (STATED, paper Methods).**
  - Three overnight culture conditions of a low-passage serovar Pomona hamster isolate: in vitro EMJH 30 °C; temperature shift to 37 °C; EMJH + 120 mM NaCl at 30 °C. Six biological replicates of each.
  - EVs were taken from culture supernatant, purified by ultracentrifugation and sucrose gradient (fractions 5-8 pooled), then digested in solution.
  - Labels: 30 °C = light, 37 °C = medium, NaCl = heavy ("respectively"). Labelled samples were pooled 1:1:1 and split into **10** high-pH RP fractions (Pierce kit). That matches F1-F10 per set.
  - Statistics confirm the pairing: M/L = 37 °C/30 °C and H/L = NaCl/30 °C.
- **Labels.**
  - DIMETHYL0 = light, CH2O/NaBH3CN, +28.0313 → UNIMOD:36.
  - DIMETHYL4 = medium, CD2O/NaBH3CN, +32.0564 → UNIMOD:199.
  - DIMETHYL8 = heavy, 13CD2O/NaBD3CN, +36.0757 → UNIMOD:330 (not 510).
  Masses are from the paper's MaxQuant settings and were matched against unimod.org. Each label's mods are written per channel on K and on `PP=Any N-term`, as in PXD046383.
- **Set → biological replicate (INFERRED).** Six sets and six biological replicates per condition, so Set*n* = replicate *n*: one L/M/H pool per replicate, fractionated into F1-F10. The paper never names the sets. Fraction identifier = F number (STATED: 10 fractions).
- **Search (paper Methods; the deposited zip was not readable).**
  - MaxQuant 2.1.1.0, Trypsin/P (2 missed cleavages); main search 4.5 ppm (first search 20 ppm).
  - Fixed: carbamidomethyl C and dimethyl label on N-term/K. Variable: oxidation M.
  - Wet lab: DTT 10 mM, IAA 40 mM, porcine trypsin.
- **Acquisition (paper).** EASY-nLC1000, DDA top-10, MS1 70k / MS2 17.5k, HCD NCE 27%, scan range 400-1600 m/z.

## Conflicts
1. **Instrument (unresolved; this is the main reason for sandbox).** The PX record says Q Exactive HF (MS:1002523). The paper says "Q-Exactive Orbitrap Plus".
   - The shell has no network, so the RAW header could not be range-read. The cloud browser cannot range-read binaries either.
   - I followed the precedence rule (paper > PX field) and wrote **Q Exactive Plus (MS:1002634)**.
   - Weak supporting context: same-lab Bangkok datasets PXD034530/PXD046383 were Q Exactive Plus by RAW header.
   - To resolve: read the first ~256 KB of any `ECV_*.raw` (utf-16-le) or `summary.txt` in the search zip.
2. **Organism.** PX lists Leptospira interrogans serovar Copenhageni str. Fiocruz L1-130 (taxid 267671). That is the **search database** organism. The samples are serovar **Pomona** (title + Methods), so I used NCBITaxon:44276, confirmed via an NCBI taxonomy exact-name search.
3. **PX modifications** say "No PTMs are included in the dataset", but the paper's search lists carbamidomethyl, dimethyl and oxidation. The paper was used.

## Values left not available / not applicable
- `organism part`, `cell type`: not applicable (bacterial culture-supernatant EVs; no anatomy or cell type).
- `disease`: not applicable.
- `comment[fragment mass tolerance]`: not available. The paper says only "default search parameters". The MaxQuant FTMS default (20 ppm) was not asserted.
- The EV nature of the material is carried in `source name` only. ms-proteomics `material type` allows only tissue/cell/cell line/organism part/whole organism/synthetic, and none fits. Strain or isolate details (low-passage hamster isolate) have no column licensed by ms-proteomics, so they were omitted.
- `characteristics[treatment]` / `factor value[treatment]` hold free text naming the condition. There is no NCIT/EFO term for these culture shifts.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics`: "Everything seems to be fine". This was **structural only**: ontology validation is unavailable in this environment because the OLS extras are not installed. A mutation test (dropping `comment[data file]`) was caught.

Accessions were verified live from primary sources because EBI/OLS4 was down on 2026-11-25:
- NCBITaxon: NCBI eutils.
- UNIMOD: unimod.org.
- MS: Ontobee.
- PRIDE: pride_cv.obo on GitHub.

Scratch evidence: `/home/claude/bangkok3/scratch/PXD042648/`.

## Review status
pending
