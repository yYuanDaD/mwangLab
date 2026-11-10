# Review packet B (the analysis' decisions): GSE222163

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the tissue level", "across": "tissue", "pairs_or_sets": 13, "samples_linked": 26, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_EX_vs_Ctrl_tissue-BAT | 37 | 39 | padj < 0.05 and |log2FoldChange| > 0.584963 | 74 | 39 | 17 | 94 | 1047 | 473 | 321 | 385 | 0.111 | 0.048 |
| grp_CREX_vs_CR_tissue-BAT | 30 | 30 | padj < 0.05 and |log2FoldChange| > 0.584963 | 62 | 30 | 15 | 91 | 1073 | 403 | 275 | 377 | 0.116 | 0.049 |
| grp_EX_vs_Ctrl_tissue-SkM | 48 | 50 | padj < 0.05 and |log2FoldChange| > 0.584963 | 102 | 50 | 20 | 137 | 822 | 261 | 113 | 327 | 0.119 | 0.038 |
| grp_CREX_vs_CR_tissue-SkM | 15 | 29 | padj < 0.05 and |log2FoldChange| > 0.584963 | 29 | 29 | 26 | 39 | 631 | 488 | 310 | 216 | 0.124 | 0.03 |

## Samples per design level

### `grp`
- **CR** (7): GSM6916806 / BAT CR1 / BAT_CR1; GSM6916807 / BAT CR2 / BAT_CR2; GSM6916808 / BAT CR3 / BAT_CR3; GSM6916809 / BAT CR4 / BAT_CR4; GSM6916821 / SkM CR1 / SkM_CR1; GSM6916822 / SkM CR2 / SkM_CR2; GSM6916823 / SkM CR3 / SkM_CR3
- **CREX** (7): GSM6916813 / BAT CE1 / BAT_CE1; GSM6916814 / BAT CE2 / BAT_CE2; GSM6916815 / BAT CE3 / BAT_CE3; GSM6916816 / BAT CE4 / BAT_CE4; GSM6916828 / SkM CE1 / SkM_CE1; GSM6916829 / SkM CE2 / SkM_CE2; GSM6916830 / SkM CE3 / SkM_CE3
- **Ctrl** (7): GSM6916810 / BAT control1 / BAT_ctrl1; GSM6916811 / BAT control2 / BAT_ctrl2; GSM6916812 / BAT control3 / BAT_ctrl3; GSM6916824 / SkM control1 / SkM_ctrl1; GSM6916825 / SkM control2 / SkM_ctrl2; GSM6916826 / SkM control3 / SkM_ctrl3; GSM6916827 / SkM control4 / SkM_ctrl4
- **EX** (8): GSM6916817 / BAT EX1 / BAT_EX1; GSM6916818 / BAT EX2 / BAT_EX2; GSM6916819 / BAT EX3 / BAT_EX3; GSM6916820 / BAT EX4 / BAT_EX4; GSM6916831 / SkM EX1 / SkM_EX1; GSM6916832 / SkM EX2 / SkM_EX2; GSM6916833 / SkM EX3 / SkM_EX3; GSM6916834 / SkM EX4 / SkM_EX4

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE222163"], "assay": "bulk RNA-seq (BGISEQ-500, PE150), STAR mm10 + RSEM quantification (S2.6.p1, S2.7.p1)", "organism": "Mouse, male C57BL/6J, 8 weeks old at start, 8-week interventions (S2.1.p1, S2.3.p1, S3.1.p1)", "tissues": ["brown adipose tissue (BAT)", "gastrocnemius muscle (SkM)"], "factors": {"diet": ["ad libitum (control)", "CR 70%"], "exercise": ["sedentary", "treadmill EX 1 h/day 5 d/wk 8 wk"], "groups": ["control", "CR", "EX", "CREX"]}, "sample_inclusion": "BAT: control 3, CR 4, EX 4, CREX 4 (15); SkM: control 4, CR 3, EX 4, CREX 3 (14) (S2.6.p1)", "primary_estimand": "Effect of 8-week treadmill exercise training on BAT and gastrocnemius gene expression, without CR (EX vs control) and under CR (CREX vs CR), each tissue analysed separately; mice harvested 24 h after the last bout (S2.1.p1, S3.3.p1, S3.6.p1)", "planned_contrasts": ["BAT EX vs control (S3.3.p1; paper: 13 up + 24 down = 37 DEGs)", "BAT CREX vs CR (S3.3.p1; paper: 25 up + 5 down = 30 DEGs)", "SkM EX vs control (S3.6.p1; paper: 20 up + 28 down = 48 DEGs)", "SkM CREX vs CR (S3.6.p1; paper: 6 up + 9 down = 15 DEGs)", "Non-exercise contrasts in the paper (CR vs control, CREX vs EX; S3.2.p1, S3.5.p1) are the CR effect and are out of scope for this exercise request"], "repeated_measure_unit": "none; one sample per mouse per tissue, tissues analysed separately", "normalization": "RSEM expected counts into DESeq2 (S2.7.p1)", "paper_method": "DESeq2 v1.38.0, two groups at a time (S2.7.p1: 'DE  ... [471 more characters]

reasoning: Methods S2.6.p1 give the per-tissue group sizes, S2.7.p1 the DESeq2 two-group route and the threshold adjusted p < 0.05 and |log2FC| > log2(1.5); GEO data_processing repeats 'adjust P value < 0.05 and |FC|>1.5'. Exercise effects are reported in S3.3.p1 (BAT) and S3.6.p1 (SkM) for EX vs control and CREX vs CR.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\input\\GSE222163_exp_all_repaired.csv", "owned": true, "checks": ["S10.p1 names GEO GSE222163", "29 GEO samples = 15 BAT + 14 SkM with the paper's per-group sizes", "GEO data_processing (STAR mm10, RSEM, DESeq2, |FC|>1.5, padj<0.05) matches S2.7.p1", "contact Xingxing Kong matches the corresponding author"], "accession": "GSE222163", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE222163\\GSE222163_metadata.csv"}

reasoning: Data availability S10.p1 cites GSE222163; sample counts per tissue and group match S2.6.p1 exactly.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 29, "n_metadata": 29, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\aligned\\aligned_metadata.csv", "columns": {"tissue": {"source": "description", "regex": "^(BAT|SkM)_"}, "grp": {"source": "description", "regex": "^(?:BAT|SkM)_(ctrl|CR|CE|EX)\\d+$", "recode": {"ctrl": "Ctrl", "CR": "CR", "CE": "CREX", "EX": "EX"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\aligned\\design_metadata.csv", "sha256": "86d0a0d4c42b038abca3e080362994c9063179226986a6bdac147fca4983130a", "levels": {"tissue": {"BAT": 15, "SkM": 14}, "grp": {"EX": 8, "CR": 7, "Ctrl": 7, "CREX": 7}}}}

