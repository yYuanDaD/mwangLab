# Review packet A (facts only): GSE250520

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC9350263.paper.md`

## Paper outline

- # Human cardiac organoids to model COVID‐19 cytokine storm induced cardiac injuries
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## INTRODUCTION  `S1` · introduction
- ## RESULTS  `S2` · results
- ### RNA seq analysis of IL‐1β treated hCOs established their transcriptomic relevance with COVID‐19 hearts  `S2.1` · results
- ### IL‐1β treated hCOs recapitulated cytokine profile from severe COVID‐19 patient serum  `S2.2` · results
- ### IL‐1β treated hCOs showed reduced cardiac function and pathological cardiac fibrosis  `S2.3` · results
- ### IL‐1β treated hCOs showed prothrombotic vasculature  `S2.4` · results
- ### IL‐1β treated hCOs are a viable platform to test immunomodulatory drugs  `S2.5` · results
- ### IL‐1β treated hCOs provide a valid platform for recovery studies  `S2.6` · results
- ## DISCUSSION  `S3` · discussion
- ## CONCLUSIONS  `S4` · conclusion
- ## METHODS  `S5` · methods
- ## AUTHOR CONTRIBUTIONS  `S6` · other
- ## CONFLICT OF INTEREST  `S7` · other
- ## Supporting information  `S8` · supplementary
- ## DATA AVAILABILITY STATEMENT  `DA` · data_availability

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.3.treatment`: control: 3; IL-1 cytokine: 3
- `trt`: VEH: 3; IL1B: 3

### Constant columns

- `status`: Public on Dec 20 2023
- `submission_date`: Dec 18 2023
- `last_update_date`: Dec 20 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: cardiac organoids
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: cardiac organoids
- `characteristics_ch1.1.cell line`: hiPSC-CM donor 01434
- `characteristics_ch1.2.cell type`: CM, Fb, EC, PC
- `treatment_protocol_ch1`: IL1B treatment went for 4 days
- `growth_protocol_ch1`: organoids were fabricated and devoped for 4 days and then treated with IL1B for 4 days.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: 30-35 organoids were collected immediately out of culture and put in lysis buffer on D10 (2 days after last media change) Total RNA was extracted with an Omega bio-tek E.Z.N.A Total RNA kit,125 ng of total RNA was used for the construction of the library using the New England Biolabs NEBNext庐 Poly(A ... [408 more characters]
- `data_processing`: Paired-end reads (fastq) were aligned to the hg38 human reference genome (Genecode GRCh38.p13) using RNA STAR [doi: 10.1093/bioinformatics/bts635] (v2.7.8a) utilizing the Galaxy Project online platform (v21.01, https://galaxyproject.org/).,gene counts were generated using htseq-count (v13.5) utilizi ... [419 more characters]
- `platform_id`: GPL24676
- `contact_name`: Dimitrios,,Arhontoulis
- `contact_email`: arhontou@musc.edu
- `contact_phone`: 6094574870
- `contact_laboratory`: Mei
- `contact_department`: Bioengineering
- `contact_institute`: MUSC
- `contact_address`: 68 President St
- `contact_city`: Charleston
- `contact_state`: South Carolina
- `contact_zip/postal_code`: 29425
- `contact_country`: USA
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE250520
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `key`

### Samples

| sample | title |
|---|---|
| GSM7980854 | cardiac organoids, Vehicle.1 |
| GSM7980855 | cardiac organoids, Vehicle.2 |
| GSM7980856 | cardiac organoids, Vehicle.3 |
| GSM7980857 | cardiac organoids, IL1bOrgs.1 |
| GSM7980858 | cardiac organoids, IL1bOrgs.2 |
| GSM7980859 | cardiac organoids, IL1bOrgs.3 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.3.treatment | 3 | 6/6 | 3 | 0 |
| suffix of key | characteristics_ch1.3.treatment | 3 | 6/6 | 3 | 0 |
| suffix of title | trt | 3 | 6/6 | 3 | 0 |
| suffix of key | trt | 3 | 6/6 | 3 | 0 |
| trt (without characteristics_ch1.3.treatment) + suffix of title | characteristics_ch1.3.treatment | 6 | 0/6 | 0 | 0 |
| trt (without characteristics_ch1.3.treatment) + suffix of key | characteristics_ch1.3.treatment | 6 | 0/6 | 0 | 0 |
| characteristics_ch1.3.treatment (without trt) + suffix of title | trt | 6 | 0/6 | 0 | 0 |
| characteristics_ch1.3.treatment (without trt) + suffix of key | trt | 6 | 0/6 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": -0.466, "other_mean_r": 0.249, "difference": -0.715, "permutation_p": 1.0, "genes_used": 10693, "status": "not_supported"}
