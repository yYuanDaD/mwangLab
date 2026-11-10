# Review packet A (facts only): GSE263838

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMID38766755.paper.md`

## Paper outline

- # The interactive effect of sustained sleep restriction and resistance exercise on skeletal muscle 1 transcriptomics in young females 2
- ## (untitled)  `S0` · other
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## METHODS  `S2` · methods
- ### Participants  `S2.1` · methods
- ### Study protocol overview  `S2.2` · methods
- ### Measures  `S2.3` · methods
- ### Sleep  `S2.4` · methods
- ### Resistance exercise 172  `S2.5` · methods
- ### Hormone sampling and analysis 179  `S2.6` · methods
- ### RNA extraction and quantification 184  `S2.7` · methods
- ### RNA sequencing and analysis  `S2.8` · methods
- ### Gene enrichment analysis  `S2.9` · methods
- ### Multi-contrast enrichment analysis  `S2.10` · methods
- ### Protein extraction and western blotting  `S2.11` · methods
- ### Statistical analysis  `S2.12` · methods
- ## Results 273  `S3` · results
- ### Participants 274  `S3.1` · results
- ### Sleep  `S3.2` · results
- ### Effect of sleep on the skeletal muscle transcriptomic response to exercise  `S3.3` · results
- ## Discussion  `S4` · discussion

## Metadata (38 samples)

### Grouping columns (level: count)

- `characteristics_ch1.3.age of_donor`: 19: 10; 32: 8; 25: 4; 24: 4; 23: 4; 21: 2; 22: 2; 20: 2; 28: 2
- `characteristics_ch1.4.treatment`: SLEEP: 19; CON: 19
- `characteristics_ch1.5.day of_collection`: 3: 19; 9: 19
- `subject`: ANLI: 4; ELLI: 4; GEDA: 4; GEKN: 4; HABA: 4; JEHA: 4; KISZ: 4; NACR: 4; TATU: 4; SASY: 2
- `cond`: SR: 19; NS: 19
- `day`: D3: 19; D9: 19
- `grp`: SR_D3: 10; NS_D9: 10; SR_D9: 9; NS_D3: 9

### Constant columns

- `status`: Public on Apr 12 2025
- `submission_date`: Apr 12 2024
- `last_update_date`: Apr 12 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: vastus lateralis muscle
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: vastus lateralis muscle
- `characteristics_ch1.1.cell type`: Skeletal Muscle
- `characteristics_ch1.2.Sex`: Female
- `treatment_protocol_ch1`: Ten healthy females aged 18-35 years undertook a randomised cross-over study of nine nights鈥 sleep restriction (SR; 5-h time in bed) and normal sleep (NS; 鈮7 h time in bed) with a minimum 6-week washout. Participants completed four REx sessions per trial  (day 3, 5, 7 and 9). Muscle biopsies were co ... [42 more characters]
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: RNA was extracted using AllPrep RNA/RNA/miRNA universal kit (Qiagen) according to manufacturer instructions,Illumina TruSeq Stranded Total RNA with Ribo-Zero Gold protocol
- `data_processing`: Reads underwent quality check with FastQC (v0.11.9); Kallisto (v0.46.1) was used to map reads to the human reference genome (HomoSapien GRCh38) and to generate transcript counts.,Assembly: HomoSapien GRCh38,Supplementary files format and content: 3col.tsv- Long format of aligned raw gene counts,Supp ... [101 more characters]
- `platform_id`: GPL24676
- `contact_name`: Danielle,,Hiam
- `contact_email`: danielle.hiam@deakin.edu.au
- `contact_department`: IPAN
- `contact_institute`: Deakin University
- `contact_address`: 221 Burwood Hwy
- `contact_city`: Burwood
- `contact_state`: Vic
- `contact_zip/postal_code`: 3125
- `contact_country`: Australia
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE263838
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM8199907 | ANLI1 |
| GSM8199908 | ANLI3 |
| GSM8199909 | ANLI5 |
| GSM8199910 | ANLI7 |
| GSM8199911 | ELLI1 |
| GSM8199912 | ELLI3 |
| GSM8199913 | ELLI5 |
| GSM8199914 | ELLI7 |
| GSM8199915 | GEDA1 |
| GSM8199916 | GEDA3 |
| GSM8199917 | GEDA5 |
| GSM8199918 | GEDA7 |
| GSM8199919 | GEKN1 |
| GSM8199920 | GEKN3 |
| GSM8199921 | GEKN5 |
| GSM8199922 | GEKN7 |
| GSM8199923 | HABA1 |
| GSM8199924 | HABA3 |
| GSM8199925 | HABA5 |
| GSM8199926 | HABA7 |
| GSM8199927 | JEHA1 |
| GSM8199928 | JEHA3 |
| GSM8199929 | JEHA5 |
| GSM8199930 | JEHA7 |
| GSM8199931 | KISZ1 |
| GSM8199932 | KISZ3 |
| GSM8199933 | KISZ5 |
| GSM8199934 | KISZ7 |
| GSM8199935 | NACR1 |
| GSM8199936 | NACR3 |
| GSM8199937 | NACR5 |
| GSM8199938 | NACR7 |
| GSM8199939 | SASY1 |
| GSM8199940 | SASY7 |
| GSM8199941 | TATU1 |
| GSM8199942 | TATU3 |
| GSM8199943 | TATU5 |
| GSM8199944 | TATU7 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| subject | grp | 10 | 38/38 | 9 | 0 |
| subject | characteristics_ch1.4.treatment | 10 | 2/38 | 1 | 9 |
| subject | characteristics_ch1.5.day of_collection | 10 | 2/38 | 1 | 9 |
| subject | cond | 10 | 2/38 | 1 | 9 |
| subject | day | 10 | 2/38 | 1 | 9 |
