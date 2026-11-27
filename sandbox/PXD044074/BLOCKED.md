# PXD044074 annotation blocked (no public TMT channel-to-sample map)

PXD044074 is a TMT10 mitochondrial proteome of HEK293T cells: empty vector, WT-MOF and mtMOF, with 3 channels each, so 9 of 10 channels are used (Hu et al., Cell Rep 2024, doi:10.1016/j.celrep.2024.114839, PMID 39392752).

**The design cannot be resolved from public sources.**

- **One RAW file.** It is a genuine Thermo file (Q Exactive Plus, Top10 DDA, HCD at NCE 35).
- **No channel map anywhere.** Nothing says which channel carries which sample, or which channel is empty. Sources checked:
  - the paper Methods, which say only "3 channels for each sample", and Figure 4A, which has no channel numbers;
  - supplementary Document S1 (figures and a primer table only);
  - the deposited Proteome Discoverer `.msfView`, which has ID index tables only, with no study grouping, channel table or search parameters;
  - the RAW header sample information;
  - Europe PMC, which does not hold the article;
  - the Data Availability statement, which cites only PXD044074.

**Other notes (ready for a future SDRF)**
- Instrument is Q Exactive Plus, from the RAW file and the paper; PRIDE lists Q Exactive. MS2 resolution is 35,000 in the RAW file and 17,500 in the paper.
- Search settings differ between the PRIDE protocol (10 ppm; TMT on K and N-term, acetyl on H/K/S/T/Y) and the paper (20 ppm; acetyl-K and Met oxidation). No search-parameter file was deposited.
- Reagents verified in OLS4: DTT (PRIDE:0000608) and IAA (PRIDE:0000599). Cellosaurus CVCL_0063 has no Population comment, so ancestry would be not available.

**To unblock:** the channel layout from the lead contact, or a Proteome Discoverer `.msf`/`.pdResult` containing the study grouping.
