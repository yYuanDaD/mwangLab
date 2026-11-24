# Review packet A (facts only): GSE144109

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\PMID33332990\PMID33332990_abstract.txt`

## Metadata (15 samples)

### Grouping columns (level: count)

- `characteristics_ch1.0.diet`: high-fat diet: 12; normal chow: 3
- `characteristics_ch1.1.treatment`: Sed: 9; Ex: 6
- `characteristics_ch1.2.parent`: P: 6; M: 6; MP: 3
- `characteristics_ch1.3.group`: NCS: 3; PHE: 3; PHS: 3; MHE: 3; MHS: 3
- `grp`: NCS: 3; PHE: 3; PHS: 3; MHE: 3; MHS: 3

### Constant columns

- `status`: Public on Jul 30 2021
- `submission_date`: Jan 23 2020
- `last_update_date`: Jul 30 2021
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Quadricep
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `treatment_protocol_ch1`: Study 1: Female mice (C57BL/6, 8 weeks old) were subjected to either normal chow (NC) diet (n = 4) or 60% high-fat (HF) diet (Research Diets, NJ; n = 8) for 6 weeks. For mating, a lean male mouse (C57BL/6, 14 weeks old) was placed in the cage with 2 female mice. Once confirmed pregnant (by vaginal p ... [1189 more characters]
- `growth_protocol_ch1`: 
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: Total RNA was extracted from skeletal muscle with TRIzol (Invitrogen, Madison, WI, USA) according to the manufacturer鈥檚 instructions.,RNA was checked for quality using the Bioanalyser instrument (Agilent Technologies) and subject to the Illumina TruSeq Stranded Total RNA with Ribo-Zero Gold protocol ... [95 more characters]
- `data_processing`: Reads were mapped to mm10 with STAR v2.5.2b and gene read coverages were computed with featureCounts v1.5.2 using GENCODE vM13 annotation,Differentially expressed genes were identified using DESeq2 v1.11.8 for maternal and paternal lines separately.,Genome_build: mm10,Supplementary_files_format_and_ ... [97 more characters]
- `platform_id`: GPL17021
- `contact_name`: Ali,,Altintas
- `contact_email`: altintas@sund.ku.dk
- `contact_laboratory`: Integrative Physiology
- `contact_department`: NNF Center for Basic Metabolic Research
- `contact_institute`: Copenhagen University
- `contact_address`: Blegdamsvej 3B
- `contact_city`: Copenhagen
- `contact_zip/postal_code`: 2200
- `contact_country`: Denmark
- `instrument_model`: Illumina HiSeq 2500
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE144109,GSE144112
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `relation`

### Samples

| sample | title |
|---|---|
| GSM4280407 | F1-3-1 |
| GSM4280408 | F1-3-7 |
| GSM4280409 | F1-4-5 |
| GSM4280410 | F2-1-2 |
| GSM4280411 | F2-3-7 |
| GSM4280412 | F2-4-7 |
| GSM4280413 | F3-4-8 |
| GSM4280414 | F4-1-1 |
| GSM4280415 | F5-3-4 |
| GSM4280416 | F6-1-5 |
| GSM4280417 | F6-3-4 |
| GSM4280418 | F7-1-3 |
| GSM4280419 | F7-2-1 |
| GSM4280420 | F7-2-4 |
| GSM4280421 | F7-4-4 |

## Values with exercise words (by column)

- `characteristics_ch1.1.treatment`: Ex, Sed
- `treatment_protocol_ch1`: Study 1: Female mice (C57BL/6, 8 weeks old) were subjected to either normal chow (NC) diet (n = 4) or 60% high-fat (HF) diet (Research Diets, NJ; n = 8) for 6 weeks. For mating, a lean male mouse (C57BL/6, 14 weeks old) was placed in the cage with 2 female mice. Once confirmed pregnant (by vaginal plug), the male mouse was removed and the female mice were housed individually in cages equipped with running wheels, which were locked for the sedentary groups. The groups were defined as normal chow, sedentary (NC-Sed), maternal high-fat diet, sedentary (M-HF-Sed) and maternal high-fat diet, exercise (M-HF-Ex).,Study 2: Male mice (C57BL/6, 8 weeks old) were subjected to either normal chow (NC) diet (n = 4) or 60% high-fat (HF) diet (Research Diets, NJ; n = 4) for 6 weeks. Male mice were then mated with lean female mice (C57BL/6, 14 weeks old) and once confirmed pregnant (by vaginal plug), the male mouse was removed, and the female mice were house individually with running wheels as described above. The groups were defined as normal chow, sedentary (NC-Sed), paternal high-fat diet, sedentary (P-HF-Sed) and paternal high-fat diet, exercise (P-HF-Ex).,In both studies, all groups were provided normal chow with sedentary activity from the day after birth and thereafter.  Adult offspring were humanely euthanized at 10 months of age and quadricep muscle collected. Study 1 and 2 were conducted in parallel allowing the NC-Sed group to serve as the control group for both studies.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| suffix of title | characteristics_ch1.2.parent | 7 | 5/15 | 1 | 2 |
| characteristics_ch1.1.treatment (without characteristics_ch1.2.parent) + suffix of title | characteristics_ch1.2.parent | 9 | 3/15 | 1 | 2 |
| suffix of title | characteristics_ch1.0.diet | 7 | 2/15 | 1 | 3 |
| suffix of title | characteristics_ch1.1.treatment | 7 | 2/15 | 1 | 3 |
| characteristics_ch1.0.diet (without characteristics_ch1.2.parent) + suffix of title | characteristics_ch1.2.parent | 10 | 2/15 | 0 | 2 |
| characteristics_ch1.1.treatment (without characteristics_ch1.0.diet) + suffix of title | characteristics_ch1.0.diet | 9 | 0/15 | 0 | 3 |
| characteristics_ch1.2.parent (without characteristics_ch1.0.diet) + suffix of title | characteristics_ch1.0.diet | 12 | 0/15 | 0 | 2 |
| characteristics_ch1.3.group (without characteristics_ch1.0.diet) + suffix of title | characteristics_ch1.0.diet | 13 | 0/15 | 0 | 2 |
