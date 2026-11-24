# Review packet A (facts only): GSE298607

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261028\papers\PMC12320216.paper.md`

## Paper outline

- # Long non‐coding RNAs Kcnq1ot1 and Lncpint are involved in skeletal muscle atrophy induced by the space exposome
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Methods  `S2` · methods
- ### Ethical approval  `S2.1` · methods
- ### Experimental model  `S2.2` · methods
- ### Hindlimb unloading  `S2.3` · methods
- ### Irradiation of animals  `S2.4` · methods
- ### Simulated psychological stress of animals  `S2.5` · methods
- ### RNA extraction, RNA sequencing and analysis  `S2.6` · methods
- ### Quantitative PCR of lncRNAs in skeletal muscle before and after long‐term bed rest  `S2.7` · methods
- ### Cell experiments  `S2.8` · methods
- ### Statistical analysis  `S2.9` · methods
- ## Results  `S3` · results
- ### Space exposome effects on mice transcriptional profiles  `S3.1` · results
- ### lncRNA regulation by space exposome  `S3.2` · results
- ### Validation in human skeletal muscle after bed rest  `S3.3` · results
- ### In vitro validation using 3‐D model of human skeletal muscle  `S3.4` · results
- ## Discussion  `S4` · discussion
- ## Competing interests  `S6` · other
- ## Author contributions  `S7` · other
- ## Funding  `S8` · other
- ## Supporting information  `S9` · supplementary
- ## Acknowledgements  `S10` · other
- ## Biography  `S11` · other
- ## (untitled)  `S12` · other
- ## Data availability statement  `S13` · data_availability
- ## Supplementary material  `SUPP` · supplementary
- ## Accession mentions

## Metadata (20 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: sham-irradiation: 10; Hind-limb unloading: 10
- `characteristics_ch1.3.treatment`: : 10; Ionizing radiation: 10
- `characteristics_ch1.4.treatment`: : 10; Stress hormone: 10
- `grp`: CONTROL: 10; SPACE: 10

### Constant columns

- `status`: Public on Aug 13 2025
- `submission_date`: May 30 2025
- `last_update_date`: Aug 13 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Soleus muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Soleus muscle
- `characteristics_ch1.1.strain`: C57BL/6J
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Bead beater device (BioSpec) was used to homogenate the soleus muscle in TriZol (Invitrogen), followed by chloroform gradient separation and ethanol dilution.  Direct-zol RNA Miniprep Kit (Zymo) was used to purify the RNA.,rRNA-depleted libraries were prepared from 90 ng of total RNA using Ribozero  ... [97 more characters]
- `data_processing`: Raw sequencing reads were submitted to MultiQC (v1.15) for quality control. Alignment to reference genome (GRCm39) was performed using subread sequence aligner and gene counts were summarised using featureCount (v1.5.1). After trimmed mean M normalization, expression values were converted to log2CPM ... [132 more characters]
- `platform_id`: GPL34290
- `contact_name`: Alen,,Lovric
- `contact_institute`: Karolinska Institutet
- `contact_address`: Nobels v盲g 5
- `contact_city`: Stockholm
- `contact_zip/postal_code`: 171 77
- `contact_country`: Sweden
- `instrument_model`: Illumina NovaSeq X Plus
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE298607
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `key`

### Samples

| sample | title | description |
|---|---|---|
| GSM9018347 | Sample 1, soleus muscle, control | Library name: Sample 1,S1001 |
| GSM9018348 | Sample 2, soleus muscle, control | Library name: Sample 2,S1002 |
| GSM9018349 | Sample 3, soleus muscle, control | Library name: Sample 3,S1003 |
| GSM9018350 | Sample 4, soleus muscle, control | Library name: Sample 4,S1004 |
| GSM9018351 | Sample 5, soleus muscle, control | Library name: Sample 5,S1005 |
| GSM9018352 | Sample 6, soleus muscle, control | Library name: Sample 6,S1006 |
| GSM9018353 | Sample 7, soleus muscle, control | Library name: Sample 7,S1007 |
| GSM9018354 | Sample 8, soleus muscle, control | Library name: Sample 8,S1008 |
| GSM9018355 | Sample 9, soleus muscle, control | Library name: Sample 9,S1009 |
| GSM9018356 | Sample 10, soleus muscle, control | Library name: Sample 10,S1010 |
| GSM9018357 | Sample 1, soleus muscle, space | Library name: Sample 11,S1011 |
| GSM9018358 | Sample 2, soleus muscle, space | Library name: Sample 12,S1012 |
| GSM9018359 | Sample 3, soleus muscle, space | Library name: Sample 13,S1013 |
| GSM9018360 | Sample 4, soleus muscle, space | Library name: Sample 14,S1014 |
| GSM9018361 | Sample 5, soleus muscle, space | Library name: Sample 15,S1015 |
| GSM9018362 | Sample 6, soleus muscle, space | Library name: Sample 16,S1016 |
| GSM9018363 | Sample 7, soleus muscle, space | Library name: Sample 17,S1017 |
| GSM9018364 | Sample 8, soleus muscle, space | Library name: Sample 18,S1018 |
| GSM9018365 | Sample 9, soleus muscle, space | Library name: Sample 19,S1019 |
| GSM9018366 | Sample 10, soleus muscle, space | Library name: Sample 20,S1020 |

## Values with exercise words (by column)

- `characteristics_ch1.2.treatment`: Hind-limb unloading

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the grp level | grp | 10 | 20/20 | 10 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the grp level", "across": "_across", "within": [], "n_same_key_pairs": 10, "same_key_mean_r": 0.018, "other_mean_r": -0.002, "difference": 0.02, "permutation_p": 0.3548225887056472, "genes_used": 8556, "status": "not_supported"}
