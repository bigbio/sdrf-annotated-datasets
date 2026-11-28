# PXD022193 SDRF annotation report

## Study
Analysis of the neuro-proteome associated with cell therapy in a mouse model of Parkinson's disease (Lebanese University, Beirut; lab head K. Zibara). Paper: "Analysis of the Neuroproteome Associated With Cell Therapy After Intranigral Grafting in a Mouse Model of Parkinson Disease", Front Neurosci 2021, doi:10.3389/fnins.2021.621121, PMC7991918. Its Data Availability statement cites PXD022193, so the link is verified. The PX record still says "publication pending".

## Scope, evidence and decisions
- **Status: sandbox.** Label-free DDA. There are 45 rows, one per deposited RAW, with 37 columns. Templates: ms-proteomics + vertebrates (sample-metadata via extends).
- **Deposited vs annotated:** PROXI lists 45 `.raw` files plus `proteinGroups.txt`. All 45 RAW files are annotated (5 regions x 3 groups x 3 mice); none are excluded. The file list is in the scratch file `files.txt`.
- **Design (stated, paper Methods):** 9 adult C57BL/6 mice (4-6 months) received a 6-OHDA lesion in the left SNpc. One week later, 3 groups (n=3) followed:
  - LSNTD1: E12.5 TH-EGFP ventral mesencephalon graft, killed after 1 day.
  - LSNTD7: same graft, killed after 7 days.
  - SHAM: vehicle-only graft, killed after 7 days.
  
  Five regions were punched: caudate putamen, nucleus accumbens, medial forebrain bundle, thalamus and ventral mesencephalon.
- **File -> sample mapping:**
  - Region prefixes CPU/NaCC|NACC/MFB/ThAL/Vm map to caudate-putamen / nucleus accumbens / medial forebrain bundle / thalamus / midbrain.
  - `D1` -> LSNTD1, `D7` -> LSNTD7, and `m1-m3` -> mouse 1-3 (`MFB D7M3` has an upper-case M and is treated as m3).
  - **Files without a D-code -> SHAM is INFERRED by elimination.** This is the main reason for sandbox status.
  - That `mN` is the same animal across the five regions is also INFERRED. Source names are `<group>_mouse<N>_<region>`, and biological replicate = N within the group.
- **Organism part:** "ventral mesencephalon" has no UBERON term, so `midbrain` (UBERON:0001891) is used, not `midbrain tegmentum`, because the 2 mm ventral punch includes SN/VTA. "thalamus" is an exact synonym of UBERON:0001897. The other region terms were checked on Ontobee: caudate-putamen UBERON:0005383, nucleus accumbens UBERON:0001882, medial forebrain bundle UBERON:0001910. OLS4 was down for this run (upstream connect error), so labels were checked on Ontobee only. The validator's ontology check is not active in this environment (its OLS dependencies are not installed), so the pass is structural only.
- **Disease:** "Parkinson disease" is used for the 6-OHDA toxin model, so it is a disease model, not a natural disease. The treatment column is "E12.5 ventral mesencephalon graft" or "vehicle sham graft". All animals carry the 6-OHDA lesion; that SHAM mice were lesioned too is INFERRED from n=9 lesioned = 3x3. Sampling time is 1 day / 7 day after grafting.
- **MS (paper):** LTQ Orbitrap Velos (matches PX; the RAW header was not read). DDA top-10 with CID at 35% NCE. MS1 range m/z 400-2000.
- **Search (paper; MaxQuant 1.6.3.4 – mqpar not deposited):**
  - Trypsin, up to 2 missed cleavages.
  - Carbamidomethyl C fixed; Oxidation M and protein N-term Acetyl variable.
  - Precursor tolerance 4.5 ppm (main search; the paper prints "pm"); fragment tolerance 0.5 Da.
  - DTT/IAA for reduction and alkylation.
- **Conflict:** the PX record says "No PTMs"; the paper's search mods are used instead.

## Values not available / not applicable
- sex: not available (the paper does not report it).
- Donor age is not encoded, because no age column is used. Developmental stage = adult (4-6 months, stated).

## Review status
pending
