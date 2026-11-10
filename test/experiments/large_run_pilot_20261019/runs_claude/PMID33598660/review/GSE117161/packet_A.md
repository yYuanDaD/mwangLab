# Review packet A (facts only): GSE117161

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC7868630.paper.md`

## Paper outline

- # Monitoring daytime differences in moderate intensity exercise capacity using treadmill test and muscle dissection
- ## Abstract  `ABS` · abstract
- ## Before you begin  `S1` · other
- ### The importance of daytime to your experimental design  `S1.1` · methods
- ### Choosing your zeitgeber time  `S1.2` · other
- ### Acclimatize mice under a light-dark cycle that suits your experimental design  `S1.3` · methods
- ### Handle mice to reduce variability  `S1.4` · other
- ### Setup your treadmill  `S1.5` · other
- ## Key resources table  `S2` · other
- ## Step-by-step method details  `S3` · methods
- ### Habituate mice to run on the treadmill  `S3.1` · methods
- ### Run mice at a moderate intensity to evaluate running capacity  `S3.2` · methods
- ### Dissecting soleus, gastrocnemius plantaris, and quadriceps muscles for further analyses  `S3.3` · methods
- ## Expected outcomes  `S4` · other
- ## Limitations  `S5` · other
- ### Use of shocks as aversive stimulus  `S5.1` · other
- ### Differences between protocols in the literature  `S5.2` · methods
- ### Strain, age, and sex differences  `S5.3` · other
- ## Troubleshooting  `S6` · other
- ### Problem 1  `S6.1` · other
- ### Potential solution  `S6.2` · other
- ### Problem 2  `S6.3` · other
- ### Potential solution  `S6.4` · other
- ### Problem 3  `S6.5` · other
- ### Potential solution  `S6.6` · other
- ### Problem 4  `S6.7` · other
- ### Potential solution  `S6.8` · other
- ### Problem 5  `S6.9` · other
- ### Potential solution  `S6.10` · other
- ## Resource availability  `S7` · other
- ### Lead contact  `S7.1` · other
- ### Materials availability  `S7.2` · methods
- ### Data and code availability  `S7.3` · data_availability
- ## Accession mentions

## Metadata (18 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.time`: Early (ZT14): 9; Late (ZT22): 9
- `characteristics_ch1.2.running protocole`: Basal: 6; High: 6; Moderate: 6
- `run`: Basal: 6; High: 6; Moderate: 6
- `time`: ZT14: 9; ZT22: 9

### Constant columns

- `status`: Public on Apr 07 2019
- `submission_date`: Jul 16 2018
- `last_update_date`: Apr 07 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: gastrocnemius muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: C57bl6
- `characteristics_ch1.3.gender`: male
- `treatment_protocol_ch1`: Mice were acclimated to treadmill running (Panlab Harvard Apparatus, Barcelona, Spain) a day prior to the sprint or the endurance exhaustion test: Pre-test: 10 min without movement follows 10 min at 0.1 m/sec with a 0% slope; 0.4mA shock intensity.Sprint cohort: phase I 鈥 5 min at 8 cm/sec with a 0% ... [559 more characters]
- `growth_protocol_ch1`: All animal experiments and procedures were conducted in conformity with the Institutional Animal Care and Use Committee (IACUC) guidelines. Three months old, males wild type mice were used. Mice were kept under 12 h light/dark regimen and fed either ad libitum or exclusively during the dark or light ... [96 more characters]
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Gastrocnemius muscles thawed for 1 minute at RT, then transferred to 2 ml TRI-reagent. Tissue was homogenized using disperser (IKA-T18) and then transferred to 1.7 ml tube and stand in RT for 5 minutes. 200 碌L chloroform was added to each tissue sample for phase separation. Samples was then centrifu ... [753 more characters]
- `data_processing`: Reads were trimmed using cutadapt and mapped to genome mm10 using STAR  v2.4.2a with default parameters.,Counting proceeded over genes annotated in Gencode release mm10 using STAR.,Genome_build: mm10.,Supplementary_files_format_and_content: RNA-seq_raw_counts_Exercise_performance_project.csv,Supplem ... [76 more characters]
- `platform_id`: GPL19057
- `contact_name`: Jonathan,Aryeh,Sobel
- `contact_email`: jonathan.sobel@weizmann.ac.il
- `contact_phone`: 972587889058
- `contact_laboratory`: Asher
- `contact_department`: Biomolecular Sciences
- `contact_institute`: Weizmann Institute of science
- `contact_address`: Benoziyo Building for Biological Sciences, room 277S, Weizmann Institute of Science
- `contact_city`: Rehovot
- `contact_zip/postal_code`: 7610001
- `contact_country`: Israel
- `instrument_model`: NextSeq 500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE117161
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM3272710 | Basal_Early_A |
| GSM3272711 | Basal_Early_B |
| GSM3272712 | Basal_Early_C |
| GSM3272713 | Basal_Late_A |
| GSM3272714 | Basal_Late_B |
| GSM3272715 | Basal_Late_C |
| GSM3272716 | High_Early_A |
| GSM3272717 | High_Early_B |
| GSM3272718 | High_Early_C |
| GSM3272719 | High_Late_A |
| GSM3272720 | High_Late_B |
| GSM3272721 | High_Late_C |
| GSM3272722 | Moderate_Early_A |
| GSM3272723 | Moderate_Early_B |
| GSM3272724 | Moderate_Early_C |
| GSM3272725 | Moderate_Late_A |
| GSM3272726 | Moderate_Late_B |
| GSM3272727 | Moderate_Late_C |

