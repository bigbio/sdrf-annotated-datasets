# PXD054427 annotation blocked

PXD054427 (Susanto et al., Mol Cell 2024, RAPIDASH, PMC11460945, DOI 10.1016/j.molcel.2024.08.023) is a single TMT injection, `Dinman_comparison_TMT.raw`. It is the only RAW among 9 files: 1 RAW, mqpar.xml, proteinGroups.txt, mzTab, 4 `allSpectra.CID.FTMS.iso_*.apl`, and checksum.txt. The file list matches the cache. The PX title says "yeast ribosomes", but the paper's Data Availability says "RAPIDASH and ribosome chromatographic purification (Meskauskas, et al.) of E14 mESCs". So the samples are mouse ESCs prepared with the original yeast protocol versus RAPIDASH, and the organism is Mus musculus, not yeast.

The channel → sample map is not available from any source I could read:
- **Paper Table 1 (TMT sample/tag table):** it covers only the sucrose-cushion comparison (130/131) and the E12.5 tissues (126–128). It has no row for the chromatography-vs-RAPIDASH comparison. The bioRxiv preprint (PMC10723405) is the same.
- **Text:** "only 61 proteins gave quantifiable signal in the reporter ion channel for the original chromatography protocol (Table S1)". This names neither the TMT tags nor the replicates.
- **Table S1** (`NIHMS2020487-supplement-2.xlsx`, the PX record's own pointer) could not be read. PMC returned a reCAPTCHA page, cell.com was not permitted in time, and Europe PMC/EBI was unreachable.
- **Deposited MaxQuant mqpar.xml / proteinGroups.txt (read 2026-11-26 via PRIDE FTP over HTTPS):** mqpar has `experiments` empty and `referenceChannel` empty. `isobaricLabels` is the full default TMT6plex set (126–131), with no sample names. The proteinGroups header has only `Reporter intensity [corrected|count] 1..6`. Signal is present in more than two channels (for example Rpl21: 23441 / 172 / 13942 / 9044 / 1535 / 14175), so the injection is not a simple two-sample 130/131 design. Nothing says which channel holds which preparation or replicate. `mzTab_reformatted.mzTab.gz` could not be read in the browser (gzip). The directory listing confirms 9 files and 1 RAW (`Dinman_comparison_TMT.raw`, 550 MB). The mqpar file path (`...\supp_tables\S1\Dinman_comparison\`) ties this RAW to Table S1.
- **Zenodo 10.5281/zenodo.13286233 / GitHub theosusanto/RAPIDASH:** these hold ribosome-profiling R scripts only, with no TMT layout.

Search and MS parameters are recoverable from the same paper (see PXD054298.report.md): Orbitrap Elite, HCD 40% NCE, TMTsixplex, MaxQuant 2.4.2.0. Without channel identities, though, no SDRF is emitted. How many channels were used (2 or more, any replicates) is also unknown.

**Evidence checked:** ProteomeCentral PROXI record (full); PMC11460945 JATS (efetch) and HTML; PMC10723405 preprint; Zenodo API; GitHub tree; attempts at PRIDE FTP and API, Europe PMC, cell.com and the PMC supplement. Scratch notes are in `/home/claude/singapore1/scratch/PXD054427/`.

**To unblock:** read Table S1 (mmc2/NIHMS supplement 2) for the reporter-channel assignment, or the `MTD assay[n]`/`sample[n]` lines of the deposited mzTab, if the submitter filled them; MaxQuant usually leaves them generic, and the gzip could not be decompressed in the browser. Alternatively, get the layout from the authors.
