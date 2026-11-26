# PXD017251 SDRF annotation report

## Study
Deep Characterization of the IFN-I/III-Stimulated Proteome in HBV-Transfected or Native HepG2 Cells. Paper: Hodge K, Makjaroen J, Robinson J, Khoomrung S, Pisitkun T., ACS Omega 2020 5(27):16796-16810, doi:10.1021/acsomega.0c01865, PMID 32685848, PMC7364717 (OA full text read through the PMC HTML).

**Status: sandbox.** The SDRF validates. Two material points are INFERRED (see below): which file series is which experiment, and the dimethyl channel→sample map.

## Scope, evidence and decisions
The SDRF has 240 rows: 95 RAW files. 50 are 3-plex, giving 150 rows, and 45 are 2-plex, giving 90 rows. It has 42 columns. Templates: ms-proteomics, human and cell-lines (all v1.1.0).

**Deposited vs annotated.** The PX/PRIDE record holds 210 files: 95 `.raw`, 95 `.mgf`, 10 `.msf` and 10 `.pdResult`. All 95 RAW files are annotated. None is excluded. They fall into two series:
- `OffFeb2017S{1-5}F{1-10}.raw` (50 files): 5 sets × 10 high-pH fractions.
- `HepG2_MAL_Set{1-5}_F{1-9}.raw` (45 files): 5 sets × 9 fractions. `Set5_F2` carries the suffix `_180221051034`.

The `.mgf`, `.msf` and `.pdResult` files are derived outputs and are not listed as data files. The file names were checked against the full expected grid, and against the PRIDE HTTPS directory listing.

**Design (STATED, paper).** The study ran two new dimethyl-labelling experiments, each with five biological replicates:
1. HepG2 untreated vs IFN-α2a vs IFN-λ3. Both IFNs were at 100 ng/mL for 24 h. IFN-α2a was PBL 11100-1 and IFN-λ3 was R&D 5259-IL-025.
2. HepG2.2.15 vs parental HepG2. The ratio is HepG2.2.15/HepG2.

The paper's third experiment (HepG2.2.15 ± IFN) is earlier data from PXD007896 (MCP 2018, PMC6210224). Its RAW names (`HepG215Set*`, `2017Jan28/29OffSet*`) do not overlap these files, so this dataset is **not** a duplicate.

**Series → experiment (INFERRED).** No source states this mapping. I assigned:
- `OffFeb2017S*` → the HepG2 IFN triplex. Evidence: the names follow the "Off…Set" scheme of the January 2017 HepG2.2.15 IFN triplex in PXD007896, and the fraction count (10) matches the stated 10.
- `HepG2_MAL_Set*` → HepG2.2.15 vs HepG2. Evidence: the "HepG2_" prefix, and a 2018-02-21 acquisition stamp in a file name.

**Channel map (INFERRED).** The paper does not say which dimethyl label carries which sample.
- IFN triplex: control = DIMETHYL0, IFN-α2a = DIMETHYL4, IFN-λ3 = DIMETHYL8. This is taken from the same lab's stated scheme in PMC6210224, which used the same protocol, the same IFNs and the same doses: untreated / IFN-α2a / IFN-λ3 = light / medium / heavy "respectively".
- HepG2.2.15 experiment: HepG2 = DIMETHYL0 and HepG2.2.15 = DIMETHYL4. This assumes a duplex, with the reference (denominator) in light by analogy.

The authoritative source would be the deposited PD `.msf` files (3.1–4.0 GB SQLite). They could not be read because the shell has no network, and the browser cannot do HTTP range reads.

**Biological replicate.** Set/S number = replicate 1–5. The paper states n=5 biological replicates per condition.

**Cell lines (Cellosaurus, verified live).**
- HepG2 = Hep-G2, CVCL_0027.
- HepG2.2.15 = Hep-G2/2.2.15, CVCL_L855. It is a child of CVCL_0027 with integrated HBV genotype D.

