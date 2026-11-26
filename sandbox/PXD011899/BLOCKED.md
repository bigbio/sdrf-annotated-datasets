# PXD011899 — BLOCKED: second SILAC run has an unresolvable channel map

BLOCKED: `FL0067_AysegulS_3.raw` can't be annotated from public evidence. Its
precursor pattern shows three SILAC channels, the paper describes a two-channel mix, and
no public source says what the third (heavy) channel is.

## Evidence used

- PRIDE project: <https://www.ebi.ac.uk/pride/archive/projects/PXD011899> (files API
  `https://www.ebi.ac.uk/pride/ws/archive/v3/projects/PXD011899/files/all`: 6 RAW,
  6 MGF, 6 Mascot `.dat`, 6 `.mzid`)
- Paper: Sapmaz *et al.*, Nat Commun 2019;10:1454. PMID
  [30926795](https://pubmed.ncbi.nlm.nih.gov/30926795/), PMC6440979,
  doi:[10.1038/s41467-019-09437-x](https://doi.org/10.1038/s41467-019-09437-x). See
  Methods "Ubiquitome analysis" and the Fig. 4 legend.
- Deposited Mascot `.dat` parameter headers, RAW header strings (first 3 MB of each
  RAW file), and the deposited MGF peak lists of the two Fusion Lumos runs.

## Design from the paper

- **LFQ arm** (Q Exactive): MelJuSo siCtrl vs siUSP32_2, with n = 2 biologically
  independent samples. The 4 QE RAW files are named `U_Ctrl*` and `U_Si*`. Methods:
  "QE for LFQ samples".
- **SILAC arm** (Orbitrap Fusion Lumos): "The orbitrap Fusion Lumos was used for SILAC
  samples."
  - Knockdown (KD) set, n = 1: MelJuSo scrambled siRNA in light (K0R0) and siUSP32 in
    heavy (K8R10).
  - Overexpression (OE) set, n = 1: HeLa empty vector in light (K0R0) and USP32-HA in
    medium (K4R6).
  - Each set was "mixed 1:1".
- Neither the paper nor PRIDE says which FL RAW file holds which set.

## What the deposited data show (`silac_pair_analysis.txt`)

The analysis counts MS2 precursor pairs at a given neutral-mass offset (±0.004 Da), with
the same charge and a retention time within 1 min. It compares each count against offsets
shifted by ±0.02–0.03 Da, which give the background level.

| offset | FL0067_AysegulS_2 (on / background) | FL0067_AysegulS_3 (on / background) |
|---|---|---|
| K4 +4.0251 | 258 / ~290 (none) | 574 / ~180 |
| R6 +6.0201 | 320 / ~290 (none) | 432 / ~200 |
| K8 +8.0142 | 1508 / ~280 | 662 / ~200 |
| R10 +10.0083 | 769 / ~280 | 365 / ~210 |
| K4→K8 +3.9891 | 256 / ~270 (none) | 668 / ~190 |

- **FL0067_AysegulS_2** has only light/heavy (K8R10) pairs, so it is the MelJuSo KD set.
  It is annotated in `PXD011899-silac.sdrf.tsv`.
- **FL0067_AysegulS_3** has light–medium, light–heavy *and* medium–heavy pairs, i.e. a
  triplex. Its light and medium channels fit the HeLa OE set. The heavy channel isn't
  described anywhere, so it is not annotated.

## Files in this folder

- `PXD011899-silac.sdrf.tsv` covers FL0067_AysegulS_2 only, with 2 rows (light siCtrl,
  heavy siUSP32). FL0067_AysegulS_3 is omitted.
- `PXD011899-lfq.sdrf.tsv` covers the 4 QE label-free runs. It is split from the SILAC
  file because `convert-openms` refuses to mix SILAC and label-free in one SDRF.
- `*.evidence.json` holds the provenance manifests. `silac_pair_analysis.txt` is the
  MGF pair analysis.

## Other open points

- **LFQ replicate conflict.** The paper reports n = 2 biologically independent LFQ
  samples. The RAW headers show that each condition's two files came from the same
  autosampler vial: `gb5` for `U_Ctrl` and `U_Ctrl_150421035129`, `gb6` for `U_Si` and
  `U_Si_150421082041`, all with the same method. The timestamp suffix is how Xcalibur
  names a re-acquisition. Each second injection started about 3 s after the first one ended
  (2015-04-21, 03:51:26 → 03:51:29 and 08:20:38 → 08:20:41). The LFQ file therefore encodes one source per condition with
  technical replicates 1 and 2. This needs author confirmation.
- The deposited `.dat` and `.mzid` for `QE0380_Aysegul_030415_U_Si_150421082041` are
  copies of the `U_Ctrl_150421035129` search. They have the same byte size, and their
  COM/FILE fields name the Ctrl file. The RAW file itself is distinct.
- Mass tolerances aren't annotated. The Mascot searches used 0.05 or 0.1 Da, and the
  MaxQuant parameters behind the quantification weren't deposited.
- The di-Gly (K-ε-GG) antibody enrichment isn't encoded, because no ontology term for it
  was found. The Fusion Lumos dissociation method is CID with ion-trap detection, taken
  from the RAW header (`ActivationType = CID`).

## Review status

- `PXD011899-lfq.sdrf.tsv`: independent adversarial review **PASS**, round 2.
- `PXD011899-silac.sdrf.tsv`: **FAIL**, on one important finding: the unannotated
  `FL0067_AysegulS_3.raw`. This is the block described above. The two annotated rows
  were judged correct. The FL0067_AysegulS_2 → knockdown-set assignment is inferred
  from MS1 isotope spacing; no metadata states it.

## Needed to unblock

- An author statement or sample sheet giving the channel map of
  `FL0067_AysegulS_3.raw`, above all what the heavy (K8R10) channel contains. A
  deposited MaxQuant `mqpar.xml` or `experimentalDesign` would also do.
- Re-review afterwards, then promote with `git mv sandbox/PXD011899 datasets/PXD011899`.
  The LFQ file passes validation and could be promoted on its own.
