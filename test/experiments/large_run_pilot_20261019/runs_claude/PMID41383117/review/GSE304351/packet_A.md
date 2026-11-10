# Review packet A (facts only): GSE304351

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC12699140.paper.md`

## Paper outline

- # NAD^+ Enhanced Mesenchymal Stromal Cells Effect on Muscle Atrophy by Improving SIRT1‐Mediated Mitochondrial Function via NAMPT
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## Introduction  `S1` · introduction
- ## Materials and Methods  `S2` · methods
- ### Human MSC Isolation, Characterisation and RNAi  `S2.1` · methods
- ### Cell Culture and RNAi  `S2.2` · methods
- ### Animal Procedure  `S2.3` · methods
- ### In Vivo Muscle Performance Analysis  `S2.4` · methods
- ### Tissue Processing  `S2.5` · methods
- ### Histology Staining  `S2.6` · methods
- ### RNA‐Seq and Real‐Time Quantitative PCR Analysis  `S2.7` · methods
- ### Untargeted Metabolomics  `S2.8` · methods
- ### Preparation of MSC Supernatant and Proteomics  `S2.9` · methods
- ### Isolation of Extracelluar Vesicles  `S2.10` · methods
- ### Western Blotting  `S2.11` · methods
- ### Transmission Electron Microscopy  `S2.12` · methods
- ### ATP Content Assay  `S2.13` · methods
- ### NAD^+ Content Assay  `S2.14` · methods
- ### Seahorse Analysis  `S2.15` · methods
- ### Statistical Analysis  `S2.16` · methods
- ## Results  `S3` · results
- ### NAD^+ Pretreatment Enhances the Therapeutic Effect of MSCs on D‐Gal–Induced Muscle Atrophy  `S3.1` · results
- ### MSCs/NAD^+‐MSCs Rescue Muscle Atrophy–Associated Impairment of the SIRT1/PGC‐1α Signalling and Mitochondrial Function  `S3.2` · results
- ### MSCs/NAD^+‐MSCs Regulate SIRT1/PGC‐1α Signaling and Mitochondrial Function in C2C12 Myotubes  `S3.3` · results
- ### SIRT1 Mediates the Beneficial Effects of MSCs/NAD^+‐MSCs in Myotubes  `S3.4` · results
- ### NAD^+ Pretreatment Promotes NAMPT Secretion by MSCs  `S3.5` · results
- ### NAD^+ Enhances the Therapeutic Effect of MSCs on Muscle Atrophy by Promoting NAMPT Secretion  `S3.6` · results
- ## Discussion  `S4` · discussion
- ## Funding  `S5` · other
- ## Ethics Statement  `S6` · other
- ## Conflicts of Interest  `S7` · other
- ## Supporting information  `S8` · supplementary
- ## Data Availability Statement  `DA` · data_availability
- ## Accession mentions

## Metadata (8 samples)

### Grouping columns (level: count)

- `grp`: PBS: 4; MSC: 4

### Constant columns

- `status`: Public on Dec 17 2025
- `submission_date`: Aug 01 2025
- `last_update_date`: Dec 17 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: skeletal muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: skeletal muscle
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was isolated  using TRIzol reagent (Invitrogen). 2ug of total RNA was used for construction of sequencing libraries.,RNA libraries for RNA-seq were prepared using VAHTS Universal V6 RNA-seq Library Prep Kit for Illumina following manufacturer's protocols.
- `data_processing`: Raw data (raw reads) of fastq format were firstly processed through in-house perl scripts. In this step, clean data(clean reads) were obtained by removing reads containing adapter, reads containing ploy-N and low quality reads from raw data. At the same time,Q20, Q30, GC-content and sequence duplica ... [547 more characters]
- `platform_id`: GPL34290
- `contact_name`: Jia,,Song
- `contact_email`: 202362000486@email.sdu.edu.cn
- `contact_phone`: 18560087437
- `contact_institute`: Qilu Hospital of Shandong University
- `contact_address`: No.107 Wenhua Xi Road, Jinan,Shandong Province
- `contact_city`: Jinan
- `contact_state`: Select...
- `contact_zip/postal_code`: 250012
- `contact_country`: China
- `instrument_model`: Illumina NovaSeq X Plus
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE304351
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `libname`

### Samples

| sample | title | description |
|---|---|---|
| GSM9148482 | the quadriceps of D-gal+PBS mice 1 | Library name: PBS1 |
| GSM9148483 | the quadriceps of D-gal+PBS mice 2 | Library name: PBS2 |
| GSM9148484 | the quadriceps of D-gal+PBS mice 3 | Library name: PBS3 |
| GSM9148485 | the quadriceps of D-gal+PBS mice 4 | Library name: PBS4 |
| GSM9148486 | the quadriceps of D-gal+MSCs mice 1 | Library name: MSC1 |
| GSM9148487 | the quadriceps of D-gal+MSCs mice 2 | Library name: MSC2 |
| GSM9148488 | the quadriceps of D-gal+MSCs mice 3 | Library name: MSC3 |
| GSM9148489 | the quadriceps of D-gal+MSCs mice 4 | Library name: MSC4 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | grp | 4 | 8/8 | 4 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 4, "same_key_mean_r": 0.155, "other_mean_r": -0.049, "difference": 0.204, "permutation_p": 0.12843578210894552, "genes_used": 8540, "status": "not_supported"}
