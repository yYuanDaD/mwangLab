# Review packet B (the analysis' decisions): GSE198229_soleus

## Mechanical flags

- none

## Samples per design level

### `trt`
- **EX** (24): GSM5944754 / A13 [soleus muscle, ANT1-/-]; GSM5944755 / A17 [soleus muscle, ANT1-/-]; GSM5944757 / A30 [soleus muscle, ANT1-/-]; GSM5944758 / A43 [soleus muscle, ANT1-/-]; GSM5944761 / A76 [soleus muscle, ANT1-/-]; GSM5944762 / A81 [soleus muscle, ANT1-/-]; GSM5944766 / B4 [soleus muscle, ND5S204F]; GSM5944767 / B9 [soleus muscle, ND5S204F]; GSM5944769 / B11 [soleus muscle, ND5S204F]; GSM5944772 / B69 [soleus muscle, ND5S204F]; GSM5944774 / B80 [soleus muscle, ND5S204F]; GSM5944776 / B98 [soleus muscle, ND5S204F]; GSM5944777 / E1 [soleus muscle, CO1V421A]; GSM5944779 / E12 [soleus muscle, CO1V421A]; GSM5944781 / E50 [soleus muscle, CO1V421A]; GSM5944783 / E56 [soleus muscle, CO1V421A]; GSM5944785 / E76 [soleus muscle, CO1V421A]; GSM5944786 / E78 [soleus muscle, CO1V421A]; GSM5944791 / I50 [soleus muscle, ND6P25L]; GSM5944792 / I59 [soleus muscle, ND6P25L]; GSM5944794 / I63 [soleus muscle, ND6P25L]; GSM5944795 / I75 [soleus muscle, ND6P25L]; GSM5944796 / I84 [soleus muscle, ND6P25L]; GSM5944798 / I94 [soleus muscle, ND6P25L]
- **SED** (24): GSM5944753 / A4 [soleus muscle, ANT1-/-]; GSM5944756 / A18 [soleus muscle, ANT1-/-]; GSM5944759 / A58 [soleus muscle, ANT1-/-]; GSM5944760 / A75 [soleus muscle, ANT1-/-]; GSM5944763 / A82 [soleus muscle, ANT1-/-]; GSM5944764 / A88 [soleus muscle, ANT1-/-]; GSM5944765 / B3 [soleus muscle, ND5S204F]; GSM5944768 / B10 [soleus muscle, ND5S204F]; GSM5944770 / B19 [soleus muscle, ND5S204F]; GSM5944771 / B47 [soleus muscle, ND5S204F]; GSM5944773 / B70 [soleus muscle, ND5S204F]; GSM5944775 / B85 [soleus muscle, ND5S204F]; GSM5944778 / E7 [soleus muscle, CO1V421A]; GSM5944780 / E42 [soleus muscle, CO1V421A]; GSM5944782 / E53 [soleus muscle, CO1V421A]; GSM5944784 / E64 [soleus muscle, CO1V421A]; GSM5944787 / E98 [soleus muscle, CO1V421A]; GSM5944788 / E100 [soleus muscle, CO1V421A]; GSM5944789 / I13 [soleus muscle, ND6P25L]; GSM5944790 / I18 [soleus muscle, ND6P25L]; GSM5944793 / I62 [soleus muscle, ND6P25L]; GSM5944797 / I85 [soleus muscle, ND6P25L]; GSM5944799 / I95 [soleus muscle, ND6P25L]; GSM5944800 / I100 [soleus muscle, ND6P25L]

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE198229"], "assay": "bulk poly-A RNA-seq, STAR + RSEM expected counts (mm10, Gencode M17)", "tissue": "soleus muscle", "factors": {"strain": ["B6 control", "ND5S204F", "ND6P25L", "CO1V421A", "ANT1-/-"], "treatment": ["exercised (8 wk treadmill, every 2nd day, 45 min at 50% max)", "non-exercised (handled)"]}, "sample_inclusion": "60 soleus muscle samples: per strain 6 non-exercised + 6 exercised (3 responders + 3 non-responders) (S3.8.1.p1)", "primary_estimand": "effect of 8-wk endurance exercise training on gene expression, exercised vs non-exercised within each strain", "planned_contrasts": ["B6 exercised vs non-exercised (S3.8.1.p3)", "ANT1 exercised vs non-exercised (S3.8.1.p3)", "ND5 exercised vs non-exercised (S3.8.1.p3)", "ND6 exercised vs non-exercised (S3.8.1.p3)", "CO1 exercised vs non-exercised (S3.8.1.p3)"], "repeated_measure_unit": "none: one sample per mouse per tissue; independent mice", "normalization": "voom on RSEM expected counts", "paper_method": "limma-voom, exercised vs non-exercised within each strain", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "S3.8.1.p3"}, "paper_results": "Soleus (S1.2.1.p1, S1.2.2.p1, S1.2.3.p1, S1.2.4.p1, S1.2.5.p1): B6 no major differences except modest IFN-gamma signaling up; ND5 strongest transcriptional response (OxPhos and stress-response genes up); ND6 no induction of mitochondrial genes; CO1 only a  ... [131 more characters]

