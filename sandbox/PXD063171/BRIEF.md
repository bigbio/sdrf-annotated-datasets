# PXD063171 SDRF annotation report

## Study
Osteogenic differentiation regulation of canine periodontal ligament stem cells by hydrogel containing magnetic nanoparticles (PX title).
Paper: Purbantoro SD, ..., Somparn P, ..., Rattanapuchpong S. "Magnetic nanohydroxyapatite-peptide silk fibroin hydrogel induces osteogenesis in canine periodontal ligament stem cells revealed by proteomic analysis". Vet Q 2026;46(1):2672558. doi:10.1080/01652176.2026.2672558, PMID 42141999, PMC13182179. Full text read on the PMC HTML page. Its Data availability statement cites PXD063171.

Design: primary canine periodontal ligament stem cells (cPDLSCs, passages 3-5) were cultured in osteogenic medium with extract media from four silk fibroin hydrogels: HG, HG/OGP (OGP 100 nM), HG/MHAp (MHAp 0.6% w/v) and HG/OGP/MHAp. Proteomes were taken on day 7 and day 14, n = 5 (Fig. 6 legend), and comparisons are made against HG as the control. Label-free, FragPipe v21.1 "default settings for LFQ".

## Scope, evidence and decisions
**Status: sandbox.** 39 rows (39 RAW x label free) and 36 columns. Templates: ms-proteomics and vertebrates.

**Deposited vs annotated.** The ProteomeCentral PROXI record (full) lists 79 files: 39 `.raw`, 38 `.mgf`, `filelist_skyline.txt` and `checksum.txt`. All 39 RAW files are annotated, and none are excluded. `D14_G2_set2.raw` is the only RAW file without a matching `.mgf`. File names follow `D{7|14}_G{1-4}_set{n}[_yyyymmddhhmmss].raw`:
- Day 7: G1-G3 each have set1-5. G4 has `set1_20250117214145`, `set2_20250117233613`, `set4`, `set5` and `set5_20250117194721`. There is no set3, and there are no un-suffixed set1 or set2 files.
- Day 14: each group has only set1 and set2. Suffixed copies bring the totals to G1 = 5 (set1 x3, set2 x2), G2 = 4 (set1 x3, set2 x1), G3 = 5 and G4 = 5.

**Sample mapping (INFERRED, the main open point).**
1. *G1-G4 → hydrogel.* Neither the paper nor the PX record defines G1-G4. I mapped them in the order the paper always uses: G1 = HG, G2 = HG/OGP, G3 = HG/MHAp, G4 = HG/OGP/MHAp. This fits the four-group proteomics design with HG as the control, but it is not stated anywhere. Each treatment value is marked `(code Gn, inferred)`.
2. *Timestamp-suffixed files.* Xcalibur appends `_yyyymmddhhmmss` when a file name already exists. I annotated the names literally: the source is `cPDLSC_D{day}_{G}_set{n}`, the biological replicate is n, and suffixed copies of the same set are technical replicates 2 and 3. The plain file is 1, and suffixed files follow in timestamp order. There is a plausible alternative I could not test. The paper states n = 5, and the five-file totals per day-14 group fit that number. So the repeated "set1" and "set2" files may be distinct biological samples (sets 3-5) acquired under a reused sequence name. D7_G4 points the same way: set3 is missing and set5 appears twice. If so, the biological replicate numbers on day 14 are wrong, and day-14 n would be 5 rather than 2. The RAW headers (sample name or vial position) and `filelist_skyline.txt` would decide this. Neither could be read: PRIDE FTP over https and the PRIDE v3 API returned upstream connect errors, and the shell has no network.

**Instrument (conflict).** The PX record says Q Exactive (MS:1001911). The paper says "Q-Exactive Orbitrap Plus" with an EASY-nLC 1000. Following the precedence paper > PX fields, I used **Q Exactive Plus (MS:1002634)**. Not verified against RAW headers. Other Chulalongkorn CESB (Somparn) datasets in this campaign show the same PX-vs-paper pattern (PXD064135, PXD030613).

**Organism (conflict).** The PX species is "Canis lupus lupus" (NEWT:443256, the grey-wolf subspecies). The paper describes client-owned donor dogs at the Small Animal Teaching Hospital. Annotated as Canis lupus familiaris (NCBITaxon:9615).

