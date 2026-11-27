# PXD053645 SDRF annotation report

## Study
"Co-IP protein identification of WT/MT IVNS1ABP in isogenic iPSCs derived NPCs" (Duke-NUS, lab head Su-Chun Zhang; announced 2026-01-23). This is a label-free AP-MS experiment. An anti-IVNS1ABP antibody was used to pull down interactors from iPSC-derived neural progenitor cells (NPCs) of one isogenic pair: the patient's mutant line and its gene-corrected control. An IgG IP serves as the negative control.

Paper: Yuan F, Tan YS, ... Reversade B, Zhang S-C. "IVNS1ABP mutation drives cellular senescence in newly identified progeroid neuropathy". Nat Commun (2026) 17:4159, DOI 10.1038/s41467-026-70756-x. It was read from the PolyU repository PDF (https://ira.lib.polyu.edu.hk/bitstream/10397/118246/1/s41467-026-70756-x.pdf). nature.com returned a client error. The PX record links the medRxiv preprint 10.1101/2024.10.12.24315363. Both the preprint and the Nat Commun article cite "PXD053645" in their data availability statements, so the PX→paper link is verified. No PMCID was found or used.

## Scope, evidence and decisions
- **Deposited files** (PROXI and the PRIDE FTP listing, both re-derived 2026-11-27): 12 files in total, 9 RAW plus `01Apr21_Duke_IP.pdResult` (2.2 GB), `01Apr21_Duke_IP.pdResultView` (108 MB) and `checksum.txt`. This matches the cached 9 RAW / 12 files. **All 9 RAW are annotated, 9 rows × 45 columns, and none is excluded.** Saved files: `scratch/PXD053645/filelist.txt`, `ftp_listing.txt`, `px_record_summary.txt`.
- **Run → sample map (bait vs control):**

  | RAW | Group (paper) | Cell lysate | IP antibody |
  |---|---|---|---|
  | `01Apr21_Duke_Control_R1-3.raw` | WT / "Ctrl" | Ctrl_III NPCs (gene-corrected) | anti-IVNS1ABP |
  | `01Apr21_Duke_MT_R1-3.raw` | MT | MT_III NPCs (patient, homozygous p.(Phe253Cys)) | anti-IVNS1ABP |
  | `01Apr21_Duke_IGG_R1-3.raw` | IgG control | **not stated** (pair III NPCs) | mouse IgG |

  STATED evidence: the Methods/legend say "n = 3 independent IPs per group: WT, MT, and IgG control; total = 9 samples". The PX description says "wild type (Ctrl) and MT IVNS1ABP". Fig. 5A/B are labelled "Ctrl_III NPCs" / "MT_III NPCs". The Results say "36 proteins in Ctrl NPCs and 30 proteins in MT NPCs ... compared to IgG control". The file tokens Control/MT/IGG match the three groups one-to-one. R1–R3 is taken as independent IP 1–3 (biological replicate). The paper states that there were three independent IPs, but the numbering comes from the file names.
- **Cell lines:** The paper says Pair III was generated "by correcting the mutation site" in an affected sibling. MT_III is therefore the patient iPSC line and Ctrl_III is its CRISPR/Cas9 + ssODN-corrected isogenic line. (There is also a KO line, but it is not used in this experiment.) The paper gives no RRID or hPSCreg name. Cellosaurus (api.cellosaurus.org, 2026-11-27) has no iPSC entry: `q=IVNS1ABP` returned 10 hits, all HAP1/HeLa/THP-1 KOs or unrelated lines, and `q="progeroid neuropathy"` returned 0. Cellosaurus accession and name are therefore `not available`, and `characteristics[cell line]` = the paper's line names Ctrl_III / MT_III. The iPSCs come from dermal fibroblasts (Sendai CytoTune 2.0), so `sampling site` = dermis and `organism part` = not applicable (in vitro-differentiated NPCs).
- **Genotype:** `characteristics[genotype]` and `factor value[genotype]` are "IVNS1ABP wild type (p.F253C corrected)" / "IVNS1ABP p.(Phe253Cys) homozygous". Using genotype requires declaring clinical-metadata, as in PXD054300. `characteristics[genetic modification]` records the CRISPR correction for Ctrl_III and is `not applicable` for the unedited patient line. The paper gives no c. notation or transcript.
- **Disease:** All lines in pair III come from one affected sibling, so the donor's disease is "progeroid neuropathy" (the paper's name) on every row, including the corrected line, following the cell-lines rule "disease of the donor". The syndrome is newly described, so **there is no MONDO term and the value is free text.**
- **Enrichment:** `characteristics[enrichment process]` and `factor value[enrichment process]` distinguish the anti-IVNS1ABP co-IP (mouse, Santa Cruz) from the IgG co-IP (mouse, Millipore). Both use Protein A/G magnetic beads and ~20 million NPCs per IP.
- **Culture medium (STATED for NPC derivation):** neural induction medium = DMEM/F12 + 100x N2 + 100x NEAA, written as 1x. The paper gives no separate NPC maintenance medium.
- **Prep:** EasyPep Mini MS Sample Prep Kit, "according to manufacturer's instructions". The kit user guide (MAN0018079) lists "Pierce Trypsin/Lys-C Protease Mix", so the cleavage agents are **Trypsin + Lys-C, INFERRED from the vendor kit and not named in the paper**. The kit's Reduction/Alkylation Solutions are not chemically identified, so reduction and alkylation reagent are `not available`.
- **MS (Methods):** EASY-nLC 1200, Orbitrap Exploris 480, MS1 60k at 350–1600 m/z, HCD at a fixed 28% NCE, MS2 at 15k, isolation 1.6 m/z. Proteome Discoverer 2.5.

