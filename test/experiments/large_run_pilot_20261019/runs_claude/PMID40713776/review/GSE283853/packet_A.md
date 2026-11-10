# Review packet A (facts only): GSE283853

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC12296675.paper.md`

## Paper outline

- # Large MAF transcription factors reawaken evolutionarily dormant fast-glycolytic type IIb myofibers in human skeletal muscle
- ## Abstract  `ABS` · abstract
- ## Background  `S1` · introduction
- ## Methods  `S2` · methods
- ### Human iPS cloning and generation of muscle stem cells  `S2.1` · methods
- ### Isolation of iMuSCs through flow cytometric sorting  `S2.2` · methods
- ### Re-culture and myogenic differentiation of sorted iMuSCs  `S2.3` · methods
- ### Preparation and culture of primary bovine muscle stem cells  `S2.4` · methods
- ### Overexpression of Adenovirus-mediated large MAFs  `S2.5` · methods
- ### Immunofluorescence  `S2.6` · methods
- ### Analysis of actively translated mRNA in human myotubes using AHA-mediated ribosomal isolation  `S2.7` · methods
- ### Quantitative analysis of transcripts using reverse transcription PCR  `S2.8` · methods
- ### RNAscope  `S2.9` · methods
- ### RNA-seq analysis of human iMuSC-derived myotubes  `S2.10` · methods
- ### Seahorse XF Glycolysis stress test  `S2.11` · methods
- ### Single-nucleus RNA-seq analysis  `S2.12` · methods
- ### Mass spectrometry  `S2.13` · methods
- ### Comparison of gene expression patterns across multiple animal species  `S2.14` · methods
- ### Motif enrichment analysis  `S2.15` · methods
- ### Study participants  `S2.16` · methods
- ### Evaluation of muscle fiber composition in human muscle biopsy samples  `S2.17` · methods
- ### RNA-seq analysis of human muscle biopsy samples  `S2.18` · methods
- ### Statistical analysis  `S2.19` · methods
- ## Results  `S3` · results
- ### Large MAFs as conserved regulators of MYH4 across species and human aging  `S3.1` · results
- ### Large MAFs specifically induce MYH4 expression in human skeletal muscle cells  `S3.2` · results
- ### Large MAFs as key regulators of type IIb myofiber-specific and glycolytic gene programs in human skeletal muscle cells  `S3.3` · results
- ### Large MAF expression levels determine MYH4 expression in human skeletal muscle tissue  `S3.4` · results
- ## Discussion  `S4` · discussion
- ## Electronic supplementary material  `S5` · supplementary
- ## Author contributions  `BK1` · other
- ## Funding  `BK2` · other
- ## Data availability  `DA` · data_availability
- ## Declarations  `BK3` · other
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `grp`: mCherry: 3; MAFA: 3; MAFB: 3; MAF: 3

### Constant columns

- `status`: Public on Jul 30 2025
- `submission_date`: Dec 09 2024
- `last_update_date`: Jul 30 2025
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: skeletal muscle
- `organism_ch1`: Homo sapiens
- `taxid_ch1`: 9606
- `characteristics_ch1.0.tissue`: skeletal muscle
- `characteristics_ch1.1.cell line`: 414C2
- `characteristics_ch1.2.cell type`: iPS cell-derived myotubes
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted from human myotubes on day 4 of infection using TRIzol reagent (Thermo Fisher Scientific, Waltham, MA, USA).,The RNA-seq library was prepared using the NEBNext Ultra Directional RNA Library Prep Kit (New England Biolabs, Ipswich, MA, USA) after ribosomal RNA (rRNA) depletion  ... [50 more characters]
- `data_processing`: CLC Genomics Workbench (Version 10.1.1; Qiagen, Hilden, Netherlands),Assembly: hg19,Supplementary files format and content: Excel files include expression values normalized by quantile
- `platform_id`: GPL18573
- `contact_name`: Shunya,,Sadaki
- `contact_email`: sadaki.shunya@gmail.com
- `contact_institute`: Kyoto University
- `contact_address`: Yoshida-Konoe-cho, Sakyo-ku
- `contact_city`: Kyoto
- `contact_state`: Kyoto
- `contact_zip/postal_code`: 606-8501
- `contact_country`: Japan
- `instrument_model`: NextSeq 500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE283853
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`, `lib`

### Samples

| sample | title | description |
|---|---|---|
| GSM8673172 | pAV-mCherry_1 | Library name: m1 |
| GSM8673173 | pAV-mCherry_2 | Library name: m2 |
| GSM8673174 | pAV-mCherry_3 | Library name: m3 |
| GSM8673175 | pAV-MAFA_1 | Library name: a1 |
| GSM8673176 | pAV-MAFA_2 | Library name: a2 |
| GSM8673177 | pAV-MAFA_3 | Library name: a3 |
| GSM8673178 | pAV-MAFB_1 | Library name: b1 |
| GSM8673179 | pAV-MAFB_2 | Library name: b2 |
| GSM8673180 | pAV-MAFB_3 | Library name: b3 |
| GSM8673181 | pAV-MAF_1 | Library name: c1 |
| GSM8673182 | pAV-MAF_2 | Library name: c2 |
| GSM8673183 | pAV-MAF_3 | Library name: c3 |

## Values with exercise words (by column)

- none found

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the grp level | grp | 3 | 12/12 | 3 | 0 |
| suffix of title | grp | 3 | 12/12 | 3 | 0 |
| suffix of description | grp | 12 | 0/12 | 0 | 0 |
| suffix of lib | grp | 12 | 0/12 | 0 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "title without the grp level", "across": "_across", "within": [], "n_same_key_pairs": 18, "same_key_mean_r": 0.222, "other_mean_r": -0.111, "difference": 0.334, "permutation_p": 0.0004997501249375312, "genes_used": 10370, "status": "supported"}
