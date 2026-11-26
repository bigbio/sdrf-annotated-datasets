# PXD007704: chronic wound-associated fibroblasts (cWAF), triple SILAC with super-SILAC mix

BLOCKED: one SILAC channel cannot be assigned a sample from public evidence. The depositor's
ReadMe.docx lists WAF1 Exp6 (`20150304_BB_WAF1_Exp6_01..10`) as Heavy SSM / Medium 4NHF /
Light 4NHF, i.e. 4NHF twice. The medium channel is annotated with the placeholder source
`UNRESOLVED_WAF1_Exp6_medium` and no sample-specific values. Promote to `datasets/` once the
authors (or the paper's supplement) confirm the sample.

Sources: [PRIDE PXD007704](https://www.ebi.ac.uk/pride/archive/projects/PXD007704);
[ReadMe.docx](https://ftp.pride.ebi.ac.uk/pride/data/archive/2020/10/PXD007704/ReadMe.docx);
[MaxQuant_Output.zip](https://ftp.pride.ebi.ac.uk/pride/data/archive/2020/10/PXD007704/MaxQuant_Output.zip)
(summary.txt, parameters.txt, experimentalDesignTemplate.txt, proteinGroups.txt); Berberich et al.,
J Invest Dermatol 2020;140(11):2280-2290.e4, PMID 32305317, doi:10.1016/j.jid.2020.02.040.
Only the abstract was reachable: Europe PMC has no full text and the publisher returns HTTP 403.

## What is annotated

- 190 RAW files = 19 triple-SILAC experiments x 10 SDS-PAGE gel slices; 570 rows (3 channels per file).
- Channel map from the ReadMe tables. Light = Arg0/Lys0, Medium = Arg6/Lys4, Heavy = Arg10/Lys8
  (MaxQuant Labels1/Labels2). Experiment-to-file and fraction numbers come from
  experimentalDesignTemplate.txt.
- The super-SILAC mix (SSM) is a pooled reference, one source per run (`SSM_<run>`), so that
  `comment[technical replicate]` stays constant within each file. Its composition is not stated.
- The sample groups and diseases are taken from the ReadMe:
  - cWAF1-5 and cWAF_RDEB: chronic ulcer of skin.
  - RDEB CL and RDEB PP: recessive dystrophic epidermolysis bullosa.
  - aWAF44 and aWAF59: skin wound.
  - 4NHF, 9NHF, NHF1 and NHF2: normal.
  - NHF1 and NHF2 + TGFbeta: normal, with treatment TGF-beta.
  Per the ReadMe, the paper uses only the NHF, cWAF and NHF+TGFbeta channels. The RDEB and aWAF
  channels are annotated because their raw files are deposited.
- Instrument LTQ Orbitrap XL for all files. For 120 files this comes from MaxQuant summary.txt; for
  the 70 later files it comes from the raw-file headers of one file per batch. The method is
  Top5 DDA with CID at 35 NCE and ion-trap MS2. The fragment tolerance is 0.5 Da (ITMS).
- `characteristics[biological replicate]` numbers repeated measurements of the same named
  fibroblast population across experiments. Channels with different labels are necessarily
  separate SILAC cultures; channels with the same label may be the same culture.

## Open points

1. WAF1 Exp6 medium channel (the block). Channel ratio profiles from proteinGroups.txt correlate
   r=0.79 with WAF1 Exp1 medium (RDEB CL) and at most 0.31 with any 4NHF channel. With RDEB CL in
   that channel, the WAF1 label-swap design would be complete (every sample measured twice). This
   is an inference, not a published map, so it is not annotated.
2. Donor age, sex and ancestry; wound location; TGFbeta isoform and dose; SSM composition. These
   are not in the deposit, and the paper's full text was unreachable.
3. `comment[precursor mass tolerance]` is `not available`. MaxQuant 1.4.1.2 parameters.txt does not
   record it, so `parse_sdrf convert-openms` refuses the file.
4. cWAF_RDEB is annotated by wound type (chronic ulcer of skin). The underlying RDEB is implied
   only by the sample name.

Validation: `parse_sdrf validate-sdrf -t ms-proteomics -t human` passes, as does each template
alone. Checked 2026-11-23.
