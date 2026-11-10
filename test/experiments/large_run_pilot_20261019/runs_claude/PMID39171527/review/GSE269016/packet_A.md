# Review packet A (facts only): GSE269016

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\paper_screen_20261019\papers\PMC11343597.paper.md`

## Paper outline

- # Postprandial exercise regulates tissue-specific triglyceride uptake through angiopoietin-like proteins
- ## Abstract  `ABS` · abstract
- ## (untitled)  `FN` · other
- ### (untitled)  `FN.1` · other
- ## Introduction  `S1` · introduction
- ## Results  `S2` · results
- ### Exercise suppression of ANGPTL3 tissue binding increases LPL activity and promotes TG uptake in energy-consumption tissues in the postprandial stage.  `S2.1` · results
- ### ANGPTL8 mediates exercise suppression of ANGPTL3 tissue binding.  `S2.2` · results
- ### Exercise suppresses Angptl8 expression through the hepatic insulin/mTOR/CEBPα signaling pathway.  `S2.3` · results
- ### Increased ANGPTL4 counteracts the decreased ANGPTL3 for LPL inhibition in response to exercise in WATs.  `S2.4` · results
- ## Discussion  `S3` · discussion
- ## Methods  `S4` · methods
- ### Sex as a biological variable.  `S4.1` · methods
- ### Materials.  `S4.2` · methods
- ### Animals.  `S4.3` · methods
- ### Exercise in humans.  `S4.4` · methods
- ### Tissue LPL activity.  `S4.5` · methods
- ### TG-^3H-palmitate tissue uptake.  `S4.6` · methods
- ### [^14C]Deoxyglucose uptake.  `S4.7` · methods
- ### Echocardiography.  `S4.8` · methods
- ### Blood chemistry.  `S4.9` · methods
- ### Cell culture and virus production.  `S4.10` · methods
- ### Immunoblot.  `S4.11` · methods
- ### Real-Time PCR.  `S4.12` · methods
- ### Angptl8 transcription analysis.  `S4.13` · methods
- ### Statistics.  `S4.14` · methods
- ### Study approval.  `S4.15` · methods
- ### Data availability.  `S4.16` · data_availability
- ## Author contributions  `S5` · other
- ## Supplementary Material  `S6` · supplementary
- ## Acknowledgments  `S7` · other
- ## (untitled)  `S8` · other
- ### 08/22/2024  `S8.1` · other
- ## Contributor Information  `S10` · other
- ## Accession mentions

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.2.treatment`: Sedentary: 6; Exercise: 6
- `treatment`: Sedentary: 6; Exercise: 6
- `grp`: SED: 6; EX: 6

### Constant columns

- `status`: Public on Aug 08 2024
- `submission_date`: Jun 04 2024
- `last_update_date`: Aug 08 2024
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Liver
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Liver
- `characteristics_ch1.1.genotype`: WT
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted from tissues or cells with TRI Reagent (Sigma-Aldrich).1ug of total RNA was used for construction of sequencing libraries.,RNA libraries for RNA-seq were prepared using BGI Optimal Dual-mode mRNA-Seq Library Prep Kit following manufactuer's protocols.
- `data_processing`: ThesequencingdatawasfilteredwithSOAPnuke( v 1.6.5)by(1)Removingreadscontainingsequencingadapter;(2)Removingreadswhoselow-qualitybaseratio(basequalitylessthanorequalto15)ismorethan20%;(3)Removingreadswhoseunknownbase(&apos;N&apos;base)ratioismorethan5%,afterwardscleanreadswereobtainedandstoredinFASTQ ... [416 more characters]
- `platform_id`: GPL30215
- `contact_name`: Yan,,Wang
- `contact_email`: Wang.y@whu.edu.cn
- `contact_institute`: College of Life Sciences, Wuhan University
- `contact_address`: Luojiashan, wuchang, wuhan
- `contact_city`: Wuhan
- `contact_state`: China
- `contact_zip/postal_code`: 430072
- `contact_country`: China
- `instrument_model`: MGISEQ-2000RS
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE269016
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`, `key`

### Samples

| sample | title |
|---|---|
| GSM8305114 | Liver, Sedentary 1(S1) |
| GSM8305115 | Liver, Sedentary 2(S2) |
| GSM8305116 | Liver, Sedentary 3(S3) |
| GSM8305117 | Liver, Sedentary 4(S4) |
| GSM8305118 | Liver, Sedentary 5(S5) |
| GSM8305119 | Liver, Sedentary 6(S6) |
| GSM8305120 | Liver, Exercise 1(E1) |
| GSM8305121 | Liver, Exercise 2(E2) |
| GSM8305122 | Liver, Exercise 3(E3) |
| GSM8305123 | Liver, Exercise 4(E4) |
| GSM8305124 | Liver, Exercise 5(E5) |
| GSM8305125 | Liver, Exercise 6(E6) |

## Values with exercise words (by column)

- `title`: Liver, Exercise 1(E1), Liver, Exercise 2(E2), Liver, Exercise 3(E3), Liver, Exercise 4(E4), Liver, Exercise 5(E5), Liver, Exercise 6(E6), Liver, Sedentary 1(S1), Liver, Sedentary 2(S2), Liver, Sedentary 3(S3), Liver, Sedentary 4(S4), Liver, Sedentary 5(S5), Liver, Sedentary 6(S6)
- `characteristics_ch1.2.treatment`: Exercise, Sedentary
- `treatment`: Exercise, Sedentary
- `grp`: EX, SED

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of key | characteristics_ch1.2.treatment | 12 | 0/12 | 0 | 0 |
| grp (without characteristics_ch1.2.treatment) + suffix of key | characteristics_ch1.2.treatment | 12 | 0/12 | 0 | 0 |
| suffix of key | treatment | 12 | 0/12 | 0 | 0 |
| grp (without treatment) + suffix of key | treatment | 12 | 0/12 | 0 | 0 |
| suffix of key | grp | 12 | 0/12 | 0 | 0 |
| characteristics_ch1.2.treatment (without grp) + suffix of key | grp | 12 | 0/12 | 0 | 0 |
| treatment (without grp) + suffix of key | grp | 12 | 0/12 | 0 | 0 |
