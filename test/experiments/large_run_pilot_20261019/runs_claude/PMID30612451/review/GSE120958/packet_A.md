# Review packet A (facts only): GSE120958

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC6411426.paper.md`

## Paper outline

- # High Phosphate Diet Induces Exercise Intolerance and Impairs Fatty Acid Metabolism in Mice
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Methods  `S2` · methods
- ### Human studies.  `S2.1` · methods
- ### Animal Studies.  `S2.2` · methods
- ### Echocardiography.  `S2.3` · methods
- ### Plasma and urine mineral quantification.  `S2.4` · methods
- ### Muscle triglyceride measurements.  `S2.5` · methods
- ### Mouse body composition measurements.  `S2.6` · methods
- ### Treadmill exercise.  `S2.7` · methods
- ### Metabolic cage studies, FA, carbohydrate oxidation calculations.  `S2.8` · methods
- ### Cell Culture.  `S2.9` · methods
- ### Mitochondrial isolation and mitochondrial functional analysis.  `S2.10` · methods
- ### DNA extraction from tissue for mtDNA quantification.  `S2.11` · methods
- ### Muscle histology and Transmission electron microscopy.  `S2.12` · methods
- ### RNA sequencing (RNA-seq), GO, and Pathway Analysis.  `S2.13` · methods
- ## Statistical Analysis.  `S3` · methods
- ### Human studies:  `S3.1` · methods
- ### Animal studies:  `S3.2` · methods
- ## Results  `S4` · results
- ### Association between serum Pi and physical activity in the general population  `S4.1` · results
- ### High Pi diet induces exercise intolerance in normal mice  `S4.2` · results
- ### High phosphate diet reduces nonesterified fatty acid (NEFA) levels and fat oxidation during exercise  `S4.3` · results
- ### High Pi diet alters genes involved in FA synthesis, transport and release in skeletal muscle  `S4.4` · results
- ### High Pi media alters genes involved in fatty acid metabolism in C2C12 myotubes  `S4.5` · results
- ## Discussion  `S5` · discussion
- ## Supplementary Material  `S6` · supplementary
- ## Figures and tables  `FLT` · other
- ### What Is New?  `FLT.2` · other
- ### What Are the Clinical Implications?  `FLT.3` · other
- ## Accession mentions

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.diet`: normal phosphate: 3; high phosphate: 3
- `grp`: NP: 3; HP: 3

### Constant columns

- `status`: Public on Jan 08 2019
- `submission_date`: Oct 09 2018
- `last_update_date`: Mar 25 2026
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: gastrocnemius
- `characteristics_ch1.1.background strain`: C57BL/6
- `characteristics_ch1.3.diet time`: 12 weeks
- `treatment_protocol_ch1`: All experiments were performed using 20-24 week-old C57BL6 male mice obtained from UT Southwestern breeding core. Mice in the high Pi (HP) group were fed with diet containing 2.0% inorganic Pi (2.3% total Pi), TD08020, Envigo Teklad Diets, Madison, WI) for 12 weeks. Mice in the control group (NP) we ... [201 more characters]
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted from gastrocnemius muscle 12wks after treatment, using TRIzol (Invitrogen) according to the manufacturer's instructions.,RNA libraries were prepared for sequencing using standard Illumina protocols
- `data_processing`: Reads with phred quality scores less than 20 and less than 35 bp after trimming were removed from further analysis using trimgalore version 0.4.1.,Quality-filtered reads were then aligned to the mouse reference genome GRCm38 (mm10) using the HiSAT2 (v 2.0.1) (Pertea et al., 2016) aligner using defau ... [771 more characters]
- `platform_id`: GPL17021
- `contact_name`: Wanpen,,Vongpatanasin
- `contact_email`: wanpen.vongpatanasin@utsouthwestern.edu
- `contact_institute`: UT Southwestern Medical Center
- `contact_address`: 5323 Harry Hines Blvd
- `contact_city`: Dallas
- `contact_state`: TX
- `contact_zip/postal_code`: 75390
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE120958
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `source_name_ch1`, `relation`

### Samples

| sample | title |
|---|---|
| GSM3422122 | NP_1 |
| GSM3422123 | NP_2 |
| GSM3422124 | NP_3 |
| GSM3422125 | HP_1 |
| GSM3422126 | HP_2 |
| GSM3422127 | HP_3 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.2.diet | 3 | 6/6 | 3 | 0 |
| suffix of source_name_ch1 | characteristics_ch1.2.diet | 3 | 6/6 | 3 | 0 |
| title without the grp level | grp | 3 | 6/6 | 3 | 0 |
| suffix of title | grp | 3 | 6/6 | 3 | 0 |
| source_name_ch1 without the grp level | grp | 3 | 6/6 | 3 | 0 |
| suffix of source_name_ch1 | grp | 3 | 6/6 | 3 | 0 |
| grp (without characteristics_ch1.2.diet) + suffix of title | characteristics_ch1.2.diet | 6 | 0/6 | 0 | 0 |
| grp (without characteristics_ch1.2.diet) + suffix of source_name_ch1 | characteristics_ch1.2.diet | 6 | 0/6 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": 0.024, "other_mean_r": -0.013, "difference": 0.037, "permutation_p": 0.5077461269365318, "genes_used": 9821, "status": "not_supported"}
