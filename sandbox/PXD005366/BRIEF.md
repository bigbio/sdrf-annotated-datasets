# PXD005366 — repaired drafts, preparation relationships incomplete

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD005366), deposited `sdrf-Hela.tsv` / `sdrf-Rattus.tsv`, all 76 RAW headers, `txt_EGF_Control.zip` parameters and summary, the [original paper](https://doi.org/10.1021/acs.jproteome.6b00753) ([author-institution copy](https://dspace.library.uu.nl/bitstream/handle/1874/359699/acs.jproteome.6b00753.pdf?isAllowed=y&sequence=4)), and [HeLa Cellosaurus](https://www.cellosaurus.org/CVCL_0030).

## Scope and supported corrections

The two replacement drafts cover 48 HeLa and 28 rat RAW files exactly once. They supersede the duplicate 76-row combined sandbox draft. The three existing canonical files remain unchanged and are not endorsed by this audit; the generic canonical file duplicates the HeLa file's RAW coverage.

- **All 76 RAWs:** Q Exactive Plus, HCD 25 NCE, MS1 375–1600 m/z. The 200–2000 range elsewhere in the method belongs to MS2. PRIDE's Q Exactive dropdown is incomplete. Both physical digestion enzymes, trypsin and Lys-C, are explicitly described.
- **HeLa:** 12 enrichment-method comparisons (four per method) and 36 input-titration runs. Enrichment amounts come from deposited RAW names, supported by their internal acquisition names and the study's design. The three `HeLa_10ug_*` files are 10 ug, correcting the archived SDRF's 100 ug; original values and RAW names remain in separate provenance columns. Cellosaurus supports female, 30Y6M and cervical cancer origin; the archived 31Y is corrected. No independent HeLa cultures are inferred from repeated enrichment numbers.
- **Rat titration:** 20 runs from the paper's pooled neuronal protein extract. Biological identifier 1 represents that extract, not one rat. Each amount has four archived runs, although the paper describes triplicate analyses; all deposited runs are retained and no specific exclusion is invented. Pool composition and animal count are unreported.
- **EGF/Control:** six primary wells (three per condition) are described in the paper. The deposited SDRF assigns `Control_1p2` / `Control_2p2` to the respective biological groups, but their exact preparation or repeat-injection role is unresolved. Their technical replicate remains unknown. No cross-condition animal pairing is inferred.

## Search settings and remaining gaps

The six ordinary EGF/Control RAW basenames match six rows in the deposited MaxQuant summary using the full internal names in the RAW headers. That result set records **MaxQuant 1.5.3.28**, Trypsin/P and fragment tolerance **20 ppm**, while the paper reports 1.5.3.30. Those actual settings are assigned only to the six linked files. The two `p2` runs are absent from that summary. Actual versions and fragment tolerances for the other 70 runs remain unknown; reported software version is retained separately. Precursor tolerance is unreported. The documented carbamidomethyl-C, oxidation-M, protein N-terminal acetyl and STY phosphorylation settings are retained.

Needed before promotion: the HeLa culture/digest preparation map, and clarification of the two `p2` acquisitions plus the four-versus-three neuronal titration runs. The HeLa draft intentionally leaves biological replication unknown; the rat draft leaves two technical replicate values unknown. These are validation blockers, not values to fill from filename counters. Metadata repairs and full RAW coverage alone do not establish independent biological replication.

Validation was run for every declared template and the repository review gate: HeLa fails only missing biological replicate; rat fails only missing technical replicate. Visible ontology warnings concern cervix, study sample, no-EGF treatment, DMEM and DDA ancestry. No warning suppression is applied.
