# Review packet A (facts only): GSE228869

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261028\papers\PMC11622572.paper.md`

## Paper outline

- # Fibro-adipogenic progenitor cells in skeletal muscle unloading: metabolic and functional impairments
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Methods  `S2` · methods
- ### Hindlimb suspension rat model  `S2.1` · methods
- ### Skeletal muscle stem cells isolation  `S2.2` · methods
- ### Flow cytometry analysis  `S2.3` · methods
- ### Adipogenic differentiation of FAPs  `S2.4` · methods
- ### RNA isolation, cDNA synthesis, and qPCR  `S2.5` · methods
- ### Statistical methods  `S2.6` · methods
- ### Bioenergetic analysis using seahorse technology  `S2.7` · methods
- ### RNA sequencing analysis  `S2.8` · methods
- ### Collective migration analysis using scratch assay  `S2.9` · methods
- ### Direct migration rate measuring  `S2.10` · methods
- ### Estimation of FAP’s population doubling time  `S2.11` · methods
- ### C2C12 myogenic differentiation induced by FAPs-conditioned medium  `S2.12` · methods
- ### Immunocytochemical staining  `S2.13` · methods
- ### Measurement of fusion index and myotubes width  `S2.14` · methods
- ## Results  `S3` · results
- ### Freshly isolated FAPs characterization  `S3.1` · results
- ### Functional unloading affected FAPs in vitro expansion rate and migration activity in time-dependent manner  `S3.2` · results
- ### The ability of FAPs to differentiate into adipocytes in vitro is significantly altered by the skeletal muscle functional unloading  `S3.3` · results
- ### Skeletal muscle unloading results in metabolic reprogramming of FAPs  `S3.4` · results
- ### FAPs conditioned medium affects wound healing and myogenic differentiation parameters in C2C12 myoblasts in unloading time-dependent manner  `S3.5` · results
- ### RNA-seq analysis confirmed unloading-induced alterations in mechanisms that control FAPs metabolisms and regenerative potential  `S3.6` · results
- ## Discussion  `S4` · discussion
- ### Study limitations  `S4.1` · discussion
- ## Conclusion  `S5` · conclusion
- ## Electronic supplementary material  `S6` · supplementary
- ## Acknowledgements  `S7` · other
- ## Abbreviations  `S8` · other
- ## Author contributions  `S9` · other
- ## Funding  `S10` · other
- ## Data availability  `S11` · data_availability
- ## Declarations  `S12` · other
- ### Ethics approval and consent to participate  `S12.1` · other
- ### Consent for publication  `S12.2` · other
- ### Competing interests  `S12.3` · other
- ## Contributor Information  `S14` · other
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.3.treatment`: Hindlimb suspension (HS): 8; Control: 4
- `characteristics_ch1.4.day of_hs`: 0: 4; 7: 4; 14: 4
- `characteristics_ch1.5.day of_differentiation`: 0: 6; 3: 6
- `grp`: C: 4; HS7: 4; HS14: 4
- `diff`: d0: 6; d3: 6

### Constant columns

