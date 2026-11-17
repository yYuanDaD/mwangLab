# Review packet A (facts only): GSE60590

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC4622000.paper.md`

## Paper outline

- # An integrative analysis reveals coordinated reprogramming of the epigenome and the transcriptome in human skeletal muscle after training
- ## Abstract  `ABS` · abstract
- ## Abbreviations  `S1` · other
- ## Introduction  `S2` · introduction
- ## Results  `S3` · results
- ### Endurance exercise training induces global alterations in DNA methylation  `S3.1` · results
- ### Enrichment of training-induced DMPs in enhancers  `S3.2` · results
- ### Differential methylation is related to genes governing muscle related processes  `S3.3` · results
- ### Specific differential methylation correlates with expression changes in an exercise-dependent manner  `S3.4` · results
- ### Integrating transcriptional network analysis with DNA methylation identifies a coordinated training response  `S3.5` · results
- ## Discussion  `S4` · discussion
- ## Materials and Methods  `S5` · methods
- ### Human physiological measurements  `S5.1` · methods
- ### DNA methylation methods  `S5.2` · methods
- ### Bioinformatics analysis of DNA methylation data  `S5.3` · methods
- ### RNA sequencing  `S5.4` · methods
- ### Integration between DNA methylation and transcriptomics  `S5.5` · methods
- ### Data availability  `S5.6` · data_availability
- ## Disclosure of Potential Conflicts of Interest  `BK1` · other
- ## Acknowledgments  `BK2` · other
- ## Funding  `BK3` · other
- ## Author Contributions  `BK4` · other
- ## Supplemental Material  `BK5` · supplementary
- ## Accession mentions

## Metadata (33 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.gender`: male: 17; female: 16
- `characteristics_ch1.2.biopsy location`: right leg: 22; left leg: 11
- `characteristics_ch1.3.exercise status`: trained: 22; untrained: 11
- `characteristics_ch1.4.time point`: post-training period 1: 22; pre-training period 1: 11
- `subject`: s14: 2; s01: 2; s22: 2; s23: 2; s24: 2; s26: 2; s27: 2; s28: 2; s02: 2; s03: 2; s05: 2; s11: 1; s12: 1; s15: 1; s16: 1; s18: 1; s19: 1; s20: 1; s21: 1; s04: 1; s07: 1; s09: 1
- `grp`: T2: 22; T1: 11

### Constant columns

- `status`: Public on Jan 21 2015
- `submission_date`: Aug 21 2014
- `last_update_date`: May 15 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: skeletal muscle
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: skeletal muscle
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Trizol庐 method,RNA libraries were prepared for sequencing using standard Illumina protocols for paired end sequencing and clustered on cBot
- `data_processing`: Bcl to Fastq conversion was performed using bcl2Fastq v1.8.3 from the CASAVA software suite,The paired-end reads were trimmed with respect to quality and remaining adapter sequences using Trim Galore and aligned to the human genome reference hg19 (ENSEMBL v71) with TopHat version 2.0.4,The aligned r ... [201 more characters]
- `platform_id`: GPL11154
- `contact_name`: Joakim,,Lundeberg
- `contact_department`: Gene Technology
- `contact_institute`: KTH-Science for Life Laboratory
- `contact_address`: Tomtebodav盲gen 23A
- `contact_city`: Solna
- `contact_zip/postal_code`: 17165
- `contact_country`: Sweden
- `instrument_model`: Illumina HiSeq 2000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE60590,GSE60591
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `characteristics_ch1.5.original sample id`, `description`, `relation`, `supplementary_file_1`

### Samples

| sample | title | description |
|---|---|---|
| GSM1482932 | 219 | Sample 1 |
| GSM1482933 | 182 | Sample 2 |
| GSM1482934 | 196 | Sample 3 |
| GSM1482935 | 201 | Sample 4 |
| GSM1482936 | 121 | Sample 5 |
| GSM1482937 | 177 | Sample 6 |
| GSM1482938 | 202 | Sample 7 |
| GSM1482939 | 207 | Sample 8 |
| GSM1482940 | 101 | Sample 9 |
| GSM1482941 | 109 | Sample 10 |
| GSM1482942 | 138 | Sample 11 |
| GSM1482943 | 213 | Sample 12 |
| GSM1482944 | 206 | Sample 13 |
| GSM1482945 | 208 | Sample 14 |
| GSM1482946 | 186 | Sample 15 |
| GSM1482947 | 194 | Sample 16 |
| GSM1482948 | 212 | Sample 17 |
| GSM1482949 | 214 | Sample 18 |
| GSM1482950 | 191 | Sample 19 |
| GSM1482951 | 104 | Sample 20 |
| GSM1482952 | 147 | Sample 21 |
| GSM1482953 | 155 | Sample 22 |
| GSM1482954 | 218 | Sample 23 |
| GSM1482955 | 220 | Sample 24 |
| GSM1482956 | 108 | Sample 25 |
| GSM1482957 | 116 | Sample 26 |
| GSM1482958 | 132 | Sample 27 |
| GSM1482959 | 140 | Sample 28 |
| GSM1482960 | 165 | Sample 29 |
| GSM1482961 | 118 | Sample 30 |
| GSM1482962 | 126 | Sample 31 |
| GSM1482963 | 180 | Sample 32 |
| GSM1482964 | 160 | Sample 33 |

## Values with exercise words (by column)

- `characteristics_ch1.3.exercise status`: trained, untrained
- `characteristics_ch1.4.time point`: post-training period 1, pre-training period 1

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| subject | characteristics_ch1.3.exercise status | 22 | 22/33 | 11 | 0 |
| subject | characteristics_ch1.4.time point | 22 | 22/33 | 11 | 0 |
| subject | grp | 22 | 22/33 | 11 | 0 |
| characteristics_ch1.5.original sample id without the grp level | grp | 26 | 14/33 | 7 | 0 |
| suffix of title | characteristics_ch1.1.gender | 33 | 0/33 | 0 | 0 |
| characteristics_ch1.2.biopsy location (without characteristics_ch1.1.gender) + suffix of title | characteristics_ch1.1.gender | 33 | 0/33 | 0 | 0 |
| characteristics_ch1.3.exercise status (without characteristics_ch1.1.gender) + suffix of title | characteristics_ch1.1.gender | 33 | 0/33 | 0 | 0 |
| characteristics_ch1.4.time point (without characteristics_ch1.1.gender) + suffix of title | characteristics_ch1.1.gender | 33 | 0/33 | 0 | 0 |