reasoning: Matrix columns equal GEO 'description' after the prep script lower-cased 'Ctrl' to 'ctrl' (the only difference; checked one-to-one). tissue and group come from the description token; 'CE' is the CR+EX group (GEO treatment field 'calorie restriction combined with treadmill running exercise training'). Group sizes per tissue match S2.6.p1.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\aligned\\aligned_matrix.csv", "sha256": "d5229633ad1e32c24cfac4fecc41bba662f00c263e3bac60fc07d1158b694d23", "n_features": 24766, "n_samples": 29, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3358851.0, "median": 15.0, "integer_fraction": 0.9389, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: 94% integer values, fractional values like 64.23 in the rest, column sums ~21-25 M (read-depth scale, not TPM sums of 1e6); GEO data_processing and S2.7.p1 say RSEM quantification feeding DESeq2, i.e. RSEM expected counts. Paper's stated input is the same.

### design (valid, not_started)

final: {"analysis_type": "two-group per tissue (paper's pairwise comparisons)", "design_column": "grp", "contrasts": [{"name": "grp_EX_vs_Ctrl_tissue-BAT", "control": "Ctrl", "treatment": "EX", "stratum": "BAT", "role": "primary"}, {"name": "grp_EX_vs_Ctrl_tissue-SkM", "control": "Ctrl", "treatment": "EX", "stratum": "SkM", "role": "primary"}, {"name": "grp_CREX_vs_CR_tissue-BAT", "control": "CR", "treatment": "CREX", "stratum": "BAT", "role": "secondary"}, {"name": "grp_CREX_vs_CR_tissue-SkM", "control": "CR", "treatment": "CREX", "stratum": "SkM", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 12}}

reasoning: Paper S3.3.p1 and S3.6.p1 report the exercise effect as EX vs control and CREX vs CR within each tissue; tissue is a stratum. Mice are independent animals randomised to groups (S2.3.p1).

rejected alternatives: [{"value": "pool BAT and SkM in one model", "reason_rejected": "the paper analyses each tissue separately; tissue effects dwarf treatment effects"}, {"value": "2x2 diet x exercise factorial with interaction", "reason_rejected": "not the paper's estimand; the paper reports pairwise group comparisons only"}, {"value": "pool CREX with EX as 'exercised'", "reason_rejected": "different diets; the paper keeps EX vs control and CREX vs CR separate"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 29, "n_columns": 4, "columns": ["Intercept", "grp_CREX", "grp_Ctrl", "grp_EX"], "rank": 4, "full_rank": true, "residual_df": 25, "levels": {"grp": {"EX": 8, "CR": 7, "Ctrl": 7, "CREX": 7}}, "cells": [{"cell": ["CR"], "n": 7}, {"cell": ["CREX"], "n": 7}, {"cell": ["Ctrl"], "n": 7}, {"cell": ["EX"], "n": 8}], "min_cell_size": 7, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 29, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 29, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 2, "status": "crossed", "crosstab": {"CR": {"brown adipose tissue": 4, "gastrocnemius muscle tissue": 3}, "CREX": {"brown adipose tissue": 4, "gastrocnemius muscle tissue": 3}, "Ctrl": {"brown adipose tissue": 3, "gastrocnemius muscle tissue": 4}, "EX": {"brown adipose tissue": 4, "gastrocnemius muscle tissue": 4}}}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_leve ... [2822 more characters]

reasoning: One tissue sample per independent mouse within each tissue stratum; no batch, lane or sex variable is recorded (all male). No blocking unit exists.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (pydeseq2 Wald), two groups at a time per tissue", "formula": "~ grp", "rounding_documented": true, "paper_route": {"method": "DESeq2 v1.38.0 (R) on RSEM counts, two-group", "status": "reproduced_with_implementation_difference", "reason": "pydeseq2 instead of R DESeq2; RSEM expected counts rounded to integers as DESeqDataSetFromMatrix requires"}, "deviations": ["pydeseq2 implementation instead of R DESeq2 1.38.0", "RSEM expected counts rounded (half to even) before DESeq2", "4 rows with Excel-mangled duplicated symbols (1-Mar, 2-Mar) dropped"], "transform": "round"}

reasoning: S2.7.p1 states DESeq2 on RSEM output; the matrix holds RSEM expected counts. Each execution keeps only the two compared groups of one tissue, matching 'DE genes analysis for the two groups'.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: S2.7.p1: adjusted p value < 0.05 and |log2FC| > log2(1.5) = 0.5849625; GEO data_processing agrees. Figure legends (FIG2, FIG4) colour volcano points with p < 0.05 and |log2FC| > 0.58, recorded as a discrepancy; methods text governs.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_EX_vs_Ctrl_tissue-BAT", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 7, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\grp_EX_vs_Ctrl_tissue-BAT\\input\\matrix.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\grp_EX_vs_Ctrl_tissue-BAT\\DEG_results_EX_vs_Ctrl.csv"], "counts": {"grp_EX_vs_Ctrl_tissue-BAT": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 15043, "n_significant": 39, "n_up": 13, "n_down": 26, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15043, "n_significant": 74, "n_up": 19, "n_down": 55, "deg_sanity": "ok"}}}}

