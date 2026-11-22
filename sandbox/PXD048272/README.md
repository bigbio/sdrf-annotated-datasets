# PXD048272 — sandbox draft

BLOCKED: the per-run sample identity is only partly resolvable from public evidence, so this
draft stays in `sandbox/` and is not promoted to `datasets/`.

- **Dataset:** [PXD048272](https://www.ebi.ac.uk/pride/archive/projects/PXD048272), KMT2D (MLL2)
  ChIP-MS in HEK293A, SILAC heavy Lys8/Arg10 vs light, Orbitrap Fusion DDA.
- **Publication:** Takemon et al., Genome Medicine 2024,
  [PMC11583415](https://europepmc.org/article/PMC/PMC11583415) / PMID 39578878 /
  doi:10.1186/s13073-024-01401-9.

## What is resolved

- All 8 raw files are 2-plex SILAC (heavy/light) runs. The deposited pepXML search results show
  60–77% of confident K/R PSMs carrying K+8.014 / R+10.008, including the two `11Oct2017 … rep1`
  runs whose names do not say SILAC.
- In the KMT2D ChIP (`MLL2`) runs, heavy = HEK293A KMT2D wild type and light = HEK293A KMT2D
  knockout. Methods: WT cells were heavy-labelled; WT and KO1/KO3 extracts were mixed 1:1 and
  immunoprecipitated with an anti-KMT2D antibody.
- Instrument, digest, tolerances and modifications come from the PRIDE protocols and the paper.

## What blocks promotion

1. **The four `GFP` runs** (`GFP_rep1`, `GFP_2`–`GFP_4`) are not described in the paper or the
   PRIDE protocols. Their IP target and channel identities are unknown, so both channels carry
   genotype `not available`.
2. **Which KO clone (KO1 D320 or KO3 D372) and which replicate each MLL2 run is** is not stated.
   Supplementary Table S4 reports R1KO1, R2KO1, R1KO3 and R2KO3 without raw-file names, so the
   clone is not encoded.
3. The ChIP antibody target per run (KMT2D vs GFP) is visible only in the file names. An optional
   `characteristics[enrichment process]` column exists, but the paper names only the anti-KMT2D
   antibody, so a value for the GFP runs would rest on file names alone. It is left out.
4. Heavy = WT / light = KO for `MLL2_rep1` (11Oct2017) is inferred from the single SILAC design in
   Methods and from the four MLL2 runs matching the four Table S4 experiments. Its SILAC status is
   confirmed by the deposited pepXML.

## What would unblock it

- A statement from the submitters (or the deposited design file, after curator review) mapping
  each raw file to its IP antibody, KO clone and replicate.
