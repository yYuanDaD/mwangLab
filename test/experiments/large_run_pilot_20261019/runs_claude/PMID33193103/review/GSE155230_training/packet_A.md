# Review packet A (facts only): GSE155230_training

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC7649134.paper.md`

## Paper outline

- # Comparative Analysis of Skeletal Muscle Transcriptional Signatures Associated With Aerobic Exercise Capacity or Response to Training in Humans and Rats
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Materials and Methods  `S2` · methods
- ### Animals  `S2.1` · methods
- #### Selective Breeding for Exercise Capacity Model  `S2.1.1` · methods
- #### Artificial Selection for Acquired Capacity Models  `S2.1.2` · methods
- #### Endurance Training of High and Low Responder Lines  `S2.1.3` · methods
- ### RNA Sequencing  `S2.2` · methods
- ### Human Training Study  `S2.3` · methods
- #### Bioinformatic Analysis  `S2.3.1` · methods
- ### Secretome Analysis  `S2.4` · methods
- ### Statistical Analysis  `S2.5` · methods
- ## Results  `S3` · results
- ### Muscle Transcriptional Signature of Aerobic Exercise Capacity Highlights Enhanced Vascularization and Oxygenation  `S3.1` · results
- ### Reduced Response to Endurance Training Is Associated With Inflammatory Gene Signature and Circadian Rhythm Regulation  `S3.2` · results
- ### The Predicted Muscle Secretomes of Exercise Capacity and Response Highlight Lipid Metabolism and Extracellular Matrix Remodelling  `S3.3` · results
- ### Gene Networks of Exercise Capacity and Response in Humans  `S3.4` · results
- ## Discussion  `S4` · discussion
- ## Limitations  `S5` · other
- ## Data Availability Statement  `S6` · data_availability
- ## Ethics Statement  `S7` · other
- ## Author Contributions  `S8` · other
- ## Funding  `S9` · other
- ## Conflict of Interest  `S10` · other
- ## Acknowledgments  `S11` · other
- ## Supplementary Material  `S12` · supplementary
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.0.group`: high response trainers: 3; low response trainers: 3; High responder to training -trained: 3; Low responder to training -trained: 3
- `lane`: L2: 6; L3: 4; L1: 2
- `grp`: HRT: 3; LRT: 3; HRTT: 3; LRTT: 3

### Constant columns

- `status`: Public on Aug 30 2020
- `submission_date`: Jul 27 2020
- `last_update_date`: Aug 30 2020
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Gastrocnemius muscle
- `organism_ch1`: Rattus norvegicus
- `taxid_ch1`: 10116
- `characteristics_ch1.1.tissue`: Skeletal muscle
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Gastrocnemius muscles were dissected, flash frozen and RNA was harvested using Trizol reagent.,Illumina TruSeq RNA Sample Prep Kit (Cat#FC-122-1001) was used with 1 ug of total RNA for the construction of sequencing libraries.
- `data_processing`: Sequenced reads were trimmed for adaptor sequence, and masked for low-complexity or low-quality sequence, then mapped to Rnor_6.0 whole genome using TopHat v2.1.1 with parameters -p 15 -N 18 --read-edit-dist 18,Differential gene expression analysis was done using cufflinks with parameters --multi-re ... [309 more characters]
- `platform_id`: GPL18694
- `contact_name`: Jorge,,Ruas
- `contact_email`: jorge.ruas@ki.se
- `contact_laboratory`: Molecular and Cellular Exercise Physiology
- `contact_department`: Department of Physiology and Pharmacology
- `contact_institute`: Karolinska Institute
- `contact_address`: Solnav盲gen 9
- `contact_city`: Stockholm
- `contact_zip/postal_code`: 171 65
- `contact_country`: Sweden
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE155230
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM4697801 | High responder to training 1 | HRT_1 |
| GSM4697802 | High responder to training 2 | HRT_2 |
| GSM4697803 | High responder to training 3 | HRT_3 |
| GSM4697804 | Low responder to training 1 | LRT_1 |
| GSM4697805 | Low responder to training 2 | LRT_2 |
| GSM4697806 | Low responder to training 3 | LRT_3 |
| GSM4697807 | High responder to training -trained 1 | HRTT_1 |
| GSM4697808 | High responder to training -trained 2 | HRTT_2 |
| GSM4697809 | High responder to training -trained 3 | HRTT_3 |
| GSM4697810 | Low responder to training -trained 1 | LRTT_1 |
| GSM4697811 | Low responder to training -trained 2 | LRTT_2 |
| GSM4697812 | Low responder to training -trained 3 | LRTT_3 |

## Values with exercise words (by column)

- `title`: High responder to training -trained 1, High responder to training -trained 2, High responder to training -trained 3, High responder to training 1, High responder to training 2, High responder to training 3, Low responder to training -trained 1, Low responder to training -trained 2, Low responder to training -trained 3, Low responder to training 1, Low responder to training 2, Low responder to training 3
- `characteristics_ch1.0.group`: High responder to training -trained, Low responder to training -trained
- `contact_laboratory`: Molecular and Cellular Exercise Physiology

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.0.group level | characteristics_ch1.0.group | 3 | 12/12 | 3 | 0 |
| suffix of title | characteristics_ch1.0.group | 3 | 12/12 | 3 | 0 |
| suffix of description | characteristics_ch1.0.group | 3 | 12/12 | 3 | 0 |
| suffix of title | grp | 3 | 12/12 | 3 | 0 |
| description without the grp level | grp | 3 | 12/12 | 3 | 0 |
| suffix of description | grp | 3 | 12/12 | 3 | 0 |
| lane (without characteristics_ch1.0.group) + suffix of title | characteristics_ch1.0.group | 8 | 8/12 | 0 | 0 |
| lane (without characteristics_ch1.0.group) + suffix of description | characteristics_ch1.0.group | 8 | 8/12 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the characteristics_ch1.0.group level", "across": "_across", "within": [], "n_same_key_pairs": 18, "same_key_mean_r": 0.153, "other_mean_r": -0.075, "difference": 0.228, "permutation_p": 0.08045977011494253, "genes_used": 7410, "status": "not_supported"}
