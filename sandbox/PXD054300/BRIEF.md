# PXD054300 SDRF annotation report

## Study
RAPIDASH ... - label-free MS RAPIDASH of L36-FLAG and S17-FLAG E14 mESCs (Figures 1G-H). Paper: Susanto TT et al., Mol Cell 2024;84(18):3545-3563.e25, DOI 10.1016/j.molcel.2024.08.023, PMC11460945. The paper's Data and code availability lists "PXD054300 (label-free MS of L36-FLAG and S17-FLAG mESCs)", which verifies the PX→paper link.

## Scope, evidence and decisions
The SDRF has 6 rows (6 RAW, label free). Deposited (PROXI, re-derived 2026-11-26): 50 files. These are 6 RAW (`L36-1/2/3-elu.raw`, `S17-1/2/3-elu.raw`), mqpar.xml, proteinGroups.txt, mzTab_reformatted.mzTab.gz, the mouse UniProt FASTA, checksum.txt, 18 `allSpectra.HCD.ITMS.iso_0..17.apl` and 21 `allSpectra.CID.ITMS.secpep.sil0_0..20.apl`. This matches the cached 6 RAW / 50 files. All 6 RAW files are annotated and none is excluded. The file list is in `/home/claude/singapore2/scratch/PXD054300/filelist.txt`.

- **Design (STATED):** the Fig. 1G legend says: "Three biological replicates of RAPIDASH were performed for each of the same cell lines and analyzed by LC-MS/MS". `L36-N-elu` / `S17-N-elu` map to the Rpl36-FLAG / Rps17-FLAG RAPIDASH eluate, biological replicate N. The replicate number comes from the file name.
- **Cell lines:** the Key Resources Table lists "Rpl36-FLAG E14-mESC" and "Rps17-FLAG E14-mESC" (ref. 5, Simsek et al. 2017 Cell), and the paper says core RPs were "endogenously tagged with FLAG epitope tag". Neither line has a Cellosaurus entry: searches for Rpl36 and Rps17 on api.cellosaurus.org returned numFound 0. They are therefore annotated with the parental line **ES-E14, CVCL_C320**, checked live: synonym E14, 129P2/Ola, male, ESC CL:0002322, derived from blastocyst. The paper states the parental "E14 … (XY)" from the Panning lab. The tag goes in `characteristics[genotype]` and `factor value[genotype]` ("Rpl36-FLAG (endogenously FLAG-tagged Rpl36)" / "Rps17-FLAG …"). Using `characteristics[genotype]` requires declaring the clinical-metadata template, which adds no further required columns. This follows the campaign's precedent for derived lines: parental accession, with the derivative named in the source name and another column.
- **Culture medium (STATED):** KnockOut DMEM, 15% ES-quality FBS, 2 mM L-glutamine, 1× pen/strep, 1× MEM NEAA, 0.055 mM 2-mercaptoethanol, mouse LIF, on 0.1% gelatin. The PMC HTML renders the LIF concentration as "103 U/mL", a lost superscript, so it is written as 1000 U/mL.
- **Prep (Methods, mESC RAPIDASH samples):** 6 M urea, 5 mM DTT, 15 mM IAA, Trypsin/Lys-C mix (Promega V5073), with both agents listed.
- **MS (Methods, "Mass spectrometry of unlabeled tryptic digests"):** Orbitrap Elite (agrees with the PX record), 90 min 1–40% B, MS1 R=120k, **CID** MS/MS top 15, isolation 1.8 m/z, NCE 35%, activation 10 ms. The label is `label free sample`.
- **Search (Methods):** MaxQuant 2.4.2.0. Trypsin ≤2 missed cleavages; main search 4.5 ppm. Fixed: Carbamidomethyl C. Variable: Oxidation M, Deamidation NQ, N-terminal acetylation (encoded `PP=Protein N-term`, INFERRED from the MaxQuant default).

## Inferred / unresolved (why sandbox)
- **The deposited mqpar.xml was NOT read.** The PRIDE FTP timed out, and then the shared cloud browser had no window left. The modifications therefore come from paper prose, not the deposited search, and the per-RAW experiment names were not checked.
- **Fragment mass tolerance = `not available`:** the paper gives a single "MS/MS match tolerance of 20 ppm". The apl names (`*.ITMS.*`) indicate ion-trap MS2 readout, where MaxQuant applies its separate ITMS tolerance, not the FTMS ppm value. Writing 20 ppm would probably be wrong, and the ITMS value is not stated anywhere I could read.
- **CID vs HCD:** the Methods say CID (35% NCE). The main peak lists are named `allSpectra.HCD.ITMS.*` and the second-peptide lists `CID.ITMS.*`. The token is inconsistent within one search, and the TMT sets of the same paper show the opposite swap, so CID is kept as stated.
- **Parental Cellosaurus accession** for knock-in derivatives (see above). `organism part` blastocyst and `developmental stage` blastocyst stage come from Cellosaurus, not the paper.
- Not checked live: PRIDE/MS/UNIMOD accessions (OLS was rate-limited). Their labels match this campaign's validated files.
- Unstated, so omitted: passage number and MS1 scan range.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` with ms-proteomics, vertebrates, cell-lines and clinical-metadata: "Everything seems to be fine". Ontology validation was skipped because the OLS extras are not installed. `sdrf_review.py`: [OK].

## To upgrade to annotated
Read `https://ftp.pride.ebi.ac.uk/pride/data/archive/2024/09/PXD054300/mqpar.xml`. It should give the ITMS MS/MS tolerance, the modification lists and the RAW → experiment names, which would confirm the rep numbering.

## Review status
pending
