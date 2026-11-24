# Review packet A (facts only): GSE221894

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\PMID36603044\PMID36603044_abstract.txt`

## Metadata (27 samples)

### Grouping columns (level: count)

- `source_name_ch1`: Human muscle, baseline: 14; Human muscle, 48hr post exercise: 13
- `characteristics_ch1.1.status`: baseline: 14; 48hr post training: 13
- `characteristics_ch1.3.Sex`: Female: 16; Male: 11
- `characteristics_ch1.4.treatment`: : 14; 7 sessions of HIIT: 13
- `sex`: Female: 16; Male: 11
- `subject`: S14: 2; S16: 2; S19: 2; S1: 2; S20: 2; S28: 2; S32: 2; S33: 2; S34: 2; S3: 2; S6: 2; S7: 2; S27: 1; S4: 1; S8: 1
- `time`: post: 14; pre: 13

### Constant columns

- `status`: Public on Jan 10 2023
- `submission_date`: Dec 29 2022
- `last_update_date`: Jan 12 2023
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: Skeletal Muscle (Quad)
- `characteristics_ch1.2.cell type`: human skeletal muscle
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was isolated from ~20 mg of the pre- and post- biopsy samples using Trizol followed by spin-column for cleanup and DNAase treatment (Qiagen, Hilden, Germany). Total RNA was eluted in 50 碌l of PCR grade water and concentration was quantified using a spectrophotometer (Nanodrop, Thermo Scien ... [290 more characters]
- `description`: P2 flowcell
- `data_processing`: Sequencing was performed on an Illumina Nextseq 2000 (San Diego, CA) to produce 100bp Single-End Reads and Illumina CASAVA 1.8 software (San Diego, CA) used for basecalling.,The bioinformatics pipeline included the following steps: Sequence reads assessed for adapters and quality scores using FastQC ... [472 more characters]
- `platform_id`: GPL30173
- `contact_name`: Matthew,M,Robinson
- `contact_email`: matthew.robinson@oregonstate.edu
- `contact_institute`: Oregon State University
- `contact_address`: Milam Hall 003
- `contact_city`: Corvallis
- `contact_state`: OR
- `contact_zip/postal_code`: 97330
- `contact_country`: USA
- `instrument_model`: NextSeq 2000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE221894
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM6909062 | 14a |
| GSM6909063 | 14b |
| GSM6909064 | 16a |
| GSM6909065 | 16b |
| GSM6909066 | 19a |
| GSM6909067 | 19b |
| GSM6909068 | 1a |
| GSM6909069 | 1b |
| GSM6909070 | 20a |
| GSM6909071 | 20b |
| GSM6909072 | 27a |
| GSM6909073 | 28a |
| GSM6909074 | 28b |
| GSM6909075 | 32a |
| GSM6909076 | 32b |
| GSM6909077 | 33a |
| GSM6909078 | 33b |
| GSM6909079 | 34a |
| GSM6909080 | 34b |
| GSM6909081 | 3a |
| GSM6909082 | 3b |
| GSM6909083 | 4b |
| GSM6909084 | 6a |
| GSM6909085 | 6b |
| GSM6909086 | 7a |
| GSM6909087 | 7b |
| GSM6909088 | 8b |

## Values with exercise words (by column)

- `source_name_ch1`: Human muscle, 48hr post exercise
- `characteristics_ch1.1.status`: 48hr post training
- `characteristics_ch1.4.treatment`: 7 sessions of HIIT

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| subject | time | 15 | 24/27 | 12 | 0 |
| subject | source_name_ch1 | 15 | 22/27 | 11 | 1 |
| subject | characteristics_ch1.1.status | 15 | 22/27 | 11 | 1 |
| subject | characteristics_ch1.4.treatment | 15 | 22/27 | 11 | 1 |
| subject | characteristics_ch1.3.Sex | 15 | 0/27 | 0 | 12 |
| subject | sex | 15 | 0/27 | 0 | 12 |
