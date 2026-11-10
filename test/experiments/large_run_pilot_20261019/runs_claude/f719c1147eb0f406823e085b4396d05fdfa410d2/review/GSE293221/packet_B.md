# Review packet B (the analysis' decisions): GSE293221

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.2.treatment", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 3, "samples_linked": 9, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_EX_vs_CON | 32 | 32 | padj < 0.05 and |log2FoldChange| > 0.584963 | 35 | 32 | 28 | 39 | 491 | 383 | 272 | 169 | 0.166 | 0.027 |
| joint/grp_PHAM_vs_CON | 176 | 3694 | padj < 0.05 and |log2FoldChange| > 0.584963 | 3875 | 3694 | 3090 | 5177 | 5894 | 5350 | 4101 | 3624 | 0.058 | 0.319 |
| twoarm_EX_vs_CON | 32 | 385 | padj < 0.05 and |log2FoldChange| > 0.584963 | 396 | 385 | 242 | 630 | 1879 | 1318 | 599 | 903 | 0.096 | 0.103 |

## Samples per design level

### `grp`
- **CON** (3): GSM8878836 / Control, rep1 / Library name: DP_MT_013; GSM8878837 / Control, rep2 / Library name: DP_MT_014; GSM8878838 / Control, rep3 / Library name: DP_MT_017
- **EX** (3): GSM8878839 / Exercise, rep1 / Library name: DP_MT_001; GSM8878840 / Exercise, rep2 / Library name: DP_MT_002; GSM8878841 / Exercise, rep3 / Library name: DP_MT_004
- **PHAM** (3): GSM8878842 / Nexrutine, rep1 / Library name: DP_MT_012; GSM8878843 / Nexrutine, rep2 / Library name: DP_MT_022; GSM8878844 / Nexrutine, rep3 / Library name: DP_MT_23b

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE293221"], "assay": "bulk RNA-seq (KAPA stranded RiboErase, HiSeq 3000 50bp SE), prostate tumor tissue of male TRAMP mice (S4.6.p1)", "sample_inclusion": "18 male TRAMP mice randomized 1:1:1 to control, exercise (voluntary wheel running, singly housed), Phellodendron amurense extract diet (S4.2.p1); 12-week intervention; tumors from 3 representative animals per group sequenced (S2.2.p1, S4.6.p1)", "factors": {"grp": ["control", "exercise", "Phellodendron amurense extract (Nexrutine)"]}, "primary_estimand": "Effect of 12 weeks of voluntary wheel running vs no intervention on prostate tumor gene expression in TRAMP mice (S2.2.p1)", "planned_contrasts": ["exercise vs control (S2.2.p1; paper: 32 DEGs)", "Phellodendron amurense extract vs control (S2.2.p2; paper: 176 DEGs, 100 down / 76 up)"], "repeated_measure_unit": "none; one tumor per animal, independent animals", "normalization": "DESeq size-factor normalization of HTSeq counts (S4.7.p1)", "paper_method": "R package DESeq (original), group-pairwise comparisons on HTSeq counts; TopHat to UCSC genome (S4.7.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false, "extra_filter": "at least one group average RPKM > 1", "source_locator": "S4.7.p1"}, "paper_results": {"exercise_vs_control": "32 DEGs; down: Lipe, Plin1, Slc7a10, Gpr83; up: Dgat2l6 (S2.2.p1, S3.p1)", "pham_vs_control": "176 DEGs (100 down, 76 up); down Spink3, Spink ... [156 more characters]

reasoning: S2.2.p1 and S4.6.p1: 3 tumors per group sequenced; S4.7.p1 gives method (DESeq, group-pairwise) and the three-part DEG rule (RPKM>1 in one group, FDR<0.05, FC>1.5 either way). Exercise vs control is the request's estimand; PhAm vs control is the paper's second planned contrast.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221_counts_gsm_shuffled.csv", "owned": true, "checks": ["DA.p1 names GSE293221", "GEO metadata: TRAMP C57BL/6 prostate tumor tissue, treatment column matches control/running wheel/Phellodendron extract arms of S4.2.p1", "9 samples = 3 per group as in S4.6.p1; HTSeq-count + TopHat mm9 in data_processing matches S4.7.p1"], "accession": "GSE293221", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE293221\\GSE293221_metadata.csv"}

