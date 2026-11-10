# Review packet A (facts only): GSE281849

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC11604346.paper.md`

## Paper outline

- # Inactivity‐mediated molecular adaptations: Insights from a preclinical model of physical activity reduction
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## INTRODUCTION  `S1` · introduction
- ## MATERIALS AND METHODS  `S2` · methods
- ### Animals, housing, and diet  `S2.1` · methods
- ### Treadmill setup and acclimation procedure  `S2.2` · methods
- ### Physical activity reduction protocol  `S2.3` · methods
- ### Graded maximal running tests  `S2.4` · methods
- ### Food intake  `S2.5` · methods
- ### Bomb calorimetry  `S2.6` · methods
- ### Tissue collection  `S2.7` · methods
- ### Insulin ELISA and HOMA‐IR  `S2.8` · methods
- ### Glycogen determination in skeletal muscle  `S2.9` · methods
- ### RNA isolation  `S2.10` · methods
- ### cDNA library prep and transcriptomics  `S2.11` · methods
- ### Statistics  `S2.12` · methods
- ## RESULTS  `S3` · results
- ### Running capacity  `S3.1` · results
- ### Body mass  `S3.2` · results
- ### Adipose and skeletal muscle mass  `S3.3` · results
- ### Energy intake and absorption  `S3.4` · results
- ### Fasting insulin, glucose, and HOMA‐IR  `S3.5` · results
- ### Muscle glycogen concentrations  `S3.6` · results
- ### Transcriptional adaptations to activity reduction in skeletal muscle  `S3.7` · results
- ## DISCUSSION  `S4` · discussion
- ## CONCLUSION  `S5` · conclusion
- ## AUTHOR CONTRIBUTIONS  `S6` · other
- ## FUNDING INFORMATION  `S7` · other
- ## CONFLICT OF INTEREST STATEMENT  `S8` · other
- ## DATA AVAILABILITY STATEMENT  `DA` · data_availability
- ## Accession mentions

## Metadata (21 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: Treadmill trained 6 weeks: 7; Treadmill trained 4 weeks, inactive 2 weeks: 7; Inactive 6 weeks: 7
- `grp`: ACT: 7; AR: 7; SED: 7

### Constant columns

- `status`: Public on Nov 18 2024
- `submission_date`: Nov 13 2024
- `last_update_date`: Nov 18 2024
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Skeletal muscle (gastrocnemius, medial belly)
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Skeletal muscle (gastrocnemius, medial belly)
- `characteristics_ch1.1.genotype`: C57BL/6NJ
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: The gastrocnemius muscle was freeze clamped immediately upon harvest. The entire medial belly was bead homogenized in trizol and RNA was extracted using chloroform methanol extraction. RNA was then column purified using a Purelink RNA kit.,RNA was sent to Azenta for PolyA cDNA library preparation an ... [12 more characters]
- `data_processing`: Raw files were imported to Galaxy and trimmed using fastp,Trimmed files were aligned to genome assembly GRCm39 using RNA STAR in Galaxy,Reads were mapped in Galaxy using featureCounts,Count normalization was completed using the DESeq2 package in R,Assembly: GRCm39,Supplementary files format and cont ... [141 more characters]
- `platform_id`: GPL24247
- `contact_name`: Erin,J,Stephenson
- `contact_institute`: Midwestern University
- `contact_address`: 555 31st street
- `contact_city`: Downers Grove
- `contact_state`: IL
- `contact_zip/postal_code`: 60515
- `contact_country`: USA
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE281849
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM8631060 | Skeletal muscle, trained, replicate 1 | M304 |
| GSM8631061 | Skeletal muscle, trained, replicate 2 | M305 |
| GSM8631062 | Skeletal muscle, trained, replicate 3 | M306 |
| GSM8631063 | Skeletal muscle, activity reduction, replicate 1 | M307 |
| GSM8631064 | Skeletal muscle, trained, replicate 4 | M308 |
| GSM8631065 | Skeletal muscle, trained, replicate 5 | M309 |
| GSM8631066 | Skeletal muscle, activity reduction, replicate 2 | M310 |
| GSM8631067 | Skeletal muscle, inactive, replicate 1 | M311 |
| GSM8631068 | Skeletal muscle, trained, replicate 6 | M312 |
| GSM8631069 | Skeletal muscle, inactive, replicate 2 | M313 |
| GSM8631070 | Skeletal muscle, activity reduction, replicate 3 | M314 |
| GSM8631071 | Skeletal muscle, inactive, replicate 3 | M315 |
| GSM8631072 | Skeletal muscle, inactive, replicate 4 | M316 |
| GSM8631073 | Skeletal muscle, inactive, replicate 5 | M317 |
| GSM8631074 | Skeletal muscle, activity reduction, replicate 4 | M318 |
| GSM8631075 | Skeletal muscle, trained, replicate 7 | M319 |
| GSM8631076 | Skeletal muscle, activity reduction, replicate 5 | M320 |
| GSM8631077 | Skeletal muscle, activity reduction, replicate 6 | M321 |
| GSM8631078 | Skeletal muscle, activity reduction, replicate 7 | M322 |
| GSM8631079 | Skeletal muscle, inactive, replicate 6 | M323 |
| GSM8631080 | Skeletal muscle, inactive, replicate 7 | M325 |

## Values with exercise words (by column)

- `title`: Skeletal muscle, trained, replicate 1, Skeletal muscle, trained, replicate 2, Skeletal muscle, trained, replicate 3, Skeletal muscle, trained, replicate 4, Skeletal muscle, trained, replicate 5, Skeletal muscle, trained, replicate 6, Skeletal muscle, trained, replicate 7
- `characteristics_ch1.2.treatment`: Treadmill trained 4 weeks, inactive 2 weeks, Treadmill trained 6 weeks
- `grp`: SED

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.2.treatment | 7 | 21/21 | 7 | 0 |
| suffix of title | grp | 7 | 21/21 | 7 | 0 |
| grp (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 21 | 0/21 | 0 | 0 |
| characteristics_ch1.2.treatment (without grp) + suffix of title | grp | 21 | 0/21 | 0 | 0 |
| title without the characteristics_ch1.2.treatment level | characteristics_ch1.2.treatment | 10 | 8/21 | 0 | 2 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 21, "same_key_mean_r": 0.103, "other_mean_r": -0.019, "difference": 0.122, "permutation_p": 0.038980509745127435, "genes_used": 8034, "status": "not_supported"}
