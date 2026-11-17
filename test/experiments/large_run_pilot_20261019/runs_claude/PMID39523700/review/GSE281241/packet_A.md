# Review packet A (facts only): GSE281241

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC11874633.paper.md`

## Paper outline

- # Actuating Extracellular Matrices Decouple the Mechanical and Biochemical Effects of Muscle Contraction on Motor Neurons
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Designing Extracellular Matrix Substrates to Enable Long‐Term Secretome Harvesting from Exercised Muscle Monolayers  `S2.1` · results
- ### Impact of Myokine Stimulation on Motor Neuron Growth  `S2.2` · results
- ### Impact of Dynamic Mechanical Stimulation on Motor Neuron Growth  `S2.3` · results
- ### Transcriptomic Impact of Exercise Stimulation on Motor Neurons  `S2.4` · results
- ## Discussion  `S3` · discussion
- ## Experimental Section  `S4` · methods
- ### Fabrication of Actuating Extracellular Matrices — Fibrin Formulation  `S4.1` · methods
- ### Magnetic Matrix Actuation  `S4.2` · methods
- ### Cell Culture — C2C12 Myoblasts  `S4.3` · methods
- ### HBG3 Embryonic Stem Cells  `S4.4` · methods
- ### Rheological Analysis  `S4.5` · methods
- ### Biochemical Stimulation  `S4.6` · methods
- ### Mechanical Stimulation  `S4.7` · methods
- ### RNA Sequencing  `S4.8` · methods
- ### RNA‐Seq Library Preparation  `S4.9` · methods
- ### RNA‐Seq Analysis  `S4.10` · methods
- ### Pathway Analysis  `S4.11` · methods
- ### Immunofluorescence Imaging  `S4.12` · methods
- ### Neuron Morphological Data Analysis  `S4.13` · methods
- ### Muscle Displacement Tracking and Force Calculations  `S4.14` · methods
- ### Fibrin Microstructure Analysis  `S4.15` · methods
- ### Gelatin Substrate Experiments  `S4.16` · methods
- ### Statistical Analysis  `S4.17` · methods
- ## Conflict of Interest  `S5` · other
- ## Supporting information  `S6` · supplementary
- ## Data Availability Statement  `DA` · data_availability
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.3.genotype`: ChR2::tdTomato: 6; Wild-Type: 6
- `grp`: ChR2: 6; WT: 6

### Constant columns

- `status`: Public on Nov 06 2024
- `submission_date`: Nov 06 2024
- `last_update_date`: Nov 06 2024
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Muscle
- `characteristics_ch1.1.cell line`: C2C12
- `characteristics_ch1.2.cell type`: myoblast
- `characteristics_ch1.4.treatment`: Differentiation media for 6 days
- `treatment_protocol_ch1`: Suspended 100k cells in a 24 wellplate (n=6) for each genotype. Seeded the cells onto a 1mm thick fibrin hydrogel consisting of 8 mg of fibrinogen/mL of GM+ media. GM+ consists of high glucose DMEM with sodium pyruvate, l-glutamine and glucose. We add 10% fetal bovine serum, 1% l-glutamine and 1% pe ... [314 more characters]
- `growth_protocol_ch1`: High glucose DMEM w/ l-glutamine, sodium pyruvate and glucose as the base, with 10% fetal bovine serum and 1% pen-strep for growth of these myoblasts.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: We extracted the multinucleated myofibril monolayers using the Rneasy mini kit with standard extraction protocols for adherent cell monolayers. Lysed the cells for 5 minutes and passed the lysate through the QIAshredder before continuing the Rneasy mini kit extraction protocol.,Ten microliters of un ... [709 more characters]
- `description`: instrument model: Singular Genomics G4
- `data_processing`: Fastq files were generated with the Illumina off-line basecaller (olb) v. 1.9.4.,Reads were aligned against mm10 (Feb., 2009) using bwa mem v. 0.7.12-r1039 with flags 鈥搕 16 鈥揻, and mapping rates, fraction of multiply-mapping reads, number of unique 20-mers at the 5麓 end of the reads, insert size dis ... [866 more characters]
- `platform_id`: GPL21103
- `contact_name`: Vincent,,Butty
- `contact_email`: vbutty@mit.edu
- `contact_laboratory`: BioMicro Center / IGE
- `contact_department`: Biology / Koch Institute / Bioengineering / CEHS
- `contact_institute`: Massachusetts Institute of Technology
- `contact_address`: 77 Massachusetts Avenue Bldg 68-317A
- `contact_city`: Cambridge
- `contact_state`: MA
- `contact_zip/postal_code`: 2139
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 4000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE281241,GSE281242
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`, `_norm_key`

### Samples

| sample | title |
|---|---|
| GSM8615539 | O1 |
| GSM8615540 | O2 |
| GSM8615541 | O3 |
| GSM8615542 | O4 |
| GSM8615543 | O5 |
| GSM8615544 | O6 |
| GSM8615545 | WT1 |
| GSM8615546 | WT2 |
| GSM8615547 | WT3 |
| GSM8615548 | WT4 |
| GSM8615549 | WT5 |
| GSM8615550 | WT6 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of key | characteristics_ch1.3.genotype | 6 | 12/12 | 6 | 0 |
| suffix of key | grp | 6 | 12/12 | 6 | 0 |
| grp (without characteristics_ch1.3.genotype) + suffix of key | characteristics_ch1.3.genotype | 12 | 0/12 | 0 | 0 |
| suffix of _norm_key | characteristics_ch1.3.genotype | 12 | 0/12 | 0 | 0 |
| grp (without characteristics_ch1.3.genotype) + suffix of _norm_key | characteristics_ch1.3.genotype | 12 | 0/12 | 0 | 0 |
| characteristics_ch1.3.genotype (without grp) + suffix of key | grp | 12 | 0/12 | 0 | 0 |
| suffix of _norm_key | grp | 12 | 0/12 | 0 | 0 |
| characteristics_ch1.3.genotype (without grp) + suffix of _norm_key | grp | 12 | 0/12 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of key", "across": "_across", "within": [], "n_same_key_pairs": 6, "same_key_mean_r": -0.05, "other_mean_r": 0.011, "difference": -0.061, "permutation_p": 0.7611194402798601, "genes_used": 10293, "status": "not_supported"}
