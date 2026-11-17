# Review packet B (the analysis' decisions): GSE199429

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/ex_RUN_vs_SED_time-ZT15 | 121 | 113 | padj < 0.05 | 113 | 78 | 35 | 309 | 2057 | 414 | 102 | 777 | 0.078 | 0.127 |
| joint/ex_RUN_vs_SED_time-ZT3 | 0 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 373 | 29 | 5 | 40 | 0.098 | 0.023 |
| joint/time_ZT15_vs_ZT3_ex-SED | 192 | 187 | padj < 0.05 | 187 | 117 | 38 | 373 | 1955 | 414 | 83 | 786 | 0.077 | 0.12 |
| joint/time_ZT15_vs_ZT3_ex-RUN | 744 | 682 | padj < 0.05 | 682 | 318 | 73 | 1280 | 3368 | 759 | 154 | 1447 | 0.06 | 0.207 |

## Samples per design level

### `ex`
- **RUN** (12): GSM5972666 / 11RUN_m; GSM5972668 / 13Run_e; GSM5972670 / 15Run_e; GSM5972672 / 17RUN_m; GSM5972674 / 19RUN_m; GSM5972675 / 1RUN_m; GSM5972677 / 21Run_e; GSM5972679 / 23Run_e; GSM5972682 / 3RUN_m; GSM5972684 / 5Run_e; GSM5972686 / 7Run_e; GSM5972688 / 9RUN_m
- **SED** (12): GSM5972665 / 10SED_m; GSM5972667 / 12SED_m; GSM5972669 / 14SED_e; GSM5972671 / 16SED_e; GSM5972673 / 18SED_m; GSM5972676 / 20SED_m; GSM5972678 / 22SED_e; GSM5972680 / 24SED_e; GSM5972681 / 2SED_m; GSM5972683 / 4SED_m; GSM5972685 / 6SED_e; GSM5972687 / 8SED_e

### `time`
- **ZT15** (12): GSM5972668 / 13Run_e; GSM5972669 / 14SED_e; GSM5972670 / 15Run_e; GSM5972671 / 16SED_e; GSM5972677 / 21Run_e; GSM5972678 / 22SED_e; GSM5972679 / 23Run_e; GSM5972680 / 24SED_e; GSM5972684 / 5Run_e; GSM5972685 / 6SED_e; GSM5972686 / 7Run_e; GSM5972687 / 8SED_e
- **ZT3** (12): GSM5972665 / 10SED_m; GSM5972666 / 11RUN_m; GSM5972667 / 12SED_m; GSM5972672 / 17RUN_m; GSM5972673 / 18SED_m; GSM5972674 / 19RUN_m; GSM5972675 / 1RUN_m; GSM5972676 / 20SED_m; GSM5972681 / 2SED_m; GSM5972682 / 3RUN_m; GSM5972683 / 4SED_m; GSM5972688 / 9RUN_m

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE199429"], "assay": "bulk RNA-seq (TruSeq Stranded Total RNA Ribo-Zero Gold, NextSeq500 38-bp PE) of inguinal WAT (S3.5.p1)", "sample_inclusion": "male C57BL6/JBomTac mice, iWAT collected immediately (0 h) after 1-h maximal treadmill exercise or sham at ZT3 (early rest) or ZT15 (early active); n = 6 per group, 4 groups, 24 libraries (S3.1.p1, FIG1, S1.2.p1)", "sample_exclusion": "not_reported", "factors": {"exercise": ["SED (sham)", "RUN (exercise)"], "time_of_day": ["ZT3 early rest", "ZT15 early active"]}, "primary_estimand": "acute exercise (RUN vs sham SED) effect on iWAT gene expression immediately post-exercise, estimated separately at ZT15 (early active) and ZT3 (early rest)", "planned_contrasts": ["RUN vs SED at ZT15 (early active) (S1.2.p1; paper: 121 DEGs, mostly up)", "RUN vs SED at ZT3 (early rest) (S1.2.p1; paper: 0 DEGs)", "ZT15 vs ZT3 in SED (time-of-day, sedentary) (S1.2.p1; paper: 192 DEGs)", "ZT15 vs ZT3 in RUN (time-of-day, exercised) (S1.2.p1; paper: 744 DEGs)"], "repeated_measure_unit": "none (independent animals, one sample per mouse)", "normalization": "edgeR filterByExpr (min count 10, design by group), TMM/CPM (S3.6.p1)", "paper_method": "edgeR quasi-likelihood NB GLM, design ~0 + group (4 groups) (S3.6.p1)", "paper_threshold": {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "S3.6.p1"}, "paper_results": "121 DEGs RUN vs SED at ZT15,  ... [355 more characters]

