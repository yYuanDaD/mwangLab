# Review packet A (facts only): GSE125630

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC6555821.paper.md`

## Paper outline

- # Transcriptome of dorsal root ganglia caudal to a spinal cord injury with modulated behavioral activity
- ## Abstract  `ABS` · abstract
- ## Background & Summary  `S1` · introduction
- ## Methods  `S2` · methods
- ### Animals  `S2.1` · methods
- ### Experimental design and SCI  `S2.2` · methods
- ### Tissue collection and RNA extraction  `S2.3` · methods
- ### Library preparation and sequencing  `S2.4` · methods
- ### RNA-seq data analysis  `S2.5` · methods
- ## Data Records  `S3` · other
- ## Technical Validation  `S4` · other
- ### Quality assessment  `S4.1` · other
- ### Gene expression variation of biological replicates  `S4.2` · other
- ### Potential batch effects  `S4.3` · other
- ## ISA-Tab metadata file  `S5` · supplementary
- ### (untitled)  `S5.1` · supplementary
- ## ISA-Tab metadata  `BK1` · other
- ## Author Contributions  `BK2` · other
- ## Code Availability  `DA` · data_availability
- ## Competing Interests  `BK3` · other
- ## Accession mentions

## Metadata (24 samples)

### Grouping columns (level: count)

- `characteristics_ch1.0.injury type`: T2 Contusion: 16; T2 Complete transection: 4; No SCI: 4
- `characteristics_ch1.1.weeks after injury?`: 13.5: 10; 11.5: 10; 8.5: 4
- `wpi`: w13p5: 10; w11p5: 10; w8p5: 4
- `injury`: T2 Contusion: 16; T2 Complete transection: 4; No SCI: 4
- `grp`: CONT: 6; SWIM: 5; SWW: 5; TX: 4; NoSCI: 4

### Constant columns

- `status`: Public on Apr 29 2019
- `submission_date`: Jan 24 2019
- `last_update_date`: Apr 29 2019
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: dorsal root ganglion
- `organism_ch1`: Rattus norvegicus
- `taxid_ch1`: 10116
- `characteristics_ch1.2.strain`: Sprague Dawley
- `treatment_protocol_ch1`: Animals were given either T2 complete transection SCI, T2 contusion SCI, or no SCI. A subset of contused SCI animals were exposed to either swimming or shallow water walking exercise.
- `growth_protocol_ch1`: All rats were housed initially in standard cages and maintained in a continuous 12h-light/dark cycle. Tap water and a standard rodent diet were available to all rats ad libitum.
- `molecule_ch1`: polyA RNA
- `extract_protocol_ch1`: Animals were perfused with PBS supplemented with 20% RNAlater (Ambion, Life Technologies). T11-L4 bilateral DRGs were retrieved from both sides of the spinal column and collected in QIAzol (Qiagen). Total RNA from each sample was isolated with RNeasy Lipid Tissue Mini Kit (Qiagen).,Libraries were pr ... [135 more characters]
- `data_processing`: Illumina BaseSpace FastQ v1.0.0 used for basecalling,Raw sequences were checked for quality values using fastQC v0.10.1.  Quality trimming was not deemed necessary.,The sequences were directly aligned to the Rattus norvegicus reference genome assembly (Rn6) using Star version 2.6.,Read counts for ge ... [442 more characters]
- `platform_id`: GPL20084
- `contact_name`: Eric,Christian,Rouchka
- `contact_email`: eric.rouchka@louisville.edu
- `contact_laboratory`: KY INBRE Bioinformatics Core
- `contact_department`: Biochemistry and Molecular Genetics
- `contact_institute`: University of Louisville
- `contact_address`: 522 East Gray Street
- `contact_city`: Louisville
- `contact_state`: Kentucky
- `contact_zip/postal_code`: 40292
- `contact_country`: USA
- `instrument_model`: NextSeq 500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE125630,GSE129704
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`, `key`, `_norm_key`

### Samples

