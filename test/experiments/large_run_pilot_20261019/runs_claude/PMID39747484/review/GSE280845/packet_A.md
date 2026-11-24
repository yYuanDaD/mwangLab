# Review packet A (facts only): GSE280845

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\PMID39747484\abstract_PMID39747484.txt`

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.genotype`: WT: 6; cFeimin MKO: 6
- `characteristics_ch1.2.treatment`: Sedentary: 6; after 90min running: 6
- `ex`: SED: 6; EXE: 6
- `geno`: WT: 6; KO: 6

### Constant columns

- `status`: Public on Nov 01 2024
- `submission_date`: Nov 01 2024
- `last_update_date`: Nov 01 2024
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: skeletal muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: skeletal muscle
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA extraction was conducted using the GeneMark Total RNA Purification kit.,To assess RNA quality, a NanoDrop ND2000 spectrophotometer from Thermo Scientific was employed. Subsequently, 18 libraries were meticulously prepared by BGI Genomics, and all samples were sequenced on the DNBSEQ platfo ... [3 more characters]
- `data_processing`: The RNA-seq data, consisting of 50-bp single-end reads from the DNBSEQ platform, underwent initial preprocessing, including the removal of adaptor sequences and quality assessment using the FastQC tool (v.0.12.1). Sequencing data were demultiplexed and subjected to primary analysis utilizing SOAPnuk ... [1480 more characters]
- `platform_id`: GPL23479
- `contact_name`: Yiguo,,Wang
- `contact_department`: School of Life Sciences
- `contact_institute`: Tsinghua University
- `contact_address`: Tsinghua University, Haidian District
- `contact_city`: Beijing
- `contact_zip/postal_code`: 100086
- `contact_country`: China
- `instrument_model`: BGISEQ-500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE280845
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM8606518 | Sed_WT_rep1 |
| GSM8606519 | Sed_WT_rep3 |
| GSM8606520 | Sed_WT_rep4 |
| GSM8606521 | Sed_KO_rep1 |
| GSM8606522 | Sed_KO_rep2 |
| GSM8606523 | Sed_KO_rep3 |
| GSM8606524 | Exe_WT_rep3 |
| GSM8606525 | Exe_WT_rep4 |
| GSM8606526 | Exe_WT_rep5 |
| GSM8606527 | Exe_KO_rep1 |
| GSM8606528 | Exe_KO_rep2 |
| GSM8606529 | Exe_KO_rep4 |

## Values with exercise words (by column)

- `title`: Exe_KO_rep1, Exe_KO_rep2, Exe_KO_rep4, Exe_WT_rep3, Exe_WT_rep4, Exe_WT_rep5
- `characteristics_ch1.2.treatment`: Sedentary, after 90min running
- `ex`: EXE, SED

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.1.genotype (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 8 | 8/12 | 4 | 0 |
| geno (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 8 | 8/12 | 4 | 0 |
| title without the ex level | ex | 8 | 8/12 | 4 | 0 |
| characteristics_ch1.1.genotype (without ex) + suffix of title | ex | 8 | 8/12 | 4 | 0 |
| geno (without ex) + suffix of title | ex | 8 | 8/12 | 4 | 0 |
| characteristics_ch1.2.treatment (without characteristics_ch1.1.genotype) + suffix of title | characteristics_ch1.1.genotype | 9 | 6/12 | 3 | 0 |
| ex (without characteristics_ch1.1.genotype) + suffix of title | characteristics_ch1.1.genotype | 9 | 6/12 | 3 | 0 |
| title without the geno level | geno | 9 | 6/12 | 3 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "characteristics_ch1.1.genotype (without characteristics_ch1.2.treatment) + suffix of title", "across": "_across", "within": ["_within"], "n_same_key_pairs": 4, "same_key_mean_r": -0.023, "other_mean_r": 0.006, "difference": -0.028, "permutation_p": 0.6371814092953523, "genes_used": 7570, "status": "not_supported"}
