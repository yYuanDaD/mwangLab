# Review packet A (facts only): GSE174785

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC8432967.paper.md`

## Paper outline

- # Exercise-induced angiogenesis is dependent on metabolically primed ATF3/4^+ endothelial cells
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### scRNA-seq reveals endothelial cell subpopulations in skeletal muscle  `S2.1` · results
- ### Muscle contains two capillary EC populations characterized by distinct Atf3/4 expression  `S2.2` · results
- ### Atf3/4^low WmECs have a lower angiogenic potential in vitro  `S2.3` · results
- ### Atf3/4 rewires AA metabolism to metabolically prime RmECs for angiogenesis  `S2.4` · results
- ### Exercise leads to selective expansion of RmECs  `S2.5` · results
- ### Deletion of Atf4 in ECs impairs exercise-induced endothelial proliferation and vascular expansion  `S2.6` · results
- ## Discussion  `S3` · discussion
- ### Limitations of study  `S3.1` · discussion
- ## STAR★Methods  `S4` · methods
- ### Key resources table  `S4.1` · methods
- ### Resource availability  `S4.2` · methods
- #### Lead contact  `S4.2.1` · methods
- #### Materials availability  `S4.2.2` · methods
- ### Experimental model and subject details  `S4.3` · methods
- #### Mice  `S4.3.1` · methods
- #### Isolation of primary muscle endothelial cells (ECs)  `S4.3.2` · methods
- ##### mEC isolation for scRNA-seq or mRNA analysis  `S4.3.2.1` · methods
- ##### Capillary mEC isolation for culturing  `S4.3.2.2` · methods
- ##### mEC isolation for metabolomics  `S4.3.2.3` · methods
- ##### Comparison of different mEC dissociation procedures  `S4.3.2.4` · methods
- #### Muscle explant ex vivo culture  `S4.3.3` · methods
- ### Method details  `S4.4` · methods
- #### Exercise experiments  `S4.4.1` · methods
- #### Single cell RNA-seq and data analysis  `S4.4.2` · methods
- #### Bulk RNA-seq and data analysis  `S4.4.3` · methods
- #### Cell culture  `S4.4.4` · methods
- ##### Knock down and overexpression plasmid constructions and lentiviral particle production  `S4.4.4.1` · methods
- #### Immunohistochemistry and histology  `S4.4.5` · methods
- #### RNA extraction and quantitative RT-PCR  `S4.4.6` · methods
- #### In vitro analysis of EC function  `S4.4.7` · methods
- ##### Proliferation  `S4.4.7.1` · methods
- ##### Scratch wound assay  `S4.4.7.2` · methods
- ##### Spheroid capillary sprouting assay  `S4.4.7.3` · methods
- #### Immunoblot analysis  `S4.4.8` · methods
- ##### Endothelial cells  `S4.4.8.1` · methods
- ##### Muscle samples  `S4.4.8.2` · methods
- ##### Amino acid uptake  `S4.4.8.3` · methods
- ##### Protein synthesis  `S4.4.8.4` · methods
- ##### Mass spectrometry analysis  `S4.4.8.5` · methods
- ##### Flow Cytometry  `S4.4.8.6` · methods
- ### Quantification and statistical analysis  `S4.5` · methods
- ## Supplemental information  `BK1` · supplementary
- ## Data and code availability  `DA` · data_availability
- ## Accession mentions

## Metadata (20 samples)

### Grouping columns (level: count)

- `source_name_ch1`: Soleus muscle: 10; Extensor digitorum longus muscle: 10
- `characteristics_ch1.2.genotype`: EC specific Atf4-/-: 10; Wild type: 10
- `muscle`: R: 10; W: 10
- `genotype`: KO: 10; WT: 10

### Constant columns

- `status`: Public on Jun 15 2021
- `submission_date`: May 20 2021
- `last_update_date`: Jun 15 2021
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.celltype`: Muscle endothelial cells
- `characteristics_ch1.1.strain`: C57BL/6N
- `treatment_protocol_ch1`: Recombination was induced in 8-10 weeks old mice by daily intraperitoneal administration of 1mg tamoxifen (T5648, Sigma-Aldrich) dissolved in 1:10 ethanol: corn oil solution for 5 consecutive days. A wash out period of at least 7 days was allowed before starting the experiments. Tamoxifen-treated Cr ... [64 more characters]
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: ECs were directly sorted (70 渭m nozzle) into 700 渭l RNA lysis buffer, and RNA extraction was performed using RNeasy Plus Micro Kit (74034 QIAGEN).,The libraries were prepared following Illumina TruSeq stranded mRNA protocol. The quality of the RNA and final libraries was determined using an Agilent  ... [181 more characters]
- `data_processing`: Expression values were computed using kallisto,Variance stabilizing transformation (VST) for negative binomial data with a dispersion-mean trend was used for exploratory analysis such as PCA and identification of highly variable genes.,Following DESeq2 analysis workflow, differential expression anal ... [814 more characters]
- `platform_id`: GPL24247
- `contact_name`: Hubert,,Rehrauer
- `contact_email`: Hubert.Rehrauer@fgcz.ethz.ch
- `contact_department`: FGCZ
- `contact_institute`: ETH Zurich / University of Zurich
- `contact_address`: Winterthurerstr. 190
- `contact_city`: Zurich
- `contact_zip/postal_code`: 8057
- `contact_country`: Switzerland
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE174785
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`

### Samples

| sample | title |
|---|---|
| GSM5328123 | Oxidative mECs ATf4-/- rep1 |
| GSM5328124 | Oxidative mECs ATf4-/- rep2 |
| GSM5328125 | Oxidative mECs ATf4-/- rep3 |
| GSM5328126 | Oxidative mECs ATf4-/- rep4 |
| GSM5328127 | Oxidative mECs ATf4-/- rep5 |
| GSM5328128 | Glycolytic mECs Atf4-/- rep1 |
| GSM5328129 | Glycolytic mECs Atf4-/- rep2 |
| GSM5328130 | Glycolytic mECs Atf4-/- rep3 |
| GSM5328131 | Glycolytic mECs Atf4-/- rep4 |
| GSM5328132 | Glycolytic mECs Atf4-/- rep5 |
| GSM5328133 | Oxidative mECs WT rep1 |
| GSM5328134 | Oxidative mECs WT rep2 |
| GSM5328135 | Oxidative mECs WT rep3 |
| GSM5328136 | Oxidative mECs WT rep4 |
| GSM5328137 | Oxidative mECs WT rep5 |
| GSM5328138 | Glycolytic mECs WT rep1 |
| GSM5328139 | Glycolytic mECs WT rep2 |
| GSM5328140 | Glycolytic mECs WT rep3 |
| GSM5328141 | Glycolytic mECs WT rep4 |
| GSM5328142 | Glycolytic mECs WT rep5 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.2.genotype (without source_name_ch1) + suffix of title | source_name_ch1 | 10 | 20/20 | 10 | 0 |
| genotype (without source_name_ch1) + suffix of title | source_name_ch1 | 10 | 20/20 | 10 | 0 |
| source_name_ch1 (without characteristics_ch1.2.genotype) + suffix of title | characteristics_ch1.2.genotype | 10 | 20/20 | 10 | 0 |
| muscle (without characteristics_ch1.2.genotype) + suffix of title | characteristics_ch1.2.genotype | 10 | 20/20 | 10 | 0 |
| characteristics_ch1.2.genotype (without muscle) + suffix of title | muscle | 10 | 20/20 | 10 | 0 |
| genotype (without muscle) + suffix of title | muscle | 10 | 20/20 | 10 | 0 |
| source_name_ch1 (without genotype) + suffix of title | genotype | 10 | 20/20 | 10 | 0 |
| muscle (without genotype) + suffix of title | genotype | 10 | 20/20 | 10 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "characteristics_ch1.2.genotype (without source_name_ch1) + suffix of title", "across": "_across", "within": ["_within"], "n_same_key_pairs": 10, "same_key_mean_r": -0.018, "other_mean_r": 0.005, "difference": -0.023, "permutation_p": 0.8760619690154923, "genes_used": 11931, "status": "not_supported"}
