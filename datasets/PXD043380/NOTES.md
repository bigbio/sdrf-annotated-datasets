# PXD043380 — annotation notes

## Removed rows: `CD_CZC_190819` (pooled QC sample, 3 fractions)

The original SDRF included 3 rows for a pooled QC sample `CD_CZC_190819`
(`characteristics[biological replicate] = pooled`,
`factor value[host disease status] = not applicable`), with data files:

- `CD_CZC_190819_X.raw`
- `CD_CZC_190819_X1.raw`
- `CD_CZC_190819_X2.raw`

These 3 files are declared in iProX's own ProteomeXchange announcement XML
(`http://download.iprox.org/IPX0006051000/PX_IPX0006051000.xml`) but return
HTTP 404 from iProX's download server
(`http://download.iprox.org/IPX0006051000/IPX0006051001/...`). This was
verified by HEAD-checking every one of the 276 raw files declared in that
XML: 273/276 resolve (HTTP 200); only the 3 `CD_CZC_190819` files 404. So
this is an isolated, confirmed gap in what iProX actually serves, not a
transient error or a broader deposition problem.

The rows were removed rather than kept with a placeholder, because:

- The sample is a pooled QC injection, not one of the 89 study subjects
  (26 CD / 29 UC / 34 controls, matching Zhang et al. 2024, *ISME Journal*,
  PMID 39073916) — removing it does not affect the disease-status
  comparison or sample counts.
- `comment[data file]` disallows the `not available` reserved word per
  `TERMS.tsv` (`allow_not_available = false`), so there is no spec-legal way
  to keep the row without a real, retrievable filename.
- Keeping an unretrievable filename in the SDRF would break automated
  reprocessing pipelines that fetch files by `comment[data file]`.

If iProX restores these files, the rows can be re-added; the removed content
is preserved in git history (see the commit removing them).

The missing-file gap itself is a repository-side issue and has not been
fixed by this change — it should be reported separately to iProX /
ProteomeXchange.
