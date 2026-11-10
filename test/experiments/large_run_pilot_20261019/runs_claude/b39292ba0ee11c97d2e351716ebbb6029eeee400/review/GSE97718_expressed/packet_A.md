# Review packet A (facts only): GSE97718_expressed

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC5647435.paper.md`

## Paper outline

- # Exercise and high-fat feeding remodel transcript-metabolite interactive networks in mouse skeletal muscle
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### HFD is linked with a gene expression pattern indicative of enhanced lipid catabolism  `S2.1` · results
- ### HFD alters skeletal muscle transcriptome remodelling induced by acute maximal exercise  `S2.2` · results
- ### HFD enhances lipid accumulation and catabolism in skeletal muscle tissue  `S2.3` · results
- ### WACNA characterisation of integrated transcript-metabolite networks  `S2.4` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### Animals  `S4.1` · methods
- ### Body composition  `S4.2` · methods
- ### Oral glucose tolerance test (OGTT)  `S4.3` · methods
- ### Maximal exercise test  `S4.4` · methods
- ### RNA isolation and quantitative PCR (qPCR)  `S4.5` · methods
- ### RNA sequencing (RNA-seq)  `S4.6` · methods
- ### Untargeted metabolomic analysis  `S4.7` · methods
- #### Sample preparation  `S4.7.1` · methods
- #### UHPLC-MS  `S4.7.2` · methods
- #### HILIC-MS  `S4.7.3` · methods
- #### Data processing and statistical analysis  `S4.7.4` · methods
- ### Weighted Analyte Correlation Network Analysis (WACNA)  `S4.8` · methods
- ### Statistical analysis  `S4.9` · methods
- ### Data availability  `S4.10` · data_availability
- ## Electronic supplementary material  `S5` · supplementary
- ### (untitled)  `S5.1` · supplementary
- ## Acknowledgements  `S6` · other
- ## Author Contributions  `S7` · other
- ## (untitled)  `S8` · other
- ### Competing Interests  `S8.1` · other
- ## Contributor Information  `S10` · other
- ## Accession mentions

## Metadata (16 samples)

### Grouping columns (level: count)

- `grp`: CONpre: 4; HFDpre: 4; CONpost: 4; HFDpost: 4

### Constant columns

- `status`: Public on Oct 31 2017
- `submission_date`: Apr 12 2017
- `last_update_date`: May 15 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Skeletal muscle (quadriceps)
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: C57BL/6NTac
- `characteristics_ch1.1.tissue`: Skeletal muscle
- `characteristics_ch1.2.age`: 16 weeks
- `molecule_ch1`: polyA RNA
- `extract_protocol_ch1`: Muscles samples were collected from anesthetized (2.5 % isoflurane) mice under basal conditions or 3 h after maximal exercise. RNA extraction was performed using RNeasy Mini Kit (QIAGEN, #74104).,Libraries were prepared with TruSeq Stranded mRNA Library Prep Kit (Illumina). Sequencing was performed  ... [31 more characters]
- `data_processing`: Reads were trimmed to remove adapter sequences and quality checked using fastqc software (http://www.bioinformatics.babraham.ac.uk/projects/fastqc/).,Reads were aligned using TopHat to mm9 version of the mouse genome (Trapnell et al., 2009).,The expression level of genes and comparison between diffe ... [227 more characters]
- `platform_id`: GPL17021
- `contact_name`: Joaqu铆n,,P茅rez-Schindler
- `contact_email`: j.perezschindler@unibas.ch
- `contact_department`: Biozentrum
- `contact_institute`: University of Basel
- `contact_address`: Klingelbergstrasse 50 / 70
- `contact_city`: Basel
- `contact_zip/postal_code`: 4056
- `contact_country`: Switzerland
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE97718
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`

### Samples

| sample | title |
|---|---|
| GSM2576093 | CON-pre 1 |
| GSM2576094 | CON-pre 2 |
| GSM2576095 | CON-pre 3 |
| GSM2576096 | CON-pre 4 |
| GSM2576097 | HFD-pre 1 |
| GSM2576098 | HFD-pre 2 |
| GSM2576099 | HFD-pre 3 |
| GSM2576100 | HFD-pre 4 |
| GSM2576101 | CON-post 1 |
| GSM2576102 | CON-post 2 |
| GSM2576103 | CON-post 3 |
| GSM2576104 | CON-post 4 |
| GSM2576105 | HFD-post 1 |
| GSM2576106 | HFD-post 2 |
| GSM2576107 | HFD-post 3 |
| GSM2576108 | HFD-post 4 |

## Values with exercise words (by column)

- `extract_protocol_ch1`: Muscles samples were collected from anesthetized (2.5 % isoflurane) mice under basal conditions or 3 h after maximal exercise. RNA extraction was performed using RNeasy Mini Kit (QIAGEN, #74104).,Libraries were prepared with TruSeq Stranded mRNA Library Prep Kit (Illumina). Sequencing was performed using the HiSeq2500 (Illumina).

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | grp | 4 | 16/16 | 4 | 0 |
| suffix of key | grp | 4 | 16/16 | 4 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 24, "same_key_mean_r": -0.029, "other_mean_r": 0.01, "difference": -0.039, "permutation_p": 0.7971014492753623, "genes_used": 7811, "status": "not_supported"}
