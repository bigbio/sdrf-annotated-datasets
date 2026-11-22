# PXD046423: sandbox status (not ready for datasets/)

**Why it is in sandbox:** Independent review round 2 = FAIL; the findings were fixed afterwards (variant reverted to `wild type`, Lys-C column, `factor value[RBD variant]`) but the fixed file has not been re-reviewed.

## To resume
- Resolve the RBD variant conflict: file names and the PRIDE description say wild type (WT), while the PRIDE sample protocol, Experimental_setup.docx and the abstract say Alpha. Read the full paper (PMID 38499233) or ask the authors; update `characteristics[RBD variant]` and `factor value[RBD variant]` together.
- Decide organism for the 72 common-channel rows (currently `not applicable`; the pool holds RBD plus mouse antibody) and consider declaring the vertebrates template.
- The modification list is a union over three search rounds; check per-search settings (msf tolerance 20 ppm/0.5 Da vs PRIDE 10 ppm/0.1 Da).
- Request a fresh adversarial review (round 3).

Files here: `PXD046423.sdrf.tsv` (current draft), `PXD046423.evidence.json` (evidence manifest: claim, source, confidence per field). The annotation report follows, written by the annotator from the NordicSDRF campaign (Odense/SDU datasets). Its 'Review status' section is the review log.

---

## PXD046423 SDRF annotation report

## Study
Larsen et al., "Epitope mapping of SARS-CoV-2 RBDs by hydroxyl radical protein footprinting reveals the importance of including negative antibody controls" (Biochim Biophys Acta Proteins Proteom 2024, PMID 38499233, doi 10.1016/j.bbapap.2024.141011). Recombinant SARS-CoV-2 RBD (two variants) and a mouse anti-RBD monoclonal antibody (20-14-5) or a non-binding anti-PAD4 control antibody were labelled by Fenton chemistry (0, 3, 9 min), digested (PNGaseF, LysC, methylated trypsin), TMT-labelled (10 tags + common channel) and run on an Orbitrap Exploris 480 (DDA, HCD, 60 min gradient). The paper is not open access (not in Europe PMC full text); the PRIDE record, the deposited Experimental_setup.docx, the .msf files and RAW headers were used.

## Templates
ms-proteomics v1.1.0 only. No organism template: the samples are recombinant proteins (SARS-CoV-2 RBD) and a mouse antibody in a tube, with no animal, tissue, strain, sex or age, so `vertebrates`/`human` would only add not-applicable columns. No cell-line, clinical or DIA template applies.

## Scope: deposited vs annotated
Deposited: 147 files (all 3 pages of 100/47 read): 72 RAW, 72 Proteome Discoverer .msf, 2 .pdResult, 1 Experimental_setup.docx. Annotated: all 72 RAW x 10 TMT channels = 720 rows x 42 columns. Search outputs are not annotated as data rows. Groups (RAW): WT/Delta x anti-RBD ("Sample") / anti-PAD4 ("Control") x BRep 1-3 x technical injections T1-T6 (WT Sample BRep2 additionally T7; Delta Sample BRep3 has only T1-T5 RAW, although a T7 .msf is deposited whose RAW is not).

## Key decisions
- Channel to sample map: read from the StudyDefinition XML inside all 72 deposited .msf files (first 700 kB of each by HTTP range read). It is identical in every file: 126 = common channel (Sample_Type_Mix "Control"), 127N antibody 3 min, 127C antibody 9 min, 128N RBD 0 min, 128C RBD 3 min, 129N RBD 9 min, 129C RBD+antibody 0 min, 130N RBD+antibody 3 min, 130C RBD+antibody 9 min, 131 antibody 0 min. Biological replicate and sample name (Sample_RBD/Control_RBD) factors in the msf agree with each RAW file name. Paper/PRIDE protocol: 10 tags of an 11plex, one common channel with 1.5 ug of each sample.
- Source = variant x antibody arm x composition x time x biological replicate (120 sources). The same source is measured in T1-T6 (six technical injections of one TMT tube, each own RAW); comment[technical replicate] = the T number in the file name, fraction identifier = 1 (no fractionation: each RAW is a replicate injection, not a fraction).
- Common channel: one source per (variant, arm, biological replicate) tube; sample type `reference`, biological replicate `pooled`, pooled sample `pooled`.
- Organism: antibody-only = Mus musculus; RBD-alone and RBD+antibody = Severe acute respiratory syndrome coronavirus 2 (the epitope-mapped protein; the mixture also contains mouse antibody but the column is single-valued). Common channel: not applicable.
- Factor values: sample composition, antibody, sampling time (time of hydroxyl radical labelling; 0 min is the unlabelled negative control). Custom characteristics columns added: sample composition, antibody, RBD variant (not in the contract).
- Instrument: Orbitrap Exploris 480 from RAW header and paper, overriding PRIDE's structured "Q Exactive HF". Also overridden: PRIDE organism list is correct but lists no disease/organism part (not applicable here).
- HCD, NCE 30, MS1 350-1500, MS2 Orbitrap resolution 45000 and 120000 MS1: RAW header (one WT and one Delta file; identical).
- Modifications: the union of those named in the PRIDE data processing protocol (Mascot rounds 1 and 2, Sequest HT round): Deamidated N,Q; Oxidation D,F,H,K,M,N,P,Q,R,S,T,W,Y; Dioxidation M,W; Trioxidation F,W,Y; Carbonyl A,E,I,L,P,Q,R,S,V (all variable), plus Carbamidomethyl C (IAA alkylation, paper) and TMT6plex K/N-term fixed (msf label method; TMT6plex mass is used for the 10plex tags, as deposited). Per-round modification sets differ; the union is written because the SDRF is file-level.
- Cleavage agent Trypsin (record: LysC and methylated trypsin, PNGaseF; msf enzyme node "Trypsin (Full)"). LysC is not representable in the single-valued column.

