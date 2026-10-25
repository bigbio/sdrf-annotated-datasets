# PXD047934: TMT mapping repaired; source conflicts remain

## Evidence and corrected coverage

The [deposit](https://www.ebi.ac.uk/pride/archive/projects/PXD047934) includes
21 RAW files and the original `experimentaldesign_labels.txt`. All native
headers identify Q Exactive HF. The design directly maps 15 samples to tags
126-133C: three DMSO, three 8451, three 0068, three cycloheximide and three
CC-885 preparations. The draft now represents 315 RAW/tag rows. The reported
16plex quantification also contains a channel-16 result column; that column
does not supply an additional biological sample absent from the author design.

The archive calls the compounds BI03058451 and BI01590068. The
[accepted manuscript](https://discovery.dundee.ac.uk/ws/files/132805097/Final_resubmission.pdf)
calls the corresponding codes ACBI-8451 and ACBI-0068. The latter is explicitly
a non-cereblon-binding control. The old BI-364518 assignment is unsupported.
The [publisher supplement](https://doi.org/10.1021/acschembio.4c00152.s001)
was also inspected.

## Remaining conflicts

Preparation Methods and PRIDE say HEK293, while accepted Figure 4 names HCT116
for the proteomics comparison. Final article text could not be retrieved from
the publisher; the conflict has not been resolved. Cell line, organ, age, sex
and other lineage fields remain unavailable instead of selecting one account.

Twenty RAW names have fractions 1-20. An additional `Frac-11-12-13.raw` file
has an unresolved relation to the separate 11/12/13 acquisitions; its fraction
and technical-replicate fields remain unavailable. It is not silently renamed
fraction 21. Preparation Methods mention 21 fractions and analysis mentions 20.
Software versions also disagree: PRIDE reports MaxQuant 1.6.14 and the accepted
manuscript 1.4.16. The general version field remains unavailable. Parameters
reported in both sources are labeled as reported, without claiming inspection
of an original MaxQuant configuration.

The old canonical 15-row file is preserved as the pre-existing baseline; this
review does not validate its fraction/channel relationships. The repaired
draft remains in sandbox pending resolution of the conflicts above.

## Local validation

Reviewed 2026-09-28 with sdrf-pipelines `701356bd5309`. Required fraction,
technical-replicate and cell-line information remains unresolved. Native RAW
prefixes, design text and the proteinGroups header were read; full spectra and
complete result tables were not downloaded or integrity-tested.
