# Review packet B (the analysis' decisions): GSE155230_capacity

## Mechanical flags

- **other_rule_matches_paper**: {"table": "hcr_vs_lcr", "paper": 434, "applied": 81, "applied_rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "closest_rule": "pvalue<0.05 & |lfc|>1", "closest_n": 399, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.0.group level", "across": "characteristics_ch1.0.group", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hcr_vs_lcr | 434 | 81 | padj < 0.05 and |log2FoldChange| > 0.584963 | 81 | 81 | 72 | 110 | 986 | 760 | 399 | 348 | 0.108 | 0.048 |

## Samples per design level

### `grp`
- **HCR** (3): GSM4697795 / High capacity runner 1 / HCR_1; GSM4697796 / High capacity runner 2 / HCR_2; GSM4697797 / High capacity runner 3 / HCR_3
- **LCR** (3): GSM4697798 / Low capacity runner 1 / LCR_1; GSM4697799 / Low capacity runner 2 / LCR_2; GSM4697800 / Low capacity runner 3 / LCR_3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE155230"], "primary_estimand": "Intrinsic aerobic capacity: untrained HCR vs LCR gastrocnemius (selectively bred lines, generation 33); associational, no exercise intervention", "sample_inclusion": "3 male HCR and 3 male LCR, archived untrained muscle (S2.1.1.p1)", "planned_contrasts": ["HCR vs LCR (S3.1.p1, Fig 1C; paper: 434 DEGs, 257 up in HCR, 177 up in LCR)"], "paper_method": "TopHat2 -> Cufflinks/Cuffdiff (S2.3.1.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "fold change", "effect_cutoff": 1.5, "effect_cutoff_log2": 0.5849625, "source_locator": "S3.1.p1"}}

reasoning: S3.1.p1: 434 DEGs, fold change > 1.5, q < 0.05. This is the paper's intrinsic-capacity result; it compares bred lines without training, so it is kept as an associational secondary case, not an exercise effect.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\prep\\GSE155230_lcr_hcr_counts_clean.csv", "owned": true, "checks": ["S6.p1 names GSE155230", "GSE155230_lcr_hcr_counts.tsv.gz holds the 6 HCR/LCR libraries", "deposited lcr_hcr Cuffdiff list reproduces 434 = 257/177 under the paper rule"], "accession": "GSE155230", "metadata_file": "test/experiments/large_run_pilot_20261019/runs_claude/PMID33193103/prep/GSE155230_metadata_lane.csv"}

reasoning: Same series as the training case.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 6, "n_metadata": 18, "coverage": 0.3333, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM4697801", "GSM4697802", "GSM4697803", "GSM4697804", "GSM4697805", "GSM4697806", "GSM4697807", "GSM4697808", "GSM4697809", "GSM4697810", "GSM4697811", "GSM4697812"], "excluded_samples": {"GSM4697801": "HRT sample, analysed in case GSE155230_training", "GSM4697802": "HRT sample, analysed in case GSE155230_training", "GSM4697803": "HRT sample, analysed in case GSE155230_training", "GSM4697804": "LRT sample, analysed in case GSE155230_training", "GSM4697805": "LRT sample, analysed in case GSE155230_training", "GSM4697806": "LRT sample, analysed in case GSE155230_training", "GSM4697807": "HRTT sample, analysed in case GSE155230_training", "GSM4697808": "HRTT sample, analysed in case GSE155230_training", "GSM4697809": "HRTT sample, analysed in case GSE155230_training", "GSM4697810": "LRTT sample, analysed in case GSE155230_training", "GSM4697811": "LRTT sample, analysed in case GSE155230_training", "GSM4697812": "LRTT sample, analysed in case GSE155230_training"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_capacity\\aligned\\aligned_metadata_kept.csv", "columns": {"grp": {"source": "description", "regex": "^([A-Z]+)_\\d$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_capacity\\aligned\\design_metadata.csv", "sha25 ... [113 more characters]

reasoning: Exact match on GEO `description` (HCR_1 ...) after the prep script renamed BAM columns.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_capacity\\aligned\\aligned_matrix.csv", "sha256": "445c371ac44d8fa1ef7af6d12eda50ade9e687324dd3bd0d2cf03fa563974f3a", "n_features": 32882, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3062228.0, "median": 1.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: featureCounts integer counts (integer fraction 1.0); GEO data_processing says raw counts.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "LCR", "treatment": "HCR", "estimand_type": "associational", "contrasts": [{"name": "grp_HCR_vs_LCR", "control": "LCR", "treatment": "HCR", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_capacity\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Two bred lines, untrained; paper direction HCR/LCR.

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "lane", "disposition": "not modelled in the primary fit: balanced (HCR L1,L1,L3; LCR L3,L1,L1); fitted as covariate in the exploratory lane_check"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 6, "n_columns": 2, "columns": ["Intercept", "grp_LCR"], "rank": 2, "full_rank": true, "residual_df": 4, "levels": {"grp": {"HCR": 3, "LCR": 3}}, "cells": [{"cell": ["HCR"], "n": 3}, {"cell": ["LCR"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "lane", "n_levels": 2, "status": "crossed", "crosstab": {"HCR": {"L1": 2, "L3": 1}, "LCR": {"L1": 2, "L3": 1}}}]}

reasoning: Independent animals, all male; lane balanced.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "Cufflinks/Cuffdiff on TopHat2 BAMs", "status": "blocked", "reason": "BAMs not deposited; only featureCounts gene counts"}, "deviations": ["DESeq2 on featureCounts counts instead of Cuffdiff"]}

