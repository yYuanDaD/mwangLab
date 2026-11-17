# Review packet A (facts only): GSE219100

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC9811128.paper.md`

## Paper outline

- # Extracellular vesicle characteristics and microRNA content in cerebral palsy and typically developed individuals at rest and in response to aerobic exercise
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Materials and methods  `S2` · methods
- ### Study design  `S2.1` · methods
- ### Participants  `S2.2` · methods
- ### Exercise bouts and blood sampling  `S2.3` · methods
- ### Extracellular vesicle isolation from human plasma  `S2.4` · methods
- ### Nanoparticle tracking analysis  `S2.5` · methods
- ### RNA isolation and small RNA sequencing  `S2.6` · methods
- ### In silico prediction of miR-486 target genes  `S2.7` · methods
- ### C2C12 culture and miR-486 mimetic  `S2.8` · methods
- ### Data analysis  `S2.9` · methods
- ## Results  `S3` · results
- ### Heart rate and rate of perceived exertion  `S3.1` · results
- ### EV concentration and size  `S3.2` · results
- ### microRNA cargo in EVs  `S3.3` · results
- ## Discussion  `S4` · discussion
- ## Data availability statement  `DA` · data_availability
- ## Ethics statement  `BK1` · other
- ## Author contributions  `BK2` · other
- ## Funding  `BK3` · other
- ## Conflict of interest  `BK4` · other
- ## Publisher’s note  `BK5` · other
- ## Supplementary material  `BK6` · supplementary
- ## Accession mentions

## Metadata (18 samples)

### Grouping columns (level: count)

- `submission_date`: Nov 16 2022: 12; Nov 30 2022: 6
- `source_name_ch1`: Extracellular vesicles from plasma: 12; C2C12: 6
- `organism_ch1`: Homo sapiens: 12; Mus musculus: 6
- `taxid_ch1`: 9606: 12; 10090: 6
- `characteristics_ch1.0.tissue`: Extracellular vesicles from plasma: 12; : 6
- `characteristics_ch1.1.group`: : 6; TD CON: 3; CP CON: 3; TD EX: 3; CP EX: 3
- `characteristics_ch1.2.treatment`: control: 6; aerobic exercise: 6; Control scramble miRNA: 3; miR-486: 3
- `treatment_protocol_ch1`: Blood was collected before and 30 minutes after a bout of aerobic exercise: 12; C2C12 myoblasts were transfected with either a mirVana miR-486 mimic or a scramble miRNA sequence (Life Technologies) used as a negative control. This control sequence does not target any known mature miRNA. Transfection was performed using lipofectamine2000 (Life Technologies), according to the manufacturer's instructions. Shortly, lipofectamine complexes were stabilized in OptiMEM (Gibco) for 5鈥塵in and incubated with the miRNA probes, diluted to 25鈥塶M in OptiMEM, for 20鈥塵in. Finally, the lipofectamine/probe complexes were added to the cells in a medium without antibiotics. After 6 hours of incubation, fresh media was added, and cells were harvested following 24 hours.: 6
- `extract_protocol_ch1`: Total RNA was isolated from EVs using Qiazol Reagent (Qiagen, Carlsbad, CA, US) and ExoRNAeasy kit (Qiagen) according to the manufacturer鈥檚 instructions,Total RNA was sent to Norgen Biotek and picograms of RNA was utilized for library preparation.,library preparation and sequencing was performed by Norgen Biotek using the Small RNA Library Prep Kit (Cat. 63600): 12; RNA extraction was performed using TRI reagent (Sigma-Aldrich, St. Louis, MO, USA) coupled with further columns-based processing using the Direct-zol Kit (Zymo Research, Irvine, CA, USA).,Total RNA was sent to Novogene for library prep.: 6
- `data_processing`: Sequencing was performed in the NextSeq 500/550 High Output Kit v2 (51 Cycles using a 75-Cycle Kit) on the Illumina NextSeq 500 platform,Single-end reads for miRNAs were mapped to miRbase version 22 using BowTie2. The alignment was performed by Norgen Biotek using sRNAbench and sRNAtoolbox,Raw counts were acquired with featurecounts and they were used as input for the statistical analysis, using DESeq2,Assembly: Gencode version 22 (hg38),Supplementary files format and content: tab-delimited text files include raw count values for each Sample: 12; High-throughput sequencing is transformed to sequenced reads (called Raw Data or Raw Reads) by CASAVA base recognition (Base Calling). Raw data are stored in FASTQ (fq) format files, which contain sequences of reads and corresponding base quality.,Paired-end reads for mRNAs were mapped to mm10 version of the mouse genome using STAR. The alignment was performed by Novogene.,Raw counts were acquired with featurecounts and they were used as input for the statistical analysis, using DESeq2.,Supplementary files format and content: mm10,Supplementary files format and content: Tab-delimited text files include count values for each Sample.: 6
- `platform_id`: GPL18573: 12; GPL17021: 6
- `instrument_model`: NextSeq 500: 12; Illumina HiSeq 2500: 6
- `series_id`: GSE218103,GSE219100: 12; GSE219099,GSE219100: 6
- `characteristics_ch1.0.cell line`: : 12; C2C12: 6
- `characteristics_ch1.1.cell type`: : 12; Myoblast: 6
- `growth_protocol_ch1`: : 12; The skeletal muscle C2C12 (ATCC, CRL-1772) myoblasts were cultured in Dulbecco's Modified Eagles Medium (DMEM) supplemented with 10% Fetal Bovine Serum (FBS), 100 units/ml of Penicillin and 100 碌g/ml of Streptomycin until reaching 60-70% confluency.: 6
- `description`: : 12; Poly-A enrichment: 6

### Constant columns

- `status`: Public on Dec 10 2022
- `last_update_date`: Dec 11 2022
- `type`: SRA
- `channel_count`: 1
- `molecule_ch1`: total RNA
- `contact_name`: Ivan,J,Vechetti
- `contact_email`: ivechetti@unl.edu
- `contact_phone`: 8596934315
- `contact_institute`: University of Nebraska-Lincoln
- `contact_address`: 1700 N. 35th Street
- `contact_city`: Lincoln
- `contact_state`: NE
- `contact_zip/postal_code`: 68583
- `contact_country`: USA
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM6734687 | Typically developed control 1 |
| GSM6734688 | Typically developed control 2 |
| GSM6734689 | Typically developed control 3 |
| GSM6734690 | Cerebral palsy control 1 |
| GSM6734691 | Cerebral palsy control 2 |
| GSM6734692 | Cerebral palsy control 3 |
| GSM6734693 | Typically developed exercise 1 |
| GSM6734694 | Typically developed exercise 2 |
| GSM6734695 | Typically developed exercise 3 |
| GSM6734696 | Cerebral palsy exercise 1 |
| GSM6734697 | Cerebral palsy exercise 2 |
| GSM6734698 | Cerebral palsy exercise 3 |
| GSM6771531 | Control 1 |
| GSM6771532 | Control 2 |
| GSM6771533 | Control 3 |
| GSM6771534 | miR-486 1 |
| GSM6771535 | miR-486 2 |
| GSM6771536 | miR-486 3 |

## Values with exercise words (by column)

- `title`: Cerebral palsy exercise 1, Cerebral palsy exercise 2, Cerebral palsy exercise 3, Typically developed exercise 1, Typically developed exercise 2, Typically developed exercise 3
- `characteristics_ch1.1.group`: CP EX, TD EX
- `characteristics_ch1.2.treatment`: aerobic exercise
- `treatment_protocol_ch1`: Blood was collected before and 30 minutes after a bout of aerobic exercise

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.2.treatment level | characteristics_ch1.2.treatment | 9 | 18/18 | 0 | 0 |
| characteristics_ch1.1.group (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 15 | 6/18 | 0 | 0 |
| submission_date (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 6 | 6/18 | 0 | 3 |
| source_name_ch1 (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 6 | 6/18 | 0 | 3 |
| organism_ch1 (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 6 | 6/18 | 0 | 3 |
| taxid_ch1 (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 6 | 6/18 | 0 | 3 |
| characteristics_ch1.0.tissue (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 6 | 6/18 | 0 | 3 |
| treatment_protocol_ch1 (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 6 | 6/18 | 0 | 3 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the characteristics_ch1.2.treatment level", "across": "_across", "within": [], "n_same_key_pairs": 9, "same_key_mean_r": 0.065, "other_mean_r": -0.003, "difference": 0.068, "permutation_p": 0.2158920539730135, "genes_used": 380, "status": "not_supported"}
