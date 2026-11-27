# PXD015393 SDRF annotation report

## Study
Phosphoproteome profiling unravels rewiring of chromatin organization factors in host cells upon
HBV infection (Singapore; IMCB/A*STAR + NUS, submitter ZiJie Lim, lab head Jayantha Gunaratne).

Publication: Lim Z, Mohd-Ismail NKB, Png E, Sze CW, Lin Q, Hong W, Lim SG, Tan YJ, Gunaratne J.
*Phosphoproteomics Unravel HBV Triggered Rewiring of Host Phosphosignaling Events.*
Int J Mol Sci 2022;23(9):5127. PMID 35563518, DOI 10.3390/ijms23095127. Open access (MDPI HTML read
directly). The paper's Data Availability statement names **PXD015393** ("project DOI:
10.6019/PXD015393"), so the PX record's linked paper is the right one — checked because two
bangkok-3 records linked the wrong paper.

## Templates
`ms-proteomics` + `human` + `cell-lines` (all v1.1.0), declared on every row.
`human` is the sample layer required by `cell-lines` for a human-derived line; it licenses
`age`/`sex`/`ancestry category`/`individual`, `cell-lines` licenses `cell line`,
`cellosaurus accession`, `cellosaurus name`, `culture medium`, and `sample-metadata` (inherited)
licenses `treatment`, `enrichment process`, `disease`, `material type`, `cell type`.
Column set resolved with `spec/scripts/resolve_templates.py`
(scratch: `resolved_cols_ms-proteomics_human_cell-lines.txt`).

## Scope — deposited vs annotated
PROXI `datasetFiles` for PXD015393 lists **10 files: 6 `.raw`**, one `.pdAnalysis`
(`AWF_Fusion_TMT_MSASPS_Normalization_and_Scaling_phospho.pdAnalysis`), one `.mzid.gz`, one `.mgf`
and one `.mzML` (the latter three all named `TBP_F_P4_180506_Batch 4-7 TMT-phospho (full)`).
This matches the campaign cache (6 RAW / 10 files) and was re-derived from the PROXI record itself,
not taken from the cache.

**All 6 deposited RAW runs are annotated**, each as 10 TMT channels → **60 rows × 48 columns**.
No run is excluded. The non-RAW files are search output/peak lists, not acquisitions.

The 6 raw files:
`TBP_F_P4_180506_01_IS1153_MSA1.raw`, `…_02_IS1153_MSA2.raw`, `…_03_IS1153_MSA3.raw`,
`…_04_IS1153_MSA4.raw`, `TBP_F_P4_180509_06_IS1153_MSA_5.raw`, `TBP_F_P4_180509_07_IS1153_MSA_6.raw`.

## Channel map (STATED)
One TMT10plex set, 5 mock + 5 HBV-infected biological replicates. Methods §4.8, verbatim:
"(Mock: 126, 127N, 127C, 128N, 128C; HBV infected; 129N, 129C, 130N, 130C and 131)", consistent with
Figure 1 ("Five biological replicates for both mock and infected HepG2-NTCP").

| channel | condition | biological replicate |
|---|---|---|
| TMT126 / 127N / 127C / 128N / 128C | mock infection | 1 / 2 / 3 / 4 / 5 |
| TMT129N / 129C / 130N / 130C / 131 | HBV infection (MOI 3000, 7 dpi) | 1 / 2 / 3 / 4 / 5 |

Channel identities are stated; which *individual* replicate culture sits in which channel within a
condition is not stated, so the replicate numbering within each condition is a 1:1 convention
(it carries no cross-condition pairing).

Label values are the SDRF/PRIDE channel terms, verified live in `pride_cv.obo`
(TMT126 PRIDE:0000516 … TMT131 PRIDE:0000529) and matching sdrf-pipelines' TMT10plex channel map.

## Key values and their evidence (all STATED unless marked)
- Instrument `NT=Orbitrap Fusion;AC=MS:1002416` — PX record *and* paper ("Orbitrap Fusion Tribrid").
  No conflict; MS:1002416 verified in psi-ms.obo. The raw headers could not be range-read (no shell
  internet; EBI unreachable), so this rests on two agreeing secondary sources.
