# Review packet A (facts only): GSE198827

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC9876571.paper.md`

## Paper outline

- # LSD1 defines the fiber type-selective responsiveness to environmental stress in skeletal muscle
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Muscle-specific LSD1 depletion exacerbates dexamethasone-induced muscle atrophy  `S2.1` · results
- ### Oxidative fiber ratio is increased in the fast-dominant muscle in LSD1-mKO mice after Dex administration  `S2.2` · results
- ### Atrophy- and slow fiber-associated genes are upregulated in fast-dominant muscles in Dex-treated LSD1-mKO mice  `S2.3` · results
- ### LSD1 regulates atrophy-associated genes by promoting the nuclear function of Foxk1  `S2.4` · results
- ### Muscle-specific LSD1 depletion promotes the hypertrophy of Sol muscle and the muscle endurance after voluntary exercise  `S2.5` · results
- ### LSD1 depletion upregulates the expression of ERRγ and mitochondrial metabolism genes after voluntary exercise  `S2.6` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### Reagents and antibodies  `S4.1` · methods
- ### Cell culture  `S4.2` · methods
- ### Animal studies  `S4.3` · methods
- ### Voluntary wheel running  `S4.4` · methods
- ### Muscle function tests  `S4.5` · methods
- ### Histological analysis  `S4.6` · methods
- ### Western blot and co-IP analyses  `S4.7` · methods
- ### Separation of nuclear and cytoplasmic fractions  `S4.8` · methods
- ### Quantitative RT-PCR  `S4.9` · methods
- ### Poly (A) RNA-seq analysis  `S4.10` · methods
- ### ChIP-qPCR  `S4.11` · methods
- ### Immunocytochemistry  `S4.12` · methods
- ### Construction of lentiviral expression vectors and their transduction  `S4.13` · methods
- ### Tabula Muris Senis  `S4.14` · methods
- ### Human muscle transcriptome data  `S4.15` · methods
- ### Statistical analyses  `S4.16` · methods
- ### Materials availability statement  `S4.17` · methods
- ## Acknowledgements  `S5` · other
- ## Appendix 1  `S6` · other
- ## Funding Statement  `S7` · other
- ## Contributor Information  `S8` · other
- ## Funding Information  `S9` · other
- ## Additional information  `S10` · supplementary
- ## Additional files  `S11` · supplementary
- ## Data availability  `S12` · data_availability
- ## Supplementary material  `SUPP` · supplementary
- ## Accession mentions

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.mouse genotype`: WT: 3; LSD1-mKO: 3
- `geno`: WT: 3; KO: 3

### Constant columns

- `status`: Public on Jan 23 2023
- `submission_date`: Mar 17 2022
- `last_update_date`: Jan 23 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: mouse soleus muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.mouse genotype`: C57BL/6
- `characteristics_ch1.2.treatment`: VWR training
- `characteristics_ch1.3.tissue`: mouse soleus muscle
- `treatment_protocol_ch1`: Eight-week-old control or LSD1-mKO mice were single-housed in cages with free access to a vertical running wheel (Shinano Seisakusho) for 38 days. After three days of familiarization,  LSD1-KO was induced by  tamoxifen injection at a dose of 75 mg/kg for five consecutive days, and running distance w ... [36 more characters]
- `growth_protocol_ch1`: Mice were maintained in a temperature-controlled animal facility with a 12-h light/12-h dark cycle and fed ad libitum on a regular diet. All procedures were conducted in accordance with the guidelines of the Animal Care and Use Committee of Kumamoto University.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA from the muscles were extracted using a Trizol reagent (Invitrogen). mRNA was purified using NEBNext Poly(A) mRNA Magnetic Isolation Module (NEB).,cDNA library for sequencing was synthesized using NEB Next Ultra DNA Library Prep Kit for Illumina (NEB) and was sequenced on NextSeq 500 seque ... [45 more characters]
- `data_processing`: Resulting reads were aligned to the UCSC mm10 reference genome by using STAR.,DESeq2 was used for quantification of gene expression changes. Top 1000 genes showing differential expression between the WT and KO mice were extracted from the genes with mean TPM >1 by using median absolute deviation (MA ... [96 more characters]
- `platform_id`: GPL19057
- `contact_name`: Hirotaka,,Araki
- `contact_email`: hiroaraki007@gmail.com
- `contact_phone`: 81963736801
- `contact_laboratory`: Department of Medical Cell Biology
- `contact_department`: Institute of Molecular Embryology and Genetics
- `contact_institute`: Kumamoto University
- `contact_address`: 2-2-1 Honjo, Chuo-ku
- `contact_city`: Kumamoto
- `contact_state`: Kumamoto
- `contact_zip/postal_code`: 860-0811
- `contact_country`: Japan
- `instrument_model`: NextSeq 500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE198827,GSE198911
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`

### Samples

| sample | title |
|---|---|
| GSM5957513 | 1_WT1 Sol VWR |
| GSM5957514 | 2_WT2 Sol VWR |
| GSM5957515 | 3_WT3 Sol VWR |
| GSM5957516 | 4_LSD1-mKO1 Sol VWR |
| GSM5957517 | 5_LSD1-mKO2 Sol VWR |
| GSM5957518 | 6_LSD1-mKO3 Sol VWR |

## Values with exercise words (by column)

- `characteristics_ch1.2.treatment`: VWR training
- `treatment_protocol_ch1`: Eight-week-old control or LSD1-mKO mice were single-housed in cages with free access to a vertical running wheel (Shinano Seisakusho) for 38 days. After three days of familiarization,  LSD1-KO was induced by  tamoxifen injection at a dose of 75 mg/kg for five consecutive days, and running distance was measured during the next 30 days.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of key | characteristics_ch1.1.mouse genotype | 6 | 0/6 | 0 | 0 |
| geno (without characteristics_ch1.1.mouse genotype) + suffix of key | characteristics_ch1.1.mouse genotype | 6 | 0/6 | 0 | 0 |
| suffix of key | geno | 6 | 0/6 | 0 | 0 |
| characteristics_ch1.1.mouse genotype (without geno) + suffix of key | geno | 6 | 0/6 | 0 | 0 |
