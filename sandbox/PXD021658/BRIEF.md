# PXD021658: sandbox status (not ready for datasets/)

**Why it is in sandbox:** Fails `parse_sdrf`: `comment[proteomics data acquisition method]` is `not available` on all 270 rows, but the ms-proteomics template requires a PRIDE:0000659 descendant. The data are MS1 full-scan only (chip-ESI method development) and no suitable term was identified. Independent review round 1 = FAIL (1 blocker, 4 important), unfixed.

## To resume
- Decide whether a defensible PRIDE:0000659 descendant exists for MS1-only acquisition; if not, this accession cannot be an ms-proteomics SDRF (do not claim DDA).
- Read `Metadata.xlsx` (deposited) and encode run conditions (stationary phase POROS R2/R3 vs LiChrosorb, flow rate 2-20 uL/min, injection volume, LC method) as characteristics/factors, and split source names by condition.
- Replace placeholder replicate numbers (the 141 BK/AngII runs are not technical replicates of one sample).
- Confirm the Hb source organism (currently Homo sapiens inferred from peptide sequences) from the paper (closed access) or use `not available`.
- Reconcile 191017_55-57 (labelled 10 um but in the 5 um date series); read more than the 12 of 270 RAW headers sampled; decide G2 vs G2 HDMS.
- Then a fresh adversarial review.

Files here: `PXD021658.sdrf.tsv` (current draft), `PXD021658.evidence.json` (evidence manifest: claim, source, confidence per field). The annotation report follows, written by the annotator from the NordicSDRF campaign (Odense/SDU datasets). Its 'Review status' section is the review log.

---

## PXD021658

"Thiol-ene microfluidic chip for fast on-chip sample clean-up, separation and ESI mass spectrometry of peptides and proteins" (Svejdal et al., Anal Chim Acta 2020, doi:10.1016/j.aca.2020.09.062). A method-development study: standard peptides/proteins run on a chip with on-chip RPC and ESI, Synapt G2, MS1 only. Not a conventional proteomics experiment.

## Templates
ms-proteomics v1.1.0 only. No organism template (samples are mostly synthetic-type standards of undefined organism), no cell-lines or clinical layers.

## Scope
Deposited: Metadata.xlsx and 4 zips of Waters .raw folders (PRIDE lists 5 files; pages 0-1 enumerated). Annotated: all 270 .raw folders found inside the zips (270 rows x 23 columns); Metadata.xlsx is the mapping. Nothing excluded.

## Key decisions
- Rows: one per .raw folder; 5 source groups (BK+AngII standard 141, Blank 116, Hb tryptic digest 6, GluFib standard 4, Protein mixture 3).
- Instrument: Synapt G2 MS (MS:1001778) from RAW headers; overrides PRIDE's generic Synapt MS. HDMS variant undetermined.
- Blanks: `negative control`, organism/part/cell type/disease not applicable; no reagents claimed.
- Hb digest: Trypsin; organism Homo sapiens inferred from human Hb peptide sequences (not stated).
- MS-only: dissociation, tolerances, modification parameters `not applicable`.
- Acquisition method: no PRIDE term fits MS1-only; DDA not used (it would be false). Written `not available`.

## Not available / not applicable
Acquisition method, organism part and cell type for Hb digest, disease for Hb digest. Everything else sample-side is not applicable.

## Conflicts
- reconcile `cleavage_agent_contradicted` (record names tryptic digestion): intentional, the digest applies to the 6 Hb rows only.
- PRIDE instrument Synapt MS vs RAW SYNAPT-G2: RAW used.

## Inferred vs stated
Inferred: Hb organism; replicate numbers (placeholders: biological replicate 1, technical replicate = run index within group). Stated: instrument, label free, sample ids, trypsin for Hb. Paper not read (closed access). Run-level conditions (stationary phase, flow rate, load, LC method) are not encoded.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only`, two runs, 3 messages on 2 issues: (a) `study sample` not in cache (artifact; PRIDE:0001013 exists live); (b) `not available` in the required acquisition-method column (real, unresolvable without a false value). `sdrf-tools structure` reports the same reserved-word issue; `check --offline` CLEAN. Terms resolved live in OLS4: MS:1001778, MS:1001251, PRIDE:0001013.

## Review status
Independent round 1 (fresh-context reviewer, sha256 c92af53b0fc12b5a3d12fa810859041048a73e2f50ad1542d89bdb9fac013c02) = FAIL, 1 blocker / 4 important. NOT FIXED, needs a decision. Blocker: `comment[proteomics data acquisition method]` is `not available` on all 270 rows, but the ms-proteomics template requires a PRIDE:0000659 descendant (`allow_not_available: false`), so the file fails `parse_sdrf`; the data are MS1 full-scan only and no suitable descendant was identified. Important: Hb organism (Homo sapiens, 6 rows) is inferred from peptide sequences, not stated; `study sample` fits calibrants/standards poorly; biological/technical replicate numbers are placeholders (the 141 BK/AngII runs span different columns, flow rates and methods); run conditions (stationary phase, flow rate, injection volume) live only in Metadata.xlsx and are not encoded as factors. Minor: Synapt G2 vs G2 HDMS undetermined; only 12 of 270 RAW headers sampled; 191017_55-57 label/folder mismatch; protein-mixture rows organism `not applicable`.