reasoning: paper's two-group DESeq2, BAT EX vs control (S3.3.p1)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_EX_vs_Ctrl_tissue-SkM", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\grp_EX_vs_Ctrl_tissue-SkM\\input\\matrix.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\grp_EX_vs_Ctrl_tissue-SkM\\DEG_results_EX_vs_Ctrl.csv"], "counts": {"grp_EX_vs_Ctrl_tissue-SkM": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14764, "n_significant": 50, "n_up": 20, "n_down": 30, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14764, "n_significant": 102, "n_up": 41, "n_down": 61, "deg_sanity": "ok"}}}}

reasoning: paper's two-group DESeq2, SkM EX vs control (S3.6.p1)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_CREX_vs_CR_tissue-BAT", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\grp_CREX_vs_CR_tissue-BAT\\input\\matrix.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\grp_CREX_vs_CR_tissue-BAT\\DEG_results_CREX_vs_CR.csv"], "counts": {"grp_CREX_vs_CR_tissue-BAT": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 13698, "n_significant": 30, "n_up": 26, "n_down": 4, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13698, "n_significant": 62, "n_up": 33, "n_down": 29, "deg_sanity": "ok"}}}}

reasoning: paper's two-group DESeq2, BAT exercise under CR (S3.3.p1)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_CREX_vs_CR_tissue-SkM", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\grp_CREX_vs_CR_tissue-SkM\\input\\matrix.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\grp_CREX_vs_CR_tissue-SkM\\DEG_results_CREX_vs_CR.csv"], "counts": {"grp_CREX_vs_CR_tissue-SkM": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14883, "n_significant": 29, "n_up": 10, "n_down": 19, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14883, "n_significant": 29, "n_up": 10, "n_down": 19, "deg_sanity": "ok"}}}}

