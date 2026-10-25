# PXD001562 — custom modification unresolved

The 5-row replacement draft was checked on 2026-09-28 against [PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD001562), all five RAW method headers, the deposited mzTab, and the [paper](https://doi.org/10.1074/mcp.M114.046896) ([author-institution full text](https://backoffice.biblio.ugent.be/download/5985175/5985191)). The canonical file has not been replaced.

## Supported repairs

- File names identify two untreated and three H2O2-treated samples. The paper explicitly describes two independent untreated experiments and three independent treated experiments. All five culture samples receive distinct biological identifiers; no cross-condition pairing is inferred from acquisition numbers.
- PSB-D suspension cells were dark-grown and collected in mid-log phase. Their 3-day culture age is recorded separately from plant developmental stage. All conditions used DYn-2; the H2O2 contrast was 0 versus 10 mM for 30 minutes.
- Every RAW confirms Q Exactive, HCD 25 NCE and 400–2000 m/z. Digestion is in-gel trypsin; the search permits cleavage before proline. Fragment tolerance 20 mmu is normalized to 0.02 Da. Correct DTT and oxidation-related Unimod identifiers replace formatting errors. No alkylating reagent is inferred.

## Remaining hard limitation

PRIDE explicitly states that the DYn-2 / DYn-2-biotin-azide modifications were represented using unrelated MOD:00067 / MOD:00444 placeholders. The mzTab therefore cannot provide a trustworthy name, accession or mass for this custom adduct. The paper names DYn-2-cycloaddition on cysteine but does not provide its exact delta mass. The draft retains the six supported modification entries plus `not available` for the unresolved seventh entry and documents it in `comment[unresolved modification]`. No placeholder accession or mass from an unrelated DYn-2 experiment is substituted.

Both declared templates and the review gate pass, with ontology warnings for plant cell, study sample, untreated and DDA ancestry. Record reconciliation passes. This is still a **sandbox draft** until the custom search-modification definition is recovered; a parser pass does not establish complete search parameters.
