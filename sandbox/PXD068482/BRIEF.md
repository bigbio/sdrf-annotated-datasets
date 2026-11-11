# PXD068482: two mapped experimental blocks; 37 acquisitions still lack a design map

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD068482), all 91 RAW headers, all 91 Mascot DAT-to-RAW links, the corresponding mzIdentML software records, and the [author preprint](https://doi.org/10.64898/2026.03.16.712046). The preprint source XML, including its supplementary methods, was available; the later journal DOI in PRIDE was not used as an inspected full text.

## Mapped subsets

| Draft | Acquisitions | Supported design |
| --- | ---: | --- |
| `PXD068482-asynchronous.sdrf.tsv` | 24 | P31/FUJ, MV4-11 and HL-60; DMSO or C-604; four independent experiments per combination |
| `PXD068482-mitotic.sdrf.tsv` | 30 | P31/FUJ: asynchronous DMSO plus three STLC-arrested treatment groups; HeLa: two STLC-arrested groups; five independent experiments per combination |

The `Exp01`/`Exp02`, cell-line, condition and R-number tokens are explicit in the deposited filenames. Figures 2 and 3 independently establish the experiment designs and independent repeat counts. C-604 was used at 2 uM for two hours; the CDK1 inhibitor is RO-3306 at 10 uM. STLC arrest was 5 uM for 18–20 hours. The filename condition `STLC` denotes the arrested vehicle comparison, while `GWLi`/`CDKi` in `Exp02` also follow STLC arrest. The asynchronous `DMSO` control in `Exp02` is retained separately. Author R numbers are preserved as experimental blocks, without asserting the same starting culture across conditions.

The cell lines are resolved through [P31/FUJ CVCL_1632](https://www.cellosaurus.org/CVCL_1632), [HL-60 CVCL_0002](https://www.cellosaurus.org/CVCL_0002), [MV4-11 CVCL_0064](https://www.cellosaurus.org/CVCL_0064) and [HeLa CVCL_0030](https://www.cellosaurus.org/CVCL_0030). Their donor metadata are not ages or identities of the experimental cultures. In particular, HL-60 is derived from a female donor.

## Methods and actual search records

All 91 RAW headers identify Q Exactive Plus. The selected intact-cell experiments have physical trypsin-bead digestion, DTT reduction, iodoacetamide alkylation and TiO2 phosphopeptide enrichment. Their reported DDA/HCD acquisition spans 375–1500 m/z. Collision energy is left unavailable rather than extrapolated from another instrument batch.

The deposited DAT files establish one-to-one RAW links, 10 ppm precursor/25 mmu fragment search tolerances, two missed cleavages, fixed C carbamidomethylation and variable M oxidation, N-terminal Q pyroglutamate and S/T/Y phosphorylation. Software versions are assigned per linked result: the full deposit contains Mascot 2.8.3 and 3.0.0 outputs, not one inferred common version. The linked peak-picking metadata report Mascot Distiller 2.8.3.0. The generic instrument accession in Mascot is superseded by the actual RAW model.

## Unresolved acquisitions

The 24 `QE1_SMMG_EXP03_PP_Sample_*` files, nine `QE1_SMMG_Kinase_Assay_Exp1_Sample_*` files and four `QE2_Sandra_Exp141_Sample_*` files do not provide a per-file condition map. The paper describes knockdown, fixed-cell kinase and purified-protein assays, but their numerical sample order cannot establish that map. The nine fixed-cell kinase results also omit fixed carbamidomethylation, so the intact-cell preparation/search settings must not be applied to them wholesale.

These 37 RAW files are deliberately absent from the two drafts. Thus coverage is **54 of 91**, and the accession remains in `sandbox/` pending a sample sheet or other direct mapping for the remaining experiments. File order, groups of three and consecutive sample numbers are not substitutes for that evidence.

## Local validation

Both subsets pass the ms-proteomics, human and cell-lines templates and the repository review script. They remain sandbox drafts because 37 deposited RAWs lack a condition map. The record-reconciliation heuristic flags disease on DMSO controls and compares some mixed-line rows against the first row: vehicle-treated cancer cell lines retain their disease provenance, and organism part is assigned separately to each verified cell line. Offline ontology warnings are retained in the validation logs.
