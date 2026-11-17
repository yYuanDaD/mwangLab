# Review packet A (facts only): GSE152919

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC8550249.paper.md`

## Paper outline

- # REV-ERB nuclear receptors in the suprachiasmatic nucleus control circadian period and restrict diet-induced obesity
- ## Abstract  `ABS` · abstract
- ## INTRODUCTION  `S1` · introduction
- ## RESULTS  `S2` · results
- ### SCN-specific deletion of REV-ERBs impairs free-running and metabolic periods  `S2.1` · results
- ### Whole-body deletion of REV-ERBs impairs ability to evaluate free-running period  `S2.2` · results
- ### SCN-specific deletion of REV-ERBs alters SCN gene transcription involved in circadian entrainment  `S2.3` · results
- ### SCN-DKO mice are entrained to 21-hour LD cycle contrary to control mice  `S2.4` · results
- ### Matching LD cycle to the SCN-DKO mouse free-running period reduces their sensitivity to HFD-induced obesity  `S2.5` · results
- ## DISCUSSION  `S3` · discussion
- ## MATERIALS AND METHODS  `S4` · methods
- ### Animals  `S4.1` · methods
- ### Record and analysis of wheel-running activity  `S4.2` · methods
- ### Definition of CT in control and SCN-DKO mice  `S4.3` · methods
- ### In vivo metabolic phenotyping by indirect calorimetry  `S4.4` · methods
- ### Analysis of PER2::LUC luminescence in SCN slices  `S4.5` · methods
- ### LD cycle modification on HFD  `S4.6` · methods
- ### Glucose and insulin tolerance tests  `S4.7` · methods
- ### Histology  `S4.8` · methods
- ### FISH of SCN Rev-erbα (Nr1d1)  `S4.9` · methods
- ### Hypothalamic nuclei microdissection  `S4.10` · methods
- ### Western blot  `S4.11` · methods
- ### mRNA isolation  `S4.12` · methods
- ### Gene expression analysis (RT-qPCR)  `S4.13` · methods
- ### RNA-seq library preparation and data analysis  `S4.14` · methods
- ### Statistical analysis  `S4.15` · methods
- ## Supplementary Materials  `BK1` · supplementary
- ### This PDF file includes:  `BK1.1` · supplementary
- ### Other Supplementary Material for this manuscript includes the following:  `BK1.2` · supplementary
- ## sec  `BK2` · other

## Metadata (15 samples)

### Grouping columns (level: count)

- `source_name_ch1`: CT16_WT_SCN: 5; CT16_KO_SCN: 4; CT4_KO_SCN: 3; CT4_WT_SCN: 3
- `characteristics_ch1.2.genotype`: control: 8; REV-ERBS DKO: 7
- `characteristics_ch1.3.time point`: CT16: 9; CT4: 6
- `geno`: WT: 8; KO: 7
- `time`: CT16: 9; CT4: 6

### Constant columns

- `status`: Public on Jul 15 2021
- `submission_date`: Jun 21 2020
- `last_update_date`: Jul 15 2021
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain background`: C57BL/6
- `characteristics_ch1.1.age`: 8-12 weeks
- `characteristics_ch1.4.sample type`: suprachiasmatic nuclei (SCN)
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: 2-4 independents hypothalamic nuclei punches were pooled together per biological replicate. Hypothalamus punches were homogenized manually by Pellet-Pestle (Kimble, 749515) for 1 minutes with 1mL QIAzol Lysis Reagent (Qiagen). Samples were then centrifuged at 4掳C for 10min at 15,000 x g. In a new tu ... [430 more characters]
- `data_processing`: #genome alignment single read: STAR --genomeDir ~/STAR_mm10_GENOME_DIR  --runThreadN 20 --readFilesIn $i --outFileNamePrefix ${i/.fastq.gz/}_ --outFilterMultimapNmax 1 --outSAMtype BAM SortedByCoordinate --readFilesCommand zcat --outSAMstrandField intronMotif,#counting reads: featureCounts -t exon - ... [158 more characters]
- `platform_id`: GPL21103
- `contact_name`: Hoang,,Nguyen
- `contact_email`: hoangchuongbuinguyen@gmail.com
- `contact_institute`: Massachussetts Eye and Ear
- `contact_address`: 243 Charles St
- `contact_city`: Boston
- `contact_state`: MA
- `contact_zip/postal_code`: 2128
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 4000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE152919
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM4629724 | CT4_KO1 |
| GSM4629725 | CT4_KO2 |
| GSM4629726 | CT4_KO3 |
| GSM4629727 | CT4_WT1 |
| GSM4629728 | CT4_WT2 |
| GSM4629729 | CT4_WT3 |
| GSM4629730 | CT16_KO1 |
| GSM4629731 | CT16_KO2 |
| GSM4629732 | CT16_KO3 |
| GSM4629733 | CT16_KO4 |
| GSM4629734 | CT16_WT1 |
| GSM4629735 | CT16_WT2 |
| GSM4629736 | CT16_WT3 |
| GSM4629737 | CT16_WT4 |
| GSM4629738 | CT16_WT5 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the source_name_ch1 level | source_name_ch1 | 9 | 12/15 | 0 | 0 |
| title without the characteristics_ch1.3.time point level | characteristics_ch1.3.time point | 9 | 12/15 | 6 | 0 |
| title without the time level | time | 9 | 12/15 | 6 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the source_name_ch1 level", "across": "_across", "within": [], "n_same_key_pairs": 6, "same_key_mean_r": 0.021, "other_mean_r": -0.0, "difference": 0.022, "permutation_p": 0.40929535232383807, "genes_used": 11386, "status": "not_supported"}
