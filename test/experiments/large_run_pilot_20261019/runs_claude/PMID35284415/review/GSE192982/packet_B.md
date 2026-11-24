# Review packet B (the analysis' decisions): GSE192982

## Mechanical flags

- **unused_subject_like_column**: {"column": "donor", "n_values": 8, "max_repeat": 3, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "characteristics_ch1.1.age", "n_values": 8, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "characteristics_ch1.1.age", "across": "characteristics_ch1.2.mechanical condition", "pairs_or_sets": 8, "samples_linked": 24, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the only interventions are in vitro mechanical loading (cyclic hydrostatic pressure in a bioreactor) and unloading (simulated microgravity) of cell-seeded scaffolds versus static culture. No organism exercised, so an exercise effect on gene expression is not identifiable from these data. The data would support CHP/SMG vs Static (donor-blocked limma), but that estimand is bioreactor mechanical stimulation, not exercise.

## Samples per design level

### `cond`
- **CHP** (8): GSM5770126 / ScACS-1-3B_S20; GSM5770129 / ScACS-2-3B_S23; GSM5770132 / ScACS-3-3B_S3; GSM5770135 / ScACS-4-3B_S6; GSM5770138 / ScACS-5-3B_S9; GSM5770141 / ScACS-6-3B_S12; GSM5770144 / ScACS-7-3_S43; GSM5770147 / ScACS-8-3_S46
- **SMG** (8): GSM5770125 / ScACS-1-2B_S19; GSM5770128 / ScACS-2-2B_S22; GSM5770131 / ScACS-3-2B_S2; GSM5770134 / ScACS-4-2B_S5; GSM5770137 / ScACS-5-2B_S8; GSM5770140 / ScACS-6-2B_S11; GSM5770143 / ScACS-7-2_S42; GSM5770146 / ScACS-8-2_S45
- **Static** (8): GSM5770124 / ScACS-1-1B_S18; GSM5770127 / ScACS-2-1B_S21; GSM5770130 / ScACS-3-1B_S24; GSM5770133 / ScACS-4-1B_S4; GSM5770136 / ScACS-5-1B_S7; GSM5770139 / ScACS-6-1B_S10; GSM5770142 / ScACS-7-1_S41; GSM5770145 / ScACS-8-1_S44

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE192982"], "assay": "bulk RNA-seq (Illumina NextSeq 500, PE 42bp) of tissue-engineered meniscus constructs made from human meniscus fibrochondrocytes (S2.6.p1)", "system": "in vitro: MFCs from 8 non-OA partial-meniscectomy donors (4F/4M) seeded on collagen I scaffolds, 2 wk static preculture, then 3 wk of Static, SMG (rotating-wall bioreactor) or CHP (0.9 MPa, 1 Hz, 1 h/day) (S2.2.p2, S2.3.p1)", "factors": {"mechanical_condition": ["Static", "SMG", "CHP"], "sex": ["F", "M"], "donor": "8 donors, each exposed to all 3 conditions (S3.1.p1)"}, "sample_inclusion": "24 libraries = 8 donors x 3 conditions; replicate constructs pooled per donor/condition before sequencing (GEO extract_protocol)", "primary_estimand": "Effect of in vitro mechanical loading (CHP) and unloading (SMG) versus static culture on the transcriptome of engineered meniscus constructs, all donors and within each sex (S1.p6, S3.2.p1, S3.4.p1). No exercise of any organism is studied.", "planned_contrasts": ["CHP vs Static, all donors (S3.2.p1; paper: 236 DEGs)", "SMG vs Static, all donors (S3.2.p1; paper: 388 DEGs)", "CHP vs Static and SMG vs Static within female and within male donors (S3.4.p1, Fig 5A; counts only in figure)"], "repeated_measure_unit": "donor (random effect within sex; S2.7.p1)", "normalization": "Partek: max-count<50 filter, add 1, TMM, log2 (S2.7.p1)", "paper_method": "Partek Flow ANOVA with sex and treatment, donor as random within sex (S2.7.p1)", "paper_threshold": {"metric" ... [210 more characters]

reasoning: The paper (S1.p6, ABS.p1) studies mechanical loading via cyclic hydrostatic pressure and unloading via simulated microgravity applied to cell-seeded scaffolds in a bioreactor, as an in vitro OA/sex-difference model. There is no exercise intervention, no exercising organism, and no training/sedentary arm.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35284415\\GSE192982_log2TMM_genes_x_samples.csv", "owned": true, "checks": ["S7.p1 names GSE192982", "24 GEO samples = 8 donors x 3 conditions as in S3.1.p1", "13,361 genes in deposited matrix = 13,361 in S3.1.p1", "Partek/STAR/RefSeq processing in data_processing matches S2.7.p1"], "accession": "GSE192982", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE192982\\GSE192982_metadata.csv"}

reasoning: Data availability statement S7.p1 names GSE192982; gene count and design match the paper exactly.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35284415\\GSE192982\\aligned\\aligned_metadata.csv", "columns": {"cond": {"alias_of": "characteristics_ch1.2.mechanical condition"}, "sex": {"alias_of": "characteristics_ch1.0.Sex"}, "donor": {"source": "title", "regex": "^ScACS-(\\d)-"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35284415\\GSE192982\\aligned\\design_metadata.csv", "sha256": "cebf58808aeec36b26023ce7441b73ea7d38d643d974696470f46770045a6a1d", "levels": {"cond": {"Static": 8, "SMG": 8, "CHP": 8}, "sex": {"F": 12, "M": 12}, "donor": {"1": 3, "2": 3, "3": 3, "4": 3, "5": 3, "6": 3, "7": 3, "8": 3}}}}

