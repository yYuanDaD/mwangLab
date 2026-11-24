# Review packet A (facts only): GSE205907

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261027\papers\PMC9260255.paper.md`

## Paper outline

- # Transcriptional Profiling Reveals Brain Region-Specific Gene Networks Regulated in Exercise in a Mouse Model of Parkinson’s Disease
- ## Abstract  `ABS` · abstract
- ## Introduction  `S1` · introduction
- ## Materials and Methods  `S2` · methods
- ### Animals  `S2.1` · methods
- ### Chronic Mouse Model of Parkinson’s Disease  `S2.2` · methods
- ### Treadmill Exercise Protocol  `S2.3` · methods
- ### Motor Behavior Analysis  `S2.4` · methods
- ### Brain Tissue Preparation  `S2.5` · methods
- ### RNA Isolation  `S2.6` · methods
- ### Transcriptome Analysis  `S2.7` · methods
- ### Immunofluorescence  `S2.8` · methods
- ### Statistical Analysis  `S2.9` · methods
- ## Results  `S3` · results
- ### Treadmill Exercise Improves Motor Dysfunction in Parkinson’s Disease Model  `S3.1` · results
- ### DEG Analysis Reveals Brain-Region-and Exercise-Specific Response Transcriptional Profiles in Parkinson’s Disease Mice  `S3.2` · results
- ### Remarkable Different Genes in SN and Striatum Regions Affected by Exercise for Parkinson’s Disease Mice  `S3.3` · results
- ### WGCNA Identify Specific Transcriptional Signatures Associated With Exercise Rehabilitation in Parkinson’s Disease Model  `S3.4` · results
- ### Exercise Increased TH^+ Fibers and Synapses Obviously in the Striatal Region but Failed to Increase DA Neurons in the SN of Parkinson’s Disease Model  `S3.5` · results
- ## Discussion  `S4` · discussion
- ## Conclusion  `S5` · conclusion
- ## Data Availability Statement  `S6` · data_availability
- ## Ethics Statement  `S7` · other
- ## Author Contributions  `S8` · other
- ## Conflict of Interest  `S9` · other
- ## Publisher’s Note  `S10` · other
- ## Funding  `BK1` · other
- ## Supplementary Material  `BK2` · supplementary
- ## Accession mentions

## Metadata (48 samples)

### Grouping columns (level: count)

- `grp`: EX: 16; MPTP: 16; SAL: 16
- `animal`: E26: 4; E27: 4; E28: 4; E29: 4; M16: 4; M21: 4; M23: 4; M6: 4; S1: 4; S2: 4; S3: 4; S4: 4
- `tissue`: Cereb: 12; Cortex: 12; Nigra: 12; Stria: 12

### Constant columns


### Per-sample columns



### Samples

| sample |  |
|---|
| E26Cereb |  |
| E26Corte |  |
| E26Nigra |  |
| E26Stria |  |
| E27Cereb |  |
| E27Corte |  |
| E27Nigra |  |
| E27Stria |  |
| E28Cereb |  |
| E28Corte |  |
| E28Nigra |  |
| E28Stria |  |
| E29Cereb |  |
| E29Corte |  |
| E29Nigra |  |
| E29Stria |  |
| M16Cereb |  |
| M16Corte |  |
| M16Nigra |  |
| M16Stria |  |
| M21Cereb |  |
| M21Corte |  |
| M21Nigra |  |
| M21Stria |  |
| M23Cereb |  |
| M23Corte |  |
| M23Nigra |  |
| M23Stria |  |
| M6Cereb |  |
| M6Corte |  |
| M6Nigra |  |
| M6Stria |  |
| S1Cereb |  |
| S1Cortex |  |
| S1Nigra |  |
| S1Stria |  |
| S2Cereb |  |
| S2Cortex |  |
| S2Nigra |  |
| S2Stria |  |
| S3Cereb |  |
| S3Cortex |  |
| S3Nigra |  |
| S3Stria |  |
| S4Cereb |  |
| S4Cortex |  |
| S4Nigra |  |
| S4Stria |  |

## Values with exercise words (by column)

- `grp`: EX

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| animal | tissue | 12 | 48/48 | 12 | 0 |
| animal | grp | 12 | 0/48 | 0 | 12 |

Expression check of the best candidate (residual correlation of same-key pairs, tools/pairing_check.py): {"key": "animal", "across": "_across", "within": [], "n_same_key_pairs": 72, "same_key_mean_r": 0.12, "other_mean_r": -0.011, "difference": 0.131, "permutation_p": 0.0004997501249375312, "genes_used": 11216, "status": "supported"}
