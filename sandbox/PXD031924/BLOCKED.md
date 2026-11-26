BLOCKED: the SILAC channel -> condition map of the secretome runs cannot be resolved from public evidence.

Dataset: PXD031924, "Equine muscle-derived mesenchymal stem cells protect cartilage explants in
osteoarthritis model: secretome characterization" (Equus caballus; in vitro osteoarthritis model).
Publication: Dechêne L et al., Stem Cell Rev Rep 2023;19(2):550-567, doi:10.1007/s12015-022-10463-4,
PMID 36271312, PMC9902419.

## What the record does establish

- Design (paper Fig. 5A): mdMSC supernatants from six conditions, drawn with A-C heavy and D-F
  medium (heavy = Arg10/Lys8, medium = Arg6/Lys4; supplementary Table 2), mixed 1:1 into
  seven pairs: 1 = A-D, 2 = A-E, 3 = B-D, 4 = B-E, 5 = C-E, 6 = C-F, 7 = F-B.
  A = mdMSC + TNFa/IL-1b; B = mdMSC + cartilage; C = cartilage + TNFa/IL-1b;
  D = mdMSC; E = mdMSC + cartilage + TNFa/IL-1b; F = cartilage. The cartilage explants are
  not pre-labelled (light in Fig. 5A). During the 24 h exposure they can incorporate labelled amino
  acids, and the paper reports labelled cartilage-derived proteins (supplementary Table 5).
- A label swap: "the same experiments were performed with mdMSCs at passages 4 and 5 but with
  swapped labelling", for 3 mdMSC donors (Methods; supplementary Table 3). The footnote of Table 3
  counts passages in labelling medium: forward "after 2 passages", reverse "after 3 passages".
- Two injections per sample (Methods), on a timsTOF Pro (PASEF, DDA). Search: PEAKS Studio X Pro,
  trypsin, Carbamidomethyl (C) fixed; Oxidation (M), Label:2H(4) (K), Label:13C(6) (R),
  Label:13C(6)15N(2) (K), Label:13C(6)15N(4) (R) variable. The deposited mzid files also search
  N-terminal acetylation (+42.0106; EXP1 and Incorpo) and oxidation of P/K (EXP2).
- 96 RAW `.d.zip` files. Their names and the three deposited mzIdentML files split them as follows:
  - `peptidesexp1b_1_1_0.mzid.gz` (PEAKS project "Supernatant EXP1"): groups `<none>`, `H`, `N`,
    digits 1-7 (presumably mixes 1-7, unverified) x 2 injections = 42 runs (`URBC-LD-200717-65min-{,H,N}{1..7}_*.d.zip`).
  - `peptidesexp2_1_1_0.mzid.gz` ("Supernatant EXP2"): groups `F`, `HH`, `NN`, digits 1-7 x 2
    injections (+ one third injection of F5) = 43 runs.
  - `peptidesIncorpo_1_1_0.mzid.gz` ("Cells", label incorporation check): 11 `totaux` cell-lysate
    runs (`totaux-8`, `-H8`, `-N8`, `-F8`, `-HH8`, `NN8-totaux`). Methods describes the
    incorporation lysates as TNFa/IL-1b-treated vs untreated cells, but no source maps a lysate
    condition to a channel or file.

## What is missing

The file names never say which group is the forward experiment (A-C heavy) and which is the reverse
one (A-C medium), and no source pairs the six groups with the three donors. Without that, the label
of conditions A-F in every secretome run is a coin toss per group. A wrong guess swaps every channel
of 14 runs (15 for `F`).

Sources checked:

1. Paper full text (PMC9902419) and both ESM files (MOESM1: Tables 1-5 incl. donor list and
   incorporation per donor x forward/reverse; MOESM2: blots and heatmap). Neither names files or
   groups.
2. PRIDE project and file list (v3 API): no sample sheet; the sample processing protocol repeats
   the Methods.
3. The deposited mzIdentML `Inputs` sections: they give only the EXP1/EXP2/Incorpo grouping above.
4. Data Availability statement: it cites only PXD031924 ("Data and analyzed are available from the
   corresponding author on reasonable request"). The paper lists exactly two ESM files
   (MOESM1/MOESM2, item 1). The Europe PMC `supplementaryFiles` endpoint returned a server error
   (`Connection refused`) on 2026-11-22. The article's JATS XML (NCBI efetch) lists only MOESM1 and
   MOESM2 as supplementary material.
5. Data-driven cross-check (not used to annotate). This assumes the digit in a file name is the
   Fig. 5A mix number (5 = C-E, 7 = F-B). Nothing public confirms that, and Fig. 5B lists the pairs
   in a different order (A/D, B/D, E/A, E/B, B/F, C/F, E/C). In mixes 5 and 7 only one channel holds
   mdMSCs (C and F are cartilage only). If that channel dominates the labelled PSMs, forward
   (A-C heavy) predicts mix 5 medium-rich and mix 7 heavy-rich; reverse predicts the opposite.
   Observed (rank-1 passing PSMs, heavy/medium): the unprefixed EXP1 group and EXP2 `F` and `HH`
   match the reverse pattern (e.g. F5 327/160, F7 168/365). No group matches the forward pattern.
   EXP1 `N` is heavy-rich in both mixes, `NN7` is about even (227/242, 262/230), and EXP1 `H` is too
   sparse in mixes 5/7 (at most 6 per channel). A design with a label swap cannot be all-reverse, so
   the proxy is internally inconsistent. Read in the Fig. 5B order instead (5 = B/F, 7 = E/C), the
   same counts would match the forward pattern for those three groups. The check cannot settle the
   direction either way.
6. Indirect hint: in Table 3, donor 2 forward has a single replicate, and only `totaux-H8` has a
   single run. That would make EXP1 the forward experiment, assuming `totaux-H8` belongs to the
   EXP1 `H` group and all EXP1 groups share one label direction. This contradicts item 5, which makes
   EXP1's unprefixed group look reverse. Neither is a map.
7. Other discrepancies: Methods say "mdMSCs challenged with pro-inflammatory cytokines were
   collected at passage 4 with the medium labelling and at passage 5 with the heavy labelling" (the
   swap is tied to passage, not to a file group). The deposited EXP1 and Incorpo searches allow 2
   missed cleavages, while the paper says 1 (EXP2 uses 1). Their precursor tolerance is 20 ppm,
   while the paper says 15 ppm (EXP2 uses 15 ppm).

## Unblock

An author statement or a sample sheet naming, for each file group (`<none>`, `H`, `N`, `F`, `HH`,
`NN`), its donor, whether A-C were heavy or medium, and which mix each file digit is, plus what the `totaux` lysates contain. With
that, the build is mechanical: 85 secretome runs (42 + 43, incl. the third F5 injection) x 2 channels (templates ms-proteomics v1.1.0 +
vertebrates v1.1.0; organism Equus caballus; cell type mesenchymal stem cell of skeletal muscle
origin only for conditions with mdMSCs (A, B, D, E); C and F are cartilage explant only; disease osteoarthritis model).

No SDRF is provided here.