reasoning: Accession, organism, tissue, arms, n and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(Control|Exercise|Nexrutine), rep\\d+$", "recode": {"Control": "CON", "Exercise": "EX", "Nexrutine": "PHAM"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\aligned\\design_metadata.csv", "sha256": "3eec5e7eef8b91c75da6dd520042db4d736a94fa2d5394b91b3806dd3018ceba", "levels": {"grp": {"CON": 3, "EX": 3, "PHAM": 3}}}}

reasoning: prep_matrix.py renames the merged HTSeq tar columns to their GSM ids (exact equal to the metadata index) and fixes row order (values unchanged); group from title (Control/Exercise/Nexrutine, rep1-3), consistent with the characteristics treatment column.

### matrix (valid, not_started)

final: {"source": "per-sample HTSeq-count files in GSE293221_RAW.tar merged by gene symbol (GSE293221_merged_from_tar.csv), columns renamed to GSM ids and rows reordered by prep_matrix.py", "paper_input": "HTSeq read counts into DESeq (S4.7.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\aligned\\aligned_matrix.csv", "sha256": "e3c48b766c3a04f91b127fc486d35f014928c42c1f344a0d247900fb0f30c9bd", "n_features": 22609, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1021924.0, "median": 61.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer fraction 1.0, median 61, max ~1e6, library sums 7.5-14M; data_processing states HTSeq-count read counts. Matches the paper's stated input.

### design (valid, not_started)

final: {"analysis_type": "multi-group, one model, pairwise contrasts against control", "design_column": "grp", "contrasts": [{"name": "grp_EX_vs_CON", "control": "CON", "treatment": "EX", "role": "primary"}, {"name": "grp_PHAM_vs_CON", "control": "CON", "treatment": "PHAM", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Three independent arms with one control (S4.2.p1); paper reports each intervention vs control (S2.2.p1, S2.2.p2). One model with planned contrasts; any other listed comparison is exploratory.

rejected alternatives: [{"value": "two separate two-arm fits (EX+CON only)", "reason_rejected": "paper's DESeq was run on all groups with group-pairwise tests; one model on all 9 samples shares dispersion as the original DESeq did"}, {"value": "pool EX and PHAM as 'intervention'", "reason_rejected": "different interventions; paper contrasts each with control"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 9, "n_columns": 3, "columns": ["Intercept", "grp_EX", "grp_PHAM"], "rank": 3, "full_rank": true, "residual_df": 6, "levels": {"grp": {"CON": 3, "EX": 3, "PHAM": 3}}, "cells": [{"cell": ["CON"], "n": 3}, {"cell": ["EX"], "n": 3}, {"cell": ["PHAM"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 9, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 9, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.mouse strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.treatment", "n_levels": 3, "status": "complete_confounding", "crosstab": {"CON": {"Control group without intervention": 3, "Mice  singularly housed and given access to a 15.5 cm diameter low-pro ... [2230 more characters]

reasoning: Independent animals, one tumor each; no batch, lane or pairing recorded in GEO or paper. Housing (single for EX, group for CON/PHAM, S4.2.p1/S4.3.p1) is part of the intervention and fully aliased with arm, so it cannot and should not be modelled.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald), one model ~ grp, contrasts vs CON", "formula": "~ grp", "paper_route": {"method": "DESeq (original Bioconductor DESeq, negative-binomial exact test, group-pairwise)", "status": "blocked", "reason": "no original-DESeq executor in this repository; DESeq2 is the validated successor on the same count input"}, "deviations": ["DESeq2 Wald test instead of original DESeq exact test", "paper's 'average RPKM > 1 in at least one group' filter not applied: no gene lengths in the deposit (gene-symbol HTSeq counts, mm9); DESeq2 independent filtering used instead; a CPM>=1 in >=3 samples low-count filter is run as a sensitivity analysis"]}

reasoning: Raw integer counts support the negative-binomial route; reproduce the paper's NB count model with DESeq2 as a declared deviation.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper rule FDR<0.05 and FC>1.5 either way (|log2FC|>log2(1.5)=0.5849625) applied on DESeq2; the RPKM>1 expression prefilter cannot be applied (no gene lengths)."}

reasoning: S4.7.p1: FDR adjusted p < 0.05 and fold change > 1.5 (either way); ABS.p1 says >= 1.5-fold, S4.7.p1 (methods) says > 1.5, methods wording used.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\joint\\DEG_results_grp_EX_vs_CON.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\joint\\DEG_results_grp_PHAM_vs_CON.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\joint\\DEG_results_grp_PHAM_vs_EX.csv"], "counts": {"joint/grp_EX_vs_CON": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 18475, "n_significant": 32, "n_up": 27, "n_down": 5, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 18475, "n_significant": 35, "n_up": 27, "n_down": 8, "deg_sanity": "ok"}}, "joint/grp_PHAM_vs_CON": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 15524, "n_significant": 3694, "n_up": 2644, "n_down": 1050, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15524, "n_significant": 3875, "n_up": 2712, "n_down": 1163, "deg_sanity": "ok"}}, "joint/grp_PHAM_vs_EX": {"applied": {"rule": "padj < 0.05 and |log2FoldChan ... [235 more characters]

reasoning: One DESeq2 model ~ grp on all 9 samples; planned EX vs CON (primary) and PHAM vs CON (secondary); any other listed comparison exploratory.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint_cpmfilter", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\joint_cpmfilter\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\joint_cpmfilter\\DEG_results_grp_EX_vs_CON.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\joint_cpmfilter\\DEG_results_grp_PHAM_vs_CON.csv"], "counts": {"joint_cpmfilter/grp_EX_vs_CON": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14218, "n_significant": 28, "n_up": 23, "n_down": 5, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14218, "n_significant": 31, "n_up": 23, "n_down": 8, "deg_sanity": "ok"}}, "joint_cpmfilter/grp_PHAM_vs_CON": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14218, "n_significant": 3399, "n_up": 2352, "n_down": 1047, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14218, "n_significant": 3584, "n_up": 2426, "n_down": 1158, "deg_sanity": "ok"}}}}

reasoning: Stand-in for the paper's RPKM>1 expression prefilter: keep genes with CPM>=1 in >=3 samples (one group's worth).

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "twoarm_EX_vs_CON", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\twoarm_EX_vs_CON\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\twoarm_EX_vs_CON\\DEG_results_EX_vs_CON.csv"], "counts": {"twoarm_EX_vs_CON": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 15070, "n_significant": 385, "n_up": 222, "n_down": 163, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15070, "n_significant": 396, "n_up": 223, "n_down": 173, "deg_sanity": "ok"}}}}

reasoning: Two-arm DESeq2 on the 6 CON+EX samples only, so dispersion and Cook flags are not driven by the heterogeneous PHAM arm; paper says group-pairwise without stating whether dispersion was pooled across all groups.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_EX_vs_CON", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_joint_grp_EX_vs_CON\\ora\\DEG_results_grp_EX_vs_CON_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_joint_grp_EX_vs_CON\\ora\\DEG_results_grp_EX_vs_CON_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_joint_grp_EX_vs_CON\\ora\\DEG_results_grp_EX_vs_CON_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_joint_grp_EX_vs_CON\\ora\\DEG_results_grp_EX_vs_CON_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 32 Mouse genes (direction=all, padj<0.05, |log2FC|>0.5849625). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Leukocy ... [1327 more characters]

reasoning: Paper reports GO BP/MF and gene set enrichment for exercise DEGs (S2.2.p1, Fig. 3C,D)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_EX_vs_CON", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_joint_grp_EX_vs_CON\\gsea\\DEG_results_grp_EX_vs_CON_GSEA_Hallmark.csv"], "summary": "GSEA complete on 19027 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 27 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=1.94 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.80 | NOM p=0.00e+00 | FDR q=2.32e-03 - HALLMARK_ANGIOGENESIS | NES=1.73 | NOM p=3.25e-03 | FDR q=5.44e-03 - HALLMARK_APICAL_SURFACE | NES=1.70 | NOM p=3.21e-03 | FDR q=6.79e-03 - HALLMARK_G2M_CHECKPOINT | NES=1.66 | NOM p=0.00e+00 | FDR q=8.99e-03 - HALLMARK_SPERMATOGENESIS | NES=1.47 | NOM p=1.85e-02 | FDR q=4.54e-02 - HALLMARK_KRAS_SIGNALING_UP | NES=1.45 | NOM p=1.36e-03 | FDR q=4.95e-02 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.44 | NOM p=6.98e-03 | FDR q=5.33e-02 - HALLMARK_MITOTIC_SPINDLE | NES=1.39 | NOM p=1.81e-02 | FDR q=8.23e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=-2.08 | NOM p=0. ... [424 more characters]

