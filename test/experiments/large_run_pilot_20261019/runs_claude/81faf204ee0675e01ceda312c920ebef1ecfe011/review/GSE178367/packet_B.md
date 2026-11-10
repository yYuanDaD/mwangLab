# Review packet B (the analysis' decisions): GSE178367

## Mechanical flags

- **unused_subject_like_column**: {"column": "source_name_ch1", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "grp", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the study's only factors are ATXN3 genotype (15Q vs 84Q) and IGF-1 injection (PBS vs IGF-1 in 84Q). No sample received an exercise or training intervention and no sedentary-vs-exercise grouping exists in the paper (S4.1.p1) or GEO metadata (source_name_ch1, genotype, treatment), so the requested exercise estimand cannot be identified. Manufacturing a genotype or IGF-1 contrast as 'exercise' would change the estimand.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE178367"], "assay": "bulk RNA-seq (paired-end 150 bp, HISAT2 mm10, featureCounts) of total cerebellar RNA from 18-month-old YAC ATXN3 transgenic mice (S4.2.p1, S4.4.p1, S4.5.p2)", "factors": {"genotype": ["15Q (control)", "84Q (SCA3)"], "treatment": ["PBS (sham)", "IGF-1 50 mg/kg i.p. weekly, 9-18 months"]}, "groups": ["15Q control (n=3)", "84Q SCA3 sham (n=3)", "84Q+IGF-1 (n=3)"], "sample_inclusion": "9 cerebellar samples, 3 per group (GEO); no exclusions described", "exercise_arm": "none: no exercise, training, or physical-activity intervention anywhere in the paper; 'exercise behavior' (ABS.p1) and rotarod/locomotor tests (S1.p3) are outcome measures from a prior GH study, not an intervention", "primary_estimand": "Transcriptomic effect of SCA3 84Q genotype vs 15Q control in cerebellum, and of IGF-1 injection in 84Q mice (S1.p4, S2.2.p1); no exercise estimand", "planned_contrasts": ["84Q vs 15Q (S2.2.p1; paper: 521 DEGs, 62 up / 459 down)", "84Q+IGF-1 vs 15Q (S2.2.p1; paper: 588 DEGs, 45 up / 543 down)", "84Q+IGF-1 vs 84Q (S2.2.p1; paper: 6 DEGs, 1 up / 5 down)"], "repeated_measure_unit": "none (independent animals)", "normalization": "DESeq2 size factors; TPM for EDA and IPA (S4.5.p2, S4.6.p2)", "paper_method": "DESeq2 v1.12.3 Wald test, BH adjustment (S4.6.p2, S4.7.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "effect_inclusive": true, "source_locator": "S4.7 ... [185 more characters]

reasoning: Paper compares SCA3 84Q transgenic vs 15Q control mice and 84Q mice injected with IGF-1 (S4.1.p1, S1.p4). DE by DESeq2 Wald, BH, |log2FC| >= log2(1.5) and padj < 0.1 (S4.7.p1). No exercise arm exists; the request's exercise estimand is not part of this study.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE178367\\GSE178367_15Q_84Q_IGF1.txt.gz", "owned": true, "checks": ["DA.p1 names GSE178367", "GEO treatment_protocol matches S4.1.p1 (PBS or IGF1 50 mg/kg weekly from 9 to 18 months)", "3 groups x 3 cerebellar samples (15Q, 84Q, 84Q+IGF1) match the paper's groups", "data_processing: Trimmomatic v0.36, hisat2, mm10, featureCounts, matching S4.5.p2"], "accession": "GSE178367", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE178367\\GSE178367_metadata.csv"}

