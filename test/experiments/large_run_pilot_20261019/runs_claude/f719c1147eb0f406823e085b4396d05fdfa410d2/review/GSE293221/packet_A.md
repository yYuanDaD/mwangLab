# Review packet A (facts only): GSE293221

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC13076624.paper.md`

## Paper outline

- # Exercise and Phellodendron amurense extract differentially impinge on oxidative stress response pathways in a mouse model of prostate cancer
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Exercise and Phellodendron amurense extract decreased tumor grade  `S2.1` · results
- ### Differential tumor transcriptional signature in response to aerobic exercise and Phellodendron amurense extract interventions  `S2.2` · results
- ## Discussion  `S3` · discussion
- ## Materials and methods  `S4` · methods
- ### Transgenic mouse model  `S4.1` · methods
- ### Experimental design  `S4.2` · methods
- ### Voluntary wheel running  `S4.3` · methods
- ### Preparation of Phellodendron amurense extract diet  `S4.4` · methods
- ### Tumor histology  `S4.5` · methods
- ### RNA-seq library preparation and next generation sequencing  `S4.6` · methods
- ### Data analysis  `S4.7` · methods
- ## Author contributions  `BK1` · other
- ## Funding  `BK2` · other
- ## Data availability  `DA` · data_availability
- ## Declarations  `BK3` · other
- ## Accession mentions

## Metadata (9 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: Control group without intervention: 3; Mice  singularly housed and given access to a 15.5 cm diameter low-profile running wheel with activity recorded.: 3; Phellodendron amurense extract was supplied in the diet: 3
- `grp`: CON: 3; EX: 3; PHAM: 3

### Constant columns

- `status`: Public on Apr 07 2025
- `submission_date`: Mar 28 2025
- `last_update_date`: Apr 07 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: prostate tumor tissue
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.mouse strain`: Transgenic adenocarcinoma of the mouse prostate (TRAMP) mice in C57BL/6 background
- `characteristics_ch1.1.tissue`: prostate tumor tissue
- `treatment_protocol_ch1`: Mice were maintained in a climate-controlled environment with a 12-hour light-dark cycle with diet and water provided ad libitum. Phellodendron amurense extract (Nexrutine) was supplied in the diet and running wheel was used as the exercise intervention. The control group mice were group housed had  ... [73 more characters]
- `molecule_ch1`: polyA RNA
- `extract_protocol_ch1`: Total RNA was extracted using TRIzol (Thermo Fisher) from tumor and quantified using nanodrop and Agilent bioanalyzer.,Total RNA samples  were used for sequencing library preparation according to Illumina stranded mRNA sample preparation guide. Each library was bar-coded and then pooled for sequenci ... [49 more characters]
- `data_processing`: Illumina bcl2fastq software used for base-calling,Sequenced reads were trimmed for adaptor sequence, and masked for low-complexity or low-quality sequence, then mapped to mm9 whole genome using Tophat algoritm (v2.0.8).,Gene count measurements were obtained using HTSeq-count,Assembly: mm9,Supplement ... [197 more characters]
- `platform_id`: GPL21493
- `contact_name`: Yidong,,Chen
- `contact_email`: cheny8@uthscsa.edu
- `contact_phone`: 2105629163
- `contact_department`: Population Health Sciences
- `contact_institute`: UT Health Science Center at San Antonio
- `contact_address`: 8403 Floyd Curl Drive, MSC 7784
- `contact_city`: San Antonio
- `contact_state`: Texas
- `contact_zip/postal_code`: 78229
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 3000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE293221
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `supplementary_file_1`

### Samples

| sample | title | description |
|---|---|---|
| GSM8878836 | Control, rep1 | Library name: DP_MT_013 |
| GSM8878837 | Control, rep2 | Library name: DP_MT_014 |
| GSM8878838 | Control, rep3 | Library name: DP_MT_017 |
| GSM8878839 | Exercise, rep1 | Library name: DP_MT_001 |
| GSM8878840 | Exercise, rep2 | Library name: DP_MT_002 |
| GSM8878841 | Exercise, rep3 | Library name: DP_MT_004 |
| GSM8878842 | Nexrutine, rep1 | Library name: DP_MT_012 |
| GSM8878843 | Nexrutine, rep2 | Library name: DP_MT_022 |
| GSM8878844 | Nexrutine, rep3 | Library name: DP_MT_23b |

## Values with exercise words (by column)

- `title`: Exercise, rep1, Exercise, rep2, Exercise, rep3
- `characteristics_ch1.2.treatment`: Mice  singularly housed and given access to a 15.5 cm diameter low-profile running wheel with activity recorded.
- `treatment_protocol_ch1`: Mice were maintained in a climate-controlled environment with a 12-hour light-dark cycle with diet and water provided ad libitum. Phellodendron amurense extract (Nexrutine) was supplied in the diet and running wheel was used as the exercise intervention. The control group mice were group housed had access to AIN-93 diet ad libitum and did not have access to running wheel
- `extract_protocol_ch1`: Total RNA was extracted using TRIzol (Thermo Fisher) from tumor and quantified using nanodrop and Agilent bioanalyzer.,Total RNA samples  were used for sequencing library preparation according to Illumina stranded mRNA sample preparation guide. Each library was bar-coded and then pooled for sequencing run with 50bp single-read sequencing protocol.
- `grp`: EX

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.2.treatment | 3 | 9/9 | 3 | 0 |
| suffix of title | grp | 3 | 9/9 | 3 | 0 |
| grp (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 9 | 0/9 | 0 | 0 |
| suffix of description | characteristics_ch1.2.treatment | 8 | 0/8 | 0 | 0 |
| grp (without characteristics_ch1.2.treatment) + suffix of description | characteristics_ch1.2.treatment | 9 | 0/9 | 0 | 0 |
| characteristics_ch1.2.treatment (without grp) + suffix of title | grp | 9 | 0/9 | 0 | 0 |
| suffix of description | grp | 8 | 0/8 | 0 | 0 |
| characteristics_ch1.2.treatment (without grp) + suffix of description | grp | 9 | 0/9 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 9, "same_key_mean_r": -0.011, "other_mean_r": 0.003, "difference": -0.014, "permutation_p": 0.631184407796102, "genes_used": 11245, "status": "not_supported"}
