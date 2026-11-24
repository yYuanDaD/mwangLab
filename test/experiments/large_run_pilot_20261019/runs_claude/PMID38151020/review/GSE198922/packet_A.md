# Review packet A (facts only): GSE198922

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC10829726.paper.md`

## Paper outline

- # Exercise-induced crosstalk between immune cells and adipocytes in humans: Role of oncostatin-M
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Exercise exerts a differential transcriptomic response in adipose tissue between individuals with normal glucose tolerance and those with type 2 diabetes  `S2.1` · results
- ### Exercise induces the expression of genes encoding for secreted proteins in adipose tissue  `S2.2` · results
- ### Oncostatin-M is acutely induced by exercise and regulates basal lipolysis in isolated adipocytes  `S2.3` · results
- ### Oncostatin-M is released from immune cells in response to exercise-like stimuli  `S2.4` · results
- ## Discussion  `S3` · discussion
- ### Limitations of the study  `S3.1` · discussion
- ## STAR★Methods  `S4` · methods
- ### Key resources table  `S4.1` · methods
- ### Resource availability  `S4.2` · methods
- #### Lead contact  `S4.2.1` · methods
- #### Materials availability  `S4.2.2` · methods
- #### Data and code availability  `S4.2.3` · data_availability
- ### Experimental model and study participants details  `S4.3` · methods
- #### Human intervention  `S4.3.1` · methods
- #### In vitro studies  `S4.3.2` · methods
- ##### Human adipocytes  `S4.3.2.1` · methods
- ##### Human primary muscle cells  `S4.3.2.2` · methods
- ##### THP1 monocytic cell line  `S4.3.2.3` · methods
- ### Method details  `S4.4` · methods
- #### Library preparation and RNA sequencing  `S4.4.1` · methods
- #### Bioinformatic analysis  `S4.4.2` · methods
- #### Plasma analysis  `S4.4.3` · methods
- #### mRNA expression in cells derived from human adipose tissue  `S4.4.4` · methods
- #### Human adipose tissue sections  `S4.4.5` · methods
- #### In situ hybridization in adipose tissue biopsies  `S4.4.6` · methods
- #### Immunohistochemistry staining of adipose tissue biopsies  `S4.4.7` · methods
- #### Western blot  `S4.4.8` · methods
- #### Kinase activity assay with PamChip  `S4.4.9` · methods
- ### Quantification and statistical analysis  `S4.5` · methods
- ## Acknowledgments  `S5` · other
- ### Author contributions  `S5.1` · other
- ### Declaration of interests  `S5.2` · other
- ### Inclusion and diversity  `S5.3` · other
- ## (untitled)  `S6` · other
- ## Contributor Information  `S8` · other
- ## Supplemental information  `S9` · supplementary
- ## Accession mentions

## Metadata (143 samples)

### Grouping columns (level: count)

- `characteristics_ch1.0.Sex`: M: 80; F: 63
- `characteristics_ch1.1.age`: 63: 24; 64: 20; 61: 15; 53: 12; 62: 12; 58: 9; 59: 9; 65: 9; 56: 9; 66: 6; 51: 3; 60: 3; 55: 3; 47: 3; 54: 3; 57: 3
- `characteristics_ch1.3.diagnosis`: T2D: 83; NGT: 60
- `characteristics_ch1.4.exercise`: PRE: 48; REC: 48; POST: 47
- `dx`: T2D: 83; NGT: 60
- `sex`: M: 80; F: 63
- `time`: PRE: 48; REC: 48; POST: 47

### Constant columns

- `status`: Public on Nov 21 2023
- `submission_date`: Mar 18 2022
- `last_update_date`: Dec 12 2023
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Adipose tissue biopsy
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.5.tissue`: Adipose tissue biopsy
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Approximately 30 mg of adipose tissue was used for RNA extraction. Tissues were homogenized using TissueLyser (Qiagen) in 1 mL TRIzol (Sigma-Aldrich). Chloroform was added, samples were mixed, subjected to centrifugation, and the aqueous phase was transferred to a new tube. Thereafter, 1:1 70% ethan ... [1966 more characters]
- `data_processing`: star/2.7.2b STAR --outReadsUnmapped Fastx --outSAMstrandField intronMotif--outFilterIntronMotifs RemoveNoncanonicalUnannotated --outSAMtype BAM SortedByCoordinate,subread/2.0.2 featureCounts -p -B -C -T $threads -t exon -g gene_id,limma_3.48.3 filterByExpr.DGEList(dataDGE, design = model.matrix(~0 + ... [175 more characters]
- `platform_id`: GPL18573
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
- `series_id`: GSE198922
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM5960611 | 1_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960612 | 1_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960613 | 11_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960614 | 11_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960615 | 11_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960616 | 12_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960617 | 12_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960618 | 12_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960619 | 15_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960620 | 15_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960621 | 15_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960622 | 16_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960623 | 16_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960624 | 16_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960625 | 17_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960626 | 17_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960627 | 17_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960628 | 18_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960629 | 18_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960630 | 18_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960631 | 19_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960632 | 19_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960633 | 19_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960634 | 2_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960635 | 2_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960636 | 2_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960637 | 20_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960638 | 20_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960639 | 20_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960640 | 21_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960641 | 21_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960642 | 21_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960643 | 22_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960644 | 22_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960645 | 22_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960646 | 23_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960647 | 23_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960648 | 23_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960649 | 26_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960650 | 26_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960651 | 26_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960652 | 27_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960653 | 27_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960654 | 27_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960655 | 3_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960656 | 3_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960657 | 3_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960658 | 30_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960659 | 30_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960660 | 30_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960661 | 31_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960662 | 31_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960663 | 31_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960664 | 32_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960665 | 32_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960666 | 32_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960667 | 33_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960668 | 33_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960669 | 33_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960670 | 34_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960671 | 34_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960672 | 34_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960673 | 35_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960674 | 35_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960675 | 35_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960676 | 37_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960677 | 37_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960678 | 37_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960679 | 38_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960680 | 38_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960681 | 38_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960682 | 4_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960683 | 4_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960684 | 4_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960685 | 42_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960686 | 42_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960687 | 42_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960688 | 44_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960689 | 44_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960690 | 44_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960691 | 46_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960692 | 46_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960693 | 46_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960694 | 49_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960695 | 49_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960696 | 49_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960697 | 50_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960698 | 50_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960699 | 50_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960700 | 53_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960701 | 53_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960702 | 53_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960703 | 56_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960704 | 56_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960705 | 56_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960706 | 57_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960707 | 57_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960708 | 57_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960709 | 58_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960710 | 58_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960711 | 58_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960712 | 59_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960713 | 59_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960714 | 59_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960715 | 6_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960716 | 6_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960717 | 6_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960718 | 60_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960719 | 60_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960720 | 60_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960721 | 62_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960722 | 62_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960723 | 62_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960724 | 63_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960725 | 63_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960726 | 63_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960727 | 64_POST | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960728 | 64_PRE | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960729 | 64_REC | RNAseq from adipose tissue biopsy obtained from participant  |
| GSM5960730 | 65_POST | RNAseq from adipose tissue biopsy obtained from participant  |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.4.exercise level | characteristics_ch1.4.exercise | 48 | 143/143 | 47 | 0 |
| description without the characteristics_ch1.4.exercise level | characteristics_ch1.4.exercise | 48 | 143/143 | 47 | 0 |
| characteristics_ch1.2.participant id | characteristics_ch1.4.exercise | 48 | 143/143 | 47 | 0 |
| pid | characteristics_ch1.4.exercise | 48 | 143/143 | 47 | 0 |
| subject | characteristics_ch1.4.exercise | 48 | 143/143 | 47 | 0 |
| title without the time level | time | 48 | 143/143 | 47 | 0 |
| description without the time level | time | 48 | 143/143 | 47 | 0 |
| characteristics_ch1.2.participant id | time | 48 | 143/143 | 47 | 0 |
