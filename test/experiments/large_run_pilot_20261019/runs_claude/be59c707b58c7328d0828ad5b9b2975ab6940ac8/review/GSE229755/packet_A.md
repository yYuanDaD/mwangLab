# Review packet A (facts only): GSE229755

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC10318136.paper.md`

## Paper outline

- # Multi-omics analysis explores the effect of chronic exercise on liver metabolic reprogramming in mice
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## 1 Introduction  `S1` · introduction
- ## 2 Materials and methods  `S2` · methods
- ### 2.1 Experimental animals  `S2.1` · methods
- ### 2.2 Chronic exercise protocol  `S2.2` · methods
- ### 2.3 Tissue collection  `S2.3` · methods
- ### 2.4 Transcriptomics analysis  `S2.4` · methods
- ### 2.5 Liquid chromatography-tandem mass spectrometry analysis  `S2.5` · methods
- ### 2.6 Proteomics and acetyl-proteomics analysis  `S2.6` · methods
- ### 2.7 Metabolomics analysis  `S2.7` · methods
- ## 3 Results  `S3` · results
- ### 3.1 Chronic exercise altered the transcriptome of liver tissue in mice  `S3.1` · results
- ### 3.2 Proteomics changes  `S3.2` · results
- ### 3.3 Correlation analysis between transcriptome and proteome  `S3.3` · results
- ### 3.4 Identification of acetylation landscape in the mouse liver  `S3.4` · results
- ### 3.5 Effect of chronic exercise on liver metabolites in mice  `S3.5` · results
- ### 3.6 Correlation analysis between proteome and metabolome  `S3.6` · results
- ## 4 Discussion  `S4` · discussion
- ## Funding Statement  `S5` · other
- ## Data availability statement  `S6` · data_availability
- ## Ethics statement  `S7` · other
- ## Author contributions  `S8` · other
- ## Conflict of interest  `S9` · other
- ## Publisher’s note  `S10` · other
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.treatment`: sedentary: 6; chronic exercise, running for 6 weeks: 6
- `description`: control, sedentary mice: 6; chronic exercise, exercise model: 6
- `grp`: Con: 6; Exe: 6

### Constant columns

- `status`: Public on Jul 12 2023
- `submission_date`: Apr 14 2023
- `last_update_date`: Jul 12 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: liver
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: liver
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNAs were isolated from liver tissue samples with TRIzol reagent.,Based on the DNBseq platform (PE150 strategy), sequencing was performed.
- `data_processing`: To obtain clean reads from RNA-sequencing results, sequence with low quality including adapter sequences, sequences with quality score < 20, sequences with N base rate of raw reads >10% and sequence less than 25bp were removed.,HISAT was used to align clean reads with the reference genome GCF_000001 ... [134 more characters]
- `platform_id`: GPL23479
- `contact_name`: Jianxin,,Wu
- `contact_institute`: Beijing Municipal Key Laboratory of Child Development and Nutriomics, Capital Institute of Pediatrics
- `contact_address`: No. 2, Yabao Road, Chaoyang District
- `contact_city`: Beijing
- `contact_zip/postal_code`: 100020
- `contact_country`: China
- `instrument_model`: BGISEQ-500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE229755
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM7177389 | Con_L1 |
| GSM7177390 | Con_L2 |
| GSM7177391 | Con_L3 |
| GSM7177392 | Con_L4 |
| GSM7177393 | Con_L5 |
| GSM7177394 | Con_L6 |
| GSM7177395 | Exe_L1 |
| GSM7177396 | Exe_L2 |
| GSM7177397 | Exe_L3 |
| GSM7177398 | Exe_L4 |
| GSM7177399 | Exe_L5 |
| GSM7177400 | Exe_L6 |

## Values with exercise words (by column)

- `title`: Exe_L1, Exe_L2, Exe_L3, Exe_L4, Exe_L5, Exe_L6
- `characteristics_ch1.1.treatment`: chronic exercise, running for 6 weeks, sedentary
- `description`: chronic exercise, exercise model, control, sedentary mice
- `supplementary_file_1`: ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7177nnn/GSM7177395/suppl/GSM7177395_Exe_L1.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7177nnn/GSM7177396/suppl/GSM7177396_Exe_L2.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7177nnn/GSM7177397/suppl/GSM7177397_Exe_L3.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7177nnn/GSM7177398/suppl/GSM7177398_Exe_L4.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7177nnn/GSM7177399/suppl/GSM7177399_Exe_L5.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM7177nnn/GSM7177400/suppl/GSM7177400_Exe_L6.txt.gz
- `grp`: Exe

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.1.treatment | 6 | 12/12 | 6 | 0 |
| suffix of title | description | 6 | 12/12 | 6 | 0 |
| title without the grp level | grp | 6 | 12/12 | 6 | 0 |
| suffix of title | grp | 6 | 12/12 | 6 | 0 |
| description (without characteristics_ch1.1.treatment) + suffix of title | characteristics_ch1.1.treatment | 12 | 0/12 | 0 | 0 |
| grp (without characteristics_ch1.1.treatment) + suffix of title | characteristics_ch1.1.treatment | 12 | 0/12 | 0 | 0 |
| characteristics_ch1.1.treatment (without description) + suffix of title | description | 12 | 0/12 | 0 | 0 |
| grp (without description) + suffix of title | description | 12 | 0/12 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 6, "same_key_mean_r": -0.083, "other_mean_r": 0.016, "difference": -0.099, "permutation_p": 0.7891054472763618, "genes_used": 6159, "status": "not_supported"}
