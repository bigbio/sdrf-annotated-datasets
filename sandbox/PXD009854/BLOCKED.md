# PXD009854 — BLOCKED

BLOCKED: the SILAC channel → condition map is not public.

**Dataset:** [PXD009854](https://www.ebi.ac.uk/pride/archive/projects/PXD009854) ·
Wang G, Simon DJ, *et al.* "Structural plasticity of actin-spectrin membrane skeleton and
functional role of actin and spectrin in axon degeneration." *eLife* 2019;8:e38730 ·
[PMID 31042147](https://pubmed.ncbi.nlm.nih.gov/31042147/) ·
[PMC6494423](https://europepmc.org/article/PMC/PMC6494423)

## What is resolved

- SILAC 2-plex. Lys +8 is `Label:13C(6)15N(2)` (UNIMOD:259) and Arg +10 is
  `Label:13C(6)15N(4)` (UNIMOD:267). Source: the paper's Methods and the PRIDE protocol. The
  MaxQuant tables contain only L/H intensities and `Ratio H/L`.
- 12 TiO2 phospho-enriched RAW files: 3 replicates of `axon` and 3 of `body` (the
  compartments of primary E12.5 mouse DRG sensory neuron spot cultures).
- The draft `PXD009854.sdrf.tsv` has 24 rows: each file once per channel (`SILAC light`,
  `SILAC heavy`). It passes `parse_sdrf validate-sdrf` for `ms-proteomics` and `vertebrates`.

## What blocks promotion to `datasets/`

1. **Which channel is trophic-deprived (TD) and which is the NGF control.** The paper
   describes "a large-scale, unbiased phosphoproteomic screen in axons undergoing TD". It does
   not say which SILAC label carried TD, or how long TD lasted. The following were checked and
   none of them state it: the paper (Methods, figure legends, Europe PMC full text), the
   Fig. 2—suppl. 2 source data (site information only, no ratios), the PRIDE metadata, the
   MaxQuant `parameters.txt`, the `PhosphoSTYSites.txt` and `peptides.txt` headers, and the RAW
   file headers. The first 8 MB of the 5.3 GB Proteome Discoverer `.msf` were also read; they hold
   only a generic "SILAC 2plex (Arg10, Lys8)" Heavy/Light method, with no condition names. No other
   repository is cited. The draft therefore has `characteristics[treatment] = not available`
   on every row and declares no treatment factor.
2. **The `_a` / `_b` file suffixes are not explained.** The draft encodes them as technical
   replicates 1 and 2, because no fractionation is described. `axon1` has no `_b` file. Its
   second file, `axon1_enriched_a_100ms_5e5_MSMS.raw`, re-injects sample `a` using the MS2
   method of the other 10 files (100 ms / AGC 5e5). `axon1_enriched_a.raw` itself used
   60 ms / AGC 2e5.
3. **`body` = neuronal cell body is read from the file names.** The paper does not describe
   the cell-body proteomics explicitly. Replicate numbers are shared between `axonN` and
   `bodyN` because the file names share them. The paper does not say whether these pairs came
   from the same culture.
4. **The precursor mass tolerance is not deposited** (`mqpar.xml` is missing), so the draft
   has `not available` there. Because of this, `parse_sdrf convert-openms` fails.

## How to unblock

The submitter (H. Molina, Rockefeller Proteomics Resource Center) or the authors would need
to confirm three things: the light/heavy → NGF/TD assignment per replicate (including any
label swap) with the TD duration, the meaning of `_a`/`_b`, and the MaxQuant precursor
tolerance.