| sample | title |
|---|---|
| GSM3579147 | Contusion SCI + SWIM, Replicate 1 |
| GSM3579148 | Contusion SCI + SWIM, Replicate 2 |
| GSM3579149 | Contusion SCI + SWIM, Replicate 3 |
| GSM3579150 | Contusion SCI + SWIM, Replicate 4 |
| GSM3579151 | Contusion SCI + SWIM, Replicate 5 |
| GSM3579152 | Contusion SCI + SWW, Replicate 1 |
| GSM3579153 | Contusion SCI + SWW, Replicate 2 |
| GSM3579154 | Contusion SCI + SWW, Replicate 3 |
| GSM3579155 | Contusion SCI + SWW, Replicate 4 |
| GSM3579156 | Contusion SCI + SWW, Replicate 5 |
| GSM3579157 | Complete transection SCI, Replicate 1 |
| GSM3579158 | Complete transection SCI, Replicate 2 |
| GSM3579159 | Complete transection SCI, Replicate 3 |
| GSM3579160 | Complete transection SCI, Replicate 4 |
| GSM3579161 | No SCI, Replicate 1 |
| GSM3579162 | No SCI, Replicate 2 |
| GSM3579163 | No SCI, Replicate 3 |
| GSM3579164 | No SCI, Replicate 4 |
| GSM3579165 | Contusion SCI, Replicate 1 |
| GSM3579166 | Contusion SCI, Replicate 2 |
| GSM3579167 | Contusion SCI, Replicate 3 |
| GSM3579168 | Contusion SCI, Replicate 4 |
| GSM3579169 | Contusion SCI, Replicate 5 |
| GSM3579170 | Contusion SCI, Replicate 6 |

## Values with exercise words (by column)

- `title`: Contusion SCI + SWIM, Replicate 1, Contusion SCI + SWIM, Replicate 2, Contusion SCI + SWIM, Replicate 3, Contusion SCI + SWIM, Replicate 4, Contusion SCI + SWIM, Replicate 5
- `treatment_protocol_ch1`: Animals were given either T2 complete transection SCI, T2 contusion SCI, or no SCI. A subset of contused SCI animals were exposed to either swimming or shallow water walking exercise.
- `supplementary_file_1`: ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM3579nnn/GSM3579147/suppl/GSM3579147_SS_01B_TCEX5_IN_SWIM_1-113370403_NORM.bw, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM3579nnn/GSM3579148/suppl/GSM3579148_SS_01_DRG_TCEx6_IN_SWIM_2-113219143_NORM.bw, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM3579nnn/GSM3579149/suppl/GSM3579149_SS_02_DRG_TCEx19_IN_SWIM_3-113217163_NORM.bw, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM3579nnn/GSM3579150/suppl/GSM3579150_SS_03_DRG_TCEx20_IN_SWIM_4-113213147_NORM.bw, ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM3579nnn/GSM3579151/suppl/GSM3579151_SS_04_DRG_TCEx23_IN_SWIM_5-113222140_NORM.bw
- `key`: Contusion_SWIM_1, Contusion_SWIM_2, Contusion_SWIM_3, Contusion_SWIM_4, Contusion_SWIM_5
- `_norm_key`: contusionswim1, contusionswim2, contusionswim3, contusionswim4, contusionswim5
- `grp`: SWIM

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.0.injury type level | characteristics_ch1.0.injury type | 16 | 12/24 | 4 | 0 |
| key without the characteristics_ch1.0.injury type level | characteristics_ch1.0.injury type | 16 | 12/24 | 4 | 0 |
| title without the injury level | injury | 16 | 12/24 | 4 | 0 |
| key without the injury level | injury | 16 | 12/24 | 4 | 0 |
| grp (without characteristics_ch1.0.injury type) + suffix of title | characteristics_ch1.0.injury type | 24 | 0/24 | 0 | 0 |
| grp (without characteristics_ch1.0.injury type) + suffix of key | characteristics_ch1.0.injury type | 24 | 0/24 | 0 | 0 |
| grp (without characteristics_ch1.1.weeks after injury?) + suffix of title | characteristics_ch1.1.weeks after injury? | 24 | 0/24 | 0 | 0 |
| grp (without characteristics_ch1.1.weeks after injury?) + suffix of key | characteristics_ch1.1.weeks after injury? | 24 | 0/24 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the characteristics_ch1.0.injury type level", "across": "_across", "within": [], "n_same_key_pairs": 12, "same_key_mean_r": -0.017, "other_mean_r": 0.0, "difference": -0.017, "permutation_p": 0.6026986506746627, "genes_used": 10320, "status": "not_supported"}
