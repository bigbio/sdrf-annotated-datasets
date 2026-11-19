# PXD020812 — sandbox brief (partial)

**Dataset:** Adipose MDM2 regulates systemic insulin sensitivity (Hallenborg et al., Sci Rep 2021 11:21839, PMID 34750429). Odense (B. Blagoev lab).

**Status:** partial. It annotates 124 of 191 RAW files (248 rows): the in vivo SILAC epiWAT proteome. It passes `parse_sdrf validate-sdrf` (ms-proteomics + vertebrates v1.1.0) and `sdrf_review.py`.

## Annotated

- **64 runs:** `20170920SSR_QexXn2_091425cmr_{WT,HET}{1-8}{,_2,_3,_4}.raw`. These are 8 wild-type and 8 *Mdm2* Adi+/- epiWAT lysates (light), each mixed 1:1 with a Lys6 SILAC reference (heavy) and each run with 4 methods. The MaxQuant groups (Sens / Fast / SuperFast / Slow) come from the deposited `*_evidence.txt` `Experiment` and `Raw file` columns and are recorded as technical replicates 1–4. Instrument: Q Exactive HF-X (RAW header).
- **60 runs:** `20171013_SSR_{20,80}{WT,HET}{1-14,flowthrough}.raw` (MaxQuant group "Opt"). These are high-pH fractions of WT and HET material; flow-through is fraction 15, and `20HET3_171016181238` is a re-injection (technical replicate 2). Instrument: Q Exactive HF.

## Not yet annotated (67 files)

- **45 runs, MDM2 co-IP:** three antibodies (4B2 = `IP_Cyt_*`, 2A10, SMP14), 15 gel bands each, SILAC Arg6/Lys4 vs Arg10/Lys8. Which SILAC state is IgG and which is anti-MDM2 is not stated in the paper, PRIDE or the evidence files.
- **12 runs, MORC2 IP** (`IP_MORC2_*`), and **10 runs, MORC2 RIME** (`IP_MORC2_RIME_*`). These are triple SILAC (L/M/H): IgG, siGFP and siMdm2 by the figure legend, but the label → condition order is not stated. The RIME raw names in the evidence file (`1st`, `1stUrea`, `1ststar`) do not match the PRIDE file names one-to-one.
- **To unblock:** the SILAC label → condition map, from the authors or the MaxQuant `mqpar.xml` if it can be obtained.

## Open points for a reviewer

- The meaning of the "20" and "80" prefixes is not stated. They are recorded as two fraction sets, each with *pooled* WT/HET material. Whether these are pools or single mice is not stated.
- **Sex and age are `not available`.** The paper's metabolic cohort is male mice on high-fat diet, but the proteomics has 8 HET mice while the reported male HET cohort is N = 7, so the cohort match is not assumed.
- The run group MaxQuant calls "Slow" (`_4`) uses a method file named `Olsen_FAST_Top20`. Both names are recorded.
- The paper says CID, but the instrument is a Q Exactive. HCD is recorded, and fragment tolerance is 0.5 Da as stated.
