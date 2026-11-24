# Review packet A (facts only): GSE87748

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC5179501.paper.md`

## Paper outline

- # Muscle Contraction Induces Acute Hydroxymethylation of the Exercise-Responsive Gene Nr4a3
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Materials and Methods  `S2` · methods
- ### Acute Exercise Study  `S2.1` · methods
- ### Total RNA Purification  `S2.2` · methods
- ### RNA Sequencing  `S2.3` · methods
- ### Cell Culture  `S2.4` · methods
- ### Electrical Pulse Stimulation  `S2.5` · methods
- ### Gene Expression Analysis  `S2.6` · methods
- ### DNA Isolation  `S2.7` · methods
- ### DNA Methylation Analysis  `S2.8` · methods
- ### DNA Hydroxymethylation Analysis  `S2.9` · methods
- ### Data Analysis  `S2.10` · methods
- ## Results  `S3` · results
- ### Identification of Exercise-Responsive Genes in Humans  `S3.1` · results
- ### EPS Mimics the Effect of Exercise on Nr4a3  `S3.2` · results
- ### EPS Induces Transient Nr4a3 Promoter Demethylation  `S3.3` · results
- ### EPS Rapidly Increases Hydroxymethylation of the Nr4a3 Promoter  `S3.4` · results
- ## Discussion  `S4` · discussion
- ## Data Availability  `S5` · data_availability
- ## Author Contributions  `S6` · other
- ## Conflict of Interest Statement  `S7` · other
- ## Acknowledgments  `S8` · other
- ## Funding  `S9` · other
- ## Supplementary Material  `S10` · supplementary
- ## Accession mentions

## Metadata (20 samples)

### Grouping columns (level: count)

- `source_name_ch1`: Muscle biopsy 240 min after exercise: 10; Muscle biopsy before exercise: 10
- `characteristics_ch1.1.treatment`: exercise: 10; control: 10
- `characteristics_ch1.2.time`: 240 min: 10; Basal: 10
- `characteristics_ch1.3.individual`: 4: 2; 5: 2; 7: 2; 8: 2; 9: 2; 11: 2; 13: 2; 14: 2; 15: 2; 16: 2
- `subject`: S04: 2; S05: 2; S07: 2; S08: 2; S09: 2; S11: 2; S13: 2; S14: 2; S15: 2; S16: 2
- `time`: Post: 10; Pre: 10

### Constant columns

- `status`: Public on Feb 22 2017
- `submission_date`: Oct 07 2016
- `last_update_date`: May 15 2019
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: Skeletal Muscle
- `treatment_protocol_ch1`: Skeletal muscle biopsies collected from danish male subjects (age 22.6+/- 0.52, body mas index 23.08+/-0.87) at fasting conditions at rest and four hours after completion of a 15-minute exercise bout. Biopsies were immediately snap-frozen in liquid nitrogen and stored at -80掳C for further analyses.
- `growth_protocol_ch1`: Human subjects were fasting at biopsy collection
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNAs were purified from skeletal muscle biopsies with the AllPrep DNA/RNA/miRNA Universal Kit (Qiagen) following manufacturer鈥檚 instructions. The quality of recovered RNA was assessed by using the Agilent RNA 6000 Nano Kit (Agilent Technologies). RNA concentration was determined by spectrophot ... [273 more characters]
- `data_processing`: Reads were trimmed for adapters and low quality flanking ends using Trim Galore v0.3.7 and Cutadapt v1.4.2 on default settings,Pre-processed reads were mapped to the human reference genome (hg19) with tophat2 using the 鈥--b2-very-sensitive鈥 setting,Gene coverages were computed with featureCounts and ... [388 more characters]
- `platform_id`: GPL16791
- `contact_name`: Lars,Roed,Ingerslev
- `contact_email`: ingerslev@sund.ku.dk
- `contact_laboratory`: Integrative Physiology
- `contact_department`: NNF Center for Basic Metabolic Research
- `contact_institute`: Copenhagen University
- `contact_address`: Blegdamsvej 3B
- `contact_city`: Copenhagen
- `contact_zip/postal_code`: 2200
- `contact_country`: Denmark
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE87748,GSE87749
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM2339828 | 4_1_240 |
| GSM2339829 | 4_1_Basal |
| GSM2339830 | 5_1_240 |
| GSM2339831 | 5_1_Basal |
| GSM2339832 | 7_1_240 |
| GSM2339833 | 7_1_Basal |
| GSM2339834 | 8_1_240 |
| GSM2339835 | 8_1_Basal |
| GSM2339836 | 9_1_240 |
| GSM2339837 | 9_1_Basal |
| GSM2339838 | 11_1_240 |
| GSM2339839 | 11_1_Basal |
| GSM2339840 | 13_1_240 |
| GSM2339841 | 13_1_Basal |
| GSM2339842 | 14_1_240 |
| GSM2339843 | 14_1_Basal |
| GSM2339844 | 15_1_240 |
| GSM2339845 | 15_1_Basal |
| GSM2339846 | 16_1_240 |
| GSM2339847 | 16_1_Basal |

## Values with exercise words (by column)

- `source_name_ch1`: Muscle biopsy 240 min after exercise, Muscle biopsy before exercise
- `characteristics_ch1.1.treatment`: exercise
- `treatment_protocol_ch1`: Skeletal muscle biopsies collected from danish male subjects (age 22.6+/- 0.52, body mas index 23.08+/-0.87) at fasting conditions at rest and four hours after completion of a 15-minute exercise bout. Biopsies were immediately snap-frozen in liquid nitrogen and stored at -80掳C for further analyses.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.3.individual | source_name_ch1 | 10 | 20/20 | 10 | 0 |
| subject | source_name_ch1 | 10 | 20/20 | 10 | 0 |
| characteristics_ch1.3.individual | characteristics_ch1.1.treatment | 10 | 20/20 | 10 | 0 |
| subject | characteristics_ch1.1.treatment | 10 | 20/20 | 10 | 0 |
| title without the characteristics_ch1.2.time level | characteristics_ch1.2.time | 10 | 20/20 | 10 | 0 |
| characteristics_ch1.3.individual | characteristics_ch1.2.time | 10 | 20/20 | 10 | 0 |
| subject | characteristics_ch1.2.time | 10 | 20/20 | 10 | 0 |
| characteristics_ch1.3.individual | time | 10 | 20/20 | 10 | 0 |