reasoning: paper's two-group DESeq2, SkM exercise under CR (S3.6.p1)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_EX_vs_Ctrl_tissue-SkM", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-SkM\\ora\\DEG_results_EX_vs_Ctrl_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-SkM\\ora\\DEG_results_EX_vs_Ctrl_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-SkM\\ora\\DEG_results_EX_vs_Ctrl_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-SkM\\ora\\DEG_results_EX_vs_Ctrl_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 50 Mouse genes (direction=all, padj<0.05, |log2FC|>0.5849625). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Regulation Of Epithelial Cell Apoptotic Process (GO:1904035) | padj=8.62e-02 | overlap=2/11 | genes=Z ... [1233 more characters]

reasoning: paper reports GO/KEGG for SkM EX DEGs (circadian rhythm up, PPAR signaling down; S3.6.p1)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_EX_vs_Ctrl_tissue-SkM", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-SkM\\gsea\\DEG_results_EX_vs_Ctrl_GSEA_Hallmark.csv"], "summary": "GSEA complete on 21423 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 23 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_E2F_TARGETS | NES=1.42 | NOM p=1.02e-02 | FDR q=3.09e-01 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.40 | NOM p=7.80e-03 | FDR q=1.92e-01 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.36 | NOM p=1.83e-02 | FDR q=1.72e-01 - HALLMARK_G2M_CHECKPOINT | NES=1.28 | NOM p=4.40e-02 | FDR q=2.77e-01 - HALLMARK_GLYCOLYSIS | NES=1.22 | NOM p=8.12e-02 | FDR q=3.67e-01 - HALLMARK_ADIPOGENESIS | NES=1.21 | NOM p=6.67e-02 | FDR q=3.13e-01 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.21 | NOM p=1.03e-01 | FDR q=2.77e-01 - HALLMARK_ANGIOGENESIS | NES=1.11 | NOM p=3.01e-01 | FDR q=4.89e-01 - HALLMARK_SPERMATOGENESIS | NES=1.09 | NOM p=2.86e-01 | FDR q=5.20e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.03 | NOM p=3.70e-01 | FDR q=6.56e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-2.05 | NOM p=0.00e+00 | FDR q=1.31e-03 - HALLMARK_PEROXISOME | NES=-1.82 | NOM p=0.00e+00 | FDR q=6.54e-03 - HALLM ... [405 more characters]

