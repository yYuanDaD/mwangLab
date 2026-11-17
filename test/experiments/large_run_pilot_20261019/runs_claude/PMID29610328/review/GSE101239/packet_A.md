# Review packet A (facts only): GSE101239

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC5910824.paper.md`

## Paper outline

- # Ectopic neurogenesis induced by prenatal antiepileptic drug exposure augments seizure susceptibility in adult mice
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## (untitled)  `S0` · other
- ## Results  `S1` · results
- ### Prenatal VPA Exposure Increases Seizure Susceptibility and Ectopic Hippocampal Neurogenesis in Adult Mice.  `S1.1` · results
- ### Developmental Stage-Dependent Gene Expression Differences in NS/PCs Between Control and VPA Mice.  `S1.2` · results
- ### Prenatal VPA Exposure Leads to Perturbation in the Expression of Cell Migration-Associated Genes in Adult NS/PCs.  `S1.3` · results
- ### Voluntary Exercise Ameliorates Enhanced Seizure Susceptibility and Abnormal Neuronal Migration in VPA Mice by Normalizing Perturbed Gene Expression in NS/PCs.  `S1.4` · results
- ## Discussion  `S2` · discussion
- ## Methods  `S3` · methods
- ## Supplementary Material  `S4` · supplementary
- ## Acknowledgments  `S5` · other

## Metadata (21 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.tissue`: hippocampal dentate gyrus: 15; forebrain: 6
- `characteristics_ch1.3.age`: 12 weeks old: 9; embryonic day15: 6; postnatal day5: 6
- `grp`: : 12; Ctrl: 3; VPA: 3; VPARun: 3

### Constant columns

- `status`: Public on Mar 15 2018
- `submission_date`: Jul 11 2017
- `last_update_date`: May 15 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Neural stem/progenitor cells
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.cell type`: Neural stem/progenitor cells
- `characteristics_ch1.1.strain`: C57BL/6
- `characteristics_ch1.4.genotype`: Nestin-EGFP
- `treatment_protocol_ch1`: Methylcellulose, as a control, or VPA (300mg/kg/day) was orally administered to pregnant Nestin-EGFP mice on E12, 13 and 14
- `molecule_ch1`: polyA RNA
- `extract_protocol_ch1`: Forebrains or dentate gyrus were dissected from Nestin-EGFP mice and GFP-positive cells were isolated by FACS. mRNAs were isolated from the cells  for the construction of sequencing libraries using Dynabeads mRNA DIRECT Micro Kit (Invitrogen) following the manufacturer's protocol,RNA libraries were  ... [57 more characters]
- `data_processing`: RNA seq was performed with 50-bp single-end sequencing by an Illumina Hiseq 2500. Obtained reads were processed with FASTX tool kit to remove short (<20bp) and low quality (quality score<20) reads, followed by trimming of the adaptor sequence.,Processed reads were mapped to the mouse genome mm10 gen ... [142 more characters]
- `platform_id`: GPL17021
- `contact_name`: Taito,,Matsuda
- `contact_email`: matsuda.taito@naist.ac.jp
- `contact_laboratory`: Laboratory of Neural Regeneration and Brain Repair
- `contact_institute`: Nara Institute of Science and Technology
- `contact_address`: 8916-5
- `contact_city`: Ikoma
- `contact_zip/postal_code`: 630-0192
- `contact_country`: Japan
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE101239
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM2700529 | Control E15 rep1 |
| GSM2700530 | Control E15 rep2 |
| GSM2700531 | Control E15 rep3 |
| GSM2700532 | VPA E15 rep1 |
| GSM2700533 | VPA E15 rep2 |
| GSM2700534 | VPA E15 rep3 |
| GSM2700535 | Control P5 rep1 |
| GSM2700536 | Control P5 rep2 |
| GSM2700537 | Control P5 rep3 |
| GSM2700538 | VPA P5 rep1 |
| GSM2700539 | VPA P5 rep2 |
| GSM2700540 | VPA P5 rep3 |
| GSM2700541 | Control 12w rep1 |
| GSM2700542 | Control 12w rep2 |
| GSM2700543 | Control 12w rep3 |
| GSM2700544 | VPA 12w rep1 |
| GSM2700545 | VPA 12w rep2 |
| GSM2700546 | VPA 12w rep3 |
| GSM2700547 | VPA+Run 12w rep1 |
| GSM2700548 | VPA+Run 12w rep2 |
| GSM2700549 | VPA+Run 12w rep3 |

## Values with exercise words (by column)

- `supplementary_file_1`: ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2700nnn/GSM2700547/suppl/GSM2700547_VPA_Run_12w_rep1.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2700nnn/GSM2700548/suppl/GSM2700548_VPA_Run_12w_rep2.txt.gz, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM2700nnn/GSM2700549/suppl/GSM2700549_VPA_Run_12w_rep3.txt.gz

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.3.age (without grp) + suffix of title | grp | 9 | 9/21 | 0 | 6 |
| suffix of title | characteristics_ch1.2.tissue | 3 | 0/21 | 0 | 3 |
| characteristics_ch1.3.age (without characteristics_ch1.2.tissue) + suffix of title | characteristics_ch1.2.tissue | 9 | 0/21 | 0 | 9 |
| grp (without characteristics_ch1.2.tissue) + suffix of title | characteristics_ch1.2.tissue | 12 | 0/21 | 0 | 3 |
| suffix of title | characteristics_ch1.3.age | 3 | 0/21 | 0 | 3 |
| characteristics_ch1.2.tissue (without characteristics_ch1.3.age) + suffix of title | characteristics_ch1.3.age | 6 | 0/21 | 0 | 6 |
| grp (without characteristics_ch1.3.age) + suffix of title | characteristics_ch1.3.age | 12 | 0/21 | 0 | 3 |
| suffix of title | grp | 3 | 0/21 | 0 | 3 |