**Other values.**
- Organism part periodontal ligament (UBERON:0008266): stated, mid-third PDL tissue.
- Cell type mesenchymal stem cell (CL:0000134): the cells were characterised as MSCs (ISCT criteria). CL has no PDL-stem-cell term.
- Disease normal: stated, clinically healthy donors without periodontal disease.
- Material type cell.
- Sampling time 7 day or 14 day, from the file prefix and the paper.
- Reduction TCEP (PRIDE:0000609) and alkylation iodoacetamide (PRIDE:0000599): stated.
- MS1 scan range 350-1400 m/z: stated as the range in which "target peaks were selected".
- Factor values: treatment and sampling time.

**Search parameters (INFERRED from "FragPipe v21.1 default settings for LFQ").** Carbamidomethyl C is fixed (UNIMOD:4), which is also supported by PX `MOD:00397` and the IAA alkylation. Oxidation M (UNIMOD:35) and Acetyl Protein N-term (UNIMOD:1) are variable. These are the defaults of the FragPipe LFQ workflow. No deposited search output (fragger.params or workflow) is available to confirm them.

**Enzyme (INFERRED).** The paper names only the EasyPep Mini MS Sample Prep Kit, so the enzyme is not stated. That kit supplies a Trypsin/Lys-C mix, so both are annotated (MS:1001251, MS:1001309). This matches how PXD064135 was annotated (same lab, same kit).

**Acquisition and dissociation (INFERRED).** DDA (PRIDE:0000627): LFQ in FragPipe, with MS2 peak lists deposited and "target peaks selected" from the MS scan. HCD (MS:1000422): the only fragmentation mode on a Q Exactive.

## Values left not available / not applicable
- `characteristics[developmental stage]`, `[sex]`, `[strain or breed]` = not available. The paper does not give the number, age, sex or breed of the donor dogs, and does not say whether cells were pooled.
- `comment[fractionation method]` = not applicable: single-shot runs, with no fractionation described.
- Omitted columns (unstated): collision energy and precursor/fragment tolerances. The FragPipe default tolerances were not asserted.

## Stated vs inferred
- STATED: organism (dog), cell source and passage, osteogenic medium, the four hydrogel compositions and their OGP/MHAp concentrations, days 7 and 14, n = 5, TCEP/IAA, EASY-nLC 1000, Q Exactive Plus (paper), MS1 range, FragPipe LFQ.
- INFERRED: the G1-G4 → hydrogel mapping; the meaning of the timestamped duplicates (treated as technical replicates); enzyme (from the kit); modifications (from FragPipe defaults); DDA; HCD; cell-type CL term.

## Conflicts
- Instrument: PX Q Exactive vs paper Q Exactive Plus. Paper used; RAW not read.
- Species: PX Canis lupus lupus vs dogs in the paper. Paper used.
- Replicates: paper n = 5 vs deposited day-14 names showing set1 and set2 only (and D7_G4 lacking set3). Unresolved; see above.

## Evidence checked
- ProteomeCentral PROXI `resultType=full` (Page URL and JSON verified PXD063171).
- PMC13182179 HTML (Methods, Results, Figure 6 legend, Data availability, Supplementary: only Table S1 primer sequences).
- Europe PMC search (OA, PMCID).

Not reachable on 2026-11-25:
- PRIDE v3 API and PRIDE FTP over https (`filelist_skyline.txt`, RAW headers): upstream connect errors.
- Europe PMC fullTextXML.
- The PMC figure page: it presented a reCAPTCHA, which was not attempted.

Term checks used Ontobee, PRIDE `pride_cv.obo` on GitHub and the OLS4 search, because OLS4 was rate-limited. UNIMOD was checked against the bundled `unimod.xml` (offline). Scratch: `/home/claude/bangkok3/scratch/PXD063171/`.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` passes, both alone and with `--template ms-proteomics` and `--template vertebrates` run separately. Ontology validation was skipped because the OLS extras are not installed, so this is a structural pass only.

## What would unblock "annotated"
- RAW headers (sample name or vial) for the D14 and D7_G4 files, or `filelist_skyline.txt`.
- Author confirmation of the G1-G4 code key.

## Review status
pending
