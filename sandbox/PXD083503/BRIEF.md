# PXD083503: physical digestion protocol unreported

The one-row draft was checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD083503), the actual Thermo RAW header, deposited mzIdentML and the read-only contents of `pl20095.sf3`.

## Supported annotations

The archive contains one `.raw` acquisition, one derived MGF, one mzIdentML and one Scaffold project. Although the archive protocol calls `.sf3` a raw file, it is a Scaffold SQLite result container and is not treated as another acquisition.

The RAW identifies **Q Exactive HF**, DDA, HCD at 27 NCE and 400–2000 m/z MS1 scans; PRIDE's instrument selector says generic Q Exactive. The mzIdentML and Scaffold metadata link the acquisition to sample `IA_1` and Mascot source `F012700.dat`, with Mascot 2.5.1 and Scaffold 5.3.4. The search used trypsin specificity, one missed cleavage, 5 ppm precursor/0.01 Da fragment tolerances, fixed carbamidomethylation and variable methionine oxidation/asparagine-glutamine deamidation.

PRIDE supports a six-hour starvation/secretion period and filtered culture supernatant. Biological identifier 1 denotes the single observed secretome preparation; it does not establish one cell, clone, flask or donor, nor exclude pooling. One deposited acquisition receives technical identifier 1. Culture strain and pooling relationships are not supplied.

## Remaining limitation

The public sample protocol does not report the actual digestion, reduction or alkylation steps. The mzIdentML search-enzyme setting and Scaffold's search configuration do not establish physical use of trypsin. Consequently `comment[cleavage agent details]` remains `not available`; no reduction or alkylation reagent is inferred from search modifications.

The template and review gate fail on the missing physical cleavage agent. Record reconciliation also flags that unresolved value. Keep this draft in `sandbox/` until a physical preparation protocol is available.
