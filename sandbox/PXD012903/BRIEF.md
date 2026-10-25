# PXD012903: iTRAQ channel-label repair

Checked on 2026-09-29 against the [PRIDE project](https://www.ebi.ac.uk/pride/archive/projects/PXD012903), its seven-file inventory, the deposited `92-5.msf`, and the primary [article](https://doi.org/10.1134/S0006297919080121).

The PRIDE protocol describes five RAW acquisitions (`92-1.raw` through `92-5.raw`) and an 8-plex design: sample 1→113, sample 2→114, sample 3→115, sample 4→116, sample 5→117, sample 6→118, sample 7→119, and sample 8→121. The deposited Proteome Discoverer MSF independently lists all five RAW inputs, Q Exactive acquisition, Trypsin, 20 ppm precursor tolerance, 0.1 Da fragment tolerance, and iTRAQ8plex reporter channels 113/114/115/116/117/118/119/121.

The article's methods describe second leaves collected at 0, 6, and 24 h after inoculation, with 0 h-1 and 0 h-2 as the two biological control measurements and three measurements at each later time point. The existing draft's condition/replicate grouping follows that sample-order convention. No deposited author table was found that independently names each iTRAQ channel with its condition, so this file remains in `sandbox/` and the condition mapping is not promoted to `datasets/`.

The only file change is the ontology spelling in `comment[label]`: non-ontology values such as `iTRAQ8plex-113` are represented as the accepted PRIDE terms `iTRAQ113` through `iTRAQ121`. No RAW, fraction, or biological-replicate row was added or removed.

Local checks: `ms-proteomics` and `plants` validation pass with the OLS cache; repository review passes. Deposit reconciliation still reports a single `cleavage_agent_unsupported` warning because the structured PRIDE project JSON omits the enzyme, while the deposited MSF and article explicitly identify Trypsin.
