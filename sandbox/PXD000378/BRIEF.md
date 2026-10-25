# PXD000378 — replicate independence unresolved

Evidence checked on 2026-09-28: [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD000378), five deposited Mascot result headers and mzTabs, all five RAW method headers, [paper](https://doi.org/10.1186/1471-2121-14-46), its Supplementary Table 1, and the [cited methods study](https://doi.org/10.1371/journal.pone.0070021).

The repaired draft covers the five deposited Tau RAW files. They represent cultured **Ostreococcus tauri**, CK1 R200C overexpression, corresponding to CK1tau-OX21. The previous canonical annotation incorrectly labels these algae as brain tissue; it also gives no applicable digestion enzyme. This draft corrects those fields, but the incomplete replacement is not promoted to the canonical directory.

Each deposited Mascot `.dat` header links to one of the five RAW basenames. All specify Mascot 2.4.0, trypsin, precursor 7 ppm, fragment 0.4 Da, fixed carbamidomethyl-C, variable oxidation-M, protein N-terminal acetylation and STY phosphorylation. The generated mzTab's no-fixed-modifications field is an export limitation explicitly noted in that file; the original search headers establish fixed carbamidomethylation. All RAW headers confirm LTQ Orbitrap XL, CID and 35 NCE. TiO2 enrichment is directly described in the project record.

The paper and Supplementary Table 1 describe five replicates per condition but do not distinguish independent cultures from repeat preparations/injections. Numeric Tau suffixes identify runs, not proven biological units. The draft leaves both biological and technical replicate fields unknown, so validation fails only those two mandatory fields. The parent CCA1-LUC condition appears in the published comparison, but its RAW files are absent from this deposit and no control rows are fabricated.

Needed for promotion: an author-level RAW-to-culture/preparation mapping clarifying those five replicates. The original canonical file remains a known unresolved issue; its brain label and inferred biological replication must not be treated as validated. The record-only digestion flag is resolved by the paper and all five original Mascot parameter headers.
