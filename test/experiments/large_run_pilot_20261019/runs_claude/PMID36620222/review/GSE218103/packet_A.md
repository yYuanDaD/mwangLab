# Review packet A (facts only): GSE218103

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

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.group`: TD CON: 3; CP CON: 3; TD EX: 3; CP EX: 3
- `characteristics_ch1.2.treatment`: control: 6; aerobic exercise: 6
- `geno`: TD: 6; CP: 6
- `time`: pre: 6; post: 6

### Constant columns

- `status`: Public on Dec 10 2022
- `submission_date`: Nov 16 2022
- `last_update_date`: Dec 11 2022
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Extracellular vesicles from plasma
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: Extracellular vesicles from plasma
- `treatment_protocol_ch1`: Blood was collected before and 30 minutes after a bout of aerobic exercise
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was isolated from EVs using Qiazol Reagent (Qiagen, Carlsbad, CA, US) and ExoRNAeasy kit (Qiagen) according to the manufacturer鈥檚 instructions,Total RNA was sent to Norgen Biotek and picograms of RNA was utilized for library preparation.,library preparation and sequencing was performed by  ... [63 more characters]
- `data_processing`: Sequencing was performed in the NextSeq 500/550 High Output Kit v2 (51 Cycles using a 75-Cycle Kit) on the Illumina NextSeq 500 platform,Single-end reads for miRNAs were mapped to miRbase version 22 using BowTie2. The alignment was performed by Norgen Biotek using sRNAbench and sRNAtoolbox,Raw count ... [247 more characters]
- `platform_id`: GPL18573
- `contact_name`: Ivan,J,Vechetti
- `contact_email`: ivechetti@unl.edu
- `contact_phone`: 8596934315
- `contact_institute`: University of Nebraska-Lincoln
- `contact_address`: 1700 N. 35th Street
- `contact_city`: Lincoln
- `contact_state`: NE
- `contact_zip/postal_code`: 68583
- `contact_country`: USA
- `instrument_model`: NextSeq 500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE218103,GSE219100
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

## Values with exercise words (by column)

- `title`: Cerebral palsy exercise 1, Cerebral palsy exercise 2, Cerebral palsy exercise 3, Typically developed exercise 1, Typically developed exercise 2, Typically developed exercise 3
- `characteristics_ch1.1.group`: CP EX, TD EX
- `characteristics_ch1.2.treatment`: aerobic exercise
- `treatment_protocol_ch1`: Blood was collected before and 30 minutes after a bout of aerobic exercise

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.1.group | 3 | 12/12 | 3 | 0 |
| characteristics_ch1.2.treatment (without characteristics_ch1.1.group) + suffix of title | characteristics_ch1.1.group | 6 | 12/12 | 0 | 0 |
| time (without characteristics_ch1.1.group) + suffix of title | characteristics_ch1.1.group | 6 | 12/12 | 0 | 0 |
| title without the characteristics_ch1.2.treatment level | characteristics_ch1.2.treatment | 6 | 12/12 | 6 | 0 |
| geno (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 6 | 12/12 | 6 | 0 |
| characteristics_ch1.1.group (without geno) + suffix of title | geno | 6 | 12/12 | 6 | 0 |
| characteristics_ch1.2.treatment (without geno) + suffix of title | geno | 6 | 12/12 | 6 | 0 |
| time (without geno) + suffix of title | geno | 6 | 12/12 | 6 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 18, "same_key_mean_r": 0.038, "other_mean_r": -0.018, "difference": 0.055, "permutation_p": 0.08945527236381809, "genes_used": 153, "status": "not_supported"}
