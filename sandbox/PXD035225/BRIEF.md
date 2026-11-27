# PXD035225 SDRF annotation report

## Study
Cohesin is involved in transcriptional repression of invasion-related genes. This is an SMC3 IP-MS study in Plasmodium falciparum (Nanyang Technological University; submitter Ameya Sinha; lab head Peter R. Preiser).

**Paper:** Rosa C, Singh P, Chen P, Sinha A, Claës A, Preiser PR, Dedon PC, Baumgarten S, Scherf A, Bryant JM. Cohesin contributes to transcriptional repression of stage-specific genes in the human malaria parasite. EMBO Rep 2023;24(10):e57090.
- DOI 10.15252/embr.202357090, PMID 37592911, PMC10561359 (CC BY 4.0).
- The paper's Data availability section cites the dataset ("SMC3-3HA Proteomics data: PRIDE repository accession # PXD035225"), so the PX-record link is verified.

## Scope, evidence and decisions
**Status: sandbox.** The SDRF has 6 rows (6 label-free Thermo `.raw` runs × 1) and 35 columns.
- Template: ms-proteomics only. There is no protist organism template, so this follows the campaign precedent for parasite/protist datasets (PXD019488, PXD056396).

**Deposited vs annotated.** The file list comes from the ProteomeCentral PROXI record (`resultType=full`; Page URL and accession checked = PXD035225). It has 10 files, which matches the campaign cache (6 RAW / 10 files):
- **6 vendor RAW, all annotated:** `20210217_AS_IP_SMC3_DSP_Rep1/2/3.raw` and `20210127_AS_IP_NF54_DSP_Rep1/2/3.raw`.
- **4 processed files, not annotated** (they are not raw): `20210127_AS_IP_1203500_DSP_Rep1-_1_` as `.mzML`, `.mgf`, `.mzid.gz` and `.msf`.
  - They belong to an IP called "1203500", which is not SMC3 and has no deposited RAW. It may be a PF3D7_1203500 bait from another experiment.
  - The paper does not mention this IP, so it is noted here and not annotated.
- I could not re-derive the file list independently:
  - PRIDE FTP `archive/2023/10/PXD035225/`: 3 attempts, all "upstream connect error / connection timeout".
  - PRIDE API v3 `files/all`: 1 attempt, failed.
  - The PROXI `datasetFiles` list is the only file list used.
- Annotated = 6/6 RAW. Nothing was excluded.

**Run → sample map: bait vs control (STATED).** The file names and the paper agree:
- `SMC3` runs (acquired 2021-02-17) = **bait**: anti-HA IP from the SMC3-3HA-glmS clone. `sample type` = study sample.
- `NF54` runs (acquired 2021-01-27) = **negative control**: the same anti-HA IP on wild-type (untagged) parasites. `sample type` = negative control.
- Paper (section "SMC3 immunoprecipitation and mass spectrometry"): the bait was run as "n = 3 technical replicates" and the "WT culture (n = 3 technical replicates)" served "as a negative control".
- Each arm is therefore one source (`biological replicate` = 1). `Rep1-3` → `technical replicate` 1-3; matching Rep number to tech-rep index is the obvious reading of the file names.
- The arm is carried in `characteristics[treatment]` and `factor value[treatment]`, as in PXD019488.

**Sample prep (paper).**
- Late-stage parasites (1.5 × 10^9) were enriched on a Percoll gradient, then crosslinked with 0.5 mM DSP for 60 min at 37 °C.
- Lysis was in RIPA buffer with protease/phosphatase inhibitors and Benzonase. IP used anti-HA magnetic beads overnight at 4 °C.
- On-bead steps: DTT reduction (PRIDE:0000608), iodoacetamide alkylation (PRIDE:0000599), and digestion with 1 µg trypsin (Thermo Fisher 90059; MS:1001251). Peptides were cleaned up on C18 ZipTips.
- No fractionation, so `fraction identifier` = 1.

**LC-MS/MS (paper).**
- Easy-nLC1000 with a 50 cm PepMap RSLC C18 column and a 70 min gradient.
- DDA (PRIDE:0000627). MS1 at 60,000 resolution over 350-1,500 m/z, which gives `ms1 scan range` = 350m/z-1500m/z. Top-15 MS/MS at NCE 30, which gives `collision energy` = 30% NCE.
- Dissociation is written as `NT=HCD;AC=MS:1000422`. This is INFERRED: the paper gives an NCE but does not name HCD, and HCD is the only fragmentation mode on Q Exactive-class instruments.

