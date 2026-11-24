# Review packet A (facts only): GSE240814_female

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\PMID37746697\PMID37746697_abstract.txt`

## Metadata (39 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: Hindlimb Unloading: 31; Control: 8
- `characteristics_ch1.4.time point`: 0h: 8; 24h: 8; 48h: 8; 72h: 8; 168h: 7
- `trt`: Hindlimb Unloading: 31; Control: 8
- `time`: h0: 8; h24: 8; h48: 8; h72: 8; h168: 7

### Constant columns

- `status`: Public on Sep 21 2023
- `submission_date`: Aug 14 2023
- `last_update_date`: Sep 21 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Skeletal muscle Gastrocnemius
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Skeletal muscle Gastrocnemius
- `characteristics_ch1.1.genotype`: C57BL6/J
- `characteristics_ch1.3.Sex`: Female
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Gastrocnemius muscles were flash frozen in liquid nitrogen and RNA was isolated using TRIzol and the Zymo MicroPrep Kit and prepared for RNA-sequencing,RNA libraries were prepared for sequencing using standard Illumina protocols
- `description`: HU female_total.xlsx
- `data_processing`: Sequenced reads were mapped to mm10 mouse genome assembly using STAR 2.7.8a with default parameters.,Aligned reads were quantified for gene counts, filtered to exclude genes  with high noise or a maximum count of less than or equal to 50.,The filtered counts were median ratio normalized and tested f ... [251 more characters]
- `platform_id`: GPL21103
- `contact_name`: Stavroula,,Tsitkanou
- `contact_email`: st060@uark.edu
- `contact_laboratory`: Cachexia Laboratory
- `contact_institute`: University of Arkansas
- `contact_address`: 155 North Stadium Drive
- `contact_city`: Fayetteville
- `contact_state`: AR
- `contact_zip/postal_code`: 72701
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 4000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE240814
- `data_row_count`: 0
- `sex`: Female

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM7709837 | H93_S12 |
| GSM7709838 | H95_S15 |
| GSM7709839 | H91_S10 |
| GSM7709840 | H90_S9 |
| GSM7709841 | H92_S11 |
| GSM7709842 | H99r_S14 |
| GSM7709843 | H94_S13 |
| GSM7709844 | H97_S16 |
| GSM7709845 | H69_S48 |
| GSM7709846 | H61_S30 |
| GSM7709847 | H65_S36 |
| GSM7709848 | H67_S42 |
| GSM7709849 | H68_S45 |
| GSM7709850 | H60_S27 |
| GSM7709851 | H63_S33 |
| GSM7709852 | H66_S39 |
| GSM7709853 | H72_S3 |
| GSM7709854 | H76_S7 |
| GSM7709855 | H73_S4 |
| GSM7709856 | H79r_S5 |
| GSM7709857 | H70_S1 |
| GSM7709858 | H74_S6 |
| GSM7709859 | H71_S2 |
| GSM7709860 | H78_S8 |
| GSM7709861 | H85_S18 |
| GSM7709862 | H82_S9 |
| GSM7709863 | H81_S6 |
| GSM7709864 | H87_S21 |
| GSM7709865 | H83_S12 |
| GSM7709866 | H84_S15 |
| GSM7709867 | H80_S3 |
| GSM7709868 | H88_S24 |
| GSM7709869 | H109_S62 |
| GSM7709870 | H104_S56 |
| GSM7709871 | H108_S60 |
| GSM7709872 | H100_S50 |
| GSM7709873 | H105_S58 |
| GSM7709874 | H102_S54 |
| GSM7709875 | H101_S52 |

## Values with exercise words (by column)

- `characteristics_ch1.2.treatment`: Hindlimb Unloading
- `trt`: Hindlimb Unloading

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.4.time point (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 39 | 0/39 | 0 | 0 |
| time (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 39 | 0/39 | 0 | 0 |
| characteristics_ch1.4.time point (without trt) + suffix of title | trt | 39 | 0/39 | 0 | 0 |
| time (without trt) + suffix of title | trt | 39 | 0/39 | 0 | 0 |
| suffix of title | characteristics_ch1.2.treatment | 34 | 6/39 | 3 | 2 |
| suffix of title | trt | 34 | 6/39 | 3 | 2 |