reasoning: Raw counts support DESeq2.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper rule applied to DESeq2 BH-adjusted p instead of Cuffdiff q."}

reasoning: S3.1.p1: fold change > 1.5, q < 0.05.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "hcr_vs_lcr", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_capacity\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_capacity\\results\\hcr_vs_lcr\\DEG_results_HCR_vs_LCR.csv"], "counts": {"hcr_vs_lcr": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14161, "n_significant": 81, "n_up": 46, "n_down": 35, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14161, "n_significant": 81, "n_up": 46, "n_down": 35, "deg_sanity": "ok"}}}}

reasoning: Paper's Fig 1 intrinsic-capacity contrast, associational.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "lane_check", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_capacity\\aligned\\aligned_matrix.csv", "formula": "~ grp + lane", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_capacity\\results\\lane_check\\DEG_results_L3_vs_L1.csv"], "counts": {"lane_check": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14580, "n_significant": 36, "n_up": 16, "n_down": 20, "deg_sanity": "tiny_n_per_group=2"}, "audit": {"rule": "padj < 0.05", "n_tested": 14580, "n_significant": 36, "n_up": 16, "n_down": 20, "deg_sanity": "ok"}}}}

reasoning: Measures the lane L3 vs L1 effect in the 6 HCR/LCR samples (lane balanced 2:1 within each line, ~ grp + lane), to judge whether the lane aliasing in the training case could explain DEGs. Not a biological contrast.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Associational line comparison (intrinsic capacity), not an effect of exercise training.", "Ppm1h contradicts the paper: S3.1.p1 lists it among genes higher in LCR, here log2FC(HCR/LCR)=+0.16, padj=1.0.", "Mup4 and Tmem8c (Mymk) were not found by symbol lookup; other paper genes agree in direction (Fam163a, Fosb, Cyp2j4 up in HCR; Ranbp3l, Igfn1 up in LCR significant)."], "results": {"hcr_vs_lcr": {"n_deg": 81, "up": 46, "down": 35, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 81}, "lane_check": {"n_deg": 36, "up": 16, "down": 20, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 36}}, "paper_counts": {"hcr_vs_lcr": 434}, "comparison": {"hcr_vs_lcr": {"ours": 81, "paper": 434}}, "paper_gene_check": {"hcr_vs_lcr": {"Pik3c2g": {"baseMean": 114.539, "log2FoldChange": 3.0159, "padj": 0.682, "pvalue": 0.0391}, "Mup4": null, "Fam163a": {"baseMean": 28.2221, "log2FoldChange": 4.1523, "padj": 6.18e-05, "pvalue": 8.73e-08}, "Fosb": {"baseMean": 50.0728, "log2FoldChange": 2.7862, "padj": 0.00129, "pvalue": 2.91e-06}, "Msln": {"baseMean": 34.0866, "log2FoldChange": 2.7084, "padj": 0.0709, "pvalue": 0.000476}, "Cyp2j4": {"baseMean": 235.8028, "log2FoldChange": 2.4621, "padj": 3.9e-13, "pvalue": 1.38e-16}, "Tmem8c": null, "Ranbp3l": {"baseMean": 67.3025, "log2FoldChange": -3.0548, "padj": 8.81e-09, "pvalue": 5.6e-12}, "Ppm1h": {"baseMean": 44.2313, "log2FoldChange": 0.1551, "padj": 0.999, "pvalue": 0.698}, "I ... [191 more characters]

