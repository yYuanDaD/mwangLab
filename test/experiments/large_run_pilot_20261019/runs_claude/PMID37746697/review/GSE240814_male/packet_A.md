# Review packet A (facts only): GSE240814_male

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\PMID37746697\PMID37746697_abstract.txt`

## Metadata (41 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: Hindlimb Unloading: 34; Control: 7
- `characteristics_ch1.4.time point`: 48h: 9; 72h: 9; 24h: 8; 168h: 8; 0h: 7
- `trt`: Hindlimb Unloading: 34; Control: 7
- `time`: h48: 9; h72: 9; h24: 8; h168: 8; h0: 7

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
- `characteristics_ch1.3.Sex`: Male
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Gastrocnemius muscles were flash frozen in liquid nitrogen and RNA was isolated using TRIzol and the Zymo MicroPrep Kit and prepared for RNA-sequencing,RNA libraries were prepared for sequencing using standard Illumina protocols
- `description`: HU male_total.xlsx
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
- `sex`: Male

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM7709796 | 41_S36 |
| GSM7709797 | 46_S26 |
| GSM7709798 | 38_S32 |
| GSM7709799 | 37_S30 |
| GSM7709800 | 42_S38 |
| GSM7709801 | 43_S40 |
| GSM7709802 | 39_S34 |
| GSM7709803 | 11_S6 |
| GSM7709804 | 12_S8 |
| GSM7709805 | 14_S10 |
| GSM7709806 | 7_S1 |
| GSM7709807 | 9_S14 |
| GSM7709808 | 15_S12 |
| GSM7709809 | 10_S4 |
| GSM7709810 | 16_S15 |
| GSM7709811 | 17_S2 |
| GSM7709812 | 19_S5 |
| GSM7709813 | 21_S9 |
| GSM7709814 | 20_S7 |
| GSM7709815 | 26_S1 |
| GSM7709816 | 22_S11 |
| GSM7709817 | 25_S16 |
| GSM7709818 | 23_S13 |
| GSM7709819 | 18_S3 |
| GSM7709820 | 34_S25 |
| GSM7709821 | 35_S28 |
| GSM7709822 | 27_S2 |
| GSM7709823 | 32_S7 |
| GSM7709824 | 28_S3 |
| GSM7709825 | 33_S8 |
| GSM7709826 | 31_S6 |
| GSM7709827 | 29_S4 |
| GSM7709828 | 30_S5 |
| GSM7709829 | 53_S39 |
| GSM7709830 | 49_S31 |
| GSM7709831 | 52_S37 |
| GSM7709832 | 48_S29 |
| GSM7709833 | 51_S35 |
| GSM7709834 | 54_S41 |
| GSM7709835 | 55_S27 |
| GSM7709836 | 50_S33 |

## Values with exercise words (by column)

- `characteristics_ch1.2.treatment`: Hindlimb Unloading
- `trt`: Hindlimb Unloading

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.4.time point (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 41 | 0/41 | 0 | 0 |
| time (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 41 | 0/41 | 0 | 0 |
| characteristics_ch1.4.time point (without trt) + suffix of title | trt | 41 | 0/41 | 0 | 0 |
| time (without trt) + suffix of title | trt | 41 | 0/41 | 0 | 0 |
| suffix of title | characteristics_ch1.2.treatment | 33 | 0/41 | 0 | 8 |
| suffix of title | trt | 33 | 0/41 | 0 | 8 |
