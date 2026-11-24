# Review packet B (the analysis' decisions): GSE198229_heart

## Mechanical flags

- none

## Samples per design level

### `trt`
- **EX** (24): GSM5944813 / A17 [heart, ANT1-/-]; GSM5944817 / A64 [heart, ANT1-/-]; GSM5944818 / A69 [heart, ANT1-/-]; GSM5944820 / A71 [heart, ANT1-/-]; GSM5944822 / A73 [heart, ANT1-/-]; GSM5944823 / A76 [heart, ANT1-/-]; GSM5944826 / B9 [heart, ND5S204F]; GSM5944828 / B11 [heart, ND5S204F]; GSM5944829 / B13 [heart, ND5S204F]; GSM5944831 / B69 [heart, ND5S204F]; GSM5944833 / B71 [heart, ND5S204F]; GSM5944836 / B83 [heart, ND5S204F]; GSM5944838 / E44 [heart, CO1V421A]; GSM5944839 / E50 [heart, CO1V421A]; GSM5944840 / E52 [heart, CO1V421A]; GSM5944843 / E56 [heart, CO1V421A]; GSM5944846 / E74 [heart, CO1V421A]; GSM5944848 / E80 [heart, CO1V421A]; GSM5944849 / I4 [heart, ND6P25L]; GSM5944850 / I50 [heart, ND6P25L]; GSM5944852 / I55 [heart, ND6P25L]; GSM5944854 / I57 [heart, ND6P25L]; GSM5944856 / I59 [heart, ND6P25L]; GSM5944858 / I63 [heart, ND6P25L]
- **SED** (24): GSM5944814 / A23 [heart, ANT1-/-]; GSM5944815 / A58 [heart, ANT1-/-]; GSM5944816 / A63 [heart, ANT1-/-]; GSM5944819 / A70 [heart, ANT1-/-]; GSM5944821 / A72 [heart, ANT1-/-]; GSM5944824 / A80 [heart, ANT1-/-]; GSM5944825 / B5 [heart, ND5S204F]; GSM5944827 / B10 [heart, ND5S204F]; GSM5944830 / B21 [heart, ND5S204F]; GSM5944832 / B70 [heart, ND5S204F]; GSM5944834 / B80 [heart, ND5S204F]; GSM5944835 / B81 [heart, ND5S204F]; GSM5944837 / E42 [heart, CO1V421A]; GSM5944841 / E53 [heart, CO1V421A]; GSM5944842 / E55 [heart, CO1V421A]; GSM5944844 / E64 [heart, CO1V421A]; GSM5944845 / E69 [heart, CO1V421A]; GSM5944847 / E75 [heart, CO1V421A]; GSM5944851 / I53 [heart, ND6P25L]; GSM5944853 / I56 [heart, ND6P25L]; GSM5944855 / I58 [heart, ND6P25L]; GSM5944857 / I62 [heart, ND6P25L]; GSM5944859 / I76 [heart, ND6P25L]; GSM5944860 / I95 [heart, ND6P25L]

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE198229"], "assay": "bulk poly-A RNA-seq, STAR + RSEM expected counts (mm10, Gencode M17)", "tissue": "heart", "factors": {"strain": ["B6 control", "ND5S204F", "ND6P25L", "CO1V421A", "ANT1-/-"], "treatment": ["exercised (8 wk treadmill, every 2nd day, 45 min at 50% max)", "non-exercised (handled)"]}, "sample_inclusion": "60 heart samples: per strain 6 non-exercised + 6 exercised (3 responders + 3 non-responders) (S3.8.2.p1)", "primary_estimand": "effect of 8-wk endurance exercise training on gene expression, exercised vs non-exercised within each strain", "planned_contrasts": ["B6 exercised vs non-exercised (S3.8.2.p3)", "ANT1 exercised vs non-exercised (S3.8.2.p3)", "ND5 exercised vs non-exercised (S3.8.2.p3)", "ND6 exercised vs non-exercised (S3.8.2.p3)", "CO1 exercised vs non-exercised (S3.8.2.p3)"], "repeated_measure_unit": "none: one sample per mouse per tissue; independent mice", "normalization": "voom on RSEM expected counts", "paper_method": "limma-voom, exercised vs non-exercised within each strain", "paper_threshold": {"metric": null, "cutoff": null, "note": "not stated for heart (S3.8.2.p3)"}, "paper_results": "Heart (S1.2.5.p2, Fig. 4D): pathways altered in exercised vs rested ANT1 hearts include amino acid metabolism (up), stress response, translation, immune activation, signal transduction. No DEG counts in the main text."}

