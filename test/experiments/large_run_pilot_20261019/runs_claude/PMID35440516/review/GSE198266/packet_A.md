# Review packet A (facts only): GSE198266

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC9085230.paper.md`

## Paper outline

- # Muscle fiber type-dependence effect of exercise on genomic networks in aged mice models
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## INTRODUCTION  `S1` · introduction
- ## RESULTS  `S2` · results
- ### Principal component analysis (PCA) plots and heatmaps  `S2.1` · results
- ### Identification of DEGs between YC vs. OC in SOL and GAS and commonly expressed DEGs  `S2.2` · results
- ### Identification of DEGs between YC vs. YE in SOL and GAS and commonly expressed DEGs  `S2.3` · results
- ### Identification of DEGs between OC vs. OE in SOL and GAS and commonly expressed DEGs  `S2.4` · results
- ### Gene Ontology (GO) term and Kyoto Encyclopedia of Genes and Genomes (KEGG) pathway enrichment analyses using DEGs of SOL/GAS in young and old groups  `S2.5` · results
- ### Gene set enrichment analysis (GSEA) for apoptosis in SOL and GAS  `S2.6` · results
- ### GSEA analysis for myogenesis in SOL and GAS  `S2.7` · results
- ## DISCUSSION  `S3` · discussion
- ### Effect of muscle fiber type on gene expression is greater than that of aging and exercise  `S3.1` · discussion
- ### Common DEGs with aging are related to apoptosis, circadian rhythm, and immune signaling  `S3.2` · discussion
- ### Common DEGs with exercise are associated with circadian rhythm and insulin signaling in young groups and hemoglobin subunit in old groups  `S3.3` · discussion
- ### Differences in metabolism according to muscle fiber type and significant upregulation of BCAA degradation in SOL compared to that in GAS  `S3.4` · discussion
- ### Necessity for different interventions depending on the muscle fiber type due to different patterns of apoptosis and myogenesis with aging  `S3.5` · discussion
- ### Mitigation of apoptosis and augmentation of myogenesis in old groups by chronic aerobic exercise in GAS but not in SOL  `S3.6` · discussion
- ## CONCLUSION  `S4` · conclusion
- ## MATERIALS AND METHODS  `S5` · methods
- ### Animals  `S5.1` · methods
- ### Exercise protocol  `S5.2` · methods
- ### SOL and GAS RNA extraction  `S5.3` · methods
- ### RNA-Seq library preparation and sequencing  `S5.4` · methods
- ### Data pre-processing and quality check  `S5.5` · methods
- ### Bioinformatics tools  `S5.6` · methods
- #### PCA analysis, heatmap, and Venn diagram  `S5.6.1` · methods
- #### DEG analysis  `S5.6.2` · methods
- #### GO and KEGG pathway enrichment analysis  `S5.6.3` · methods
- #### GSEA  `S5.6.4` · methods
- ## Supplementary Materials  `S6` · supplementary
- ## Accession mentions

## Metadata (24 samples)

### Grouping columns (level: count)

- `source_name_ch1`: soleus of young control: 3; soleus of young exercise: 3; soleus of old control: 3; soleus of old exercise: 3; gastrocnemius of young control: 3; gastrocnemius of young exercise: 3; gastrocnemius of old control: 3; gastrocnemius of old exercise: 3
- `characteristics_ch1.0.age`: 9-weeks-old: 12; 84-weeks-old: 12
- `characteristics_ch1.2.intervention`: control: 12; 4 weeks of treadmill exercise: 12
- `tissue`: SOL: 12; GAS: 12
- `grp`: YC: 6; YE: 6; OC: 6; OE: 6
- `mouse`: YC_1: 2; YC_2: 2; YC_3: 2; YE_1: 2; YE_2: 2; YE_4: 2; OC_3: 2; OC_4: 2; OC_5: 2; OE_1: 2; OE_2: 2; OE_3: 2

### Constant columns

- `status`: Public on Mar 14 2022
- `submission_date`: Mar 09 2022
- `last_update_date`: Mar 15 2022
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.1.gender`: male
- `treatment_protocol_ch1`: Before 4 weeks of treadmill exercise were performed, adaptation  exercise was previously performed, mice were familiarized  with the treadmill for 15 min/session at a 0 m/min for 3 min, 5m/  min for 2 min and 8 m/min for 10 min and 6掳 incline once a day for  3 days prior to the experimental day. In  ... [437 more characters]
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNAwas extracted from mice skeletal muscles using a total RNA  extraction kit (Ribozol, Amresco) following manufacture鈥檚 manual.,RNA libraries were prepared for sequencing using standard affymetrix protocol
- `data_processing`: We preprocessed the raw reads from the sequencer to remove low quality and adapter sequence before analysis and aligned the processed reads to the Mus musculus (mm10) using HISAT v2.1.0(1).,HISAT utilizes two types of indexes for alignment (a global, whole-genome index and tens of thousands of small ... [1353 more characters]
- `platform_id`: GPL24247
- `contact_name`: Summin,,Lee
- `contact_email`: snu7212@snu.ac.kr
- `contact_phone`: 1073347212
- `contact_institute`: Seoul National university
- `contact_address`: 1, gwanak-ro
- `contact_city`: Seoul
- `contact_state`: Gwanak-gu
- `contact_zip/postal_code`: 8826
- `contact_country`: South Korea
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE198266
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM5942476 | soleus of young control 1 | N_SOL_YC-1 |
| GSM5942477 | soleus of young control 2 | N_SOL_YC-2 |
| GSM5942478 | soleus of young control 3 | N_SOL_YC-3 |
| GSM5942479 | soleus of young exercise 1 | N_SOL_YE-1 |
| GSM5942480 | soleus of young exercise 2 | N_SOL_YE-2 |
| GSM5942481 | soleus of young exercise 4 | N_SOL_YE-4 |
| GSM5942482 | soleus of old control 3 | N_SOL_OC-3 |
| GSM5942483 | soleus of old control 4 | N_SOL_OC-4 |
| GSM5942484 | soleus of old control 5 | N_SOL_OC-5 |
| GSM5942485 | soleus of old exercise 1 | N_SOL_OE-1 |
| GSM5942486 | soleus of old exercise 2 | N_SOL_OE-2 |
| GSM5942487 | soleus of old exercise 3 | N_SOL_OE-3 |
| GSM5942488 | gastrocnemius of young control 1 | N_GAS_YC-1 |
| GSM5942489 | gastrocnemius of young control 2 | N_GAS_YC-2 |
| GSM5942490 | gastrocnemius of young control 3 | N_GAS_YC-3 |
| GSM5942491 | gastrocnemius of young exercise 1 | N_GAS_YE-1 |
| GSM5942492 | gastrocnemius of young exercise 2 | N_GAS_YE-2 |
| GSM5942493 | gastrocnemius of young exercise 4 | N_GAS_YE-4 |
| GSM5942494 | gastrocnemius of old control 3 | N_GAS_OC-3 |
| GSM5942495 | gastrocnemius of old control 4 | N_GAS_OC-4 |
| GSM5942496 | gastrocnemius of old control 5 | N_GAS_OC-5 |
| GSM5942497 | gastrocnemius of old exercise 1 | N_GAS_OE-1 |
| GSM5942498 | gastrocnemius of old exercise 2 | N_GAS_OE-2 |
| GSM5942499 | gastrocnemius of old exercise 3 | N_GAS_OE-3 |

## Values with exercise words (by column)

- `title`: gastrocnemius of old exercise 1, gastrocnemius of old exercise 2, gastrocnemius of old exercise 3, gastrocnemius of young exercise 1, gastrocnemius of young exercise 2, gastrocnemius of young exercise 4, soleus of old exercise 1, soleus of old exercise 2, soleus of old exercise 3, soleus of young exercise 1, soleus of young exercise 2, soleus of young exercise 4
- `source_name_ch1`: gastrocnemius of old exercise, gastrocnemius of young exercise, soleus of old exercise, soleus of young exercise
- `characteristics_ch1.2.intervention`: 4 weeks of treadmill exercise
- `treatment_protocol_ch1`: Before 4 weeks of treadmill exercise were performed, adaptation  exercise was previously performed, mice were familiarized  with the treadmill for 15 min/session at a 0 m/min for 3 min, 5m/  min for 2 min and 8 m/min for 10 min and 6掳 incline once a day for  3 days prior to the experimental day. In 4 weeks of treadmill exercise,  mice allocated to perform treadmill running were subject to  6掳 incline and for warm up, 2 min speed of 0 m/min, speed of 5m/  min, 8 m/min, 10 m/min for 1 min each, and then 12 m/min for  30 min at first week, 2 m/min were increased every weeks, and cool  down at 5 m/min for 2 min for 1 session (37 min). 2 session/day  were performed. Between the session, there were at least 1 h break  time was given.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| grp (without tissue) + suffix of title | tissue | 12 | 24/24 | 12 | 0 |
| mouse (without tissue) + suffix of title | tissue | 12 | 24/24 | 12 | 0 |
| description without the tissue level | tissue | 12 | 24/24 | 12 | 0 |
| grp (without tissue) + suffix of description | tissue | 12 | 24/24 | 12 | 0 |
| mouse (without tissue) + suffix of description | tissue | 12 | 24/24 | 12 | 0 |
| mouse | tissue | 12 | 24/24 | 12 | 0 |
| tissue (without grp) + suffix of title | grp | 10 | 22/24 | 0 | 0 |
| description without the grp level | grp | 10 | 22/24 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "grp (without tissue) + suffix of title", "across": "_across", "within": ["_within"], "n_same_key_pairs": 12, "same_key_mean_r": 0.108, "other_mean_r": -0.054, "difference": 0.161, "permutation_p": 0.0239880059970015, "genes_used": 5301, "status": "not_supported"}
