# Review packet A (facts only): GSE122628

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\PMID31433691\abstract_PMID31433691.txt`

## Metadata (6 samples)

### Grouping columns (level: count)

- `source_name_ch1`: acute electrical stimulation (S): 3; unstimulated sham control (U): 3
- `characteristics_ch1.4.treatment`: Exercised: 3; Not Exercised: 3
- `grp`: STIM: 3; SHAM: 3

### Constant columns

- `status`: Public on Apr 14 2020
- `submission_date`: Nov 16 2018
- `last_update_date`: Apr 14 2020
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.strain background`: C57BL/6J
- `characteristics_ch1.1.genotype/variation`: WT
- `characteristics_ch1.2.age`: 14 weeks
- `characteristics_ch1.3.Sex`: male
- `characteristics_ch1.5.tissue`: skeletal muscle
- `characteristics_ch1.6.tissue`: gastrocnemius-soleus complexes
- `characteristics_ch1.7.cell type`: CD146+CD45-CD31- pericytes
- `treatment_protocol_ch1`: 14 week-old WT mice were randomly assigned to a unstimulated sham control (U) or an acute electrical stimulation (S) group.  Males (n=3/group) were equally represented in each of the two groups. Crural muscles (anterior, posterior, and lateral muscles responsible for foot movement) are stimulated to ... [484 more characters]
- `growth_protocol_ch1`: All mice were housed in the animal facility at the University of Illinois in a temperature-controlled specific pathogen-free animal room maintained on a 12:12 light-dark cycle. The animals were fed standard laboratory chow and water ad libitum. Protocols for animal use were approved by the Instituti ... [93 more characters]
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: The sorted CD146+CD45-CD31- pericytes were frozen in QIAzol Lysis Reagent and later homogenized and processed using the Qiagen miRNeasy Mini Kit. Spectrophotometer was used to determine approximate concentration and quality control was performed using the 2100  Bioanalyzer (Agilent, Santa Clara, CA) ... [118 more characters]
- `data_processing`: The libraries were quantitated by qPCR and sequenced on one lane for 101 cycles from one end of the fragments on a HiSeq 4000 using a HiSeq 4000 sequencing kit version 1.,Fastq files were generated and demultiplexed with with the bcl2fastq v2.17.1.14 Conversion Software (Illumina).,Each sample's fas ... [1030 more characters]
- `platform_id`: GPL21103
- `contact_name`: Marni,,Boppart
- `contact_email`: mboppart@illinois.edu
- `contact_laboratory`: Molecular Muscle Physiology
- `contact_department`: Kinesiology
- `contact_institute`: University of Illinois at Champaign-Urbana
- `contact_address`: 405 N Matthews
- `contact_city`: Urbana
- `contact_zip/postal_code`: 61801
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 4000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE122628
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `supplementary_file_1`, `key`

### Samples

| sample | title | description |
|---|---|---|
| GSM3476630 | Stim 1 [S1] | S1_ATTCAGAA-ATAGAGGC_L002,WT, exercised, replicate 1 |
| GSM3476631 | Stim 2 [S2] | S2_GAATTCGT-ATAGAGGC_L002,WT, exercised, replicate 1 |
| GSM3476632 | Stim 3 [S3] | S3_CTGAAGCT-ATAGAGGC_L002,WT, exercised, replicate 1 |
| GSM3476633 | Unstim 1 [U1] | U1_TCCGGAGA-ATAGAGGC_L002,WT, not exercised, replicate 1 |
| GSM3476634 | Unstim 2 [U2] | U2_CGCTCATT-ATAGAGGC_L002,WT, not exercised, replicate 1 |
| GSM3476635 | Unstim 3 [U3] | U3_GAGATTCC-ATAGAGGC_L002,WT, not exercised, replicate 1 |

## Values with exercise words (by column)

- `source_name_ch1`: acute electrical stimulation (S)
- `characteristics_ch1.4.treatment`: Exercised, Not Exercised
- `treatment_protocol_ch1`: 14 week-old WT mice were randomly assigned to a unstimulated sham control (U) or an acute electrical stimulation (S) group.  Males (n=3/group) were equally represented in each of the two groups. Crural muscles (anterior, posterior, and lateral muscles responsible for foot movement) are stimulated to rotate from 19掳 of ankle dorsiflexion to 19掳 ankle plantarflexion (for eccentric contraction) and vice versa (for concentric contraction). The electrical stimulation is then applied for a total of 40 contractions (20 eccentric and 20 concentric) lasting approximately 10 minutes per animal. Mice were euthanized via carbon dioxide asphyxiation 3 hr post-exercise. The gastrocnemius-soleus complexes were rapidly dissected and processed for cell sorting of CD146+CD45-CD31- pericytes.
- `description`: S1_ATTCAGAA-ATAGAGGC_L002,WT, exercised, replicate 1, S2_GAATTCGT-ATAGAGGC_L002,WT, exercised, replicate 1, S3_CTGAAGCT-ATAGAGGC_L002,WT, exercised, replicate 1, U1_TCCGGAGA-ATAGAGGC_L002,WT, not exercised, replicate 1, U2_CGCTCATT-ATAGAGGC_L002,WT, not exercised, replicate 1, U3_GAGATTCC-ATAGAGGC_L002,WT, not exercised, replicate 1
- `data_processing`: The libraries were quantitated by qPCR and sequenced on one lane for 101 cycles from one end of the fragments on a HiSeq 4000 using a HiSeq 4000 sequencing kit version 1.,Fastq files were generated and demultiplexed with with the bcl2fastq v2.17.1.14 Conversion Software (Illumina).,Each sample's fastq file run through trimmomatic (v 0.36) to first remove any remaining standard Illumina adapters, then trim bases from both ends with quality scores below 28, and finally to remove reads shorter than 30 bp (parameters ILLUMINACLIP:$EBROOTTRIMMOMATIC/adapters/TruSeq3-SE:2:15:10 LEADING:28 TRAILING:28 MINLEN:30),Salmon (v 0.8.2) was used to quasi-map reads to Gencode's Release M17 transcript sequences with arguments --seqBias, --gcBias and --numBootstraps=30,tximport (v 1.8.0, R 3.5.1) was used to sum the transcript counts to the gene level using the lengthScaledTPM method,Genome_build: Gencode M17, based on GRCm38,Supplementary_files_format_and_content: The quant.sf files are tab-delimited text files containing transcript names, lengths, effective lengths, Transcript Per Million values and estimated count values. The gene-level counts are in the tab-delimited supplementary data file Boppart_GeneCounts_GEO.txt; these counts were analyzed directly using the edgeR-quasi method, and hence are the final normalized data.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of key | source_name_ch1 | 6 | 0/6 | 0 | 0 |
| characteristics_ch1.4.treatment (without source_name_ch1) + suffix of key | source_name_ch1 | 6 | 0/6 | 0 | 0 |
| grp (without source_name_ch1) + suffix of key | source_name_ch1 | 6 | 0/6 | 0 | 0 |
| suffix of key | characteristics_ch1.4.treatment | 6 | 0/6 | 0 | 0 |
| source_name_ch1 (without characteristics_ch1.4.treatment) + suffix of key | characteristics_ch1.4.treatment | 6 | 0/6 | 0 | 0 |
| grp (without characteristics_ch1.4.treatment) + suffix of key | characteristics_ch1.4.treatment | 6 | 0/6 | 0 | 0 |
| suffix of key | grp | 6 | 0/6 | 0 | 0 |
| source_name_ch1 (without grp) + suffix of key | grp | 6 | 0/6 | 0 | 0 |
