# PXD050494 SDRF annotation report

## Study
Coexistence of Klebsiella pneumonia biofilms with Candida albicans in an acute pneumonia. Phuengmaung P et al., Int J Mol Sci 2024;25(22):12157, DOI 10.3390/ijms252212157, PMID 39596223. The PMCID was not resolved: Europe PMC was rate-limited, and the MDPI page shows none.

## Scope, evidence and decisions
Status: **sandbox**. 135 rows (45 RAW x 3 dimethyl labels) x 32 columns. Template: `ms-proteomics` v1.1.0.

**Deposited vs annotated.** The PX record (proteomecentral PROXI, accession verified) and the OmicsDI mirror of the PRIDE record agree on 95 files:
- 45 `.raw` files, `Biofilm_S{1-5}F{1-7,9,10}.raw`. F8 is absent in every set.
- 45 `.mgf` files with the same stems.
- 5 `.msf` files, `Biofilm_S{1-5}F.msf`.

All 45 RAW are annotated, each with the 3 label channels. The mgf and msf files are derived files and are not rows. The PRIDE v3 API and the PRIDE FTP/HTTPS mirror returned "upstream connect error" today, and the shell has no internet. So **no RAW header or `.msf` was read**.

**Channel map (STATED).** The PRIDE sample protocol, read via OmicsDI `ws/dataset/pride/PXD050494.json`, gives the map. Biofilms of three groups were labelled light, medium and heavy, "respectively":
- KP clinical isolate → light (CH2O/NaBH3CN), `DIMETHYL0`
- KP from ATCC → medium (CD2O/NaBH3CN), `DIMETHYL4`
- KP co-cultured with C. albicans → heavy (13CD2O/NaBD3CN), `DIMETHYL8`

The peptides were pooled and fractionated with a high-pH RP kit (PRIDE:0000564). Biofilms were grown 72 h, extracted in 8 M urea with sonication, and digested in solution.

**Search and acquisition (STATED, PRIDE data protocol).**
- Instrument: EASY-nLC1000 + Q-Exactive Orbitrap Plus. MS1 at 70k, 350–1400 m/z. Top-10 DDA, MS2 at 17.5k. HCD NCE 32%.
- Software: PD 2.1, SEQUEST-HT. Databases: C. albicans SC5314 plus K. pneumoniae MGH 78578.
- Enzyme: trypsin, 2 missed cleavages. Tolerances: 10 ppm / 0.02 Da.
- Fixed modifications:
  - carbamidomethyl C (UNIMOD:4)
  - light, medium and heavy dimethyl on K and N-term, at 28.031300, 32.056407 and 36.075670 Da. These are UNIMOD 36, 199 and 330, checked against unimod.org. The heavy +36.0757 label is UNIMOD:330, not 510.
- Variable modification: oxidation M (UNIMOD:35).

As in PXD046383 (same lab and pipeline), each row carries only its own label's dimethyl term.

**Sets → biological replicate (INFERRED).** S1–S5 are taken as biological replicates 1–5, one triplex set each, with one `.msf` per set. **Conflict:** the protocol says "across all 3 biological replicates", but five sets are deposited. It cannot be settled without the msf files or the authors.

**Organism / co-culture.** One `characteristics[organism]` column = Klebsiella pneumoniae (NCBITaxon:573) on all rows. This follows the PXD035814 precedent: one value, co-culture flagged as sandbox. KP is the labelled and analysed organism in all three channels; the reported ratios are KP protein ratios. The heavy channel also contains C. albicans (NCBITaxon:5476), and the search included its proteome. This is recorded in `source name` and `characteristics[treatment]`, not as a second organism.

The PX record registers **only** C. albicans, which is wrong for 2/3 of the samples. The spec allows repeated columns for multi-value fields, but `characteristics[organism]` is not declared multiple-cardinality. A repeated organism column for the heavy rows (the alternative: second column `Candida albicans` on co-culture rows, `not applicable` elsewhere) is left for curator decision.

**Other columns.**
- `characteristics[strain or breed]` was not used, because no declared template licenses it. Strain context ("clinical isolate", "ATCC strain") is in `treatment`.
- `material type` = whole organism. These are biofilms of unicellular microbes. Attack if `cell` is preferred.
- Reduction/alkylation (DTT/IAA): this is stated only by reference. The paper says extraction followed ref [25] (Phuengmaung 2022, IJMS 23:9202), which uses DTT/IAA. The fixed Carbamidomethyl in the search is consistent.

## Values not available / not applicable
- `organism part` and `disease` are not applicable: these are in-vitro microbial biofilms, and no host tissue was analysed.
- The ATCC strain number for the medium channel is unstated:
  - the paper's DB names "ATCC13833" [sic, probably 13883];
  - the protocol's DB names ATCC 700721/MGH 78578;
  - neither is said to be the cultured strain.

  It is therefore not encoded.

## Conflicts
1. **Instrument.** PX `instruments` says Q Exactive HF (MS:1002523). Both the PRIDE data protocol and the paper Methods say Q-Exactive Orbitrap Plus. Written as **Q Exactive Plus (MS:1002634)**, by Methods > PX fields. The RAW header is unread, which is the deciding source and is open.
2. **Groups.**
   - The paper's proteomics compares KP biofilm vs **planktonic** KP (Fig. 2) and KP+CA vs KP biofilm (Fig. 3). The paper does not mention dimethyl labelling or an ATCC arm.
   - The deposit protocol compares clinical KP and KP+CA against **KP_ATCC**.

   The deposit's own protocol is used, because it is the only source that maps labels to groups. A planktonic arm may instead sit in one channel. This is open.
3. **Replicates:** 3 stated vs 5 sets deposited (see above).
4. **Database:** the paper lists KP Swiss-Prot only (509 proteins). The protocol lists C. albicans (1,143) plus KP MGH 78578 (715). This does not affect SDRF columns.

## Stated vs INFERRED
- STATED (PRIDE protocol): label → group map, mods, tolerances, enzyme, HCD 32%, scan range, fractionation kit, instrument (also in the paper).
- INFERRED: set = biological replicate; fraction identifier taken from the `F<n>` file suffix; DTT/IAA via ref [25]; KP+CA strain identity (clinical isolates, per paper §4.1).

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics`: "Everything seems to be fine". **Caveat:** in this environment parse_sdrf reported that ontology validation was unavailable (OLS dependencies missing), so only structural checks ran.

All accessions were therefore checked live by other routes, because EBI OLS was down:
- NCBITaxon 573/5476: NCBI eutils
- UNIMOD 4/35/36/199/330: unimod.org
- MS:1002634/1000422/1001251: ontobee
- PRIDE:0000564/0608/0599/0627: pride_cv.obo on GitHub

Evidence files are in the private scratch directory, `bangkok3/scratch/PXD050494/`.

## Review status
pending
