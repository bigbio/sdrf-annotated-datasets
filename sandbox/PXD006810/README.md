# PXD006810 — NleB arginine GlcNAcylation (EPEC / *Citrobacter rodentium* infection)

Scott NE, Giogha C, Pollock GL, Kennedy CL, Webb AI, Williamson NA, Pearson JS, Hartland EL.
*The bacterial arginine glycosyltransferase effector NleB preferentially modifies Fas-associated
death domain protein (FADD).* J Biol Chem 2017. PMID
[28860194](https://europepmc.org/article/MED/28860194), doi:10.1074/jbc.M117.805036.
Dataset: [PXD006810](https://www.ebi.ac.uk/pride/archive/projects/PXD006810).

Two files, because organism templates are mutually exclusive and the deposit mixes human cell
lines with mouse tissue:

| file | runs | rows | templates |
|---|---|---|---|
| `PXD006810-human.sdrf.tsv` | 97 human runs (HeLa triple-SILAC proteomes, HeLa Arg-GlcNAc pulldowns and inputs, EPEC infection of HT-29, human PRM) | 221 | `ms-proteomics` v1.1.0, `human` v1.1.0, `cell-lines` v1.1.0 |
| `PXD006810-mouse.sdrf.tsv` | 8 mouse colon runs (*C. rodentium* WT vs Δ*nleB*, days 4 and 8) | 8 | `ms-proteomics` v1.1.0, `vertebrates` v1.1.0 |

All 105 deposited `.raw` files are claimed exactly once (each SILAC run three times, one row per
label channel). Both files pass `parse_sdrf validate-sdrf` against their declared templates.

## BLOCKED: the SILAC channel → condition map is not publicly resolvable

The 62 `Nsco_NleB_SILAC_*` runs are a **triple SILAC** experiment (MaxQuant multiplicity 3;
`Labels1 = Arg6;Lys4`, `Labels2 = Arg10;Lys8`), and the paper's Experimental Procedures give the
three media recipes (light = L-Arg/L-Lys; medium = L-[13C6]Arg/d4-L-Lys; heavy =
L-[13C6,15N4]Arg/L-[13C6,15N2]Lys). The study design is also stated (Fig. 7A: FLAG-NleB1 and
FLAG-NleB1<sup>DXD</sup> lines induced with doxycycline for 2, 8 or 24 h, compared with uninduced
controls). **No public source says which culture went into which channel.**

Rungs checked:

1. Paper (PMC5655511) Experimental Procedures and the Fig. 7 legend — design and label recipes
   present, channel assignment absent.
2. Every deposited PRIDE file — the MaxQuant `summary-*`/`proteinGroups-*` tables name the nine
   SILAC experiments only `1`–`9` and the ratio columns only `M/L`, `H/L`, `H/M`; the deposit
   contains no sample sheet.
3. Europe PMC supplementary files — refused: *"Article with id PMC5655511 is not open access one"*.
4. Publisher supplementary tables (supplemental Table 8 holds the SILAC result) — PMC's
   supplementary download returns a reCAPTCHA interstitial; jbc.org returns HTTP 403.
5. No external repository (Zenodo/figshare/OSF/GitHub) is cited for a layout file.

Consequently `characteristics[genotype]`, `factor value[genotype]` and
`characteristics[sampling time]` are `not available` on all 186 SILAC rows: the channels are
annotated honestly as light/medium/heavy, but the condition behind each channel is **not** invented.
That is why this accession sits in `sandbox/` although both files validate.

**To unblock:** supplemental Table 8 of the paper (or any layout file from the authors) stating
which condition and induction time was light, medium and heavy in each of the three SILAC sets.
Then fill the three columns above and promote the folder to `datasets/`.

## Points a human reviewer should confirm

- **Cell-line identities.** `HeLa` (ectopic-expression and SILAC runs) and `HT-29` (EPEC
  infection runs) come from two sentences of the paper's Results — *"Using HeLa cell lines stably
  expressing doxycycline-inducible FLAG-NleB1"* and *"within HT-29 cells during EPEC infection"* —
  read through the PMC article page. Neither line is named in the PRIDE record, the deposited
  MaxQuant files or the raw-file headers, and the article is not open access, so this cannot be
  re-verified from a saved copy here. The split is corroborated by two verifiable facts: the runs
  annotated HeLa are exactly those searched against `HUMAN.fasta;NleB.fasta` on the Q Exactive, and
  the runs annotated HT-29 are exactly those searched against the EPEC E2348/69 FASTA on the Lumos.
  All demographics hang off these identities via Cellosaurus (CVCL_0030, CVCL_0320).
- **Two user-defined characteristics columns.** `characteristics[infection]` is not in the spec's
  `TERMS.tsv`, and `characteristics[genotype]` is defined only by templates not declared here. They
  carry free text because `characteristics[organism]` is single-valued (so it cannot also hold the
  pathogen) and `characteristics[treatment]` accepts only NCIT/EFO terms, which do not cover these
  strain and construct descriptions. Happy to rename or drop them if the repo prefers.
- **`comment[label]` is written bare** (`SILAC light`, `label free sample`), which matches the
  `ms-proteomics` template's own examples and validates cleanly, but the two files already in
  `datasets/` use the `NT=…;AC=…` form. Say the word and it can be switched.

## Other open points

- `comment[precursor mass tolerance]` is `not available` — the deposited MaxQuant
  `parameters-*.txt` record only `MS/MS tol. (FTMS) 20 ppm`. `parse_sdrf convert-openms -t2`
  therefore exits 1 (`Cannot read precursor mass tolerance`) for both files; `validate-sdrf` passes.
- UNIMOD has no arginine-specific GlcNAc entry. MaxQuant's custom `Arg_GlcNAc` is written as
  `NT=HexNAc;AC=UNIMOD:43;TA=R;MT=Variable` — correct composition and mass (+203.0794) with a
  target amino acid Unimod does not list for that term.
- Mouse strain, sex and age, the digestion detail (a possible Lys-C/trypsin double digest) and the
  reduction/alkylation reagents are not in the deposit and the article is not open access, so they
  are left as reserved words rather than written from a summarised reading of the Methods.
- Only the three `*_input_*` runs name their NleB1 construct (`WT` / `DXD`). The three
  `NleB_Arg_pulldown_sample*` runs say only that FLAG-NleB1 was ectopically expressed, and the two
  `arg_glycosylation_peptide_pulldown_160516` runs name neither construct nor cell line (a
  glycopeptide-bait pulldown need not use an NleB-expressing line), so their genotype is
  `not available`. The batch-wide `HUMAN.fasta;NleB.fasta` search database cannot tell wild type
  from DXD and is not used to.
- `characteristics[enrichment process]` is `not applicable` on the runs the deposit names `input`
  (unenriched proteomes) but `not available` on the PRM runs: the deposit does not say whether the
  targeted measurements were made on antibody-enriched or unenriched material.
- The strain infecting `Nsco_Arg_glycosylation_nleB_EPEC_rep1-3_20161004_EThcD` is not identifiable
  from the run name or the deposited search outputs (`characteristics[infection]` = `not available`).
- Three runs named in the deposited summaries (both D4 cecum inputs and the D4 cecum PRM run) are
  not in the PRIDE file list and are absent here; conversely
  `Nsco_NleB_SILAC_20160609_B3_exp2_fraction5_failed.raw` and the three `Arg_pulldown_input_*` runs
  are deposited but appear in no deposited search output.

Modifications are per-run too: each row carries only the modifications its own deposited search
used (`Variable modifications` in the corresponding `summary-*.txt`), so the 21 EPEC
infection/PRM runs carry no protein N-terminal acetylation, the four mouse input runs carry no
Arg-GlcNAc, and the four runs that appear in no deposited search output carry `not available`
rather than a borrowed search space. The enzyme is `Trypsin/P` (MS:1001313), as the summaries state.

Instrument, dissociation method, acquisition mode and MS1 scan range are per-run values read from
each raw file's embedded Xcalibur instrument method (first 400 kB of each file), not from the
project-level dropdowns: 70 runs on a Q Exactive (HCD), 35 on an Orbitrap Fusion Lumos (EThcD, or
HCD for the mouse inputs), with the `*_PRM_*` runs acquired by targeted inclusion-list methods.
