# Review packet A (facts only): GSE114062

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC6072066.paper.md`

## Paper outline

- # Brain region-dependent gene networks associated with selective breeding for increased voluntary wheel-running behavior
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Materials and methods  `S2` · methods
- ### Animal experiments, sampling and sequencing  `S2.1` · methods
- ### Differential expression analysis  `S2.2` · methods
- ### Functional, interacting, and regulatory network analyses  `S2.3` · methods
- ## Results and discussion  `S3` · results
- ### Locomotor and sequencing statistics  `S3.1` · results
- ### Voluntary activity line-by-brain region interaction effects on the transcriptome  `S3.2` · results
- ### Functional analysis of voluntary activity line-by-region interaction effects  `S3.3` · results
- ### Functional analysis of voluntary activity lines within brain region  `S3.4` · results
- ### Interaction networks of voluntary activity lines within brain region  `S3.5` · results
- ### Brain-region independent effect of activity line  `S3.6` · results
- ### Main effect of brain region on gene expression  `S3.7` · results
- ### Regulatory networks of brain-region dependent and independent activity line effects  `S3.8` · results
- ## Conclusions  `S4` · conclusion
- ## Supporting information  `S5` · supplementary
- ## Data Availability  `S6` · data_availability
- ## Funding Statement  `S7` · other
- ## Accession mentions

## Metadata (15 samples)

### Grouping columns (level: count)

- `source_name_ch1`: cerebellum: 8; striatum: 7
- `characteristics_ch1.1.condition`: Control: 8; Selected: 7
- `characteristics_ch1.3.tissue`: cerebellum: 8; striatum: 7
- `description`: Cerebellum was obtained and RNA extracted using standards protocols  (Gibbons et al. 2014, Behavioural brain research, 272: 131-40.): 8; Striatum was obtained and RNA extracted using standards protocols  (Gibbons et al. 2014, Behavioural brain research, 272: 131-40.): 7
- `region`: Ce: 8; St: 7
- `line`: Co: 8; Hi: 7

### Constant columns

- `status`: Public on Dec 25 2018
- `submission_date`: May 04 2018
- `last_update_date`: Dec 25 2018
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: Hsd:ICR
- `characteristics_ch1.2.Sex`: male
- `characteristics_ch1.4.age`: 6 weeks
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Brain was extracted from each mouse and the whole striatum and cerebellum were dissected, snap frozen on dry ice and stored in a centrifuge tube at -80掳C following proven protocols (Gibbons et al. 2014). Tissue from each mouse was homogenized with an RNase-free disposable pellet pestle (Fisher) and  ... [270 more characters]
- `data_processing`: Quality-scores line in fastq files processed with Casava1.8 use an ASCII offset of 33,Sequences were trimmed for adaptor seuqences and masked for low-complexity and low-quality,100 nt paired-end reads were mapped to the Mus musculus NCBI GRCm38 assembly,Reads were assembled into transcript isoforms  ... [193 more characters]
- `platform_id`: GPL13112
- `contact_name`: Sandra,,Rodriguez Zas
- `contact_institute`: University of Illinois at Urbana
- `contact_address`: 1207 W. Gregory Dr.
- `contact_city`: Urbana
- `contact_state`: IL - Illinois
- `contact_zip/postal_code`: 61801
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 2000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE114062
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM3131807 | cerebellum_Control_0 |
| GSM3131808 | cerebellum_Control_1 |
| GSM3131809 | cerebellum_Control_2 |
| GSM3131810 | cerebellum_Control_3 |
| GSM3131811 | cerebellum_Selected_0 |
| GSM3131812 | cerebellum_Selected_1 |
| GSM3131813 | cerebellum_Selected_2 |
| GSM3131814 | cerebellum_Selected_3 |
| GSM3131815 | striatum_Control_0 |
| GSM3131816 | striatum_Control_1 |
| GSM3131817 | striatum_Control_2 |
| GSM3131818 | striatum_Control_3 |
| GSM3131819 | striatum_Selected_0 |
| GSM3131820 | striatum_Selected_1 |
| GSM3131821 | striatum_Selected_2 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the source_name_ch1 level | source_name_ch1 | 8 | 14/15 | 7 | 0 |
| characteristics_ch1.1.condition (without source_name_ch1) + suffix of title | source_name_ch1 | 8 | 14/15 | 7 | 0 |
| line (without source_name_ch1) + suffix of title | source_name_ch1 | 8 | 14/15 | 7 | 0 |
| title without the characteristics_ch1.1.condition level | characteristics_ch1.1.condition | 8 | 14/15 | 7 | 0 |
| source_name_ch1 (without characteristics_ch1.1.condition) + suffix of title | characteristics_ch1.1.condition | 8 | 14/15 | 7 | 0 |
| characteristics_ch1.3.tissue (without characteristics_ch1.1.condition) + suffix of title | characteristics_ch1.1.condition | 8 | 14/15 | 7 | 0 |
| description (without characteristics_ch1.1.condition) + suffix of title | characteristics_ch1.1.condition | 8 | 14/15 | 7 | 0 |
| region (without characteristics_ch1.1.condition) + suffix of title | characteristics_ch1.1.condition | 8 | 14/15 | 7 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the source_name_ch1 level", "across": "_across", "within": [], "n_same_key_pairs": 7, "same_key_mean_r": 0.249, "other_mean_r": -0.036, "difference": 0.284, "permutation_p": 0.0009995002498750624, "genes_used": 11116, "status": "supported"}