reasoning: S3.6.p1 gives the DE route (edgeR QL, ~0+group, filterByExpr min count 10, FDR 0.05, no fold-change rule). S1.2.p1 gives the four contrasts and their counts. S3.1.p1/FIG1 give the 2x2 design with n = 6 per group at the 0 h time point. The fasting experiment (S1.4) is qPCR only and not in GEO.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE199429\\GSE199429_processed.data.csv.gz", "owned": true, "checks": ["paper S3.6.p1 and S8.p1 name GSE199429", "metadata series_id GSE199429, 24 samples, inguinal WAT, male C57BL6", "groups SED/RUN x ZT3/ZT15 with 6 per cell match FIG1 / S3.1.p1 (n = 6 per group)", "submitter Lundell (author L.S.L.); paper scripts at github leonidaslundell/GSE199429"], "accession": "GSE199429", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE199429\\GSE199429_metadata.csv"}

reasoning: Accession, tissue, sex, strain, design and n per group all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": ["entrez"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\aligned\\aligned_metadata.csv", "columns": {"ex": {"alias_of": "characteristics_ch1.4.exercise"}, "time": {"alias_of": "characteristics_ch1.3.sampling time"}, "grp": {"combine": ["ex", "time"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\aligned\\design_metadata.csv", "sha256": "0b37ad7800d6a6011034a69bcb5772d41f7ccfa4b5b3b8d6ef56da1260f78e1f", "levels": {"ex": {"SED": 12, "RUN": 12}, "time": {"ZT3": 12, "ZT15": 12}, "grp": {"SED_ZT3": 6, "RUN_ZT3": 6, "RUN_ZT15": 6, "SED_ZT15": 6}}}}

reasoning: Matrix columns (e.g. 13RUN_E) equal metadata titles (13Run_e) up to case; inspect reports 24/24 matches with normalize_keys. ex and time copied from GEO characteristics; grp is the paper's 4-level group (SED_ZT3, RUN_ZT3, SED_ZT15, RUN_ZT15). The _m/_e title suffix agrees with ZT3/ZT15 (morning/evening).

### matrix (valid, not_started)

final: {"matrix_type": "CPM normalized (linear scale)", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\aligned\\aligned_matrix.csv", "sha256": "278abe11c41f240f58996aab5b7ad31966e9e06eb04ebf30f5d734b3cfb741aa", "n_features": 16233, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 78383.8956541157, "median": 15.3800936812134, "integer_fraction": 0.0017, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: 'processed.data.csv contains cpm after filtering by expression with cutoff at 10 counts'. Profile agrees: 0.17% integers, column sums 0.84-1.19 million (CPM, likely TMM-scaled), max 78k, no negatives, 16,233 Ensembl genes already filtered. Linear normalized expression, not counts. The paper's input was featureCounts raw counts (S3.6.p1), which were not deposited (supplementary_file NONE for samples). Library sizes are not deposited either, so counts cannot be recovered and must not be reconstructed.

### design (valid, not_started)

final: {"analysis_type": "factorial 2x2 cell-means (exercise x time of day), independent animals", "formula": "~ 0 + cell (cell = ex x time, equivalent to the paper's ~0 + group)", "contrasts": [{"name": "ex_RUN_vs_SED_time-ZT15", "control": "SED_ZT15", "treatment": "RUN_ZT15", "role": "primary"}, {"name": "ex_RUN_vs_SED_time-ZT3", "control": "SED_ZT3", "treatment": "RUN_ZT3", "role": "primary"}, {"name": "time_ZT15_vs_ZT3_ex-SED", "control": "SED_ZT3", "treatment": "SED_ZT15", "role": "secondary"}, {"name": "time_ZT15_vs_ZT3_ex-RUN", "control": "RUN_ZT3", "treatment": "RUN_ZT15", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: The paper fits one model on all four groups (S3.6.p1 ~0+group) and reports the exercise effect within each time of day plus the time-of-day effect within each exercise state (S1.2.p1). The exercise-effect contrasts answer the request; the time-of-day ones reproduce the paper's other reported counts. The exercise x time interaction (difference of exercise effects) is implied by the paper's claim of a timing-specific response but was not tested as such; it runs as exploratory from the same model. Pooling ZT3 and ZT15 into one RUN vs SED contrast is rejected because the paper's estimand is time-specific.

rejected alternatives: [{"value": "pooled RUN vs SED ignoring time", "reason_rejected": "the paper's estimand is exercise effect per time of day; pooling mixes the two phases"}, {"value": "separate fits per time (strata)", "reason_rejected": "the paper fits one ~0+group model on all 24 samples"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "sex", "disposition": "excluded: constant (all male); the GEO filterByExpr call's '+ sex' term cannot apply"}], "design_check": {"formula_equivalent": "~ C(ex) + C(time)", "n_samples": 24, "n_columns": 3, "columns": ["Intercept", "ex_SED", "time_ZT3"], "rank": 3, "full_rank": true, "residual_df": 21, "levels": {"ex": {"SED": 12, "RUN": 12}, "time": {"ZT3": 12, "ZT15": 12}}, "cells": [{"cell": ["RUN", "ZT15"], "n": 6}, {"cell": ["RUN", "ZT3"], "n": 6}, {"cell": ["SED", "ZT15"], "n": 6}, {"cell": ["SED", "ZT3"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 24, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 24, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 4, "status": "nested_in_primary", "crosstab": {"RUN": {"Murine inguinal white adipose tissue from exercised animals sampled at ZT15": 6, "Murine inguinal white adipose tissue from exercised animals sampled at ZT3": 6, "Murine inguinal white adipose tissue from sedentary animals sampled at ZT15": 0, "Murine inguinal white adipose tissue ... [2998 more characters]

reasoning: One iWAT sample per independent mouse; no subject, batch, or lane column in GEO. S3.1.p1 says the 0 h protocol was repeated in a subset of 24 mice; which cohort each library came from is not recorded, so a cohort term cannot be modelled (caveat). The paper's model has no covariates.

### method (valid, not_started)

final: {"matrix_type": "CPM normalized (linear scale)", "method": "limma (moderated t, empirical Bayes) on log2(CPM+1), joint cell-means model", "formula": "~ 0 + C(cell)", "transform": "log2(x+1) on deposited CPM", "paper_route": {"method": "edgeR QL NB GLM on raw counts, ~0 + group", "status": "blocked", "reason": "GEO deposits only filtered CPM; raw counts and library sizes are not available, and CPM must not be converted back into integer counts"}, "deviations": ["limma on log2(CPM+1) instead of edgeR QL on counts", "filtering taken as deposited (authors' filterByExpr); no further filter"]}

reasoning: Matrix policy: linear normalized expression -> log2(x+1) then limma. The joint limma executor fits ~0 + cell on all 24 samples, the same parameterization as the paper, so each contrast shares the variance prior over all groups as in the paper.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S3.6.p1: all P values FDR-adjusted, alpha 0.05; no fold-change rule. Applied on the limma deviation route, BH within each contrast.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 24, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\joint\\DEG_results_ex_RUN_vs_SED_time-ZT15.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\joint\\DEG_results_ex_RUN_vs_SED_time-ZT3.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\joint\\DEG_results_time_ZT15_vs_ZT3_ex-RUN.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\joint\\DEG_results_time_ZT15_vs_ZT3_ex-SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\joint\\DEG_results_ex_time_RUN_ZT15_vs_SED_ZT3.csv"], "counts": {"joint/ex_RUN_vs_SED_time-ZT15": {"applied": {"rule": "padj < 0.05", "n_tested": 16233, "n_significant": 113, "n_up": 81, "n_down": 32, "deg_sanity": "ok"}}, "joint/ex_RUN_vs_SED_time-ZT3": {"applied": {"rule": "padj < 0.05", "n_tested": 16233, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "joint/time_ZT15_vs_ZT3_ex-RUN": {"applied": {"rule": "padj < 0.05", "n_tested": 16233, "n_significant": 682, "n_up": 408, "n_down": 274, " ... [337 more characters]

reasoning: One ~0+cell limma model on all 24 samples (paper's ~0+group); returns the four planned contrasts plus the exercise x time interaction (exploratory).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/ex_RUN_vs_SED_time-ZT15", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\enrichment_joint_ex_RUN_vs_SED_time-ZT15\\ora\\DEG_results_ex_RUN_vs_SED_time-ZT15_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\enrichment_joint_ex_RUN_vs_SED_time-ZT15\\ora\\DEG_results_ex_RUN_vs_SED_time-ZT15_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\enrichment_joint_ex_RUN_vs_SED_time-ZT15\\ora\\DEG_results_ex_RUN_vs_SED_time-ZT15_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\enrichment_joint_ex_RUN_vs_SED_time-ZT15\\ora\\DEG_results_ex_RUN_vs_SED_time-ZT15_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 112 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Response To Peptide Hormone S ... [1301 more characters]

reasoning: Paper reports GO molecular-function enrichment of the ZT15 exercise DEGs (S1.2.p2, FIG2D).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/ex_RUN_vs_SED_time-ZT15", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36780527\\GSE199429\\results\\enrichment_joint_ex_RUN_vs_SED_time-ZT15\\gsea\\DEG_results_ex_RUN_vs_SED_time-ZT15_GSEA_Hallmark.csv"], "summary": "GSEA complete on 16206 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 38 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.69 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=2.63 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.56 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_DN | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.10 | NOM p=0.00e+00 | FDR q=2.85e-04 - HALLMARK_ANDROGEN_RESPONSE | NES=2.07 | NOM p=0.00e+00 | FDR q=2.44e-04 - HALLMARK_PROTEIN_SECRETION | NES=2.01 | NOM p=0.00e+00 | FDR q=4.27e-04 - HALLMARK_ANGIOGENESIS | NES=1.95 | NOM p=1.99e-03 | FDR q=3.80e-04 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.81 | NOM p=0.00e+00 | FDR q=2.56e-03 ### Top 7 DOWN (NES < 0, depleted in treatment): - HALLMARK_E2F_TARGETS | NES=-2.41 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-1.90 ... [427 more characters]

reasoning: Paper reports GO molecular-function enrichment of the ZT15 exercise DEGs (S1.2.p2, FIG2D).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper's edgeR QL on counts could not run; limma on log2(CPM+1) from the deposited CPM is a declared deviation, so DEG counts are not expected to match exactly.", "Cohort of origin (original vs repeated 0 h subset, S3.1.p1) is not recorded in GEO and cannot be modelled.", "GEO processing notes (STAR 2.7.2b, Ensembl release 99, filterByExpr min.count 15 with + sex) differ from the paper's Methods (STAR 2.5.3a, release 92, min count 10)."], "results": {"joint/ex_RUN_vs_SED_time-ZT15": {"n_deg": 113, "up": 81, "down": 32, "rule": "padj < 0.05"}, "joint/ex_RUN_vs_SED_time-ZT3": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "joint/time_ZT15_vs_ZT3_ex-RUN": {"n_deg": 682, "up": 408, "down": 274, "rule": "padj < 0.05"}, "joint/time_ZT15_vs_ZT3_ex-SED": {"n_deg": 187, "up": 95, "down": 92, "rule": "padj < 0.05"}, "joint/ex_time_RUN_ZT15_vs_SED_ZT3": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}}, "paper_counts": {"joint/ex_RUN_vs_SED_time-ZT15": 121, "joint/ex_RUN_vs_SED_time-ZT3": 0, "joint/time_ZT15_vs_ZT3_ex-SED": 192, "joint/time_ZT15_vs_ZT3_ex-RUN": 744}, "comparison": {"joint/ex_RUN_vs_SED_time-ZT15": {"ours": 113, "paper": 121}, "joint/ex_RUN_vs_SED_time-ZT3": {"ours": 0, "paper": 0}, "joint/time_ZT15_vs_ZT3_ex-SED": {"ours": 187, "paper": 192}, "joint/time_ZT15_vs_ZT3_ex-RUN": {"ours": 682, "paper": 744}}, "paper_gene_check": {"joint/ex_RUN_vs_SED_time-ZT15": {"Nr4a1": {"AveExpr": 4.6795, "log2FoldChange": 2.480 ... [1313 more characters]

reasoning: Paper route blocked by missing counts; thresholds and contrasts follow the paper.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "deposited matrix",
    "paper": "featureCounts raw counts analysed with edgeR QL (S3.6.p1)",
    "data": "only filtered CPM deposited",
    "disposition": "declared_deviation: limma on log2(CPM+1)"
  },
  {
    "item": "processing versions",
    "paper": "STAR 2.5.3a, Ensembl mm10 release 92, filterByExpr min count 10 (S3.6.p1)",
    "data": "GEO data_processing: STAR 2.7.2b, release 99, filterByExpr min.count = 15 with design ~0 + group + sex; text says cutoff 10 counts",
    "disposition": "executable_without_change: filtering already applied by authors; recorded"
  },
  {
    "item": "sex covariate in GEO filter design",
    "paper": "all male mice (S3.1.p1)",
    "data": "all samples male; '+ sex' in GEO note cannot apply",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 36780527 / GSE199429

Paper: Time of day determines postexercise metabolism in mouse adipose tissue (PMC9974500).
Status: **finished** (route `declared_deviation`). The validator reported no errors in 12 records.

## What ran
- `case_runner inspect GSE199429` downloaded the series into `E:/agent/mwangLab_pdf/data/GSE199429`. One matrix was there, `GSE199429_processed.data.csv.gz`, with 16,233 Ensembl genes and 24 samples.
- `case_runner execute case_spec.json`:
  - **Alignment:** matched on `title` with `normalize_keys` (for example `13Run_e` = `13RUN_E`). All 24/24 samples aligned.
  - **Factors:** `ex` (SED/RUN) and `time` (ZT3/ZT15), with 6 samples per cell.
  - **Matrix:** CPM after the authors' filterByExpr. GEO `data_processing` says "processed.data.csv contains cpm after filtering". The profile agrees: 0.17% of values are integers and column sums run from 0.84M to 1.19M.
  - **Method:** limma on log2(CPM+1). It is one joint cell-means model `~ 0 + C(cell)` fitted on all 24 samples, the same parameterization as the paper's `~0 + group`. It produced the 4 planned contrasts plus the exercise×time interaction as an exploratory contrast.
  - **Threshold:** BH FDR < 0.05 with no fold-change rule. This is the paper's rule (S3.6.p1), applied on the deviation route.
  - **Enrichment:** ORA (Enrichr GO BP/MF/CC and KEGG) and Hallmark GSEA, run on the ZT15 RUN-vs-SED contrast only.

## DEG counts vs paper (FDR < 0.05, no FC cutoff)
| Contrast | Ours (up/down) | Paper |
|---|---|---|
| RUN vs SED at ZT15 (early active), primary | 113 (81/32) | 121, "most up-regulated" |
| RUN vs SED at ZT3 (early rest), primary | 0 | 0 |
| ZT15 vs ZT3 within SED | 187 (95/92) | 192 |
| ZT15 vs ZT3 within RUN | 682 (408/274) | 744 |
| Interaction ex×time, exploratory | 0 | not tested |

**Named genes, ZT15 exercise:** all 15 have a positive log2FC, the same direction as the paper.
- 8 pass FDR < 0.05: Nr4a1, Nr4a3, Cpeb2, Cyp2b10, Gadd45g, Irf4, Zfp516, Crem.
- 4 fall just short (padj 0.053–0.079): Adrb2, Slc25a25, Pdk4, Vegfa.
- 3 are clearly not significant: Ppargc1a (padj 0.21), Dio2 (0.51), Ucp1 (0.92, log2FC 0.49).

The paper shows these genes as up-regulated in the FIG2F heatmap.

**GO MF (ORA):** the top terms are nuclear glucocorticoid receptor binding (padj 0.0013), MAPK binding, DNA-binding transcription activator activity (RNA Pol II), and CREB binding. This agrees with the paper's FIG2D, which reports glucocorticoid receptor binding and DNA-binding t ... [2064 more characters]
