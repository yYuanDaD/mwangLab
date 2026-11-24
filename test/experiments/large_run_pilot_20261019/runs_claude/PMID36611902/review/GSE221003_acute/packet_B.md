# Review packet B (the analysis' decisions): GSE221003_acute

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 13, "samples_linked": 39, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the sequenced hearts are Ctrl (vehicle), Doxo and Doxo-NMN only (S2.2.p2, S3.3.p1). Exercise appears only as a treadmill exhaustion test outcome in a non-sequenced chronic cohort (S2.5.p1, S3.7.p1). An exercise effect on gene expression is not identifiable from these data.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE221003"], "assay": "bulk RNA-seq (poly(A), NovaSeq 6000, STAR + featureCounts) of mouse heart", "primary_estimand": "Effect of doxorubicin vs vehicle, and of NMN on top of doxorubicin, on heart gene expression (acute regimen, D5). No exercise intervention: the only exercise-related measure is a treadmill exhaustion TEST (S2.5.p1, S3.7.p1) used as a phenotypic outcome in chronic cohort-2; RNA-seq hearts come from acute cohort-1 and chronic cohort-3 (S2.2.p2, S2.2.p4).", "sample_inclusion": "Acute: 13-14 hearts per group of cohort-1 (S2.2.p2)", "factors": {"treatment": ["Ctrl (vehicle)", "Doxo", "Doxo-NMN"]}, "planned_contrasts": ["Acute Doxo vs Ctrl (S3.3.p1; paper: 3874 DEGs)", "Acute Doxo-NMN vs Doxo (S3.3.p1; paper: 2207 DEGs)"], "repeated_measure_unit": "none (one heart per mouse)", "paper_method": "edgeR 3.32.1, TMM, estimateDisp, glmQLFit + QL F-test (S2.9.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "source_locator": "S3.3.p1"}, "exercise_arm": "none"}

reasoning: S2.2.p1-p4 and S2.9.p1 define the RNA-seq design: heart tissue from Ctrl, Doxo, Doxo-NMN mice in an acute (cohort-1) and a chronic (cohort-3) study. Exercise appears only as a treadmill exhaustion test outcome (S2.5.p1, S3.7.p1) on chronic cohort-2, which has no RNA-seq. No group trains or exercises as an intervention. Acute threshold: adjusted p < 0.05 and FC 1.5 (S3.3.p1).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE221003\\GSE221003_Acute_Doxo_Heart.csv.gz", "owned": true, "checks": ["S11.p1 names GSE221003", "GEO titles: acute study mouse heart control/doxo/doxo+NMN; 14/13/13 samples match 13-14 per group (S2.2.p2)", "data_processing: STAR + featureCounts count table Acute_Doxo_Heart.csv"], "accession": "GSE221003", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE221003\\GSE221003_metadata.csv"}

reasoning: Data availability S11.p1 cites GSE221003; acute matrix holds 40 heart samples matching acute cohort-1 RNA-seq.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 40, "n_metadata": 57, "coverage": 0.7018, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM6837051", "GSM6837052", "GSM6837053", "GSM6837054", "GSM6837055", "GSM6837056", "GSM6837057", "GSM6837058", "GSM6837059", "GSM6837060", "GSM6837061", "GSM6837062", "GSM6837063", "GSM6837064", "GSM6837065", "GSM6837066", "GSM6837067"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36611902\\GSE221003_acute\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.2.treatment"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36611902\\GSE221003_acute\\aligned\\design_metadata.csv", "sha256": "1229eff64744484b658b9127554189150abcf9c04ba05b2b16f378c72d33a575", "levels": {"grp": {"Vehicle": 14, "Doxo": 13, "Doxo beta-NMN (180 mg/kg)": 13}}}}

reasoning: Matrix columns X<n>_counts carry the heart number that the GEO description stores as ',Heart_<n>'; exact match on that number. Chronic-study GSMs are absent from this matrix and stay unmatched. Key = text after the last comma in description, with an acute 'Heart_' prefix stripped (acute -> heart number, chronic -> CTRL-17-Heart style); one regex covers all 57 GSMs.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "source": "GSE221003_Acute_Doxo_Heart.csv.gz", "paper_input": "featureCounts count table (S2.9.p1)", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36611902\\GSE221003_acute\\aligned\\aligned_matrix.csv", "sha256": "64d14aebce52d999cc6e996035aa06229053c865b158958377622082269cbc49", "n_features": 25416, "n_samples": 40, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4183184.0, "median": 26.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 4.2e6; GEO data_processing: featureCounts count table; paper used edgeR on counts (S2.9.p1).

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_arm": "absent", "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36611902\\GSE221003_acute\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: The request asks for an exercise effect. No sample group differs by exercise or training; treatment levels are Vehicle/Doxo/Doxo-NMN only. Running a drug contrast would not answer the question.

rejected alternatives: [{"value": "grp Doxo vs Vehicle", "reason_rejected": "drug-toxicity contrast, not exercise"}, {"value": "grp Doxo-NMN vs Doxo", "reason_rejected": "NMN supplementation contrast, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 40 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise",
    "paper": "treadmill exhaustion test as a functional outcome in chronic cohort-2 (S2.5.p1)",
    "data": "no exercise factor in GEO; RNA-seq from acute cohort-1 and chronic cohort-3",
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
