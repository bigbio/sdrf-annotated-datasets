# PXD084067 SDRF annotation report

## Study
Type III CI Factors from wAlbB Induce Cytoplasmic Incompatibility via a Host Modification Mechanism.
Hou X, Goh FG, Liu S, Liu Y, Yong XE, Lin Q, Cai Y. PLoS Pathog 2026;22(10):e1014760,
doi:10.1371/journal.ppat.1014760, PMID 42956080 (CC-BY, read on journals.plos.org; no PMCID yet).
The paper's Data Availability statement and its Methods both cite PXD084067, so the PX publication link
is correct (checked per the bangkok-3 lesson about mislinked papers).

## Scope, evidence and decisions
Status **sandbox**: 6 rows (6 `.wiff` runs, label-free DDA), 34 columns.
Templates declared on every row: `ms-proteomics` v1.1.0 + `invertebrates` v1.1.0.

- **Deposited vs annotated (re-derived, not taken from the cache).** The ProteomeCentral PROXI record
  (`resultType=full`, Page URL verified to carry PXD084067) lists 15 files: 6 `.wiff`, 6 matching
  `.wiff.scan`, and 3 PEAKS `ProteinSummary` xlsx files
  (`2403S12_ProteinSummary_PEAKS_C.xlsx`, `2404S12_ProteinSummary_PEAKS_C2C3.xlsx`,
  `2406S05_ProteinSummary_PEAKS_T-W1W2W3.xlsx`). A `.wiff` plus its `.wiff.scan` is one run, so the
  deposit holds **6 runs**, matching the campaign cache (6 runs / 15 files, TripleTOF 6600). All 6 are
  annotated; none excluded. `comment[data file]` carries the `.wiff` name, with the `.wiff.scan`
  companion implied, as in the campaign's other SCIEX datasets.
  The PRIDE v3 API and the PRIDE FTP folder (`.../2026/10/PXD084067/`) both failed today with upstream
  connect errors, so the file list rests on PROXI alone and no deposited submitter metadata file or
  PEAKS result header could be inspected.
- **Samples (paper Methods + Results).** Testes and CI-arrested embryos from a stable
  wAlbB-transinfected *Aedes aegypti* line (cytoplasm transferred from *Ae. albopictus* eggs into
  *Ae. aegypti* eggs, then six further generations of self-crossing; "Stable strain was subjected to
  sample collection for proteomics analysis"). Fig 4F: both Cifs(wAlbB TIII) and Cifs(wAlbB TIV) are
  detected in wAlbB-infected *Ae. aegypti* testis among ~450 Wolbachia peptides; S1 Table is the list of
  Wolbachia proteins "detected in wAlbB-carrying mosquito testis **in all three replicates**".
  Fig 4G: eight Wolbachia polypeptides, none of them the Type III Cifs, in CI-arrested embryos
  "collected within 20 min after egg laying".
- **Run → sample mapping (INFERRED — the principal open point).** `240731_2406S05_T-W1/W2/W3` are mapped
  to the three wAlbB testis replicates, and `240401_2403S12_C`, `240508_2404S12_C2`,
  `240508_2404S12_C3` to the CI-arrested embryo samples. Evidence: the file-name tokens
  (`T-W` = testis, wAlbB; `C` = CI embryo), the 3-vs-3 split, the acquisition dates (the three T-W runs
  share one date and one PEAKS output, the C runs do not), and the paper's statement of exactly three
  testis replicates. The paper never gives run names, and never states how many embryo samples were
  analysed. There is no deposited sample sheet to confirm this, which is why the status is `sandbox`
  and not `annotated`.
- **Organism — `Aedes aegypti` (NCBITaxon:7159), against the PX record.** PX registers
  *Aedes albopictus* (NEWT:7160), but that species is only the source of the cloned `cifs` genes and of
  the transferred cytoplasm; the Methods say the *cifs* were "cloned from *Aedes albopictus* mosquito".
  The material actually measured is *Ae. aegypti*: the mosquito-breeding, transinfection and proteomics
  sections all describe *Ae. aegypti*, and the PEAKS search used the *Ae. aegypti* reference proteome
  UP000008820 plus the wAlbB proteome UP000290937. Per the brief's precedence rule (paper Methods beat
  PX fields) the SDRF records *Ae. aegypti*. Wolbachia is recorded inside
  `characteristics[strain or breed]` rather than as a second organism, because these are single-host
  samples with an endosymbiont, not a two-organism co-culture.
- **Instrument and acquisition.** SCIEX TripleTOF 6600 (MS:1002533) — paper and PX agree, so no conflict
  to resolve; the `.wiff` headers were not read (no network to the FTP). EvoSep One, IonOpticks Aurora
  Elite SX C18, Whisper 40 SPD. DDA, top-50 precursors, charge 2–5; MS1 400–1600 m/z (250 ms),
  MS2 100–1800 m/z (50 ms), high-sensitivity mode; dynamic exclusion 15 s.