**Search (paper; deposited `.msf` not used).**
- Proteome Discoverer 2.3.0.523 with SEQUEST. Precursor tolerance 10 ppm, fragment tolerance 0.8 Da. Trypsin, up to 2 missed cleavages.
- Fixed: Carbamidomethyl C (UNIMOD:4).
- Variable: Oxidation M (UNIMOD:35); CAMthiopropanoyl on K and protein N-term (UNIMOD:293, which is the DSP remnant after reduction and alkylation); Phospho S/T/Y (UNIMOD:21).
- UNIMOD:293's sites (K anywhere; Protein N-term) were checked against the unimod.xml shipped with sdrf-pipelines.
- The only deposited `.msf` belongs to the non-SMC3 "1203500" IP and could not be opened (FTP down), so the paper's parameters are used.
- The PX record's modification list (MOD:00397, iodoacetamide-derivatized residue) is consistent with this.

**Values left not available / not applicable.**
- `organism part` and `cell type` = not applicable. The sample is a unicellular parasite culture in human erythrocytes, with Percoll-enriched late stages.
- The stage ("late stage", i.e. trophozoite/schizont) has no licensed column under ms-proteomics, so it is recorded here only.
- `disease` = not applicable (in vitro culture).
- No strain or genotype column: ms-proteomics does not license `strain or breed` or `genotype`. Strain information is in this report.
- Not stated in the paper, so omitted: the protein database (no FASTA named, so it is unknown whether human or RBC sequences were included), the FDR, and the MS2 resolution.

## Conflicts
1. **Instrument.**
   - The PX record (all three revisions) says Q Exactive HF (MS:1002523).
   - The paper Methods say "Q Exactive HF-X mass spectrometer (Thermo Fisher)".
   - Following the precedence rule (paper > PX field), I annotated **Q Exactive HF-X (MS:1002877)**. The RAW headers could not be read (FTP unreachable; the shell has no network), so this is unresolved and is the main reason for sandbox status.
2. **Organism.**
   - The PX species is Homo sapiens (9606). The study organism is *P. falciparum*, grown in human RBCs, so the samples will contain some human (host) proteins.
   - I annotated `Plasmodium falciparum` (NCBITaxon:5833), at species level as in PXD056396.
3. **Control strain.**
   - The control file names say `NF54`. The paper describes only 3D7 cultures and a "WT culture" control, and never mentions NF54. The SMC3-3HA-glmS line was made by CRISPR in 3D7 WT.
   - The control is described as "wild-type untagged parasites" without naming a strain, and the species-level taxon covers both readings.
4. **Extra IP files.** The "1203500" processed files (see the scope section above) are deposited without RAW files and are not in the paper.

**Stated vs INFERRED.**
- Stated: the bait/control arms, n = 3 technical replicates per arm, enzyme, reagents, tolerances, modifications, NCE, MS1 range and DDA.
- INFERRED: the HCD term, Rep number = technical-replicate index, and `material type` = cell.

**Ontology verification.** EBI OLS4 was unreachable today (upstream connect errors on every attempt).
- TIB Terminology Service (OLS API): MS:1002877 "Q Exactive HF-X", MS:1002523 "Q Exactive HF", MS:1000422 "beam-type collision-induced dissociation" (synonym HCD), MS:1001251 "Trypsin", NCBITaxon:5833 "Plasmodium falciparum".
- Upstream pride_cv.obo (release 2026-11-23): PRIDE:0000608 "Dithiothreitol (DTT)", PRIDE:0000599 "Iodoacetamide (IAA)", PRIDE:0000627 "Data-dependent acquisition", MS:1002038 "label free sample".
- unimod.xml (sdrf-pipelines): UNIMOD:293 CAMthiopropanoyl. UNIMOD:4, 21 and 35 were taken from campaign convention.

**Validation.**
- `parse_sdrf validate-sdrf --template ms-proteomics --use_ols_cache_only` → "Everything seems to be fine". This was structural only, because the OLS dependencies are not installed.
- `sdrf_review.py` → [OK].

Evidence is in `/home/claude/singapore2/scratch/PXD035225/` (`proxi_PXD035225_summary.txt`, `paper_PMC10561359_notes.txt`). The build script is `scripts/build.py`.

## Review status
pending. A reviewer should challenge these points:
1. Q Exactive HF-X (paper) was chosen over HF (PX), and the RAW headers are unread.
2. The NF54-named control runs are annotated as the paper's "WT" control.
3. The three runs per arm are technical replicates (biological replicate = 1), as the paper states.
4. The non-SMC3 "1203500" processed files are excluded.
5. Organism is *P. falciparum* rather than the PX record's Homo sapiens.
