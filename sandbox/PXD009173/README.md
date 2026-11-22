# PXD009173 — HipA / HipA7 phosphoproteomics in *E. coli* (sandbox draft)

**BLOCKED:** the SILAC channel → sample map is not available from public evidence.
The deposit is a triple-SILAC design (Lys0 / Lys4 / Lys8). For each of the 16 mixed samples (MaxQuant experiments),
the record does not say which strain, plasmid, induction state or time point sits in the
light, medium and heavy channel. Without that map, `characteristics[genotype]` is
`not available` and the SILAC SDRF has no `factor value[...]` column.

- PRIDE: https://www.ebi.ac.uk/pride/archive/projects/PXD009173
- Publication: Semanjski M *et al.* *Sci Signal* 2018;11(547):eaat5750 —
  PMID [30206139](https://europepmc.org/article/MED/30206139),
  doi:[10.1126/scisignal.aat5750](https://doi.org/10.1126/scisignal.aat5750)

## Files

| file | content | status |
|---|---|---|
| `PXD009173-silac.sdrf.tsv` | 449 SILAC raw files × 3 channels = 1347 rows, from 5 MaxQuant searches (Fig1 HipA/HipB, Fig2 HipA7 vs HipA pBAD, Fig3 high/low copy, Fig4 chromosomal *hipA7*, FigS1 HipA S150/S359) | validates; **BLOCKED**: per-channel sample identity is unknown |
| `PXD009173-kinase-assay.sdrf.tsv` | 80 label-free raw files of the *in vitro* kinase assay (2 replicates × 20 reactions × Lys-C / chymotrypsin) | validates; fully resolved from the deposited MaxQuant experiment names |

## Where the values come from

All 529 deposited `.raw` files map 1:1 onto the `Raw file` column of the six deposited
MaxQuant `*_txt.zip` searches (`summary.txt`, `experimentalDesignTemplate.txt`,
`parameters.txt`, read by HTTP range request):

- run → experiment, fraction, enzyme (Lys-C or chymotrypsin) and SILAC multiplicity
  (Lys4 = `Label:2H(4)` UNIMOD:481, Lys8 = `Label:13C(6)15N(2)` UNIMOD:259)
- fixed and variable modifications (Carbamidomethyl C; Oxidation M, Acetyl protein N-term,
  Phospho STY), and a 20 ppm FTMS MS/MS tolerance; precursor tolerance is 4.5 ppm (protocol)
- instrument model, read from each raw file header: 494 runs Q Exactive HF, 35 runs Orbitrap
  Elite (all in the Fig4 chromosomal *hipA7* search, as the protocol states). The Elite headers
  show HCD with Orbitrap MS2.

## Sources checked for the channel map

1. **PRIDE project record**: the protocol describes Lys0/Lys4/Lys8 labelling and gives no
   per-channel assignment.
2. **PRIDE files**: the MaxQuant outputs carry only generic `Ratio M/L` and `Ratio H/L`
   columns, the experiment names give no channel identities, and no sample sheet is deposited.
3. **Europe PMC**: abstract only. The paper has no PMCID and no supplementary files.
4. **Full text and Data Availability**: Science Signaling (subscription only), not
   reachable from the allowed sources.

Run names hint at the designs (`HipAinduction_..._012`, `HipBinduction_..._034`,
`CPH_123`, `CPH_145`, `WT_deltahipBA_hipA7`, `pMG_pNDM`, `hipA7vshipA`). They do not
say which label each condition carried, so no value was taken from them.

## To unblock

From the paper's figure legends or Methods, take the light/medium/heavy assignment for
each MaxQuant experiment: `HipA_Rep1/2` and `HipB_Rep1/2` (Fig1), `A7vsA_Rep1-3` (Fig2),
`HipA7_Rep1/2` and `HipA_Rep1/2` (Fig3), `hipA7_Rep1-3` (Fig4), and `S150` / `S359` (FigS1).
Then replace `characteristics[genotype]` per source and add `factor value[...]` columns.
Watch for label swaps between replicates.

## Other open points

- Seven raws re-measure an (experiment, fraction) slot that an earlier raw already holds
  in the deposited design. They are written as `comment[technical replicate]` 2. In
  `Fig3 HipA_Rep1`, the slot holds `..._pNDMpMGhipA7_Proteome_Fast` (technical replicate 1),
  a raw whose name says *hipA7*, and `..._pNDMpMGhipA_Proteome` (technical replicate 2). Both
  runs share a date, so the 1/2 order is arbitrary, and the *hipA7* raw may be mis-assigned
  in the deposited search.
- `20161008_MS_Ecoli_LysC_hipA7vshipA_Rep2II_Phospho01` carries MaxQuant fraction 3, the
  same as Phospho03. It is written as fraction 1, following its file name; this is a
  curator correction.
- Single-shot proteome raws keep their MaxQuant fraction numbers (101/103/105) so rows stay
  traceable to the deposited design.
- `characteristics[enrichment process]` differs between the phospho and proteome runs of one
  source. Keep this in mind when factor columns are added.
- The protocol counts 471 raws, 249 of them phospho-enrichment raws. The deposit has 529
  raws, and 267 of them are named `Phospho`.
- Kinase-assay reactions S14–S16 are not in the deposit.
