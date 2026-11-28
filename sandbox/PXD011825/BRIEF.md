# PXD011825 SDRF annotation report

## Study
Proteomic analysis of TMV and TMV 24A+UPD infected N. benthamiana plants by iTRAQ (NUS, Wong Sek Man lab). Paper: Macharia M, Das PP, Naqvi NI, Wong SM. Phytopathology Research 2020;2:1, doi:10.1186/s42483-019-0043-5 (open access; no PMCID used).

## Scope, evidence and decisions
Status: **sandbox**. 40 rows = 5 WIFF runs x 8 iTRAQ channels; one assay name per WIFF shared by its 8 channel rows.

- **Deposited vs annotated:** the PROXI record lists 18 files: 5 `.wiff`, 5 `.wiff.scan`, 5 `.mzML` (`180502_Mecury_RPRP_8plex_F1..F5_5ul`), and 3 ProteinPilot outputs (`...combine search.group`, `.group.xml`, `__FDR.xlsx`). The campaign cache said "10 RAW". That counted wiff plus wiff.scan; there are 5 acquisitions. All 5 are annotated. The `.wiff.scan`/`.mzML` files are companions and are not separate rows.
- **Channel map (STATED, paper Fig. 1b, read from the figure image).** It is a single 8-plex. Group 1: TMV 2 dpi = 113, TMV 3 dpi = 117, TMV 24A+UPD 2 dpi = 119, TMV 24A+UPD 3 dpi = 116. Group 2: TMV 2 dpi = 115, TMV 3 dpi = 121, TMV 24A+UPD 2 dpi = 118, TMV 24A+UPD 3 dpi = 114. Each channel pools 2 plants ("four biological replicates ... grouped into two"). The iTRAQ group (1/2) is used as the biological replicate. There is no mock channel.
- **Fractions:** high-pH RP-HPLC (20 mM ammonium formate pH 10, C18), pooled into 5 fractions. F1-F5 in the file names give the fraction identifiers 1-5.
- **Sample prep (stated):** 4-week-old plants, 16 h/8 h at 25 C, TMV U1, mechanical RNA inoculation. Protein comes from inoculated and newly emerged leaves. TCEP / MMTS, in-gel trypsin, iTRAQ 8PLEX (SCIEX).
- **Instrument:** TripleTOF 5600 (PX record and paper agree). Precursor range 400-1800 m/z, used as the MS1 scan range.
- **Search:** ProteinPilot against a Nicotiana database. Mods are annotated as Methylthio C (from MMTS) and iTRAQ8plex K / N-term, all fixed. This is INFERRED from the chemistry and the ProteinPilot convention. The deposited `.group` could not be read: the PRIDE FTP returned an upstream timeout today.
- **Not annotated:** the PX record's methylthiolated / acetylated / monohydroxylated residues. These look like ProteinPilot "biological modification" ID-focus findings, not search parameters.

## Values left not available / INFERRED
- Precursor and fragment mass tolerance: not available. ProteinPilot does not use user tolerances, and the paper does not state any.
- Dissociation: CID (MS:1000133). This is INFERRED from the TripleTOF 5600 convention and is not stated.
- Strain: not available.
- Disease: free text "tobacco mosaic virus infection". No ontology term was verified, because live OLS was unreachable (WebFetch quota, shell offline).
- Accessions were reused from validated campaign files and not re-checked live: UNIMOD:39, UNIMOD:730, PRIDE:0000564/0000605/0000609, MS:1000932/1000133.

## Conflicts / why sandbox
- The paper does not cite PXD011825; its data-availability statement says "Not applicable". The dataset-to-paper link is INFERRED from several matches: same submitter (Macharia) and lab head (Wong, NUS), same viruses and title topic, a single iTRAQ 8-plex with 5 fractions, the same instrument, and 2018 file dates.
- The Fig. 1 legend says "two iTRAQ 8-plex experiments", but the Methods and the deposited files show one 8-plex holding two 4-channel groups.
- The mods were not read from the deposited search file.

## Validation
`parse_sdrf validate-sdrf --use_ols_cache_only --template plants`: clean (structural only; OLS deps not installed). `sdrf_review.py`: [OK].

## Review status
pending
