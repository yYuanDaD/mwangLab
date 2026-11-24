# Review packet A (facts only): GSE74570

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC4985182.paper.md`

## Paper outline

- # Loss of NAD homeostasis leads to progressive and reversible degeneration of skeletal muscle
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Nampt-deficient muscle exhibits compromised energetics  `S2.1` · results
- ### mNKO mice develop myonecrosis and progressive loss of muscle function  `S2.2` · results
- ### Nicotinamide riboside functionally and morphologically restores NAD-deficient muscle  `S2.3` · results
- ### Gain of Nampt function maintains exercise capacity into old age  `S2.4` · results
- ## Discussion  `S3` · discussion
- ## Experimental procedures  `S4` · methods
- ### Generation of transgenic animals  `S4.1` · methods
- ### NR and NAM administration  `S4.2` · methods
- ### NAD and ATP measurement  `S4.3` · methods
- ### Mitochondrial isolation  `S4.4` · methods
- ### Mitochondrial respiration assays  `S4.5` · methods
- ### Statistical Analyses  `S4.6` · methods
- ## Supplementary Material  `S5` · supplementary
- ## Figures and tables  `FLT` · other
- ## Accession mentions

## Metadata (23 samples)

### Grouping columns (level: count)

- `characteristics_ch1.0.genotype`: wild type: 12; overexpressing Nampt in skeletal muscle: 7; deficient for Nampt in skeletal muscle: 4
- `characteristics_ch1.2.age`: 7 months: 8; 24 months: 8; 4 months: 7
- `extract_protocol_ch1`: Total RNA was purified from the Quadricep muscle (Trizol reagent, Life Technologies). Poly(A)+ RNA was isolated using oligo dT beads (Life Technologies, Frederick, MD).,RNA was fragmented for 7 minutes using Fragmentation Reagent (Life Technologies, Waltham, MA).  mRNA-seq libraries were then generated using the Illumina mRNA-seq kit (illumina, San Diego, CA).: 15; Total RNA was purified from the Quadricep muscle (miRNeasy; Qiagen, Valencia, CA). Poly(A)+ RNA was isolated using oligo dT beads (Life Technologies, Frederick, MD).,RNA was fragmented for 7 minutes using Fragmentation Reagent (Life Technologies, Waltham, MA).  mRNA-seq libraries were then generated using the Illumina mRNA-seq kit (illumina, San Diego, CA).: 8
- `geno`: WT: 12; OE: 7; KO: 4
- `age`: m7: 8; m24: 8; m4: 7
- `grp`: WT_m7: 4; KO_m7: 4; WT_m4: 4; WT_m24: 4; OE_m24: 4; OE_m4: 3

### Constant columns

- `status`: Public on Jul 22 2016
- `submission_date`: Nov 02 2015
- `last_update_date`: May 15 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Quadricep muscle
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.1.tissue`: quadricep muscle
- `characteristics_ch1.3.background strain`: C57BL/6
- `treatment_protocol_ch1`: Mice were occassionally subjected to glucose and exercise tolerance tests before sacrifice.
- `growth_protocol_ch1`: Mice were maintained under standard housing conditions on standard chow diet.
- `molecule_ch1`: polyA RNA
- `data_processing`: Reads were trimmed with Cutadapt (v1.4.2), mapped with Tophat2, and gene expression was quantified using HTseq (Trapnell et al. 2009; Martin 2011; Anders et al. 2015). DEseq2 was used perform differential expression analysis (Love et al. 2014).,Genome_build: mm10,Supplementary_files_format_and_conte ... [216 more characters]
- `platform_id`: GPL13112
- `contact_name`: Ian,M,Silverman
- `contact_email`: ian.silverman@gmail.com
- `contact_laboratory`: Brian D. Gregory Lab
- `contact_department`: Biology
- `contact_institute`: University of Pennsylvania
- `contact_address`: 433 South University Ave, Room 104
- `contact_city`: Philadelphia
- `contact_state`: Pennsylvania
- `contact_zip/postal_code`: 19104
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 2000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE74570
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM1923140 | WT_3691 |
| GSM1923141 | WT_3766 |
| GSM1923142 | WT_3788 |
| GSM1923143 | WT_3790 |
| GSM1923144 | mNamptKO_3685 |
| GSM1923145 | mNamptKO_3690 |
| GSM1923146 | mNamptKO_3696 |
| GSM1923147 | mNamptKO_4016 |
| GSM1923148 | WT_4m_1957 |
| GSM1923149 | WT_4m_1959 |
| GSM1923150 | WT_4m_1965 |
| GSM1923151 | WT_4m_1971 |
| GSM1923152 | MCK-NamptOE_4m_2010 |
| GSM1923153 | MCK-NamptOE_4m_2027 |
| GSM1923154 | MCK-NamptOE_4m_2035 |
| GSM1923155 | WT_24m_2372 |
| GSM1923156 | WT_24m_1044 |
| GSM1923157 | WT_24m_1279 |
| GSM1923158 | WT_24m_2373 |
| GSM1923159 | MCK-NamptOE_24m_1242 |
| GSM1923160 | MCK-NamptOE_24m_905 |
| GSM1923161 | MCK-NamptOE_24m_906 |
| GSM1923162 | MCK-NamptOE_24m_1357 |

## Values with exercise words (by column)

- `treatment_protocol_ch1`: Mice were occassionally subjected to glucose and exercise tolerance tests before sacrifice.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| grp | characteristics_ch1.0.genotype | 6 | 0/23 | 0 | 6 |
| grp | characteristics_ch1.2.age | 6 | 0/23 | 0 | 6 |
| grp | extract_protocol_ch1 | 6 | 0/23 | 0 | 6 |
| grp | geno | 6 | 0/23 | 0 | 6 |
| grp | age | 6 | 0/23 | 0 | 6 |
