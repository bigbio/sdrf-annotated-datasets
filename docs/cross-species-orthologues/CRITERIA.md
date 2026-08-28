# Cross-species orthologues-to-human metascreen criteria

## Goal
Shortlist PRIDE/ProteomeXchange shotgun proteomics datasets from non-human animals that help define **orthologous proteins to human** (deep coverage, clear organism identity, preferably multi-tissue or reference proteome context).

## Target organisms
- Monkey / NHP: *Macaca mulatta*, *Chlorocebus sabaeus*, *Cercopithecus aethiops*, other macaques/primates
- Horse: *Equus caballus*
- Dog: *Canis lupus familiaris* / *Canis familiaris*
- Cat: *Felis catus*
- Rabbit: *Oryctolagus cuniculus*
- Rat: *Rattus norvegicus*
- Chicken / Gallus: *Gallus gallus*
- Zebrafish: *Danio rerio*
- Cattle: *Bos taurus*
- Other vertebrates (include when atlas/reference depth is clear): pig (*Sus scrofa*), sheep (*Ovis aries*), goat (*Capra hircus*), guinea pig (*Cavia porcellus*), other fish/birds/mammals with recoverable multi-tissue or deep tissue proteomes
- Fruit fly / Drosophila: *Drosophila melanogaster* (and closely related *Drosophila* spp. when orthologue mapping to human is explicit)

Mouse (*Mus musculus*) is **not** a primary target (human orthologue resources are already abundant); include only when it is part of an explicit multi-species comparative design with other targets.

## Include when
- Organism is one of the targets (single-species or multi-species including human + target)
- Bottom-up / shotgun / DDA or DIA proteomics of tissues, organs, or whole organism
- Depth useful for orthologue mapping (prefer multi-tissue atlases, deep tissue proteomes, reference proteomes, cross-species comparative studies)
- Organism / organism-part metadata recoverable from PRIDE + publication
- Prefer studies where experimental factor is organism part, developmental stage, or species (not only drug/disease cell models)

## Exclude when
- Pure cell-line drug screens, IP/AP-MS interactomes, clinical biomarker panels with tiny protein lists
- Metaproteomics / microbiome / pathogen-only (unless host tissue deep proteome is the main product)
- Affinity-proteomics arrays (Olink/SomaScan) without MS shotgun depth
- Already fully annotated in `datasets/` for this campaign (note as `skip` with existing path)
- Organism mislabeled or mixed without recoverable mapping

## Extract columns
- species_group (monkey|horse|dog|cat|rabbit|rat|gallus|zebrafish|bos|pig|sheep|goat|other_vertebrate|drosophila)
- organism_taxname
- n_tissues_or_parts
- study_type (tissue_atlas|deep_tissue|comparative_multispecies|reference_proteome|other)
- includes_human (yes|no)
- estimated_files_or_samples
- publication
- orthologue_utility (high|medium|low)
- already_annotated (yes|no|partial)