## Values with exercise words (by column)

- `treatment_protocol_ch1`: Mice were acclimated to treadmill running (Panlab Harvard Apparatus, Barcelona, Spain) a day prior to the sprint or the endurance exhaustion test: Pre-test: 10 min without movement follows 10 min at 0.1 m/sec with a 0% slope; 0.4mA shock intensity.Sprint cohort: phase I 鈥 5 min at 8 cm/sec with a 0% slope; phase II 鈥 increases by 2 cm/sec every min. Mice ran until they reached failure, which was pre-define as 15 shocks per 60 sec or 25 shocks within 90sec or 30 within 120sec. Time to failure was recorded. Endurance  cohort: phase I 鈥 5 min at 8 cm/sec with a 0% slope; phase II 鈥 increases by 2 cm/sec every min until reaching a final speed of 20cm/sec. Mice fully performed the high intensity protocol, or performed the moderate intensity test for 1 hour, subsequently their Gastrocnemius muscle was dissected and immediately frozen in liquid nitrogen.
- `data_processing`: Reads were trimmed using cutadapt and mapped to genome mm10 using STAR  v2.4.2a with default parameters.,Counting proceeded over genes annotated in Gencode release mm10 using STAR.,Genome_build: mm10.,Supplementary_files_format_and_content: RNA-seq_raw_counts_Exercise_performance_project.csv,Supplementary_files_format_and_content: Raw read count for each gene in each sample

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.1.time level | characteristics_ch1.1.time | 9 | 18/18 | 9 | 0 |
| characteristics_ch1.2.running protocole (without characteristics_ch1.1.time) + suffix of title | characteristics_ch1.1.time | 9 | 18/18 | 9 | 0 |
| run (without characteristics_ch1.1.time) + suffix of title | characteristics_ch1.1.time | 9 | 18/18 | 9 | 0 |
| title without the characteristics_ch1.2.running protocole level | characteristics_ch1.2.running protocole | 6 | 18/18 | 6 | 0 |
| characteristics_ch1.1.time (without characteristics_ch1.2.running protocole) + suffix of title | characteristics_ch1.2.running protocole | 6 | 18/18 | 6 | 0 |
| time (without characteristics_ch1.2.running protocole) + suffix of title | characteristics_ch1.2.running protocole | 6 | 18/18 | 6 | 0 |
| title without the run level | run | 6 | 18/18 | 6 | 0 |
| characteristics_ch1.1.time (without run) + suffix of title | run | 6 | 18/18 | 6 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the characteristics_ch1.1.time level", "across": "_across", "within": [], "n_same_key_pairs": 9, "same_key_mean_r": 0.274, "other_mean_r": -0.034, "difference": 0.309, "permutation_p": 0.0004997501249375312, "genes_used": 8836, "status": "supported"}
