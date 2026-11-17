# Review packet A (facts only): GSE58608

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC4622000.paper.md`

## Paper outline

- # An integrative analysis reveals coordinated reprogramming of the epigenome and the transcriptome in human skeletal muscle after training
- ## Abstract  `ABS` · abstract
- ## Abbreviations  `S1` · other
- ## Introduction  `S2` · introduction
- ## Results  `S3` · results
- ### Endurance exercise training induces global alterations in DNA methylation  `S3.1` · results
- ### Enrichment of training-induced DMPs in enhancers  `S3.2` · results
- ### Differential methylation is related to genes governing muscle related processes  `S3.3` · results
- ### Specific differential methylation correlates with expression changes in an exercise-dependent manner  `S3.4` · results
- ### Integrating transcriptional network analysis with DNA methylation identifies a coordinated training response  `S3.5` · results
- ## Discussion  `S4` · discussion
- ## Materials and Methods  `S5` · methods
- ### Human physiological measurements  `S5.1` · methods
- ### DNA methylation methods  `S5.2` · methods
- ### Bioinformatics analysis of DNA methylation data  `S5.3` · methods
- ### RNA sequencing  `S5.4` · methods
- ### Integration between DNA methylation and transcriptomics  `S5.5` · methods
- ### Data availability  `S5.6` · data_availability
- ## Disclosure of Potential Conflicts of Interest  `BK1` · other
- ## Acknowledgments  `BK2` · other
- ## Funding  `BK3` · other
- ## Author Contributions  `BK4` · other
- ## Supplemental Material  `BK5` · supplementary
- ## Accession mentions

## Metadata (24 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.gender`: female: 12; male: 12
- `characteristics_ch1.3.biopsy location`: right leg: 12; left leg: 12
- `subject`: s11: 2; s12: 2; s13: 2; s15: 2; s16: 2; s18: 2; s19: 2; s20: 2; s21: 2; s04: 2; s07: 2; s09: 2
- `grp`: T1: 12; U1: 12

### Constant columns

- `status`: Public on Jul 15 2014
- `submission_date`: Jun 18 2014
- `last_update_date`: May 15 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: skeletal muscle
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: skeletal muscle
- `characteristics_ch1.2.exercise status`: untrained
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Trizol庐 method,RNA libraries were prepared for sequencing using standard Illumina protocols for paired end sequencing and clustered on cBot
- `data_processing`: Bcl to Fastq conversion was performed using bcl2Fastq v1.8.3 from the CASAVA software suite,The paired-end reads were trimmed with respect to quality and remaining adapter sequences using Trim Galore and aligned to the human genome reference hg19 (ENSEMBL v71) with TopHat version 2.0.4,The aligned r ... [201 more characters]
- `platform_id`: GPL11154
- `contact_name`: Joakim,,Lundeberg
- `contact_department`: Gene Technology
- `contact_institute`: KTH-Science for Life Laboratory
- `contact_address`: Tomtebodav盲gen 23A
- `contact_city`: Solna
- `contact_zip/postal_code`: 17165
- `contact_country`: Sweden
- `instrument_model`: Illumina HiSeq 2000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE58608,GSE60591
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `characteristics_ch1.4.original sample id`, `characteristics_ch1.5.sample id (used in publication)`, `description`, `relation`, `supplementary_file_1`

### Samples

| sample | title | description |
|---|---|---|
| GSM1415126 | 217 | Sample 1 |
| GSM1415127 | 225 | Sample 2 |
| GSM1415128 | 174 | Sample 3 |
| GSM1415129 | 235 | Sample 4 |
| GSM1415130 | 135 | Sample 5 |
| GSM1415131 | 230 | Sample 6 |
| GSM1415132 | 113 | Sample 7 |
| GSM1415133 | 226 | Sample 8 |
| GSM1415134 | 169 | Sample 9 |
| GSM1415135 | 227 | Sample 10 |
| GSM1415136 | 223 | Sample 11 |
| GSM1415137 | 228 | Sample 12 |
| GSM1415138 | 205 | Sample 13 |
| GSM1415139 | 231 | Sample 14 |
| GSM1415140 | 130 | Sample 15 |
| GSM1415141 | 229 | Sample 16 |
| GSM1415142 | 211 | Sample 17 |
| GSM1415143 | 232 | Sample 18 |
| GSM1415144 | 157 | Sample 19 |
| GSM1415145 | 233 | Sample 20 |
| GSM1415146 | 172 | Sample 21 |
| GSM1415147 | 234 | Sample 22 |
| GSM1415148 | 152 | Sample 23 |
| GSM1415149 | 224 | Sample 24 |

## Values with exercise words (by column)

- `characteristics_ch1.2.exercise status`: untrained

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| subject | characteristics_ch1.3.biopsy location | 12 | 24/24 | 12 | 0 |
| subject | grp | 12 | 24/24 | 12 | 0 |
| characteristics_ch1.4.original sample id without the grp level | grp | 15 | 18/24 | 9 | 0 |
| suffix of title | characteristics_ch1.1.gender | 24 | 0/24 | 0 | 0 |
| characteristics_ch1.3.biopsy location (without characteristics_ch1.1.gender) + suffix of title | characteristics_ch1.1.gender | 24 | 0/24 | 0 | 0 |
| subject (without characteristics_ch1.1.gender) + suffix of title | characteristics_ch1.1.gender | 24 | 0/24 | 0 | 0 |
| grp (without characteristics_ch1.1.gender) + suffix of title | characteristics_ch1.1.gender | 24 | 0/24 | 0 | 0 |
| suffix of description | characteristics_ch1.1.gender | 24 | 0/24 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "subject", "across": "_across", "within": [], "n_same_key_pairs": 12, "same_key_mean_r": 0.273, "other_mean_r": -0.023, "difference": 0.296, "permutation_p": 0.0004997501249375312, "genes_used": 5566, "status": "supported"}