reasoning: Data availability statement and GEO protocols match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\81faf204ee0675e01ceda312c920ebef1ecfe011\\GSE178367\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "source_name_ch1", "regex": "^Cerebellar tissue - (15Q|84Q|84Q\\+IGF1)$", "recode": {"15Q": "Q15", "84Q": "Q84", "84Q+IGF1": "Q84IGF"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\81faf204ee0675e01ceda312c920ebef1ecfe011\\GSE178367\\aligned\\design_metadata.csv", "sha256": "0cab692b374bd9bad6e2e4bce16c81139a53d083d262de4ba7421abd4561f536", "levels": {"grp": {"Q15": 3, "Q84": 3, "Q84IGF": 3}}}}

reasoning: Matrix columns are 'counts.<lab id>'; the lab id sits in brackets at the end of the GEO title (e.g. 'Cerebellar tissue - 84Q_rep1 [18_1_4]'). Exact match after stripping the 'counts.' prefix. Group from source_name_ch1, recoded to formula-safe names.

### matrix (valid, not_started)

final: {"source": "GSE178367_15Q_84Q_IGF1.txt.gz (GEO supplementary)", "paper_input": "featureCounts raw counts into DESeq2 (S4.5.p2, S4.7.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\81faf204ee0675e01ceda312c920ebef1ecfe011\\GSE178367\\aligned\\aligned_matrix.csv", "sha256": "abd292f9ad5b70ea04daa3f65314ae9894f1fc7fa34ec30482f9c5fd77532561", "n_features": 37816, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 360695.0, "median": 10.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (integer_fraction 1.0, max 360695, median 10); GEO data_processing says raw counts from featureCounts; matches paper input.

### design (refused, not_started)

final: {"analysis_type": "none", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\81faf204ee0675e01ceda312c920ebef1ecfe011\\GSE178367\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: The request asks how exercise affects gene expression. The paper's estimands are SCA3 genotype and IGF-1 treatment effects; the word 'exercise' appears only as a behavioral outcome of prior GH treatment (ABS.p1). Refused at design.

rejected alternatives: [{"value": "grp_Q84_vs_Q15 (genotype)", "reason_rejected": "disease-genotype effect, not exercise"}, {"value": "grp_Q84IGF_vs_Q84 (IGF-1 injection)", "reason_rejected": "pharmacological IGF-1 treatment, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG threshold",
    "paper": "Methods S4.7.p1: padj < 0.1 and |log2FC| >= log2(1.5)",
    "data": "Results S2.2.p1 reports DEG counts with 'adjusted p-value < 0.05'",
    "disposition": "recorded_not_executed"
  },
  {
    "item": "Requested estimand",
    "paper": "No exercise intervention; genotype and IGF-1 injection only (S4.1.p1)",
    "data": "GEO groups 15Q / 84Q / 84Q+IGF1; no exercise metadata",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE178367 / PMC8348158 (SCA3 transgenic mice, IGF-1)

**Status: refused at `design`. The study has no exercise contrast.**

## What ran
- `python -m tools.case_runner inspect GSE178367` (data cached in `E:/agent/mwangLab_pdf/data/GSE178367`): one matrix, `GSE178367_15Q_84Q_IGF1.txt.gz`, 37,816 Ensembl genes x 9 samples, all integer values (featureCounts raw counts).
- `python -m tools.case_runner execute case_spec.json`: gates `paper_reconstruction`, `ownership`, `alignment`, `matrix` valid; `design` refused. Validator: 5 records, 0 errors. No executors or enrichment ran.
- Alignment: exact on a key taken from the bracketed lab id in the GEO title, after `matrix_column_pattern ^counts\.(.+)$`. 9/9 matched. Groups: Q15=3, Q84=3, Q84IGF=3.

## Why refused
Paper (S4.1.p1) and GEO metadata have only two factors: ATXN3 genotype (15Q control vs 84Q SCA3) and weekly i.p. IGF-1 (50 mg/kg) vs PBS in 84Q mice, months 9 to 18. No animal was exercised or trained. "Exercise behavior" (ABS.p1) and the rotarod tests (S1.p3) are behavioral outcomes from an earlier GH study, not an intervention. Calling the genotype or IGF-1 contrast an "exercise" effect would change the estimand. The suitability report rated the 3 genotype/treatment comparisons analyzable, but none of them answers the request.

## DEG counts vs paper
None computed, because the case was refused. For reference, the paper reports:
- 84Q vs 15Q: 521 (62 up / 459 down)
- 84Q+IGF-1 vs 15Q: 588 (45 up / 543 down)
- 84Q+IGF-1 vs 84Q: 6 (1 up / 5 down)

The paper's threshold is DESeq2 Wald with BH, padj < 0.1 and |log2FC| >= log2(1.5) = 0.5849625 (S4.7.p1). The Results (S2.2.p1) say the counts used "adjusted p-value < 0.05", which conflicts with the Methods; this is recorded as a discrepancy.

## Deviations
None. Nothing was executed.

## Tool problems
None blocking. Minor: `inspect` returned `alignment_keys: []` for this series. The matrix names (`counts.18_1_4`) carry a `counts.` prefix and the key sits in brackets inside `title`, so the contained-name detector (`tools/case_runner.py:314` `_contained_keys`) suggested nothing. I had to work out `key_patterns` + `matrix_column_pattern` by hand. A hint that strips a common column prefix would have found it.

