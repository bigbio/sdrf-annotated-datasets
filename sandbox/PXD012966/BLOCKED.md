# PXD012966 annotation blocked (no public TMT channel-to-sample map)

PXD012966 is a lysine crotonylation study of PBMCs in systemic lupus erythematosus (Clin Rheumatol 2022).

**The design cannot be resolved from public sources.**

- **One RAW file.** `7128TPCR_1.raw` is a genuine Thermo file (Q Exactive Plus). It is a single TMT6plex run of crotonylation-enriched PBMC peptides; the companion deposit PXD042217's `mqpar` lists TMT6plex 126–131, and the MaxQuant output has six reporter channels.
- **Pooled design, no map.** The study sampled 47 donors (11 SLE, 36 healthy controls) into those 6 channels, so the channels must be pools or a subset of donors. These sources were checked, and none gives a channel map:
  - the paper and its supplementary DOCX (per-patient clinical table only);
  - this accession's MaxQuant output (generic channel names; the `mqpar` experiment field is empty);
  - Europe PMC supplementary files for this paper and the companion ACS Omega 2023 paper (PMC10688171);
  - the Data Availability statement, which cites only PRIDE;
  - the companion deposit PXD042217 (`mqpar`, `.sld`, MaxQuant zips).
- **Reconstruction rejected.** Comparing channel intensities with the 692 published SLE/NC site ratios gave at best r = 0.54 and 69% sign agreement (channels {1,2,4} vs {0,3,5}). That is too weak to assign samples, and it cannot tell pools from replicates.

**Other notes (ready for a future SDRF)**
- Instrument Q Exactive Plus from the raw file (PRIDE says Q Exactive); NCE 30 from the raw file (paper says 28); precursor tolerance 4.5 ppm from the `mqpar` (paper says 5 ppm).
- MaxQuant's custom "Crotony(K)" modification corresponds to UNIMOD:1363 Crotonyl (+68.026 Da, matching the evidence masses).

**To unblock:** a per-channel sheet from the submitters stating which group is in each channel and which donors each pool contains.
