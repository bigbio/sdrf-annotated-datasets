# PXD025304

BLOCKED: 52 of the 106 raw files (104 of 212 rows) cannot be tied to a SILAC channel → sample map from public evidence. The other 54 files are fully resolved. The file stays in `sandbox/` until the rest can be resolved.

Study: Geijer et al. 2021, *Nat Cell Biol* 23:608-619, "Elongation factor ELOF1 drives transcription-coupled repair and prevents genome instability" (doi:10.1038/s41556-021-00692-z, PMID 34108662, PMC7611218). The design is SILAC duplex (Lys6/Arg10) interaction proteomics with forward/reverse label swaps. Samples were separated by SDS-PAGE gel slices, with one raw file per slice.

## Resolved (54 files, rows 1-108)

| Files | Experiment (MaxQuant name) | Paper | Channels |
|---|---|---|---|
| `2149_..._FW_12-22` / `Rev_1-11` | Pol II P-Ser2 IP, HCT116 WT vs ELOF1-/-A, unperturbed ("Basal complex") | Fig. 2g | forward: light WT, heavy KO; reverse: light KO, heavy WT |
| `2147_..._FW_1-8` / `Rev_1-8` | same, 1 h after 16 J/m2 UV-C ("UV interactors") | Fig. 5c | as above |
| `2006_..._01-08` / `09-16` | ELOF1 HA-IP (DSP crosslinked) in HCT116 ELOF1-mScarletI-HA KI vs empty beads ("Basal complex") | Ext. Data Fig. 2d | forward: heavy bait; reverse: light bait |

How it was resolved:
- **Paper to experiment.** The ratio columns in Extended Data Table 2 (MOESM4) match the deposited `*_proteinGroups.txt` experiment columns value for value (for example, 802/802 values match for the ELOF1 IP).
- **Experiment to file.** A protein seen in only one MaxQuant experiment shows up only in that experiment's fraction numbers, and those numbers equal the raw-file suffixes. For 2149, forward is fractions 12-22 and reverse is 1-11; 2147 covers fractions 1-8.
- **Label direction.** Taken from the figure legends ("ELOF1-/-A relative to Wt", "relative to empty beads"). It agrees with the channel intensities: ELOF1 is absent from the KO channel, and Pol II is enriched in the bait channel.

## Unresolved (52 files, rows 109-212)

- **`1776_F_MaritGeijer_*` (36 files).** These runs belong to four MaxQuant experiments of MRC-5 Flag IPs. "Wt vs #7 FOR/REV" is the GFP-RPB1 IP of Ext. Data Fig. 2e. "No UV vs 16J FOR/REV" is not shown in the paper. Raw-file headers show that the files were acquired as four consecutive 9-file blocks, written as blocks A-D in the SDRF. All four experiments use fraction numbers 1-9, so it is not known which block is which experiment. Genotype, treatment and sample type are `not available`.
- **`2006_F_MaritGeijer_17-32` (16 files).** These are ELOF1 HA-IPs "Nt vs 16J UV forward" (17-24) and "NT vs 12J UV reverse" (25-32), neither shown in the paper. Which SILAC channel was UV-irradiated is not documented, so treatment is `not available`.

## Other limitations

- Instruments differ by series. 1776 and 2006 were run on an Orbitrap Fusion with EASY-nLC 1000, and 2147 and 2149 on an Orbitrap Fusion Lumos (from the raw headers). PRIDE lists only the Lumos.
- No `mqpar.xml` was deposited. Variable modifications are read from the proteinGroups site-ID columns. The MaxQuant custom `DSP`/`DSP cleaved` modifications of the 2006 search are omitted because their UNIMOD mapping cannot be verified. Tolerances are `not available`, so `parse_sdrf convert-openms` stops on this file.
- PRIDE gives the disease as "Cockayne syndrome", but that is the study context only. No patient cells were measured: HCT116 is colon carcinoma and MRC-5 is normal.

- MRC-5 rows use the parental Cellosaurus line CVCL_0440 (fetal lung, 14 fetal weeks). The paper used an SV40-immortalised MRC-5 derivative carrying the GFP-RPB1 knock-in, and the paper does not say which SV40 subline (e.g. MRC-5V1 CVCL_D690 or MRC-5V2 CVCL_2627).
- The 1776 rows carry `characteristics[biological replicate]` = 1 for all four blocks only as a placeholder. Two of the blocks must be reverse label-swap experiments, but the column does not allow a reserved word.
- Basal experiments were mock-treated (Methods), and the SDRF writes `not applicable` in the treatment column for them.
- In the unresolved UV pairs, the CSB (1776) and ubiquitin (2006) ratios suggest heavy = UV in forward and light = UV in reverse. This is only an inference and is deliberately not encoded.
- The ELOF1 knock-in line is HCT116 osTIR1 with ELOF1-mScarletI-HA (including an auxin-inducible degron).

## Return criteria

- The MaxQuant `mqpar.xml`/`experimentalDesign` for searches 1776 and 2006, or `evidence.txt` with raw-file names, or an author statement mapping the 1776 blocks and the 2006 UV pairs to experiments and channels.
- Then rebuild those rows, re-run the independent review, and move the folder to `datasets/PXD025304/`.
