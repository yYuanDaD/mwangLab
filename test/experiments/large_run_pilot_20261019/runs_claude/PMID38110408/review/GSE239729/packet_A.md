# Review packet A (facts only): GSE239729

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC10728194.paper.md`

## Paper outline

- # Cdo1-Camkk2-AMPK axis confers the protective effects of exercise against NAFLD in mice
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Hepatic Cdo1 is induced through the cAMP/PKA/CREB pathway during exercise in mice  `S2.1` · results
- ### Hepatocyte-specific knockout of Cdo1 (Cdo1LKO) impairs exercise-mediated alleviation of fatty liver in mice  `S2.2` · results
- ### Cdo1-regulated AMPK signaling is involved in exercise-mediated alleviation of fatty liver in mice  `S2.3` · results
- ### Cdo1 deficiency exacerbates hepatocytes steatosis in vitro  `S2.4` · results
- ### Cdo1 overexpression alleviates hepatocytes steatosis in vitro  `S2.5` · results
- ### AMPK signaling is indispensable for Cdo1-mediated amelioration of hepatocytes steatosis  `S2.6` · results
- ### Cdo1 tethers Camkk2 to AMPK by interacting with both of them, thereby promoting AMPK phosphorylation  `S2.7` · results
- ### Hepatocyte-specific overexpression of Cdo1 (Cdo1LTG) and exercise synergistically alleviate NAFLD in mice  `S2.8` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### Animals  `S4.1` · methods
- ### Treadmill training and time to exhaustion  `S4.2` · methods
- ### Mouse metabolic and liver function assays  `S4.3` · methods
- ### Primary hepatocytes isolation and cells culture  `S4.4` · methods
- ### Lipid analysis  `S4.5` · methods
- ### MitoScene analysis  `S4.6` · methods
- ### Cysteine and taurine levels analysis  `S4.7` · methods
- ### FAO level analysis  `S4.8` · methods
- ### Chromatin immunoprecipitation (ChIP)  `S4.9` · methods
- ### Measurement of cellular oxygen consumption rate (OCR)  `S4.10` · methods
- ### Luciferase reporter assays  `S4.11` · methods
- ### RNA extraction and reverse transcription-quantitative PCR (RT-qPCR)  `S4.12` · methods
- ### Western blotting  `S4.13` · methods
- ### Generation of recombinant adenoviruses and RNA interference  `S4.14` · methods
- ### H&E staining, Oil O staining and immunofluorescence assay  `S4.15` · methods
- ### The mitoDNA content quantification by quantitative real-time PCR  `S4.16` · methods
- ### Detection of mice metabolic rate  `S4.17` · methods
- ### Cell-free kinase assay  `S4.18` · methods
- ### RNA-seq analysis  `S4.19` · methods
- ### Statistical analyses  `S4.20` · methods
- ### Reporting summary  `S4.21` · methods
- ## Supplementary information  `S5` · supplementary
- ## Source data  `S6` · supplementary
- ## Supplementary information  `BK1` · supplementary
- ## Author contributions  `BK2` · other
- ## Peer review  `BK3` · other
- ### Peer review information  `BK3.1` · other
- ## Data availability  `DA` · data_availability
- ## Competing interests  `BK4` · other
- ## Accession mentions

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.genotype`: WT: 3; Cdo1 liver KO: 3
- `genotype`: WT: 3; LKO: 3

### Constant columns

- `status`: Public on Aug 07 2023
- `submission_date`: Jul 31 2023
- `last_update_date`: Aug 07 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Liver
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Liver
- `characteristics_ch1.2.treatment`: HFD feeding 12 weeks
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Retinas were removed, flash frozen on dry ice, and RNA was harvested using Trizol reagent.,RNA libraries were prepared for sequencing using standard IIIumina protocols
- `data_processing`: Illumina Casava1.7 software used for basecalling.,Sequenced reads were trimmed for adaptor sequence, and masked for low-complexity or low-quality sequence, then mapped to mm8 whole genome using bowtie v0.12.2 with parameters,FeatureCounts (v1.5.0-p3) was used to count the reads numbers mapped to eac ... [323 more characters]
- `platform_id`: GPL24247
- `contact_name`: Min,,Chen
- `contact_email`: min18328620206@outlook.com
- `contact_phone`: 550666
- `contact_institute`: Shanghai University of sports
- `contact_address`: YangPu
- `contact_city`: Shanghai
- `contact_zip/postal_code`: 200438
- `contact_country`: China
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE239729
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM7670607 | WT 1 |
| GSM7670608 | WT 2 |
| GSM7670609 | WT 3 |
| GSM7670610 | Cdo1-LKO 1 |
| GSM7670611 | Cdo1-LKO 2 |
| GSM7670612 | Cdo1-LKO 3 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.1.genotype | 3 | 6/6 | 3 | 0 |
| suffix of title | genotype | 3 | 6/6 | 3 | 0 |
| genotype (without characteristics_ch1.1.genotype) + suffix of title | characteristics_ch1.1.genotype | 6 | 0/6 | 0 | 0 |
| characteristics_ch1.1.genotype (without genotype) + suffix of title | genotype | 6 | 0/6 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": 0.102, "other_mean_r": -0.053, "difference": 0.154, "permutation_p": 0.3468265867066467, "genes_used": 6427, "status": "not_supported"}