Both lines are male, 15Y, with hepatoblastoma (NCIt C3728). The HepG2.2.15 cells were a gift from A. Bertoletti and were cultured with Geneticin 150 µg/mL. Parental HepG2 had no vector or Geneticin control; the paper states this limitation.

**Instrument.** I used Q Exactive Plus (MS:1002634). Both this paper and PMC6210224 say "Q-Exactive Orbitrap Plus", but PX says Q Exactive. The RAW header was not readable, so this conflict is unresolved. Precedence used: paper > PX.

**Search parameters (paper Methods; the .msf was not read).**
- Software: PD 2.1 SEQUEST-HT.
- Enzyme: trypsin, 2 missed cleavages.
- Tolerances: precursor 10 ppm, fragment 0.02 Da.
- Fixed modifications: Carbamidomethyl C (UNIMOD:4), and light/medium/heavy dimethyl on K and N-term, written per channel (UNIMOD 36/199/330, mass shifts 28.0313/32.0564/36.0757).
- Variable modification: Oxidation M.
- Reagents: DTT and iodoacetamide.
- Acquisition: high-pH RP kit, HCD NCE 32%, MS1 350–1400 m/z, DDA top-10.

The PX `modifications` field also lists an acetylated residue. The paper does not list acetylation, so it is not annotated.

## Values left not available / not applicable
- None. Every required column is filled.
- `cell type` = hepatocyte is not stated by the source. It follows the precedent of earlier campaign HepG2 files (e.g. PXD000760).
- `culture medium` omits the FBS percentage. This paper does not give it (the 2018 paper says 10%).
- Ancestry, passage number and storage temperature are omitted, because no source gives them.
- Fraction identifiers are taken from the `F#` in each file name. The HepG2_MAL series has 9 fractions, while the paper says 10. The difference is unexplained; possibly one fraction was pooled or not deposited.

## Stated vs INFERRED
**STATED:**
- conditions, IFN doses and 24 h exposure
- n=5
- both cell lines
- the HBV/Geneticin culture
- fractionation, LC-MS and search parameters
- the light/medium/heavy masses

**INFERRED:**
- series → experiment
- label → condition in both experiments
- that the HBV experiment is a duplex
- instrument variant (paper used over PX; RAW not checked)

## Conflicts
- **Instrument:** PX says Q Exactive; the paper says QE Plus.
- **Fraction count:** the HepG2_MAL series has 9 fractions vs the 10 stated.
- **Species:** PX lists "HBV genotype D" (taxon 489483) as a species. HBV is integrated in HepG2.2.15, so `characteristics[organism]` is kept as Homo sapiens for every row, following the Cellosaurus OX field. The HBV content is carried by the cell line identity.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` was run separately with each of `--template ms-proteomics`, `--template human` and `--template cell-lines`. Each run reported "Everything seems to be fine" with 0 errors.

Ontology validation was skipped: the OLS dependencies are not installed, and OLS4 itself was unreachable today. For that reason:
- The UNIMOD 199 and 330 accessions were verified on unimod.org.
- The MS and PRIDE accessions were reused from reviewed campaign files (PXD046383, PXD034530).

## Sources checked
- ProteomeCentral PROXI record and the PRIDE HTTPS file listing
- PMC7364717 (Methods/Results)
- PMC6210224 (the earlier same-lab protocol and its channel map)
- PROXI record of PXD007896
- Cellosaurus CVCL_0027 and CVCL_L855
- UNIMOD

These were unreachable: the PRIDE v3 API, the PRIDE web page, Europe PMC, OLS4, and the authors' resource site (sysbio.chula.ac.th/IFN_HepG2_Proteomics). The ACS SI was not inspected.

**To promote to annotated:** read the `Workflows`/`QuanChannels` (study factors) and the label definitions from one `.msf` of each series (e.g. `OffFeb2017S1F.msf`, `HepG2_MAL_Set1_F.msf`), and the instrument model from a RAW header.

## Review status
pending