reasoning: Methods S3.8.2.p3 describe within-strain exercised vs non-exercised limma-voom on RSEM expected counts; S3.8.2.p1 gives the sample design; DA.p1 deposits GSE198229.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE198229\\GSE198229_heart_expected_counts_matrix.tsv.gz", "owned": true, "checks": ["DA.p1 and S3.8.2.p7 name GSE198229", "matrix GSE198229_heart_expected_counts_matrix.tsv.gz has 60 columns matching the 60 heart samples (48 by animal ID; 12 B6 columns are numbered)", "strain x treatment counts in GEO (6/6 per strain) match S3.8.1.p1/S3.8.2.p1"], "accession": "GSE198229", "metadata_file": "E:/agent/mwangLab_pdf/test/experiments/large_run_pilot_20261019/runs_claude/PMID35482926/prep/GSE198229_heart_metadata.csv"}

reasoning: Paper's own deposit; tissue-specific matrix.

### alignment (valid, not_started)

final: {"method": "exact:animal", "n_aligned": 48, "n_metadata": 60, "coverage": 0.8, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM5944861", "GSM5944862", "GSM5944863", "GSM5944864", "GSM5944865", "GSM5944866", "GSM5944867", "GSM5944868", "GSM5944869", "GSM5944870", "GSM5944871", "GSM5944872"], "excluded_samples": {"N2": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N5": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N63": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N65": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N66": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N8": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N1": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N6 ... [1583 more characters]

reasoning: Matrix columns are animal IDs (A76, B9, E42, I50); metadata per tissue was split by a prep script and the ID parsed from title (e.g. 'A76 [heart, ANT1-/-]'). Exact match for ANT1/ND5/ND6/CO1 (48/48). The 12 B6 columns are numbers (25-36 soleus, 37-48 heart) while GEO titles are N1..N69; nothing links them, so the B6 samples are excluded and the numeric columns dropped by matrix_column_pattern. The B6 contrast cannot be run (manual_review: needs the submitter number-to-N-ID map).

### matrix (valid, not_started)

final: {"source": "GSE198229_heart_expected_counts_matrix.tsv.gz", "paper_input": "RSEM expected counts (S3.8.1.p1, S3.8.1.p3)", "matrix_type": "estimated counts", "recommended_method": "limma-voom", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\aligned\\aligned_matrix.csv", "sha256": "16a7ec56300eecb0ae72d436c51d35071f8d0641c48835de289fa628e086b773", "n_features": 53656, "n_samples": 48, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3349033.32, "median": 0.0, "integer_fraction": 0.9332, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name 'expected_counts', ~94% integer values with fractional remainder, max ~3e6, data_processing: STAR --quantMode TranscriptomeSAM + RSEM. These are RSEM expected counts, the input the paper fed to voom. The sibling fpkm file is not used.

### design (valid, not_started)

final: {"analysis_type": "two-group within each strain stratum", "design_column": "trt", "control": "SED", "treatment": "EX", "contrasts": [{"name": "trt_EX_vs_SED_strain-ANT1", "control": "SED", "treatment": "EX", "role": "primary"}, {"name": "trt_EX_vs_SED_strain-ND5", "control": "SED", "treatment": "EX", "role": "primary"}, {"name": "trt_EX_vs_SED_strain-ND6", "control": "SED", "treatment": "EX", "role": "primary"}, {"name": "trt_EX_vs_SED_strain-CO1", "control": "SED", "treatment": "EX", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\suitability\\suitability.md", "n_comparisons": 4, "n_analyzable": 4}}

reasoning: S3.8.2.p3: 'comparing each gene in the exercise-trained vs. the non-exercise-trained group within each strain'. Strain is a stratum: each strain fitted separately as in the paper. Responder/non-responder status (soleus only) splits the exercised arm by outcome; the paper pools both into the exercised group, so it is not a factor. Between-strain comparisons are baseline genotype questions, not the exercise estimand, and are not run.

rejected alternatives: [{"value": "joint model ~ strain*trt on all samples", "reason_rejected": "paper fits within strain; per-strain fit reproduces its variance estimate"}, {"value": "responders vs non-responders", "reason_rejected": "outcome-defined split of the exercised arm, not the exercise effect; n=3 vs 3"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "exercise response", "disposition": "not used: defined only within the exercised arm (aliased with trt), outcome-based"}], "design_check": {"formula_equivalent": "~ C(trt)", "n_samples": 48, "n_columns": 2, "columns": ["Intercept", "trt_SED"], "rank": 2, "full_rank": true, "residual_df": 46, "levels": {"trt": {"EX": 24, "SED": 24}}, "cells": [{"cell": ["EX"], "n": 24}, {"cell": ["SED"], "n": 24}], "min_cell_size": 24, "missing_values": {}}, "confounding": []}

reasoning: Independent mice, one sample per mouse per tissue; no batch or lane recorded. Exercise response is nested in the exercised arm and cannot be a covariate.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "limma-voom (R limma::voom + eBayes, library size = column sums)", "formula": "~ trt", "rounding_documented": true, "paper_route": {"method": "limma-voom on RSEM expected counts", "status": "reproduced"}, "deviations": ["expected counts rounded to integers before voom (the tool requires integers; the paper passed non-integer expected counts)", "no TMM normalization factors (tool uses column-sum library sizes; paper normalization factors unknown)", "genes with zero counts in all 12 samples dropped by the tool (paper reports 58,581 tested; matrix has 53,656 rows)"], "transform": "round"}

reasoning: S3.8.2.p3: voom on RSEM expected counts then limma. The repository limma-voom executor runs R limma::voom.

### threshold (valid, not_started)

final: {"paper_threshold": null, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Heart methods (S3.8.2.p3) state no DEG threshold; the nominal P < 0.05 Metascape rule is described only for skeletal muscle (S3.8.1.p3). It is kept as an audit rule."}

reasoning: S3.8.2.p3 gives no threshold for heart DE; workflow_default BH padj < 0.05, no effect cutoff.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ANT1_EX_vs_SED", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ANT1_EX_vs_SED\\input\\matrix.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ANT1_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"ANT1_EX_vs_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 26240, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26240, "n_significant": 621, "n_up": 417, "n_down": 204, "deg_sanity": "ok"}}}}

