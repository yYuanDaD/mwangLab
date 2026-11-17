# Review packet A (facts only): GSE199429

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC9974500.paper.md`

## Paper outline

- # Time of day determines postexercise metabolism in mouse adipose tissue
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## (untitled)  `S0` · other
- ## Results  `S1` · results
- ### Exercise Elicits Time-Dependent Effects on Lipid Metabolism without Disturbing the Adipose Molecular Clock.  `S1.1` · results
- ### Adipose Tissue Transcriptomic Profile Is Altered by Active Phase Exercise.  `S1.2` · results
- ### Gene Expression and Lipolytic Response to Isoproterenol Are Clock Associated in 3T3-L1 Adipocytes.  `S1.3` · results
- ### Adipose Tissue Response to Exercise Is Partially Independent of Nutritional Status.  `S1.4` · results
- ## Discussion  `S2` · discussion
- ## Materials and Methods  `S3` · methods
- ### Animal Experiments.  `S3.1` · methods
- ### Cell Culture.  `S3.2` · methods
- ### Gene Expression Analysis.  `S3.3` · methods
- ### Biochemistry Analysis.  `S3.4` · methods
- ### Library Preparation and RNA Sequencing Library.  `S3.5` · methods
- ### Bioinformatic Analysis.  `S3.6` · methods
- ### Protein Isolation and Western Blot Analysis.  `S3.7` · methods
- ### Statistical Analysis.  `S3.8` · methods
- ### Ethical Review.  `S3.9` · methods
- ## Supplementary Material  `S4` · supplementary
- ## Acknowledgments  `S5` · other
- ### Author contributions  `S5.1` · other
- ### Competing interests  `S5.2` · other
- ## Contributor Information  `S7` · other
- ## Data, Materials, and Software Availability  `S8` · data_availability
- ## Accession mentions

## Metadata (24 samples)

### Grouping columns (level: count)

- `source_name_ch1`: Murine inguinal white adipose tissue from sedentary animals sampled at ZT3: 6; Murine inguinal white adipose tissue from exercised animals sampled at ZT3: 6; Murine inguinal white adipose tissue from exercised animals sampled at ZT15: 6; Murine inguinal white adipose tissue from sedentary animals sampled at ZT15: 6
- `characteristics_ch1.3.sampling time`: ZT3: 12; ZT15: 12
- `characteristics_ch1.4.exercise`: SED: 12; RUN: 12
- `ex`: SED: 12; RUN: 12
- `time`: ZT3: 12; ZT15: 12
- `grp`: SED_ZT3: 6; RUN_ZT3: 6; RUN_ZT15: 6; SED_ZT15: 6

### Constant columns

- `status`: Public on Jan 19 2023
- `submission_date`: Mar 25 2022
- `last_update_date`: Jan 19 2023
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: inguinal white adipose tissue
- `characteristics_ch1.1.Sex`: male
- `characteristics_ch1.2.strain`: C57BL6
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Inguinal adipose tissue was used for RNA extraction. Tissues were homogenized using TissueLyser (Qiagen) in 1 mL TRIzol (Sigma-Aldrich). Chloroform was added, samples were mixed, subjected to centrifugation, and the aqueous phase was transferred to a new tube. Thereafter, 1:1 70% ethanol was added,  ... [1984 more characters]
- `data_processing`: star/2.7.2b STAR --outReadsUnmapped Fastx --outSAMstrandField intronMotif--outFilterIntronMotifs RemoveNoncanonicalUnannotated --outSAMtype BAM SortedByCoordinate,subread/1.6.2 featureCounts -p -B -C -T $threads -t exon -g gene_id,limma_3.48.3 filterByExpr.DGEList(dataDGE, design = model.matrix(~0 + ... [230 more characters]
- `platform_id`: GPL19057
- `contact_name`: Leonidas,S,Lundell
- `contact_email`: leonidas.lundell@gmail.com
- `contact_laboratory`: Integrative Physiology
- `contact_department`: Physiology and Pharmacology
- `contact_institute`: Karolinska Institute
- `contact_address`: Von Eulers V盲g 4a
- `contact_city`: Stockholm
- `contact_state`: Stockholm
- `contact_zip/postal_code`: 171 77
- `contact_country`: Sweden
- `instrument_model`: NextSeq 500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE199429
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `_norm_key`

### Samples

| sample | title |
|---|---|
| GSM5972665 | 10SED_m |
| GSM5972666 | 11RUN_m |
| GSM5972667 | 12SED_m |
| GSM5972668 | 13Run_e |
| GSM5972669 | 14SED_e |
| GSM5972670 | 15Run_e |
| GSM5972671 | 16SED_e |
| GSM5972672 | 17RUN_m |
| GSM5972673 | 18SED_m |
| GSM5972674 | 19RUN_m |
| GSM5972675 | 1RUN_m |
| GSM5972676 | 20SED_m |
| GSM5972677 | 21Run_e |
| GSM5972678 | 22SED_e |
| GSM5972679 | 23Run_e |
| GSM5972680 | 24SED_e |
| GSM5972681 | 2SED_m |
| GSM5972682 | 3RUN_m |
| GSM5972683 | 4SED_m |
| GSM5972684 | 5Run_e |
| GSM5972685 | 6SED_e |
| GSM5972686 | 7Run_e |
| GSM5972687 | 8SED_e |
| GSM5972688 | 9RUN_m |

## Values with exercise words (by column)

- `source_name_ch1`: Murine inguinal white adipose tissue from exercised animals sampled at ZT15, Murine inguinal white adipose tissue from exercised animals sampled at ZT3, Murine inguinal white adipose tissue from sedentary animals sampled at ZT15, Murine inguinal white adipose tissue from sedentary animals sampled at ZT3
- `characteristics_ch1.4.exercise`: RUN, SED
- `ex`: RUN, SED
- `grp`: RUN_ZT15, RUN_ZT3

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | source_name_ch1 | 2 | 0/24 | 0 | 2 |
| characteristics_ch1.4.exercise (without source_name_ch1) + suffix of title | source_name_ch1 | 4 | 0/24 | 0 | 4 |
| ex (without source_name_ch1) + suffix of title | source_name_ch1 | 4 | 0/24 | 0 | 4 |
| grp (without source_name_ch1) + suffix of title | source_name_ch1 | 4 | 0/24 | 0 | 4 |
| suffix of title | characteristics_ch1.3.sampling time | 2 | 0/24 | 0 | 2 |
| source_name_ch1 (without characteristics_ch1.3.sampling time) + suffix of title | characteristics_ch1.3.sampling time | 4 | 0/24 | 0 | 4 |
| characteristics_ch1.4.exercise (without characteristics_ch1.3.sampling time) + suffix of title | characteristics_ch1.3.sampling time | 4 | 0/24 | 0 | 4 |
| ex (without characteristics_ch1.3.sampling time) + suffix of title | characteristics_ch1.3.sampling time | 4 | 0/24 | 0 | 4 |
