# Review packet B (the analysis' decisions): GSE233004

## Mechanical flags

- **unused_subject_like_column**: {"column": "description", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint4/trt_EX_vs_SED_sex-F | 1 | 1 | padj < 0.05 | 1 | 1 | 1 | 1 | 701 | 344 | 252 | 153 | 0.187 | 0.021 |
| joint4/trt_EX_vs_SED_sex-M | 22 | 26 | padj < 0.05 | 26 | 4 | 0 | 38 | 1220 | 320 | 161 | 320 | 0.19 | 0.037 |

## Samples per design level

### `trt`
- **EX** (6): GSM7400614 / FEX360; GSM7400615 / FEX361; GSM7400616 / FEX362; GSM7400620 / MEX363; GSM7400621 / MEX364; GSM7400622 / MEX365
- **SED** (6): GSM7400617 / FSE366; GSM7400618 / FSE367; GSM7400619 / FSE368; GSM7400623 / MSE369; GSM7400624 / MSE370; GSM7400625 / MSE371

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE233004"], "assay": "bulk RNA-seq, mouse left ventricle (S1.7.p1)", "organism": "Mouse (C57BL/6J, ABS.p2)", "factors": {"sex": ["female", "male"], "treatment": ["sedentary", "exercised (treadmill 6 wk)"]}, "sample_inclusion": "3 sedentary + 3 exercised LV per sex, n=12 (S1.7.p1, FIG6 legend)", "primary_estimand": "Effect of 6-week moderate treadmill endurance exercise on LV gene expression, estimated separately within each sex (exercised vs sedentary)", "planned_contrasts": ["Female EX vs Female Sed (FIG6B/C; S2.5.p2: 1 DEG, Ddx3y up in EX)", "Male EX vs Male Sed (FIG6B/D; S2.5.p2: 22 DEGs)", "Female vs Male within Sed (FIG7; 896 DEGs) and within EX (174 DEGs) -- sex comparisons, not exercise estimands"], "repeated_measure_unit": "none for RNA-seq (one heart per mouse)", "normalization": "DESeq2 default size factors (S1.8.p3)", "paper_method": "DESeq2 Wald test, BH-adjusted p (S1.8.p3), per-sex exercised vs sedentary comparison", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S1.8.p3 (Padj < 0.05; log2FC cutoff 0 for volcano/KEGG; 2 only for top-gene plots); FIG6 legend"}, "paper_results": {"female_EX_vs_Sed": 1, "male_EX_vs_Sed": 22, "Sed_F_vs_M": 896, "EX_F_vs_M": 174}, "paper_direction_convention": "log2FC = Sedentary minus Exercised (S1.7.p1); positive = up in Sed. Our tables use EX vs SED (positive = up in EX)."}

reasoning: Methods S1.7.p1 and S1.8.p3 define DESeq2 Wald + BH, padj<0.05; the DEG counts quoted in S2.5.p2 come from the volcano plots, whose log2FC cutoff is 0 (S1.8.p3). The exercise question is answered per sex in Figure 6; Figure 7 is sex-difference, not exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE233004\\GSE233004_countdata.csv.gz", "owned": true, "checks": ["Data availability S1.p1 names GSE233004", "GEO: Mus musculus heart, bulk tissue, WT, Exercise/Sedentary, treadmill 1 km/h 45 min/day 5 d/wk 6 wk", "12 samples = 3 per sex x treatment, matching S1.7.p1"], "accession": "GSE233004", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE233004\\GSE233004_metadata.csv"}

reasoning: Paper S1.p1 cites GSE233004; series design and n match the methods.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\aligned\\aligned_metadata.csv", "columns": {"sex": {"source": "title", "regex": "^([FM])(?:EX|SE)\\d+$"}, "trt": {"source": "title", "regex": "^[FM](EX|SE)\\d+$", "recode": {"EX": "EX", "SE": "SED"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\aligned\\design_metadata.csv", "sha256": "8323d421ff57dc6795135ecd4ad514eccb65a4e2e4f9bcccab7a2678b29f030a", "levels": {"sex": {"F": 6, "M": 6}, "trt": {"EX": 6, "SED": 6}}}}

