# Review packet A (facts only): GSE273795

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC11682372.paper.md`

## Paper outline

- # Pharmacological inactivation of a non-canonical gp130 signaling arm attenuates chronic systemic inflammation and multimorbidity induced by a high-fat diet
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Pharmacological inhibition of gp130/SFK signaling reduces inflammatory responses in mice on HFD  `S2.1` · results
- ### R159 mitigates degenerative changes induced by HFD in musculoskeletal tissues  `S2.2` · results
- ### R159 mitigates inflammation-induced decline in neurogenesis  `S2.3` · results
- ### R159 increased activity levels in mice on HFD  `S2.4` · results
- ## Discussion  `S3` · discussion
- ## Methods and materials  `S4` · methods
- ### Ethics  `S4.1` · methods
- ### Animals and treatments  `S4.2` · methods
- ### Serum ELISA  `S4.3` · methods
- ### Quantitative real-time PCR  `S4.4` · methods
- ### RNA sequencing library preparation and sequencing  `S4.5` · methods
- ### RNA sequencing data analysis  `S4.6` · methods
- ### Picro sirius red staining  `S4.7` · methods
- ### Immunohistochemistry (IHC)  `S4.8` · methods
- ### Micro-computed tomography (µCT) data collection and analysis  `S4.9` · methods
- ### Flow cytometry  `S4.10` · methods
- ### TRAP staining and quantification  `S4.11` · methods
- ### OARSI scoring  `S4.12` · methods
- ### Western blot  `S4.13` · methods
- ### Voluntary activity assay  `S4.14` · methods
- ### Brain tissue processing and staining  `S4.15` · methods
- ### Quantification of NSCs and neurogenesis  `S4.16` · methods
- ### Statistical analysis  `S4.17` · methods
- ## Electronic supplementary material  `S5` · supplementary
- ## Acknowledgements  `S6` · other
- ## Author contributions  `S7` · other
- ## Funding  `S8` · other
- ## Data availability  `S9` · data_availability
- ## Declarations  `S10` · other
- ### Competing interests  `S10.1` · other
- ## Accession mentions

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: HFD, R159: 3; HFD, Vehicle: 3
- `treat`: HFD, R159: 3; HFD, Vehicle: 3

### Constant columns

- `status`: Public on Jan 02 2025
- `submission_date`: Aug 01 2024
- `last_update_date`: Jan 02 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Liver
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Liver
- `characteristics_ch1.1.genotype`: C57BL/6
- `treatment_protocol_ch1`: 1-year-old aged male C57BL/6 mice were placed on high-fat diet and administered R159 or vehicle (Veh) twice a week via intraperitoneal injection for 12 weeks
- `molecule_ch1`: polyA RNA
- `extract_protocol_ch1`: Total RNA was isolated using QIAGEN RNeasy Mini kit and quantified using Qubit fluorometer (Thermo Fisher Scientific). Quality of the isolated RNA was checked using Agilent Bioanalyzer 2100. Universal Plus mRNA-Seq Library with NuQuant (TECAN) was used to generate stranded RNA-seq libraries. Briefly ... [596 more characters]
- `data_processing`: Quality of the raw fastq files were determined using FastQC(v0.11.9). Adapters were trimmed using Cutadapt.  Trimmed and filtered reads were aligned to mouse reference genome (mm39- GENCODE Release M30) using STAR aligner (version 2.7.8a). Transcript levels were quantified to the reference using a m ... [615 more characters]
- `platform_id`: GPL34290
- `contact_name`: Denis,,Evseenko
- `contact_email`: evseenko@usc.edu
- `contact_phone`: 323-219-0234
- `contact_laboratory`: Evseenko Lab
- `contact_department`: Orthopaedic Surgery
- `contact_institute`: University of Southern  California
- `contact_address`: 1450 Biggy St
- `contact_city`: Los Angeles
- `contact_state`: CA
- `contact_zip/postal_code`: 90033
- `contact_country`: USA
- `instrument_model`: Illumina NovaSeq X Plus
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE273795
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM8437093 | HFD-R159_rep1 |
| GSM8437094 | HFD-R159_rep2 |
| GSM8437095 | HFD-R159_rep3 |
| GSM8437096 | HFD-Veh_rep1 |
| GSM8437097 | HFD-Veh_rep2 |
| GSM8437098 | HFD-Veh_rep3 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.2.treatment | 3 | 6/6 | 3 | 0 |
| suffix of title | treat | 3 | 6/6 | 3 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": -0.036, "other_mean_r": 0.018, "difference": -0.054, "permutation_p": 0.6781609195402298, "genes_used": 8694, "status": "not_supported"}
