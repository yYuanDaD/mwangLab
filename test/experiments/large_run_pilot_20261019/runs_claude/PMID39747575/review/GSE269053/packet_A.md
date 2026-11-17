# Review packet A (facts only): GSE269053

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC11696687.paper.md`

## Paper outline

- # Two-hit mouse model of heart failure with preserved ejection fraction combining diet-induced obesity and renin-mediated hypertension
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Development and optimization of AAV-mediated renin delivery to achieve hypertension-related LV hypertrophy and remodeling in mice  `S2.1` · results
- ### The HFD-Renin model results in features of HFpEF, including systemic metabolic derangements, LV hypertrophy, diastolic dysfunction, and exercise intolerance  `S2.2` · results
- ### Two-hit HFpEF model results in cardiac fibrosis  `S2.3` · results
- ### Transcriptomic and metabolomic changes mirror observations in human HFpEF  `S2.4` · results
- ### Human HFpEF standard-of-care therapy improves a subset of pathophysiologic parameters in the HFD-Renin model  `S2.5` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### In vivo studies  `S4.1` · methods
- ### AAV8-Renin generation and treatment  `S4.2` · methods
- ### Telemetry study  `S4.3` · methods
- ### Mouse echocardiography  `S4.4` · methods
- ### Exercise testing  `S4.5` · methods
- ### Metabolic measurements  `S4.6` · methods
- ### Histology  `S4.7` · methods
- ### RNA isolation and qRT-PCR  `S4.8` · methods
- ### RNA-seq library preparation, sequencing, and analysis  `S4.9` · methods
- ### Statistics  `S4.10` · methods
- ### Study approval  `S4.11` · methods
- ## Electronic supplementary material  `S5` · supplementary
- ## Author contributions  `BK1` · other
- ## Funding  `BK2` · other
- ## Data availability  `DA` · data_availability
- ## Declarations  `BK3` · other
- ## Accession mentions

## Metadata (21 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.diet`: HFD: 11; chow: 10
- `characteristics_ch1.2.treatment`: Renin: 11; novirus: 10
- `diet`: HFD: 11; chow: 10
- `virus`: Renin: 11; novirus: 10
- `grp`: chow_Renin: 6; HFD_novirus: 6; HFD_Renin: 5; chow_novirus: 4

### Constant columns

- `status`: Public on Jan 01 2025
- `submission_date`: Jun 04 2024
- `last_update_date`: Jan 01 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Heart
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Heart
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was isolated using the RNeasy Mini Kit (QIAGEN) and the RNase-Free DNase Set (QIAGEN) according to the manufacturer鈥檚 instructions. cDNA was synthesized using the Affinity Script cDNA Synthesis Kit (Agilent Technologies) with 0.25 渭g total RNA.,RNA library preparations and sequencing react ... [99 more characters]
- `data_processing`: We used Salmon v1.10.2 to count reads in GRCm38 (mm10) reference transcripts,The counts were summarized at gene level and differentially expressed genes were identified with DESeq2 1.40.2,Assembly: GRCm38,Supplementary files format and content: *raw_counts.tsv: Salmon transcript-level count for the  ... [160 more characters]
- `platform_id`: GPL24247
- `contact_name`: Daniel,,Kelly
- `contact_email`: dankelly@pennmedicine.upenn.edu
- `contact_laboratory`: Kelly Lab
- `contact_department`: Penn Cardiovascular Institute
- `contact_institute`: University of Pennsylvania
- `contact_address`: 3400 Civic Center Blvd
- `contact_city`: Philadelphia
- `contact_state`: PA
- `contact_zip/postal_code`: 19104
- `contact_country`: USA
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE269053
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM8305606 | Heart, chow, novirus, rep1 |
| GSM8305607 | Heart, chow, novirus, rep2 |
| GSM8305608 | Heart, chow, novirus, rep3 |
| GSM8305609 | Heart, chow, novirus, rep4 |
| GSM8305610 | Heart, chow, Renin, rep1 |
| GSM8305611 | Heart, chow, Renin, rep2 |
| GSM8305612 | Heart, chow, Renin, rep3 |
| GSM8305613 | Heart, chow, Renin, rep4 |
| GSM8305614 | Heart, chow, Renin, rep5 |
| GSM8305615 | Heart, chow, Renin, rep6 |
| GSM8305616 | Heart, HFD, novirus, rep1 |
| GSM8305617 | Heart, HFD, novirus, rep2 |
| GSM8305618 | Heart, HFD, novirus, rep3 |
| GSM8305619 | Heart, HFD, novirus, rep4 |
| GSM8305620 | Heart, HFD, novirus, rep5 |
| GSM8305621 | Heart, HFD, novirus, rep6 |
| GSM8305622 | Heart, HFD, Renin, rep1 |
| GSM8305623 | Heart, HFD, Renin, rep2 |
| GSM8305624 | Heart, HFD, Renin, rep3 |
| GSM8305625 | Heart, HFD, Renin, rep4 |
| GSM8305626 | Heart, HFD, Renin, rep5 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the grp level | grp | 6 | 21/21 | 4 | 0 |
| suffix of title | grp | 6 | 21/21 | 4 | 0 |
| title without the characteristics_ch1.1.diet level | characteristics_ch1.1.diet | 12 | 18/21 | 9 | 0 |
| characteristics_ch1.2.treatment (without characteristics_ch1.1.diet) + suffix of title | characteristics_ch1.1.diet | 12 | 18/21 | 9 | 0 |
| virus (without characteristics_ch1.1.diet) + suffix of title | characteristics_ch1.1.diet | 12 | 18/21 | 9 | 0 |
| grp (without characteristics_ch1.1.diet) + suffix of title | characteristics_ch1.1.diet | 12 | 18/21 | 9 | 0 |
| title without the characteristics_ch1.2.treatment level | characteristics_ch1.2.treatment | 12 | 18/21 | 9 | 0 |
| characteristics_ch1.1.diet (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 12 | 18/21 | 9 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the grp level", "across": "_across", "within": [], "n_same_key_pairs": 28, "same_key_mean_r": 0.047, "other_mean_r": -0.01, "difference": 0.057, "permutation_p": 0.010494752623688156, "genes_used": 10904, "status": "not_supported"}
