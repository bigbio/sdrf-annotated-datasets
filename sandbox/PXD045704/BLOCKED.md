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
  (Europe PMC has abstract only; no open full text).

The sister datasets PXD045694, PXD045636 and PXD045637 (same study, same submitter) are SILAC
label-swap experiments and are annotated separately.

What a label-free annotation would look like (for whoever picks this up; not done here):

- 225 Thermo .raw files from an Orbitrap Exploris 480 (MS:1003028), trypsin, in-gel digest,
  8 gel slices (`gb01`-`gb08`) per lane, each slice injected twice (`_01`, `_02`).
- 14 lanes = 7 replicates (`Rep01`-`Rep07`) x 2 baits: wild-type Emu enhancer+MARs (`WT`) vs.
  E1-box-mutant (`E1mt`). Nuclear extract from the 38B9 mouse pre-B cell line (Mus musculus).
- The lane -> bait map is in the `proteinGroups.txt` experiment names
  (`WT_Rep{n}_{A,C,E,G,I,L,O}`, `E1mt_Rep{n}_{B,D,F,H,K,M,P}`). Note that the Rep06 control lane is
  named `M_EnhancerMAR_WT_E1mt` in its raw files but is `E1mt_Rep6_M` in the search output.
- Irregular files to handle explicitly: `Rep01_00001617___B_EnhancerMAR_E1mt_gb07b_01.raw` (B lane,
  slice 7 has `_01`, `_02` and `07b_01`, 17 files for that lane), and
  `Rep07_00001792___P_EnhancerMAR_E1mt_gb05_02b.raw` (stands in for `gb05_02`).
- MaxQuant settings: fixed Carbamidomethyl (C); variable Oxidation (M), Acetyl (Protein N-term),
  Deamidation (NQ).
- PRIDE lists disease "lymphoma" (DOID:0060058): 38B9 is an Abelson-MuLV transformed pre-B cell
  line, so this needs a Cellosaurus check rather than being copied from the dropdown.

Unblock: annotate as a label-free dataset (`ms-proteomics` + `vertebrates` + `cell-lines`) in a
label-free pass, or confirm with the submitter that no SILAC runs exist for this accession.

No SDRF is provided here.
