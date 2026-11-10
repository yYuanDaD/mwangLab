# Review packet A (facts only): GSE69699

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC4742069.paper.md`

## Paper outline

- # Genome-Wide Analysis of Acute Endurance Exercise-Induced Translational Regulation in Mouse Skeletal Muscle
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Materials and Methods  `S2` · methods
- ### Accession number  `S2.1` · data_availability
- ### Animals and endurance exercise  `S2.2` · methods
- ### Total RNA extraction for mRNA-Seq and ribosome profiling  `S2.3` · methods
- ### ribosomal RNA (rRNA) removal, 5′ phosphorylation, and 3′ dephosphorylation from RPF  `S2.4` · methods
- ### Sequence library preparation, sequencing, and alignment  `S2.5` · methods
- ### Reproducibility and validity of sequencing  `S2.6` · methods
- ### Sequenced data analysis  `S2.7` · methods
- ### Real time qPCR and western blotting  `S2.8` · methods
- ## Results  `S3` · results
- ## Discussion  `S4` · discussion
- ## Supporting Information  `S5` · supplementary
- ## Acknowledgments  `S6` · other
- ## Data Availability  `S7` · data_availability
- ## Funding Statement  `S8` · other
- ## Accession mentions

## Metadata (8 samples)

### Grouping columns (level: count)

- `characteristics_ch1.4.protocol`: control: 4; acute endurance exercise: 4
- `characteristics_ch1.5.profiling`: mRNA-Seq: 4; Ribo-Seq: 4
- `grp`: ctrl: 4; ex: 4
- `assay`: mRNA: 4; RPF: 4

### Constant columns

- `status`: Public on Feb 16 2016
- `submission_date`: Jun 09 2015
- `last_update_date`: May 15 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: gastrocnemius
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain`: C57BL/6
- `characteristics_ch1.1.tissue`: gastrocnemius
- `characteristics_ch1.2.age`: 9-10 weeks
- `characteristics_ch1.3.genotype/variation`: wild type
- `treatment_protocol_ch1`: exercise mice underwent a 60min treadmill running at 20 m/min
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: After cycloheximide injection into right gastrocnemius, gastrocnemius was immediately harvested and flash-frozen in liquid nitrogen. The skeletal muscle was processed by either ribosome profiling or mRNA-Seq protocols, followed by Ion PGM total RNA-Seq protocols.,Sequence library was constructed usi ... [32 more characters]
- `data_processing`: Base-calling and alignment were conducted by using the built-in Ion torrent software (V4.0.1).,Sequenced reads shorter than 24 nt were removed.,Sequenced reads were mapped and aligned to coding DNA sequences extended to 25 nt upstream of translational start site of each gene, retrieved from Ensembl  ... [181 more characters]
- `platform_id`: GPL16331
- `contact_name`: Hiroaki,,Sako
- `contact_institute`: Waseda University
- `contact_address`: 2-579-15
- `contact_city`: Tokorozawa
- `contact_zip/postal_code`: 359-1192
- `contact_country`: Japan
- `instrument_model`: Ion Torrent PGM
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE69699
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM1707648 | mRNA-Seq no exercise rep1 |
| GSM1707649 | mRNA-Seq no exercise rep2 |
| GSM1707650 | mRNA-Seq exercise rep1 |
| GSM1707651 | mRNA-Seq exercise rep2 |
| GSM1707652 | Ribosome profiling no exercise rep1 |
| GSM1707653 | Ribosome profiling no exercise rep2 |
| GSM1707654 | Ribosome profiling exercise rep1 |
| GSM1707655 | Ribosome profiling exercise rep2 |

## Values with exercise words (by column)

- `title`: Ribosome profiling exercise rep1, Ribosome profiling exercise rep2, Ribosome profiling no exercise rep1, Ribosome profiling no exercise rep2, mRNA-Seq exercise rep1, mRNA-Seq exercise rep2, mRNA-Seq no exercise rep1, mRNA-Seq no exercise rep2
- `characteristics_ch1.4.protocol`: acute endurance exercise
- `treatment_protocol_ch1`: exercise mice underwent a 60min treadmill running at 20 m/min
- `supplementary_file_1`: ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1707nnn/GSM1707650/suppl/GSM1707650_Gastro_mRNA_Ex0min_Rep1_RPM.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1707nnn/GSM1707651/suppl/GSM1707651_Gastro_mRNA_Ex0min_Rep2_RPM.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1707nnn/GSM1707654/suppl/GSM1707654_Gastro_RPF_Ex0min_Rep1_RPM.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1707nnn/GSM1707655/suppl/GSM1707655_Gastro_RPF_Ex0min_Rep2_RPM.txt.gz
- `grp`: ex

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.5.profiling (without characteristics_ch1.4.protocol) + suffix of title | characteristics_ch1.4.protocol | 4 | 8/8 | 4 | 0 |
| assay (without characteristics_ch1.4.protocol) + suffix of title | characteristics_ch1.4.protocol | 4 | 8/8 | 4 | 0 |
| characteristics_ch1.4.protocol (without characteristics_ch1.5.profiling) + suffix of title | characteristics_ch1.5.profiling | 4 | 8/8 | 4 | 0 |
| grp (without characteristics_ch1.5.profiling) + suffix of title | characteristics_ch1.5.profiling | 4 | 8/8 | 4 | 0 |
| characteristics_ch1.5.profiling (without grp) + suffix of title | grp | 4 | 8/8 | 4 | 0 |
| assay (without grp) + suffix of title | grp | 4 | 8/8 | 4 | 0 |
| characteristics_ch1.4.protocol (without assay) + suffix of title | assay | 4 | 8/8 | 4 | 0 |
| grp (without assay) + suffix of title | assay | 4 | 8/8 | 4 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "characteristics_ch1.5.profiling (without characteristics_ch1.4.protocol) + suffix of title", "across": "_across", "within": ["_within"], "n_same_key_pairs": 4, "same_key_mean_r": 0.149, "other_mean_r": -0.149, "difference": 0.297, "permutation_p": 0.25037481259370314, "genes_used": 1008, "status": "not_supported"}