reasoning: Matrix sample names (after transposing the deposited samples-by-genes file) equal GEO titles exactly. Donor number is the first digit group of the title (ScACS-<donor>-<condition>); condition and sex come from GEO characteristics, which agree with the deposited annotation columns.

### matrix (valid, not_started)

final: {"matrix_type": "log2(TMM-normalized count + 1) from Partek, low-count filtered", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35284415\\GSE192982\\aligned\\aligned_matrix.csv", "sha256": "21822b35e5ba1354eedebf63dca349544ed335c90c5e67e78ab3cf89c7e11756", "n_features": 13361, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 13318, "negative_fraction": 0.041533, "min": -4.63026, "max": 16.5824, "median": 4.23965, "integer_fraction": 0.0, "candidates": ["signed_log_scale (log ratios, M-values, or centered data)"]}}

reasoning: Non-integer values, range -4.6..16.6, median 4.2; data_processing and S2.7.p1 state add 1, TMM, log2. Same input as the paper's Partek ANOVA. Not raw counts, so DESeq2/edgeR do not apply.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "cond", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35284415\\GSE192982\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: The request is an exercise effect as the paper intends. The paper intends mechanical loading/unloading of engineered meniscus in vitro (ABS.p1, S1.p6, S2.3.p1); none of its factors is exercise. Design is therefore refused; groups would be analyzable (8 donors x 3 conditions, n=8 per arm) if mechanical stimulation itself were requested.

rejected alternatives: [{"value": "cond CHP vs Static (donor-blocked) as an exercise surrogate", "reason_rejected": "CHP is 0.9 MPa hydrostatic pressure applied 1 h/day to engineered tissue in vitro (S2.3.p1); the paper frames it as mechanical loading for an OA model (S1.p6), not exercise. Labelling it an exercise effect would misstate the estimand."}, {"value": "cond SMG vs Static", "reason_rejected": "Mechanical unloading (simulated microgravity), not exercise."}, {"value": "sex F vs M", "reason_rejected": "Donor se ... [29 more characters]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix orientation",
    "paper": "n/a",
    "data": "deposited file is samples x genes with 4 annotation columns",
    "disposition": "executable_without_change (transposed by prep_transpose.py, values unchanged)"
  },
  {
    "item": "estimand vs request",
    "paper": "in vitro mechanical loading/unloading (CHP, SMG) vs static",
    "data": "same",
    "disposition": "blocking: request is an exercise effect; no exercise arm exists"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID35284415 / GSE192982

**Status: refused at `design`. No exercise contrast exists.**

## What ran
- `python -m tools.case_runner inspect GSE192982` (cached data). One processed matrix: `GSE192982_ACS_CHP_ProcessedData_NormalizedCount.txt.gz`. It is deposited as samples x genes (24 x 13,361) with 4 annotation columns.
- `prep_transpose.py` removes the annotation columns and transposes the matrix to genes x samples. Values are unchanged. Output: `GSE192982_log2TMM_genes_x_samples.csv`.
- `python -m tools.case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment, matrix, design (refused). Contract validator: 5 records, 0 errors. Suitability report: `analyzable`, 3/3 comparisons.

## Decisions
- **Ownership:** S7.p1 names GSE192982. The matrix has 13,361 genes, the same number as S3.1.p1. It has 24 libraries (8 donors x 3 conditions). Processing is Partek STAR/E-M/TMM/log2, as in S2.7.p1.
- **Alignment:** exact match on `title`, 24/24 samples. `donor` is parsed from the title. `cond` and `sex` come from the GEO characteristics.
- **Matrix:** log2(TMM+1) from Partek with low counts filtered. This is non-integer, log-scale data, so the valid route is limma, not DESeq2.
- **Design: refused.** The paper's interventions are all in vitro:
  - cyclic hydrostatic pressure (CHP: 0.9 MPa, 1 Hz, 1 h/day for 3 weeks in a bioreactor);
  - simulated microgravity (SMG) unloading;
  - static culture as control.

  These are applied to engineered meniscus constructs grown from fibrochondrocytes (S2.3.p1). The paper frames them as mechanical loading/unloading for an osteoarthritis and sex-difference model (S1.p6). No organism exercises, so an exercise effect is not identifiable. I rejected treating CHP as an exercise surrogate; the reason is recorded in `candidates`.

## DEG counts vs paper
- None computed, because the case was refused.
- Paper threshold: fold change > 2 (|log2FC| > 1) and q < 0.05 (S3.2.p1).
- Paper counts: CHP vs Static 236 DEGs, SMG vs Static 388 DEGs, 52 shared. Per-sex counts appear only in Fig 5A.

## Deviations
- None executed.
- If mechanical loading itself is wanted, the data could answer it: limma on the deposited log2-TMM matrix with `~ cond` and donor blocking, n = 8 per arm. The paper's method was a Partek ANOVA with donor as a random effect within sex (S2.7.p1).

## Tool problems
- Inspect reports a transposed matrix without flagging it. It reads the deposited file as 24 "features" x 13,36 ... [522 more characters]