## Values left not available / not applicable
organism part, disease: not applicable (recombinant proteins). Antibody not applicable for RBD-alone; RBD variant not applicable for antibody-alone. No reserved word `not available` is used.

## Conflicts
- Search tolerances: PRIDE protocol says 10 ppm / 0.1 Da; the one workflow node readable in the first 700 kB of the msf shows 20 ppm / 0.5 Da. PRIDE text used (the msf node could be a recalibration/first-pass step; the full workflow was not read).
- Variant name: RAW names say "WT" and the paper title/description say wild type, but the PRIDE sample protocol says "RBD Alpha". Re-annotated as `Alpha (B.1.1.7)` after review: the PRIDE sample protocol, the deposited Experimental_setup.docx and the Europe PMC abstract (Alpha and Delta) all say Alpha; only file names and the PRIDE project description say wild type/WT (source names keep the file-derived `WT`).
- `reconcile` BLOCKER cleavage_agent_unsupported is a false positive: the record names "methylated trypsin (methylated in-house)" and the msf enzyme is Trypsin.
- PRIDE says "six technical triplicates"; the files show T1-T6 injections (T7 extra for one tube).

## Inferred vs stated
Stated (deposited file or record): channel map (msf), tolerances, mods, instrument, HCD/NCE 30 (RAW), reduction DTT, alkylation IAA. Inferred: that channel 126 labelled "Control" in the msf is the common channel (consistent with the 10 channels = 9 conditions + 1 common channel in the protocol; the msf does not name it); the common-channel source granularity (per tube); the channel map for WT Sample BRep2 T7 (its .msf is not deposited; same tube as T1-T6); the single organism value for mixtures; the missing BioRep factor on channel 131 in the msf (taken from the file name, same tube); source and custom column names; Delta/WT per-round modification union.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` (one round): only error is "Term: study sample ... not found in the given ontology list pride", the known cache artifact (PRIDE:0001013 resolves live in OLS4; kept). `reconcile`: one false positive (above). All 14 NT/AC terms resolved against live OLS4 (HCD = beam-type collision-induced dissociation MS:1000422, Orbitrap = orbitrap MS:1000484, labels match); `reference` = PRIDE:0000899, `study sample` = PRIDE:0001013.

## Review status
Independent round 1 (fresh-context reviewer, sha256 8b7258989e51ca0ebc280f430556793ae83020b47bfbc0102e4e19ebdcc8e5d8) = FAIL, 2 important. (1) `characteristics[RBD variant]` said `wild type`, but the PRIDE protocol, Experimental_setup.docx and the abstract say Alpha: changed to `Alpha (B.1.1.7)` on the 36 WT-file groups. (2) RBD variant had no factor value: added `factor value[RBD variant]`. Also added the Lys-C `comment[cleavage agent details]` column (minor 3). File mapping 72/72 RAW, channel map consistent. `tools check` flagged 3 UNIMOD terms (425, 345, 1918) that resolve live. Minor not changed: vertebrates template not declared for the antibody rows; common-channel organism `not applicable`. Round 2 (fresh-context reviewer, sha256 603101c6f3af1b4078fce97b20f7760f083d00418d85dab58a1e89cb9a238ae3) = FAIL, 2 important: `Alpha (B.1.1.7)` was unsupported (no source cites a lineage; file names and the PRIDE description say wild type) and evidence.json was stale on Lys-C. Fixed: variant reverted to `wild type` in characteristics and factor columns, evidence.json updated with the conflict and the Lys-C column. Round 3: pending
