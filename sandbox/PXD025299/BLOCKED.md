# PXD025299 annotation blocked

PXD025299 is a GlycopeptideGraphMS glycoproteomics study of biologics (Pang et al., Front Chem 2021, 9:661406, DOI 10.3389/fchem.2021.661406, PMID 34084765; the paper's Data Availability statement cites PXD025299). It covers human serum IgG, trastuzumab (Herceptin), adalimumab (Humira), and an in-house CHO-K1 trastuzumab biosimilar from 14-day Ambr250 fed-batch cultures in SAFC or GE medium. The data were acquired in MSe mode on a Waters BioAccord (ACQUITY RDa compact TOF detector).

There is no deposited run-level data file that can carry a sample:
- **The 6 "RAW" files are UNIFI export packages**, not acquisition runs. The paper states the data were "exported as .uep file using the UNIFI Scientific Information System". The files are 2.4–4.3 GB each. Every package bundles several distinct samples:
  - `IgG_Trastuzumab_Adalimumab_ProteomeXchange.uep` holds three different proteins (serum IgG, trastuzumab and adalimumab). The paper uses n = 4 for these.
  - `Trastuzumab_<SAFC|GE>_<RxBy>_D3-14_ProteomeXchange.uep` (x5) each hold a time course from day 3 to day 14 of the culture. The Methods give days 3/5/7/9/14, but the Results say "every 2nd day from days 3 to 14".
  - `Trastuzumab_GE_R5B3_R2B3_D3-14` also merges two bioreactors.
- **The injection list inside each .uep cannot be read.** It is a proprietary multi-GB Waters archive, and no range read is possible from this environment. The paper does not state the injections per sample. The bioreactor codes (R2B5, R3B3, R4B7, R3B1, R5B3, R2B3) do not appear in the paper.
- One SDRF row per .uep would need one sample identity per package. That would collapse different proteins, days and bioreactors into a single sample, so it would be fabricated. Splitting a package into per-injection rows would need invented assay names.

**Instrument (verified):** the paper says BioAccord LC-MS / ACQUITY RDa detector. The PX record says "Waters instrument model" (MS:1000126). A live OLS search of PSI-MS for "RDa", "ACQUITY RDa" and "BioAccord" returned no specific term, so an SDRF would have to use MS:1000126 with the model named in the report.

**Deposited vs annotatable:** the FTP listing has 8 entries:
- 6 .uep files (3.1G, 3.1G, 4.3G, 2.5G, 2.4G, 2.4G)
- `Results.zip` (229K, SEARCH, mapped to all 6 packages)
- `README.txt`

The campaign cache count of "6 RAW / 7 files" is confirmed. None of the six packages maps to a single sample, so 0 are annotatable.

**Evidence checked:**
- ProteomeCentral PROXI record (v2, 2024-10-22).
- PRIDE FTP directory listing and README.txt.
- Frontiers full text (Methods, Results, figure captions, Data Availability).
- OLS PSI-MS for an instrument term.

Not opened: `Results.zip`. It is a binary zip, and downloading it needs user approval. It holds Progenesis QI / GraphMS outputs, which may list per-injection names but cannot change the fact that the data files are multi-sample bundles.

**To unblock:** either of these would work:
- Per-injection raw files (Waters `.raw` folders exported from UNIFI, or mzML per injection), deposited by the authors.
- An injection manifest for each .uep (sample name, protein, medium, bioreactor, day, replicate), plus acceptance that one .uep can be annotated as a multi-sample container. That would need a spec-level decision.

`Results.zip` should be inspected first, in case it has per-injection names that could seed such a manifest.

Scratch evidence: `/home/claude/singapore2/scratch/PXD025299/` (px_record_summary.txt, ftp_listing.txt, paper_notes.txt).
