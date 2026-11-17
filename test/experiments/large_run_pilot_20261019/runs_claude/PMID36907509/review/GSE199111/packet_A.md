# Review packet A (facts only): GSE199111

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC10033748.paper.md`

## Paper outline

- # microRNA-501 controls myogenin^+/CD74^+ myogenic progenitor cells during muscle regeneration
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Material and Methods  `S2` · methods
- ### Human biopsy acquisition  `S2.1` · methods
- ### Mice  `S2.2` · methods
- ### Generation of miR-501 knockout mouse models  `S2.3` · methods
- ### Blood Parameters  `S2.4` · methods
- ### Eccentric Exercise  `S2.5` · methods
- ### Grip Strength measurement  `S2.6` · methods
- ### Evans Blue Dye  `S2.7` · methods
- ### Cell preparation and FACS  `S2.8` · methods
- ### Cell culture  `S2.9` · methods
- ### RNA extraction, cDNA synthesis, quantitative RT-PCR  `S2.10` · methods
- ### LDH Activity  `S2.11` · methods
- ### Proliferation assay  `S2.12` · methods
- ### Fusion Index and fiber diameter  `S2.13` · methods
- ### Protein extraction and western blot  `S2.14` · methods
- ### Histology  `S2.15` · methods
- ### Sarcomere analysis  `S2.16` · methods
- ### Single cell RNA-sequencing  `S2.17` · methods
- ### RNA-seq  `S2.18` · methods
- ### Statistical analysis  `S2.19` · methods
- ## Results  `S3` · results
- ### Deletion of miR-501 reveals unique myogenic progenitor cells enriched for macrophage markers  `S3.1` · results
- ### miR-501 determines myofiber size in adult skeletal muscle  `S3.2` · results
- ### miR-501 is necessary for neofiber formation and resilience in the adult skeletal muscle  `S3.3` · results
- ### miR-501 controls sarcomeric gene expression in muscle cells from mice and humans  `S3.4` · results
- ### MP^CD74 is upregulated in aged skeletal muscle where miR-501 is downregulated  `S3.5` · results
- ## Discussion  `S4` · discussion
- ## Conclusions  `S5` · conclusion
- ## Author contributions  `S6` · other
- ## Acknowledgements  `S8` · other
- ## CONFLICT OF INTEREST  `S9` · other
- ## Supplementary data  `S10` · supplementary
- ## Data availability  `S11` · data_availability
- ## Accession mentions

## Metadata (10 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.genotype`: wild type: 5; miR-501 -/-: 5
- `genotype`: WT: 5; KO: 5

### Constant columns

- `status`: Public on Mar 16 2023
- `submission_date`: Mar 22 2022
- `last_update_date`: Mar 16 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Tibialis anterior
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: C57BL/6
- `characteristics_ch1.2.Sex`: male
- `characteristics_ch1.3.age`: 12 weeks
- `characteristics_ch1.4.treatment`: cardiotoxin-induced muscle regeneration
- `characteristics_ch1.5.time point`: day 6
- `characteristics_ch1.6.tissue`: Tibialis anterior
- `treatment_protocol_ch1`: Intramuscular injection of Cardiotoxin into Tibialis Anterior, RNA extraction at day 6 of regeneration
- `growth_protocol_ch1`: 12 week old male mice were used for experimentation
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: TA muscles were removed, snap frozen, and RNA was extracted using TRIzol Reagent (Invitrogen) according to manufacturer麓s instruction.,Illumina TruSeq Stranded mRNA Library Prep kit (Cat# 20020594) was used with 500 ng of total RNA for the construction of sequencing libraries. Libraries were sequenc ... [71 more characters]
- `data_processing`: Rna-seq reads were aligned with STAR-aligner using the gene annotation as provided by ENCODE release 91.,Gene expression values were computed with the function featureCounts from the R package Rsubread.,R version 3.5.1,Assembly: Mus_musculus/Ensembl/GRCm38.p5/Annotation/Release_91-2018-02-26,Supplem ... [78 more characters]
- `platform_id`: GPL24247
- `contact_name`: Alexandra,,Fahrner
- `contact_email`: alexandra.fahrner@gmail.com
- `contact_department`: Division of Endocrinology, Diabetes and Clinical Nutrition
- `contact_institute`: University Hospital Zurich
- `contact_address`: R盲mistrasse 100
- `contact_city`: Zurich
- `contact_zip/postal_code`: 8091
- `contact_country`: Switzerland
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE199111
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM5964521 | Pax7Cre mouse 1 |
| GSM5964522 | Pax7Cre mouse 2 |
| GSM5964523 | Pax7Cre mouse 3 |
| GSM5964524 | Pax7Cre mouse 4 |
| GSM5964525 | Pax7Cre mouse 5 |
| GSM5964526 | miR-501KO mouse 1 |
| GSM5964527 | miR-501KO mouse 2 |
| GSM5964528 | miR-501KO mouse 3 |
| GSM5964529 | miR-501KO mouse 4 |
| GSM5964530 | miR-501KO mouse 5 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.1.genotype | 5 | 10/10 | 5 | 0 |
| suffix of title | genotype | 5 | 10/10 | 5 | 0 |
| genotype (without characteristics_ch1.1.genotype) + suffix of title | characteristics_ch1.1.genotype | 10 | 0/10 | 0 | 0 |
| characteristics_ch1.1.genotype (without genotype) + suffix of title | genotype | 10 | 0/10 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 5, "same_key_mean_r": 0.079, "other_mean_r": -0.018, "difference": 0.096, "permutation_p": 0.2683658170914543, "genes_used": 10823, "status": "not_supported"}