reasoning: Pik3c2g, Mup4, Fam163a, Fosb, Msln, Cyp2j4 higher in HCR; Tmem8c, Ranbp3l, Ppm1h, Igfn1, Ifit1 higher in LCR (S3.1.p1).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "Cuffdiff",
    "data": "featureCounts counts",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID33193103 / GSE155230

Paper: Comparative Analysis of Skeletal Muscle Transcriptional Signatures Associated With Aerobic Exercise Capacity or Response to Training in Humans and Rats (PMC7649134).
Decision maker: Claude Opus 5.5 session. Route: case spec (`case_spec.json`) → `python -m tools.case_runner execute`. Run status: **completed**. Contract validator: 25 records, 0 errors.

## What ran

The data are 18 rat gastrocnemius bulk RNA-seq samples, all male, n=3 per group. The paper's own route (TopHat2 → Cufflinks/Cuffdiff on BAMs, S2.3.1.p1) is blocked because only featureCounts gene counts were deposited. Every table below is therefore a **declared deviation**: DESeq2 (pydeseq2 Wald) on raw counts, using the paper's threshold.

**Threshold (paper, S3.1.p1 / S3.2.p1):** fold change > 1.5 and FDR/q < 0.05, applied as `padj < 0.05 & |log2FC| > 0.5849625`. The source is recorded as `paper_on_deviation_route`. An audit rule (padj < 0.05, no fold-change cutoff) is also recorded.

**Case `GSE155230_training`** (exercise estimand, 12 samples): one joint model `~ grp` with 4 levels (LRT, LRTT, HRT, HRTT). Trained and untrained rats are separate animals (S2.1.3.p1), so the design is unpaired.
- Training effect: `grp_LRTT_vs_LRT` and `grp_HRTT_vs_HRT` (primary, S3.2.p3). These are causal within each line.
- `grp_HRTT_vs_LRTT` (Fig 2C headline) and `grp_HRT_vs_LRT` (untrained baseline) are secondary. They compare selectively bred lines, so they are associational.

**Case `GSE155230_capacity`** (6 samples): `hcr_vs_lcr`, untrained HCR vs LCR (Fig 1C). This is associational intrinsic capacity, not an exercise effect. It also holds an exploratory `lane_check` model (L3 vs L1, `~ grp + lane`).

### Paper counts

The text gives counts only for HCR/LCR (434) and HRTT/LRTT (255). The training-contrast counts come from the authors' deposited Cuffdiff lists (`GSE155230_*_deg.csv.gz`). Under the paper rule those lists reproduce the text exactly: 434 = 257/177 and 255 = 68/187.

| table | ours n (up/down) | paper n (up/down) | audit n (padj<0.05) |
|---|---|---|---|
| training_joint/grp_LRTT_vs_LRT | 8 (4/4) | 255 (174/81), deposited list | 8 |
| training_joint/grp_HRTT_vs_HRT | 2 (1/1) | 90 (62/28), deposited list | 3 |
| training_joint/grp_HRTT_vs_LRTT | 34 (18/16) | 255 (68/187), S3.2.p1 | 35 |
| training_joint/grp_HRT_vs_LRT | 20 (9/11) | 234 (64/170), deposited list | 23 |
| hcr_vs_lcr | 81 (46/35) | 434 (257/177), S3.1.p1 | 81 |

Our counts are 3–45× lowe ... [5521 more characters]
