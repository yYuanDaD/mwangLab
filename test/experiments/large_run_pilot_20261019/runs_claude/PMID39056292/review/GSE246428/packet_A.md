# Review packet A (facts only): GSE246428

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC11281781.paper.md`

## Paper outline

- # SPAG7 deletion causes intrauterine growth restriction, resulting in adulthood obesity and metabolic dysfunction
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### SPAG7-deficient animals are obese and insulin resistant  `S2.1` · results
- ### Obesity in SPAG7-deficient animals is caused by decreased energy expenditure  `S2.2` · results
- ### SPAG7-deficient animals display decreased exercise capacity and muscle function  `S2.3` · results
- ### Induction of SPAG7-deficiency after early development does not cause obesity or skeletal muscle abnormalities  `S2.4` · results
- ### SPAG7-deficiency causes placental insufficiency and intrauterine growth restriction  `S2.5` · results
- ## Discussion  `S3` · discussion
- ## Materials and methods  `S4` · methods
- ### Mice  `S4.1` · methods
- ### Generation of Spag7 cKO mouse model using the CRISPR/Cas9 technology  `S4.2` · methods
- ### Western blotting  `S4.3` · methods
- ### Quantitative RT-PCR  `S4.4` · methods
- ### Bone mineral density and body length  `S4.5` · methods
- ### Circulating lipid and liver enzyme analysis  `S4.6` · methods
- ### In vivo metabolic studies  `S4.7` · methods
- ### Adipose tissue analysis  `S4.8` · methods
- ### Triglyceride content assays  `S4.9` · methods
- ### Food intake  `S4.10` · methods
- ### Metabolic cage studies  `S4.11` · methods
- ### Treadmill endurance test  `S4.12` · methods
- ### In vivo muscle max force generation  `S4.13` · methods
- ### Histology and immunohistochemistry  `S4.14` · methods
- ### Skeletal muscle SDH activity stain  `S4.15` · methods
- ### Skeletal muscle citrate synthase activity  `S4.16` · methods
- ### RNAseq sample preparation  `S4.17` · methods
- ### RNA sequencing  `S4.18` · methods
- ### Transcriptomic analysis  `S4.19` · methods
- ### iSPAG7 KO study design  `S4.20` · methods
- ### Placenta histological analysis  `S4.21` · methods
- ### mtDNA copy number  `S4.22` · methods
- ### Statistical analysis  `S4.23` · methods
- ## Funding Information  `BK1` · other
- ## Additional files  `BK3` · supplementary
- ## Data availability  `DA` · data_availability
- ## Supplementary material  `SUPP` · supplementary
- ## Accession mentions

## Metadata (9 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.genotype`: WT: 5; Spag7 KO: 4
- `genotype`: WT: 5; KO: 4

### Constant columns

- `status`: Public on Nov 01 2023
- `submission_date`: Oct 27 2023
- `last_update_date`: Nov 01 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: gastrocnemius muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: gastrocnemius muscle
- `molecule_ch1`: polyA RNA
- `extract_protocol_ch1`: Tissue was pulverized and total RNA was extracted using Qiagen Rneasy Plus Universal mini kit following manufacturer鈥檚 instructions (Qiagen, Hilden, Germany). The RNA samples were quantified using Qubit 2.0 Fluorometer (ThermoFisher Scientific, Waltham, MA, USA) and RNA integrity was checked using T ... [847 more characters]
- `data_processing`: The raw FASTQ files were processed using an internal pipeline, Rnaseq Experiment DAshboard, utilizing STAR (v2.7.3a)  and Salmon (v1.5.2) to map reads to the mouse genome and transcriptome (GRCm39, Ensembl release 106), respectively.,The Salmon transcript abundance estimates were aggregated to the g ... [419 more characters]
- `platform_id`: GPL24247
- `contact_name`: Mary,,Piper
- `contact_institute`: Pfizer Inc
- `contact_address`: 1 Portland St
- `contact_city`: Cambridge
- `contact_state`: Massachusetts
- `contact_zip/postal_code`: 2139
- `contact_country`: USA
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE246428
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM7868730 | sample2_spag7_WT | X2 |
| GSM7868731 | sample3_spag7_KO | X3 |
| GSM7868732 | sample4_spag7_WT | X4 |
| GSM7868733 | sample5_spag7_WT | X5 |
| GSM7868734 | sample6_spag7_WT | X6 |
| GSM7868735 | sample7_spag7_KO | X7 |
| GSM7868736 | sample8_spag7_WT | X8 |
| GSM7868737 | sample9_spag7_KO | X9 |
| GSM7868738 | sample10_spag7_KO | X10 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of description | characteristics_ch1.1.genotype | 9 | 0/9 | 0 | 0 |
| suffix of description | genotype | 9 | 0/9 | 0 | 0 |
| characteristics_ch1.1.genotype (without genotype) + suffix of description | genotype | 9 | 0/9 | 0 | 0 |