reasoning: paper reports GO/KEGG for SkM EX DEGs (circadian rhythm up, PPAR signaling down; S3.6.p1)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_EX_vs_Ctrl_tissue-BAT", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-BAT\\ora\\DEG_results_EX_vs_Ctrl_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-BAT\\ora\\DEG_results_EX_vs_Ctrl_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-BAT\\ora\\DEG_results_EX_vs_Ctrl_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-BAT\\ora\\DEG_results_EX_vs_Ctrl_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 39 Mouse genes (direction=all, padj<0.05, |log2FC|>0.5849625). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Regulation Of Fatty Acid Oxidation (GO:0046320) | padj=1.92e-03 | overlap=3/16 | genes=NR4A3;KLHL25;P ... [1233 more characters]

reasoning: pathway view of the BAT exercise effect for comparison; paper shows only DEG counts (S3.3.p1)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_EX_vs_Ctrl_tissue-BAT", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36839405\\GSE222163\\results\\enrichment_grp_EX_vs_Ctrl_tissue-BAT\\gsea\\DEG_results_EX_vs_Ctrl_GSEA_Hallmark.csv"], "summary": "GSEA complete on 21913 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 37 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYOGENESIS | NES=2.70 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.04 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_GLYCOLYSIS | NES=1.79 | NOM p=0.00e+00 | FDR q=8.76e-04 - HALLMARK_MTORC1_SIGNALING | NES=1.70 | NOM p=0.00e+00 | FDR q=4.82e-03 - HALLMARK_PROTEIN_SECRETION | NES=1.61 | NOM p=3.15e-03 | FDR q=1.33e-02 - HALLMARK_KRAS_SIGNALING_DN | NES=1.51 | NOM p=1.53e-03 | FDR q=3.36e-02 - HALLMARK_APICAL_JUNCTION | NES=1.41 | NOM p=1.04e-02 | FDR q=7.88e-02 - HALLMARK_ANGIOGENESIS | NES=1.39 | NOM p=6.53e-02 | FDR q=8.57e-02 - HALLMARK_UV_RESPONSE_DN | NES=1.39 | NOM p=1.90e-02 | FDR q=7.62e-02 - HALLMARK_COAGULATION | NES=1.37 | NOM p=2.49e-02 | FDR q=8.42e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-2.41 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=-1.99 | NOM p=0.00e+00 | FDR q=6.10e-04 - HALLMARK_TG ... [405 more characters]

reasoning: pathway view of the BAT exercise effect for comparison; paper shows only DEG counts (S3.3.p1)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["pydeseq2 and rounded RSEM counts instead of R DESeq2 1.38.0; small count differences expected", "paper threshold is padj; volcano legends mention raw p < 0.05, which would give larger counts", "group sizes are 3-4 per arm; exercise effects are small (paper S4.p4) so DEG counts are unstable"], "results": {"grp_EX_vs_Ctrl_tissue-BAT": {"n_deg": 39, "up": 13, "down": 26, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 74}, "grp_EX_vs_Ctrl_tissue-SkM": {"n_deg": 50, "up": 20, "down": 30, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 102}, "grp_CREX_vs_CR_tissue-BAT": {"n_deg": 30, "up": 26, "down": 4, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 62}, "grp_CREX_vs_CR_tissue-SkM": {"n_deg": 29, "up": 10, "down": 19, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 29}}, "paper_counts": {"grp_EX_vs_Ctrl_tissue-BAT": 37, "grp_CREX_vs_CR_tissue-BAT": 30, "grp_EX_vs_Ctrl_tissue-SkM": 48, "grp_CREX_vs_CR_tissue-SkM": 15}, "comparison": {"grp_EX_vs_Ctrl_tissue-BAT": {"ours": 39, "paper": 37}, "grp_CREX_vs_CR_tissue-BAT": {"ours": 30, "paper": 30}, "grp_EX_vs_Ctrl_tissue-SkM": {"ours": 50, "paper": 48}, "grp_CREX_vs_CR_tissue-SkM": {"ours": 29, "paper": 15}}, "paper_gene_check": {}}

