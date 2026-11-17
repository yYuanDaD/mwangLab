# Review packet A (facts only): GSE144133

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC8355925.paper.md`

## Paper outline

- # Epigenetic rewiring of skeletal muscle enhancers after exercise training supports a role in whole-body function and human health
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Methods  `S2` · methods
- ### Human subjects  `S2.1` · methods
- ### Exercise intervention and collection of biopsies  `S2.2` · methods
- ### Total RNA purification  `S2.3` · methods
- ### RNA-sequencing  `S2.4` · methods
- ### Chromatin IP-sequencing (ChIP-seq)  `S2.5` · methods
- ### GWAS overlap  `S2.6` · methods
- #### Data retrieval from the GWAS catalog  `S2.6.1` · methods
- #### Categorization of GWAS catalog traits  `S2.6.2` · methods
- #### Generation of control SNPs  `S2.6.3` · methods
- #### Overlapping training-responsive enhancer regions and SNP positions  `S2.6.4` · methods
- #### Selecting tag SNPs across disease/trait categories  `S2.6.5` · methods
- #### Statistical analysis  `S2.6.6` · methods
- ## Results  `S3` · results
- ### Gene expression analysis identifies genes regulated after exercise training  `S3.1` · results
- ### Remodeling of enhancer activities after exercise training  `S3.2` · results
- ### Training-responsive enhancers regulate the expression of connected genes  `S3.3` · results
- ### Training-responsive enhancers are enriched for genetic variants identified by GWAS  `S3.4` · results
- ## Discussion  `S4` · discussion
- ### Data statement  `S4.1` · data_availability
- ## Author contributions  `S5` · other
- ## Conflict of interest  `BK1` · other
- ## Appendix ASupplementary data  `BK2` · supplementary
- ## Accession mentions

## Metadata (16 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.participant`: P1: 2; P2: 2; P3: 2; P4: 2; P5: 2; P6: 2; P7: 2; P8: 2
- `characteristics_ch1.2.training`: Untrained: 8; Trained: 8
- `subject`: P1: 2; P2: 2; P3: 2; P4: 2; P5: 2; : 2; P7: 2; P6: 1; P8: 1
- `train`: pre: 8; post: 6; : 2

### Constant columns

- `status`: Public on Jul 20 2021
- `submission_date`: Jan 23 2020
- `last_update_date`: Jul 20 2021
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: vastus lateralis
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: vastus lateralis
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: 20-30 mg of human skeletal muscle tissue was used for purification of total RNA. After lysis of muscle tissue in RLT buffer (Qiagen) by the use of a Tissuelyzer II (Qiagen, 30 hertz for 3x30sec), total RNA was purified using AllPrep DNA/RNA/miRNA Universal Kit (Qiagen). The quality of recovered RNA  ... [592 more characters]
- `data_processing`: Using the Kallisto aligner78 v. 0.46, reads were aligned to the hg38 ENSEMBL release 7979 transcripts, with a transcript support level between 1 and 3,Read summation onto genes and differential expression analysis was performed by sleuth v. 0.3080,Differential expression p-values and Bonferroni corr ... [398 more characters]
- `platform_id`: GPL11154
- `contact_name`: Lars,Roed,Ingerslev
- `contact_email`: ingerslev@sund.ku.dk
- `contact_laboratory`: Integrative Physiology
- `contact_department`: NNF Center for Basic Metabolic Research
- `contact_institute`: Copenhagen University
- `contact_address`: Blegdamsvej 3B
- `contact_city`: Copenhagen
- `contact_zip/postal_code`: 2200
- `contact_country`: Denmark
- `instrument_model`: Illumina HiSeq 2000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE144133,GSE144134
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`

### Samples

| sample | title |
|---|---|
| GSM4281952 | P1_1_R1_RNA |
| GSM4281953 | P1_2_R1_RNA |
| GSM4281954 | P2_1_R1_RNA |
| GSM4281955 | P2_2_R1_RNA |
| GSM4281956 | P3_1_R1_RNA |
| GSM4281957 | P3_2_R1_RNA |
| GSM4281958 | P4_1_R1_RNA |
| GSM4281959 | P4_2_R1_RNA |
| GSM4281960 | P5_1_R1_RNA |
| GSM4281961 | P5_2_R1_RNA |
| GSM4281962 | P6_1_R1_RNA |
| GSM4281963 | P6_2_R1_RNA |
| GSM4281964 | P7_1_R1_RNA |
| GSM4281965 | P7_2_R1_RNA |
| GSM4281966 | P8_1_R1_RNA |
| GSM4281967 | P8_2_R1_RNA |

## Values with exercise words (by column)

- `characteristics_ch1.2.training`: Trained, Untrained
- `extract_protocol_ch1`: 20-30 mg of human skeletal muscle tissue was used for purification of total RNA. After lysis of muscle tissue in RLT buffer (Qiagen) by the use of a Tissuelyzer II (Qiagen, 30 hertz for 3x30sec), total RNA was purified using AllPrep DNA/RNA/miRNA Universal Kit (Qiagen). The quality of recovered RNA was assessed by the Agilent RNA 6000 Nano Kit (Agilent Technologies) and RNA concentration was determined by spectrophotometry using a NanoDrop 2000 (Thermo Scientific).,For RNA-sequencing, 0.5 microgram of total RNA was depleted of rRNA and subsequently used to generate libraries using the TruSeq standard total RNA with Ribo-Zero Gold kit (Illumina). The PCR cycle number for each library amplification was optimized by running 10% of the library DNA in a real-time PCR reaction using Brilliant III Ultra-fast SYBR Green QPCR Master Mix (AH Diagnostic) and a C1000 Thermal cycler (Bio-Rad)
- `data_processing`: Using the Kallisto aligner78 v. 0.46, reads were aligned to the hg38 ENSEMBL release 7979 transcripts, with a transcript support level between 1 and 3,Read summation onto genes and differential expression analysis was performed by sleuth v. 0.3080,Differential expression p-values and Bonferroni corrected q-values were calculated using a likelihood ratio test comparing a model containing only participant information (~ Participant) to a model with participant and training status information (~ Participant + Training),Fold changes were calculated using a Wald-test, as described in the Sleuth manual.,Genome_build: hg38,Supplementary_files_format_and_content: csv file with estimated abundances

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.1.participant | characteristics_ch1.2.training | 8 | 16/16 | 8 | 0 |
| characteristics_ch1.1.participant | train | 8 | 16/16 | 0 | 0 |
| subject | characteristics_ch1.2.training | 8 | 12/14 | 6 | 0 |
| subject | train | 8 | 12/14 | 6 | 0 |
| characteristics_ch1.1.participant (without characteristics_ch1.2.training) + suffix of key | characteristics_ch1.2.training | 16 | 0/16 | 0 | 0 |
| characteristics_ch1.1.participant (without train) + suffix of key | train | 16 | 0/16 | 0 | 0 |
| suffix of key | characteristics_ch1.2.training | 2 | 0/16 | 0 | 2 |
| subject (without characteristics_ch1.2.training) + suffix of key | characteristics_ch1.2.training | 15 | 0/16 | 0 | 1 |
