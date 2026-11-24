# Review packet A (facts only): GSE324693

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261028\papers\PMC13022470.paper.md`

## Paper outline

- # Systemic Consequences of Chronic Ethanol Intake: From Microbiome Shifts to Metabolic Impairment
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Methods and Materials  `S2` · methods
- ### Ethics Approval and Animal Models  `S2.1` · methods
- ### Ethanol (EtOH) Feeding  `S2.2` · methods
- ### Experimental Design  `S2.3` · methods
- ### Experimental Procedures  `S2.4` · methods
- #### Body Composition  `S2.4.1` · methods
- #### Running Endurance  `S2.4.2` · methods
- #### Grip Strength  `S2.4.3` · methods
- #### Walking Speed  `S2.4.4` · methods
- #### Glucose Tolerance  `S2.4.5` · methods
- #### Gut Microbial Profiles  `S2.4.6` · methods
- #### Fecal Short‐Chain Fatty Acids (SCFAs)  `S2.4.7` · methods
- #### Serum Markers of Liver Damage  `S2.4.8` · methods
- #### Serum Markers of Gut Permeability  `S2.4.9` · methods
- #### Contents of Specific Liver Proteins  `S2.4.10` · methods
- #### Serum Lipid Profiles  `S2.4.11` · methods
- #### Liver Lipid Profiles  `S2.4.12` · methods
- #### Liver Pathophysiology  `S2.4.13` · methods
- #### Liver Amyloid‐β Content  `S2.4.14` · methods
- #### Tissue Free Fatty Acids  `S2.4.15` · methods
- #### Transcriptomics  `S2.4.16` · methods
- ### Statistical Analyses  `S2.5` · methods
- ## Results  `S3` · results
- ### EtOH Disrupts Energy Balance, Body Composition and Physical Function  `S3.1` · results
- ### EtOH Drives Taxonomic Shifts in Gut Microbiota and Depletes Key SCFAs  `S3.2` · results
- ### EtOH Promotes “Leaky Gut”, Induces Liver Inflammation & Amyloidosis and Impairs Cholesterol Biosynthesis  `S3.3` · results
- ### EtOH Causes Dyslipidemia and Glucose Intolerance With Minimal Impact on White Adipose Tissue Gene Expression  `S3.4` · results
- ## Discussion  `S4` · discussion
- ## Author Contributions  `S5` · other
- ## Funding  `S6` · other
- ## Ethics Statement  `S7` · other
- ## Conflicts of Interest  `S8` · other
- ## Supporting information  `S9` · supplementary
- ## Data Availability Statement  `S10` · data_availability
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: Vehicle: 6; EtOH: 6
- `grp`: CTRL: 6; ETOH: 6

### Constant columns

- `status`: Public on Apr 01 2026
- `submission_date`: Mar 12 2026
- `last_update_date`: Apr 01 2026
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: subcutaneous WAT
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: subcutaneous WAT
- `characteristics_ch1.1.genotype`: C57BL/6
- `characteristics_ch1.3.batch`: 1
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: RNA was isolated from WAT using a Takara NucleoSpin RNA kit according to the manufacturer鈥檚 instructions, and 300ng total RNA was sequenced,QIAseq Fast Select rRNA HMR; QIAseq Low Input RNA Library Kit (primers N6-T RT and ODT-RT)
- `data_processing`: Alignment and mapping using Rsubread and featureCounts,Assembly: GRCm39,Supplementary files format and content: Raw counts matrix (counts_matrix.csv)
- `platform_id`: GPL34290
- `contact_name`: Michael,,Tranter
- `contact_email`: Michael.tranter@osumc.edu
- `contact_department`: Molecular Medicine and Therapeutics
- `contact_institute`: The Ohio State University
- `contact_address`: 2255 Kenny Road
- `contact_city`: Columbus
- `contact_state`: OH
- `contact_zip/postal_code`: 43210
- `contact_country`: USA
- `instrument_model`: Illumina NovaSeq X Plus
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE324693
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `skey`

### Samples

| sample | title | description |
|---|---|---|
| GSM9583069 | S1 ctrl | Library name: Sample1 |
| GSM9583070 | S2 ctrl | Library name: Sample2 |
| GSM9583071 | S3 ctrl | Library name: Sample3 |
| GSM9583072 | S4 ctrl | Library name: Sample4 |
| GSM9583073 | S5 ctrl | Library name: Sample5 |
| GSM9583074 | S6 ctrl | Library name: Sample6 |
| GSM9583075 | S7 EtOH | Library name: Sample7 |
| GSM9583076 | S8 EtOH | Library name: Sample8 |
| GSM9583077 | S9 EtOH | Library name: Sample9 |
| GSM9583078 | S10 EtOH | Library name: Sample10 |
| GSM9583079 | S11 EtOH | Library name: Sample11 |
| GSM9583080 | S12 EtOH | Library name: Sample12 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of skey | characteristics_ch1.2.treatment | 12 | 0/12 | 0 | 0 |
| grp (without characteristics_ch1.2.treatment) + suffix of skey | characteristics_ch1.2.treatment | 12 | 0/12 | 0 | 0 |
| suffix of skey | grp | 12 | 0/12 | 0 | 0 |
| characteristics_ch1.2.treatment (without grp) + suffix of skey | grp | 12 | 0/12 | 0 | 0 |
