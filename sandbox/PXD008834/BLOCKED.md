# PXD008834 annotation blocked

PXD008834 is "Proteomic analysis of *Candida albicans* dnm1 mutant" from the Seneviratne lab at NUS. The linked paper is Truong T et al., Proteomics 2020;20(1):e1900240 (doi 10.1002/pmic.201900240, PMID 31811746). It is not in PMC.

The study compares the haploid dnm1Δ mutant with its parent strain, GZY803, using iTRAQ 8-plex:
- One 8-plex set, split into 10 RP-RP fractions (`171030_Thyuen_8plex_RPRP_F1..F10`).
- Searched in ProteinPilot (`..._10fractions_combine.group`).
- Run on a TripleTOF 5600.

## Why blocked

The iTRAQ channel → sample map is not available.

- **PX record:** it names only the two strains ("haploid dnm1 mutant and the wild type GZY803"). It says nothing about channels or replicate counts.
- **Paper:** the full text (Wiley) is paywalled and sits behind a Cloudflare human-verification check, which I did not attempt. There is no PMC or Europe PMC full text, and the abstract has no channel layout. Even if the 8 channels are 4 dnm1Δ + 4 GZY803, as in the sister study PXD004274, the reporter assignment cannot be guessed.
- **Deposited files:** the only other candidate source is the ProteinPilot `.group` / `.group.xml`, which may hold the sample names per reporter. The PRIDE FTP over HTTPS returned an upstream connection timeout today, so neither file could be read.

## Deposited files (PROXI `resultType=full`, re-derived; list in scratch)

There are 30 files:
- 10 `*_F<n>_10ul-Thyuen_8plex_RPRP_F<n>.mzML` (F1-F10)
- 9 `*_F<n>_10ul.wiff` and 9 `*.wiff.scan` (F2-F10)
- `.group` and `.group.xml`

The campaign cache ("10 RAW / 30 files") matches. The vendor `.wiff` files are deposited, but F1 has no `.wiff`/`.wiff.scan`; only its mzML exists. A future SDRF should use the `.wiff` files for F2-F10 and the mzML for F1, or mzML throughout. Verify this against the FTP listing first.

## Evidence checked
- ProteomeCentral PROXI record. It lists the files above, TripleTOF 5600 (MS:1000932), and modifications MOD:01549 iTRAQ8plex, MOD:00394 acetyl and MOD:00397 iodoacetamide.
- PubMed 31811746: abstract and DOI only.
- Wiley full text: Cloudflare check, not passed.
- Europe PMC REST: upstream connect error.
- PRIDE FTP over HTTPS: timeout.
- Web search: no open full text found.
- Precedent PXD004274 (same lab): there the map came from Fig. 1A of an open-access PMC paper. That route does not exist here.

Scratch: `/home/claude/singapore3/scratch/PXD008834/px_files.txt`.

## To unblock
Any one of these would do:
1. The paper's Methods or figure with the iTRAQ reporter → strain/replicate layout (needs institutional Wiley access).
2. Read the `.group.xml` / `.group` from the PRIDE FTP once it is reachable. Check whether its sample/reporter names identify dnm1Δ vs GZY803 per channel.
3. Get the layout from the authors.

With the map, the SDRF would be 10 fractions × 8 channels = 80 rows. It would use `ms-proteomics` + strain (dnm1Δ in the GZY803 background vs GZY803), trypsin, iTRAQ8plex (UNIMOD:730), and a cysteine alkylation to be confirmed (the PX record says iodoacetamide; the sister study used MMTS).