reasoning: Paper counts from S3.3.p1 (BAT) and S3.6.p1 (SkM); no exercise-specific genes are named in the text.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 29 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "threshold wording",
    "paper": "S2.7.p1 adjusted p < 0.05 and |log2FC| > log2(1.5)",
    "data": "FIG2/FIG4 legends colour volcano points by p < 0.05 and |log2FC| > 0.58",
    "disposition": "executable_without_change"
  },
  {
    "item": "RSEM version",
    "paper": "rsem v2.0.1 (S2.7.p1)",
    "data": "GEO data_processing says RSEM v1.2.28 and DESeq2 1.3.40",
    "disposition": "executable_without_change"
  },
  {
    "item": "sample name case",
    "paper": "n/a",
    "data": "matrix columns 'Ctrl' vs GEO description 'ctrl'; fixed by prep_matrix.py",
    "disposition": "executable_without_change"
  },
  {
    "item": "duplicated feature IDs",
    "paper": "n/a",
    "data": "1-Mar and 2-Mar each appear twice (Excel date mangling); rows dropped by prep_matrix.py",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID36839405 / GSE222163

Paper: Transcriptomics Dissection of Calorie Restriction and Exercise Training in Brown Adipose Tissue and Skeletal Muscle (Nutrients 2023, PMC9966723).
Outcome: **finished**. The route is `paper_aligned`, and the decision-contract validator returned 0 errors over 17 records.

## What ran
- `case_runner inspect GSE222163`. Then `prep_matrix.py`: it lower-cases `Ctrl` to `ctrl` in the matrix column names so they match the GEO `description` field one to one, and it drops 4 rows with Excel-mangled duplicate symbols (`1-Mar`, `2-Mar`, two rows each). Then `case_runner execute case_spec.json`.
- Alignment: an exact match on `description` covers 29/29 samples. The derived columns are `tissue` (BAT/SkM) and `grp` (Ctrl/CR/EX/CREX). GEO's `CE` is recoded to CREX.
- Matrix: RSEM expected counts. About 94% of values are integers, column sums are about 21-25 M, and S2.7.p1 says RSEM fed DESeq2. The counts were rounded at case level, then run through DESeq2 (pydeseq2 Wald, `~ grp`). Each run used only the two compared groups of one tissue, which is the paper's "two groups" route (S2.7.p1).
- Suitability: analyzable. 12/12 comparisons have n >= 3. The sex check passed (all male).
- Covariance: none needed. Animals are independent and no batch is recorded.
- Enrichment: ORA (Enrichr GO + KEGG, all-direction DEGs) and Hallmark GSEA for EX vs control in both tissues.

## DEG counts vs the paper
Threshold (paper, S2.7.p1; also in GEO `data_processing`): padj < 0.05 and |log2FC| > log2(1.5) = 0.5849625.

| Contrast | Ours (up/down) | Paper (up/down) | Audit: padj < 0.05 only |
|---|---|---|---|
| BAT EX vs control (primary) | 39 (13/26) | 37 (13/24), S3.3.p1 | 74 |
| SkM EX vs control (primary) | 50 (20/30) | 48 (20/28), S3.6.p1 | 102 |
| BAT CREX vs CR | 30 (26/4) | 30 (25/5), S3.3.p1 | 62 |
| SkM CREX vs CR | 29 (10/19) | 15 (6/9), S3.6.p1 | 29 |

Three of the four counts are close to the paper's. SkM CREX vs CR gives about twice the paper's count (n = 3 vs 3, so the count is unstable).

Enrichment, reported separately from DE:
- SkM EX vs control, KEGG ORA:
  - Top term is "Circadian rhythm" (Per2, Per3, Arntl; adj p = 0.007).
  - "PPAR signaling" is next (Fabp3, Ehhadh, Plin5, all down; adj p = 0.058, just above 0.05).
  - This matches the paper's statement in S3.6.p1: circadian rhythm among up genes, PPAR among down genes. Arntl is down while Per2/Per3 are up, as expected for clock-phase genes.
- SkM Hallmark GSEA: nothing reaches  ... [1740 more characters]
