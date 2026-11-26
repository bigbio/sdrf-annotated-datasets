BLOCKED: the SILAC channel-to-condition map for biological replicates 2 and 3 is contradicted by the deposited data.

`PXD016166.sdrf.tsv` in this folder is a DRAFT. It has 144 rows: 48 raw files x 3 SILAC channels, covering the SUMO, ubiquitin and phospho workflows of HEK293 SUMO3m cells after arsenic trioxide (0 / 1 / 10 uM, 4 h).

## Where the draft map comes from
The draft copies the rotating label scheme in Figure 12 of the open-access M.Sc. thesis (Rinfret Robert C., Universite de Montreal 2019, http://hdl.handle.net/1866/23640, PDF page 52). It assumes that file `REPn` is the figure's "Replicat n":

| | Control | 1 uM ATO | 10 uM ATO |
|---|---|---|---|
| Replicat 1 | light | medium | heavy |
| Replicat 2 | heavy | light | medium |
| Replicat 3 | medium | heavy | light |

## Why it is blocked
An independent reviewer downloaded the deposited MaxQuant output (SUMOtxt.zip and UBItxt.zip). Holding replicate 1 fixed, they tested all six channel orientations for files REP2 and REP3 against the site-level ratios:
- **Figure-based map:** it ranks last for both REP2 and REP3, with r about -0.45 against replicate 1 (SUMO n=594 sites, ubiquitin similar). Under it, REP2 and REP3 also disagree with each other (r=-0.36).
- **Best fit:** REP2 follows the figure's "Replicat 3" row and REP3 its "Replicat 2" row, with r = 0.76-0.84.
- **Biology:** the swapped map fits the biology. PML SUMO/ubiquitin sites come out lowest in the control in every replicate.

This evidence is documented here but **not applied**: a channel map derived from data similarity is not accepted for `datasets/`.

## What would unblock it
A public statement that ties files REP1-3 to the figure's replicate rows (e.g. from the authors or the J Proteome Res 2020 paper, PMID 32223133, doi:10.1021/acs.jproteome.9b00807, which is paywalled), or a deposited experimental design with condition names per channel.

## Other known issues in the draft
- `characteristics[enrichment process]` = `antibody enrichment` (PRIDE:0000954) for SUMO and ubiquitin is outside the EFO:0009090 branch that TERMS.tsv expects. EFO:0009106 "sample enrichment" is an in-branch alternative.
- The precursor mass tolerance is `not available`, because no mqpar.xml is deposited and MaxQuant 1.5.5.1 does not record it.

## Sandbox notes
- This is a blocked draft, kept in `sandbox/` because its channel map conflicts with the deposited data. Promote it to `datasets/` only once the map is resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Review status: an independent fresh-context adversarial review FAILED this draft on the REP2/REP3 orientation (and the enrichment term above).
