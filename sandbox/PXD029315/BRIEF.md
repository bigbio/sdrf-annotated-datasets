# PXD029315 SDRF annotation report

## Study
Proteomic response to cytotoxicity of methylglyoxal (PX title "...methylglyoxall"). Paper: "Studies of Glyoxalase 1-Linked Multidrug Resistance Reveal Glycolysis-Derived Reactive Metabolite, Methylglyoxal, Is a Common Contributor in Cancer Chemotherapy Targeting the Spliceosome", Front Oncol 2021, doi:10.3389/fonc.2021.748698, PMC8591171. The paper's Data Availability cites PXD029315 (verified); the PX record itself still says "publication pending".

## Scope, evidence and decisions
sandbox: 18 rows (18 RAW, label-free), templates ms-proteomics + human + cell-lines.

- Deposited (PROXI full record, 2026-11-27): 18 `.raw` (OT_181023_56_MS18-194_{MC,MM,MIMC,MIMM}{1-3}, OT_181113_56_MS18-194_{NC,NM}{1-3}) + 18 Mascot `.dat`. Annotated: 18/18 RAW. `.dat` files are search outputs, not rows.
- Stated (paper Methods): HEK293 (ATCC CRL-1573), DMEM 4.5 g/L glucose + 10% FBS; 131 uM MG for 6 h vs untreated; subcellular extracts (cytoplasm, nuclei, mitochondrial matrix+intermembrane space, mitochondrial membranes) from 3e6 cells; 3 independent biological replicates; DTT reduction, iodoacetamide alkylation, Lys-C then trypsin; label-free nanoLC-Orbitrap Fusion; Mascot 2.5.0, 5 ppm / 0.8 Da, carbamidomethyl-Cys, MG-H1, Met sulfoxide; Progenesis QI.
- INFERRED file-code key (no legend in paper, supplement text or PX record): trailing digit = biological replicate; last letter C = control, M = MG-treated; prefix N = nuclei, MIM = mitochondrial matrix + intermembrane space, M = mitochondrial membranes. Under this reading the cytoplasm extract (the paper's main dataset, 4091 proteins) is NOT deposited. Run dates support prefix = compartment (N runs on 2018-11-13, others 2018-10-23). The alternative (prefix M = cytoplasm, mitochondrial membranes not deposited) cannot be excluded. The compartment is encoded in source name only (no licensed characteristics column for subcellular fraction).
- Cell line: Cellosaurus CVCL_0045 (female, fetus, fetal kidney UBERON:0002113). Paper does not say whether proteomics used parental, empty-vector or Glo1+ HEK293; annotated as HEK293.
- MG-H1 = UNIMOD:859 on R, Variable; oxidation Variable; carbamidomethyl Fixed (fixed/variable status INFERRED from standard practice, Mascot .dat not readable today).
- Instrument Orbitrap Fusion: PX and paper agree; RAW headers not read (PRIDE FTP and API returned upstream connection errors).

## Values left not available / not applicable
- cell type: not available (Cellosaurus gives no cell type for HEK293).
- age, ancestry category: not available (fetal donor, not stated).
- dissociation method: not available (paper defers to Irshad et al. Sci Rep 2019; that paper could not be fetched: PMC captcha, Europe PMC error). 0.8 Da fragment tolerance suggests ion-trap CID, not asserted. Collision energy, MS1 range omitted for the same reason.
- Accessions: UNIMOD:859 verified live in OLS; Lys-C MS:1001309, MS:1002416, DTT/IAA PRIDE terms taken from repository usage because OLS rate-limited (validator cache only).

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics --template human --template cell-lines`: no errors. `sdrf_review.py`: [OK].

## Review status
pending
