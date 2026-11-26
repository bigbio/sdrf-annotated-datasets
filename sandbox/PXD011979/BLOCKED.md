# PXD011979: BLOCKED (partial annotation, 120 of 150 raw files)

BLOCKED: 30 of the 150 deposited raw files have no public TMT channel-to-sample map. They are
`David-Ho-TMT-Hypoxia-Acidosis-Mix1-Fraction1..15.raw` and `...-Mix2-Fraction1..15.raw`, from the
LARP1 / "Acidosis Studies" TMT-pSILAC experiment (60 high-pH fractions concatenated to 15).

- **Annotated (`PXD011979.sdrf.tsv`, 780 rows):** `Hypoxia-7plex-F1..F60.raw` and
  `Normoxia-6plex-F1..F60.raw`, one row per raw file per occupied TMT10plex channel.
  - Hypoxia 7-plex channel map: Ho et al., Nat Commun 2020 (PMID 32472050), Fig. 2a, and the
    Source Data sheet "Figure 2b" column headers.
  - Normoxia 6-plex channel map: Supplementary Fig. 3b, upper panel.
- **Not annotated:** the 30 Mix1/Mix2 files. Supplementary Fig. 3b (lower panels) shows four
  LARP1 conditions (control vs LARP1 siRNA at 21% and 1% O2) but no TMT tags. The PRIDE protocol
  calls this experiment "Acidosis Studies" without listing its samples. The Source Data has no
  LARP1 channel columns, and the deposited mzIdentML holds no sample names.

**To unblock:** get the TMT tag → sample assignment for Mix1/Mix2 from the submitters (SPARC
BioCentre / Lee lab), add those rows, re-validate, then promote the folder to `datasets/`.
Alternatively, maintainers can accept the partial file in `datasets/` as is.

**Labelling design:** the deposit is TMT10plex combined with pulsed SILAC (TMT-pSILAC). Light
R0K0 medium for 7 days, then heavy R10K8 for 16 h, in every channel. Sample identity is carried by
the TMT tag, so the SDRF has one row per raw file per occupied TMT channel. The SILAC pulse
(Label:13C(6)15N(2) on K, Label:13C(6)15N(4) on R) is encoded in `comment[modification parameters]`,
not as SILAC light/heavy label rows.
