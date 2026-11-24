# Review packet A (facts only): GSE281210

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261028\papers\PMC12607142.paper.md`

## Paper outline

- # Single-cell transcriptome analysis profiles the enlarged subsets of myeloid-biased HSPCs with preleukemic characters in disuse osteoporosis mice
- ## Abstract  `ABS` · abstract
- ## Background  `S1` · introduction
- ## Materials and methods  `S2` · methods
- ### Animal and Hindlimb unloading model  `S2.1` · methods
- ### Flow cytometry for BM cells and peripheral blood  `S2.2` · methods
- ### Peripheral blood cell counting  `S2.3` · methods
- ### Micro-CT analysis  `S2.4` · methods
- ### Colony-forming unit assay  `S2.5` · methods
- ### Bulk RNA-seq of bone marrow cells  `S2.6` · methods
- ### Histochemistry  `S2.7` · methods
- ### Single-cell RNA sequencing and analysis  `S2.8` · methods
- ### RNA isolation and quantitative PCR analysis  `S2.9` · methods
- #### ELISA  `S2.9.1` · methods
- #### Statistical analysis  `S2.9.2` · methods
- ## Results  `S3` · results
- ### Osteoporosis increases myeloid cells in the peripheral blood of mice  `S3.1` · results
- ### Myeloid-biased HSPC pools expanded with impaired differentiation and apoptosis in the bone marrow of OP-HU mice  `S3.2` · results
- ### Bone marrow microenvironment of OP-HU mice supports the expansion of HSC pool and myeloid-biased hematopoiesis  `S3.3` · results
- ### Single cell RNA-seq identifies the specifically expanded subsets of HSPCs in OP-HU mice  `S3.4` · results
- ### The expanded specific subsets of HSPCs in OP-HU mice were characterized with altered transcriptional programs contributed to myeloid-biased hematopoiesis and leukemogenesis  `S3.5` · results
- ### Inhibition of BRD4 partially reverses the tumor cell-like characters of HSCs in OP-HU mice  `S3.6` · results
- ## Discussion  `S4` · discussion
- ## Conclusions  `S5` · conclusion
- ## Supplementary Information  `S6` · supplementary
- ## Author contributions  `BK1` · other
- ## Funding  `BK2` · other
- ## Data availability  `DA` · data_availability
- ## Declarations  `BK3` · other
- ## Accession mentions

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.3.treatment`: : 3; hindlib unloading: 3
- `grp`: Con: 3; HU: 3

### Constant columns

- `status`: Public on Dec 04 2025
- `submission_date`: Nov 06 2024
- `last_update_date`: Dec 04 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: femur
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Bone marrow
- `characteristics_ch1.1.cell type`: Bone marrow cells
- `characteristics_ch1.2.genotype`: WT
- `treatment_protocol_ch1`: Mice were treated with or without hindlimb unloading for four weeks.
- `growth_protocol_ch1`: Freshly isolated bone marrow cells were used for total RNA extraction
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was isolated using TRNzol (DP424, TIANGEN) according to the manufacturer鈥檚 instructions and used for library preparation.,RNA libraries for RNA-seq were prepared using NEBNext庐 Ultra鈩 RNA Library Prep Kit for Illumina庐 following manufacturer's protocols.
- `data_processing`: CASAVA was used for base-calling.,Clean reads were obtained by removing reads containing adapter, reads containing N base and low quality  through in-house perl scripts.,Paired-end clean reads were aligned to the reference genome using Hisat2 (v2.0.5).,featureCounts (v1.5.0-p3) was used to count the ... [149 more characters]
- `platform_id`: GPL24247
- `contact_name`: Chen,,Zhang
- `contact_email`: chenzhanghouston@gmail.com
- `contact_department`: Department of hematology
- `contact_institute`: Tangdu Hospital
- `contact_address`: Xinsi road
- `contact_city`: Xi'an
- `contact_zip/postal_code`: 710038
- `contact_country`: China
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE281210
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`, `_norm_key`

### Samples

| sample | title |
|---|---|
| GSM8614889 | BM control 1 |
| GSM8614890 | BM control 2 |
| GSM8614891 | BM control 3 |
| GSM8614892 | BM OP-HU1 |
| GSM8614893 | BM OP-HU2 |
| GSM8614894 | BM OP-HU3 |

## Values with exercise words (by column)

- `characteristics_ch1.3.treatment`: hindlib unloading
- `treatment_protocol_ch1`: Mice were treated with or without hindlimb unloading for four weeks.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of key | characteristics_ch1.3.treatment | 3 | 6/6 | 3 | 0 |
| suffix of key | grp | 3 | 6/6 | 3 | 0 |
| grp (without characteristics_ch1.3.treatment) + suffix of key | characteristics_ch1.3.treatment | 6 | 0/6 | 0 | 0 |
| characteristics_ch1.3.treatment (without grp) + suffix of key | grp | 6 | 0/6 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of key", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": -0.039, "other_mean_r": 0.019, "difference": -0.058, "permutation_p": 0.6691654172913544, "genes_used": 9929, "status": "not_supported"}
