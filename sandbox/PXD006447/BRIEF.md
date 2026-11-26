# PXD006447: unresolved UC controls

The complete [deposit](https://www.ebi.ac.uk/pride/archive/projects/PXD006447)
has twelve UC RAW acquisitions, in addition to the 84 concentration-series
and yeast-control acquisitions. Native headers and all 96 matched original
Comet configurations were inspected. Search-parameter corrections to the
existing canonical file are described in `datasets/PXD006447/README.md`.

The [paper](https://doi.org/10.1039/c8mo00077h) supplies preparation methods
and twelve technical injections for each named dilution-series concentration.
It does not establish the composition, concentration or preparation relationship
of these UC files. The previous assertion of UPS1 without yeast is removed.
Organism, biological/technical replicate and physical enzyme remain unavailable
for UC. A semi-tryptic search and a combined yeast/UPS1 search database do not
prove the material or digestion reagent used in the control.

## Local validation

Reviewed 2026-09-28. The corrected UC file fails required organism,
biological-replicate, technical-replicate and physical-enzyme checks and remains
in sandbox. Deposit reconciliation also mistakes the literal `not available`
enzyme sentinel for an unsupported reagent; no reagent is claimed here.
