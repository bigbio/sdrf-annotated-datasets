# PXD043870 SDRF annotation report

## Study
Role of Rab11 in Enterovirus A71 (EV-A71) infection — RAB11A co-immunoprecipitation / mass spectrometry
in human neuroblastoma SH-SY5Y cells (Ng QY et al., "Enterovirus-A71 exploits RAB11 to recruit chaperones
for virus morphogenesis", J Biomed Sci 31:65, 2024, DOI 10.1186/s12929-024-01053-2, CC-BY).
The paper's Methods ("Co-IP/mass spectrometry") cites PXD043870 explicitly, so the PX-linked publication
is confirmed as the right paper. Submitter Qing Yong Ng, lab head Sylvie Alonso (NUS, Singapore).

## Scope, deposited vs annotated
Deposited (PRIDE FTP 2024/06/PXD043870, re-derived today; matches the campaign cache of 12 RAW / 16 files):
12 Thermo `.raw` (770–966 MB) + 4 `*_MASCOT_ProteinSummaryStat.DAT` exports. All 12 raw runs are annotated
(12 rows); the 4 Mascot exports are search outputs, not runs, so they get no row.

Four pull-down conditions × three runs each, from the file names and the paper's Co-IP/MS design:
- `220712_EV71_AntiRab11a_01..03`  — EV-A71-infected lysate, anti-RAB11A bait
- `220712_EV71_IgG_01..03`         — EV-A71-infected lysate, IgG isotype control
- `220712_Uninfected_AntiRab11a_01..03` — uninfected lysate, anti-RAB11A bait
- `220712_Uninfected_IgG_01..03`   — uninfected lysate, IgG isotype control
This bait/control mapping is STATED: the Methods normalise each protein's emPAI against "the corresponding
IgG isotype control sample" and against RAB11A pulled down by the anti-RAB11A Co-IP, and Fig. 7's legend
states "SH-SY5Y cells were infected with EV-A71 S41 (MOI 0.1). At 24 h.p.i, cell lysates were pulled down
with antiRAB11A antibody." One Mascot summary file exists per condition, matching the four conditions.

## Templates
`ms-proteomics` + `human` + `cell-lines` (v1.1.0), declared on every row (whole-file CI gate satisfied).
`characteristics[enrichment process]`, `[treatment]`, `[culture medium]`, `[sampling site]`,
`[cellosaurus accession/name]`, `[age]`, `[sex]` are all licensed by these three.

## Key decisions and evidence
- STATED (paper Methods): SH-SY5Y human neuroblastoma cell line; DMEM + 10% FBS, 37 °C, 5% CO2;
  EV-A71 S41 (sub-genotype B4, GenBank AF316321) at MOI 0.1, harvested 24 h.p.i.; Dynabeads-coupled
  antibody Co-IP, elution in Laemmli buffer; SDS-PAGE (8–20 % gradient), bands excised, in-gel trypsin
  digestion; Dionex Ultimate 3000 RSLCnano, 60-min gradient; Proteome Discoverer 1.4 → mgf → Mascot.
- STATED (Cellosaurus CVCL_0019, verified live today): SH-SY5Y, female, 4Y donor, neuroblastoma,
  derived from metastatic bone marrow → `characteristics[sampling site] = bone marrow`.
- `comment[fraction identifier] = 1/2/3` with `comment[fractionation method] = NT=SDS PAGE;AC=PRIDE:0000568`:
  INFERRED. The three runs per condition correspond to the excised gel bands of one lane (in-gel digestion
  is stated, and the four deposited Mascot summaries are one merged result per condition, not per run).
  The suffixes `_01/_02/_03` are never defined by the paper or by any deposited metadata; they could
  instead be technical replicates. This is the single most attackable call in the file.
- `comment[instrument]`: CONFLICT. The paper Methods say a **Q Exactive** (MS:1001911); the PX/PRIDE record
  says **Q Exactive HF** (MS:1002523). Precedence (raw > paper > PX) could not be exercised: the shell has
  no network and the browser cannot range-read an 800–900 MB `.raw` header, so the raw headers are unread.
  Paper Methods therefore win; flagged here.
- `comment[modification parameters] = Carbamidomethyl UNIMOD:4 TA=C MT=Fixed`: from the PX record's
  declared modification MOD:00397 (iodoacetamide derivatized residue). The deposited `.DAT` exports are
  protein-summary tables only (no enzyme, tolerance or modification block), so no deposited search output
  overrides it. Cleavage agent Trypsin (MS:1001251) is stated ("in-gel trypsin digestion").
- `comment[label] = label free sample` — no labelling anywhere in the workflow (emPAI-based comparison).
- `comment[proteomics data acquisition method] = Data-dependent acquisition (PRIDE:0000627)`: INFERRED from
  a Q Exactive + Mascot/mgf workflow; the paper does not name DDA explicitly.
- `characteristics[biological replicate] = 1` for all rows: a single Co-IP/MS experiment is described
  (one acquisition date token `220712`, one Mascot result per condition); no replicate structure is stated.
- Organism = `Homo sapiens` only. The PX record also lists Enterovirus A71 (NCBITaxon:39054), but the
  deposited Mascot results are human-only hits (`OS=Homo sapiens` throughout), and infection is carried by
  `characteristics[treatment]` / `factor value[treatment]` instead of a second organism row.

## Values left reserved, and why
- `characteristics[organism part]`, `[cell type]`, `[material type] = cell line`: cultured cell line, no tissue;
  organism part and cell type set `not applicable` (sampling site carries the donor site).
- `characteristics[developmental stage]`, `[ancestry category]`, `[individual]`: `not available` — the
  4-year-old donor's stage/ancestry are not stated by the paper and Cellosaurus gives only age and sex.
- `comment[precursor mass tolerance]`, `[fragment mass tolerance]`, `[dissociation method]`,
  `[reduction reagent]`, `[alkylation reagent]`: `not available` — the Mascot search parameters are not
  deposited (the `.DAT` files are protein summaries) and the paper states none. Per the brief, silence about
  the alkylation reagent is `not available`, not `not applicable`, even though the PX record implies IAA use.

## Conflicts
1. Instrument: paper Q Exactive vs PX Q Exactive HF (unresolved, see above).
2. PX species list includes Enterovirus A71 while the deposited search is human-only (resolved in favour of
   the deposited search output).

## Stated vs inferred summary
STATED: file list, bait/control mapping, cell line and medium, virus strain/MOI/timepoint, trypsin,
SDS-PAGE in-gel digestion, label-free, donor sex/age/disease/site.
INFERRED: `_01/_02/_03` = gel fractions, DDA, Carbamidomethyl (from PX modification field), instrument choice.

## Status
`sandbox` — validates and every run is mapped, but the run-suffix semantics (fraction vs technical replicate)
and the instrument model are not resolvable from stated evidence.

## Validation
`parse_sdrf validate-sdrf --sdrf_file PXD043870.sdrf.tsv --use_ols_cache_only --template ms-proteomics
--template human --template cell-lines` → "Everything seems to be fine." (ontology validation unavailable in
this container: the sdrf-pipelines ontology extra is not installed, so the pass is structural only).
BigBio gate `sdrf_review.py PXD043870.sdrf.tsv` → `[OK]`.
OLS4 (`ols4/api/search`) returned upstream connection errors for every query this run, so MS/PRIDE/UNIMOD
accessions were cross-checked against reviewed campaign SDRFs; Cellosaurus CVCL_0019 was verified live.

## Review status
pending