reasoning: ANT1 exercised vs non-exercised, limma-voom (S3.8.2.p3)

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ND5_EX_vs_SED", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ND5_EX_vs_SED\\input\\matrix.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ND5_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"ND5_EX_vs_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 27394, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 27394, "n_significant": 623, "n_up": 149, "n_down": 474, "deg_sanity": "ok"}}}}

reasoning: ND5 exercised vs non-exercised, limma-voom (S3.8.2.p3)

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ND6_EX_vs_SED", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ND6_EX_vs_SED\\input\\matrix.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ND6_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"ND6_EX_vs_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 26883, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26883, "n_significant": 2481, "n_up": 2392, "n_down": 89, "deg_sanity": "ok"}}}}

reasoning: ND6 exercised vs non-exercised, limma-voom (S3.8.2.p3)

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "CO1_EX_vs_SED", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\CO1_EX_vs_SED\\input\\matrix.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\CO1_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"CO1_EX_vs_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 26206, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26206, "n_significant": 1278, "n_up": 1053, "n_down": 225, "deg_sanity": "ok"}}}}

reasoning: CO1 exercised vs non-exercised, limma-voom (S3.8.2.p3)

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ANT1_EX_vs_SED_filtered", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ANT1_EX_vs_SED_filtered\\input\\rounded_counts.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ANT1_EX_vs_SED_filtered\\DEG_results_EX_vs_SED.csv"], "counts": {"ANT1_EX_vs_SED_filtered": {"applied": {"rule": "padj < 0.05", "n_tested": 12525, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 12525, "n_significant": 145, "n_up": 137, "n_down": 8, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: the paper tested all genes without a low-count filter; in the unfiltered fit hundreds of genes detected in 1-2 samples share identical t statistics and dominate the nominal-P counts. Keep genes with CPM >= 1 in >= 6 samples (the arm size) as in the usual voom workflow.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ND5_EX_vs_SED_filtered", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ND5_EX_vs_SED_filtered\\input\\rounded_counts.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ND5_EX_vs_SED_filtered\\DEG_results_EX_vs_SED.csv"], "counts": {"ND5_EX_vs_SED_filtered": {"applied": {"rule": "padj < 0.05", "n_tested": 13229, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 13229, "n_significant": 49, "n_up": 20, "n_down": 29, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: the paper tested all genes without a low-count filter; in the unfiltered fit hundreds of genes detected in 1-2 samples share identical t statistics and dominate the nominal-P counts. Keep genes with CPM >= 1 in >= 6 samples (the arm size) as in the usual voom workflow.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ND6_EX_vs_SED_filtered", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ND6_EX_vs_SED_filtered\\input\\rounded_counts.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\ND6_EX_vs_SED_filtered\\DEG_results_EX_vs_SED.csv"], "counts": {"ND6_EX_vs_SED_filtered": {"applied": {"rule": "padj < 0.05", "n_tested": 13181, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 13181, "n_significant": 1444, "n_up": 1436, "n_down": 8, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: the paper tested all genes without a low-count filter; in the unfiltered fit hundreds of genes detected in 1-2 samples share identical t statistics and dominate the nominal-P counts. Keep genes with CPM >= 1 in >= 6 samples (the arm size) as in the usual voom workflow.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "CO1_EX_vs_SED_filtered", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\CO1_EX_vs_SED_filtered\\input\\rounded_counts.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\CO1_EX_vs_SED_filtered\\DEG_results_EX_vs_SED.csv"], "counts": {"CO1_EX_vs_SED_filtered": {"applied": {"rule": "padj < 0.05", "n_tested": 12570, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 12570, "n_significant": 538, "n_up": 457, "n_down": 81, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: the paper tested all genes without a low-count filter; in the unfiltered fit hundreds of genes detected in 1-2 samples share identical t statistics and dominate the nominal-P counts. Keep genes with CPM >= 1 in >= 6 samples (the arm size) as in the usual voom workflow.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ANT1_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_ANT1_EX_vs_SED\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 26240 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 28 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_DNA_REPAIR | NES=2.00 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.82 | NOM p=0.00e+00 | FDR q=1.13e-03 - HALLMARK_APICAL_JUNCTION | NES=1.74 | NOM p=0.00e+00 | FDR q=2.26e-03 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.71 | NOM p=1.10e-03 | FDR q=4.07e-03 - HALLMARK_UV_RESPONSE_UP | NES=1.64 | NOM p=0.00e+00 | FDR q=1.26e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.62 | NOM p=3.78e-03 | FDR q=1.33e-02 - HALLMARK_P53_PATHWAY | NES=1.60 | NOM p=0.00e+00 | FDR q=1.60e-02 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.57 | NOM p=1.10e-03 | FDR q=1.91e-02 - HALLMARK_NOTCH_SIGNALING | NES=1.57 | NOM p=8.33e-03 | FDR q=1.90e-02 ### Top 1 DOWN (NES < 0, depleted in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=-1.02 | NOM p=3.88e-01 | FDR q=3.93e-01 Full results saved to: test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35 ... [108 more characters]

reasoning: paper ran GSEA (Hallmark + C2 CP) on each within-strain exercise contrast (S3.8.2.p3); Hallmark only here

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ND5_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_ND5_EX_vs_SED\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 27394 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 7 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.91 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.39 | NOM p=1.35e-02 | FDR q=1.51e-01 - HALLMARK_KRAS_SIGNALING_DN | NES=1.22 | NOM p=5.33e-02 | FDR q=3.93e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=1.14 | NOM p=1.78e-01 | FDR q=5.43e-01 - HALLMARK_ADIPOGENESIS | NES=1.09 | NOM p=1.89e-01 | FDR q=6.43e-01 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.03 | NOM p=3.93e-01 | FDR q=8.39e-01 - HALLMARK_SPERMATOGENESIS | NES=1.02 | NOM p=3.69e-01 | FDR q=7.32e-01 - HALLMARK_PEROXISOME | NES=1.01 | NOM p=4.42e-01 | FDR q=7.09e-01 - HALLMARK_DNA_REPAIR | NES=0.99 | NOM p=4.38e-01 | FDR q=6.90e-01 - HALLMARK_E2F_TARGETS | NES=0.89 | NOM p=8.83e-01 | FDR q=9.84e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.02 | NOM p=0.00e+00 | FDR q=9.01e-04 - HALLMARK_ANGIOGENESIS | NES=-1.64 | NOM p=5.87e-03 | FDR q=2.75e-02 - HALLMARK_T ... [386 more characters]

reasoning: paper ran GSEA (Hallmark + C2 CP) on each within-strain exercise contrast (S3.8.2.p3); Hallmark only here

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ND6_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_ND6_EX_vs_SED\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 26883 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 40 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.26 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=1.83 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=1.78 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_NOTCH_SIGNALING | NES=1.72 | NOM p=0.00e+00 | FDR q=7.37e-04 - HALLMARK_COAGULATION | NES=1.71 | NOM p=0.00e+00 | FDR q=7.86e-04 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.56 | NOM p=0.00e+00 | FDR q=7.53e-03 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.54 | NOM p=0.00e+00 | FDR q=7.30e-03 - HALLMARK_GLYCOLYSIS | NES=1.51 | NOM p=0.00e+00 | FDR q=9.58e-03 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.51 | NOM p=4.01e-03 | FDR q=8.73e-03 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.51 | NOM p=1.00e-03 | FDR q=8.06e-03 ### Top 1 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.00 | NOM p=1.00e+00 | FDR q=4.80e-01 Full results saved to: test\\experiments\\large_run_pilot_20261019\\r ... [125 more characters]

reasoning: paper ran GSEA (Hallmark + C2 CP) on each within-strain exercise contrast (S3.8.2.p3); Hallmark only here

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "CO1_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_CO1_EX_vs_SED\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 26206 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 25 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.77 | NOM p=0.00e+00 | FDR q=4.55e-03 - HALLMARK_ANGIOGENESIS | NES=1.72 | NOM p=1.15e-03 | FDR q=5.01e-03 - HALLMARK_NOTCH_SIGNALING | NES=1.59 | NOM p=1.28e-02 | FDR q=2.67e-02 - HALLMARK_APICAL_JUNCTION | NES=1.56 | NOM p=0.00e+00 | FDR q=2.98e-02 - HALLMARK_COAGULATION | NES=1.52 | NOM p=1.03e-03 | FDR q=3.77e-02 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.50 | NOM p=0.00e+00 | FDR q=4.19e-02 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.49 | NOM p=2.70e-02 | FDR q=3.98e-02 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.42 | NOM p=1.99e-02 | FDR q=8.27e-02 - HALLMARK_E2F_TARGETS | NES=1.36 | NOM p=9.06e-03 | FDR q=1.33e-01 - HALLMARK_KRAS_SIGNALING_UP | NES=1.35 | NOM p=8.04e-03 | FDR q=1.33e-01 ### Top 6 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.84 | NOM p=0.00e+00 | FDR q=1.06e-02 - HALLMARK_FATTY_ACID_METABOLISM | NES=-1.31 | NOM p=0.00e+00 | FDR q=1. ... [390 more characters]

reasoning: paper ran GSEA (Hallmark + C2 CP) on each within-strain exercise contrast (S3.8.2.p3); Hallmark only here

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ANT1_EX_vs_SED_filtered", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_ANT1_EX_vs_SED_filtered\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12525 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 6 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_NOTCH_SIGNALING | NES=1.54 | NOM p=1.16e-02 | FDR q=9.27e-02 - HALLMARK_DNA_REPAIR | NES=1.50 | NOM p=0.00e+00 | FDR q=6.55e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.49 | NOM p=6.07e-03 | FDR q=5.94e-02 - HALLMARK_MYC_TARGETS_V1 | NES=1.47 | NOM p=0.00e+00 | FDR q=5.72e-02 - HALLMARK_APICAL_JUNCTION | NES=1.36 | NOM p=0.00e+00 | FDR q=1.62e-01 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.32 | NOM p=2.30e-02 | FDR q=2.41e-01 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.29 | NOM p=2.00e-02 | FDR q=2.77e-01 - HALLMARK_UV_RESPONSE_UP | NES=1.27 | NOM p=3.20e-02 | FDR q=2.94e-01 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.25 | NOM p=1.60e-02 | FDR q=3.38e-01 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.24 | NOM p=1.67e-01 | FDR q=3.57e-01 ### Top 0 DOWN (NES < 0, depleted in treatment): Full results saved to: test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_AN ... [70 more characters]

reasoning: GSEA on the filtered ranking: tied low-count statistics distort the unfiltered ranking

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ND5_EX_vs_SED_filtered", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_ND5_EX_vs_SED_filtered\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13229 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 33 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.93 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.31 | NOM p=4.58e-02 | FDR q=3.07e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=1.31 | NOM p=6.98e-02 | FDR q=2.11e-01 - HALLMARK_KRAS_SIGNALING_DN | NES=1.24 | NOM p=1.14e-01 | FDR q=2.69e-01 - HALLMARK_SPERMATOGENESIS | NES=1.17 | NOM p=1.89e-01 | FDR q=3.41e-01 - HALLMARK_ADIPOGENESIS | NES=1.17 | NOM p=1.22e-01 | FDR q=2.94e-01 - HALLMARK_DNA_REPAIR | NES=1.12 | NOM p=2.22e-01 | FDR q=3.54e-01 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.03 | NOM p=3.90e-01 | FDR q=5.32e-01 - HALLMARK_PEROXISOME | NES=1.00 | NOM p=4.53e-01 | FDR q=5.60e-01 - HALLMARK_XENOBIOTIC_METABOLISM | NES=0.97 | NOM p=5.36e-01 | FDR q=5.66e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.61 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=-2.13 | NOM p=0.00e+00  ... [404 more characters]

reasoning: GSEA on the filtered ranking: tied low-count statistics distort the unfiltered ranking

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ND6_EX_vs_SED_filtered", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_ND6_EX_vs_SED_filtered\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13181 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 14 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=1.77 | NOM p=0.00e+00 | FDR q=4.81e-04 - HALLMARK_NOTCH_SIGNALING | NES=1.57 | NOM p=8.02e-03 | FDR q=1.73e-02 - HALLMARK_COAGULATION | NES=1.57 | NOM p=0.00e+00 | FDR q=1.49e-02 - HALLMARK_APICAL_JUNCTION | NES=1.56 | NOM p=0.00e+00 | FDR q=1.27e-02 - HALLMARK_PANCREAS_BETA_CELLS | NES=1.50 | NOM p=2.82e-02 | FDR q=1.97e-02 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.34 | NOM p=4.00e-03 | FDR q=1.21e-01 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.33 | NOM p=4.50e-02 | FDR q=1.16e-01 - HALLMARK_MYOGENESIS | NES=1.32 | NOM p=4.00e-03 | FDR q=1.19e-01 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.29 | NOM p=1.60e-02 | FDR q=1.54e-01 ### Top 2 DOWN (NES < 0, depleted in treatment): - HALLMARK_FATTY_ACID_METABOLISM | NES=-1.00 | NOM p=1.00e+00 | FDR q=5.00e-01 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.00 |  ... [235 more characters]

reasoning: GSEA on the filtered ranking: tied low-count statistics distort the unfiltered ranking

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "CO1_EX_vs_SED_filtered", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_heart\\results\\enrichment_CO1_EX_vs_SED_filtered\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12570 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 23 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.74 | NOM p=0.00e+00 | FDR q=4.62e-03 - HALLMARK_ANGIOGENESIS | NES=1.70 | NOM p=3.45e-03 | FDR q=5.54e-03 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.61 | NOM p=2.09e-03 | FDR q=1.72e-02 - HALLMARK_COAGULATION | NES=1.59 | NOM p=1.03e-03 | FDR q=1.94e-02 - HALLMARK_APICAL_SURFACE | NES=1.55 | NOM p=1.20e-02 | FDR q=2.51e-02 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.55 | NOM p=0.00e+00 | FDR q=2.26e-02 - HALLMARK_NOTCH_SIGNALING | NES=1.54 | NOM p=1.26e-02 | FDR q=2.19e-02 - HALLMARK_APICAL_JUNCTION | NES=1.49 | NOM p=0.00e+00 | FDR q=3.36e-02 - HALLMARK_E2F_TARGETS | NES=1.43 | NOM p=2.02e-03 | FDR q=5.91e-02 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.38 | NOM p=6.21e-02 | FDR q=1.04e-01 ### Top 5 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=-1.60 | NOM p=0.00 ... [413 more characters]

reasoning: GSEA on the filtered ranking: tied low-count statistics distort the unfiltered ranking

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["B6 control (wild-type) exercise contrast not run: B6 matrix columns cannot be mapped to GEO samples", "Paper reports no DEG counts in the main text; supplementary Datasets S1-S11 were not available, so comparison is qualitative only"], "results": {"ANT1_EX_vs_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 621}, "ND5_EX_vs_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 623}, "ND6_EX_vs_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 2481}, "CO1_EX_vs_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 1278}, "ANT1_EX_vs_SED_filtered": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 145}, "ND5_EX_vs_SED_filtered": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 49}, "ND6_EX_vs_SED_filtered": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 1444}, "CO1_EX_vs_SED_filtered": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 538}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {}}

reasoning: Within-strain voom contrasts reproduce the paper route for 4 of 5 strains; the B6 contrast is blocked at alignment.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 48 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "B6 control sample IDs",
    "paper": "6 exercised + 6 non-exercised B6 per tissue",
    "data": "matrix columns 25-36 / 37-48 have no mapping to GEO N-IDs or exercise status",
    "disposition": "blocks_contrast"
  },
  {
    "item": "genes tested",
    "paper": "58,581",
    "data": "53,656 rows in the deposited matrix",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID35482926 / GSE198229

Paper: *Mitochondrial mutations alter endurance exercise response and determinants in mice* (PNAS 2022, PMC9170171).
Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. The validator reported 50 records and 0 errors. Both cases are `completed`, `valid` and `paper_aligned`.

## What the paper does
- It studies five mouse strains: B6 control, ND5^S204F, ND6^P25L, CO1^V421A and ANT1^-/-. Half of each strain had 8 weeks of treadmill training and half were handled but not run (S3.2.p1).
- RNA-seq covers soleus and heart: 6 non-exercised and 6 exercised animals per strain, with the exercised arm made of 3 responders and 3 non-responders (S3.8.1.p1, S3.8.2.p1).
- DE was exercised vs non-exercised **within each strain**, using voom on RSEM expected counts followed by limma. It tested all 58,581 genes with no filter (S3.8.1.p3, S3.8.2.p3). Pathways used GSEA with Hallmark and C2 CP gene sets.
- Threshold:
  - Soleus: the only stated rule is nominal **P < 0.05** with no fold-change cutoff, used for the Metascape gene lists (S3.8.1.p3).
  - Heart: no threshold is stated.
- **The main text gives no DEG counts.** They are in supplementary Datasets S1–S11, which were not available here, so the comparison is qualitative only.

## What ran
Prep: `prep/split_metadata_by_tissue.py` splits the GEO metadata by tissue and parses the animal ID from `title`, because the same animal ID appears in both tissues. No values are changed.

Two cases. Each fits limma-voom (R `limma::voom` + `eBayes`, `~ trt`) separately within each strain, EX vs SED, on rounded RSEM expected counts:

| Table | Soleus n (up/down), P<0.05 [paper rule] | Soleus padj<0.05 (audit) | Heart n, padj<0.05 [workflow_default] | Heart P<0.05 (audit) |
|---|---|---|---|---|
| ANT1_EX_vs_SED | 711 (370/341) | 0 | 0 | 621 |
| ND5_EX_vs_SED | 3300 (153/3147) | 0 | 0 | 623 |
| ND6_EX_vs_SED | 1220 (816/404) | 0 | 0 | 2481 |
| CO1_EX_vs_SED | 1230 (516/714) | 0 | 0 | 1278 |
| *_filtered (sensitivity, CPM≥1 in ≥6) | ANT1 150, ND5 2039 (67/1972), ND6 389, CO1 572 | 0 | 0 | ANT1 145, ND5 49, ND6 1444, CO1 538 |

Paper's counts: none in the main text, so a numeric comparison is not possible.

Qualitative check against the soleus text (S1.2.x):
- **ND5 has the largest response**, which matches "strongest transcriptional response". The response is mostly **down-regulation**, and Hallmark OXPHOS is not significant. That does not show the "induction of OxPhos/stress-r ... [3720 more characters]