- `status`: Public on Apr 10 2023
- `submission_date`: Apr 03 2023
- `last_update_date`: Apr 10 2023
- `type`: SRA
- `channel_count`: 1
- `organism_ch1`: Rattus norvegicus
- `taxid_ch1`: 10116
- `characteristics_ch1.0.tissue`: m. soleus
- `characteristics_ch1.1.cell line`: fibro-adipogenic progenitor cells
- `characteristics_ch1.2.cell type`: primary cells
- `treatment_protocol_ch1`: Cells were isoleted and cultured to subconfluent state.
- `growth_protocol_ch1`: Fibro-adipogenic progenitor cells (FAPs) were cultured in DMEM supplemented with 1% penicillin-streptomycin, 1% L-glutamine, 10% FBS (HyClone, USA) on cell culture dishes. Adipogenic differentiation of FAPs was stimulated by replacing the culture media with adipocyte induction medium composed of cul ... [103 more characters]
- `molecule_ch1`: polyA RNA
- `extract_protocol_ch1`: Total RNA was isolated from the cells with an Extract RNA kit (Evrogen, Russia),Libraries were constructed using TruSeq Stranded mRNA library prep kit
- `data_processing`: Read quality was checked for each sample using FastQC v0.11.9.,Sequenced reads were mapped to the mouse genome using mapper STAR v2.7 with rat reference genome Rnor_6.0 (Ensembl release 104) and annotation Rnor_6.0.104.chr.gtf,Aligned reads were count with featureCounts program v1.6.4.,Further analy ... [274 more characters]
- `platform_id`: GPL32190
- `contact_name`: Margarita,,Sorokina
- `contact_email`: komarovamy96@yandex.ru, sorokinamy96@yandex.ru
- `contact_institute`: Almazov National Medical Research Centre
- `contact_address`: Akkuratova 2
- `contact_city`: Saint-Petersburg
- `contact_zip/postal_code`: 197341, 123007
- `contact_country`: Russia
- `instrument_model`: NextSeq 2000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE228869
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `source_name_ch1`, `relation`

### Samples

| sample | title |
|---|---|
| GSM7140884 | Control, day0, rep1 |
| GSM7140885 | Control, day0, rep2 |
| GSM7140886 | Control, day3, rep1 |
| GSM7140887 | Control, day3, rep2 |
| GSM7140888 | HS7, day0, rep1 |
| GSM7140889 | HS7, day0, rep2 |
| GSM7140890 | HS7, day3, rep1 |
| GSM7140891 | HS7, day3, rep2 |
| GSM7140892 | HS14, day0, rep1 |
| GSM7140893 | HS14, day0, rep2 |
| GSM7140894 | HS14, day3, rep1 |
| GSM7140895 | HS14, day3, rep2 |

## Values with exercise words (by column)

- `characteristics_ch1.3.treatment`: Hindlimb suspension (HS)

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| characteristics_ch1.5.day of_differentiation (without characteristics_ch1.4.day of_hs) + suffix of title | characteristics_ch1.4.day of_hs | 4 | 12/12 | 4 | 0 |
| diff (without characteristics_ch1.4.day of_hs) + suffix of title | characteristics_ch1.4.day of_hs | 4 | 12/12 | 4 | 0 |
| characteristics_ch1.5.day of_differentiation (without characteristics_ch1.4.day of_hs) + suffix of source_name_ch1 | characteristics_ch1.4.day of_hs | 4 | 12/12 | 4 | 0 |
| diff (without characteristics_ch1.4.day of_hs) + suffix of source_name_ch1 | characteristics_ch1.4.day of_hs | 4 | 12/12 | 4 | 0 |
| characteristics_ch1.4.day of_hs (without characteristics_ch1.5.day of_differentiation) + suffix of title | characteristics_ch1.5.day of_differentiation | 6 | 12/12 | 6 | 0 |
| grp (without characteristics_ch1.5.day of_differentiation) + suffix of title | characteristics_ch1.5.day of_differentiation | 6 | 12/12 | 6 | 0 |
| characteristics_ch1.4.day of_hs (without characteristics_ch1.5.day of_differentiation) + suffix of source_name_ch1 | characteristics_ch1.5.day of_differentiation | 6 | 12/12 | 6 | 0 |
| grp (without characteristics_ch1.5.day of_differentiation) + suffix of source_name_ch1 | characteristics_ch1.5.day of_differentiation | 6 | 12/12 | 6 | 0 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "characteristics_ch1.5.day of_differentiation (without characteristics_ch1.4.day of_hs) + suffix of title", "across": "_across", "within": ["_within"], "n_same_key_pairs": 12, "same_key_mean_r": -0.048, "other_mean_r": 0.048, "difference": -0.096, "permutation_p": 0.9315342328835582, "genes_used": 9182, "status": "not_supported"}
