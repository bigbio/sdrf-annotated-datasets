PARTIAL: 1960 of 1976 deposited RAW files are annotated (from the authors' deposited MaxQuant summary.txt); 16 RAW files have no public sample map and are left out.

Unmapped PRIDE RAW files (not in any deposited search output, not described in the paper or PRIDE):
- PT4923-1.raw, PT4923-2.raw, PT4923-3.raw, PT4923-4.raw
- PT5013-1.raw ... PT5013-12.raw (12 files)

Sources checked for these 16 files: the paper's full text (PMC5989152) and its supplementary list, the PRIDE
project and file records, txt.zip members txt/summary.txt (2112 raw files) and "phospho search/summary.txt"
(672 raw files) and "phospho search/experimentalDesignTemplate.txt". None of them lists PT4923 or PT5013.
The Europe PMC supplementaryFiles endpoint returned HTTP 500. txt.zip/methyl_txt.zip (a 10 GB nested archive)
was not opened.

The opposite gap also exists: 152 raw files that the MaxQuant search used are not in PRIDE (PT5064: 95 of 96,
PT5074: 57 of 96). Because of it, Exp B LMH_OHT_T48 replicates 2-3 and LMH_OHT_T06 replicate 2 have no
deposited files, and LMH_OHT_T48 replicate 1 has only fraction 21.

Files:
- PXD009270-expA-abundance.sdrf.tsv: Exp A, SILAC 2-plex abundance time course (672 raw files, 1344 rows)
- PXD009270-expB-turnover.sdrf.tsv: Exp B, pulsed-SILAC 3-plex turnover (1288 raw files, 3864 rows)
- *.evidence.json: evidence manifests; validation.txt: validation log; build/: samples/technical tables,
  build/mapping_gaps.json lists both file gaps; scripts/: the table and manifest generators and the
  range-read zip extractor that was used on txt.zip.

## Sandbox notes
- This is a partial annotation, kept in `sandbox/` because the files listed above as unmapped have no public sample/channel map. Promote to `datasets/` only once they are resolved and the annotation passes `parse_sdrf validate-sdrf`.
- Working files mentioned above (evidence/, validation output, scripts, tables) are not part of this submission.
- Review status: the SDRF(s) in this folder passed an independent fresh-context adversarial review.
