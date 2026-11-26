# PXD000612: HeLa-S3 phosphoproteome draft

This 273-row SDRF remains in sandbox. The actual physical digestion enzyme
sequence is unresolved: the primary paper names FASP and a tryptic search,
but the inspected main text and supplement do not establish the enzyme
reagents used in this study. `comment[cleavage agent details]` is therefore
`not available`. A generic FASP reference or search specificity does not
establish study-specific digestion reagents.

## Verified mapping and repairs

[PRIDE](https://www.ebi.ac.uk/pride/archive/projects/PXD000612), the
[paper](https://doi.org/10.1016/j.celrep.2014.07.036), its
[public manuscript](https://pure.mpg.de/rest/items/item_2060412_2/component/file_2062301/content),
and the [supplement](https://ars.els-cdn.com/content/image/1-s2.0-S2211124714006202-mmc1.pdf)
were checked. The deposited `combined.zip/experimentalDesignTemplate_FINAL.txt`
maps all 273 native RAW files: 126 phosphopeptide, 132 unenriched proteome
and 15 phosphotyrosine-enriched acquisitions. Its 42 additional names are
absent from the RAW inventory and are not added as invented acquisitions.

The exact author analysis indices are retained: SCX fractions 1-6, SCX
flow-through 8-10, SAX 12-17 and unfractionated pY index 19. These are
MaxQuant analysis indices, not physical fraction counts. Original RAW
fraction labels remain in a separate column. Author biological-replicate
codes are retained; the paper describes quadruplicate treated conditions
and six untreated controls. The pY subset is not silently assigned to the
same preparation as similarly numbered total-proteome samples.

The original `parameters.txt` establishes MaxQuant 1.5.0.0, 20 ppm FTMS
fragment tolerance, and matching between runs with 0.5/20 minute windows.
The previous 0.05 Da fragment tolerance is unsupported. A fixed main-search
precursor tolerance was not recovered; it is unavailable. The per-RAW
variable phosphorylation search scope for unenriched proteome files also
remains unavailable. HeLa-S3 origin metadata uses
[Cellosaurus CVCL_0058](https://www.cellosaurus.org/CVCL_0058), including
the reported age 30Y6M. Its disease and anatomical fields describe cell-line
origin; an untreated HeLa control is not a healthy-donor control.

## Local validation

Reviewed 2026-09-28 with sdrf-pipelines `701356bd5309`. Human and cell-lines
templates pass. The ms-proteomics template and repository review fail
because the required physical cleavage-agent value is unavailable.
Offline warnings for treatment descriptions and ontology terms remain.
The earlier file passed repository review, but that did not validate its
digestion or search parameters.

Deposit reconciliation reports five findings. Its cell-line/tissue and
control/disease rules do not distinguish cell-line origin from treatment;
the cell-lines template and Cellosaurus establish that distinction. Its
trypsin findings do not supply missing study-specific reagent evidence.
These findings are recorded, and the draft is not promoted. The existing
canonical SDRF is unchanged and is not certified by this review. Complete
native methods and spectra were not audited.
