# Review packet A (facts only): GSE126001

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC9731977.paper.md`

## Paper outline

- # Genome-wide analysis of a cellular exercise model based on electrical pulse stimulation
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### The EPS-based in silico model can predict the effect of in vivo exercise  `S2.1` · results
- ### In vitro exercise mimics in vivo exercise  `S2.2` · results
- ### Identification of a putative myokine  `S2.3` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### Cell culture  `S4.1` · methods
- ### Electrical pulse stimulation  `S4.2` · methods
- ### Immunofluorescence  `S4.3` · methods
- ### RNA isolation  `S4.4` · methods
- ### Library preparation and sequencing  `S4.5` · methods
- ### Transcriptome profiling  `S4.6` · methods
- ### Upstream regulator analysis  `S4.7` · methods
- ### Development of the prediction model  `S4.8` · methods
- ### Publicly available in vivo exercise datasets  `S4.9` · methods
- ### Quantitative RT-PCR  `S4.10` · methods
- ### Animal experiments  `S4.11` · methods
- ### Enzyme-linked immunosorbent assay  `S4.12` · methods
- ### Statistical analysis  `S4.13` · methods
- ### Ethics declarations  `S4.14` · methods
- ## Supplementary Information  `S5` · supplementary
- ### (untitled)  `S5.1` · supplementary
- ## Supplementary Information  `BK1` · supplementary
- ## Author contributions  `BK2` · other
- ## Data availability  `DA` · data_availability
- ## Competing interests  `BK3` · other
- ## Accession mentions

## Metadata (16 samples)

### Grouping columns (level: count)

- `characteristics_ch1.3.genotype`: wild type: 8; Il13-/-: 8
- `characteristics_ch1.4.treatment`: Untrained: 8; 5 weeks endurance exercise: 8
- `geno`: WT: 8; KO: 8
- `train`: UT: 8; TR: 8

### Constant columns

- `status`: Public on Jun 01 2020
- `submission_date`: Feb 01 2019
- `last_update_date`: Jun 01 2020
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Gastrocnemius
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: C57Bl6/J
- `characteristics_ch1.1.gender`: male
- `characteristics_ch1.2.age`: 20-weeks old
- `characteristics_ch1.5.tissue`: gastrocnemius muscle
- `treatment_protocol_ch1`: WT or Il13-/- mice were untrained (control) or endurance exercise trained for 5 weeks by daily treadmill running.
- `growth_protocol_ch1`: All animals were 20-week old male C57Bl6/J mice.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Gastrocnemius muscles were removed, flash frozen in liquid nitrogen, and RNA was harvested using Trizol reagent.,RNA libraries were prepared for sequencing using Illumina鈥檚 TruSeq Stranded mRNA Library Preparation Kit based on the Kit鈥檚 manual. 2 ug total RNA was used as input.
- `data_processing`: Trimming of Illumina adapters (CLC Genomics Workbench v.10 ),Quality control for individual samples (CLC Genomics Workbench v.10 ),Mapping against the reference genome (CLC Genomics Workbench v.10 ),Calculation of expression values using unique matches (CLC Genomics Workbench v.10),Normalization by  ... [197 more characters]
- `platform_id`: GPL19057
- `contact_name`: Nelson,Howard,Knudsen
- `contact_email`: nknudsen@fas.harvard.edu
- `contact_laboratory`: Chih-Hao Lee
- `contact_department`: Genetics and Complex Diseases
- `contact_institute`: Harvard T. H. Chan School of Public Health
- `contact_address`: 655 Huntington Avenue
- `contact_city`: Boston
- `contact_state`: MA
- `contact_zip/postal_code`: 2115
- `contact_country`: USA
- `instrument_model`: NextSeq 500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE126001
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `characteristics_ch1.6.mouse id`, `relation`

### Samples

| sample | title |
|---|---|
| GSM3587593 | WT_Untrained1 |
| GSM3587594 | WT_Untrained2 |
| GSM3587595 | WT_Untrained3 |
| GSM3587596 | WT_Untrained4 |
| GSM3587597 | WT_Trained1 |
| GSM3587598 | WT_Trained2 |
| GSM3587599 | WT_Trained3 |
| GSM3587600 | WT_Trained4 |
| GSM3587601 | Il13-KO_Untrained1 |
| GSM3587602 | Il13-KO_Untrained2 |
| GSM3587603 | Il13-KO_Untrained3 |
| GSM3587604 | Il13-KO_Untrained4 |
| GSM3587605 | Il13-KO_Trained1 |
| GSM3587606 | Il13-KO_Trained2 |
| GSM3587607 | Il13-KO_Trained3 |
| GSM3587608 | Il13-KO_Trained4 |

## Values with exercise words (by column)

- `characteristics_ch1.4.treatment`: 5 weeks endurance exercise, Untrained
- `treatment_protocol_ch1`: WT or Il13-/- mice were untrained (control) or endurance exercise trained for 5 weeks by daily treadmill running.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| none | | | | | |
