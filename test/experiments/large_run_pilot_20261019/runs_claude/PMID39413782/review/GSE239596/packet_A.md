# Review packet A (facts only): GSE239596

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC11706709.paper.md`

## Paper outline

- # Vagal Sensory Neuron-Derived FGF3 Controls Insulin
- ## Abstract  `ABS` · abstract
- ## Introduction:  `S1` · introduction
- ## Results:  `S2` · results
- ### Transcriptome profiling of the vagal sensory ganglia under acute metabolic
- ### Systemic and vagal sensory-derived Fgf3 enhance insulin secretion:  `S2.2` · results
- ### Pancreas-projecting vagal sensory Fgf3 modulates insulin secretion:  `S2.3` · results
- ### Vagal afferent signaling regulates insulin secretion:  `S2.4` · results
- ## Discussion:  `S3` · discussion
- ### Limitations of the study:  `S3.1` · discussion
- ## STAR Methods  `S4` · methods
- ### Resource availability  `S4.1` · methods
- #### Lead contact  `S4.1.1` · methods
- #### Materials availability  `S4.1.2` · methods
- #### Data and code availability  `S4.1.3` · data_availability
- ### Experimental model and study participant details  `S4.2` · methods
- #### Animals:  `S4.2.1` · methods
- #### S961 and high-fat diet studies:  `S4.2.2` · methods
- ### Method details  `S4.3` · methods
- #### RNA sequencing:  `S4.3.1` · methods
- #### RNA sequencing data analysis:  `S4.3.2` · methods
- #### Intravenous tail-vein injection:  `S4.3.3` · methods
- #### Nodose ganglia injection:  `S4.3.4` · methods
- #### Pancreas intraductal injection:  `S4.3.5` · methods
- #### Islet isolation and glucose-stimulated insulin secretion:  `S4.3.6` · methods
- #### Afferent vagal nerve stimulation:  `S4.3.7` · methods
- #### Electrocardiogram (ECG) recording:  `S4.3.8` · methods
- #### Real-Time Quantitative Reverse Transcription Polymerase Chain Reaction
- #### Pancreas immunostaining and islet morphometric studies:  `S4.3.10` · methods
- ### Quantification and statistical analysis  `S4.4` · methods
- ## Supplementary Material  `S5` · supplementary
- ## Figures and tables  `FLT` · other
- ## Accession mentions

## Metadata (6 samples)

### Grouping columns (level: count)

- `grp`: PBS: 3; S961: 3

### Constant columns

- `status`: Public on Aug 04 2024
- `submission_date`: Jul 28 2023
- `last_update_date`: Aug 04 2024
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: spinal cord
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: spinal cord
- `characteristics_ch1.1.cell line`: vagal jugular-nodose ganglia
- `characteristics_ch1.2.cell type`: jugular-nodose ganglia
- `characteristics_ch1.3.genotype`: WT
- `characteristics_ch1.4.treatment`: S961
- `treatment_protocol_ch1`: C57BL/6J male mice were anesthetized and infused, using osmotic pumps (ALZET) implanted subcutaneously, with PBS alone or PBS with the insulin receptor antagonist S961 at the dose of 10 nmoles/week for two weeks. For high-fat diet experiments, mice were challenged with a diet containing 60% kcal fat ... [56 more characters]
- `growth_protocol_ch1`: Mice were housed in pathogen-free facilities and maintained on a 12-hour light/dark cycle in the Animal Care Facility at the Child Health Institute of New Jersey and New York Medical College. All studies and protocols were approved by the Rutgers University and New York Medical College Animal Care a ... [482 more characters]
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: RNA samples were quantified and assessed for quality using Agilent BioAnalyzer (Agilent Technologies, Palo Alto, CA, USA).  The RIN values were 7.95 +/- 0.86 [6.6 to 9.1] and a median concentration of 48.5 ng/ul but with a very wide range [1.8 to 266.6] ng/ul.,Illumina sequencing libraries were prep ... [749 more characters]
- `data_processing`: Image analysis and base calling were conducted by the HiSeq Control Software (HCS). Raw sequence data (.bcl files) generated from Illumina HiSeq was converted into fastq files and de-multiplexed using Illumina bcl2fastq 2.20 software. The RNA-seq data analyses were performed as previously described  ... [2177 more characters]
- `platform_id`: GPL13112
- `contact_name`: Ying-Tao,,Zhao
- `contact_email`: yzhao47@nyit.edu
- `contact_laboratory`: Jerry Zhao Lab
- `contact_department`: Biomedical Sciences
- `contact_institute`: New York Institute of Technology
- `contact_address`: Riland building, Room 024 Northern Boulevard, P.O. Box 8000
- `contact_city`: Old Westbury
- `contact_state`: NY
- `contact_zip/postal_code`: 11568
- `contact_country`: USA
- `instrument_model`: Illumina HiSeq 2000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `series_id`: GSE239596
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `supplementary_file_1`, `supplementary_file_2`, `supplementary_file_3`

### Samples

| sample | title |
|---|---|
| GSM7668477 | NG_Ctrl 1 |
| GSM7668478 | NG_Ctrl 2 |
| GSM7668479 | NG_Ctrl 3 |
| GSM7668480 | NG_Treat 1 |
| GSM7668481 | NG_Treat 2 |
| GSM7668482 | NG_Treat 3 |

## Values with exercise words (by column)

- `data_processing`: Image analysis and base calling were conducted by the HiSeq Control Software (HCS). Raw sequence data (.bcl files) generated from Illumina HiSeq was converted into fastq files and de-multiplexed using Illumina bcl2fastq 2.20 software. The RNA-seq data analyses were performed as previously described [64, 65]. Briefly, the FASTQ files were aligned to mouse mm10 genome using STAR 2.7.7a [66] with the following parameters: 鈥樷搑unThreadN 40 鈥搊utFilterMultimapNmax 1 鈥搊utFilterMismatchNmax 3 鈥搊utFilterScoreMinOverLread 0.25 鈥搊utFilterMatchNminOverLread 0.25鈥. A Perl script was used to calculate the total number of mapped reads and the number of reads that aligned to the exons of each gene. The table of raw read counts was normalized, and the top 1000 variable genes were selected to perform the principal component analysis by DESeq2 [67] and to perform the distance between variables by pheatmap. The edgeR [68] and the Genewise Negative Binomial Generalized Linear Models with Quasi-likelihood Tests (glmQLFTest) were used to compare the gene expression levels between the groups. The false discovery rate (FDR) < 0.05 was used as the cutoff to identify differentially expressed genes (DEGs). The functional enrichment analysis was performed using g:Profiler (version_e106_eg53_p16_65fcd97) and Gene set enrichment analysis (GSEA) software [69]. The list of DEGs were used as the input files for g:Profiler. Briefly, the Benjamini-Hochberg FDR with a threshold of 0.05 was used to determine the statistical significance and carried out to detect the Gene Ontology (GO), Reactome, and KEGG pathway. The gene ratio was defined as the intersection size divided by the query size. The intersection size, gene ratio, and adjusted P-value were used as input to generate a dot plot for GO enrichment analysis. The TPM values from edgeR were used as input files for the GSEA analysis. Briefly, the msigdb.v2022.1.Mm.symbols.gmt was used as gene sets database and Mouse-Gene_Symbol_Remapping_MsigDB.v2022.1.Mm.Chip was used as the chip platform. The parameters of 鈥1000 permutation鈥, 鈥榗ollapse鈥 and 鈥榞ene_set as permutation type鈥 were selected to run GSEA. The scripts used in this study are available at GitHub repository (https://github.com/Jerry-Zhao/NG2023).,Assembly: mm10,Supplementary files format and content: bigwig format files including the tracks for the data,Supplementary files format and content: tab-delimited text files include raw read count values for each sample

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | grp | 3 | 6/6 | 3 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "suffix of title", "across": "_across", "within": [], "n_same_key_pairs": 3, "same_key_mean_r": 0.361, "other_mean_r": -0.196, "difference": 0.556, "permutation_p": 0.17641179410294852, "genes_used": 10933, "status": "not_supported"}