- Acquisition DDA (`PRIDE:0000627`); MSA SPS-MS3 TMT workflow ("Data-dependent MS2 and MS3 … were
  configured according to the MSA SPS MS3 method"), which also explains the `MSA` token in the run
  names and the `MSASPS` token in the `.pdAnalysis` name.
- Dissociation method `NT=CID;AC=MS:1000133` — MS2 is "CID OT … collision energy at 35% …
  isolation width 0.7 m/z"; the MS3 quantification scan is HCD at 65% ("HCD OT … isolation width
  2 m/z"). Only one dissociation-method column exists, so the identification-level MS2 method is
  recorded there and both energies are in `comment[collision energy]` = `35% NCE;65% NCE`
  (35% = CID MS2, 65% = HCD MS3). CID/HCD synonyms verified in psi-ms.obo.
- Scan ranges: MS1 `400m/z-1500m/z` (stated "400–1500 m/z at a resolution of 120K");
  MS3 `100m/z-500m/z` (stated).
- Enzymes: Lys-C 1:100 overnight then trypsin 1:50, 8 h → two `comment[cleavage agent details]`
  columns (`MS:1001309`, `MS:1001251`). The search section does not restate the enzyme; the wet-lab
  statement is used.
- Reduction 5 mM DTT, alkylation 10 mM iodoacetamide (both stated) → PRIDE:0000608 / PRIDE:0000599.
- Search (PD 2.2 / SEQUEST HT, 1% FDR): precursor 10 ppm, fragment 0.02 Da; fixed carbamidomethyl
  (C) and TMT10plex on K and peptide N-terminus (+229.163 → UNIMOD:737 TMT6plex, whose Unimod record
  states "Also applies to TMT10plex"); variable oxidation (M), phospho (S/T/Y), N-terminal acetyl.
  Every UNIMOD accession was verified on unimod.org in this run.
- Enrichment: Fe-NTA phosphopeptide enrichment kit → `characteristics[enrichment process]` =
  `enrichment of phosphorylated protein` (EFO:0010806, verified via Ontobee). Note the labelled
  peptides were **pooled before enrichment**, i.e. one enriched sample feeds all six runs.
- Cells: HepG2-NTCP from Dr Koichi Watashi; DMEM/F-12 GlutaMax + 5% heat-inactivated FBS, NEAA,
  pen/strep, L-glutamine, 5 µg/mL insulin, 500 µg/mL G418; HBV from Hep38.7 (tet-off), MOI 3000,
  24 h infection with PEG 8000/DMSO, harvest 7 dpi; mock = same procedure without virus.
- Donor characteristics `age 15Y`, `sex male` come from Cellosaurus for the parental Hep-G2
  (CVCL_0027), as does `organism part liver` (Cellosaurus: derived from liver, UBERON_0002107) and
  `disease hepatoblastoma` (MONDO:0018666, verified via Ontobee). Per the `cell-lines` template,
  `characteristics[disease]` is the disease of the tissue the line came from, so it is
  hepatoblastoma on every row and the infection lives in `treatment` / `factor value[treatment]`.

## INFERRED (not stated)
1. **The 6 runs are 6 technical replicates (repeat injections) of the single pooled, TMT-labelled,
   phospho-enriched sample**, numbered 1–6 in run order (MSA1…MSA4 acquired 2018-05-06, MSA_5/MSA_6
   on 2018-05-09), with `comment[fraction identifier] = 1` throughout. The Methods describe **no**
   fractionation (no high-pH RP, no SCX) and do not say how many injections were made; all six names
   share the same `TBP_F_P4` prefix and `IS1153` sample id, and the single deposited result set is
   one merged search. Nothing supports a fraction interpretation, but nothing states "technical
   replicate" either — this is the main reason the status is `sandbox` rather than `annotated`.
2. `characteristics[cell type] = hepatocyte` (CL:0000182) — conventional for HepG2-derived cells;
   not stated in the paper.
3. `NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable` — the paper says only "N-terminal
   acetylation (+42.011 Da)"; protein N-terminus is the Proteome Discoverer default. The deposited
   `.pdAnalysis` would settle it but was unreachable.
4. Within-condition replicate numbering (see channel-map note above).

## Values left `not available` / `not applicable`, and why
- `characteristics[cellosaurus accession]` and `[cellosaurus name]` = `not available`. The line is
  the Watashi HepG2-hNTCP-C4-type HepG2-NTCP; a live Cellosaurus query for "HepG2-hNTCP-C4" returns
  **0 records**, and the two existing HepG2 NTCP derivatives (CVCL_JY40 HepG2-hNTCP, Ni et al. 2014;
  CVCL_C9B9 HepG2-NTCP1) have different provenance, so assigning either would be wrong. The
  parental line is CVCL_0027 (used only as the source of donor age/sex/tissue, stated here, not in
  the accession field).
- `characteristics[ancestry category]` = `not available`. Cellosaurus records population
  "Caucasian" for Hep-G2; mapping that to a HANCESTRO term could not be verified live (OLS/EBI was
  down all through this run), and the paper says nothing.
- `characteristics[developmental stage]` = `not available` — nothing stated; the donor was 15 years
  old but no verified HsapDv term was obtainable offline.
- `characteristics[individual]` = `not applicable` — an immortalised cell line, no per-sample donor.
- Passage number, sample storage temperature, acquisition date columns: omitted (optional,
  unstated).

## Conflicts
None found: PX record and paper agree on instrument (Orbitrap Fusion), organism (Homo sapiens,
NCBITaxon 9606) and modification set (Phospho, TMT6plex, Oxidation, Acetyl, Carbamidomethyl).

## Sources checked and what failed
- ProteomeCentral PROXI `datasets/PXD015393?resultType=full` — OK (accession checked in the Page URL
  and the payload).
- PRIDE FTP directory `…/2022/06/PXD015393/`, PRIDE API v3 `files/all`, and OLS4 — **all unreachable**
  for the whole session (upstream connect error / connection timeout from the cloud browser, 403
  CONNECT from the shell proxy, robots-unreachable from WebFetch; retried ~6 times over two days).
  Consequence: the deposited `.pdAnalysis` (Proteome Discoverer study: would give the authoritative
  static/dynamic modification list, the enzyme, and possibly a per-run study-factor table) was never
  read, and the file list could not be cross-checked against PRIDE itself.
- Paper full text (MDPI HTML) including Methods §4.1–4.11, Figure 1 legend, Data Availability.
- Cellosaurus (web + API), Unimod record pages, PSI-MS CV, PRIDE CV, Ontobee (MONDO/CL/EFO/NCIT).

## Validation
`parse_sdrf validate-sdrf --sdrf_file annotations/PXD015393.sdrf.tsv --use_ols_cache_only
--template <t>` for each of `ms-proteomics`, `human`, `cell-lines`: "Everything seems to be fine."
Ontology validation was *not* exercised (the installed sdrf-pipelines lacks the optional ontology
extra, so it ran structural checks only) — every CV term in the file was therefore verified by hand
against the live sources listed above.
BigBio CI gate `python3 .github/scripts/sdrf_review.py annotations/PXD015393.sdrf.tsv` → `[OK]`.
Uniqueness of (source name, biological replicate, technical replicate, fraction) and of
(source name, assay name, label) is asserted in the build script.

## Judgement calls a reviewer should attack hardest
1. 6 runs = technical replicates 1–6 vs. unstated fractions (see INFERRED 1).
2. `cell line = HepG2-NTCP` with `cellosaurus accession = not available` instead of forcing
   CVCL_JY40/CVCL_C9B9 or the parental CVCL_0027.
3. `disease = hepatoblastoma` on all rows (cell-line-of-origin reading of the column) with infection
   expressed only as treatment/factor.
4. Single dissociation-method column = CID (MS2) with `35% NCE;65% NCE` carrying the MS3 HCD energy.
5. `cell type = hepatocyte` and the Acetyl `PP=Protein N-term` default.

## Review status
pending
