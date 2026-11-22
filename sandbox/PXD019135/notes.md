# PXD019135

BLOCKED: the HGF stimulation arm and the replicate number for each gel lane (MaxQuant experiments `MAS 1`-`MAS 6`) are not in any public source I could read, so the file cannot go in `datasets/` yet.

## What is annotated and evidenced
- 24 raw files `392MAS_<lane><A-D>.raw`: 6 SDS-PAGE lanes × 4 gel slices (fractions 1-4). Source: MaxQuant `combined.zip` → `txt/summary.txt`, and the paper's Methods ("each lane was cut into 4 pieces").
- SILAC triplex, 3 rows per raw file (72 rows):
  - light (R0K0) = Hepa1-6 with empty pWPT vector (HV)
  - medium (Arg6/Lys4, UNIMOD:188 / UNIMOD:481) = Hepa1-6 with SOCS1 wild type (HS)
  - heavy (Arg10/Lys8, UNIMOD:267 / UNIMOD:259) = Hepa1-6 with SOCS1 R105K (HR)

  Sources: bioRxiv 10.1101/2020.07.31.231225 (Methods and Fig. 1B legend), and the MaxQuant `summary.txt` labels.
- `factor value[genotype]` = the three cell line variants.

## Why this is in sandbox
- The design is 3 genotypes × 2 treatments (unstimulated vs HGF 25 ng/ml for 24 h) × 3 experiments, which gives the 6 lanes.
- Which lane is HGF-stimulated, and which experiment each lane belongs to, is not stated in:
  - the PRIDE record
  - the MaxQuant output (`summary.txt`, `parameters.txt`, `proteinGroups` headers only name `MAS 1`-`MAS 6`)
  - the preprint text
- Only Figure 1A of the preprint might show it. bioRxiv returned HTTP 429 every time I tried to fetch it.
- The published version (Biochimie 2021, doi:10.1016/j.biochi.2021.01.012, PMID 33493533) is not open access.
- So `characteristics[treatment]` is `not available`, there is no `factor value[treatment]`, and `characteristics[biological replicate]` is `1` for every source. That is a placeholder: the real replicate numbers 1-3 depend on the same missing lane map.

## Return criteria
- The lane → (treatment, experiment) map for `MAS 1`-`MAS 6`, from Fig. 1A, the Biochimie paper or the submitters.
- Confirm the inferred structure (one lane = one experiment × one treatment). The paper says proteins "from three experiments were pooled" / "mixed into two combinations", which could also mean pooled lanes or technical replicates. If so, revisit the source-name granularity (currently one source per genotype per lane).
- Then: set `characteristics[treatment]` and `factor value[treatment]`, renumber `characteristics[biological replicate]` 1-3 within each genotype × treatment, re-validate, get a fresh independent review, and `git mv` the folder to `datasets/PXD019135/`.
