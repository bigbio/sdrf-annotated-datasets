# PXD050991 — sandbox

BLOCKED: this was screened as a SILAC dataset, but PXD050991 is the **label-free DIA**
part of the study. It is kept in `sandbox/` until a curator decides whether a
label-free annotation should go to `datasets/` here. The SILAC data are in the
companion accessions PXD051015 (dynamic SILAC turnover) and PXD051016
(microfluidic devices, differential dynamic SILAC).

Evidence:

- Publication: Cavarischia-Rega C, Sharma K, Fitzgerald JC, Macek B. *Proteome
  Dynamics in iPSC-Derived Human Dopaminergic Neurons.* Mol Cell Proteomics 2024;
  doi:10.1016/j.mcpro.2024.100838, PMID 39251023, PMC11474371. Data Availability:
  "PXD050991 (DIA dataset), PXD051015 (turnover dataset), and PXD051016
  (microfluidic devices)".
- Deposited search (`dataset_1_dia.zip` → `mqpar.xml`): MaxDIA, multiplicity 1, no
  label modifications. Label-free quantification was used.

The SDRF (`PXD050991.sdrf.tsv`, 27 rows: 3 biological replicates × 9 high-pH
fractions, `label free sample`) passes
`parse_sdrf validate-sdrf -t ms-proteomics -t human -t dia-acquisition`.

Open points:

- The iPSC line name and Cellosaurus ID are not given in the paper; it cites only
  Schwarz et al. 2021.
- Donor age and ancestry are not reported.
- The dissociation method is not stated for the DIA runs.
- There is no factor value column because this is a single-condition reference
  proteome.
