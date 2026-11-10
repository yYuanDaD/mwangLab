# Review packet A (facts only): GSE256152

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC10990956.paper.md`

## Paper outline

- # Transcriptomics and metabonomics study on the effect of exercise combined with curcumin supplementation on breast cancer in mice
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Materials and methods  `S2` · methods
- ### Cell culture and mouse model establishment  `S2.1` · methods
- ### Sample collection  `S2.2` · methods
- ### RNA sequencing and data analysis  `S2.3` · methods
- ### Metabonomics analysis  `S2.4` · methods
- ### Integrative analysis of multi-omics data  `S2.5` · methods
- ### Statistical analysis  `S2.6` · methods
- ## Results  `S3` · results
- ### Curcumin combined with exercise enhanced the inhibitory effect on breast cancer  `S3.1` · results
- ### Transcriptomic analysis of curcumin-exercise combination treatment effects on breast tumour in mice  `S3.2` · results
- ### Differential analysis of metabolites in the intestinal contents of mice under the combined action of curcumin and exercise  `S3.3` · results
- ### Integrative analysis of metabolomics and transcriptomics data  `S3.4` · results
- ## Discussion  `S4` · discussion
- ## Ethical approval  `S5` · other
- ## Funding  `S6` · other
- ## Data availability statement  `S7` · data_availability
- ## CRediT authorship contribution statement  `S8` · other
- ## Declaration of competing interest  `S9` · other
- ## Contributor Information  `S11` · other
- ## Supplementary data  `S12` · supplementary
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.4.treatment`: The mice were given corn oil: 6; Mice were given curcumin solution (100mg/Kg): 6
- `grp`: Tnm: 3; cur: 3; swim: 3; union: 3

### Constant columns

- `status`: Public on Apr 10 2024
- `submission_date`: Feb 20 2024
- `last_update_date`: Apr 10 2024
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: tumor stage
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: tumor stage
- `characteristics_ch1.1.cell line`: 4T1-LUC
- `characteristics_ch1.2.cell type`: Breast cancer cell
- `characteristics_ch1.3.host strain`: BALB/c
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Mouse 4T1 breast cancer cells were cultured in complete medium containing 90%DMEM, 10% fetal bovine serum (high quality) and 1% penicillin streptomycin at 37鈩 in a 5% C02 incubator, and cell suspension with cell concentration of 1脳10^7/ml was prepared for use. Thirty healthy BALB/c mice, aged 4 to 6 ... [1284 more characters]
- `data_processing`: In this project, mRNA with polyA structure in total RNA was enriched by Oligo(dT) magnetic beads, and a gene library was constructed using RNA as a template, and the library fragments were enriched by PCR amplification. The library was inspected by Agilent 2100 Bioanalyzer, and then the total concen ... [2038 more characters]
- `platform_id`: GPL15103
- `contact_name`: He,,Kan
- `contact_email`: hekan@ahu.edu.cn
- `contact_phone`: 19965343623
- `contact_institute`: Anhui University
- `contact_address`: No. 111 Jiulong Road, Furong community, Shushan District, Hefei City, Anhui province
- `contact_city`: HeFei
- `contact_state`: AnHui
- `contact_zip/postal_code`: 230000
- `contact_country`: China
- `instrument_model`: Illumina HiSeq 1000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE256152
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM8086540 | Tnm-1 |
| GSM8086541 | Tnm-2 |
| GSM8086542 | Tnm-3 |
| GSM8086543 | Tnm-cur-1 |
| GSM8086544 | Tnm-cur-2 |
| GSM8086545 | Tnm-cur-3 |
| GSM8086546 | Tnm-swim-1 |
| GSM8086547 | Tnm-swim-2 |
| GSM8086548 | Tnm-swim-3 |
| GSM8086549 | Tnm+union-1 |
| GSM8086550 | Tnm+union-2 |
| GSM8086551 | Tnm+union-3 |

## Values with exercise words (by column)

- `title`: Tnm-swim-1, Tnm-swim-2, Tnm-swim-3
- `extract_protocol_ch1`: Mouse 4T1 breast cancer cells were cultured in complete medium containing 90%DMEM, 10% fetal bovine serum (high quality) and 1% penicillin streptomycin at 37鈩 in a 5% C02 incubator, and cell suspension with cell concentration of 1脳10^7/ml was prepared for use. Thirty healthy BALB/c mice, aged 4 to 6 weeks and weighing 18 to 20 g, were randomly divided into 5 groups, 5 in each group. The ck group was injected with the same amount of normal saline, and the BALB/c mice in the other 4 groups were subcutly inoculated with 0.2ml cell suspension of corresponding concentration (the number of cells was about 200W) on the chest wall of 5-6 intercostocal and lateral abdominal walls. The four groups were named Tnm, Tnm+swim, Tnm+cur and Tnm+union. Each afternoon, the Tnm group and Tnm+swim group received 200ul solution intragastric administration, and the Tnm+cur and Tnm+union group received 200ul curcumin solution dissolved in corn oil (100mg/Kg) intragastric administration. Half an hour after gavage, Tnm+swim and Tnm+union groups were subjected to swimming exercise intervention for 30 minutes, and weight and tumor volume were weighed every two days.,PE150 platform used forbasecalling. sequenced reads were trimmed for adaptorsequence,and masked forlow-complexity or low-qualitysequence,then mapped tomm9 whole genome using HISAT2 v2.0.5. We used HTSeq(0.9.1) statistics to compare the ReadCount values on each gene asthe original expression of thegene, and then used FPKM tostandardize the expression.Difference expression of genes was analyzed by DESeq(1.30.0) with screened
- `grp`: swim

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | grp | 3 | 12/12 | 3 | 0 |
| characteristics_ch1.4.treatment (without grp) + suffix of title | grp | 6 | 12/12 | 0 | 0 |
| title without the grp level | grp | 6 | 9/12 | 0 | 0 |
| grp (without characteristics_ch1.4.treatment) + suffix of title | characteristics_ch1.4.treatment | 12 | 0/12 | 0 | 0 |
| suffix of title | characteristics_ch1.4.treatment | 3 | 0/12 | 0 | 3 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 18, "same_key_mean_r": -0.034, "other_mean_r": 0.016, "difference": -0.051, "permutation_p": 0.8040979510244878, "genes_used": 10159, "status": "not_supported"}
