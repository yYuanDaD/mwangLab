# Review packet A (facts only): GSE269698_aged_vehicle

Answer the blind questions from this file and the paper before opening packet B.

Paper: `E:\agent\mwangLab_pdf\test\experiments\large_run_pilot_20261019\runs_claude\PMID38314723\paper\PMID38314723_abstract.txt`

## Metadata (12 samples)

### Grouping columns (level: count)

- `characteristics_ch1.1.contractions protocol`: Non-Stim: 6; Stim: 6
- `subject`: m1: 2; m2: 2; m3: 2; m4: 2; m5: 2; m6: 2
- `stim`: N: 6; S: 6

### Constant columns

- `status`: Public on Oct 28 2024
- `submission_date`: Jun 12 2024
- `last_update_date`: Oct 28 2024
- `type`: SRA
- `channel_count`: 1
- `source_name_ch1`: Skeletal muscle (Tibialis anterior)
- `organism_ch1`: Mus musculus
- `taxid_ch1`: 10090
- `characteristics_ch1.0.tissue`: Skeletal muscle (Tibialis anterior)
- `characteristics_ch1.2.age`: Aged
- `characteristics_ch1.3.genotype`: WT
- `characteristics_ch1.4.treatment`: Vehicle
- `treatment_protocol_ch1`: At the start of the mouse light cycle, 4-mo-old male mice (Charles River; Young) and 24-25-mo-old male mice (NIA; Aged) were randomized to receive an intraperitoneal (IP) injection of dexamethasone at 2 mg/kg diluted in saline or an IP injection of saline only as a control. The mice were given 2 h r ... [1182 more characters]
- `growth_protocol_ch1`: Male C57BL/6 mice were housed in a temperature- (25鈩) and light- (12 h light/12 h dark) controlled environment within the vivarium at Florida State University and were provided standard 5001 rodent chow (LabDiet, St. Louis, MO) and water ad libitum until the day of testing. Animals were euthanized b ... [53 more characters]
- `molecule_ch1`: total RNA
- `extract_protocol_ch1`: RNA was isolated using Zymo RNA Miniprep kit with on-column Dnase treatment. 300 micrograms of total RNA was used for construction of sequencing libraries.,A cDNA library was prepared for each sample using the the NEBNext PolyA mRNA and Ultra II Directional RNA library kit for Illumina. Libraries we ... [583 more characters]
- `data_processing`: Adapters were trimmed during demultiplexing by the core facility and trimmed reads were aligned to the genome using STAR version 2.7.10a for alignment to the mouse genome (GRCm39) and to generate count tables using default settings.,Differential expression analysis of count tables was performed usin ... [229 more characters]
- `platform_id`: GPL24247
- `contact_name`: Cynthia,,Vied
- `contact_email`: cynthia.vied@med.fsu.edu
- `contact_department`: Translational Science Laboratory
- `contact_institute`: Florida State University
- `contact_address`: 1115 W. Call St
- `contact_city`: Tallahassee
- `contact_state`: Florida
- `contact_zip/postal_code`: 32306
- `contact_country`: USA
- `instrument_model`: Illumina NovaSeq 6000
- `library_selection`: cDNA
- `library_source`: transcriptomic
- `library_strategy`: RNA-Seq
- `supplementary_file_1`: NONE
- `series_id`: GSE269698
- `data_row_count`: 0

### Per-sample columns

`title`, `geo_accession`, `description`, `relation`

### Samples

| sample | title | description |
|---|---|---|
| GSM8324955 | Non-Stim TA, Aged Vehicle, 1 | OVN1 |
| GSM8324956 | Non-Stim TA, Aged Vehicle, 2 | OVN2 |
| GSM8324957 | Non-Stim TA, Aged Vehicle, 3 | OVN3 |
| GSM8324958 | Non-Stim TA, Aged Vehicle, 4 | OVN4 |
| GSM8324959 | Non-Stim TA, Aged Vehicle, 5 | OVN5 |
| GSM8324960 | Non-Stim TA, Aged Vehicle, 6 | OVN6 |
| GSM8324961 | Stim TA, Aged Vehicle, 1 | OVS1 |
| GSM8324962 | Stim TA, Aged Vehicle, 2 | OVS2 |
| GSM8324963 | Stim TA, Aged Vehicle, 3 | OVS3 |
| GSM8324964 | Stim TA, Aged Vehicle, 4 | OVS4 |
| GSM8324965 | Stim TA, Aged Vehicle, 5 | OVS5 |
| GSM8324966 | Stim TA, Aged Vehicle, 6 | OVS6 |

## Values with exercise words (by column)

- `treatment_protocol_ch1`: At the start of the mouse light cycle, 4-mo-old male mice (Charles River; Young) and 24-25-mo-old male mice (NIA; Aged) were randomized to receive an intraperitoneal (IP) injection of dexamethasone at 2 mg/kg diluted in saline or an IP injection of saline only as a control. The mice were given 2 h recovery after the injection to allow for full activation of the glucocorticoid receptor in the DEX treated group. Mice were then subjected to unilateral high force eccentric contractions by electrical stimulation of the sciatic nerve under deep isoflurane (3%) anesthesia. The left thigh was shaved, two subcutaneous bipolar electrodes straddled the sciatic nerve, and the nerve was stimulated with a ~20 mAmp current at a stimulation frequency of 100 Hz using a constant current stimulator (Model #701C, Aurora Scientific, ON, Canada). Each stimulus consisted of 300 pulses, each 1 ms in duration. The entire protocol consisted of 10 sets of 6 stimuli with each stimulus within a set separated by a 10 s rest period, and each set separated by a 60 s rest period. Following the contractions, all mice received a 500鈥壜礚 subcutaneous injection of warm saline before returning to their cages. During the recovery, all mice had access to water but not food. Four hours after completing the contractions protocol (6.5 h post-DEX or saline injection), the TA muscles were extracted under deep isoflurane (3%) anesthesia, snap-frozen in liquid nitrogen, and stored at -80掳C until analysis.

## Candidate pairing keys

A key that marks one animal/person appears at most once in each level of the `across` factor. `keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.

| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |
|---|---|---|---|---|---|
| title without the characteristics_ch1.1.contractions protocol level | characteristics_ch1.1.contractions protocol | 6 | 12/12 | 6 | 0 |
| suffix of title | characteristics_ch1.1.contractions protocol | 6 | 12/12 | 6 | 0 |
| subject (without characteristics_ch1.1.contractions protocol) + suffix of title | characteristics_ch1.1.contractions protocol | 6 | 12/12 | 6 | 0 |
| subject | characteristics_ch1.1.contractions protocol | 6 | 12/12 | 6 | 0 |
| suffix of title | stim | 6 | 12/12 | 6 | 0 |
| subject (without stim) + suffix of title | stim | 6 | 12/12 | 6 | 0 |
| subject | stim | 6 | 12/12 | 6 | 0 |
| stim (without characteristics_ch1.1.contractions protocol) + suffix of title | characteristics_ch1.1.contractions protocol | 12 | 0/12 | 0 | 0 |
