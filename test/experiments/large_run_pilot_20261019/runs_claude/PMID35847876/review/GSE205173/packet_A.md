# Review packet A (facts only): GSE205173

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC9285133.paper.md`

## Paper outline

- # Swimming Impedes Intestinal Microbiota and Lipid Metabolites of Tumorigenesis in Colitis-Associated Cancer
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Materials and Methods  `S2` · methods
- ### Experimental Animals  `S2.1` · methods
- ### Reagents  `S2.2` · methods
- ### Experimental Procedure  `S2.3` · methods
- ### Collection and Preparation of Samples  `S2.4` · methods
- ### Evaluation of Histopathology and Immunohistochemistry  `S2.5` · methods
- ### RNA Isolation and Library Preparation  `S2.6` · methods
- ### Analysis of RNA Sequencing and Differentially Expressed Genes  `S2.7` · methods
- ### Analysis of the Metabolic Profile  `S2.8` · methods
- ### Short-Chain Fatty Acid Analysis  `S2.9` · methods
- ### Sequencing Analysis of the 16S rRNA Gene  `S2.10` · methods
- ### Statistics  `S2.11` · methods
- ## Results  `S3` · results
- ### Swimming Pretreatment Attenuates AOM/DSS-Induced Tumor Development  `S3.1` · results
- ### AOM/DSS and Swimming Pretreatment-Induced Changes in Transcription  `S3.2` · results
- ### Swimming Pretreatment Alters Composition of the Intestinal Microbiota Community  `S3.3` · results
- ### Lipid Metabolism Changes in Colonic Environment Induced by AOM/DSS and Swimming Pretreatment  `S3.4` · results
- ### Integration Analysis Among Intestinal Microbiota Community, Colonic Lipid Metabolites, and Transcriptomics to Construct Anti-Inflammatory and Anti-Tumorigenic Transcriptional Networks  `S3.5` · results
- ## Discussion  `S4` · discussion
- ## Data Availability Statement  `S5` · data_availability
- ## Ethics Statement  `S6` · other
- ## Author Contributions  `S7` · other
- ## Funding  `S8` · other
- ## Conflict of Interest  `S9` · other
- ## Publisher’s Note  `S10` · other
- ## Supplementary Material  `BK1` · supplementary
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.treatment`: NC: 3; swim only: 3; AOM/DSS treated: 3; AOM/DSS treated+swimming pretreatment: 3
- `description`: Natural colorectal morphology: 6; AOM/DSS induced significantly the shortening of colonic length and colitis-induced tumorigenicity.: 3; Swimming pretreatment significantly inhibited the shortening of colonic length and colitis-induced tumorigenicity.: 3
- `grp`: Ctrl: 3; CtrlSwim: 3; Model: 3; ModelSwim: 3

### Constant columns

- `status`: Public on Jul 20 2022
- `submission_date`: May 31 2022
- `last_update_date`: Jul 20 2022
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Colorectal tissue
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Colorectal tissue
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted using the mirVana miRNA Isolation Kit (Ambion) following the manufacturer鈥檚 protocol.,Then the libraries were constructed using TruSeq Stranded mRNALTSample Prep Kit(Ilumina,San Diego, CA, USA) . 1 ug of total RNA was used for the construction of sequencing libraries.
- `data_processing`: CLC Genomics Workbenchv 11.0.1,Sequence reads were trimmed for adaptor sequence/low-quality sequence using CLC genomic benchwork (parameter- Quality limit: 0.05),Trimmed sequence reads were mapped to NCBI_GRCm38.p6 using CLC genomic benchwork (parameters- mismath cost: 2 insertion cost: 3 deletion c ... [257 more characters]
- `platform_id`: GPL24247
- `contact_name`: weiyi,,wang
- `contact_email`: wwy4348@shtrhospital.com
- `contact_department`: Department of Endoscopy
- `contact_institute`: Shanghai Tong Ren Hospital, Shanghai Jiao Tong University School of Medicine, Shanghai, China
- `contact_address`: No. 1111 Xianxia Road, Changning District, Shanghai, PR China
- `contact_city`: shanghai
- `contact_zip/postal_code`: 20000
- `contact_country`: China
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE205173
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM6206813 | Ctrl1 |
| GSM6206814 | Ctrl2 |
| GSM6206815 | Ctrl3 |
| GSM6206816 | Ctrl_Swim2 |
| GSM6206817 | Ctrl_Swim3 |
| GSM6206818 | Ctrl_Swim4 |
| GSM6206819 | Model1 |
| GSM6206820 | Model2 |
| GSM6206821 | Model3 |
| GSM6206822 | Swim1 |
| GSM6206823 | Swim2 |
| GSM6206824 | Swim3 |

## Values with exercise words (by column)

- `title`: Ctrl_Swim2, Ctrl_Swim3, Ctrl_Swim4, Swim1, Swim2, Swim3
- `characteristics_ch1.1.treatment`: AOM/DSS treated+swimming pretreatment, swim only
- `description`: Swimming pretreatment significantly inhibited the shortening of colonic length and colitis-induced tumorigenicity.
- `grp`: CtrlSwim, ModelSwim

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the grp level | grp | 10 | 4/12 | 0 | 0 |
