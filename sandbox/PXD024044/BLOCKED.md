# PXD024044 annotation blocked (no public TMT channel-to-sample map)

PXD024044 is the hypoxia extracellular-vesicle proteome study (PMC7999156): EVs from adipose-derived mesenchymal stem cells grown under normoxia or hypoxia.

**The design cannot be resolved from public sources.**

- **One RAW file.** `20191126_KKL_AG_Exosomes.raw` is a genuine Thermo file (Q Exactive HF, TMT10 method, matching PRIDE). The paper says it holds 6 EV samples: 3 normoxia and 3 hypoxia.
- **No channel map anywhere.** These sources were checked:
  - the paper, which says "three nEVs versus three hEVs" but gives no channel assignment;
  - the deposited supplement (s001.pdf), which has no proteomics layout; Table S1 is not in the PMC or Europe PMC copy, and the publisher's supplement link was not reachable;
  - the deposited Proteome Discoverer `.msf`, which has 10 samples with default names and empty factors;
  - the Data Availability statement, which cites only PXD024044.
- **Cannot be inferred from the data.** Reporter signal is dominated by 127N and 127C (about 46% and 30% of each spectrum's signal), so it is not even clear which 6 of the 10 channels were used, and the published markers (CFL1, CXCL8) do not separate a 3 vs 3 split.

**Other notes (ready for a future SDRF)**
- Run-level values are prepared and verified in OLS4: Lys-C + trypsin, HCD at NCE 35, Orbitrap MS2, DDA, 10 ppm / 0.02 Da (from the `.msf`), TCEP reduction; TMT6plex on peptide N-term and K (fixed), Oxidation M, protein N-term Acetyl, Met-loss and Met-loss+Acetyl.
- The PRIDE processing text lists TMT6+K8 and Arg10; the deposited search contradicts it, so the search was followed.
- The cysteine alkylation (+113.084 Da, 2-chloro-N,N-diethylacetamide) has no UNIMOD or PRIDE term.
- Expected sample values: Homo sapiens, adipose tissue, mesenchymal stem cell of adipose tissue (CL:0002570), female, normal; factor treatment = hypoxia vs normoxia.

**To unblock:** the authors' channel table for this run, for example the Proteome Discoverer `.pdStudy`, the full publisher supplement, or a sheet from the submitter.
