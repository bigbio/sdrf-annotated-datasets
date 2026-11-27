# PXD004652 annotation blocked

PXD004652 is the hESC-to-MSC differentiation proteome and phosphoproteome study by Billing et al. (Mol Cell Proteomics 2019, 18(10):1950-1966, DOI 10.1074/mcp.ra119.001356, PMID 31332097, PMC6773553). The paper cites PXD004652 in its Data Availability section. It does not mention PXD004658. It is a reductive-dimethyl **triplex** study on a Q Exactive. Light is a pooled standard of all samples. Each time point was labelled medium or heavy. The time points are ES04 hESC D0, 8 h, D1, D2, D5, D15 and D30, each in biological triplicate (21 samples).

The deposit has 11 sets (`Sample01`-`Sample11` / `Sample_1`-`11` / `Hilic_10`, `Hilic_11`):
- **Proteome:** OFFGEL, 12 fractions (`OG1`-`OG8_SampleNN`, `OGFraction9`-`12_SampleNN`, including several `_Rerun` files).
- **Phosphoproteome:** HILIC, 16 fractions (`Hilic_Sample_N_Fraction_NN`), plus one multiphosphorylated SIMAC run per set (`20140709_QE_NEG_..._Simac_01`-`11`).
- **Additional series:** `20140828_..._Kinetics_SIMAC_Fraction_01`-`11`, which the paper does not describe.

**Why blocked:** there is no stated set/channel → sample map.
- The paper does not say which time point or replicate is medium or heavy in which set. It has no labelling table, and Fig. 1 shows only the harvest schedule.
- The capacity does not resolve it either. 11 sets × 2 channels = 22 slots against 21 stated samples, and the paper does not say whether BM-MSCs were in the proteomics.
- Any assignment would be guessed, so per the campaign rules no SDRF is emitted.

**Evidence checked:**
- PROXI full record (file list, Q Exactive, mods phospho/oxidation/acetyl/IAA).
- PMC6773553 full text: Methods give DTT/IAA, Lys-C + trypsin, OFFGEL 12 fractions, TiSH/HILIC 16 fractions + 1 multi-phospho fraction, HCD NCE 25 and Top10. MaxQuant settings: 20/4.5 ppm and 20 ppm MS/MS, carbamidomethyl fixed, phospho STY / deamidation N / oxidation M variable, triplex dimethyl.
- PRIDE FTP directory: connection timeout today. Europe PMC REST: upstream error / rate limit.

**To unblock:**
- Read `MaxQuant_output_txt.zip` (about 1 GB+): `summary.txt` or `parameters.txt`, plus `mqpar.xml` if present. Raw file → experiment names could carry the time-point labels.
- Alternatively, get the label layout from the authors (Graumann lab, WCM-Q / MPI Bad Nauheim).
- Also needed: what the `Kinetics_SIMAC` series is, and whether set 11 or a 22nd slot holds BM-MSC or a spare.

Search parameters and sample metadata are otherwise ready: Homo sapiens; ES04 hESC line (WiCell; Cellosaurus accession still to verify); Q Exactive MS:1001911; Lys-C + trypsin; dimethyl channel UNIMOD accessions to be taken from the MaxQuant label definitions (not stated in the paper).