reasoning: Methods S3.8.1.p3 describe within-strain exercised vs non-exercised limma-voom on RSEM expected counts; S3.8.1.p1 gives the sample design; DA.p1 deposits GSE198229.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE198229\\GSE198229_skeletal_muscle_expected_counts_matrix.tsv.gz", "owned": true, "checks": ["DA.p1 and S3.8.2.p7 name GSE198229", "matrix GSE198229_skeletal_muscle_expected_counts_matrix.tsv.gz has 60 columns matching the 60 soleus muscle samples (48 by animal ID; 12 B6 columns are numbered)", "strain x treatment counts in GEO (6/6 per strain) match S3.8.1.p1/S3.8.2.p1"], "accession": "GSE198229", "metadata_file": "E:/agent/mwangLab_pdf/test/experiments/large_run_pilot_20261019/runs_claude/PMID35482926/prep/GSE198229_soleus_metadata.csv"}

reasoning: Paper's own deposit; tissue-specific matrix.

### alignment (valid, not_started)

final: {"method": "exact:animal", "n_aligned": 48, "n_metadata": 60, "coverage": 0.8, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM5944801", "GSM5944802", "GSM5944803", "GSM5944804", "GSM5944805", "GSM5944806", "GSM5944807", "GSM5944808", "GSM5944809", "GSM5944810", "GSM5944811", "GSM5944812"], "excluded_samples": {"N2": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N5": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N63": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N65": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N66": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N8": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N1": "B6 control: matrix columns for B6 are bare numbers (25-48) and no GEO field maps them to the N-IDs in the sample titles; positional alignment is not allowed", "N6 ... [1585 more characters]

reasoning: Matrix columns are animal IDs (A76, B9, E42, I50); metadata per tissue was split by a prep script and the ID parsed from title (e.g. 'A76 [heart, ANT1-/-]'). Exact match for ANT1/ND5/ND6/CO1 (48/48). The 12 B6 columns are numbers (25-36 soleus, 37-48 heart) while GEO titles are N1..N69; nothing links them, so the B6 samples are excluded and the numeric columns dropped by matrix_column_pattern. The B6 contrast cannot be run (manual_review: needs the submitter number-to-N-ID map).

### matrix (valid, not_started)

final: {"source": "GSE198229_skeletal_muscle_expected_counts_matrix.tsv.gz", "paper_input": "RSEM expected counts (S3.8.1.p1, S3.8.1.p3)", "matrix_type": "estimated counts", "recommended_method": "limma-voom", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\aligned\\aligned_matrix.csv", "sha256": "ca0b5781bb58a4b87e7b6192f7d4b31b583d8bbf17e2b321fa1fd3bf982ee70d", "n_features": 53656, "n_samples": 48, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3082723.68, "median": 0.0, "integer_fraction": 0.9418, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name 'expected_counts', ~94% integer values with fractional remainder, max ~3e6, data_processing: STAR --quantMode TranscriptomeSAM + RSEM. These are RSEM expected counts, the input the paper fed to voom. The sibling fpkm file is not used.

### design (valid, not_started)

final: {"analysis_type": "two-group within each strain stratum", "design_column": "trt", "control": "SED", "treatment": "EX", "contrasts": [{"name": "trt_EX_vs_SED_strain-ANT1", "control": "SED", "treatment": "EX", "role": "primary"}, {"name": "trt_EX_vs_SED_strain-ND5", "control": "SED", "treatment": "EX", "role": "primary"}, {"name": "trt_EX_vs_SED_strain-ND6", "control": "SED", "treatment": "EX", "role": "primary"}, {"name": "trt_EX_vs_SED_strain-CO1", "control": "SED", "treatment": "EX", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\suitability\\suitability.md", "n_comparisons": 4, "n_analyzable": 4}}

reasoning: S3.8.1.p3: 'comparing each gene in the exercise-trained vs. the non-exercise-trained group within each strain'. Strain is a stratum: each strain fitted separately as in the paper. Responder/non-responder status (soleus only) splits the exercised arm by outcome; the paper pools both into the exercised group, so it is not a factor. Between-strain comparisons are baseline genotype questions, not the exercise estimand, and are not run.

rejected alternatives: [{"value": "joint model ~ strain*trt on all samples", "reason_rejected": "paper fits within strain; per-strain fit reproduces its variance estimate"}, {"value": "responders vs non-responders", "reason_rejected": "outcome-defined split of the exercised arm, not the exercise effect; n=3 vs 3"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "exercise response", "disposition": "not used: defined only within the exercised arm (aliased with trt), outcome-based"}], "design_check": {"formula_equivalent": "~ C(trt)", "n_samples": 48, "n_columns": 2, "columns": ["Intercept", "trt_SED"], "rank": 2, "full_rank": true, "residual_df": 46, "levels": {"trt": {"SED": 24, "EX": 24}}, "cells": [{"cell": ["EX"], "n": 24}, {"cell": ["SED"], "n": 24}], "min_cell_size": 24, "missing_values": {}}, "confounding": []}

reasoning: Independent mice, one sample per mouse per tissue; no batch or lane recorded. Exercise response is nested in the exercised arm and cannot be a covariate.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "limma-voom (R limma::voom + eBayes, library size = column sums)", "formula": "~ trt", "rounding_documented": true, "paper_route": {"method": "limma-voom on RSEM expected counts", "status": "reproduced"}, "deviations": ["expected counts rounded to integers before voom (the tool requires integers; the paper passed non-integer expected counts)", "no TMM normalization factors (tool uses column-sum library sizes; paper normalization factors unknown)", "genes with zero counts in all 12 samples dropped by the tool (paper reports 58,581 tested; matrix has 53,656 rows)"], "transform": "round"}

reasoning: S3.8.1.p3: voom on RSEM expected counts then limma. The repository limma-voom executor runs R limma::voom.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "S3.8.1.p3"}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S3.8.1.p3: the gene list for exercised vs non-exercised within each strain (Metascape input) used nominal P < 0.05; no fold-change rule. No other DEG cut-off is stated. BH padj < 0.05 is reported as a labelled audit rule.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ANT1_EX_vs_SED", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ANT1_EX_vs_SED\\input\\matrix.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ANT1_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"ANT1_EX_vs_SED": {"applied": {"rule": "pvalue < 0.05", "n_tested": 23999, "n_significant": 711, "n_up": 370, "n_down": 341, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 23999, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: ANT1 exercised vs non-exercised, limma-voom (S3.8.1.p3)

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ND5_EX_vs_SED", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ND5_EX_vs_SED\\input\\matrix.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ND5_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"ND5_EX_vs_SED": {"applied": {"rule": "pvalue < 0.05", "n_tested": 25504, "n_significant": 3300, "n_up": 153, "n_down": 3147, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 25504, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: ND5 exercised vs non-exercised, limma-voom (S3.8.1.p3)

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ND6_EX_vs_SED", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ND6_EX_vs_SED\\input\\matrix.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ND6_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"ND6_EX_vs_SED": {"applied": {"rule": "pvalue < 0.05", "n_tested": 25279, "n_significant": 1220, "n_up": 816, "n_down": 404, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 25279, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: ND6 exercised vs non-exercised, limma-voom (S3.8.1.p3)

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "CO1_EX_vs_SED", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\CO1_EX_vs_SED\\input\\matrix.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\CO1_EX_vs_SED\\DEG_results_EX_vs_SED.csv"], "counts": {"CO1_EX_vs_SED": {"applied": {"rule": "pvalue < 0.05", "n_tested": 25008, "n_significant": 1230, "n_up": 516, "n_down": 714, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 25008, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: CO1 exercised vs non-exercised, limma-voom (S3.8.1.p3)

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ANT1_EX_vs_SED_filtered", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ANT1_EX_vs_SED_filtered\\input\\rounded_counts.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ANT1_EX_vs_SED_filtered\\DEG_results_EX_vs_SED.csv"], "counts": {"ANT1_EX_vs_SED_filtered": {"applied": {"rule": "pvalue < 0.05", "n_tested": 11444, "n_significant": 150, "n_up": 99, "n_down": 51, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 11444, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: the paper tested all genes without a low-count filter; in the unfiltered fit hundreds of genes detected in 1-2 samples share identical t statistics and dominate the nominal-P counts. Keep genes with CPM >= 1 in >= 6 samples (the arm size) as in the usual voom workflow.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ND5_EX_vs_SED_filtered", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ND5_EX_vs_SED_filtered\\input\\rounded_counts.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ND5_EX_vs_SED_filtered\\DEG_results_EX_vs_SED.csv"], "counts": {"ND5_EX_vs_SED_filtered": {"applied": {"rule": "pvalue < 0.05", "n_tested": 12606, "n_significant": 2039, "n_up": 67, "n_down": 1972, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12606, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: the paper tested all genes without a low-count filter; in the unfiltered fit hundreds of genes detected in 1-2 samples share identical t statistics and dominate the nominal-P counts. Keep genes with CPM >= 1 in >= 6 samples (the arm size) as in the usual voom workflow.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "ND6_EX_vs_SED_filtered", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ND6_EX_vs_SED_filtered\\input\\rounded_counts.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\ND6_EX_vs_SED_filtered\\DEG_results_EX_vs_SED.csv"], "counts": {"ND6_EX_vs_SED_filtered": {"applied": {"rule": "pvalue < 0.05", "n_tested": 12300, "n_significant": 389, "n_up": 156, "n_down": 233, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12300, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: the paper tested all genes without a low-count filter; in the unfiltered fit hundreds of genes detected in 1-2 samples share identical t statistics and dominate the nominal-P counts. Keep genes with CPM >= 1 in >= 6 samples (the arm size) as in the usual voom workflow.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "CO1_EX_vs_SED_filtered", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\CO1_EX_vs_SED_filtered\\input\\rounded_counts.csv", "transform": "round", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\CO1_EX_vs_SED_filtered\\DEG_results_EX_vs_SED.csv"], "counts": {"CO1_EX_vs_SED_filtered": {"applied": {"rule": "pvalue < 0.05", "n_tested": 12344, "n_significant": 572, "n_up": 55, "n_down": 517, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12344, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: the paper tested all genes without a low-count filter; in the unfiltered fit hundreds of genes detected in 1-2 samples share identical t statistics and dominate the nominal-P counts. Keep genes with CPM >= 1 in >= 6 samples (the arm size) as in the usual voom workflow.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ANT1_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\enrichment_ANT1_EX_vs_SED\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 23999 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 15 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PROTEIN_SECRETION | NES=1.94 | NOM p=0.00e+00 | FDR q=5.54e-03 - HALLMARK_MYC_TARGETS_V1 | NES=1.68 | NOM p=0.00e+00 | FDR q=2.08e-02 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.60 | NOM p=5.30e-03 | FDR q=2.68e-02 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.51 | NOM p=0.00e+00 | FDR q=5.54e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.42 | NOM p=3.73e-02 | FDR q=1.17e-01 - HALLMARK_DNA_REPAIR | NES=1.41 | NOM p=2.30e-02 | FDR q=1.05e-01 - HALLMARK_PI3K_AKT_MTOR_SIGNALING | NES=1.37 | NOM p=4.78e-02 | FDR q=1.26e-01 - HALLMARK_MTORC1_SIGNALING | NES=1.37 | NOM p=1.59e-02 | FDR q=1.20e-01 - HALLMARK_ADIPOGENESIS | NES=1.37 | NOM p=1.83e-02 | FDR q=1.06e-01 - HALLMARK_HEME_METABOLISM | NES=1.31 | NOM p=3.99e-02 | FDR q=1.55e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-1.87 | NOM p=0.00e+00 | FDR q=4.39e-03 - HALLMARK_HYPOXIA | NES=-1.38 | NOM p=9.03e-03 | FDR q=3.52e-01 - HALLMARK_EPITHEL ... [389 more characters]

reasoning: paper ran GSEA (Hallmark + C2 CP) on each within-strain exercise contrast (S3.8.1.p3); Hallmark only here

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ND5_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\enrichment_ND5_EX_vs_SED\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25504 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 23 significant at FDR q < 0.25. ### Top 6 UP (NES > 0, enriched in treatment): - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.37 | NOM p=7.14e-02 | FDR q=2.14e-01 - HALLMARK_MYC_TARGETS_V2 | NES=1.12 | NOM p=2.50e-01 | FDR q=7.29e-01 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.00 | NOM p=1.00e+00 | FDR q=4.71e-01 - HALLMARK_ADIPOGENESIS | NES=1.00 | NOM p=1.00e+00 | FDR q=4.71e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=1.00 | NOM p=1.00e+00 | FDR q=4.71e-01 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.00 | NOM p=1.00e+00 | FDR q=4.71e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-1.83 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=-1.70 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=-1.60 | NOM p=0.00e+00 | FDR q=3.53e-03 - HALLMARK_APICAL_JUNCTION | NES=-1.52 | NOM p=0.00e+00 | FDR q=1.19e-02 - HALLMARK_PROTEIN_SECRETION | NES=-1.51 | NOM p=0.00e+00 | FDR q=1.11e-02 - HALLMARK_MITOTIC_SPINDLE | NES=-1.46 | NOM p=0.00e+00 | FDR q ... [391 more characters]

reasoning: paper ran GSEA (Hallmark + C2 CP) on each within-strain exercise contrast (S3.8.1.p3); Hallmark only here

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ND6_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\enrichment_ND6_EX_vs_SED\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25279 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 2 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.66 | NOM p=0.00e+00 | FDR q=3.42e-02 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.39 | NOM p=2.05e-02 | FDR q=3.91e-01 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.36 | NOM p=1.81e-02 | FDR q=3.97e-01 - HALLMARK_MTORC1_SIGNALING | NES=1.30 | NOM p=4.96e-02 | FDR q=5.16e-01 - HALLMARK_G2M_CHECKPOINT | NES=1.22 | NOM p=1.04e-01 | FDR q=8.07e-01 - HALLMARK_E2F_TARGETS | NES=1.22 | NOM p=9.57e-02 | FDR q=7.05e-01 - HALLMARK_APOPTOSIS | NES=1.18 | NOM p=1.78e-01 | FDR q=8.29e-01 - HALLMARK_COAGULATION | NES=1.14 | NOM p=2.28e-01 | FDR q=9.15e-01 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.14 | NOM p=1.70e-01 | FDR q=8.26e-01 - HALLMARK_COMPLEMENT | NES=1.14 | NOM p=2.07e-01 | FDR q=7.44e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_UV_RESPONSE_DN | NES=-1.44 | NOM p=0.00e+00 | FDR q=2.34e-01 - HALLMARK_MYOGENESIS | NES=-1.24 | NOM p=5.56e-02 | FDR q=6.17e-01 - HALLMARK_BILE_ACID_METABOLISM ... [387 more characters]

reasoning: paper ran GSEA (Hallmark + C2 CP) on each within-strain exercise contrast (S3.8.1.p3); Hallmark only here

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "CO1_EX_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\enrichment_CO1_EX_vs_SED\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25008 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 33 significant at FDR q < 0.25. ### Top 4 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.15 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=0.97 | NOM p=5.11e-01 | FDR q=1.00e+00 - HALLMARK_SPERMATOGENESIS | NES=0.91 | NOM p=6.63e-01 | FDR q=9.19e-01 - HALLMARK_FATTY_ACID_METABOLISM | NES=0.89 | NOM p=7.38e-01 | FDR q=7.33e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_DNA_REPAIR | NES=-2.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=-2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=-2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PROTEIN_SECRETION | NES=-2.03 | NOM p=0.00e+00 | FDR q=3.54e-04 - HALLMARK_UV_RESPONSE_DN | NES=-1.99 | NOM p=0.00e+00 | FDR q=2.83e-04 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-1.97 | NOM p=0.00e+00 | FDR q=2.36e-04 - HALLMARK_MITOTIC_SPINDLE | NES=-1.89 | NOM p=0.00e+00 | FDR q=6.07e-04 - HALLMARK_P53_PATHWAY | NES=-1.86 | NOM p=0.00e+00 | FDR q=1.06e-03 - HA ... [332 more characters]

reasoning: paper ran GSEA (Hallmark + C2 CP) on each within-strain exercise contrast (S3.8.1.p3); Hallmark only here

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ANT1_EX_vs_SED_filtered", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\enrichment_ANT1_EX_vs_SED_filtered\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 11444 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 17 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PROTEIN_SECRETION | NES=1.60 | NOM p=5.51e-03 | FDR q=9.02e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.43 | NOM p=3.49e-02 | FDR q=3.10e-01 - HALLMARK_MTORC1_SIGNALING | NES=1.19 | NOM p=1.49e-01 | FDR q=1.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.19 | NOM p=1.56e-01 | FDR q=1.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.18 | NOM p=1.90e-01 | FDR q=1.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=1.17 | NOM p=1.59e-01 | FDR q=8.94e-01 - HALLMARK_PI3K_AKT_MTOR_SIGNALING | NES=1.14 | NOM p=2.33e-01 | FDR q=9.27e-01 - HALLMARK_DNA_REPAIR | NES=1.13 | NOM p=2.46e-01 | FDR q=8.82e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=1.08 | NOM p=3.39e-01 | FDR q=9.95e-01 - HALLMARK_G2M_CHECKPOINT | NES=1.08 | NOM p=3.18e-01 | FDR q=9.11e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-2.77 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=-2.15 | NOM p=0.00e+00 | FDR q=0.00e+ ... [407 more characters]

reasoning: GSEA on the filtered ranking: tied low-count statistics distort the unfiltered ranking

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ND5_EX_vs_SED_filtered", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\enrichment_ND5_EX_vs_SED_filtered\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12606 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 16 significant at FDR q < 0.25. ### Top 6 UP (NES > 0, enriched in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=1.54 | NOM p=0.00e+00 | FDR q=1.14e-01 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.42 | NOM p=1.25e-01 | FDR q=1.52e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=1.42 | NOM p=0.00e+00 | FDR q=1.01e-01 - HALLMARK_ADIPOGENESIS | NES=1.00 | NOM p=1.00e+00 | FDR q=4.56e-01 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.00 | NOM p=1.00e+00 | FDR q=4.56e-01 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.00 | NOM p=1.00e+00 | FDR q=4.56e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-1.79 | NOM p=0.00e+00 | FDR q=8.80e-04 - HALLMARK_APICAL_JUNCTION | NES=-1.65 | NOM p=0.00e+00 | FDR q=4.40e-03 - HALLMARK_G2M_CHECKPOINT | NES=-1.51 | NOM p=0.00e+00 | FDR q=2.58e-02 - HALLMARK_APICAL_SURFACE | NES=-1.45 | NOM p=2.35e-02 | FDR q=4.18e-02 - HALLMARK_PROTEIN_SECRETION | NES=-1.42 | NOM p=4.00e-03 | FDR q=4.98e-02 - HALLMARK_HEDGEHOG_SIGNALING | NES=-1.36  ... [408 more characters]

reasoning: GSEA on the filtered ranking: tied low-count statistics distort the unfiltered ranking

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "ND6_EX_vs_SED_filtered", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\enrichment_ND6_EX_vs_SED_filtered\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12300 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 23 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=1.77 | NOM p=0.00e+00 | FDR q=1.74e-02 - HALLMARK_COAGULATION | NES=1.77 | NOM p=0.00e+00 | FDR q=1.16e-02 - HALLMARK_APOPTOSIS | NES=1.61 | NOM p=0.00e+00 | FDR q=4.12e-02 - HALLMARK_MYC_TARGETS_V1 | NES=1.54 | NOM p=0.00e+00 | FDR q=6.47e-02 - HALLMARK_COMPLEMENT | NES=1.52 | NOM p=3.85e-03 | FDR q=6.15e-02 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.49 | NOM p=2.98e-02 | FDR q=7.43e-02 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.47 | NOM p=1.33e-02 | FDR q=7.65e-02 - HALLMARK_GLYCOLYSIS | NES=1.42 | NOM p=1.76e-02 | FDR q=1.04e-01 - HALLMARK_KRAS_SIGNALING_UP | NES=1.39 | NOM p=1.46e-02 | FDR q=1.23e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=-1.28 | NOM p=5.87e-02 | FDR q=8.08e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=-1.28 | NOM p=9.07e-02 | FDR q=4.25e-01 ... [405 more characters]

reasoning: GSEA on the filtered ranking: tied low-count statistics distort the unfiltered ranking

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "CO1_EX_vs_SED_filtered", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35482926\\GSE198229_soleus\\results\\enrichment_CO1_EX_vs_SED_filtered\\gsea\\DEG_results_EX_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12344 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 5 significant at FDR q < 0.25. ### Top 7 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.35 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.76 | NOM p=0.00e+00 | FDR q=9.85e-03 - HALLMARK_SPERMATOGENESIS | NES=1.21 | NOM p=1.92e-01 | FDR q=2.89e-01 - HALLMARK_ADIPOGENESIS | NES=1.00 | NOM p=1.00e+00 | FDR q=7.95e-01 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=0.99 | NOM p=4.09e-01 | FDR q=6.73e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=0.93 | NOM p=5.32e-01 | FDR q=7.06e-01 - HALLMARK_PEROXISOME | NES=0.78 | NOM p=7.27e-01 | FDR q=8.86e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_G2M_CHECKPOINT | NES=-1.46 | NOM p=2.01e-03 | FDR q=3.02e-01 - HALLMARK_PROTEIN_SECRETION | NES=-1.44 | NOM p=5.05e-03 | FDR q=1.83e-01 - HALLMARK_DNA_REPAIR | NES=-1.40 | NOM p=3.01e-03 | FDR q=2.01e-01 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=-1.38 | NOM p=1.51e-02 | FDR q=2.09e-01 - HALLMARK_UV_RESPONSE_DN | NES=-1.28 | NOM p=5.51e-02 | FDR q ... [405 more characters]

reasoning: GSEA on the filtered ranking: tied low-count statistics distort the unfiltered ranking

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["B6 control (wild-type) exercise contrast not run: B6 matrix columns cannot be mapped to GEO samples", "Paper reports no DEG counts in the main text; supplementary Datasets S1-S11 were not available, so comparison is qualitative only"], "results": {"ANT1_EX_vs_SED": {"n_deg": 711, "up": 370, "down": 341, "rule": "pvalue < 0.05", "audit_n": 0}, "ND5_EX_vs_SED": {"n_deg": 3300, "up": 153, "down": 3147, "rule": "pvalue < 0.05", "audit_n": 0}, "ND6_EX_vs_SED": {"n_deg": 1220, "up": 816, "down": 404, "rule": "pvalue < 0.05", "audit_n": 0}, "CO1_EX_vs_SED": {"n_deg": 1230, "up": 516, "down": 714, "rule": "pvalue < 0.05", "audit_n": 0}, "ANT1_EX_vs_SED_filtered": {"n_deg": 150, "up": 99, "down": 51, "rule": "pvalue < 0.05", "audit_n": 0}, "ND5_EX_vs_SED_filtered": {"n_deg": 2039, "up": 67, "down": 1972, "rule": "pvalue < 0.05", "audit_n": 0}, "ND6_EX_vs_SED_filtered": {"n_deg": 389, "up": 156, "down": 233, "rule": "pvalue < 0.05", "audit_n": 0}, "CO1_EX_vs_SED_filtered": {"n_deg": 572, "up": 55, "down": 517, "rule": "pvalue < 0.05", "audit_n": 0}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {}}

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
