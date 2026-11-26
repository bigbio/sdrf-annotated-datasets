# PXD054298 SDRF annotation report

## Study
RAPIDASH: Tag-free enrichment of ribosome-associated proteins ... - TMT MS RAPIDASH comparison with sucrose cushion of E14 mESCs. Paper: Susanto TT et al., Mol Cell 2024;84(18):3545-3563.e25, DOI 10.1016/j.molcel.2024.08.023, PMID 39260367, PMC11460945 (NIHMS author manuscript). The paper's Data Availability names this PXD ("PXD054298 (TMT MS RAPIDASH and sucrose cushion of E14 mESCs)"), so the PX→paper link is verified.

## Scope, evidence and decisions
6 rows = 3 RAW × 2 TMT channels. Deposited (PROXI, 33 files): 3 RAW (`pellet_eluate_rep1/2/3.raw`), mqpar.xml, proteinGroups.txt, mzTab_reformatted.mzTab.gz, the mouse UniProt FASTA, and 26 MaxQuant `allSpectra.CID.FTMS.iso_0..25.apl` peak lists. That matches the cached 3 RAW / 33 files. All 3 RAW files are annotated; nothing is excluded.

- **Channel map (STATED):** Mol Cell STAR Methods Table 1 lists "RAPIDASH eluate vs. sucrose cushion pellet in mESCs", rep 1–3. In each rep the sucrose cushion pellet is TMT 130 and the RAPIDASH eluate is TMT 131, with 25 µg each; "Each TMT replicate constitutes a single injection". The bioRxiv preprint (PMC10723405) has the identical table. Rep N maps to `pellet_eluate_repN.raw` by file name (the name-to-rep link is by naming only). The Figure 1D legend calls these "three biological replicates", which gives biological replicate 1–3.
- **Kit:** TMTsixplex (Thermo 90066), so the labels are TMT130 and TMT131. The other four channels are unused, because the table lists only two samples per injection.
- **Samples:** wild-type E14 mESCs (XY), a gift from the Panning lab. The cell line is Cellosaurus ES-E14 CVCL_C320 (synonym E14; 129P2/Ola; male; blastocyst-derived; ESC CL:0002322), checked live on api.cellosaurus.org. The condition is in `characteristics[enrichment process]` and in the factor value: sucrose cushion pellet vs RAPIDASH eluate.
- **MS (paper):** Acquity UPLC M-class + Orbitrap Elite, DDA top-15, HCD 40% NCE, MS1 R=60k, MS2 R=15k, 180 min gradient. The instrument (LTQ Orbitrap Elite, MS:1001910) agrees with the PX record; the RAW header was not read.
- **Prep:** 5 mM DTT, 15 mM iodoacetamide, Trypsin/Lys-C mix (Promega V5073). Both cleavage agents are listed.
- **Search (deposited mqpar.xml, read via PRIDE FTP over HTTPS, plus paper Methods):** MaxQuant 2.4.2.0, `lcmsRunType` Reporter MS2. The three RAW files are experiments 1/2/3. `isobaricLabels` holds only TMT6plex-Lys130/Nter130 and TMT6plex-Lys131/Nter131, which confirms the two-channel design in Table 1 independently. Fixed: Carbamidomethyl (C). Variable: Oxidation (M), Acetyl (Protein N-term), Deamidation (NQ). Enzyme: Trypsin/P, ≤2 missed cleavages. Tolerances come from the paper: main search 4.5 ppm (first search 20 ppm), MS/MS 20 ppm.

## Inferred / unresolved (why sandbox)
- **TMT6plex on K and peptide N-term (now confirmed):** the deposited mqpar sets TMT6plex as MaxQuant isobaric labels on Lys and N-term. These are annotated `MT=Fixed`, the usual SDRF encoding for an isobaric label. Note that mqpar `fixedModifications` lists only Carbamidomethyl, because MaxQuant keeps isobaric labels in a separate block.
- **HCD vs CID (unresolved; the only reason this is still sandbox):** the Methods say HCD at 40% NCE, but MaxQuant named the deposited peak lists `allSpectra.CID.FTMS.*`. mqpar has no dissociation field, and the RAW headers were not range-read (the cloud browser cannot do byte-range reads). I kept HCD as stated in the Methods.
- **E14 vs E14Tg2a (CVCL_9108, a child of CVCL_C320):** the paper says only "E14", so I annotated the parental ES-E14.
- `developmental stage` = blastocyst stage and `organism part` = blastocyst are taken from Cellosaurus (the origin of the line), not from the paper.
- The ontology accessions not checked live are MS, UNIMOD and PRIDE: EBI/OLS was unreachable. I matched their labels against this campaign's validated files. CL:0002322 and UBERON:0000358 were checked live on Ontobee.
- The value `not applicable` is not used. MS1 scan range is unstated and is omitted.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only`, with each of ms-proteomics, vertebrates and cell-lines: no errors. Ontology validation was skipped because the OLS dependencies are not installed. `sdrf_review.py`: [OK].

## Review status
pending
