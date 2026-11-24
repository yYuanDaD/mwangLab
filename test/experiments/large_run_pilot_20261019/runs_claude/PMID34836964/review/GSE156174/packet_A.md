# Review packet A (facts only): GSE156174

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261028\papers\PMC8626488.paper.md`

## Paper outline

- # Transcriptional responses of skeletal stem/progenitor cells to hindlimb unloading and recovery correlate with localized but not systemic multi-systems impacts
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### HU induces localized skeletal pathology and muscle atrophy  `S2.1` · results
- ### HU-induced MAT accumulation correlates with localized increases in BM leptin and TH expression  `S2.2` · results
- ### HU mice exhibit elevated corticosterone levels and increased activity but normal circadian rhythms  `S2.3` · results
- ### HU has disparate effects on SSC and MSC gene expression and promotes SSC quiescence  `S2.4` · results
- ### Prolonged (14wk) HU induces progressive bone loss and promotes SSC quiescence  `S2.5` · results
- ### HUR restores muscle and body fat mass, BM leptin, and TH expression but not trabecular bone or SSC transcription  `S2.6` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### Mice  `S4.1` · methods
- ### Stem cell isolation and characterization  `S4.2` · methods
- ### Metabolic profiling  `S4.3` · methods
- ### Micro-CT analysis  `S4.4` · methods
- ### Mouse behavior studies  `S4.5` · methods
- ### Histological staining  `S4.6` · methods
- ### RNA sequencing  `S4.7` · methods
- ### RNA-Seq data analysis  `S4.8` · methods
- ### Quantification and statistical analysis  `S4.9` · methods
- ### Reporting summary  `S4.10` · methods
- ## Supplementary information  `S5` · supplementary
- ### (untitled)  `S5.1` · supplementary
- ## Author contributions  `S6` · other
- ## Data availability  `S7` · data_availability
- ## Code availability  `S8` · data_availability
- ## Competing interests  `S9` · other
- ## Supplementary information  `S11` · supplementary
- ## Accession mentions

## Metadata (10 samples)

### Grouping columns (level: count)

- `source_name_ch1`: flow sorted SSCs: 6; depleted MSCs: 4
- `characteristics_ch1.2.cell type`: flow sorted SSCs: 6; depleted MSCs: 4
- `characteristics_ch1.3.treatment`: AMB: 4; HU: 4; HU+recovery: 1; recovery AMB: 1
- `characteristics_ch1.4.duration`: 8 weeks: 4; 14 weeks: 4; 8 weeks + reloaded: 1; Reloading control: 1
- `cell`: SSC: 6; MSC: 4
- `trt`: AMB: 4; HU: 4; HUR: 1; AMBR: 1
- `dur`: w8: 4; w14: 4; w16: 2
- `grp`: AMB_w8: 2; HU_w8: 2; AMB_w14: 2; HU_w14: 2; HUR_w16: 1; AMBR_w16: 1

### Constant columns

- `status`: Public on Dec 01 2021
- `submission_date`: Aug 13 2020
- `last_update_date`: Dec 01 2021
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: C57BL/6
- `characteristics_ch1.1.tissue`: limb bone marrow
- `treatment_protocol_ch1`: Amb mice were ambulatory throughout the experimentation.  HU mice were tail suspended for the indicated duration.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Hind limbs bone marrow was flushed.  SSCs were isolated by FACS and RNA was isolated by mini-prep.  MSCs were derived by plating whole bone marrow and depletion before extraction by mini-prep.,RNA libraries were prepared for sequencing using standard Illumina protocols
- `data_processing`: Adapter sequences were removed using the cutadapt program,Sequences were aligned to the mouse genome via HISAT2,Alignments were mapped to gene transcripts using the featurecount program,Genome_build: mm9,Supplementary_files_format_and_content: csv file, raw transcript counts
- `platform_id`: GPL19057
- `contact_name`: Donald,G.,Phinney
- `contact_department`: Molecular Medicine
- `contact_institute`: The Scripps Research Institute
- `contact_address`: 130 Scripps Way Bldg A215
- `contact_city`: Jupiter
- `contact_state`: Florida
- `contact_zip/postal_code`: 33453
- `contact_country`: USA
- `instrument_model`: NextSeq 500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE156174
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM4726006 | 8wk ambulatory MSC |
| GSM4726007 | 8wk ambulatory SSC |
| GSM4726008 | 8wk hindlimb unloaded MSC |
| GSM4726009 | 8wk hindlimb unloaded SSC |
| GSM4726010 | 14wk ambulatory MSC |
| GSM4726011 | 14wk ambulatory SSC |
| GSM4726012 | 14wk hindlimb unloaded MSC |
| GSM4726013 | 14wk hindlimb unloaded SSC |
| GSM4726014 | hindlimb unloaded+recovery |
| GSM4726015 | recovery ambulatory |

## Values with exercise words (by column)

- `title`: 14wk hindlimb unloaded MSC, 14wk hindlimb unloaded SSC, 8wk hindlimb unloaded MSC, 8wk hindlimb unloaded SSC, hindlimb unloaded+recovery

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| grp | source_name_ch1 | 6 | 8/10 | 4 | 0 |
| grp | characteristics_ch1.2.cell type | 6 | 8/10 | 4 | 0 |
| title without the cell level | cell | 6 | 8/10 | 4 | 0 |
| grp | cell | 6 | 8/10 | 4 | 0 |
| grp | dur | 6 | 0/10 | 0 | 4 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "grp", "across": "_across", "within": [], "n_same_key_pairs": 4, "same_key_mean_r": 0.651, "other_mean_r": -0.129, "difference": 0.78, "permutation_p": 0.01199400299850075, "genes_used": 5706, "status": "not_supported"}
