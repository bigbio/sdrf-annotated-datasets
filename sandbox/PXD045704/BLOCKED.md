BLOCKED: PXD045704 is a label-free (MaxLFQ) dataset, not SILAC, so it is out of scope for the SILAC annotation series it was queued in.

Evidence (all public):

- PRIDE project record (https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD045704): the description
  says "Max LFQ quantitative proteomics was employed in an approach incubating wild-type and control DNA
  with (unlabeled) nuclear extracts", the sample processing protocol says "38B9 preB cell nuclear
  extracts (non-labeled)", and `quantificationMethods` is `PRIDE:0000425` (MS1 intensity based
  label-free quantification). The `Silac` entry in `keywords` is the only SILAC mention and is
  contradicted by all of the above.
- Deposited MaxQuant output (`parameters.txt`, MaxQuant 1.6.14.0): no SILAC labels/multiplicity;
  `proteinGroups.txt` holds `LFQ intensity <experiment>` columns only, no `Ratio H/L` columns.
- Publication: Phongbunchoo et al. 2024, Cell Rep 43:114456, doi:10.1016/j.celrep.2024.114456, PMID 38990722
  (Europe PMC has abstract only; no open full text there). The article is gold open access at
  https://doi.org/10.1016/j.celrep.2024.114456 and in MPG PuRe
  (https://pure.mpg.de/pubman/item/item_3635981_1/component/file_3635982/10.1016_j.celrep.2024.114456.pdf),
  (PDF also at https://pure.mpg.de/rest/items/item_3635981_1/component/file_3635982/content).
  Its Methods say MaxQuant used "the Max LFQ algorithm for label-free data", with "label-free data
  acquired on Q Exactive and Exploris mass spectrometers"; PXD045704 is the only one of the four
  accessions acquired on an Exploris 480.

The sister datasets PXD045694, PXD045636 and PXD045637 (same study, same submitter) are SILAC
label-swap experiments and are annotated separately.

What a label-free annotation would look like (for whoever picks this up; not done here):

- 225 Thermo .raw files from an Orbitrap Exploris 480 (MS:1003028), trypsin, in-gel digest,
  8 gel slices (`gb01`-`gb08`) per lane, each slice injected twice (`_01`, `_02`).
- 14 lanes = 7 replicates (`Rep01`-`Rep07`) x 2 baits: wild-type Emu enhancer+MARs (`WT`) vs.
  E1-box-mutant (`E1mt`). Nuclear extract from the A-MuLV-transformed 38B9 mouse pro-B cell line (per the article) (Mus musculus).
- The lane -> bait map is in the `proteinGroups.txt` experiment names
  (`WT_Rep{n}_{A,C,E,G,I,L,O}`, `E1mt_Rep{n}_{B,D,F,H,K,M,P}`). Note that the Rep06 control lane is
  named `M_EnhancerMAR_WT_E1mt` in its raw files but is `E1mt_Rep6_M` in the search output.
- Irregular files to handle explicitly: `Rep01_00001617___B_EnhancerMAR_E1mt_gb07b_01.raw` (B lane,
  slice 7 has `_01`, `_02` and `07b_01`, 17 files for that lane), and
  `Rep07_00001792___P_EnhancerMAR_E1mt_gb05_02b.raw` (stands in for `gb05_02`).
- MaxQuant settings: fixed Carbamidomethyl (C); variable Oxidation (M), Acetyl (Protein N-term),
  Deamidation (NQ).
- Cell stage of 38B9: PRIDE says "preB", but the article calls it "A-MuLV-transformed 38B9 pro-B
  cells" and lists "38B9 pro B cell line (Alt et al., 1984)" in its key resources table. Follow the
  article: CL:0000826 "pro-B cell" (CL:0000817 "precursor B cell" is a different, later stage).
  38B9 has no Cellosaurus entry. Culture medium per the article: RPMI 1640, 10% FCS.
- PRIDE lists disease "lymphoma" (DOID:0060058); this is a submitter field and needs confirming
  from the article before it is used.

Unblock: annotate as a label-free dataset (`ms-proteomics` + `vertebrates` + `cell-lines`) in a
label-free pass, or confirm with the submitter that no SILAC runs exist for this accession.

No SDRF is provided here.
