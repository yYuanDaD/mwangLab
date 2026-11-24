# Review packet A (facts only): GSE132930_cortex_midlife

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC6854620.paper.md`

## Paper outline

- # Transcriptional profiling predicts running promotes cerebrovascular remodeling in young but not midlife mice
- ## Abstract  `ABS` · abstract
- ## Background  `S1` · introduction
- ## Results  `S2` · results
- ### Voluntary running distances at midlife showed a bimodal distribution  `S2.1` · results
- ### Young running affects transcriptional signatures more robustly than midlife running  `S2.2` · results
- ### Extracellular matrix-related genes are altered in young but not midlife runners  `S2.3` · results
- ### Running upregulates genes related to vascular remodeling in young but not midlife mice  `S2.4` · results
- ### Running activates genes in multiple cerebrovascular-related cell types  `S2.5` · results
- ## Discussion  `S3` · discussion
- ## Conclusions  `S4` · conclusion
- ## Methods  `S5` · methods
- ### Mouse strains  `S5.1` · methods
- ### Exercise by voluntary running  `S5.2` · methods
- ### Nuclear magnetic resonance (NMR) imaging  `S5.3` · methods
- ### Harvesting, tissue preparation and blood chemistry  `S5.4` · methods
- ### RNA and protein extraction, library construction and RNA sequencing  `S5.5` · methods
- ### RNA-seq quality control and gene set enrichment  `S5.6` · methods
- ### Statistical analyses  `S5.7` · methods
- ## Supplementary information  `S6` · supplementary
- ### (untitled)  `S6.1` · supplementary
- ## Supplementary information  `BK1` · supplementary
- ## Authors’ contributions  `BK2` · other
- ## Funding  `BK3` · other
- ## Availability of data and materials  `DA` · data_availability
- ## Ethics approval and consent to participate  `BK4` · other
- ## Consent for publication  `BK5` · other
- ## Competing interests  `BK6` · other
- ## Accession mentions

## Metadata (22 samples)

### Grouping columns (level: count)

- `characteristics_ch1.3.activity`: Sed: 10; RunLow: 6; RunHi: 6
- `grp`: Sed: 10; RunLow: 6; RunHi: 6
- `pool`: L001: 11; L005: 11

### Constant columns

- `status`: Public on Jun 19 2019
- `submission_date`: Jun 18 2019
- `last_update_date`: Jun 19 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Cortex
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: C57BL/6J
- `characteristics_ch1.1.brain region`: Cortex
- `characteristics_ch1.2.age`: One Year
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: MagMAX mirVana Total RNA,HiSeq4000, 2x100, 45 million reads聽
- `description`: processed data file:,GeneCount_C.txt
- `data_processing`: RNA quality was measured via the Bioanalyzer 2100 (Agilent Technologies) and poly(A) RNA-seq sequencing libraries were compiled by TruSeq RNA Sample preparation kit v2 (Illumina).,Quantification was performed using qPCR (Kapa Biosystems).,RNA-seq was performed on the HiSeq 4,000 platform (Illumina)  ... [1745 more characters]
- `platform_id`: GPL21103
- `contact_name`: Kate,,Foley
- `contact_email`: Kate.Foley@jax.org
- `contact_phone`: 6315536994
- `contact_institute`: The Jackson Laboratory
- `contact_address`: 600 Main St
- `contact_city`: Bar Harbor
- `contact_state`: ME
- `contact_zip/postal_code`: 4609
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 4000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE132930
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM3896744 | 0533C |
| GSM3896745 | 1003C |
| GSM3896746 | 23886C |
| GSM3896747 | 3494C |
| GSM3896748 | 3597C |
| GSM3896749 | 5943C |
| GSM3896750 | 6332C |
| GSM3896751 | 6967C |
| GSM3896752 | 9555C |
| GSM3896753 | 9926C |
| GSM3896754 | 0304C |
| GSM3896755 | 1990C |
| GSM3896756 | 2084C |
| GSM3896757 | 2747C |
| GSM3896758 | 3545C |
| GSM3896759 | 5581C |
| GSM3896760 | 5915C |
| GSM3896761 | 6859C |
| GSM3896762 | 7182C |
| GSM3896763 | 7383C |
| GSM3896764 | 7785C |
| GSM3896765 | 1388C |

## Values with exercise words (by column)

- `characteristics_ch1.3.activity`: Sed
- `data_processing`: RNA quality was measured via the Bioanalyzer 2100 (Agilent Technologies) and poly(A) RNA-seq sequencing libraries were compiled by TruSeq RNA Sample preparation kit v2 (Illumina).,Quantification was performed using qPCR (Kapa Biosystems).,RNA-seq was performed on the HiSeq 4,000 platform (Illumina) for 2x100bp reads for a total of 45 million reads according to the manufacturer鈥檚 instructions.,Quality control for each sample was completed using NGSQCToolkit v2.3 which removed adaptors and trimmed low quality bases (Phred<30),To quantify gene expression of the trimmed reads, we used RSEM v1.2.12 which uses Bowtie2 v2.2.0 for alignment of these reads,Differential gene expression (DGE) analysis was completed on the hippocampus and cortex separately, using EdgeR 3.20.9,Normalization of trimmed mean of M values (TMM) was performed and quasi-likelihood F-test was used to attain DGE,Genome_build: mm10,Supplementary_files_format_and_content: GeneCount_H.txt: all gene counts for hippocampal samples,Supplementary_files_format_and_content: GeneCount_C.txt: all gene counts for cortical samples,Supplementary_files_format_and_content: OneYearRun2017_H_hilow_RunHi_vs_Sed.txt: FDR and P values for all hippocampal high running vs high running samples,Supplementary_files_format_and_content: OneYearRun2017_H_hilow_RunLow_vs_Sed.txt: FDR and P values for all hippocampal sedentary vs low running samples,Supplementary_files_format_and_content: OneYearRun2017_C_hilow_RunHi_vs_Sed.txt: FDR and P values for all cortical sedentary vs high running samples,Supplementary_files_format_and_content: OneYearRun2017_C_hilow_RunLow_vs_Sed.txt: FDR and P values for all hippocampal sedentary vs low running samples,Supplementary_files_format_and_content: Early_Diet_hippo_8wkrun_wo18606_CD.8weeks.Run.H_vs_CD.8weeks.Sed.H.txt: FDR and P values for all young running vs sedentary samples,Supplementary_files_format_and_content: Early_Diet_cortex_8wkrun_CD.8weeks.Run.C_vs_CD.8weeks.Sed.C.txt: FDR and P values for all cortical running vs sedentary samples
- `grp`: Sed

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| none | | | | | |
