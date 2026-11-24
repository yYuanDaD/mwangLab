# Review packet B (the analysis' decisions): GSE221003_chronic

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 6, "samples_linked": 17, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: chronic hearts are Ctrl/Doxo/Doxo-NMN only (S2.2.p4); exercise was a treadmill test outcome on non-sequenced cohort-2 (S2.5.p1).
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE221003"], "assay": "bulk RNA-seq of mouse heart, chronic regimen (day 60)", "primary_estimand": "Effect of chronic doxorubicin vs PBS, and of oral NMN on top of doxorubicin, on heart gene expression. No exercise intervention (treadmill only a test on cohort-2, S2.5.p1; RNA-seq on cohort-3, S2.2.p4).", "sample_inclusion": "5-6 hearts per group of cohort-3 (S2.2.p4)", "factors": {"treatment": ["Ctrl (PBS)", "Doxo", "Doxo-NMN"]}, "planned_contrasts": ["Chronic Doxo vs Ctrl (S3.6.p1; paper: 9 DEGs)", "Chronic Doxo-NMN vs Doxo (S3.6.p1; paper: 0 DEGs)"], "repeated_measure_unit": "none", "paper_method": "edgeR TMM + QL F-test (S2.9.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.6.p1"}, "exercise_arm": "none"}

reasoning: S2.2.p3-p4, S3.6.p1: chronic Ctrl/Doxo/Doxo-NMN hearts, n=5-6. Exercise capacity was measured (S3.7.p1) on a different cohort and is not a sample factor.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE221003\\GSE221003_Chronic_Doxo_Heart.csv.gz", "owned": true, "checks": ["S11.p1 names GSE221003", "17 chronic heart samples (5/6/6) match 5-6 per group of cohort-3 (S2.2.p4)"], "accession": "GSE221003", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE221003\\GSE221003_metadata.csv"}

reasoning: Chronic matrix matches the GEO chronic-study GSMs.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 17, "n_metadata": 57, "coverage": 0.2982, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM6837011", "GSM6837012", "GSM6837013", "GSM6837014", "GSM6837015", "GSM6837016", "GSM6837017", "GSM6837018", "GSM6837019", "GSM6837020", "GSM6837021", "GSM6837022", "GSM6837023", "GSM6837024", "GSM6837025", "GSM6837026", "GSM6837027", "GSM6837028", "GSM6837029", "GSM6837030", "GSM6837031", "GSM6837032", "GSM6837033", "GSM6837034", "GSM6837035", "GSM6837036", "GSM6837037", "GSM6837038", "GSM6837039", "GSM6837040", "GSM6837041", "GSM6837042", "GSM6837043", "GSM6837044", "GSM6837045", "GSM6837046", "GSM6837047", "GSM6837048", "GSM6837049", "GSM6837050"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36611902\\GSE221003_chronic\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.2.treatment"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36611902\\GSE221003_chronic\\aligned\\design_metadata.csv", "sha256": "eae1c02a601cf57f739ea25dd37e3548c7a185608951c8925a1204c1b8e395f8", "levels": {"grp": {"Doxo": 6, "Doxo beta-NMN (500 mg/kg)": 6, "Vehicle": 5}}}}

reasoning: Matrix columns such as CTRL.17.Heart equal the GEO description suffix CTRL-17-Heart up to separators; normalize_keys matches ignoring -/. Key = text after the last comma in description, with an acute 'Heart_' prefix stripped (acute -> heart number, chronic -> CTRL-17-Heart style); one regex covers all 57 GSMs.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "source": "GSE221003_Chronic_Doxo_Heart.csv.gz", "paper_input": "featureCounts count table (S2.9.p1)", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36611902\\GSE221003_chronic\\aligned\\aligned_matrix.csv", "sha256": "5520add49a39cec7426d302484607e9271d18f4d1fe0f2405cd09cc3296db1d7", "n_features": 54658, "n_samples": 17, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1987433.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0; featureCounts per GEO data_processing.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_arm": "absent", "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36611902\\GSE221003_chronic\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: No exercise factor among the sequenced samples.

rejected alternatives: [{"value": "grp Doxo vs Vehicle", "reason_rejected": "drug contrast, not exercise"}, {"value": "grp Doxo-NMN vs Doxo", "reason_rejected": "NMN contrast, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 17 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise",
    "paper": "treadmill test outcome on cohort-2 only (S2.5.p1)",
    "data": "no exercise factor",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID36611902 / GSE221003

**Status: refused at `design` (both cases).** No exercise contrast exists in the sequenced samples.

## What ran
- `case_runner inspect GSE221003` (cached in `data/GSE221003`): two featureCounts integer count matrices — `Acute_Doxo_Heart.csv.gz` (25,416 genes × 40) and `Chronic_Doxo_Heart.csv.gz` (54,658 × 17). There are 57 GSMs, and the only grouping column is `treatment` (Vehicle / Doxo / Doxo beta-NMN 180 or 500 mg/kg).
- `case_runner execute case_spec.json` with two cases, `GSE221003_acute` and `GSE221003_chronic`. The gates `paper_reconstruction`, `ownership`, `alignment` and `matrix` were recorded as valid. `design` was refused. The validator reported 10 records and 0 errors.
  - Acute alignment: an exact match on a key taken from the GEO `description` (`,Heart_<n>`) against the matrix columns `X<n>_counts`. It aligned 40/40 samples (14 Vehicle, 13 Doxo, 13 Doxo-NMN).
  - Chronic alignment: a normalised-key match (`CTRL-17-Heart` = `CTRL.17.Heart`). It aligned 17/17 samples (5 / 6 / 6).
  - Matrix: raw counts in both cases (all values are integers, and GEO `data_processing` says STAR + featureCounts). The paper also used counts with edgeR.

## Why it was refused
The paper is about doxorubicin cardiotoxicity and NMN protection. The heart RNA-seq groups are Ctrl, Doxo and Doxo-NMN only: acute cohort-1 (S2.2.p2) and chronic cohort-3 (S2.2.p4). Exercise appears only as a treadmill exhaustion **test**, used as a functional outcome in chronic cohort-2 (S2.5.p1, S3.7.p1). That cohort was not sequenced, and no group was given exercise or training as an intervention. So an effect of exercise on gene expression cannot be identified from these data. I rejected the drug contrasts (Doxo vs Ctrl, Doxo-NMN vs Doxo) as alternatives, because they do not answer the exercise question.

## DEG counts vs paper
None computed (refused). For reference, the paper reports:
- Acute (padj < 0.05 and FC 1.5, i.e. |log2FC| > 0.5849625; S3.3.p1): Doxo vs Ctrl 3874, Doxo-NMN vs Doxo 2207.
- Chronic (padj < 0.05, no fold-change rule; S3.6.p1): Doxo vs Ctrl 9, Doxo-NMN vs Doxo 0.
- Method in the paper: edgeR TMM with the QL F-test (S2.9.p1).

## Deviations
None. The case stopped before the method gate.

## Tool problems
1. `alignment.key_patterns` requires the regex to match **every** metadata row (`tools/native.py:392`, `derive_columns`). This holds even when the matrix covers only one of the two sub-studies deposited in the GSE. I first had to ... [849 more characters]
