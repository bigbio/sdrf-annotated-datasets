# PXD042852 annotation blocked

PXD042852 (QMDiab, Weill Cornell Medicine-Qatar, Doha) is "Nanoparticle enrichment mass-spectrometry proteomics identifies protein-altering variants for precise pQTL mapping", Suhre et al., Nat Commun 2024, doi:10.1038/s41467-024-45233-y, PMC10837160. The paper's Data Availability section cites PXD042852. The study used citrate plasma from 345 QMDiab participants. Each sample was enriched with five Seer Proteograph nanoparticles, then run on a timsTOF Pro 2 with dia-PASEF (22 min gradient) and searched with DIA-NN 1.8.1 (library-free, Trypsin/Lys-C, `--cut K*,R*`, `--unimod4`, `--met-excision`, 10/10 mass accuracy).

The deposit holds about 2,000 Bruker `.d.zip` runs. This count is an estimate from the PROXI payload size, about 395,900 characters at about 196 per entry. It is consistent with 345 samples x 5 NPs plus controls, but it was not enumerated. Run names follow the pattern `EXP22038_2022ms0<292-314><a|b>X<1-96>_<A|B>_<R|G|B><well>_1_<n>.d.zip`, which encodes plate, plate half, well and acquisition number. Neither the participant nor the nanoparticle can be read from the name.

There is no run -> sample key, and no run -> nanoparticle key:
- **PROXI record:** it lists only raw files, the DIA-NN outputs (`*_report.pg_matrix.tsv`, `*_report.stats.tsv`, `plus_variant_report.tsv`, `minus_variant_seer_swath_convert_PEP.txt`), a `.speclib` and a FASTA. There is no sample sheet or SDRF. Its publication field says "pending".
- **Paper (PMC10837160):** Supplementary Data 1-4 cover NP correlations, variant peptides, PAV/pQTL results and non-genetic associations. None is described as a file -> sample or file -> NP table. Genetic and participant-level data are access-controlled (IRB, WCM-Q), so a public participant map is not expected.
- **Not read (infrastructure down today):** the PRIDE FTP directory listing (upstream connect error), the PRIDE v3 API (connect error) and the Europe PMC REST search and supplementary files (rate-limited / connect error). The 308 MB Source Data zip was not opened.

Writing ~2,000 rows needs, at minimum, the NP identity for each run, and ideally the sample and plate for each run. Guessing NP identity from the R/G/B plate prefix or from well position would be fabrication. That is why no SDRF is emitted.

**Evidence checked:** PROXI `PXD042852?resultType=full/compact` (Page URL verified; head and tail read, middle not paged); PMC10837160 full text (Methods, Data Availability, Supplementary list).

**To unblock:**
1. Re-read the PRIDE FTP folder for any metadata or design file, and the DIA-NN `*.stats.tsv` headers (File.Name only, so probably no map).
2. Open the Nat Commun Source Data zip and Supplementary Information for a run/NP/plate manifest.
3. Otherwise, ask the authors (lab head Karsten Suhre) for the run -> NP -> de-identified sample key.

If a run -> NP key alone turns up, a de-identified sandbox SDRF becomes possible: source = de-identified sample ID or plate well, organism Homo sapiens, organism part blood plasma, NP as a fractionation/enrichment comment, timsTOF Pro 2, dia-PASEF.
