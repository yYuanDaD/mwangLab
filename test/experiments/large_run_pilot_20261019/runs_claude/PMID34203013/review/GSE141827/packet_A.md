# Review packet A (facts only): GSE141827

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261028\papers\PMC8235325.paper.md`

## Paper outline

- # Genome-Wide Atlas of Promoter Expression Reveals Contribution of Transcribed Regulatory Elements to Genetic Control of Disuse-Mediated Atrophy of Skeletal Muscle
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## 1. Introduction  `S1` · introduction
- ## 2. Materials and Methods  `S2` · methods
- ### 2.1. Animals  `S2.1` · methods
- ### 2.2. Experimental Design  `S2.2` · methods
- ### 2.3. Immunochemistry  `S2.3` · methods
- ### 2.4. Morphometric and Statistical Analysis  `S2.4` · methods
- ### 2.5. RNA Isolation  `S2.5` · methods
- ### 2.6. CAGE-Seq  `S2.6` · methods
- ### 2.7. Data Analysis  `S2.7` · methods
- #### 2.7.1. Quality Control  `S2.7.1` · methods
- #### 2.7.2. Genome, Annotation, and Indexing  `S2.7.2` · methods
- #### 2.7.3. Read Mapping  `S2.7.3` · methods
- #### 2.7.4. CTSS Aggregation  `S2.7.4` · methods
- #### 2.7.5. TSS Peaks  `S2.7.5` · methods
- #### 2.7.6. Enhancers  `S2.7.6` · methods
- #### 2.7.7. Annotation of TSS Peaks to Genes and Enhancers  `S2.7.7` · methods
- #### 2.7.8. Differentially Expressed Peaks, Genes, and Enhancers  `S2.7.8` · methods
- #### 2.7.9. Gene Set Enrichment Analysis (GSEA)  `S2.7.9` · methods
- ## 3. Results and Discussion  `S3` · results
- ### 3.1. Morphometric Analysis Confirms Distinct Disuse Associated Remodeling in Slow, but Not Fast Muscles  `S3.1` · results
- ### 3.2. Integrative Database of Rat’s Regulatory Elements with a Focus on Muscles  `S3.2` · results
- ### 3.3. Muscle Atrophy and Recovery are Associated with Large Changes in the Unique Gene Set Expression Profiles, with Distinct Dynamics on Each Stage  `S3.3` · results
- ### 3.4. Gene Enrichment Analysis Reveals that Adaption to Disuse Processes in Slow and Fast Muscles is Mediated by Different Molecular Pathways  `S3.4` · results
- ### 3.5. Tissue-Specific Intergenic TSS Show Different Patterns in Slow and Fast Muscles and Widely Co-Express with Coding Genes in Response to Disuse  `S3.5` · results
- ### 3.6. Alternative Usage of Dominating Transcription Starting Sites in Differentially Expressed Genes  `S3.6` · results
- ### 3.7. Expression of Transcribed Enhancers in Rat Skeletal Muscles is Linked to Disuse-Recovery Cycle  `S3.7` · results
- #### 3.7.1. Differentially Expressed Enhancers Mediate Muscle-Specific Transcription Program  `S3.7.1` · results
- #### 3.7.2. Switch ON/OFF Enhancers on First Day of Recovery (R1)  `S3.7.2` · results
- ## 4. Conclusions  `S4` · conclusion
- ## Abbreviations  `S5` · other
- ## Supplementary Materials  `S6` · supplementary
- ## Author Contributions  `S7` · other
- ## Funding  `S8` · other
- ## Institutional Review Board Statement  `S9` · other
- ## Informed Consent Statement  `S10` · other
- ## Data Availability Statement  `S11` · data_availability
- ## Conflicts of Interest  `S12` · other
- ## Accession mentions

## Metadata (42 samples)

### Grouping columns (level: count)

- `characteristics_ch1.0.tissue`: soleus muscle: 21; EDL muscle: 21
- `characteristics_ch1.1.protocol`: unloading 24 hours: 6; control: 6; unloading 3 days: 6; unloading 7 days: 6; unloading 7 days; recovery 24 hours: 6; unloading 7 days; recovery 3 days: 6; unloading 7 days; recovery 7 days: 6
- `tissue`: Sol: 21; EDL: 21
- `protocol`: D1: 6; CTRL: 6; D3: 6; D7: 6; R1: 6; R3: 6; R7: 6

### Constant columns

- `status`: Public on Jun 17 2021
- `submission_date`: Dec 11 2019
- `last_update_date`: Jun 17 2021
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: hindlimb
- `organism_ch1`: Rattus norvegicus
- `taxid_ch1`: 10116
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted from EDL and Soleus muscles using RNeasy Fibrous Tissue Mini Kit QIAGEN,5 碌g of total RNA RIN鈮7 processed into cDNA by reverse transcriptase. CAGE libraries prepared according to Murata et al., 2014 (doi: 10.1007/978-1-4939-0805-9_7).
- `description`: nAnTi-CAGE
- `data_processing`: Reads were trimmed using fastx_trimmer and removeN scripts from Moirai pipeline (http://fantom.gsc.riken.jp/software/). Adapters were removed by using Trimmomatic-0.38,Trimmed reads mapped on Rnor_6.0 Ensembl genome assembly for Rattus norvegicus using BWA, unmapped reads remapped by Hisat2 and merg ... [805 more characters]
- `platform_id`: GPL18694
- `contact_name`: Ruslan,,Deviatiiarov
- `contact_email`: r.deviatiiarov.ek@juntendo.ac.jp
- `contact_phone`: +81 80-6292-5289
- `contact_department`: Intractable Disease Research Center
- `contact_institute`: Juntendo University
- `contact_address`: Hongo 2-1-1, Bunkyo-ku
- `contact_city`: Tokyo
- `contact_zip/postal_code`: 113-8421
- `contact_country`: Japan
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE141827
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `characteristics_ch1.2.lib.sizes`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM4213782 | U24_Sol |
| GSM4213783 | U6_EDL |
| GSM4213784 | U6_Sol |
| GSM4213785 | U7_EDL |
| GSM4213786 | U7_Sol |
| GSM4213787 | U8_EDL |
| GSM4213788 | U8_Sol |
| GSM4213789 | U10_Sol |
| GSM4213790 | U25_EDL |
| GSM4213791 | U25_Sol |
| GSM4213792 | U26_EDL |
| GSM4213793 | U26_Sol |
| GSM4213794 | U9_EDL |
| GSM4213795 | U9_Sol |
| GSM4213796 | U11_EDL |
| GSM4213797 | U11_Sol |
| GSM4213798 | U1_EDL |
| GSM4213799 | U1_Sol |
| GSM4213800 | U2_EDL |
| GSM4213801 | U2_Sol |
| GSM4213802 | U3_Sol |
| GSM4213803 | U18_EDL |
| GSM4213804 | U18_Sol |
| GSM4213805 | U20_EDL |
| GSM4213806 | U20_Sol |
| GSM4213807 | U21_EDL |
| GSM4213808 | U21_Sol |
| GSM4213809 | U4_Sol |
| GSM4213810 | U12_EDL |
| GSM4213811 | U12_Sol |
| GSM4213812 | U13_Sol |
| GSM4213813 | U16_EDL |
| GSM4213814 | U16_Sol |
| GSM4213815 | U5_EDL |
| GSM4213816 | U5_Sol |
| GSM4213817 | U10_EDL |
| GSM4213818 | U13_EDL |
| GSM4213819 | U19_EDL |
| GSM4213820 | U19_Sol |
| GSM4213821 | U24_EDL |
| GSM4213822 | U3_EDL |
| GSM4213823 | U4_EDL |

## Values with exercise words (by column)

- `source_name_ch1`: hindlimb
- `characteristics_ch1.1.protocol`: unloading 24 hours, unloading 3 days, unloading 7 days, unloading 7 days; recovery 24 hours, unloading 7 days; recovery 3 days, unloading 7 days; recovery 7 days

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the tissue level | tissue | 21 | 42/42 | 21 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the tissue level", "across": "_across", "within": [], "n_same_key_pairs": 21, "same_key_mean_r": 0.201, "other_mean_r": -0.008, "difference": 0.209, "permutation_p": 0.0004997501249375312, "genes_used": 6112, "status": "supported"}
