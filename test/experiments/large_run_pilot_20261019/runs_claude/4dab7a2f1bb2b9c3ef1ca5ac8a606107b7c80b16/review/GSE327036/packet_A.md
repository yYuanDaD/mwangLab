# Review packet A (facts only): GSE327036

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\4dab7a2f1bb2b9c3ef1ca5ac8a606107b7c80b16.paper.md`

## Paper outline

- # Untitled paper
- ## (untitled)  `S0` · other
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Materials and Methods 117  `S2` · methods
- ### Immunoblot analysis  `S2.1` · methods
- ### Grip strength test  `S2.2` · methods
- ### Exercise tolerance test  `S2.3` · methods
- ### Measurement of blood lactate levels  `S2.4` · methods
- ### Whole-transcriptome analysis by RNA-seq  `S2.5` · methods
- ### Preparation of muscle cryosections and immunofluorescence imaging  `S2.6` · methods
- ### Isolation of mitochondria and measurement of oxygen consumption rate (OCR)  `S2.7` · methods
- ### Blue Native PAGE  `S2.8` · methods
- ### Quantification of phospholipid molecular species and CoQ by LC-MS/MS  `S2.9` · methods
- ### Specificity of STARD7 for PC molecular species  `S2.10` · methods
- ### Electron microscopy  `S2.11` · methods
- ### Quantification of mitochondrial DNA (mtDNA)  `S2.12` · methods
- ### Statistical analyses  `S2.13` · methods
- ## Results  `S3` · results
- ### STARD7 is highly expressed in mitochondria-rich slow-twitch muscle  `S3.1` · results
- ### Muscle-specific deletion of STARD7 impairs exercise performance without structural abnormalities  `S3.2` · results
- ### Loss of STARD7 suppresses fast-twitch fiber-associated gene expression in the soleus  `S3.3` · results
- ### STARD7 deficiency reduces mitochondrial OCR  `S3.4` · results
- ### STARD7 deficiency disrupts mitochondrial phospholipid homeostasis  `S3.5` · results
- ### Selective transport of linoleoyl-PC by STARD7 contributes to CL maintenance  `S3.6` · results
- ### Abnormal mitochondrial morphology in STARD7-deficient muscle  `S3.7` · results
- ## Discussion  `S4` · discussion
- ## Data Availability  `DA` · data_availability
- ## Conflicts of Interest  `S5` · other
- ## Author Contributions  `S6` · other
- ## Acknowledgments  `S7` · other
- ## Figures and tables  `FLT` · other

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.genotype`: WT: 3; mKO: 3
- `genotype`: WT: 3; mKO: 3

### Constant columns

- `status`: Public on Apr 14 2026
- `submission_date`: Apr 06 2026
- `last_update_date`: Apr 14 2026
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: soleus
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: soleus
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was purified using the Maxwell RSC simply RNA Tissue Kit (Promega).,RNA-seq libraries were prepared from total RNA using the NEBNext Poly(A) mRNA Magnetic Isolation Module and the NEBNext Ultra II Directional RNA Library Prep Kit for Illumina (New England Biolabs) according to the manufact ... [20 more characters]
- `data_processing`: CLC Genomics Workbench (v23.0.2),Assembly: GRCm39,Supplementary files format and content: Processed data files contain raw gene counts for each sample in tab-delimited text format.
- `platform_id`: GPL24247
- `contact_name`: Yasuhiro,,Horibata
- `contact_institute`: Dokkyo Medical University
- `contact_address`: 880 Kitakobayashi
- `contact_city`: Tochigi
- `contact_zip/postal_code`: 3210293
- `contact_country`: Japan
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE327036
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `supplementary_file_1`

### Samples

| sample | title | description |
|---|---|---|
| GSM9646929 | WT soleus rep1 | Library name: Control_1 |
| GSM9646930 | WT soleus rep2 | Library name: Control_2 |
| GSM9646931 | WT soleus rep3 | Library name: Control_3 |
| GSM9646932 | mKO soleus rep1 | Library name: KO_1 |
| GSM9646933 | mKO soleus rep2 | Library name: KO_2 |
| GSM9646934 | mKO soleus rep3 | Library name: KO_3 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.1.genotype level | characteristics_ch1.1.genotype | 3 | 6/6 | 3 | 0 |
| suffix of title | characteristics_ch1.1.genotype | 3 | 6/6 | 3 | 0 |
| suffix of description | characteristics_ch1.1.genotype | 3 | 6/6 | 3 | 0 |
| title without the genotype level | genotype | 3 | 6/6 | 3 | 0 |
| suffix of title | genotype | 3 | 6/6 | 3 | 0 |
| suffix of description | genotype | 3 | 6/6 | 3 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the characteristics_ch1.1.genotype level", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": 0.136, "other_mean_r": -0.068, "difference": 0.204, "permutation_p": 0.17641179410294852, "genes_used": 6804, "status": "not_supported"}
