# Review packet A (facts only): GSE180877

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC8636928.paper.md`

## Paper outline

- # Nucleus Type-Specific DNA Methylomics Reveals Epigenetic “Memory” of Prior Adaptation in Skeletal Muscle
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Nucleus Type-Specific Promoter Methylation Revealed Reciprocal Regulation of Resident Myonuclei and Interstitial Nuclei with Muscle Adaptation  `S2.1` · results
- ### Persistent Promoter Methylation Changes 12 wk After PoWeR in Myonuclei  `S2.2` · results
- ### Evidence for Persistent Methylation Changes in Interstitial Nuclei After Detraining  `S2.3` · results
- ### Methylation of Myonuclear Ribosomal DNA (rDNA) With Training and Detraining  `S2.4` · results
- ### Gene Expression Changes From Training Do Not Persist Following Detraining  `S2.5` · results
- ### Accelerated Whole Muscle and Muscle Fiber Hypertrophy in Previously Trained Muscle  `S2.6` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### Statistics  `S4.1` · methods
- ## Supplementary Material  `S5` · supplementary
- ## Data Availability  `DA` · data_availability
- ## Author Contributions  `BK1` · other
- ## Funding  `BK2` · other
- ## Conflict of Interest Statement  `BK3` · other
- ## Accession mentions

## Metadata (15 samples)

### Grouping columns (level: count)

- `submission_date`: Jul 26 2021: 12; Sep 03 2021: 3
- `characteristics_ch1.1.treatment`: Sedentary: 9; Exercise: 3; Detrained: 3
- `characteristics_ch1.2.age`: 6mo: 9; 9mo: 6
- `grp`: PoW6: 6; UT6: 3; UT9: 3; DT9: 3
- `grpx`: UT6: 3; PoW6: 3; UT9: 3; DT9: 3; LD6: 3

### Constant columns

- `status`: Public on Dec 08 2021
- `last_update_date`: Dec 08 2021
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: plantaris
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Skeletal Muscle
- `characteristics_ch1.3.Sex`: male
- `treatment_protocol_ch1`: Adult male (>4 months) mice were subjected to progressive weighted wheel running (PoWeR) for 8 weeks then detrained for 12 weeks. Age-matched mice served as controls.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Plantaris muscles were flash frozen in liquid nitrogen and RNA was isolated using TRIzol and the Zymo MicroPrep Kit and prepared for RNA-sequencing,RNA libraries were prepared for sequencing using standard Illumina protocols
- `data_processing`: Sequenced reads were mapped to mm10 mouse genome assembly using STAR 2.7.3a with default parameters.,Aligned reads were quantified for gene counts, filtered to exclude genes  with high noise or a maximum count of less than or equal to 50.,The filtered counts were median ratio normalized and tested f ... [225 more characters]
- `platform_id`: GPL24247
- `contact_name`: Yuan,,Wen
- `contact_email`: ywen2@g.uky.edu
- `contact_phone`: 8592186846
- `contact_institute`: University of Kentucky
- `contact_address`: 760 Press Ave
- `contact_city`: Lexington
- `contact_state`: Kentucky
- `contact_zip/postal_code`: 40536
- `contact_country`: USA
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE180877
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`, `_norm_key`

### Samples

| sample | title |
|---|---|
| GSM5474092 | 6M UT1 [PoW3] |
| GSM5474093 | 6M UT2 [PoW12] |
| GSM5474094 | 6M UT3 [PoW17] |
| GSM5474095 | 6M PoW1 [PoW13] |
| GSM5474096 | 6M PoW2 [PoW15] |
| GSM5474097 | 6M PoW3 [PoW16] |
| GSM5474098 | 9M UT1 [DT2] |
| GSM5474099 | 9M UT2 [DT3] |
| GSM5474100 | 9M UT3 [DT4] |
| GSM5474101 | 9M PoW+DT1 [DT6] |
| GSM5474102 | 9M PoW+DT2 [DT7] |
| GSM5474103 | 9M PoW+DT3 [DT8] |
| GSM5556584 | 6M POW4 [LD1] |
| GSM5556585 | 6M POW5 [LD2] |
| GSM5556586 | 6M POW6 [LD3] |

## Values with exercise words (by column)

- `characteristics_ch1.1.treatment`: Detrained, Exercise, Sedentary
- `treatment_protocol_ch1`: Adult male (>4 months) mice were subjected to progressive weighted wheel running (PoWeR) for 8 weeks then detrained for 12 weeks. Age-matched mice served as controls.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| grpx | submission_date | 5 | 0/15 | 0 | 5 |
| grpx | characteristics_ch1.1.treatment | 5 | 0/15 | 0 | 5 |
| grpx | characteristics_ch1.2.age | 5 | 0/15 | 0 | 5 |
| grpx | grp | 5 | 0/15 | 0 | 5 |
