# PXD034528 annotation blocked

PXD034528 is a dimethyl-labelled study of *P. aeruginosa* (PA) and *P. aeruginosa* + *C. albicans* (PA+CA) biofilms grown on NCI-H292 human pulmonary mucoepidermoid carcinoma cells (Int J Mol Sci 2022 23(16):9202, PMID 36012475, PMC9409386, doi:10.3390/ijms23169202). The deposit has 127 files:
- 50 RAW files, `H292_Set{1-5}_F{1-10}.raw`. That is 5 sets × 10 fractions, and every combination is present.
- 50 matching `.mgf` files.
- For each set: `H292_SetN_F.msf`, `.msfView`, `.pdResult`, `.pdResultView` and `_Proteins.txt`.
- `H292_ATCC_26042022.pdStudy` and its `.bak` copy.

The label → sample map is contradicted between sources, and the deposited search outputs that could settle it were not readable today:
- **PRIDE sample protocol** (read from the OmicsDI mirror because the PRIDE API was down): it says "C, P, and CP" were labelled light, medium and heavy, gives "9 fractions" and "three biological replicates", and reports ratios "C/P and CP/P".
- **Deposit:** it has 5 sets × 10 fractions, which contradicts the protocol's 9 fractions and three replicates.
- **PRIDE data protocol and paper §4.3:** both search only *light and medium* dimethyl (+28.0313 / +32.0564) as fixed modifications, with no heavy label.
- **Paper (Fig. 2 legend):** it has two proteomic groups, PA+CA relative to PA, with "five samples per group". That fits a 2-plex per set (one PA and one PA+CA sample in each of the 5 sets). It does not fit a C/P/CP triplex. Neither the paper nor the protocol states which of the two groups was light and which was medium.
- So the protocol's label order looks templated (it does not match this deposit). Each of the 50 runs would need a group assigned to each label channel, and any assignment would be a guess. A wrong one passes validation and inverts every fold change.

Other open points that do not block on their own:
- **Instrument:** the PX record says Q Exactive HF (MS:1002523), while the paper and the PRIDE protocol both say "Q-Exactive Orbitrap Plus". The RAW header was not readable, so the conflict is unresolved.
- **Organisms:** PRIDE lists only *C. albicans*. In fact the co-culture samples contain *Homo sapiens* (NCI-H292), *P. aeruginosa* and *C. albicans*, and the PA samples contain human and PA. The PRIDE data protocol searched Human, PAO1 and SC5314 Swiss-Prot. The paper names only the PAO1 database, yet it analyses "host proteins". The organisms are clinical isolates, so strain = not available. This needs the campaign's co-culture convention (see PXD035814, sandbox).
- **Search settings** are recoverable from the PRIDE data protocol: PD 2.1 SEQUEST-HT, trypsin with 2 missed cleavages, 10 ppm / 0.02 Da, fixed Carbamidomethyl C plus fixed light/medium dimethyl on N-term and K, variable Oxidation M, DTT/IAA, Pierce high-pH RP fractionation, HCD 32% NCE, MS1 350-1400 m/z, DDA.
- **Time point for proteomics** is not stated (8 h and 24 h are used elsewhere in the paper).

**Evidence checked:**
- ProteomeCentral PROXI `PXD034528?resultType=full`: file list, instrument, species, publication.
- OmicsDI `ws/dataset/pride/PXD034528`: PRIDE sample/data protocol and a file list that matches the PROXI one.
- MDPI full text and the PMC9409386 render: Methods §4.1 and §4.3, and the Fig. 2 legend. The supplements are only Figs S1/S2, with no proteomics tables.
- PRIDE API v3: down (upstream error).
- `ftp.pride.ebi.ac.uk` and `ftp.ebi.ac.uk/pride-archive`: connection timeout, so the `.msf`, `.pdStudy`, `_Proteins.txt` and RAW headers could not be read.
- Europe PMC REST: rate-limited / upstream error.
- Payloads are saved in `/home/claude/bangkok3/scratch/PXD034528/`.

**To unblock:**
1. Read `H292_ATCC_26042022.pdStudy` (PD 2.1 study: sample names and conditions per quan channel) and/or the `.msf` `AnalysisDefinition`/quan-channel tables. Also read a `_Proteins.txt` header (the abundance-ratio labels) to fix which group is light and which is medium.
2. HTTP-range the first ~256 KB of one RAW file to settle HF vs Plus.

If the pdStudy carries no conditions either, the authors must supply the light/medium assignment. Once the map is known, the SDRF has 100 rows (50 RAW × 2 labels).
