# PXD001528

BLOCKED: iTRAQ4plex channel-to-sample map is incomplete for the Paraquat non-specific-binding runs (four channels, no table).

## Why this is in sandbox
- Sod2 knockdown Libra channels 114/115/117 are evidenced (Fig. 4 caption vs pep.xml 114/115/117).
- Paraquat quantitative runs use Libra 114+116 only; 116/114 median 1.53 matches the paper paraquat/control ratio, but that pairing was not written into the SDRF at review time.
- Non-specific-binding pep.xml uses 114/115/116/117 with no channel table (control vs paraquat × biotin hydrazide vs omitted).
- Independent review FAIL on unmapped Paraquat/NSB channels.

## Return criteria
- Author or supplementary table for NSB four-channel layout (and confirmation of 114 vs 116 on the Paraquat plex).
- Then promote `sandbox/PXD001528` → `datasets/PXD001528` in a dedicated PR.
