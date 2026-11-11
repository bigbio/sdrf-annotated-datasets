# PXD069978: four patient identifiers; R1/R2 preparation stage unresolved

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD069978), all 16 RAW headers and linked Mascot DAT/mzIdentML metadata, and Figure 6 plus supplementary methods in the [author preprint](https://doi.org/10.64898/2026.03.16.712046).

The 16-row draft represents four deposited patient codes, F6659, F8757, F8903 and R3762, each with DMSO and C-604 acquisitions labelled R1/R2. Figure 6 states that four patients underwent phosphoproteomics, although eight were included in the separate viability experiment. Accordingly, biological identifiers follow the four patients and do not count R1/R2 as eight donors.

Primary mononuclear cells were treated ex vivo with 2 uM C-604 or vehicle for two hours. Supplementary methods give a final DMSO concentration of 0.2%. Cells originated from peripheral blood or bone marrow, but the per-patient collection site is not resolved; organism part, age and sex remain unavailable.

All RAWs identify Q Exactive Plus. The physical protocol reports trypsin-bead digestion, DTT, iodoacetamide and TiO2 enrichment. The actual DAT files map one-to-one to all 16 RAWs and specify 10 ppm precursor/25 mmu fragment tolerances, two missed cleavages, fixed C carbamidomethylation, and variable M oxidation, N-terminal Q pyroglutamate and S/T/Y phosphorylation. Matching mzIdentML files identify Mascot 3.0.0; peak processing identifies Mascot Distiller 2.8.3.0.

The public methods do not establish whether R1/R2 are repeated injections or independently prepared aliquots. Their literal codes remain in a separate field, and technical replicate stays `not available`. Acquisition-linked source names do not imply distinct donors or proven independent cultures. Keep this draft in `sandbox/` until the replicate stage and specimen origin can be resolved. The 3–4 technical replicates reported for viability assays are not assigned to the phosphoproteomics files.

## Local validation

The ms-proteomics and human templates, and consequently the repository review script, fail only because technical replicate is unavailable. This preserves the unresolved R1/R2 stage. The record-reconciliation disease-on-control warning is not applicable: both vehicle and drug arms are cells from patients with AML. Offline ontology warnings are retained in the validation logs.
