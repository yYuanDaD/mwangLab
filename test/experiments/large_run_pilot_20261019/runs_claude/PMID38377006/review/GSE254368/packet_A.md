# Review packet A (facts only): GSE254368

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\PMID38377006\abstract_PMID38377006.txt`

## Metadata (20 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.Sex`: male: 10; female: 10
- `characteristics_ch1.2.time point`: Pre: 10; Post: 10
- `characteristics_ch1.4.treatment`: Pre-acute resistance exercise: 10; Post-acute resistance exercise: 10
- `sex`: male: 10; female: 10
- `subject`: m1: 2; m12: 2; m17: 2; m33: 2; m39: 2; f3: 2; f2: 2; f4: 2; f34: 2; f35: 2
- `time`: pre: 10; post: 10

### Constant columns

- `status`: Public on Jan 27 2025
- `submission_date`: Jan 28 2024
- `last_update_date`: Jan 27 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Blood Plasma
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: Blood Plasma
- `characteristics_ch1.3.condition`: Acute resistance exercise
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: RNA extraction using Plasma/Serum Exosome Purification and RNA Isolation Mini Kit (Norgen Biotek Corp., 55000; Thorold, ON, Canada), according to manufacturer's instructions,Single-end libraries constructed from EV RNA using TruSeq Small RNA library kit from Illumina according to manufacturer's reco ... [34 more characters]
- `data_processing`: Quality control completed with bcl2fastq.gz from Illumina, no trimming required,Reads were mapped to the designated reference genome (miRbase_v22) using Ensembl release 101 primary assembly with STAR version 2.5.1a,Differential gene expression analysis was performed using the edgeR workflow,Assembly ... [150 more characters]
- `platform_id`: GPL21697
- `contact_name`: WILLIAM,,CONKRIGHT
- `contact_email`: wrc16@pitt.edu
- `contact_phone`: 2108961127
- `contact_institute`: US Army
- `contact_address`: 2938 73rd Avenue Ct W
- `contact_city`: University Place
- `contact_state`: WA
- `contact_zip/postal_code`: 98466-4223
- `contact_country`: USA
- `instrument_model`: NextSeq 550
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE254368
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM8041095 | Plasma, pre acute, Male 1 | sample.bn5_m1_pre |
| GSM8041096 | Plasma, post acute, Male 1 | sample.bn6_m1_pwo |
| GSM8041097 | Plasma, pre acute, Male 2 | sample.bn7_m12_pre |
| GSM8041098 | Plasma, post acute, Male 2 | sample.bn8_m12_pwo |
| GSM8041099 | Plasma, pre acute, Male 3 | sample.bn9_m17_pre |
| GSM8041100 | Plasma, post acute, Male 3 | sample.bn10_m17_pwo |
| GSM8041101 | Plasma, pre acute, Male 4 | sample.bn11_m33_pre |
| GSM8041102 | Plasma, post acute, Male 4 | sample.bn12_m33_pwo |
| GSM8041103 | Plasma, pre acute, Male 5 | sample.bn13_m39_pre |
| GSM8041104 | Plasma, post acute, Male 5 | sample.bn14_m39_pwo |
| GSM8041105 | Plasma, pre acute, Female 1 | sample.bn15_f3_pre |
| GSM8041106 | Plasma, post acute, Female 1 | sample.bn16_f3_pwo |
| GSM8041107 | Plasma, pre acute, Female 2 | sample.bn17_f2_pre |
| GSM8041108 | Plasma, post acute, Female 2 | sample.bn18_f2_pwo |
| GSM8041109 | Plasma, pre acute, Female 3 | sample.bn19_f4_pre |
| GSM8041110 | Plasma, post acute, Female 3 | sample.bn20_f4_pwo |
| GSM8041111 | Plasma, pre acute, Female 4 | sample.bn21_f34_pre |
| GSM8041112 | Plasma, post acute, Female 4 | sample.bn22_f34_pwo |
| GSM8041113 | Plasma, pre acute, Female 5 | sample.bn23_f35_pre |
| GSM8041114 | Plasma, post acute, Female 5 | sample.bn24_f35_pwo |

## Values with exercise words (by column)

- `characteristics_ch1.3.condition`: Acute resistance exercise
- `characteristics_ch1.4.treatment`: Post-acute resistance exercise, Pre-acute resistance exercise

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.1.Sex level | characteristics_ch1.1.Sex | 10 | 20/20 | 10 | 0 |
| characteristics_ch1.2.time point (without characteristics_ch1.1.Sex) + suffix of title | characteristics_ch1.1.Sex | 10 | 20/20 | 10 | 0 |
| characteristics_ch1.4.treatment (without characteristics_ch1.1.Sex) + suffix of title | characteristics_ch1.1.Sex | 10 | 20/20 | 10 | 0 |
| time (without characteristics_ch1.1.Sex) + suffix of title | characteristics_ch1.1.Sex | 10 | 20/20 | 10 | 0 |
| title without the characteristics_ch1.2.time point level | characteristics_ch1.2.time point | 10 | 20/20 | 10 | 0 |
| characteristics_ch1.1.Sex (without characteristics_ch1.2.time point) + suffix of title | characteristics_ch1.2.time point | 10 | 20/20 | 10 | 0 |
| sex (without characteristics_ch1.2.time point) + suffix of title | characteristics_ch1.2.time point | 10 | 20/20 | 10 | 0 |
| subject (without characteristics_ch1.2.time point) + suffix of title | characteristics_ch1.2.time point | 10 | 20/20 | 10 | 0 |
