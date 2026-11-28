# PXD013827 SDRF annotation report

## Study
Tissue Proteome Profiling of Ovarian cancer in Pakistani Population (M. Waheed Akhtar lab, School of Biological Sciences, University of the Punjab, Lahore).

Paper: Noreen S, Gardner QA, Fatima I, Sadaf S, Akhtar MW. "Upregulated Expression of Calcium-Dependent Annexin A6: A Potential Biomarker of Ovarian Carcinoma." *Proteomics Clin Appl* 2020;14(2):e1900078. DOI 10.1002/prca.201900078, PMID 31747122. The PX record links this paper. Its title, authors and lab match the submitter, and its topic (2-DE + MALDI-TOF, AnxA6) matches the deposited ANXA6/ANXA5/LDHA fasta files. No PMCID was found. The paper is closed: Wiley returned a Cloudflare bot check, and Europe PMC REST returned an upstream error. Only the PubMed abstract and MeSH were read.

## Scope, evidence and decisions
**Status: sandbox.** 11 rows (11 runs, label-free) x 33 columns. Templates: ms-proteomics + human, both v1.1.0.

**Design.** Abstract: 2-DE coupled with MALDI-TOF MS of malignant and non-malignant (benign) human ovarian biopsies. Six 2D gel spots (five proteins) were differential (FDR <= 0.05, PMF score >= 79). So one deposited run = one excised 2-DE spot, measured by MALDI-TOF peptide mass fingerprinting.

**Deposited vs annotated.** The file list comes from the PROXI record, read in this session. It has 11 "Associated raw file URI" zips: B1516, Ov3R, ST12, TBS-7, TBS-8, TBS-9, TBS25, TBS4, TW18, X1, st26. All 11 are annotated as `comment[data file]`, with none missing and none extra. Each zip also has derived files that are not rows: `*Spectrum.mzXML`, `*peaklist.xml`, `SPECTRUM_*.mgf.mgf`/`X1.mgf`, Mascot `.dat`, `.xml` and `.mzid`. Other files that are not rows: 11 protein fasta files (ANXA2/4/5/6, LDHA, GAPDH, PRDX2, CYHR1, ENOA, PDIA3, OV3) and 2 gel images (Controlbenigndisease.png, ovariancancer.png).

**Search parameters** were read from the deposited Mascot XML `TBS4.xml` on the PRIDE FTP:
- Mascot 2.6.2.1, PMF search, SwissProt_2019_03, Homo sapiens
- Trypsin, 1 missed cleavage
- Carbamidomethyl (C) fixed, Oxidation (M) variable; this matches the PX MOD:00397/MOD:00425
- 140 ppm peptide tolerance, charge 1+

These values are applied to all spots, which assumes every search used the same settings. Only TBS4.xml was read, because the EBI FTP was intermittently unreachable.

**Instrument.** ultraflex (MS:1000201), from the PX field. The paper and the raw zips could not be read to check it. `ultraflex` may be a generic label for an ultrafleXtreme or ultraflex III instrument, and the companion dataset PXD014352 uses ultraflex III TOF/TOF.

**Acquisition and fractionation.**
- Acquisition = DDA (PRIDE:0000627). The template forbids reserved words in this column, and no PMF/MS1-only term exists, so DDA follows the bigbio precedent for MALDI datasets (PXD002849, PXD000178, PXD014352).
- Fractionation = 2-DE (PRIDE:0000122), as in PXD014768. It is not SDS-PAGE (PRIDE:0000568), because these spots come from 2D gels.
- Dissociation and fragment tolerance = not applicable, because PMF has no MS/MS.

## Values left not available / not applicable, and why
- `characteristics[disease]` = **not available** on every row. This is the main open point. Spots may have been excised from a carcinoma gel or a benign-control gel, and no spot-to-gel or spot-to-patient key was found:
  - The spot stems (TBS, TW, ST, X, B, Ov3R) are undefined.
  - The Mascot header gives only the local path `MALDI DATA\TBS4\0_K1`.
  - The paper is closed.

  The companion dataset PXD014352 (same lab, MM/N/Ov/TW/X stems) set `ovarian carcinoma` on every row. We did not copy that, because the design includes benign controls. For the same reason there is no factor value column.
- `characteristics[individual]`, `characteristics[age]`: not available, because there is no per-spot patient key.
- `characteristics[biological replicate]` = 1: a placeholder.
- `characteristics[developmental stage]` = adult: INFERRED from the PubMed MeSH terms (Adult, Middle Aged).
- `characteristics[sex]` = female: inferred from the ovary and the MeSH term Female.
- Reduction and alkylation reagents: not available, because the Methods were unread. The carbamidomethyl search shows that alkylation was done.

## Conflicts
None found between PX and the Mascot XML. The instrument was not verified against the raw data.

## Sources not reachable
- Wiley full text (Cloudflare)
- Europe PMC REST (upstream error)
- OLS (WebFetch permission not granted)

Accessions were taken from the PX record, from prior validated campaign files (PRIDE:0000122, PRIDE:0000627, MS:1000201, MS:1001251), and from UNIMOD 4/35. They were not re-checked live today. `parse_sdrf` ran with the OLS cache only (structural validation).

## Validation
- `parse_sdrf validate-sdrf --template ms-proteomics --template human`: no errors.
- `sdrf_review.py`: [OK], with the advisory no_factor_value.

## Review status
pending
