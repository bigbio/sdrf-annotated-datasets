# PXD062502 annotation blocked

PXD062502 ("Interactome of *Entamoeba histolytica* KERP2 with host epithelial cells", A*STAR GIS / Univ. Tokyo,
announced 2026-02-26) is the host-side arm of Peng R, Santos HJ, Nozaki T., *Nat Commun* 17:4433 (2026),
DOI 10.1038/s41467-026-70847-9, PMID 41888128 (open access; the paper's Data availability names PXD062502 and
PXD062553, and the PRIDE record for PXD062502 matches the Caco-2 experiment: human search database, Caco-2 cells).
The companion PXD062553 (MassIVE MSV000097502, *E. histolytica* HM-1:IMSS) is the amoebic nuclear/cytosolic co-IP
and is a different deposit.

Design (stated): confluent Caco-2 (ATCC HTB-37, EMEM + 20% heat-inactivated FBS) co-cultured 1 h at 5:1 with
*E. histolytica* HM-1:IMSS Cl6 trophozoites expressing **HA-KERP2 (bait)** or **HA-mock (control)**; parasites
washed off with cold 2% galactose/PBS; host cells scraped, DSP-cross-linked, M-PER lysis, anti-HA (11MO) IP on
Protein A Dynabeads, HA-peptide elution; SP3, DTT, iodoacetamide, on-bead trypsin; EasyLC 1100 + Orbitrap Fusion
Lumos, DDA, HCD CE 30, MS1 350-1800 m/z; Mascot 2.8.2 vs UniProt human, 5 ppm precursor / 10 ppm fragment,
fixed Carbamidomethyl (C), variable deamidation (N/Q), oxidation (M), phospho (S/T/K), formyl (K, protein N-term);
Scaffold (PeptideProphet 1% FDR, ProteinProphet 95%). **Three biological replicates** per arm (hits = >=2-fold over
HA-mock in >=2/3 or 3/3 replicates; 78 double-hit, 5 triple-hit proteins; Supplementary Data 6a-b).

## Why no SDRF is emitted: the run -> arm (bait vs control) key is unknown

The deposit has 6 RAW files whose names carry only a facility code and a serial sample number — nothing that
identifies HA-KERP2 vs HA-mock, and no replicate index:

| RAW | bytes | Scaffold search |
|---|---|---|
| `JS-CS-E482_240404_NozakiT_HS_S1_50pct.raw` | 1896582760 | 240404 |
| `JS-CS-E482_240404_NozakiT_HS_S2_50pct.raw` | 2006587704 | 240404 |
| `JS-E480-CS_240425_NozakiT_HS_DDA_S1_10pct.raw` | 1078587562 | 240425 |
| `JS-E480-CS_240425_NozakiT_HS_DDA_S2_10pct.raw` | 1263360312 | 240425 |
| `JS-E480-CS_240425_NozakiT_HS_DDA_S3_10pct.raw` | 1363231535 | 240425 |
| `JS-E480-CS_240425_NozakiT_HS_DDA_S4_10pct.raw` | 1081195006 | 240425 |

Every SDRF row for a pull-down needs its arm; with a 2-arm, 3-replicate design and 6 identically-named runs, any
assignment (which S is bait, which is mock, how the two acquisition batches pair into replicates) would be pure
guesswork. Campaign rule: a condition map that is only guessed is never `annotated`, and a run -> sample key that
is unknown is `blocked`.

A second inconsistency makes guessing worse: the 8 deposited MGF peak lists embed the byte size of the run they
came from, which pairs them to RAW files exactly. Six match the deposited RAW files; two do not
(`...1264859552...F016705...MGF` in the 240425 Scaffold set and `...1769860427...F016388...MGF` in the 240404 set).
So the two Scaffold analyses covered **8** LC-MS runs (5 + 3) while only **6** RAW files were deposited — the
deposit is not even a complete image of the analysis, so "6 runs = 3 bait + 3 mock" cannot be assumed either.

## Evidence checked

- ProteomeCentral PROXI `datasets/PXD062502?resultType=full` (cloud browser, Page URL verified): 16 files
  (6 RAW, 2 Scaffold `.mzid.gz`, 8 MGF), instrument Orbitrap Fusion Lumos, species *Homo sapiens* only,
  "No PTMs are included in the dataset", no publication beyond the dataset DOI, submitter keyword "None".
- PRIDE v3 `projects/PXD062502` and `projects/PXD062502/files/all` (WebFetch): all 16 entries carry
  `projectAccessions = PXD062502`; sizes as tabled; sample and data processing protocols as above. No sample
  sheet, README, checksum or search-parameter file is deposited — only RAW, MGF and the two Scaffold mzid.
- The two `*_Scaffold.mzid.gz` result files (5.9 / 6.7 MB, gzip) are the only place a Scaffold biological-sample
  name per run could live; they cannot be read here (the shell has no network — agent proxy 403 — and the PRIDE
  FTP over HTTPS, both `ftp.pride.ebi.ac.uk` and the `ftp.ebi.ac.uk/pride-archive` mirror, returned upstream
  connect errors / connection timeouts from the cloud browser throughout this run; WebFetch is robots-disallowed
  for that host).
- Full text of the Nat Commun paper (cloud browser + WebFetch): Methods and Results describe the arms and the
  replicate count but give no run table, no file names and no per-replicate labels.
- Supplementary Data 6a-b (`...MOESM8_ESM.xlsx`), the Scaffold-derived interactor table that would most likely
  carry per-replicate column headers: `static-content.springer.com` is robots-disallowed for WebFetch and the
  file cannot be downloaded or parsed here.
- Sibling deposit PXD062553 / MSV000097502 (PROXI + MassIVE PROXI): different experiment (amoebic
  nuclear/cytosolic co-IP), no file list exposed, no bearing on this run key.

## What would unblock it

Any one of: (a) the Scaffold biological-sample names inside `240404_NozakiT_HS_Scaffold.mzid.gz` /
`240425_NozakiT_HS_Scaffold.mzid.gz` (readable once PRIDE FTP is reachable — these are small files);
(b) the column headers of Supplementary Data 6a-b, if they name the raw runs; (c) a statement from the
submitters mapping `JS-CS-E482_240404_..._S1/S2` and `JS-E480-CS_240425_..._S1-S4` to HA-KERP2 vs HA-mock and to
biological replicates 1-3 — which would also explain the two analysed runs that were not deposited.

Also to be settled when the arms are known: this is a host+parasite system. `characteristics[organism]` would be
`Homo sapiens` (NCBITaxon:9606; Caco-2, CVCL_0025, EFO:0001099) with the parasite
(*Entamoeba histolytica* HM-1:IMSS, NCBITaxon:294381) carried as the treatment/co-culture characteristic, since
the IP, the lysate and the Mascot database for this deposit are all human-side.

## Review status

pending
