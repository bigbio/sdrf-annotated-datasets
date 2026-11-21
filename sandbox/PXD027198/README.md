# PXD027198 — Personalised phosphoproteomics (human skeletal muscle, exercise × insulin)

BLOCKED: not a SILAC dataset, and subject-level metadata (health status, age, sex) cannot be
resolved from public evidence. Kept in `sandbox/` until a curator with access to the paper's
Methods fills these in.

- Dataset: <https://www.ebi.ac.uk/pride/archive/projects/PXD027198>
- Publication: Needham EJ *et al.* Personalized phosphoproteomics identifies functional
  signaling. *Nat Biotechnol* (2021, online). PMID 34857927, doi:10.1038/s41587-021-01099-9
  (not open access).

## Why BLOCKED

1. **No SILAC label in the deposit.** PRIDE lists SILAC (PRIDE:0000315) among the
   quantification methods, but the deposited MaxQuant 1.6.2.2 `mqpar.xml` (discovery search)
   has `multiplicity=1`, empty `labelMods` and no isobaric labels. The validation Spectronaut
   Phospho(STY) table has one intensity column per sample. Both cohorts are label-free, so
   every row is `label free sample`.
2. **Demographics and disease are unverified.** The paper's Methods are paywalled, and no
   per-subject age or sex is deposited. PRIDE's project-level disease (DOID type 2 diabetes
   mellitus) is not supported by the abstract (exercise-potentiated insulin action in human
   muscle), so `characteristics[disease]`, `[age]` and `[sex]` are `not available`.
3. **Validation-cohort search settings are not deposited.** Tolerances are omitted and
   non-phospho modifications are `not available`. The digest enzyme (Trypsin/P) is carried
   over from the discovery MaxQuant search.
4. **Discovery runs `_F1`–`_F6` are not in the deposited sample key.** Their sample identity
   is `not available`.

## Files

| file | runs | acquisition | templates |
|---|---|---|---|
| `PXD027198-discovery.sdrf.tsv` | 26 (20 biopsies + F1–F6) | DDA Top15, Q Exactive HF-X | ms-proteomics 1.1.0, human 1.1.0 |
| `PXD027198-validation.sdrf.tsv` | 40 biopsies | DIA (nominal 14 m/z isolation, 1 m/z overlap, optimised placement, 350–1022 m/z), Orbitrap Exploris 480 | ms-proteomics 1.1.0, human 1.1.0, dia-acquisition 1.1.0 |

Sample → file mapping comes from the deposited `Needham_PersonalisedPhospho_sample_key.xlsx`:
5 discovery subjects and 10 validation subjects, each with 4 biopsies (exercise or rest × ground state or
insulin, as labelled in the key). The two factors are `factor value[exercise]` and
`factor value[insulin stimulation]`. Acquisition settings were read from the instrument
methods embedded in the raw files.

## To unblock

Fill in from the Methods / Supplementary Table of the paper: subject health status (disease or
`normal`), sex, age, the biopsied muscle, the digest enzymes, and the Spectronaut search
settings. Also document what `_F1`–`_F6` are. Then re-validate and promote to `datasets/`.
