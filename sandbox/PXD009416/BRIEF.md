# PXD009416 SDRF annotation report

## Study
ATP synthase nLC-MSMS: alpha-synuclein oligomers interact with ATP synthase and open the permeability transition pore in Parkinson's disease. Ludtmann et al., Nat Commun 2018;9:2293, DOI 10.1038/s41467-018-04422-2, PMID 29895861. The paper's Methods and Data availability cite PXD009416, so the PX link is correct. Submitter: Anti Doping Lab Qatar.

## Scope, evidence and decisions
Status: **sandbox**. 24 rows (24 RAW x label free), 37 columns. Templates: ms-proteomics, vertebrates.

- **File list** comes from the PROXI record (fetched 2026-11-27). It has 24 RAW files, `P1{A..H}{5,6,7}.raw` (`P1H5` is deposited as `P1H5_170321162321.raw`), and 6 PD 1.4 `.msf` files (`Rt_Ox_quant_P1_{5,6,7}.msf`, `Rt_SpecOx_quant_P1_{5,6,7}.msf`). The PRIDE FTP listing and the EBI REST/OLS endpoints timed out today, so the `.msf` files were not read.
- **Deposited vs annotated:** all 24 RAW files are annotated, and none are excluded.
- **Design (paper, stated):** rat brain mitochondria were split and treated for 15 min with buffer, alpha-synuclein monomers or oligomers. Each sample was run on SDS-PAGE, either directly or after ATP synthase co-IP. Each lane was cut into eight equal parts.
- **Design (INFERRED):** the plate-well names suggest a layout. Rows A-H are the 8 gel slices (`comment[fraction identifier]` 1-8), and columns 5/6/7 are three lanes (three source names, `P1_lane5/6/7`). The msf naming supports this, with one `_5/_6/_7` search per column.
- **Open point (why sandbox, not annotated):** nothing states which lane is buffer, monomer or oligomer, or whether the lanes are whole mitochondria or the co-IP eluate. For that reason `characteristics[treatment]` = `not available` and no factor column is written: a factor that is all `not available` fails CI as `hollow_factor_value`, while a missing factor is only advisory. The deposited `.msf` StudyDefinition or the authors could resolve this.
- **Instrument:** the PX record says Orbitrap Fusion ETD (MS:1002417). The paper says "Orbitrap Fusion tribrid", so Orbitrap Fusion (MS:1002416) was used. Raw headers are unread, so this conflict is unresolved.
- **Acquisition (paper):** DDA; MS1 400-1600 m/z at 120k; HCD 30% NCE; ion-trap MS2. PD 1.4 SEQUEST HT with 10 ppm precursor / 0.6 Da fragment tolerance, trypsin (2 missed cleavages), DTT/IAA.
- **Modifications:** the paper lists 12 variable mods, but their residues are in Suppl. Table 1 (not read). Only mods with a stated or unique residue are annotated, all as Variable: Carbamidomethyl C (UNIMOD:4; the paper lists it as variable, not fixed), Oxidation M (UNIMOD:35), His->Asn (348), His->Asp (349), Lys->AminoadipicAcid (381).
- **Mods omitted:** carbonylation (+13.979, UNIMOD:1918), dioxidation (425) and trioxidation (345) were left out because their target residues are unknown.
- **Accessions:** checked against the sdrf-pipelines ontology cache because live OLS was unreachable: PRIDE:0000568 = SDS PAGE, MS:1002416, MS:1000264, MS:1000422, MS:1001251, UNIMOD 348/349/381, UBERON brain, NCBITaxon 10116.

## Values not available / not applicable
- treatment: lane -> condition map is absent.
- sex: "of either sex" is stated only for the pups; the adult rats' sex is unstated.
- cell type: not applicable (organelle prep from tissue).
- developmental stage: `adult` is INFERRED from 200-250 g rats.
- biological replicate: set to the lane number (5/6/7), which is a placeholder identity and INFERRED.

## Conflicts
- PX says Orbitrap Fusion ETD; the paper says Orbitrap Fusion. The paper was used.
- PX modifications (MOD:00425, MOD:00397) are a subset of the paper's list.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics --template vertebrates`: OK, structural only, because OLS dependencies are not installed. `sdrf_review.py`: [OK], with advisory no_factor_value.

## Review status
pending
