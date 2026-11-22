# PXD037425 — sandbox

BLOCKED: the SILAC channel → treatment map is not resolvable from public evidence.

PXD037425 (Lu L, Ye Z, ... Olsen JV, Yuan Y, Mao Y. *ETD-Based Proteomic Profiling Improves
Arginine Methylation Identification and Reveals Novel PRMT5 Substrates.* J Proteome Res 2024,
PMID 38272855) compares SILAC-labelled HeLa cells with and without the PRMT5 inhibitor
EPZ015666. Which label (light Arg0/Lys0 or heavy Arg10/Lys8) received the inhibitor is
not stated in any source that could be checked:

- the PRIDE project record (description, sample and data-processing protocols) does not say;
- the deposited Proteome Discoverer 2.4 result
  (`20210402_..._SILAC_PRMT5_inhibitor_IAP_3xR_LightOnly_Quant.pdResult`) defines only the
  Light and Heavy quan channels. Its `AnalysisDefinition` has empty `<Factors/>`, and the
  samples are named only `<run> - [Light]` / `<run> - [Heavy]`;
- the article is closed access. Europe PMC, Unpaywall and Semantic Scholar have no open
  copy, so only the abstract was read.

Peptide-level Light/Heavy ratios in the PD result hint that heavy was the inhibitor
channel. The median log2 L/H is +1.64 for dimethyl-R peptides and −2.05 for unmodified
peptides. This was **not** used, because it is an inference and the unmodified-peptide
shift makes it ambiguous.

Also unresolved: whether the three SILAC runs (`_IAP_1/2/3`, acquired one after another on
2021-04-03, PD result named "3xR") are independent biological replicates or repeated
injections. Each run/channel is therefore its own source with biological replicate 1.

## Files

| file | runs | rows | content |
|---|---|---|---|
| `PXD037425-silac.sdrf.tsv` | 3 | 6 | SILAC 2plex (Arg10/Lys8), light + heavy row per run; `characteristics[treatment]` and `factor value[treatment]` = `not available` (blocked) |
| `PXD037425.sdrf.tsv` | 20 | 20 | label-free runs: 16 HeLa ulilysin sdme-RG IAP fragmentation-optimisation runs (ETD, ETciD, EThcD, HCD; Orbitrap Fusion Lumos), 2 earlier HeLa HCD runs (ulilysin and trypsin, Q Exactive Plus), 2 HCC827 ulilysin runs (Q Exactive Plus, PRM + DDA method) |

The runs are split into two files because quantms/`parse_sdrf convert-openms` refuses
SILAC and label-free runs in one SDRF. Both files pass `parse_sdrf validate-sdrf` for
ms-proteomics, human and cell-lines (v1.1.0), as well as `sdrf-tools structure` and
`parse_sdrf convert-openms`.

## To unblock

Get the light/heavy assignment (and the replicate type) from the article's Methods or
Supporting Information (doi:10.1021/acs.jproteome.3c00724), or from the authors. Then set
`characteristics[treatment]` / `factor value[treatment]` in `PXD037425-silac.sdrf.tsv`
(e.g. `EPZ015666` vs the vehicle the paper names), re-validate, and promote the folder to
`datasets/`.

## Notes for reviewers

- The deposit also holds `SERBP1_P5P1_MALDI.zip` (category OTHER, MALDI data). It is not an
  LC-MS raw file, so it has no SDRF row.
- The HCC827 runs use a hybrid Q Exactive Plus method: a PRM experiment with an inclusion
  list runs alongside a top10 DDA experiment. They are recorded as DDA only.
- The `ETciD30_HCD`, `EThcD25_HCD` and SILAC runs take an extra HCD (30 %) scan for every
  precursor. `comment[dissociation method]` holds a single value, so it records only the
  ETD-based activation. The `_HCD` scheme is kept in `factor value[fragmentation method]`.
- In the SILAC file, the `Label:13C(6)15N(4)` (R) and `Label:13C(6)15N(2)` (K) modification
  parameters come from the PD "SILAC 2plex (Arg10, Lys8)" quantification method. The deposited
  "LightOnly" search did not use them as search modifications.
