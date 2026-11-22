# BLOCKED: PXD045502 (SILAC part), draft only

**Dataset:** [PXD045502](https://www.ebi.ac.uk/pride/archive/projects/PXD045502), "Quantitative Proteomics Reveal the Role of Matrine in Lipid Metabolism"
**Publication:** Feng H. et al., ACS Omega 2024;9(23):24308-24320. PMID [38882153](https://europepmc.org/article/MED/38882153), [PMC11170650](https://europepmc.org/article/PMC/PMC11170650), doi:10.1021/acsomega.3c09983

`PXD045502-silac.sdrf.tsv` is a **partial draft**. It covers only the A549 SILAC
(matrine vs control) mixtures that the public evidence resolves. It passes
`parse_sdrf validate-sdrf` for `ms-proteomics`, `human` and `cell-lines` (v1.1.0). It
stays in `sandbox/` until the points below are settled.

## Why it is blocked

1. **Two of the four SILAC runs do not match the published design.** The paper says
   every A549 sample is a 1:1 light/heavy mixture, with the labels swapped in the
   second biological replicate. A spot check of the deposited spectra (MS1 peak-pair
   excess at +8.0142 Da (Lys8) and +10.0083 Da (Arg10), one ~15 MB region per file)
   gives these results:
   - `Ren_20220112_1991028_TPPpro_FHX_SILAC_PBS_heavy.mzXML` and
     `Ren_20220112_1992028_TPPpro_FHX_SILAC_Ku_heavy.mzXML` are clear 1:1 Lys8/Arg10
     mixtures. They are annotated in the draft.
   - `Ren_20220104_1945028_TPPpro_FHX_SILAC_PBS_light.mzXML` and
     `Ren_20220104_1948028_TPPpro_FHX_SILAC_ku_light.mzXML` show **no** heavy-partner
     excess (none for Lys4, Lys8 or Arg10). Neither the paper nor the deposit says
     what these runs are: unmixed light-only runs, a failed labelling or a label
     check. They are **not** annotated, so no channel map was invented for them.
2. **Only peak lists were deposited.** PRIDE holds `.mzXML` files only. The vendor
   `.raw` parents named in the mzXML headers are not in the archive.
   `comment[data file]` therefore points to the `.mzXML` files.
3. **Some channel-to-condition mapping is inferred.** The mapping uses file-name
   tokens: `PBS_heavy` means control heavy and matrine light (the paper's replicate
   1), and `Ku_heavy` means matrine heavy and control light (the swap). Reading `Ku`
   as matrine is an inference (the paper names the source plant "Kushen").
4. **Sources disagree on two values:**
   - Vehicle: the paper says DMSO and the file names say PBS. The draft writes `control`.
   - Instrument: PRIDE says Q Exactive HF, while the paper's LC-MS/MS section (written
     for TPP) and the `FHX` file token suggest Q Exactive HF-X. The draft uses HF-X.
5. **The heavy isotopes come from the spectra, not the text.** The paper only says
   "heavy amino acids". Lys8 (UNIMOD:259) and Arg10 (UNIMOD:267) were inferred from
   the spectra.

## What would unblock it

- The authors confirm the role of the two 2022-01-04 `*_light` runs, the vehicle
  (DMSO or PBS) and the heavy amino acids. Alternatively, the SILAC MaxQuant output
  (`evidence.txt` / `mqpar.xml`) would answer the same questions. It was not deposited:
  only the TPP and HepG2 search outputs are in PRIDE.

## Out of scope for this draft

The same PXD also holds HepG2 label-free runs (`pro_PBS_re1-3`, `pro_Matrine_re1-3`)
and A549 TMT10 thermal proteome profiling runs (`TPPDMSO_*` / `TPPMatrine_TMTF1-4_re1/re2`).
They are not annotated here.
