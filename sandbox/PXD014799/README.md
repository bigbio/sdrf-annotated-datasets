PARTIAL: 231 of 255 raw files of PXD014799 are annotated (PXD014799-silac.sdrf.tsv: 177 SILAC files; PXD014799-labelfree.sdrf.tsv: 54 label-free co-IP files). The 24 files below are not annotated, because no public source gives their channel->condition map.

Unmapped files:

1. F150714_DM__PRMT1KD_* (24 files: INPUT_FWD_1-9_ingel, INPUT_REV_1-9_ingel, FWD_pepIP_MONO/ASYM/SYM, REV_pepIP_MONO/ASYM/SYM). This is the standard SILAC PRMT1 knockdown experiment, searched as txt_PRMT1KD_STD_SILAC. Its summary.txt gives each file's experiment (DM_KD_FWD_input, DM_KD_FWD_IP, DM_KD_REV_input, DM_KD_REV_IP) and the heavy label (Arg10;Lys8, Multiplicity 2). But neither the paper nor Tables S1-S4 say which condition (control vs PRMT1 knockdown, with or without CDDP) is in the light or heavy channel. Table S1 lists only the triple-total, triple-nuclear and standard UT/CDDP designs. The map is not inferred from the data.

Mapped since the previous version (from the deposited MaxQuant summary.txt files plus Table S1):
- F150414_DM_* (10) and F150604_PepIP_* (4): standard SILAC UT/CDDP (txt_CDDP_STD_SILAC: DM_CDDP_FWD_input, DM_CDDP_FWD_IP, DM_CDDP_REV_IP).
- HF190404_RG_* (27, forward) and HF190619_MMRG_* (27, reverse): triple SILAC nuclear extract (txt_TripleSILAC_nuclearextract: FWD_/REV_input, me1 = IP_MMA, me2 = IP_ADMA).

Sources checked: the paper (Musiani et al. 2020 Cell Rep, full text mmc6.pdf), Tables S1-S4 (mmc2-mmc5.xlsx), the PRIDE project record and file list, the PRIDE protocol text, summary.txt and parameters.txt of all four deposited MaxQuant txt zips (evidence/txt_*/), the proteinGroups_PRMT1_coIP.txt header, the raw-file headers of 25 files for the instrument (evidence/raw_header_instrument.txt), and the method section of 55 raw headers, at least one per file group, for the MS1 scan range and collision energy (evidence/raw_method_settings.txt).

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the 24 F150714 files listed above have no public channel map. Promote to `datasets/` only once they are resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Working files mentioned above (evidence/, validation output, scripts, tables) are not part of this submission.
- Review status: the two SDRFs in this folder passed an independent fresh-context adversarial review (third round, after fixes for instrument, coverage, MS1 scan range, collision energy and label-free modifications).
