PARTIAL: 96 of 102 raw files are annotated in PXD007278.sdrf.tsv (diaCys experiment: 90 C. difficile files plus 6 BSA files). The 6 iodoTMT raw files are not annotated because no public source gives their channel-to-sample map.

Unmapped raw files:
- 150812_OV3_P5_RN_SuS_HCD_8uL_180min_1_1.raw (MaxQuant experiment sample1_1)
- 150812_OV3_P5_RN_SuS_HCD_8uL_180min_1_2.raw (sample1_2)
- 150812_OV3_P5_RN_SuS_HCD_8uL_180min_2_1.raw (sample2_1)
- 150812_OV3_P5_RN_SuS_HCD_8uL_180min_2_2.raw (sample2_2)
- 180112_OV3_P5_ATS_A_HCD_01.raw (BSA iodoTMT, sample_1)
- 180112_OV3_P5_ATS_B_HCD_02.raw (BSA iodoTMT, sample_2)

Sources checked for these files:
1. Paper (PMC5930413), Table I. It gives each C. difficile sample's two iodoTMT channels: control 1 126/127, control 2 127/128, control 3 128/129, diamide 1 129/126, diamide 2 130/131, diamide 3 131/130. It also gives the two pools: (control 1 + diamide 2 + control 3) and (control 2 + diamide 1 + diamide 3), each run in two technical replicates.
2. The deposited iodoTMT_result.zip mqpar.xml and summary.txt. They name the runs only sample1_1/1_2/2_1/2_2, with iodoTMT6plex-Cys126..131 and no condition names.
3. The PRIDE record and sample protocol: these repeat the paper text.
4. BSA_iodoTMT_result.zip mqpar.xml: sample_1 and sample_2 only. The paper does not describe the BSA iodoTMT channel layout.

Missing link: nothing public says which pool is MaxQuant "sample1" and which is "sample2". The only way to decide is to assume that sample1 is the pool the paper lists first. That is an inference, not evidence. For BSA there is no channel map at all.

What would unblock it: a statement from the authors (or any deposited table) linking sample1/sample2 to the two pools, and the BSA iodoTMT channel layout. These would go in a separate SDRF, PXD007278-iodotmt.sdrf.tsv, because TMT and the diaCys runs must not share one file.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above as unmapped have no public sample/channel map. Promote to `datasets/` only once they are resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Working files mentioned above (evidence/, validation output, scripts, tables) are not part of this submission.
- Review status: the SDRF(s) in this folder passed an independent fresh-context adversarial review.
