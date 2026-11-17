# Review packet A (facts only): GSE219099

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

## Metadata (6 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: Control scramble miRNA: 3; miR-486: 3
- `grp`: scr: 3; mir486: 3

### Constant columns

- `status`: Public on Dec 10 2022
- `submission_date`: Nov 30 2022
- `last_update_date`: Dec 11 2022
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: C2C12
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.cell line`: C2C12
- `characteristics_ch1.1.cell type`: Myoblast
- `treatment_protocol_ch1`: C2C12 myoblasts were transfected with either a mirVana miR-486 mimic or a scramble miRNA sequence (Life Technologies) used as a negative control. This control sequence does not target any known mature miRNA. Transfection was performed using lipofectamine2000 (Life Technologies), according to the man ... [378 more characters]
- `growth_protocol_ch1`: The skeletal muscle C2C12 (ATCC, CRL-1772) myoblasts were cultured in Dulbecco's Modified Eagles Medium (DMEM) supplemented with 10% Fetal Bovine Serum (FBS), 100 units/ml of Penicillin and 100 碌g/ml of Streptomycin until reaching 60-70% confluency.
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: RNA extraction was performed using TRI reagent (Sigma-Aldrich, St. Louis, MO, USA) coupled with further columns-based processing using the Direct-zol Kit (Zymo Research, Irvine, CA, USA).,Total RNA was sent to Novogene for library prep.
- `description`: Poly-A enrichment
- `data_processing`: High-throughput sequencing is transformed to sequenced reads (called Raw Data or Raw Reads) by CASAVA base recognition (Base Calling). Raw data are stored in FASTQ (fq) format files, which contain sequences of reads and corresponding base quality.,Paired-end reads for mRNAs were mapped to mm10 versi ... [339 more characters]
- `platform_id`: GPL17021
- `contact_name`: Ivan,J,Vechetti
- `contact_email`: ivechetti@unl.edu
- `contact_phone`: 8596934315
- `contact_institute`: University of Nebraska-Lincoln
- `contact_address`: 1700 N. 35th Street
- `contact_city`: Lincoln
- `contact_state`: NE
- `contact_zip/postal_code`: 68583
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE219099,GSE219100
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM6771531 | Control 1 |
| GSM6771532 | Control 2 |
| GSM6771533 | Control 3 |
| GSM6771534 | miR-486 1 |
| GSM6771535 | miR-486 2 |
| GSM6771536 | miR-486 3 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.2.treatment level | characteristics_ch1.2.treatment | 3 | 6/6 | 3 | 0 |
| suffix of title | characteristics_ch1.2.treatment | 3 | 6/6 | 3 | 0 |
| suffix of title | grp | 3 | 6/6 | 3 | 0 |
| grp (without characteristics_ch1.2.treatment) + suffix of title | characteristics_ch1.2.treatment | 6 | 0/6 | 0 | 0 |
| characteristics_ch1.2.treatment (without grp) + suffix of title | grp | 6 | 0/6 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the characteristics_ch1.2.treatment level", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": -0.076, "other_mean_r": 0.036, "difference": -0.113, "permutation_p": 0.8295852073963018, "genes_used": 10067, "status": "not_supported"}
