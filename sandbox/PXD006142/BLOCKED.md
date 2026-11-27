# PXD006142 annotation blocked (triplex dimethyl channels cannot be built)

PXD006142 is a phosphoproteomic analysis of T-cell receptor stimulation in human primary CD4+CD25− T cells with and without regulatory T cells (PMID 28993769, doi:10.3389/fimmu.2017.01163).

**The design is resolved; only the label encoding blocks the SDRF.** The deposit holds one genuine Thermo RAW file, `OR9_20130901_NB_KI_Mix3_TiIMAC.raw`. Its instrument record reads Orbitrap Elite. The file contains three samples labelled with triplex dimethyl (DIMETHYL0/4/8; PRIDE:0000848/850/852). The PRIDE protocol and the paper give the channel map, and the deposited Proteome Discoverer `.msf` quantification method confirms the masses:

| label | sample |
|---|---|
| light | unstimulated |
| medium | stimulated after coculture with T cells |
| heavy | stimulated after coculture with regulatory T cells |

The SDRF builder used for agent-assisted annotation (sdrf-skills `sdrf-tools build`) recognises only TMT, iTRAQ and SILAC labels as channels. It treats the dimethyl rows as three label-free sources claiming one file and refuses. Relabelling the channels as SILAC would pass validation, but dimethyl is chemical labelling, so no SDRF is emitted.

The search settings come from the deposited `.msf`:
- fixed Carbamidomethyl (C);
- variable Oxidation (M), Phospho (STY), and dimethyl light/medium/heavy on K and N-term (UNIMOD:36/199/330);
- precursor tolerance 50 ppm;
- fragment tolerance 0.05 Da (HCD) and 0.6 Da (ETD);
- Lys-C then trypsin.

**Other open points**
- **Donor:** the paper calls this "Donor 4", but the `.msf` input path says "Donor3".
- **Second run:** the `.msf` also searched a second run (`…Mix3_TiIMAC2.raw`) that is not deposited.
- **Fragmentation:** the run used both HCD and ETD, and the SDRF has a single dissociation column.

**To unblock:** builder support for `DIMETHYL(0|2|4|6|8)` channels, or a hand-curated SDRF with one row per dimethyl channel.
