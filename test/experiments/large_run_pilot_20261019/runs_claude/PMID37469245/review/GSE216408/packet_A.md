# Review packet A (facts only): GSE216408

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261028\papers\PMC10570112.paper.md`

## Paper outline

- # Skeletal muscle‐specific DJ‐1 ablation‐induced atrogenes expression and mitochondrial dysfunction contributing to muscular atrophy
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## Introduction  `S1` · introduction
- ## Methods  `S2` · methods
- ### Human subjects  `S2.1` · methods
- ### Animals  `S2.2` · methods
- ### Immobilization protocol  `S2.3` · methods
- ### Compound 23 treatment  `S2.4` · methods
- ### Autophagy flux protocol  `S2.5` · methods
- ### In vivo muscle contractility analysis  `S2.6` · methods
- ### Muscle‐grip strength test  `S2.7` · methods
- ### Maximal load capacity test  `S2.8` · methods
- ### Hanging test  `S2.9` · methods
- ### Rotarod  `S2.10` · methods
- ### Treadmill performance test  `S2.11` · methods
- ### Histology and immunofluorescence  `S2.12` · methods
- ### Transmission electron microscopy  `S2.13` · methods
- ### Nuclear and cytoplasmic protein extraction  `S2.14` · methods
- ### Muscle fibres permeabilization and mitochondrial respiration studies  `S2.15` · methods
- ### RNA sequencing studies  `S2.16` · methods
- ### Cell lines, cell culture, C2C12 myotube differentiation, and transfection  `S2.17` · methods
- ### qRT‐PCR and western blot analysis  `S2.18` · methods
- ### Reactive oxygen species staining  `S2.19` · methods
- ### Luciferase reporter assay  `S2.20` · methods
- ### Statistical analyses  `S2.21` · methods
- ## Results  `S3` · results
- ### DJ‐1 expression is positively correlated with muscle mass in humans and mice  `S3.1` · results
- ### Mice with skeletal muscle‐specific DJ‐1 ablation have slightly decreased lean mass and impaired exercise performance  `S3.2` · results
- ### Ablation of DJ‐1 decreases fibre CSA without affecting fibre types  `S3.3` · results
- ### Mitochondrial function is impaired in muscles with DJ‐1 deletion  `S3.4` · results
- ### MDKO mice show aggravated muscle dystrophy during immobilization  `S3.5` · results
- ### MDKO mice muscles show molecular characteristics specific to atrophy  `S3.6` · results
- ### FoxO1 pathway is responsible for DJ‐1 ablation‐induced muscle atrophy  `S3.7` · results
- ### Mice treated with compound 23, a DJ‐1 antagonist, exhibited progressive muscular atrophy symptoms during immobilization  `S3.8` · results
- ## Discussion  `S4` · discussion
- ## Conflict of interest  `S5` · other
- ## Supporting information  `S6` · supplementary
- ## Accession mentions

## Metadata (7 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.genotype`: skeletal muscle PARK7KO: 4; WT: 3
- `geno`: KO: 4; WT: 3

### Constant columns

- `status`: Public on Dec 12 2023
- `submission_date`: Oct 24 2022
- `last_update_date`: Dec 12 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: gas
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Gastrocnemius muscle
- `characteristics_ch1.2.treatment`: immobilization-induced muscle atrophy
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: GAS tissues from immobilized muscle-specific DJ-1 knockout (MPARK7KO) mice and flox mice were extracted for RNA sequencing.,cDNA libraries for each sample were constructed as reported previously (Yao et al., 2022).,Libraries were sequenced on BGIseq500 platform (BGI-Shenzhen, China), using 150 bp pa ... [52 more characters]
- `data_processing`: The clean reads were mapped to the reference genome (mm10) using STAR (2.7.10a).,Quantification of gene expression was calculated using RSEM (v1.2.28).,Differential expression analysis between groups was conducted using the DESeq2(1.3.40) with adjust P value < 0.05 and |FC|>1.5. GO enrichment analys ... [206 more characters]
- `platform_id`: GPL23479
- `contact_name`: Kong,,Xingxing
- `contact_email`: kongxingxing@fudan.edu.cn
- `contact_department`: School of Life Sciences
- `contact_institute`: Fudan University
- `contact_address`: Songhu Road 2005
- `contact_city`: Shanghai
- `contact_zip/postal_code`: 200438
- `contact_country`: China
- `instrument_model`: BGISEQ-500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE216408
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`, `_norm_key`

### Samples

| sample | title |
|---|---|
| GSM6672082 | GAS WT rep1 |
| GSM6672083 | GAS WT rep2 |
| GSM6672084 | GAS WT rep3 |
| GSM6672085 | GAS MPARK7KO rep1 |
| GSM6672086 | GAS MPARK7KO rep2 |
| GSM6672087 | GAS MPARK7KO rep3 |
| GSM6672088 | GAS MPARK7KO rep4 |

## Values with exercise words (by column)

- `characteristics_ch1.2.treatment`: immobilization-induced muscle atrophy
- `extract_protocol_ch1`: GAS tissues from immobilized muscle-specific DJ-1 knockout (MPARK7KO) mice and flox mice were extracted for RNA sequencing.,cDNA libraries for each sample were constructed as reported previously (Yao et al., 2022).,Libraries were sequenced on BGIseq500 platform (BGI-Shenzhen, China), using 150 bp paired-end reads aimed at 30 million reads per sample.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.1.genotype | 4 | 6/7 | 3 | 0 |
| suffix of key | characteristics_ch1.1.genotype | 4 | 6/7 | 3 | 0 |
| suffix of title | geno | 4 | 6/7 | 3 | 0 |
| key without the geno level | geno | 4 | 6/7 | 3 | 0 |
| suffix of key | geno | 4 | 6/7 | 3 | 0 |
| geno (without characteristics_ch1.1.genotype) + suffix of title | characteristics_ch1.1.genotype | 7 | 0/7 | 0 | 0 |
| geno (without characteristics_ch1.1.genotype) + suffix of key | characteristics_ch1.1.genotype | 7 | 0/7 | 0 | 0 |
| characteristics_ch1.1.genotype (without geno) + suffix of title | geno | 7 | 0/7 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": 0.147, "other_mean_r": -0.049, "difference": 0.196, "permutation_p": 0.09495252373813093, "genes_used": 7890, "status": "not_supported"}
