# PXD027027 SDRF annotation report

## Study
A prion-like protein from a red-type pyrenoid forms heterotypic Rubisco condensates via sticker tetrads
(PX title). Published as Oh ZG et al., "A linker protein from a red-type pyrenoid phase separates with Rubisco via
oligomerizing sticker motifs", PNAS 2023;120(25):e2304833120, doi 10.1073/pnas.2304833120, PMID 37311001,
PMCID PMC10288592. The paper's Data Availability section and the SI Methods both cite PXD027027, so the PX link is correct.

## Scope, evidence and decisions
sandbox: 5 rows (5 RAW x label free), 30 columns, template ms-proteomics only.

- **Deposited vs annotated.** ProteomeCentral PROXI (resultType=full) lists 29 files: 5 .raw, 10 .msf (Phatr2a + SwissProt
  search of each run), 12 .txt (protein/peptide exports, Overall_Summary.txt, Explanatory_Information.txt),
  Phatr2a_Database.fas and a gel/WB PDF. All 5 RAW are annotated, so the campaign cache count (5 RAW / 29 files) is correct.
  No runs were excluded.
- **Organism.** The organism is *Phaeodactylum tricornutum* (diatom), not *Chlamydomonas reinhardtii* or a recombinant system.
  The SI Methods describe anti-Rubisco co-IP from *P. tricornutum* soluble lysate. *C. reinhardtii* Rubisco and *E. coli*-expressed
  PYCO1 and other Rubiscos were used only in the in-vitro LLPS, activity and cryo-EM work, not for MS. The SI states the strain:
  "Phaeodactylum tricornutum Pt 1 8.6, CCMP 2561". The PX record gives strain-level NCBITaxon:556484 (*P. tricornutum* CCAP 1055/1).
  I annotated species-level NCBITaxon:2850 because the paper names the strain only as Pt1 8.6/CCMP2561, and equating it with
  CCAP 1055/1 would be my inference. Both taxa were checked live through NCBI eutils esummary and are in the OLS cache.
  `characteristics[strain or breed]` was not used because ms-proteomics alone does not license it; the strain is recorded here only.
- **Samples and run mapping.** Results text: Rubisco was isolated by immunoprecipitation from soluble algal lysate, and "In
  three of five samples, the algae were exposed to dithiobis(succinimidyl propionate) prior to lysis". The SI gives 4 mM DSP
  for 30 min at room temperature in Co-IP XL buffer, quenched with Tris. The deposited file names carry the submitter's own
  `XL_` prefix on exactly 3 of the 5 runs (XL_IP_Rbc_1/2/3), and the other 2 runs (IP_Rbc_1/2) have no prefix. This matches
  the stated 3/5 split, so the files map as 3 DSP and 2 no crosslinker. Biological replicate numbers follow the file-name
  indices within each arm. The no-antibody bead control was not analysed by LC-MS/MS (stated), so no control rows exist.
  DSP is used here as an in-vivo interaction-stabilising treatment, not for XL-MS (no crosslink search is described), so the
  crosslinking template was not declared. The treatment is recorded as free text in characteristics[treatment] and as the
  factor value.
- **Sample prep.** 50 mL mid-log cultures were lysed with glass beads (Co-IP buffer + 1 mM PMSF, 5 mM DTT). Protein A Sepharose
  carried rabbit anti-Rubisco large subunit antibody, and elution was in SDS loading buffer. The eluate was stacked into a single
  12% gel layer, excised, and digested in-gel with trypsin "as described (Shevchenko et al. Nat Protoc 2006) with some
  modifications". There is one gel band per sample, so the fraction identifier is 1 and the fractionation method is not
  applicable.
- **MS.** The SI states a Dionex Ultimate 3000 RSLCnano with an EASY-Spray 75 um x 10 cm PepMap C18 column, a 60 min gradient at
  300 nL/min, and a Q Exactive with EASY nanospray at 1.5 kV. The instrument is Q Exactive (MS:1001911) in both the paper and PX.
  The search used Proteome Discoverer 2.1 with Mascot against the *P. tricornutum* nuclear genome DB (Phatr2a) and SwissProt.
- **Culture medium.** Stated as modified F/2 (artificial sea salt), at room temperature under continuous light of about
  100 umol m-2 s-1. ms-proteomics alone licenses no growth-condition column, so this is recorded here only.

## Values left not available / not applicable
- comment[modification parameters], comment[reduction reagent], comment[alkylation reagent]: **not available**. The paper does
  not state search modifications or reduction/alkylation reagents, and the PX record says "No PTMs". The authoritative source
  is the 10 deposited PD 2.1 .msf files, but the PRIDE FTP and the PRIDE API were unreachable from the cloud browser all session
  (upstream connect timeout, 4 attempts). The Shevchenko in-gel protocol normally includes DTT/IAA, but "with some
  modifications", so I asserted nothing.
- comment[precursor/fragment mass tolerance], comment[collision energy], comment[ms1 scan range]: **not available** (not stated;
  .msf/.raw unread).
- comment[fractionation method]: **not applicable** (single stacked gel band).
- characteristics[organism part], [cell type], [disease]: **not applicable** (unicellular alga culture).

## Stated vs INFERRED
- Stated: organism and strain, co-IP design, 3 of 5 samples DSP-treated, DSP conditions, trypsin in-gel digestion, Q Exactive,
  PD 2.1/Mascot, absence of an MS-analysed control.
- From the submitter's file names, consistent with the stated count: which 3 runs are DSP (the `XL_` prefix).
- INFERRED: Data-dependent acquisition (Q Exactive with PD/Mascot search, 2016; the acquisition mode is not stated) and HCD
  dissociation (the Q Exactive fragments only by HCD). Also inferred: that the replicate indices are independent cultures and
  that the same index in the two arms (e.g. IP_Rbc_1 and XL_IP_Rbc_1, both 160927) are not paired. No pairing was encoded.

## Conflicts
- PX organism is strain-level CCAP 1055/1 (556484), while the paper names Pt1 8.6 / CCMP2561. I annotated species 2850 (see above).
- PX "No PTMs are included" conflicts with the near-certain search modifications in the .msf. These were left not available
  rather than guessed.
- Some .msf file names spell the initials "OhZG", but the raw files use "OhGZ". This is cosmetic, and the raw names were used verbatim.
- The WebFetch tool returned another accession's (PXD004355) Europe PMC payload for my queries. It was discarded, and the paper
  was read through the cloud browser from PMC and the SI PDF.

## Why sandbox
The run-to-sample mapping is defensible, but the search modifications, reduction/alkylation and tolerances are unresolved
pending a read of the deposited .msf (Workflows node), and no raw header was read to confirm the instrument. To upgrade to
annotated, read one .msf by HTTP-range (SQLite Workflows XML) and the first ~256 KB of one .raw once the PRIDE FTP is reachable.

SDRF file(s): PXD027027.sdrf.tsv. Built by script and validated with `parse_sdrf validate-sdrf --template ms-proteomics
--use_ols_cache_only` (ci-venv with the ontology cache). The only warnings are the free-text treatment values and an
HCD label/accession check that cannot be done offline. The BigBio `sdrf_review.py` gate prints [OK].
Evidence saved in /home/claude/singapore2/scratch/PXD027027/ (files.txt, proxi_summary.txt, paper_notes.txt).

## Review status
pending
