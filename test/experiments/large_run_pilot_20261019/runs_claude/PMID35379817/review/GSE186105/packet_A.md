# Review packet A (facts only): GSE186105

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC8980083.paper.md`

## Paper outline

- # Sirt6 reprograms myofibers to oxidative type through CREB-dependent Sox6 suppression
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Sirt6 ablation in skeletal muscle leads to a decrease in exercise performance  `S2.1` · results
- ### Sirt6 ablation decreases oxidative myofiber relative to glycolytic myofiber  `S2.2` · results
- ### Sirt6 ablation reduces mitochondrial content and oxidative capacity  `S2.3` · results
- ### Sirt6 ablation suppresses CREB transcription and its downstream genes  `S2.4` · results
- ### Sirt6 induces oxidative fiber conversion through the CREB-Sox6 axis  `S2.5` · results
- ### Pharmacological Sirt6 activation enhances exercise performance  `S2.6` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### Animal studies  `S4.1` · methods
- ### Grip strength measurement and treadmill running  `S4.2` · methods
- ### Body fat and lean percentage  `S4.3` · methods
- ### Indirect calorimetry  `S4.4` · methods
- ### Ex vivo muscle isometric force and fatigue measurement  `S4.5` · methods
- ### Histology  `S4.6` · methods
- ### Transmission electron microscopy (TEM) and image analysis  `S4.7` · methods
- ### Cell culture, transient transfection and reporter gene assays  `S4.8` · methods
- ### Generation of Sirt6 KO cells using CRISPR/Cas9 system  `S4.9` · methods
- ### Primary myofiber isolation  `S4.10` · methods
- ### Mitochondrial respiration  `S4.11` · methods
- ### Western blotting  `S4.12` · methods
- ### RNA isolation and real-time quantitative RT-PCR (qPCR)  `S4.13` · methods
- ### Chromatin immunoprecipitation  `S4.14` · methods
- ### RNA sequencing (RNA-Seq) and data analysis  `S4.15` · methods
- ### Bioinformatic analysis  `S4.16` · methods
- ### Statistical analysis  `S4.17` · methods
- ### Reporting summary  `S4.18` · methods
- ## Supplementary information  `S5` · supplementary
- ### (untitled)  `S5.1` · supplementary
- ## Acknowledgements  `S6` · other
- ## (untitled)  `S7` · other
- ## Author contributions  `S8` · other
- ## Peer review  `S9` · other
- ### Peer review information  `S9.1` · other
- ## Data availability  `S10` · data_availability
- ## Competing interests  `S11` · other
- ## Contributor Information  `S13` · other
- ## Supplementary information  `S14` · supplementary
- ## Accession mentions

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.3.genotype`: WT: 3; Muscle-specific Sirt6 KO: 3
- `geno`: WT: 3; KO: 3

### Constant columns

- `status`: Public on Feb 25 2022
- `submission_date`: Oct 19 2021
- `last_update_date`: Feb 25 2022
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: C57BL/6
- `characteristics_ch1.1.tissue`: Gastrocnemius muscle
- `characteristics_ch1.2.age`: 20 weeks
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Gastrocnemius muscles tissues were excised from mice and stored in RNAlater solution. Total RNA was extracted using Trizol.,A library was independently prepared with 1ug of total RNA for each sample by Illumina TruSeq Stranded mRNA LT Sample Prep Kit (#RS-122-2001)
- `data_processing`: bcl2fastq2-v2.20.0 package was used for basecalling.,Quality check of basecalling was done using FastQC v0.11.7 by calculating phred quality score.,Sequenced reads were trimmed for adaptor sequence using Trimmomatic0.38, then mapped to mm10 whole genome using HISAT2 v2.1.0 and Bowtie2 v2.3.4.1,Trans ... [302 more characters]
- `platform_id`: GPL24247
- `contact_name`: Byung-Hyun,,Park
- `contact_institute`: Jeonbuk National University Medical School
- `contact_address`: 567 Baekje-daero, Deokjin-gu
- `contact_city`: Jeonju-si
- `contact_zip/postal_code`: 54896
- `contact_country`: South Korea
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE186105
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM5632366 | Sirt6 flox/flox, rep 1 | WT1 |
| GSM5632367 | Sirt6 flox/flox, rep 2 | WT4 |
| GSM5632368 | Sirt6 flox/flox, rep 3 | WT6 |
| GSM5632369 | Myl1-Cre; Sirt6 flox/flox, rep 1 | KO3 |
| GSM5632370 | Myl1-Cre; Sirt6 flox/flox, rep 2 | KO6 |
| GSM5632371 | Myl1-Cre; Sirt6 flox/flox, rep 3 | KO7 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.3.genotype | 3 | 6/6 | 3 | 0 |
| suffix of title | geno | 3 | 6/6 | 3 | 0 |
| characteristics_ch1.3.genotype (without geno) + suffix of title | geno | 6 | 0/6 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": 0.164, "other_mean_r": -0.095, "difference": 0.259, "permutation_p": 0.5077461269365318, "genes_used": 8103, "status": "not_supported"}