reasoning: Matrix columns (FEX360...) equal metadata title exactly for 12/12. Sex and treatment are encoded in the title prefix and agree with the 'description' and 'treatment' characteristics.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\aligned\\aligned_matrix.csv", "sha256": "3ac275ad73d3f7fb3d48185e7e01008d2365cbd662249035ce74b0aa800a6ac1", "n_features": 55401, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3095729.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer, 0..3.1e6, library sizes 22-33M; GEO data_processing: STAR + featureCounts hit counts (gene_id). The paper's input to DESeq2 is the same counts.

### design (valid, not_started)

final: {"analysis_type": "one 4-group model (sex x treatment cells), per-sex EX vs SED contrasts", "design_column": "trt", "control": "SED", "treatment": "EX", "contrasts": [{"name": "trt_EX_vs_SED_sex-F", "control": "SED", "treatment": "EX", "role": "primary"}, {"name": "trt_EX_vs_SED_sex-M", "control": "SED", "treatment": "EX", "role": "primary"}], "formula": "~ cell (cell = sex x trt)", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: Paper FIG6 compares exercised with sedentary mice within each sex (n=3 vs 3), using DESeq2 (S1.7.p1, S1.8.p3). The paper does not say whether each sex was fitted separately; the standard DESeq2 workflow for a 4-group study is one model on all 12 samples (~ group) with per-sex contrasts. A first attempt with separate per-sex fits gave 24 (F) / 0 (M) DEGs against the paper's 1 / 22, while one 4-group model gives 1 / 26 and reproduces Ddx3y as the only female DEG, so the joint 4-group model is taken as the paper's route and the separate fits are kept as sensitivity.

rejected alternatives: [{"value": "separate DESeq2 fits per sex (6 samples each)", "reason_rejected": "gives 24/0 DEGs (F/M) and loses Ddx3y in females, inconsistent with the paper's 1/22; kept as sensitivity"}, {"value": "pooled EX vs SED across sexes", "reason_rejected": "paper reports exercise effects per sex (FIG6); pooled additive model kept only as exploratory"}, {"value": "Female vs Male within each treatment (FIG7)", "reason_rejected": "sex-difference contrast, not an exercise estimand; outside the request"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "sex", "disposition": "part of the 4-level cell factor; contrasts are within sex. Additive ~ sex + trt only in the exploratory pooled model"}], "design_check": {"formula_equivalent": "~ C(trt)", "n_samples": 12, "n_columns": 2, "columns": ["Intercept", "trt_SED"], "rank": 2, "full_rank": true, "residual_df": 10, "levels": {"trt": {"EX": 6, "SED": 6}}, "cells": [{"cell": ["EX"], "n": 6}, {"cell": ["SED"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "sex", "n_levels": 2, "status": "crossed", "crosstab": {"EX": {"F": 3, "M": 3}, "SED": {"F": 3, "M": 3}}}]}

reasoning: Independent animals, one LV each; no batch, lane or date recorded in GEO or the paper. Sex is balanced with treatment (3/3 in each sex), so it is not confounded.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, BH)", "formula": "~ cell (cell = sex x trt; 4 levels), contrasts F/EX vs F/SED and M/EX vs M/SED", "paper_route": {"method": "DESeq2 Wald + BH", "status": "reproduced"}, "deviations": ["pydeseq2 rather than R DESeq2; independent filtering/Cook's outlier handling may differ slightly", "paper does not state the fit layout; one 4-group model chosen (matches the paper's counts), separate per-sex fits run as sensitivity"]}

reasoning: Raw featureCounts counts support the paper's DESeq2 route directly.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 2.0, "inclusive": false}}

