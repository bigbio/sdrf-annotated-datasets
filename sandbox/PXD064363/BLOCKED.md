# PXD064363 annotation blocked (no acquisition files deposited)

PXD064363 is the LRBA / CTLA4 degradation study (Ge X et al., Nat Commun 2025; PMID 41390689; PMC12815959; doi:10.1038/s41467-025-67365-5). PRIDE marks the submission as `PARTIAL`.

**The deposit holds no mass-spectrometry run file.** The PRIDE v3 file list has three files:

| file | PRIDE category | what it actually is |
|---|---|---|
| `LC427_Statistics_Summary.raw` | RAW | a gzip stream (magic `1f 8b 08 00`), not a Thermo RAW. It decompresses to an xlsx that is byte-identical to `LC427_Statistics_Summary.xlsx` |
| `LC427.rar` | SEARCH | a RAR5 archive whose only member is another copy of the same xlsx |
| `LC427_Statistics_Summary.xlsx` | OTHER | a processed protein table: 6,410 proteins × abundances `C427-1..3` / `Ctrl-1..3` |

A genuine Thermo `.raw` begins with `01 A1` followed by UTF-16 "Finnigan"; this file does not. There is also no search-engine output (no `.msf`/`.pdResult`/params). An SDRF has nothing to put in `comment[data file]`, and listing the xlsx as a run would fabricate a data file. No SDRF is emitted.

**Metadata the record already supports** (for when it is unblocked):
- Organism: Mus musculus.
- Sample: mouse splenic T cells, CD3/CD28-activated for 5 days.
- Factor: LC427 vs DMSO vehicle (protocol; paper Fig. 3A).

**To unblock:** the submitters upload the real Thermo `.raw` acquisitions (LTQ-Orbitrap Velos Pro) plus the Proteome Discoverer result and ideally a TMT channel-to-sample map, or PRIDE reclassifies the mislabelled `.raw`.