## Conflicts
1. **Instrument: PX says LTQ Orbitrap Elite, the paper says Orbitrap Exploris 480.** I annotated **Exploris 480** (MS:1003028) because paper Methods take precedence over PX fields. Several parameters only make sense on the Exploris: normalized AGC target 300%/75%, MS2 Orbitrap at 15k, and first mass 120. PX's "LTQ Orbitrap Elite" is a known recurring default error. **The RAW headers were NOT read**: the shell has no network, and the cloud browser cannot range-read a 450 MB binary. This conflict is therefore unresolved by raw evidence.
2. **DDA vs DIA:** the Methods say the instrument "was operated in data-independent ... mode" but also "Peptides were then selected for ddMS2". I annotated **DDA (INFERRED)** for three reasons: the explicit ddMS2 selection, processing in PD 2.5 (a DDA search workflow; the deposited result is a `.pdResult`), and an AP-MS design with 15k MS2 at 1.6 m/z isolation. "Data-independent" is read as a wording error, but this is a judgement call.
3. The preprint says three affected siblings and the article says two (siblings 1 and 4). This makes no difference here.

## Values left not available / not applicable and why
- `age`, `sex`, `developmental stage`: **not available**. Neither the paper nor the preprint gives sex or age for any sibling ("teenaged"/"adolescent" members only).
- `individual` = `pairIII_donor`: the paper does not say whether sibling 1 or sibling 4 donated pair III.
- `cellosaurus accession` / `cellosaurus name`: **not available**, because there is no Cellosaurus entry (see above).
- **IgG rows:** `genotype` and `genetic modification` are **not available**. `cell line` is "isogenic pair III iPSC line (Ctrl_III or MT_III; IgG lysate line not stated)". The paper never says which lysate was used for the IgG IPs: Ctrl, MT or pooled. The column forbids reserved words, so the text says this explicitly.
- `precursor/fragment mass tolerance`, `modification parameters`: **not available**. The paper gives no PD search settings. The deposited `.pdResult` (2.2 GB) and `.pdResultView` (108 MB, SQLite) could not be range-read without shell network access. The kit implies carbamidomethylation, but under campaign rules modifications must come from the deposited search, so none are asserted.
- `reduction reagent` / `alkylation reagent`: **not available**, because the kit's reagents are proprietary and unnamed.
- Unstated, so omitted: NPC day used for the co-IP (the Methods only say "day 10 or day 20" in general) and passage number.

## Stated vs INFERRED (why sandbox)
- STATED: the three groups (WT/MT/IgG) × 3 independent IPs, the pair III lines and their genotypes, the IP antibodies, the Exploris 480 / HCD 28% / scan range, and the medium.
- INFERRED: the IgG lysate line (unknown, and flagged in the cell line value), R1–R3 = IP replicate 1–3, DDA, Trypsin + Lys-C (from the vendor kit), and the instrument choice against PX (not verified from RAW headers).

## Ontology checks
OLS4 was down or rate-limited (HTTP upstream reset and RATE_LIMIT on 2026-11-27). The following were verified live on Ontobee: MS:1003028 "Orbitrap Exploris 480", MS:1001309 "Lys-C", MS:1000422 "beam-type collision-induced dissociation", and CL:0011020 "neural progenitor cell". MS:1001251 Trypsin and PRIDE:0000627 DDA were not re-checked live; their labels match this campaign's validated files.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only` with ms-proteomics, human, cell-lines and clinical-metadata: "Everything seems to be fine. Well done." (structural only; the OLS extras are not installed). `sdrf_review.py`: [OK].

## To upgrade to annotated
- Range-read a RAW header (e.g. `01Apr21_Duke_MT_R1.raw`) for the instrument model and scan type.
- Read the `.pdResultView` SQLite (`Workflows` / `StudyInformation`) for search modifications, tolerances, enzyme and the file→sample grouping, which might name the IgG lysate.
- Alternatively, get the submitter or Supplementary Data 4 to state which NPCs were used for the IgG IPs.

## Review status
pending
