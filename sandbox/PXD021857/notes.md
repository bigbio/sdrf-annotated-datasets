# PXD021857

BLOCKED: this is not a SILAC dataset, and 5 of the 63 raw files have no verifiable sample/channel map (listed below).

Stopfer LE et al. *High-Density, Targeted Monitoring of Tyrosine Phosphorylation Reveals Activated
Signaling Networks in Human Tumors.* Cancer Res 2021;81(9):2495-2509. PMID 33509940, PMC8137532.

## Why this is in sandbox

- **No metabolic SILAC.** PRIDE lists `SILAC` and `TMT` as quantification methods. The "heavy"
  channel is a synthetic stable-isotope-labelled (SIL) pTyr peptide internal-standard mix: about
  1 pmol of each peptide is spiked into the digest before enrichment. The SureQuant acquisition is
  triggered by these standards. The endogenous sample itself is unlabelled.
  - So the SureQuant rows are `label free sample`, and the standards go in
    `characteristics[spiked compound]`. This follows SAMPLE-GUIDELINES "Spiked-in Samples", which
    covers quantification standards.
  - The heavy-label masses come from the deposited Skyline exports: R +10, K +8, A +4, I +7, V/P +6.
    They are listed as `comment[modification parameters]` (UNIMOD:267/259/1297/695/268).
- **`A549_EGF_pTyr_TMT_DDA.raw` is not annotated.** It is a TMT10 DDA run of the A549 EGF time
  course. Its channel-to-sample map is only in the paper's supplementary tables S4/S5 (NIHMS1669161),
  which could not be retrieved. The deposited PSM file gives only `Abundance 126..131`.
- **The discovery TMT10 runs are not annotated.** These are `DiscoveryCRC_TMT_1/2/4.raw` and
  `DIscoveryCRC_TMT_3.raw`, on a Q Exactive HF-X.
  - The deposited `CRC_Discovery.xlsx` "Table 1" gives the channel map for "Analysis 1-4": 5 matched
    adjacent-normal/tumour pairs per plex, with normal on 126/127C/127N/128C/128N and tumour on
    129C/129N/130C/130N/131, identified by CPTAC IDs.
  - No public source says which Analysis is which raw file. The original acquisition names in the
    raw headers are `20180830_CRC_run1_spindirectload`, `20180904_CRC_run3`, `_run4` and `_run6`.
  - An independent review failed an index-based mapping, so these runs are left out until the link
    is confirmed.

## Annotated here

Both files below pass `parse_sdrf validate-sdrf` for every template they declare.

| file | runs / rows | templates | design |
|---|---|---|---|
| `PXD021857-crc-tumors-surequant.sdrf.tsv` | 34 / 34 | ms-proteomics, human | 31 CPTAC colon tumours (T1-T31) plus Tumor32 in triplicate; SureQuant pTyr on an Exploris 480 |
| `PXD021857-a549-benchmark.sdrf.tsv` | 24 / 24 | ms-proteomics, human, cell-lines | A549 + EGF: SureQuant reproducibility (3 runs), label-free DDA (3), and EGF 0/0.5/2 min x 3 by both SureQuant and PRM (18) |

## Open points

- Per-patient demographics and the mapping from T1-T31 to CPTAC IDs are in Supplementary Table S7,
  which could not be retrieved, so age and sex are `not available`.
- It is not stated whether Tumor32 is one of T1-T31, or whether its three runs are separate
  enrichments or re-injections. Its runs used a different method file from T1-T31.
  - The raw headers of `Tumor32_pTyr_SQ_{1,2,3}.raw` carry the original names
    `20200916_Tumor25_SQ_{1,2,3}_inj2`, which may make it the same tumour as T25.
  - No public source links that lab numbering to the paper's T25, so individual is `not available`.
- `sdrf-tools reconcile` flags `labelled_annotated_as_label_free` because PRIDE lists SILAC.
  This is a false positive: the heavy species are spiked synthetic standards.
- `QY=1 pmol` in `characteristics[spiked compound]` is the amount of each IS peptide, not of the
  whole mix.
- Search tolerances and the fixed/variable status of modifications are in the supplementary methods,
  which could not be retrieved. The tolerance columns are omitted.
- `sdrf-tools check` flags UNIMOD:1297 and UNIMOD:695. These are false positives: both resolve in OLS4.

## Return criteria

- Sample sheets that link each TMT channel to its sample and each "Analysis" to its raw file. With
  them, the remaining 5 runs can be added. Re-review before promoting to `datasets/PXD021857/`.
- The campaign also needs to decide whether SIL-peptide (SureQuant) datasets count as SILAC.
