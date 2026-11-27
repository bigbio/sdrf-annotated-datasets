# PXD054304 SDRF annotation report

## Study
RAPIDASH: Tag-free enrichment of ribosome-associated proteins ... - TMT MS RAPIDASH of E12.5 mouse limbs, forebrain, and liver. Paper: Susanto TT et al., Mol Cell 2024;84(18):3545-3563.e25, DOI 10.1016/j.molcel.2024.08.023, PMC11460945. The paper's Data and code availability lists "PXD054304 (TMT MS of E12.5 limbs, forebrain, and liver)", which verifies the PX→paper link. The PX record also links the same DOI. Same paper as PXD054298 and PXD054427 (singapore-1), but everything here was re-derived.

## Scope, evidence and decisions
The SDRF has 12 rows: 4 RAW × 3 TMT channels. Deposited (ProteomeCentral PROXI, re-derived 2026-11-26): 44 files. These are 4 RAW (`tissues_TMT_rep1..4.raw`), mqpar.xml, proteinGroups.txt, mzTab_reformatted.mzTab.gz, the mouse UniProt FASTA, checksum.txt and 35 MaxQuant `allSpectra.CID.FTMS.iso_0..34.apl` peak lists. This matches the cached 4 RAW / 44 files. All 4 RAW files are annotated and none is excluded. The peak lists and search outputs are not data files. The file list is in `/home/claude/singapore2/scratch/PXD054304/filelist.txt`.

- **Channel map (STATED, paper Table 1):** in "E12.5 tissues rep 1–4", Limbs are TMT 126, Forebrain TMT 127 and Liver TMT 128, with the same tags in every replicate. Protein per channel was 15 µg (rep 1), 25 µg (rep 2), 13 µg (rep 3) and 25 µg (rep 4). Table rep N maps to `tissues_TMT_repN.raw` **by file name only**; nothing else ties a RAW file to a Table 1 replicate.
- **Replicates:** the Fig. 4A legend gives four biological replicates per tissue, and Fig. 4B uses a paired Welch's t-test. The Methods say: "Each biological replicate consisted of tissues pooled from the same litter (9–12 embryos)". So biological replicate = litter = TMT injection 1–4, and the three tissues in one injection come from the same litter (source names `E12.5_FVB_litter{N}_{tissue}`). `pooled sample` = pooled.
- **Organism / strain / stage:** wild-type FVB/NJ (JAX 001800), timed matings, embryos collected at E12.5. These give `developmental stage` "embryonic day 12.5" (the format other campaign files use) and `strain or breed` FVB/NJ.
- **Organism part (factor):** limb UBERON:0002101, forebrain UBERON:0001890, liver UBERON:0002107. All three were checked live on Ontobee with their definitions. OLS4 search returned empty or rate-limited results today.
- **Enrichment:** all samples are RAPIDASH eluates (`characteristics[enrichment process]`, licensed through sample-metadata, which ms-proteomics and vertebrates extend).
- **Prep (Methods):** 6 M urea; 5 mM DTT; 15 mM iodoacetamide; Trypsin/Lys-C mix (Promega V5073), with both agents listed. Tissues were digested "as described" for the mESC samples. TMTsixplex (Thermo 90066), labels TMT126/127/128; the 129–131 channels are not used in Table 1.
- **MS (Methods):** Acquity UPLC M-class + Orbitrap Elite; 180 min 5–40% B; MS1 R=60k; HCD MS2 R=15k; top 15; NCE 40%. The instrument agrees with the PX record (LTQ Orbitrap Elite, MS:1001910). RAW headers were not read.
- **Search (Methods):** MaxQuant 2.4.2.0, reviewed mouse SwissProt (7 June 2024; the deposited FASTA name matches). Trypsin with ≤2 missed cleavages; main search 4.5 ppm (first search 20 ppm); MS/MS 20 ppm. Fixed: Carbamidomethyl C. Variable: Oxidation M, Deamidation NQ, N-terminal acetylation. TMT6plex is annotated K + any N-term `MT=Fixed`, the usual SDRF encoding for isobaric labels.

## Inferred / unresolved (why sandbox)
- **The deposited mqpar.xml was NOT read.** The PRIDE FTP returned "upstream connect error … connection timeout" twice. After that, the shared cloud browser had no window left and the tool forbade further browser calls. As a result:
  - the modifications come from paper prose, not from the deposited search (brief rule: the search is authoritative). "N-terminal acetylation" is encoded as `PP=Protein N-term`, MaxQuant's standard. That encoding is INFERRED, though it matched the mqpar of sibling PXD054298;
  - the TMT channel set in mqpar `isobaricLabels` could not cross-check Table 1. In PXD054298 the mqpar did confirm its Table 1 channels.
- **HCD vs CID:** the Methods say HCD at 40% NCE, but MaxQuant named the peak lists `allSpectra.CID.FTMS.*`, the same anomaly as PXD054298. HCD is kept because TMT reporter ions at m/z 126–128 would fall below the ion-trap CID low-mass cutoff, so CID is implausible for a quantitative TMT run.
- **RAW ↔ Table 1 replicate:** linked by name (`repN`) only.
- **Sex:** `not available`. The pools hold 9–12 embryos and sex is not stated.
- Not checked live: PRIDE (DDA PRIDE:0000627, DTT PRIDE:0000608, IAA PRIDE:0000599), MS (MS:1001910, 1001251, 1001309, 1000422) and UNIMOD (4, 35, 7, 1, 737) accessions. OLS was rate-limited. Their labels match this campaign's validated files.
- `cell type` is omitted (whole-tissue samples). MS1 scan range is unstated and omitted.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template ms-proteomics --template vertebrates`: "Everything seems to be fine". Ontology validation was skipped because the OLS extras are not installed. `sdrf_review.py`: [OK].

## To upgrade to annotated
Read `https://ftp.pride.ebi.ac.uk/pride/data/archive/2024/09/PXD054304/mqpar.xml`. Check `isobaricLabels` (expect 126/127/128 only), the experiment names per RAW, and the fixed/variable modification lists, then correct the modification columns if they differ.

## Review status
pending
