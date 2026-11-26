PARTIAL: PXD008642. 54 of 114 deposited raw files are annotated, in two label-free SDRFs. The other 60 files have no public file-to-sample or channel-to-sample evidence.

# PXD008642: ISE-affinity proteogenomics of breast cancer cell lines and tissues

Annotated (label-free, LTQ Orbitrap Velos, MaxQuant LFQ searches):

- `PXD008642-tissue.sdrf.tsv`: 48 files. Clinical tissues from 4 patients (2 luminal ER+/PR-, 2 basal triple-negative). Each patient gave tumour tissue (code B) and adjacent non-malignant tissue (code A), and each tissue was pulled down with an ISE RNA probe and with a non-ISE control probe. File-to-sample map: the deposited `Clinicaltissues_LFQ_ISE.zip` mqpar.xml (filePaths aligned with experiments). Tissue codes come from Table S2 (mmc3.xlsx, Description sheet).
- `PXD008642-cellline.sdrf.tsv`: 6 files. T-47D, ISE probe and control probe, 3 technical replicates each. Map: the deposited `Cellline_LFQ_ISE.zip` mqpar.xml (cT47D_n / T47D_n).

## Unmapped files (60)

### AACT/SILAC cell-line runs (48 files): BLOCKED

These are the 3-plex SILAC (AACT) ISE pull-downs of MCF10A, T47D and MDA-MB-231:

- `AS_RNA1_120417150936.raw`, `AS_RNA2.raw` ... `AS_RNA24.raw` (24 files, `Cellline_AACT_ISE_Run1.zip`)
- `AS_RNA_Rep_1_120530182118.raw` ... `AS_RNA_Rep_24_120601190832.raw` (24 files, `Cellline_AACT_ISE_RepeatRun.zip`)

The rungs of the channel-map ladder checked were:

1. Paper STAR Methods (Cell Lines). It says: "MCF10A or MDA-MB-231 cells were cultured in DMEM medium containing 13C614N2-Lysine/13C614N4-arginine (Heavy) ..., whereas T47D cells were cultured in ... 13C6-Lysine/13C6-arginine (Medium)". T47D is therefore the medium channel. The text does not say which of MCF10A and MDA-MB-231 is light and which is heavy, and "MCF10A or MDA-MB-231 ... Heavy" could also describe a label swap between the two replicates.
2. Deposited mqpar.xml files (MaxQuant 1.2.2.5). Labels are none / Arg6;Lys6 / Arg10;Lys8, with no experiment names. proteinGroups.txt has only the generic columns `Ratio M/L`, `Ratio H/L` and `Ratio H/M`.
3. Table S1 (mmc2.xlsx), AACT sheet. It reports log2 `MDA231/MCF10A` and `T47D/MCF10A` ratios, and the methods say ratios are M/L or H/L. This suggests L = MCF10A and H = MDA-MB-231, but that conflicts with the "MCF10A ... (Heavy)" sentence, and no per-run orientation is published.
4. Whether the 24 files per run are gel-slice fractions of one mixed sample is also not stated explicitly. The paper says AACT used the gel-based (in-gel digestion) route.

The per-file channel assignment cannot be evidenced, so no SILAC SDRF is written.

### Cell-line LFQ runs not named in any deposited search (12 files)

- `LW061815_LX_Con_6_1_1.raw`, `LW061815_LX_Con_6_1_2.raw`, `LW061815_LX_Con_6_1_3.raw`
- `LW061815_LX_Con_6_4_1.raw`, `LW061815_LX_Con_6_4_2.raw`, `LW061815_LX_Con_6_4_3.raw`
- `LW061815_LX_ISE_5_1_1.raw`, `LW061815_LX_ISE_5_1_2.raw`, `LW061815_LX_ISE_5_1_3.raw`
- `LW061815_LX_ISE_5_4_1.raw`, `LW061815_LX_ISE_5_4_2.raw`, `LW061815_LX_ISE_5_4_3.raw`

The deposited cell-line mqpar names only the `_6_2` and `_5_2` files (T47D) and the `_6_3` and `_5_3` files (HCC1806, not deposited). The deposited proteinGroups.txt in the same zip holds cMCF10A/MCF10A experiments, and Table S1 reports MDA-MB-231 and T47D. The `_1` and `_4` series are plausibly MCF10A and MDA-MB-231, but no public source states which is which.

What would unblock: the authors' experimental design for the AACT runs (channel per cell line per replicate) and for the LX `_1` / `_4` series.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above as unmapped have no public sample/channel map. Promote to `datasets/` only once they are resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Working files mentioned above (evidence/, validation output, scripts, tables) are not part of this submission.
- Review status: the SDRF(s) in this folder passed an independent fresh-context adversarial review.