reasoning: S1.8.p3: Padj < 0.05, log2FC cutoff 0 for volcano/KEGG (the DEG counts). The |log2FC| > 2 rule applied only to the top-gene panels and is kept as a labelled audit rule.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint4", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\joint4\\DEG_results_trt_EX_vs_SED_sex-F.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\joint4\\DEG_results_trt_EX_vs_SED_sex-M.csv"], "counts": {"joint4/trt_EX_vs_SED_sex-F": {"applied": {"rule": "padj < 0.05", "n_tested": 33215, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 2", "n_tested": 33215, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}}, "joint4/trt_EX_vs_SED_sex-M": {"applied": {"rule": "padj < 0.05", "n_tested": 4230, "n_significant": 26, "n_up": 14, "n_down": 12, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 2", "n_tested": 4230, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paper route: one DESeq2 model on all 12 samples with the 4-level sex x treatment group; per-sex EX vs SED contrasts (FIG6).

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "sepfit_trt_EX_vs_SED_sex-F", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\sepfit_trt_EX_vs_SED_sex-F\\input\\matrix.csv", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\sepfit_trt_EX_vs_SED_sex-F\\DEG_results_EX_vs_SED.csv"], "counts": {"sepfit_trt_EX_vs_SED_sex-F": {"applied": {"rule": "padj < 0.05", "n_tested": 16874, "n_significant": 24, "n_up": 17, "n_down": 7, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 2", "n_tested": 16874, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: separate DESeq2 fit on this sex's 6 samples (~ trt); dispersion from 6 samples only.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "sepfit_trt_EX_vs_SED_sex-M", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\sepfit_trt_EX_vs_SED_sex-M\\input\\matrix.csv", "formula": "~ trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\sepfit_trt_EX_vs_SED_sex-M\\DEG_results_EX_vs_SED.csv"], "counts": {"sepfit_trt_EX_vs_SED_sex-M": {"applied": {"rule": "padj < 0.05", "n_tested": 29958, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 2", "n_tested": 29958, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: separate DESeq2 fit on this sex's 6 samples (~ trt); dispersion from 6 samples only.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "trt_EX_vs_SED_pooled_sexadj", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\aligned\\aligned_matrix.csv", "formula": "~ sex + trt", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\trt_EX_vs_SED_pooled_sexadj\\DEG_results_EX_vs_SED.csv"], "counts": {"trt_EX_vs_SED_pooled_sexadj": {"applied": {"rule": "padj < 0.05", "n_tested": 33161, "n_significant": 2, "n_up": 2, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 2", "n_tested": 33161, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Not in the paper: pooled exercise main effect adjusted for sex (~ sex + trt), all 12 samples

### enrichment (valid, failed)

final: {"organism": "Mouse", "subset": "joint4/trt_EX_vs_SED_sex-F", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "execution_error": "Only 1 valid genes after filtering / ID conversion. Enrichment requires at least ~5 genes for meaningful results."}

reasoning: paper reports KEGG pathways per sex (FIG6E/F)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint4/trt_EX_vs_SED_sex-F", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\enrichment_joint4_trt_EX_vs_SED_sex-F\\gsea\\DEG_results_trt_EX_vs_SED_sex-F_GSEA_Hallmark.csv"], "summary": "GSEA complete on 32258 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 33 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.17 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.90 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.67 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.43 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=2.00 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.89 | NOM p=0.00e+00 | FDR q=2.49e-04 - HALLMARK_BILE_ACID_METABOLISM | NES=1.85 | NOM p=0.00e+00 | FDR q=2.18e-04 - HALLMARK_PEROXISOME | NES=1.79 | NOM p=0.00e+00 | FDR q=5.81e-04 - HALLMARK_UV_RESPONSE_UP | NES=1.78 | NOM p=0.00e+00 | FDR q=5.23e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-1.82 | NOM p=0.00e+00 | FDR q=1.35e-03 - HALLMARK_MITOTIC_SPINDLE | NE ... [417 more characters]

reasoning: paper reports KEGG pathways per sex (FIG6E/F)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint4/trt_EX_vs_SED_sex-M", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\enrichment_joint4_trt_EX_vs_SED_sex-M\\ora\\DEG_results_trt_EX_vs_SED_sex-M_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\enrichment_joint4_trt_EX_vs_SED_sex-M\\ora\\DEG_results_trt_EX_vs_SED_sex-M_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\enrichment_joint4_trt_EX_vs_SED_sex-M\\ora\\DEG_results_trt_EX_vs_SED_sex-M_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\enrichment_joint4_trt_EX_vs_SED_sex-M\\ora\\DEG_results_trt_EX_vs_SED_sex-M_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 26 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Respiration (GO:0045333) | padj=1.34e-03 | overlap=4/85 | gen ... [1270 more characters]

reasoning: paper reports KEGG pathways per sex (FIG6E/F); oxidative phosphorylation enriched

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint4/trt_EX_vs_SED_sex-M", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38686869\\GSE233004\\results\\enrichment_joint4_trt_EX_vs_SED_sex-M\\gsea\\DEG_results_trt_EX_vs_SED_sex-M_GSEA_Hallmark.csv"], "summary": "GSEA complete on 32258 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 43 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.86 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_P53_PATHWAY | NES=2.34 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_UP | NES=2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.13 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APOPTOSIS | NES=1.98 | NOM p=0.00e+00 | FDR q=2.06e-04 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.96 | NOM p=0.00e+00 | FDR q=1.83e-04 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.94 | NOM p=0.00e+00 | FDR q=1.65e-04 ### Top 4 DOWN (NES < 0, depleted in treatment): - HALLMARK_PROTEIN_SECRETION | NES=-1.30 | NOM p=5.75e-02 | FDR q=1.75e-01 - HALLMARK_MYOGENESIS | NES=-1.21 | NO ... [393 more characters]

reasoning: paper reports KEGG pathways per sex (FIG6E/F); oxidative phosphorylation enriched

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper's log2FC sign is Sed minus EX; ours is EX minus Sed.", "Ddx3y (Y-linked) reported up in exercised females; female samples carry low Ddx3y counts (FEX 14-26 vs FSE 0-5) while Xist is uniformly high in females, so this looks like low-level male-read contamination or cross-mapping, not a sex mislabel."], "results": {"joint4/trt_EX_vs_SED_sex-F": {"n_deg": 1, "up": 1, "down": 0, "rule": "padj < 0.05", "audit_n": 1}, "joint4/trt_EX_vs_SED_sex-M": {"n_deg": 26, "up": 14, "down": 12, "rule": "padj < 0.05", "audit_n": 0}, "sepfit_trt_EX_vs_SED_sex-F": {"n_deg": 24, "up": 17, "down": 7, "rule": "padj < 0.05", "audit_n": 0}, "sepfit_trt_EX_vs_SED_sex-M": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 0}, "trt_EX_vs_SED_pooled_sexadj": {"n_deg": 2, "up": 2, "down": 0, "rule": "padj < 0.05", "audit_n": 0}}, "paper_counts": {"joint4/trt_EX_vs_SED_sex-F": 1, "joint4/trt_EX_vs_SED_sex-M": 22}, "comparison": {"joint4/trt_EX_vs_SED_sex-F": {"ours": 1, "paper": 1}, "joint4/trt_EX_vs_SED_sex-M": {"ours": 26, "paper": 22}}, "paper_gene_check": {"joint4/trt_EX_vs_SED_sex-F": {"Ddx3y": {"baseMean": 1065.1781, "log2FoldChange": 3.1518, "padj": 0.0181, "pvalue": 5.44e-07}}, "joint4/trt_EX_vs_SED_sex-M": {"Gpx1": {"baseMean": 1320.3347, "log2FoldChange": 0.3901, "padj": 0.0287, "pvalue": 6.11e-05}, "Mtmr14": {"baseMean": 529.1456, "log2FoldChange": 0.4381, "padj": null, "pvalue": 1.47e-05}, "Mrps24": {"baseMean": 1508.4056, "log2FoldCh ... [240 more characters]

reasoning: Counts and named genes from S2.5.p2 and FIG6.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |
- | trt_EX_vs_SED_sex-F | simple | F/EX (3), F/SED (3) | yes |
- | trt_EX_vs_SED_sex-M | simple | M/EX (3), M/SED (3) | yes |

## Recorded paper-data discrepancies

[
  {
    "item": "log2FC direction",
    "paper": "Sedentary minus Exercised (S1.7.p1)",
    "data": "our tables report EX vs SED",
    "disposition": "executable_without_change"
  },
  {
    "item": "Ddx3y in female samples",
    "paper": "only DEG in females, up in EX; attributed to probe cross-reactivity (S2.5.p2)",
    "data": "female Ddx3y counts 14-26 (EX) vs 0-5 (SED); males ~1700-2300; Xist high only in females",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID38686869 / GSE233004

Paper: Moderate Endurance Exercise Increases Arrhythmia Susceptibility and Modulates Cardiac Structure and Function in a Sexually Dimorphic Manner (PMC11179941).
Status: **finished**. The case spec ran with all gates `valid` and execution `completed`. The contract validator reported 0 errors on 17 records.

## What ran

- **Data.** Bulk RNA-seq of mouse left ventricle. The matrix is `GSE233004_countdata.csv.gz`: 55,401 Ensembl genes x 12 samples of integer STAR + featureCounts counts. The design is 3 sedentary (SED) and 3 exercised (EX) mice per sex; exercise was 6 weeks of treadmill running.
- **Alignment.** Matrix columns match the GEO `title` exactly (12/12). Sex and treatment come from the title prefixes (`FEX`, `FSE`, `MEX`, `MSE`).
- **Sex check.** The X/Y-gene check passed. Xist is high only in females, and Ddx3y, Eif2s3y and Uty are high only in males.
- **Paper route.** The paper used DESeq2 Wald with BH correction and reports DEGs at padj < 0.05 with no fold-change cutoff for the volcano/KEGG counts (S1.8.p3). It compares exercised with sedentary mice within each sex (FIG6).
- **Primary analysis (`joint4`).** One pydeseq2 model on all 12 samples with a 4-level sex x treatment cell (`~ cell`). Two contrasts were extracted from it: F/EX vs F/SED and M/EX vs M/SED.
- **Sensitivity analysis (`sepfit_*`).** Separate DESeq2 fits per sex, 6 samples each (`~ trt`).
- **Exploratory analysis (`trt_EX_vs_SED_pooled_sexadj`).** A pooled `~ sex + trt` model for the exercise main effect. The paper does not report this.
- **Enrichment.** On the `joint4` tables: ORA (Enrichr GO + KEGG 2019 Mouse) and GSEA (Hallmark, ranked by `stat`).

## DEG counts vs the paper (threshold padj < 0.05, no log2FC cutoff; source S1.8.p3)

| Contrast | Ours (joint4, primary) | Paper (S2.5.p2) | Separate fit (sensitivity) |
|---|---|---|---|
| Female EX vs SED | 1 (1 up) | 1 | 24 (17 up / 7 down) |
| Male EX vs SED | 26 (14 up / 12 down) | 22 | 0 |
| Pooled, sex-adjusted (exploratory) | 2 | n/a | n/a |

- **Female.** As in the paper, the only female DEG is Ddx3y, up in EX (padj 0.018).
- **Male.** Of the 5 male genes the paper names, Gpx1, Mrps24, Klf2 and Fth1 pass padj < 0.05, all up in EX. Mtmr14 has p = 1.5e-5 but padj = NA: pydeseq2's outlier/filtering step dropped it.
- **Labelled audit rule (padj < 0.05 and |log2FC| > 2, the paper's top-gene rule).** Female 1 (Ddx3y), male 0.
- **Pathways.**
  - Both sexes are enriched for oxidative phosp ... [2624 more characters]
