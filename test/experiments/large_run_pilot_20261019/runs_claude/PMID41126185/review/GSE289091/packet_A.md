# Review packet A (facts only): GSE289091

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC12542426.paper.md`

## Paper outline

- # Lamin A/C protects chromatin accessibility during mechanical loading in human skeletal muscle
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Materials and methods  `S2` · methods
- ### Human muscle cell culture  `S2.1` · methods
- ### siRNA transfection  `S2.2` · methods
- ### Mechanical stretch  `S2.3` · methods
- ### Immunocytochemistry and image analysis  `S2.4` · methods
- ### SDS-PAGE and protein analysis  `S2.5` · methods
- ### RNA-seq and quantification of gene expression  `S2.6` · methods
- ### Assay for transposase-accessible chromatin with sequencing (ATAC-seq)  `S2.7` · methods
- ### Integration of ATAC-seq and RNA-seq  `S2.8` · methods
- ### Additional statistical analysis  `S2.9` · methods
- ## Results  `S3` · results
- ### Lamin A/C Deficiency alters nuclear shape and chromatin organization in human muscle cells  `S3.1` · results
- ### Chromatin compaction and transcriptional output are altered in lamin A/C deficient myotubes  `S3.2` · results
- ### A-type lamin deficiency disrupts nuclear mechanoresponses in myotubes  `S3.3` · results
- ## Discussion  `S4` · discussion
- ## Supplementary Information  `S5` · supplementary
- ## Acknowledgements  `S6` · other
- ## Abbreviations  `S7` · other
- ## Authors’ contributions  `S8` · other
- ## Funding  `S9` · other
- ## Data availability  `S10` · data_availability
- ## Declarations  `S11` · other
- ### Competing interests  `S11.1` · other
- ## Accession mentions

## Metadata (18 samples)

### Grouping columns (level: count)

- `submission_date`: Feb 09 2025: 17; Aug 18 2025: 1
- `characteristics_ch1.2.genotype`: lamin A/C knockdown: 11; WT: 7
- `treatment_protocol_ch1`: Differentiation into myotubes was induced by switching confluent myoblasts to differentiation medium containing DMEM (Gibco) and 50 mg/mL gentamycin. Gentamycin was removed when siRNA treatment is applied.: 17; Differentiation into myotubes was induced by switching confluent myoblasts to differentiation medium containing DMEM (Gibco) and 50 mg/mL gentamycin. Gentamycin was removed when siRNA treatment is applied. The siRNA transfections were done with Lipofectamine RNAiMAX (Life Technologies, Carlsbad, CA, 13778-150) according to manufacturer鈥檚 instructions 24h and 48h after switching confluent myoblasts to differentiation medium using 50 nM of siRNA. Gene or protein of interest was analyzed 72 h after the first transfection: 1
- `molecule_ch1`: total RNA: 17; polyA RNA: 1
- `extract_protocol_ch1`: The siRNA transfections were done with Lipofectamine RNAiMAX (Life Technologies, Carlsbad, CA, 13778-150) according to manufacturer鈥檚 instructions 24h and 48h after switching confluent myoblasts to differentiation medium using 50 nM of siRNA. Gene or protein of interest was analyzed 72 h after the first transfection,RNA was harvested using Rneasy mini plus kit (Qiagen). 1.3 ug of total RNA was used for the construction of sequencing libraries.,RNA libraries for RNA-seq were prepared using mRNA-Seq Library Prep Kit following manufacturer's protocols.: 17; RNA was harvested using Rneasy mini plus kit (Qiagen). 1.3 ug of total RNA was used for the construction of sequencing libraries.,RNA libraries for RNA-seq were prepared using mRNA-Seq Library Prep Kit following manufacturer's protocols.: 1
- `platform_id`: GPL24676: 10; GPL21697: 8
- `instrument_model`: Illumina NovaSeq 6000: 10; NextSeq 550: 8
- `geno`: siLMNA: 11; Ctl: 6; : 1
- `cond`: static: 10; stretch: 7; : 1
- `run`: r1: 9; r2: 8; : 1
- `grp`: siLMNA_static: 7; siLMNA_stretch: 4; Ctl_static: 3; Ctl_stretch: 3; : 1

### Constant columns

- `status`: Public on Sep 19 2025
- `last_update_date`: Sep 19 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: myotubes
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.clone`: 8220
- `characteristics_ch1.1.cell type`: myotubes
- `characteristics_ch1.3.treatment`: myogenic differentiation
- `characteristics_ch1.4.time`: Day 3
- `growth_protocol_ch1`: Human immortalized muscle cell precursors, clone 8220, were cultured with 5% CO2 at 37掳C in growth medium consisting of 1 vol 199 Medium/4 vol DMEM (Life Technologies, Carlsbad, CA, USA) supplemented with 20% fetal calf serum (Life technologies, Carlsbad, CA, USA), 5 ng/mL hEGF (Life Technologies, C ... [278 more characters]
- `data_processing`: Quality of raw data was evaluated with FastQC.,Poor quality sequences were trimmed or removed with fastp tool, with default parameters, to retain only good quality paired reads.,Illumina DRAGEN bio-IT Plateform (v3.8.4) was used for mapping on hg38 reference genome and quantification with gencode v3 ... [235 more characters]
- `contact_name`: Catherine,,Coirault
- `contact_email`: catherine.coirault@inserm.fr
- `contact_laboratory`: U974
- `contact_institute`: Inserm
- `contact_address`: 47 bd de l'H么pital
- `contact_city`: Paris
- `contact_zip/postal_code`: 75013
- `contact_country`: France
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE289091
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `supplementary_file_1`

### Samples

| sample | title | description |
|---|---|---|
| GSM8783555 | myotubes, siControl, Hours72, static, rep1 | Library name: ctrl2,run1 |
| GSM8783556 | myotubes, siControl, Hours72, static, rep2 | Library name: ctrl3,run1 |
| GSM8783558 | myotubes, siLaminsA/C, Hours72, static, rep1 | Library name: si-1,run1 |
| GSM8783559 | myotubes, siLaminsA/C, Hours72, static, rep2 | Library name: si-2,run1 |
| GSM8783560 | myotubes, siLaminsA/C, Hours72, static, rep3 | Library name: si-3,run1 |
| GSM8783562 | myotubes, siControl, Hours72, stretch, rep1 | Library name: Sctrl3,run1 |
| GSM8783563 | myotubes, siControl, Hours72, stretch,rep2 | Library name: Sctrl4,run1 |
| GSM8783564 | myotubes, siControl, Hours72, stretch,rep 3 | Library name: Sctrl5,run1 |
| GSM8783565 | myotubes, siControl, Hours72, stretch,rep 4 | Library name: Sctrl6,run1 |
| GSM8783566 | myotubes, siLaminsA/C, Hours72, static, rep5 | Library name: Nsi-0,run2 |
| GSM8783567 | myotubes, siLaminsA/C, Hours72, static,rep6 | Library name: Nsi-2,run2 |
| GSM8783568 | myotubes, siLaminsA/C, Hours72, static,rep 7 | Library name: Nsi-3,run2 |
| GSM8783569 | myotubes, siLaminsA/C, Hours72, static,rep 8 | Library name: Nsi-4,run2 |
| GSM8783570 | myotubes, siLaminsA/C, Hours72, stretch,rep 1 | Library name: Ssi_1_1,run2 |
| GSM8783571 | myotubes, siLaminsA/C, Hours72, stretch,rep 2 | Library name: Ssi_1_2,run2 |
| GSM8783572 | myotubes, siLaminsA/C, Hours72, stretch,rep 3 | Library name: Ssi_1_3,run2 |
| GSM8783573 | myotubes, siLaminsA/C, Hours72, stretch,rep 4 | Library name: Ssi_4_1,run2 |
| GSM9181790 | human myotubes, siControl, Hours72, static | Library name: ctrl1,run1 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| cond (without characteristics_ch1.2.genotype) + suffix of title | characteristics_ch1.2.genotype | 13 | 10/18 | 5 | 0 |
| grp (without characteristics_ch1.2.genotype) + suffix of title | characteristics_ch1.2.genotype | 18 | 0/18 | 0 | 0 |
| grp (without platform_id) + suffix of title | platform_id | 18 | 0/18 | 0 | 0 |
| grp (without instrument_model) + suffix of title | instrument_model | 18 | 0/18 | 0 | 0 |
| submission_date (without characteristics_ch1.2.genotype) + suffix of title | characteristics_ch1.2.genotype | 12 | 8/18 | 4 | 1 |
| treatment_protocol_ch1 (without characteristics_ch1.2.genotype) + suffix of title | characteristics_ch1.2.genotype | 12 | 8/18 | 4 | 1 |
| molecule_ch1 (without characteristics_ch1.2.genotype) + suffix of title | characteristics_ch1.2.genotype | 12 | 8/18 | 4 | 1 |
| extract_protocol_ch1 (without characteristics_ch1.2.genotype) + suffix of title | characteristics_ch1.2.genotype | 12 | 8/18 | 4 | 1 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "cond (without characteristics_ch1.2.genotype) + suffix of title", "across": "_across", "within": ["_within"], "n_same_key_pairs": 5, "same_key_mean_r": 0.074, "other_mean_r": -0.014, "difference": 0.088, "permutation_p": 0.22588705647176413, "genes_used": 10081, "status": "not_supported"}