reasoning: Paper reports GO BP/MF and gene set enrichment for exercise DEGs (S2.2.p1, Fig. 3C,D)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "twoarm_EX_vs_CON", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_twoarm_EX_vs_CON\\ora\\DEG_results_EX_vs_CON_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_twoarm_EX_vs_CON\\ora\\DEG_results_EX_vs_CON_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_twoarm_EX_vs_CON\\ora\\DEG_results_EX_vs_CON_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\f719c1147eb0f406823e085b4396d05fdfa410d2\\GSE293221\\results\\enrichment_twoarm_EX_vs_CON\\ora\\DEG_results_EX_vs_CON_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 385 Mouse genes (direction=all, padj<0.05, |log2FC|>0.5849625). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Extracellular Matrix Organization (GO ... [1296 more characters]

reasoning: sensitivity: the two-arm fit recovers the paper named exercise genes; check whether its DEGs reproduce the paper triglyceride/lipase GO terms (Fig. 3)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["n = 3 tumors per arm, chosen as 'representative' by the authors (S2.2.p1); small study", "exercise arm singly housed while control group housed: housing is aliased with exercise", "original DESeq and RPKM>1 prefilter not reproduced; DEG counts are expected to differ", "Direction contradiction: paper says BB123696 and Lman1l increased with exercise and with PhAm (S2.2.p3); here both are lower in EX (log2FC -1.58, -1.83, not significant) and significantly lower in PHAM (log2FC -4.32, -5.33).", "Paper exercise DEGs Lipe, Plin1, Slc7a10 agree in direction (down in EX, log2FC -1.5 to -2.4) but get padj NA in the joint model (Cook outlier flag driven by the heterogeneous PHAM arm); Dgat2l6 up (log2FC 5.8) but not significant.", "Two of three PHAM tumors (GSM8878842, GSM8878843) are transcriptionally distinct from all other samples (Spearman ~0.6-0.7 vs >=0.93), with high Dcx/Sncb and loss of Spink3/Plin1 -- consistent with a different tumor phenotype; PHAM vs CON gives thousands of DEGs instead of the paper 176.", "Exercise DEG set overlaps the paper only in count (32 vs 32); most of our EX DEGs are up (27/32) and include seminal-vesicle secretory genes (Svs1-6, Sva, Spinkl), suggesting differing seminal-vesicle tissue content in the excised tumors.", "The two-arm CON+EX sensitivity fit recovers all five paper exercise genes in the paper direction (Lipe, Plin1, Slc7a10, Gpr83 down; Dgat2l6 up; padj<0.05) but calls 385 DEGs; the joint fit ... [4007 more characters]

reasoning: Counts from S2.2.p1 / S2.2.p2; genes from S2.2.p1-p3, S3.p1, S3.p2. Expected directions: EX down Lipe, Plin1, Slc7a10, Gpr83; EX up Dgat2l6, BB123696, Lman1l; PHAM down Spink3..Atp2c2, up Dcx, Sncb, BB123696, Lman1l.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample count",
    "paper": "6 per arm randomized, 1 exercise mouse died (S2.1.p1); 3 per arm sequenced (S4.6.p1)",
    "data": "9 samples, 3 per arm",
    "disposition": "executable_without_change"
  },
  {
    "item": "library prep",
    "paper": "KAPA stranded RNA-seq with RiboErase (S4.6.p1)",
    "data": "GEO extract protocol: Illumina stranded mRNA, molecule polyA RNA",
    "disposition": "executable_without_change"
  },
  {
    "item": "DE method",
    "paper": "original DESeq (S4.7.p1)",
    "data": "raw HTSeq counts; only DESeq2 available",
    "disposition": "declared_deviation"
  },
  {
    "item": "RPKM>1 prefilter",
    "paper": "average RPKM > 1 in at least one group (S4.7.p1)",
    "data": "gene-symbol counts without gene lengths",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE293221 (PMC13076624, exercise / Phellodendron amurense in TRAMP prostate tumors)

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`); validator: 14 records, 0 errors; status completed, route `declared_deviation`.
- Input: per-sample HTSeq-count files from `GSE293221_RAW.tar` (merged), columns renamed to GSM ids and rows put in a fixed shuffled order by `prep_matrix.py` (values unchanged; see tool problem 1). Raw integer counts, 22,609 gene symbols x 9 samples; exact alignment on the GSM index, 9/9.
- Design: `grp` from title: CON / EX (voluntary wheel running) / PHAM (Nexrutine diet), 3 each, independent animals. No blocking. Housing (EX single-housed, others group-housed) is part of the intervention and fully aliased with it.
- Executions:
  - `joint` (primary): one pydeseq2 model `~ grp` on all 9 samples, contrasts EX vs CON (primary), PHAM vs CON (secondary), PHAM vs EX (exploratory).
  - `joint_cpmfilter` (sensitivity): same model after a CPM >= 1 in >= 3 samples filter (14,722 genes kept), standing in for the paper's RPKM > 1 filter.
  - `twoarm_EX_vs_CON` (sensitivity): DESeq2 on the 6 CON+EX samples only.
- Enrichment: ORA (Enrichr GO/KEGG) + Hallmark GSEA on joint EX vs CON; ORA on the two-arm table.

## Threshold
Paper rule (S4.7.p1): FDR < 0.05 and fold change > 1.5 either way, i.e. padj < 0.05 and |log2FC| > 0.5849625, applied as `paper_on_deviation_route`. The paper's third criterion (average RPKM > 1 in at least one group) could not be applied because the deposit has no gene lengths.

## DEG counts vs paper (paper rule)
| Contrast | Ours | Paper |
|---|---|---|
| EX vs CON, joint (primary) | 32 (27 up / 5 down) | 32 |
| EX vs CON, joint + CPM filter | 28 (23 / 5) | 32 |
| EX vs CON, two-arm | 385 (222 / 163) | 32 |
| PHAM vs CON, joint | 3694 (2644 / 1050) | 176 (76 up / 100 down) |
| PHAM vs CON, joint + CPM filter | 3399 | 176 |

The count match on the primary table is a coincidence, not a reproduction. Paper-named exercise genes:
- Joint fit: Lipe, Plin1 and Slc7a10 go in the paper's direction (down, log2FC -1.5 to -2.4), but their padj is NA (Cook's outlier flag driven by the PHAM arm). Gpr83 is down and Dgat2l6 up (log2FC 5.8), both non-significant.
- Two-arm fit: all five are significant in the paper's direction: Lipe, Plin1, Slc7a10 and Gpr83 down, Dgat2l6 up.

The joint EX DEGs are mostly up. They include seminal-vesicle secretory genes (Svs1-6, Sva, Spinkl), which suggests the excise ... [2394 more characters]
