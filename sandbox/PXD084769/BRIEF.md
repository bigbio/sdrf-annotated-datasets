# PXD084769: RAW-confirmed DDA and 36 author sample codes; treatment map incomplete

Checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD084769), all **51 RAW headers**, the deposited injection sequence, both Skyline documents and both peptide-area exports. The [associated preprint](https://doi.org/10.64898/2026.09.08.749914) was identified through the bioRxiv API, but its full text returned rate-limit errors and was not used as inspected design evidence.

## Acquisition and analysis corrections

Every RAW identifies Q Exactive HF, **Top10 DDA**, HCD at 27 NCE and 250–1600 m/z MS1. The injection sequence independently names the DDA method. This conflicts with the PRM wording in the project protocol. The actual Skyline documents identify **20.1.0.76**, whereas the archive description gives 4.2.0.19072. Both documents link to all 51 deposited RAWs, and the draft uses their actual software version.

Physical preparation reports liver histone extraction, in-gel acylation and trypsin digestion. Skyline's ArgC specificity is a configured analysis rule, not evidence of physical Arg-C digestion. Lysine acetylation, di-/trimethylation, propionylation, author-defined `Monomethyl_Prop(K)` (C4H6O) and M oxidation are retained from the document settings. No invented Unimod accession is assigned to the custom term. The documents also contain heavy-modification definitions, but the actual precursors and exported isotope-label fields are light; those template definitions do not establish extra isotope-labelled samples.

## Sample and coverage limits

The injection sequence directly links **36 complete author codes** to 36 numbered RAWs. The literal C/H/I/E suffixes are preserved. They are not translated into CNT/HFD/INT conditions without a crosswalk, particularly because four suffixes appear while the archive describes three experimental groups. The complete composite code is retained: two entries share the `675I` suffix, so stripping the leading number would lose distinctions whose meaning is unproven.

The remaining **12 QC and 3 blank acquisitions** are explicitly excluded from this liver-sample subset. Their repeated injection positions do not establish pool composition or equivalence to a study animal. Ages, sex, individual-animal identifiers, biological replicates, disease and treatment remain unavailable. Cell type is unavailable because whole liver tissue is not proof of purified hepatocytes. Keep the 36-row subset in `sandbox/` until animal/condition mapping and QC composition are supplied.

## Local validation

The ms-proteomics and vertebrates templates, and consequently repository review, fail only because biological replicate is unavailable. The required developmental-stage column is present with an unavailable value. Deposit-record reconciliation passes, but does not detect or resolve all differences between archive prose and actual RAW/Skyline metadata. No numeric replicate IDs or treatment translations were invented to obtain a validator pass. Offline ontology warnings remain in the stored logs.
