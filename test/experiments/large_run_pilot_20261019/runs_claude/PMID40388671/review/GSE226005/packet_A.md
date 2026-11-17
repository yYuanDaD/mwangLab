# Review packet A (facts only): GSE226005

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC12165025.paper.md`

## Paper outline

- # Histone Lactylation Antagonizes Senescence and Skeletal Muscle Aging by Modulating Aging‐Related Pathways
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Histone Lactylation Dramatically Decreases During Senescence  `S2.1` · results
- ### Glycolysis Inhibition Leads to a Loss of Histone Lactylation During Senescence  `S2.2` · results
- ### Histone Lactylation Modulates Cell Cycle‐ and DNA Repair‐Related Genes to Antagonize Cellular Senescence  `S2.3` · results
- ### Inhibiting Lactyltransferase p300 or Delactylase HDAC Reduces Histone Lactylation and Accelerates Cellular Senescence  `S2.4` · results
- ### Glycolysis and Histone Lactylation Levels decrease During Skeletal Muscle Aging  `S2.5` · results
- ### Decreased Histone Lactylation in Aged Muscle Dampens DNA Repair and Proteostasis Pathways  `S2.6` · results
- ### Exercise Activates Glycolysis and Restores Histone Lactylation Levels in Skeletal Muscle  `S2.7` · results
- ### Exercise Increases Lactylation Levels and Promotes DNA Repair and Proteostasis  `S2.8` · results
- ## Discussion  `S3` · discussion
- ## Conclusion  `S4` · conclusion
- ## Experimental Section  `S5` · methods
- ### Cell Culture  `S5.1` · methods
- ### Mouse Models  `S5.2` · methods
- ### Behavioral Performance Test  `S5.3` · methods
- ### Senescence‐Associated β‐Galactosidase Staining (SA‐β‐Gal Staining)  `S5.4` · methods
- ### Immunofluorescence  `S5.5` · methods
- ### Immunoblotting  `S5.6` · methods
- ### Lactate Measurement  `S5.7` · methods
- ### CUT&Tag Sequencing (CUT&Tag‐seq)  `S5.8` · methods
- ### RNA‐seq  `S5.9` · methods
- ### qPCR  `S5.10` · methods
- ### Hematoxylin and Eosin (H&E) Staining  `S5.11` · methods
- ### Bulk RNA‐seq Data Processing  `S5.12` · methods
- ### CUT&Tag Data Processing  `S5.13` · methods
- ### Processing of Raw Data, Filtering, Integration, Clustering, and Identification of Cell Types  `S5.14` · methods
- ### Aging‐Related and Running‐Related Differential Expression Analysis  `S5.15` · methods
- ### Transcriptional Noise Analysis  `S5.16` · methods
- ### Cell Type Prioritization Analysis  `S5.17` · methods
- ### Gene Set Score Analysis  `S5.18` · methods
- ### Functional Enrichment Analyses  `S5.19` · methods
- ### Statistical Analysis  `S5.20` · methods
- ## Conflict of Interest  `S6` · other
- ## Supporting information  `S7` · supplementary
- ## Data Availability Statement  `DA` · data_availability
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `submission_date`: Feb 23 2023: 8; May 11 2023: 4
- `characteristics_ch1.4.treatment`: : 4; Hypoxia: 4; Normoxia: 2; 2-DG+Hypoxia: 2
- `grp`: SEN: 2; YNG: 2; HYP: 2; NOR: 2; DG: 2; CTL1: 2

### Constant columns

- `status`: Public on May 01 2024
- `last_update_date`: Oct 12 2024
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: lung
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: lung
- `characteristics_ch1.1.cell line`: IMR90
- `characteristics_ch1.2.cell type`: Fibroblast
- `characteristics_ch1.3.genotype`: WT
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted from cells for the construction of sequencing libraries using TRIzol庐 (Invitrogen, 15596018),RNA libraries were prepared for sequencing using Illumina protocols
- `data_processing`: The raw sequencing data were processed using trim_galore (version 0.6.10) to remove adapters and low-quality reads,The trimmed reads were then mapped to the hg38 or mm10 reference genome using hisat2 (version 2.2.1), and the SAM files were converted to sorted BAM files using samtools (version 1.7),T ... [246 more characters]
- `platform_id`: GPL24676
- `contact_name`: Wei,,Tao
- `contact_email`: weitao@pku.edu.cn
- `contact_phone`: 010-62758903
- `contact_laboratory`: Tao lab
- `contact_department`: School of Life Sciences
- `contact_institute`: Peking University
- `contact_address`: No.5 Yiheyuan Road
- `contact_city`: Beijing
- `contact_zip/postal_code`: 100871
- `contact_country`: China
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE226005,GSE226008
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM7061572 | IMR90_Senescent_rep1(RNA-seq) |
| GSM7061573 | IMR90_Senescent_rep2(RNA-seq) |
| GSM7061574 | IMR90_Young_rep1(RNA-seq) |
| GSM7061575 | IMR90_Young_rep2(RNA-seq) |
| GSM7061576 | IMR90_Hypoxia_rep1(RNA-seq) |
| GSM7061577 | IMR90_Hypoxia_rep2(RNA-seq) |
| GSM7061578 | IMR90_Normoxia_rep1(RNA-seq) |
| GSM7061579 | IMR90_Normoxia_rep2(RNA-seq) |
| GSM7329325 | IMR90_2-DG_rep1(RNA-seq) |
| GSM7329326 | IMR90_2-DG_rep2(RNA-seq) |
| GSM7329327 | IMR90_Control1_rep1(RNA-seq) |
| GSM7329328 | IMR90_Control1_rep2(RNA-seq) |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.4.treatment level | characteristics_ch1.4.treatment | 10 | 4/12 | 0 | 0 |
| grp | submission_date | 6 | 0/12 | 0 | 6 |
| grp | characteristics_ch1.4.treatment | 6 | 0/12 | 0 | 6 |
