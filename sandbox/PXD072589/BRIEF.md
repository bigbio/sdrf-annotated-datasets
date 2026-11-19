# PXD072589 — sandbox brief

**Dataset:** Modelling synaptic maturation from growth cone to synapse in human organoids. Odense (M.R. Larsen lab). Paper: J Neurochem 2026 170(5):e70458, PMID 42108706 / PMC13158549.

**Status:** draft for review. It covers all 196 of 196 deposited files (911 rows). It passes `parse_sdrf validate-sdrf` (ms-proteomics + vertebrates v1.1.0). The only warnings are the non-enum `material type = organoid` and the usual HCD lookup notice. It also passes `sdrf_review.py`. Not independently reviewed.

## Sub-experiments

| Files | Specimen | Workflow | Instrument |
|---|---|---|---|
| 20 | ALI-CO day 150 (H9, CVCL_9773) | differential centrifugation: H, P5000, P12000, P22000, cytosolic × 4 | timsTOF Pro, DIA-PASEF |
| 15 | ALI-CO day 90 (H9) | same 5 fractions × 3 | timsTOF Pro |
| 20 | Forebrain organoid day 100 (IMR90-4, CVCL_C437) | 5 fractions × 4 | timsTOF Pro |
| 20 | Human neocortex (non-tumorous, from glioma surgery) | 5 fractions × 4 | timsTOF Pro |
| 16 | Mouse W8, Percoll workflow | H, P1, F3, F4 × 4 | timsTOF Pro |
| 40 | Mouse P2 and W8 | 5 fractions × 4 | Orbitrap Exploris 480, DIA |
| 15 + 15 | ALI-CO day 90, TMTpro 12 ch: P5000/P12000 × control/KCl × 3 | phospho (TiO2) and non-modified, high-pH fractions | Orbitrap Eclipse |
| 15 + 20 | ALI-CO day 150, TMTpro 12 ch (126–129N, 131C–134N) | phospho and non-modified | **Orbitrap Fusion Lumos** (RAW header) |

The TMT channel maps come from the PD `.msf` study factors.

## Open points for a reviewer

- **Inferred channels.** Two channel factors were unreadable in the `.msf` byte stream: D90 phospho 132N and d150 phospho 128C. They were filled from the 3-per-group block pattern (P12000 KCl and P12000 control respectively), which the non-modified `.msf` of each set agrees with.
- **Instrument conflict.** The paper says all TMT runs were on an Eclipse, but the RAW headers of the d150 runs say Orbitrap Fusion Lumos. The header is used.
- **d150 phospho fractions f8–f10.** These are 50-min "rescue" re-runs (original names `..._f8_rescue.raw` etc.). The PD file set also names the original material `P&deglyco`; deglycosylation is not described in the paper.
- Fractions deposited but not in the PD file set: D90 phospho HpHF10 and d150 non-modified f4. Both are kept.
- **Replicate model.** The S1 fraction was split into 3–4 workflow replicates, recorded as technical replicates of one biological sample per specimen and fraction. The H (homogenate) aliquots are treated the same way.
- **Human cortex donor.** Age and sex are not given. The tissue is non-tumorous but came from high-grade glioma patients; disease is set to `normal`. A reviewer may prefer the donor's diagnosis.
- **Mouse P2/W8 instrument.** The paper is internally inconsistent (one passage says timsTOF). The `.raw` files are Exploris 480 per their headers.
