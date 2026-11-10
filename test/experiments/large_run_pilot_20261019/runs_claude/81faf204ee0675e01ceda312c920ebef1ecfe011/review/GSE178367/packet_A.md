# Review packet A (facts only): GSE178367

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC8348158.paper.md`

## Paper outline

- # Transcriptomic and Metabolic Network Analysis of Metabolic Reprogramming and IGF-1 Modulation in SCA3 Transgenic Mice
- ## Abstract  `ABS` · abstract
- ## 1. Introduction  `S1` · introduction
- ## 2. Results  `S2` · results
- ### 2.1. Exploratory Data Analysis  `S2.1` · results
- ### 2.2. Differential Gene Expression (DGE) Analysis  `S2.2` · results
- ### 2.3. Functional Enrichment Analysis  `S2.3` · results
- ### 2.4. Metabolic Network Analysis  `S2.4` · results
- ## 3. Discussion  `S3` · discussion
- ## 4. Materials and Methods  `S4` · methods
- ### 4.1. SCA3 Transgenic Mouse Model  `S4.1` · methods
- ### 4.2. RNA Extraction and qPCR  `S4.2` · methods
- ### 4.3. High-Resolution Respirometry  `S4.3` · methods
- ### 4.4. RNA Sequencing of Mouse Cerebellar RNA  `S4.4` · methods
- ### 4.5. Preprocessing RNA-Seq Data  `S4.5` · methods
- ### 4.6. Expression Profile  `S4.6` · methods
- ### 4.7. Differential Gene Expression (DGE) Analysis and Functional Enrichment Analysis  `S4.7` · methods
- ### 4.8. Metabolic Network Model Reconstruction and Flux Analysis  `S4.8` · methods
- ## app-group  `APP1` · other
- ## Author Contributions  `BK2` · other
- ## Funding  `BK3` · other
- ## Institutional Review Board Statement  `BK4` · other
- ## Informed Consent Statement  `BK5` · other
- ## Data Availability Statement  `DA` · data_availability
- ## Conflicts of Interest  `BK6` · other
- ## Figures and tables  `FLT` · other
- ## Accession mentions

## Metadata (9 samples)

### Grouping columns (level: count)

- `source_name_ch1`: Cerebellar tissue - 15Q: 3; Cerebellar tissue - 84Q: 3; Cerebellar tissue - 84Q+IGF1: 3
- `characteristics_ch1.1.genotype/variation`: 84Q: 6; 15Q: 3
- `characteristics_ch1.2.treatment`: untreated: 6; treated with IGF1(50 mg/kg) per week: 3
- `grp`: Q15: 3; Q84: 3; Q84IGF: 3

### Constant columns

- `status`: Public on Aug 11 2021
- `submission_date`: Jun 17 2021
- `last_update_date`: Aug 11 2021
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain background`: C57BL/6
- `characteristics_ch1.3.cell type`: cerebellar tissue
- `treatment_protocol_ch1`: The SCA3 15Q and 84Q transgenic mice were administered intraperitoneal injections of PBS(0.01 M) or IGF1(50 mg/kg) weekly from the postnatal age of 9 months to 18 months.
- `growth_protocol_ch1`: Tissue was harvest from 18-month old mice.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted using Trizol庐 Reagent (Invitrogen, USA) according to the instruction manual. Purified RNA was quantified at OD260nm using a ND-1000 spectrophotometer (Nanodrop Technology,USA) and qualitated by using a Bioanalyzer 2100 (Agilent Technology, USA) with RNA 6000 LabChip kit (Agil ... [560 more characters]
- `data_processing`: Basecalls performed using bcl2fastq version 2.20.,Both adaptor clipping and sequence quality trimming were performed using Trimmomatic v0.36 with a sliding-window approach,RNAseq reads were aligned to the mm10 genome assembly using hisat2 version 2.2.0 with default setting,Genome_build: mm10,Supplem ... [116 more characters]
- `platform_id`: GPL17021
- `contact_name`: Chin-San,,Liu
- `contact_email`: 26602@cch.org.tw
- `contact_institute`: Changhua Christian Hospital
- `contact_address`: 135 Nan-Hsiao Street
- `contact_city`: Changhua
- `contact_zip/postal_code`: 500-06
- `contact_country`: Taiwan
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE178367
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`

### Samples

| sample | title |
|---|---|
| GSM5388434 | Cerebellar tissue - 15Q_rep1 [Q15_2_1] |
| GSM5388435 | Cerebellar tissue - 15Q_rep2 [Q15_3_5] |
| GSM5388436 | Cerebellar tissue - 15Q_rep3 [Q15_5_3] |
| GSM5388437 | Cerebellar tissue - 84Q_rep1 [18_1_4] |
| GSM5388438 | Cerebellar tissue - 84Q_rep2 [19_2_4] |
| GSM5388439 | Cerebellar tissue - 84Q_rep3 [22_2_4] |
| GSM5388440 | Cerebellar tissue - 84Q+IGF1_rep1 [18_2_1] |
| GSM5388441 | Cerebellar tissue - 84Q+IGF1_rep2 [22_1_1] |
| GSM5388442 | Cerebellar tissue - 84Q+IGF1_rep3 [22_2_1] |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of key | source_name_ch1 | 4 | 0/9 | 0 | 2 |
| characteristics_ch1.2.treatment (without source_name_ch1) + suffix of key | source_name_ch1 | 5 | 0/9 | 0 | 2 |
| grp (without source_name_ch1) + suffix of key | source_name_ch1 | 5 | 0/9 | 0 | 2 |
| suffix of key | characteristics_ch1.1.genotype/variation | 4 | 0/9 | 0 | 2 |
| source_name_ch1 (without characteristics_ch1.1.genotype/variation) + suffix of key | characteristics_ch1.1.genotype/variation | 5 | 0/9 | 0 | 2 |
| characteristics_ch1.2.treatment (without characteristics_ch1.1.genotype/variation) + suffix of key | characteristics_ch1.1.genotype/variation | 5 | 0/9 | 0 | 2 |
| grp (without characteristics_ch1.1.genotype/variation) + suffix of key | characteristics_ch1.1.genotype/variation | 5 | 0/9 | 0 | 2 |
| suffix of key | characteristics_ch1.2.treatment | 4 | 0/9 | 0 | 2 |
