# Review packet A (facts only): GSE164890

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC9027771.paper.md`

## Paper outline

- # RNA Sequencing of Whole Blood Defines the Signature of High Intensity Exercise at Altitude in Elite Speed Skaters
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## 1. Introduction  `S1` · introduction
- ## 2. Materials and Methods  `S2` · methods
- ### 2.1. Subjects and Study Protocol  `S2.1` · methods
- ### 2.2. Blood Sample Collection and RNA Isolation  `S2.2` · methods
- ### 2.3. Library Preparation and Illumina RNA Sequencing  `S2.3` · methods
- ### 2.4. Alignment and Quantification  `S2.4` · methods
- ### 2.5. Differential Expression and Pathway Enrichment Analysis  `S2.5` · methods
- ### 2.6. Public Single Cell RNA-Seq Dataset Processing  `S2.6` · methods
- ### 2.7. Microarray Dataset Reanalysis  `S2.7` · methods
- ## 3. Results  `S3` · results
- ### 3.1. Blood Panel and Physiological Measurements  `S3.1` · results
- ### 3.2. Differential Gene Expression Analysis  `S3.2` · results
- ### 3.3. Pathway and Functional Category Analysis  `S3.3` · results
- ### 3.4. Analysis of Cell Type Composition Changes Based on Expression Signatures  `S3.4` · results
- ### 3.5. Context of Other Exercise Expression Datasets  `S3.5` · results
- ## 4. Discussion  `S4` · discussion
- ## Supplementary Materials  `S5` · supplementary
- ## Author Contributions  `S6` · other
- ## Funding  `S7` · other
- ## Institutional Review Board Statement  `S8` · other
- ## Informed Consent Statement  `S9` · other
- ## Data Availability Statement  `S10` · data_availability
- ## Conflicts of Interest  `S11` · other
- ## Accession mentions

## Metadata (14 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.time point`: before exercise: 7; after exercise: 7
- `subject`: S1: 2; S2: 2; S3: 2; S4: 2; S5: 2; S6: 2; S7: 2
- `time`: pre: 7; post: 7

### Constant columns

- `status`: Public on Jul 12 2021
- `submission_date`: Jan 15 2021
- `last_update_date`: Jul 12 2021
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: whole blood (globin-depleted)
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: whole blood (globin-depleted)
- `treatment_protocol_ch1`: For each participant, 2.5 mL whole blood sample was collected before and after the exercise using the RNAgard Blood Tubes (Biomatrica, USA) according to the manufacturer鈥檚 protocol and then stored at 鈭20 掳C until further processing.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted from blood using PureLink RNA Mini Kit (Thermo Fisher Scientific, Inc.) and 芦BioMaxi鈩 Precipitation Buffer禄 (Biomatrica, USA), according to the manufacturer鈥檚 protocol. RNA concentration was measured using Quantus Fluorometer TM with QuantiFluor RNA System kit (Promega, USA). ... [874 more characters]
- `data_processing`: Raw sequencing reads were aligned to full human genome and transcriptome using STAR v2.5.3a splice-aware alignment software. Primary part of GRCh38.p10 human genome assembly and Gencode v26 annotation were used to generate the genomic and transcriptomic reference index.,The resulting transcriptome-a ... [463 more characters]
- `platform_id`: GPL20301
- `contact_name`: Alexander,,Predeus
- `contact_email`: predeus@gmail.com
- `contact_phone`: 447472882494
- `contact_institute`: Wellcome Sanger Institute
- `contact_address`: Wellcome Trust Genome Campus
- `contact_city`: Hinxton
- `contact_zip/postal_code`: CB10 1RQ
- `contact_country`: United Kingdom
- `instrument_model`: Illumina HiSeq 4000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE164890
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM5022469 | Skater 1 - before exercise | 1before |
| GSM5022470 | Skater 1 - after exercise | 1after |
| GSM5022471 | Skater 2 - before exercise | 2before |
| GSM5022472 | Skater 2 - after exercise | 2after |
| GSM5022473 | Skater 3 - before exercise | 3before |
| GSM5022474 | Skater 3 - after exercise | 3after |
| GSM5022475 | Skater 4 - before exercise | 4before |
| GSM5022476 | Skater 4 - after exercise | 4after |
| GSM5022477 | Skater 5 - before exercise | 5before |
| GSM5022478 | Skater 5 - after exercise | 5after |
| GSM5022479 | Skater 6 - before exercise | 6before |
| GSM5022480 | Skater 6 - after exercise | 6after |
| GSM5022481 | Skater 7 - before exercise | 7before |
| GSM5022482 | Skater 7 - after exercise | 7after |

## Values with exercise words (by column)

- `title`: Skater 1 - after exercise, Skater 1 - before exercise, Skater 2 - after exercise, Skater 2 - before exercise, Skater 3 - after exercise, Skater 3 - before exercise, Skater 4 - after exercise, Skater 4 - before exercise, Skater 5 - after exercise, Skater 5 - before exercise, Skater 6 - after exercise, Skater 6 - before exercise
- `characteristics_ch1.1.time point`: after exercise, before exercise
- `treatment_protocol_ch1`: For each participant, 2.5 mL whole blood sample was collected before and after the exercise using the RNAgard Blood Tubes (Biomatrica, USA) according to the manufacturer鈥檚 protocol and then stored at 鈭20 掳C until further processing.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.1.time point level | characteristics_ch1.1.time point | 7 | 14/14 | 7 | 0 |
| subject | characteristics_ch1.1.time point | 7 | 14/14 | 7 | 0 |
| subject | time | 7 | 14/14 | 7 | 0 |
