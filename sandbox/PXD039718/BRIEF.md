# PXD039718 — sandbox draft

Korat chicken thigh muscle, 3 high-FCR vs 3 low-FCR males at 10 wk (Kaewsatuan P et al. Poult Sci 2023;102:102741, PMC10192536, read). Protocol and MaxQuant settings from the paper (trypsin, Carbamidomethyl C fixed, Oxidation M + Acetyl protein N-term variable, 6 ppm / 20 ppm). Instrument: paper Q Exactive vs PX Q Exactive HF (paper used). **Open:** RAW names end in `H`/`L` (`TH76H`, `TH2L` …), but the paper names its groups both by FCR (high/low) and by FE (low-FE = high FCR), so `H` is ambiguous. `phenotype` left `not available` until the deposited MaxQuant `txt.zip` or the authors settle it.

Validation: fails only on `comment[cleavage agent details] = not available` (or hollow factor), the reason for sandbox.
