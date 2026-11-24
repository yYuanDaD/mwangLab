# Review packet A (facts only): GSE99963

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC5680174.paper.md`

## Paper outline

- # Transcriptomic and epigenetic responses to short-term nutrient-exercise stress in humans
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Research Design and Methods  `S2` · methods
- ### Study participants and experimental design  `S2.1` · methods
- ### Plasma Analysis  `S2.2` · methods
- ### RNA sequencing  `S2.3` · methods
- ### DNA methylation analysis  `S2.4` · methods
- ### Accession Numbers  `S2.5` · data_availability
- ### Bioinformatic analysis  `S2.6` · methods
- ### Statistics  `S2.7` · methods
- ## Results and Discussion  `S3` · results
- ### Short-term resistance exercise causes major changes in the skeletal muscle transcriptome compared with HFD alone  `S3.1` · results
- ### Short-term HFD induces immune and inflammatory genes regardless of physical activity  `S3.2` · results
- ### Transcriptional response to short-term HFD  `S3.3` · results
- ### Epigenetic response to HFD and resistance exercise  `S3.4` · results
- ## Electronic supplementary material  `S4` · supplementary
- ### (untitled)  `S4.1` · supplementary
- ## Author Contributions  `BK1` · other
- ## Competing Interests  `BK2` · other
- ### Competing Interests  `BK2.1` · other
- ## Accession mentions

## Metadata (28 samples)

### Grouping columns (level: count)

- `source_name_ch1`: Sedentary_Post_muscle: 7; Exercise_Post_muscle: 7; Sedentary_Pre_muscle: 7; Exercise_Pre_muscle: 7
- `characteristics_ch1.0.subject id`: S11: 2; S13: 2; S2: 2; S4: 2; S6: 2; S8: 2; S9: 2; S10: 2; S12: 2; S14: 2; S1: 2; S3: 2; S5: 2; S7: 2
- `characteristics_ch1.1.group`: Sedentary; 9 days of a high-fat diet alone (Sed-HFD): 14; Exercise; 9 days of a high-fat diet in combination with resistance exercise (Ex-HFD): 14
- `characteristics_ch1.2.time point`: Post: 14; Pre: 14
- `subject`: S11: 2; S13: 2; S2: 2; S4: 2; S6: 2; S8: 2; S9: 2; S10: 2; S12: 2; S14: 2; S1: 2; : 2; S5: 2; S7: 2
- `time`: Post: 13; Pre: 13; : 2
- `grp`: Ex: 14; Sed: 12; : 2
- `ex_post`: 0: 19; 1: 7; : 2

### Constant columns

- `status`: Public on Feb 13 2018
- `submission_date`: Jun 13 2017
- `last_update_date`: May 15 2019
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.3.tissue`: muscle
- `treatment_protocol_ch1`: High-fat diet (HFD) intervention, sedentary or exercised
- `growth_protocol_ch1`: Not applicable
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Allprep庐 DNA/RNA/miRNA Universal Kit (Qiagen),Illumina TruSeq Stranded Total RNA with Ribo-Zero Gold protocol (Illumina)
- `data_processing`: Reads were trimmed using  trim_galore v0.4.0 and cutadapt v1.9.1 on default settings,Trimmed reads were mapped to hg38 with Rsubread and gene read coverages were computed with featureCounts and the Ensemble v84 gtf file,Differentially expressed genes were determined using edgeR,Genome_build: hg38,Su ... [115 more characters]
- `platform_id`: GPL16791
- `contact_name`: Lars,Roed,Ingerslev
- `contact_email`: ingerslev@sund.ku.dk
- `contact_laboratory`: Integrative Physiology
- `contact_department`: NNF Center for Basic Metabolic Research
- `contact_institute`: Copenhagen University
- `contact_address`: Blegdamsvej 3B
- `contact_city`: Copenhagen
- `contact_zip/postal_code`: 2200
- `contact_country`: Denmark
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE99963,GSE99965
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM2666592 | Post_S11 |
| GSM2666593 | Post_S13 |
| GSM2666594 | Post_S2 |
| GSM2666595 | Post_S4 |
| GSM2666596 | Post_S6 |
| GSM2666597 | Post_S8 |
| GSM2666598 | Post_S9 |
| GSM2666599 | Pre_S10 |
| GSM2666600 | Pre_S12 |
| GSM2666601 | Pre_S14 |
| GSM2666602 | Pre_S1 |
| GSM2666603 | Pre_S3 |
| GSM2666604 | Pre_S5 |
| GSM2666605 | Pre_S7 |
| GSM2666606 | Post_S10 |
| GSM2666607 | Post_S12 |
| GSM2666608 | Post_S14 |
| GSM2666609 | Post_S1 |
| GSM2666610 | Post_S3 |
| GSM2666611 | Post_S5 |
| GSM2666612 | Post_S7 |
| GSM2666613 | Pre_S11 |
| GSM2666614 | Pre_S13 |
| GSM2666615 | Pre_S2 |
| GSM2666616 | Pre_S4 |
| GSM2666617 | Pre_S6 |
| GSM2666618 | Pre_S8 |
| GSM2666619 | Pre_S9 |

## Values with exercise words (by column)

- `source_name_ch1`: Exercise_Post_muscle, Exercise_Pre_muscle, Sedentary_Post_muscle, Sedentary_Pre_muscle
- `characteristics_ch1.1.group`: Exercise; 9 days of a high-fat diet in combination with resistance exercise (Ex-HFD), Sedentary; 9 days of a high-fat diet alone (Sed-HFD)
- `treatment_protocol_ch1`: High-fat diet (HFD) intervention, sedentary or exercised
- `grp`: Ex, Sed

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the source_name_ch1 level | source_name_ch1 | 14 | 28/28 | 0 | 0 |
| suffix of title | source_name_ch1 | 14 | 28/28 | 0 | 0 |
| characteristics_ch1.0.subject id (without source_name_ch1) + suffix of title | source_name_ch1 | 14 | 28/28 | 0 | 0 |
| characteristics_ch1.1.group (without source_name_ch1) + suffix of title | source_name_ch1 | 14 | 28/28 | 0 | 0 |
| subject (without source_name_ch1) + suffix of title | source_name_ch1 | 14 | 28/28 | 0 | 0 |
| grp (without source_name_ch1) + suffix of title | source_name_ch1 | 14 | 28/28 | 0 | 0 |
| characteristics_ch1.0.subject id | source_name_ch1 | 14 | 28/28 | 0 | 0 |
| title without the characteristics_ch1.2.time point level | characteristics_ch1.2.time point | 14 | 28/28 | 14 | 0 |
