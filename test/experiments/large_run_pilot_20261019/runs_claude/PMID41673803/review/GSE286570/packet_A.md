# Review packet A (facts only): GSE286570

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC12998337.paper.md`

## Paper outline

- # Multi-omics analysis of the gut-liver axis revealed the effects of different exercise interventions in NAFLD mice
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Exercise reduces HFD-induced hepatic steatosis and liver damage  `S2.1` · results
- ### Exercise enhances intestinal barrier integrity and function  `S2.2` · results
- ### Exercise modulates the gut microbiome’s composition and structure  `S2.3` · results
- ### Identification of exercise-related gut microbiota in hepatic steatosis  `S2.4` · results
- ### Exercise restores gut microbiota metabolism in NAFLD mice  `S2.5` · results
- ### Exercise reverses HFD-induced changes in liver gene expression  `S2.6` · results
- ### Correlation between exercise-recovered gut microbiota biomarkers and liver DEGs  `S2.7` · results
- ## Discussion  `S3` · discussion
- ## Conclusion  `S4` · conclusion
- ### Methodology details  `S4.1` · conclusion
- #### Animals and experimental diets  `S4.1.1` · conclusion
- #### Exercise protocol  `S4.1.2` · conclusion
- ### Biochemical assays  `S4.2` · conclusion
- ### Histological examination  `S4.3` · conclusion
- ### Quantitative RT-PCR  `S4.4` · conclusion
- ### RNA sequencing and data analysis  `S4.5` · conclusion
- ### Faecal microbiome sequencing and analysis  `S4.6` · conclusion
- ### Statistical analysis  `S4.7` · conclusion
- ## Supplementary Information  `S5` · supplementary
- ## Authors’ contributions  `BK1` · other
- ## Funding  `BK2` · other
- ## Data availability  `DA` · data_availability
- ## Declarations  `BK3` · other
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.genotype`: NC: 3; HFD: 3; HFD+AE: 3; HFD+RE: 3
- `characteristics_ch1.2.treatment`: NC: 3; HFD: 3; HFD+AE: 3; HFD+RE: 3
- `grp`: NC: 3; HFD: 3; HAE: 3; HRE: 3

### Constant columns

- `status`: Public on Jan 16 2025
- `submission_date`: Jan 13 2025
- `last_update_date`: Jan 16 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Liver
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Liver
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: RNA was harvested using RNApure Tissue&Cell Kit (CWBIO). 2ug of total RNA was used for the construction of sequencing libraries.,RNA libraries for RNA-seq were prepared using Fast RNA-seq Lib Pre Kit V2 (ABclonal) following manufacturer's protocols.
- `data_processing`: Adapters and low-quality bases were removed with Fastp (version 0.23.4, https://github.com/OpenGene/fastp) using the following parameters: 鈥-f 10 -F 10 -l 30 --adapter_sequence AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC --adapter_sequence_r2 AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT鈥.,The cleaned RNA-seq reads were ... [563 more characters]
- `platform_id`: GPL28330
- `contact_name`: Mingliang Wei,,Mingliang Wei
- `contact_phone`: 15535363169
- `contact_institute`: Wuhan University
- `contact_address`: 299 Bayi Road, Wuchang District
- `contact_city`: Wuhan
- `contact_state`: Hubei
- `contact_zip/postal_code`: 430070
- `contact_country`: China
- `instrument_model`: DNBSEQ-T7
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE286570
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `_norm_key`

### Samples

| sample | title | description |
|---|---|---|
| GSM8729503 | H-NC-2 | Library name: H-NC-2 |
| GSM8729504 | H-NC-4 | Library name: H-NC-4 |
| GSM8729505 | H-NC-5 | Library name: H-NC-5 |
| GSM8729506 | H-HFD-1 | Library name: H-HFD-1 |
| GSM8729507 | H-HFD-2 | Library name: H-HFD-2 |
| GSM8729508 | H-HFD-3 | Library name: H-HFD-3 |
| GSM8729509 | H-AE-1 | Library name: H-AE-1 |
| GSM8729510 | H-AE-2 | Library name: H-AE-2 |
| GSM8729511 | H-AE-3 | Library name: H-AE-3 |
| GSM8729512 | H-RE-3 | Library name: H-RE-3 |
| GSM8729513 | H-RE-4 | Library name: H-RE-4 |
| GSM8729514 | H-RE-5 | Library name: H-RE-5 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.1.genotype | 5 | 12/12 | 0 | 0 |
| suffix of description | characteristics_ch1.1.genotype | 5 | 12/12 | 0 | 0 |
| suffix of title | characteristics_ch1.2.treatment | 5 | 12/12 | 0 | 0 |
| suffix of description | characteristics_ch1.2.treatment | 5 | 12/12 | 0 | 0 |
| suffix of title | grp | 5 | 12/12 | 0 | 0 |
| suffix of description | grp | 5 | 12/12 | 0 | 0 |
| title without the characteristics_ch1.1.genotype level | characteristics_ch1.1.genotype | 11 | 2/12 | 0 | 0 |
| grp (without characteristics_ch1.1.genotype) + suffix of title | characteristics_ch1.1.genotype | 11 | 2/12 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 9, "same_key_mean_r": -0.083, "other_mean_r": 0.01, "difference": -0.093, "permutation_p": 0.7496251874062968, "genes_used": 8497, "status": "not_supported"}
