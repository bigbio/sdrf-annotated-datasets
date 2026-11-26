# PXD004355 SDRF annotation report

## Study
Characterization of protein deamidation by shotgun proteomics (PRIDE / ProteomeXchange; submitter Aida Serra, lab head Siu Kwan Sze, School of Biological Sciences, Nanyang Technological University, Singapore). The record is label-free LERLIC-MS/MS (a 50 cm weak-anion-exchange capillary run in ERLIC mode, "polyWAX" in the file names) of a soluble human brain extract, used to characterise Gln/Asn deamidation.

Publication: the PX record still says "Dataset with its publication pending", and no paper found cites PXD004355 (searches of Europe PMC, PMC and the web returned nothing). The matching paper is **INFERRED**: Serra A, Gallart-Palau X, Wei J, Sze SK, *Anal Chem* 2016;88(21):10573-82, doi:10.1021/acs.analchem.6b02688, PMID 27689507, no PMCID. The evidence for the match:
- the same submitter and lab head;
- the abstract describes LERLIC-MS/MS with a 50 cm anion-exchange column on soluble brain extracts in a single injection;
- the PXD was requested 2016-06-17, and the raw files are dated 150729.

I could not read the paper's full text: pubs.acs.org and the DR-NTU repository copy (hdl 10356/84813) both put up bot checks. The Methods values therefore come from the same group's open-access protocol paper: Gallart-Palau X, Serra A, Sze SK, *J Vis Exp* 2017;(122):55626, doi:10.3791/55626, PMID 28448026, **PMC5564503**. That paper describes the same LERLIC-MS/MS workflow on human brain tissue but does not cite PXD004355 either.

## Scope, evidence and decisions
Status: **sandbox**. The file has 3 rows (3 RAW × label-free) and 38 columns. Templates: ms-proteomics + human.

**Deposited vs annotated.** The PRIDE FTP listing (re-derived on 2026-11-26) holds 5 files. The 3 RAW files are all annotated:
- `150729_Long_polyWAX_Brain_sol_1uL_0_4ulmin_280min.raw` (1.0G)
- `150729_Long_polyWAX_BrainSol_sol_1uL_0_4ulmin_600min.raw` (2.4G)
- `150729_Long_polyWAX_BrainSol_sol_1uL_0_4ulmin_1200min.raw` (4.4G)

The other 2 files are not annotated:
- `Dataanalysis.rar` (50M): the search output. README.txt maps it to the 3 RAW files.
- `README.txt`

The campaign cache said "3 RAW / 4 files"; there are 3 RAW and 5 files, and the extra file is README.txt. The PX record's datasetFiles lists the 3 RAW files plus the .rar.

**Sample and run structure.** The file names encode the same injection (1 µL at 0.4 µL/min) and three gradient lengths: 280, 600 and 1200 min. I modelled one source ("human brain soluble extract", biological replicate 1) with technical replicates 1, 2 and 3. `comment[gradient]` and `factor value[gradient]` hold the gradient length, following the campaign precedent in PXD046283. The 280-min file is named "Brain_sol" and the other two "BrainSol_sol". Treating all three as the same extract is **INFERRED** from the shared date, injection and flow tokens.

**Sample-prep and acquisition values.** These are stated in the JoVE protocol (PMC5564503), not in a document tied to this PXD:
- 1% SDC in 100 mM ammonium acetate; 10 mM DTT; 20 mM IAA; trypsin 1:50, in solution.
- HCD with Orbitrap MS2 (R 30,000), top-10 DDA.
- Full MS 350-2000 m/z; MS/MS 150-2000 m/z.
- Search: 10 ppm / 0.05 Da; carbamidomethyl C fixed; oxidation M and deamidation N,Q variable; UniProt human.

The PX modifications (MOD:00397 iodoacetamide-derivatized residue, MOD:00400 deamidated residue) agree with this.

**Instrument.** Orbitrap Elite (MS:1001910) comes from the PX record only; its PX name is "LTQ Orbitrap Elite". The JoVE paper says only "an orbitrap mass spectrometer". The RAW headers were not read: the shell has no internet and I had no HTTP-range access.

**Modifications.** These come from protocol prose, not from the deposited search output. `Dataanalysis.rar` was not opened (a 50 MB RAR, no shell network). The search engine is not named anywhere.

**Accession checks.** EBI OLS4 was down (upstream connect error), so I checked every accession live by other routes:
- MS:1001910, MS:1000422, MS:1001251, MS:1002038, MS:1000484, UBERON:0000955 and NCBITaxon:9606 on ontobee;
- UNIMOD:4, 7 and 35 on unimod.org;
- PRIDE:0000627, 0000608 and 0000599 in the PRIDE CV obo on GitHub.

The evidence files are in `/home/claude/singapore1/scratch/PXD004355/`.

**Validation.** `parse_sdrf validate-sdrf --use_ols_cache_only` passed (clean) with no template, with `--template ms-proteomics` and with `--template human`. The OLS ontology check was skipped (dependencies not installed), so the pass is structural only. A mutation test (an invalid sex value) was rejected, which shows the human template rules are enforced. `sdrf_review.py` printed [OK].

## Values left not available / not applicable
- **disease, age, sex, ancestry category, individual = not available.** Neither the abstract nor the JoVE protocol gives donor details, the number of donors, or post-mortem or disease status. The lab's other brain papers use AD/VaD post-mortem cohorts, but nothing ties this extract to one.
- **organism part = brain.** No brain region is stated.
- **cell type = not applicable.** The sample is a bulk tissue lysate.
- **fractionation method = not applicable.** This is a single-injection online LERLIC run with no offline fractionation.
- **collision energy:** omitted (optional; not stated).

## Stated vs INFERRED
- **Stated:**
  - From the PX record: organism, tissue = brain (keyword), instrument, and the deamidation/IAA modifications.
  - From the JoVE protocol: reagents, enzyme, HCD, scan ranges, tolerances and the search modifications.
  - From the file names: the gradient lengths, 1 µL injection and 0.4 µL/min flow.
- **INFERRED:**
  - the link to the Anal Chem 2016 paper;
  - that the JoVE protocol parameters apply to these 2015 runs;
  - that all 3 runs come from one extract;
  - that gradient length is the experimental factor.

## Conflicts
- Instrument name: the PX record says "LTQ Orbitrap Elite", while the current PSI-MS label for MS:1001910 is "Orbitrap Elite". It is the same accession, and I used the CV label.
- No other conflicts were found. The deposited search output and the RAW headers, which would be the strongest evidence, were not read.

## Judgement calls a reviewer should attack
1. Whether the paper link is right. The PX record says the publication is pending, the Anal Chem paper's full text was unreadable, and the JoVE paper does not cite the PXD.
2. That the search parameters and modifications come from the JoVE protocol rather than `Dataanalysis.rar`.
3. That "Brain_sol" (280 min) and "BrainSol_sol" (600/1200 min) are the same extract, entered as technical replicates 1-3 with gradient as the factor.
4. That the instrument comes from the PX record only (RAW headers unread).

## Review status
pending
