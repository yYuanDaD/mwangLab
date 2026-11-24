# Review packet A (facts only): GSE146336

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC7702122.paper.md`

## Paper outline

- # Thyroid hormone receptor α in skeletal muscle is essential for T3‐mediated increase in energy expenditure
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## INTRODUCTION  `S1` · introduction
- ## MATERIALS AND METHODS  `S2` · methods
- ### Animals  `S2.1` · methods
- ### In vivo pharmacology and energy metabolism studies  `S2.2` · methods
- ### Glucose tolerance studies  `S2.3` · methods
- ### Exercise studies  `S2.4` · methods
- #### Voluntary running  `S2.4.1` · methods
- #### Treadmill‐running  `S2.4.2` · methods
- ### Transcriptomic analysis by RNA sequencing  `S2.5` · methods
- ### Bioinformatic analysis  `S2.6` · methods
- ### Quantitative real‐time PCR  `S2.7` · methods
- #### RNA extraction & cDNA synthesis  `S2.7.1` · methods
- #### qPCR  `S2.7.2` · methods
- #### Western blotting  `S2.7.3` · methods
- ### Mitochondrial respiratory capacity  `S2.8` · methods
- ### Muscle morphology  `S2.9` · methods
- ### Blood plasma analyses  `S2.10` · methods
- ### Statistics  `S2.11` · methods
- ## RESULTS  `S3` · results
- ### Skeletal muscle TRα_1 defines fiber‐type composition in slow‐twitch muscle but is largely dispensable for exercise capacity and energy homeostasis  `S3.1` · results
- ### TRα_1 in skeletal muscle is required for T3‐induced energy expenditure but is dispensable for T3‐induced elevation in body temperature  `S3.2` · results
- ### Structural and metabolic pathways dominate the transcriptome in response to T3‐mediated activation of TRα_1 in soleus muscle  `S3.3` · results
- ## DISCUSSION  `S4` · discussion
- ## CONFLICT OF INTEREST  `S5` · other
- ## AUTHOR CONTRIBUTION  `S6` · other
- ## Supporting information  `S7` · supplementary
- ## DATA AVAILABILITY STATEMENT  `DA` · data_availability
- ## Accession mentions

## Metadata (22 samples)

### Grouping columns (level: count)

- `characteristics_ch1.0.genotype`: WT: 11; TRa1 KO: 11
- `characteristics_ch1.3.treatment`: T3 treatmant: 13; vechicle: 9

### Constant columns

- `status`: Public on Sep 21 2020
- `submission_date`: Mar 04 2020
- `last_update_date`: Sep 21 2020
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Soleus muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.1.Sex`: Male
- `characteristics_ch1.2.tissue`: Soleus muscle
- `molecule_ch1`: polyA RNA
- `extract_protocol_ch1`: Total RNA was isolated using RNeasy mini kit (Qiagen) according to the manufacturer鈥檚 protocol. Messenger RNA sequencing libraries were prepared using the Illumina TruSeq Stranded mRNA protocol (Illumina). Poly-A containing mRNAs were purified by poly-T attached magnetic beads, fragmented, and cDNA  ... [477 more characters]
- `data_processing`: The STAR aligner v. 2.7.3a was used to align RNA-seq read against the mm10 mouse genome assembly and GENCODE vM22 mouse transcripts.,The software program featureCounts v. 1.6.4 was used to summarize reads onto genes.,Testing for differential expression was performed using edgeR v. 3.26.8 using the q ... [468 more characters]
- `platform_id`: GPL24247
- `contact_name`: Lars,Roed,Ingerslev
- `contact_email`: ingerslev@sund.ku.dk
- `contact_laboratory`: Integrative Physiology
- `contact_department`: NNF Center for Basic Metabolic Research
- `contact_institute`: Copenhagen University
- `contact_address`: Blegdamsvej 3B
- `contact_city`: Copenhagen
- `contact_zip/postal_code`: 2200
- `contact_country`: Denmark
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE146336
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`

### Samples

| sample | title |
|---|---|
| GSM4378238 | 033_1: Sample 1 |
| GSM4378239 | 033_2: Sample 2 |
| GSM4378240 | 033_3: Sample 3 |
| GSM4378241 | 033_4: Sample 4 |
| GSM4378242 | 033_5: Sample 5 |
| GSM4378243 | 033_6: Sample 6 |
| GSM4378244 | 033_7: Sample 7 |
| GSM4378245 | 033_8: Sample 8 |
| GSM4378246 | 033_9: Sample 9 |
| GSM4378247 | 033_10: Sample 10 |
| GSM4378248 | 033_11: Sample 11 |
| GSM4378249 | 033_12: Sample 12 |
| GSM4378250 | 033_13: Sample 13 |
| GSM4378251 | 033_14: Sample 14 |
| GSM4378252 | 033_15: Sample 15 |
| GSM4378253 | 033_16: Sample 16 |
| GSM4378254 | 033_17: Sample 17 |
| GSM4378255 | 033_18: Sample 18 |
| GSM4378256 | 033_19: Sample 19 |
| GSM4378257 | 033_20: Sample 20 |
| GSM4378258 | 033_21: Sample 21 |
| GSM4378259 | 033_22: Sample 22 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.0.genotype | 22 | 0/22 | 0 | 0 |
| characteristics_ch1.3.treatment (without characteristics_ch1.0.genotype) + suffix of title | characteristics_ch1.0.genotype | 22 | 0/22 | 0 | 0 |
| suffix of key | characteristics_ch1.0.genotype | 22 | 0/22 | 0 | 0 |
| characteristics_ch1.3.treatment (without characteristics_ch1.0.genotype) + suffix of key | characteristics_ch1.0.genotype | 22 | 0/22 | 0 | 0 |
| suffix of title | characteristics_ch1.3.treatment | 22 | 0/22 | 0 | 0 |
| characteristics_ch1.0.genotype (without characteristics_ch1.3.treatment) + suffix of title | characteristics_ch1.3.treatment | 22 | 0/22 | 0 | 0 |
| suffix of key | characteristics_ch1.3.treatment | 22 | 0/22 | 0 | 0 |
| characteristics_ch1.0.genotype (without characteristics_ch1.3.treatment) + suffix of key | characteristics_ch1.3.treatment | 22 | 0/22 | 0 | 0 |