- **Search parameters (paper Methods; the deposited PEAKS xlsx could not be opened).** PEAKS Studio 11.5,
  trypsin, up to 3 missed cleavages, 15 ppm precursor / 0.05 Da fragment, 1% FDR.
  Fixed: "beta-methylthiolation" on cysteine = **Methylthio, UNIMOD:39** (verified live on unimod.org:
  description "Beta-methylthiolation", alternative description "MMTS") — deliberately *not*
  Carbamidomethyl, which the reflex annotation would have used.
  Variable: Acetyl (UNIMOD:1) with `PP=Any N-term` (the paper says "acetylation (N-term)", not protein
  N-term) and Oxidation (UNIMOD:35) `TA=M`.
- **Sample prep.** S-Trap Micro (Protifi) from 50 mM TEAB / 5% SDS lysate; 1 µg peptides per Evotip.

## Values left `not available` / `not applicable`, and why
- `characteristics[developmental stage]`: `embryo stage` for the embryo rows; **`not available`** for the
  testis rows — the paper gives the rearing protocol and a "day 3–5 post-emergence" age only for the
  blood-feeding step, never for the males whose testes were taken, so "adult" would be an assumption.
- `comment[reduction reagent]`, `comment[alkylation reagent]`: **`not available`**. The S-Trap paragraph
  names neither. The fixed Methylthio implies an MMTS-type alkylation, but the reagent itself is unstated
  and the brief forbids asserting an unstated reagent (silence is `not available`, not `not applicable`).
- `characteristics[disease]`: `not applicable` — Wolbachia carriage is an endosymbiosis, not a disease,
  and no disease is studied. (`invertebrates` makes this column required but allows the reserved word.)
- `characteristics[cell type]`: `not applicable` — whole dissected testes and whole embryos, not a
  sorted cell type.
- Embryo collection window ("within 20 min after egg laying") is **not** encoded in
  `characteristics[sampling time]`, whose format is a single number + time unit and cannot express an
  interval of that kind without inventing a point value.
- Sex is not encoded: no declared template licenses `characteristics[sex]` (it is a `human`/`vertebrates`
  column), and declaring one of those templates would conflict with `invertebrates`, which is mutually
  exclusive with them. Testis implies male, and that is stated here instead.
- `comment[fraction identifier]` = 1 and `comment[technical replicate]` = 1 on every row: single
  injection per sample, no fractionation described. (source name, biological replicate, technical
  replicate, fraction) is therefore unique across the file.

## Stated vs INFERRED
- **Stated:** organism of the measured material; transinfected wAlbB line; testis and CI-arrested embryo
  as the two sample types; three testis replicates; instrument; LC and MS acquisition settings; enzyme,
  missed cleavages, tolerances, FDR; the three search modifications; S-Trap prep.
- **INFERRED:** which `.wiff` file is which sample (file-name tokens + PEAKS output grouping);
  that the three `C*` runs are three biological replicates numbered 1–3 in file order;
  that the CI-arrested embryos came from wAlbB-carrying males crossed to uninfected females (this is
  what "CI-arrested" means and what the Discussion implies, but the mosquito cross is not written out in
  the Methods); `beam-type collision-induced dissociation` and `time-of-flight` as the TripleTOF's
  fixed fragmentation and MS2 analyser (not stated in the paper, as in the campaign's other SCIEX files).

## Conflicts found and how resolved
1. **Species.** PX `species` = *Aedes albopictus*; paper = *Aedes aegypti* material. Resolved for the
   paper (see above); documented so a reviewer can attack it.
2. **Modifications.** PX `modifications` = "No PTMs are included in the dataset"; the paper lists one
   fixed and two variable modifications. Resolved for the paper, per the known unreliability of that PX
   field. The authoritative source would have been the deposited PEAKS output, which was unreachable.

## Validation
`parse_sdrf validate-sdrf --sdrf_file PXD084067.sdrf.tsv --use_ols_cache_only --template <t>` run once
per declared template (`ms-proteomics`, `invertebrates`): "Everything seems to be fine. Well done." in
both cases, no errors and no warnings. Both templates are declared on **all** rows, so the whole-file
BigBio gate applies cleanly: `python3 /home/claude/sdrf-annotated-datasets/.github/scripts/sdrf_review.py`
prints `[OK]` (1/1 clean, 0 with defects). Note that this `parse_sdrf` build reports
"Ontology validation is not available because OLS dependencies are not installed", so the clean pass is
structural only; every accession was checked by hand instead and the evidence is listed in
`/home/claude/singapore2/scratch/PXD084067/accession_checks.txt`.

## Evidence files (private scratch)
`/home/claude/singapore2/scratch/PXD084067/`: `px_files.txt` (PROXI payload, file list, PX fields),
`paper_excerpts.txt` (verbatim Methods and Results paragraphs), `accession_checks.txt` (ontology
verification), `build_PXD084067.py` (the builder that wrote the TSV).

## Review status
pending
