# PXD020885 SDRF annotation report

## Study
Characterization of Plasmodium falciparum NEDD8 (PX title). Paper: Bhattacharjee M, Adhikari N, ..., Sijwali PS. Characterization of Plasmodium falciparum NEDD8 and identification of cullins as its substrates. Sci Rep 2020;10:20220. DOI 10.1038/s41598-020-77001-5, PMID 33214620. The paper cites PXD020885 for the yeast anti-HA IP data (and separately PXD020952, which is the other deposition).

Status: **sandbox** (A/B = gel fraction is INFERRED; see below).

## Scope, evidence and decisions
- File list from the PROXI record (v2, fetched 2026-11-27, saved in scratch): 20 .raw + 10 .msf (PD search outputs, one per strain x experiment, each grouping an A and a B raw). PRIDE FTP and OLS were unreachable today (upstream connection errors).
- Deposited vs annotated: 20/20 raw files annotated, 20 rows (label-free). The 10 .msf are search outputs and not rows.
- Samples: S. cerevisiae BY4741 (paper: MATa his3D1 leu2D0 met15D0 ura3D0) wild type ("WT mock"), rub1D complemented with pLE124-HA-PfNEDD8, and rub1D complemented with pLE124-HA-ScRub1 (CUP1 promoter). Anti-HA (mouse) IP from 2 mg lysate on protein A/G magnetic beads; WT IP is the negative control (STATED).
- Exp 1/2/3 = three independent experiments / biological replicates (STATED: "three independent experiments", cultures "in triplicates") -> characteristics[biological replicate] 1-3.
- A/B -> comment[fraction identifier] 1/2 with SDS-PAGE fractionation (PRIDE:0000568). INFERRED: the paper only says the gel slice with the protein band was excised; A and B are searched together in one .msf per sample, consistent with two gel pieces of one lane but also with two injections. Raw headers not readable (no network) to check.
- "WT mock A2/B2 Exp 2" (own .msf "WT mock 2 Exp 2") -> same source as WT Exp 2, comment[technical replicate] 2. INFERRED (could be a second WT IP/culture).
- Instrument Q Exactive HF (paper and PX agree; raw header not checked), HCD, DDA. Trypsin, DTT 10 mM / IAA 55 mM, PD 2.2 SEQUEST HT: 5 ppm / 0.05 Da, Carbamidomethyl C fixed, Oxidation M and Deamidated N,Q variable (paper; matches PX modifications MOD:00397/00425/00400). .msf workflow node not read (no network) - search mods are from the paper.

## Values not available / not applicable
- organism part, cell type, disease: not applicable (yeast culture).
- collision energy, MS1 scan range: not stated -> columns omitted.

## Conflicts / caveats
- Paper says search was against UniProt P. falciparum 3D7; for yeast IPs a yeast database was presumably also used, not stated.
- Strain/genotype carried in factor value[genotype] and source name; characteristics[strain or breed]/[genotype] not used because ms-proteomics alone does not license them and no template covers fungi.
- Ontology accessions could not be re-verified live (OLS down); PRIDE:0000568 per coordinator, others identical to previously reviewed campaign files; UNIMOD:7 = Deamidated.

## Validation
parse_sdrf validate-sdrf --template ms-proteomics: "Everything seems to be fine" (OLS ontology check unavailable in env); sdrf_review.py: [OK].

## Review status
pending
