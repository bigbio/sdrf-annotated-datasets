# PXD011893 — sandbox draft (instrument conflict + enzyme unstated)

*Nepenthes ampullaria* pitcher fluid, UKM (Goh lab); 9 RAW = 3 conditions × 3 technical replicates
(`{D0,D3C,D3L}_150818_0{1-3}.raw`), MaxQuant output deposited.

## D3C vs D3L — resolved

The same group's transcriptome work on these pitchers defines the codes: newly opened pitchers (D0),
pitchers after 3 days of opening (D3C), and pitchers whose endogenous fluid proteins (>10 kDa) were
filtered out at opening (D3L) (Sci Rep 2020, PMC7170878; Front Plant Sci 2015 lists SRA samples
"Day 0 control", "Day 3 control", "day 3 depleted"). Encoded as `sampling time` 0/3 day and
`treatment` untreated / "endogenous fluid proteins >10 kDa removed by filtration at opening".
Each condition is one pool of 6 pitchers (PX description), so `biological replicate = 1`,
`pooled sample = pooled`, technical replicate = `_01–_03`.

## Instrument — still unresolved

- PX structured field: **LTQ Orbitrap Elite** (MS:1001910, PSI-MS label "Orbitrap Elite") — used in the draft.
- PX description: "Orbitrap Fusion Tribid", but that paragraph is copied from PXD007599 (it says
  "for each species" although this deposit has one species), so it is weak evidence.
- The proteomics paper that would settle it is not identified: the linked Front Plant Sci 2015
  paper is RNA-seq only, and the 2021 Front Plant Sci paper cites PXD007599, not this deposit.
- Settle by reading the RAW header (first ~256 KB, UTF-16) of `D0_150818_01.raw` from PRIDE FTP, or
  `Maxquant_result.zip` → `summary.txt`.

## Why sandbox

Enzyme not stated anywhere reachable (`cleavage agent details` = `not available`); the same lab's
companion deposit used Trypsin/P in MaxQuant, but that is not evidence for this one. Carbamidomethyl
C (fixed) follows the PX "iodoacetamide derivatized residue"; confirm both from the MaxQuant zip.
