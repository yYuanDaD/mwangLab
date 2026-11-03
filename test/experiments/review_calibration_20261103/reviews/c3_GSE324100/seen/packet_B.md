# Review packet B (the analysis' decisions): GSE324100

## Mechanical flags

- **other_rule_matches_paper**: {"table": "primary/grp_C26_PoWeR_vs_C26_SED", "paper": 963, "applied": 255, "applied_rule": "padj < 0.05", "closest_rule": "pvalue<0.05 & |lfc|>1", "closest_n": 889, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| primary/grp_PBS_PoWeR_vs_PBS_SED | 42 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 1424 | 480 | 230 | 332 | 0.11 | 0.08 |
| primary/grp_C26_SED_vs_PBS_SED | 2740 | 2165 | padj < 0.05 | 2165 | 1362 | 632 | 3023 | 4432 | 2263 | 1153 | 2534 | 0.073 | 0.25 |
| primary/grp_C26_PoWeR_vs_C26_SED | 963 | 255 | padj < 0.05 | 255 | 177 | 82 | 652 | 2923 | 1429 | 889 | 1131 | 0.056 | 0.165 |

## Samples per design level

### `grp`
- **C26_PoWeR** (5): GSM9568248 / MaleC26PoWeR1 / Library name: P10_S34,8-week-old BALB/c ; GSM9568249 / MaleC26PoWeR2 / Library name: P12_S36,8-week-old BALB/c ; GSM9568259 / FemaleC26PoWeR1 / Library name: P22_S46,8-week-old BALB/c ; GSM9568260 / FemaleC26PoWeR2 / Library name: P23_S47,8-week-old BALB/c ; GSM9568261 / FemaleC26PoWeR3 / Library name: P24_S48,8-week-old BALB/c 
- **C26_SED** (5): GSM9568246 / MaleC26SED1 / Library name: P7_S31,8-week-old BALB/c m; GSM9568247 / MaleC26SED2 / Library name: P8_S32,8-week-old BALB/c m; GSM9568256 / FemaleC26SED1 / Library name: P19_S43,8-week-old BALB/c ; GSM9568257 / FemaleC26SED2 / Library name: P20_S44,8-week-old BALB/c ; GSM9568258 / FemaleC26SED3 / Library name: P21_S45,8-week-old BALB/c 
- **PBS_PoWeR** (6): GSM9568243 / MalePBSPoWeR1 / Library name: P4_S28,8-week-old BALB/c m; GSM9568244 / MalePBSPoWeR2 / Library name: P5_S29,8-week-old BALB/c m; GSM9568245 / MalePBSPoWeR3 / Library name: P6_S30_,8-week-old BALB/c ; GSM9568253 / FemalePBSPoWeR1 / Library name: P16_S40,8-week-old BALB/c ; GSM9568254 / FemalePBSPoWeR2 / Library name: P17_S41,8-week-old BALB/c ; GSM9568255 / FemalePBSPoWeR3 / Library name: P18_S42,8-week-old BALB/c 
- **PBS_SED** (6): GSM9568240 / MalePBSSED1 / Library name: P1_S25,8-week-old BALB/c m; GSM9568241 / MalePBSSED2 / Library name: P2_S26,8-week-old BALB/c m; GSM9568242 / MalePBSSED3 / Library name: P3_S27,8-week-old BALB/c m; GSM9568250 / FemalePBSSED1 / Library name: P13_S37,8-week-old BALB/c ; GSM9568251 / FemalePBSSED2 / Library name: P14_S38,8-week-old BALB/c ; GSM9568252 / FemalePBSSED3 / Library name: P15_S39,8-week-old BALB/c 

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE324100"], "assay": "bulk total RNA-seq, gastrocnemius, BALB/c mice (S2.7.p1)", "factors": {"tumour": ["PBS", "C26"], "intervention": ["SED", "PoWeR (progressive weighted wheel running, ~11.5-12 wk, 8 wk before and 3.5 wk after C26 inoculation)"], "sex": ["Male", "Female"]}, "sample_inclusion": "subset of n = 2-3 mice per sex per group chosen to represent group averages (S2.7.p1); FIG8 legend: PBS SED n=6, PBS PoWeR n=6, C26 SED n=5, C26 PoWeR n=5; sexes collapsed (S2.8.p1, S3.7.p1)", "primary_estimand": "effect of PoWeR training on gastrocnemius gene expression in healthy mice (PBS PoWeR vs PBS SED) and in tumour-bearing mice (C26 PoWeR vs C26 SED); tumour effect C26 SED vs PBS SED as context", "planned_contrasts": ["PBS PoWeR vs PBS SED (S3.7.p1; paper: 42 DEGs)", "C26 SED vs PBS SED (S3.7.p1; paper: 2740 DEGs)", "C26 PoWeR vs C26 SED (S3.7.p1; paper: 963 DEGs)"], "repeated_measure_unit": "none; one gastrocnemius per independent mouse", "normalization": "DESeq2 median ratio after excluding genes with max count < 5 (S2.7.p1)", "paper_method": "DESeq2 in Partek Flow, sexes pooled, genes with geometric mean < 1 excluded before BH correction (S2.7.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.7.p1"}, "paper_results": {"PBS_PoWeR_vs_PBS_SED": 42, "C26_SED_vs_PBS_SED": 2740, "C26_PoWeR_vs_C26_SED": 963, "corrected_mito_genes": 131}}

reasoning: S2.7.p1 gives assay, normalisation, DESeq2 and BH FDR < 0.05 with no fold-change rule. S3.7.p1 gives the three pairwise comparisons and their DEG counts; FIG8 legend gives n per group; S2.8.p1 says sexes were collapsed for all presented analyses.

### ownership (valid, not_started)

final: {"matrix_file": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100_normalized_counts_genes_x_samples.csv", "owned": true, "checks": ["S15.p1 names GSE324100 as the RNA-seq deposit", "GEO: gastrocnemius, BALB/c, PBS/C26 x Sedentary/PoWeR, 22 samples = 6+6+5+5 as in FIG8", "deposited matrix Group/Sex labels agree with GEO titles/sex for all 22 libraries (prep_transpose.py)"], "accession": "GSE324100", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE324100\\GSE324100_metadata.csv"}

reasoning: Accession cited in data availability (S15.p1); sample counts and groups match the FIG8 legend exactly; the supplementary matrix carries its own group labels which agree with metadata.

### alignment (valid, not_started)

final: {"method": "exact:lib", "n_aligned": 22, "n_metadata": 22, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\aligned\\aligned_metadata.csv", "columns": {"sex": {"alias_of": "characteristics_ch1.2.Sex"}, "tum": {"source": "title", "regex": "^(?:Male|Female)(PBS|C26)"}, "ex": {"source": "title", "regex": "(SED|PoWeR)\\d+$"}, "grp": {"combine": ["tum", "ex"], "separator": "_", "of": "recoded values"}}, "output": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\aligned\\design_metadata.csv", "sha256": "0f5e004754df993423478d8ec5137b57a889ad2453448ff2261d9debcd4ba247", "levels": {"sex": {"Female": 12, "Male": 10}, "tum": {"PBS": 12, "C26": 10}, "ex": {"SED": 11, "PoWeR": 11}, "grp": {"PBS_SED": 6, "PBS_PoWeR": 6, "C26_SED": 5, "C26_PoWeR": 5}}}}

reasoning: Matrix columns are library names (P1_S25 ...); GEO description holds 'Library name: P1_S25' (one has a trailing underscore, P6_S30_, which the regex drops). Exact match on the derived key. Group labels from title; grp combines tumour and intervention into four cells.

### matrix (valid, not_started)

final: {"matrix_type": "DESeq2 median-ratio normalized counts (linear normalized, non-integer)", "recommended_method": "limma on log2(x+1)", "profile": {"path": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\aligned\\aligned_matrix.csv", "sha256": "22288335c8fe1d462ba30d31b4aa39baab224104b57fedde411c38489e67b069", "n_features": 17725, "n_samples": 22, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1348560.017085, "median": 110.731579, "integer_fraction": 0.03, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: integer fraction 0.03, max 1.35e6, no negatives; file name says Normalized_counts and data_processing states 'Normalized with DESeq2 median ratio ... Supplementary files format and content: DESeq2 Normalized Counts'. Raw counts were not deposited (supplementary_file_1 NONE on samples; only this series file). The paper's input is raw counts into DESeq2 (S2.7.p1), so the paper input is unavailable.

### design (valid, not_started)

final: {"analysis_type": "multi-group (4 cells, one model, planned pairwise contrasts)", "design_column": "grp", "contrasts": [{"name": "grp_PBS_PoWeR_vs_PBS_SED", "control": "PBS_SED", "treatment": "PBS_PoWeR", "role": "primary"}, {"name": "grp_C26_PoWeR_vs_C26_SED", "control": "C26_SED", "treatment": "C26_PoWeR", "role": "primary"}, {"name": "grp_C26_SED_vs_PBS_SED", "control": "PBS_SED", "treatment": "C26_SED", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: Paper compares the four tumour x intervention cells pairwise with sexes pooled (S3.7.p1, S2.8.p1). One model on all 22 samples with planned pairwise contrasts, never pooled levels. Exercise contrasts within PBS and within C26 are primary; the tumour effect is secondary context. Rejected: a two-factor main-effect model (paper does not report main effects, and an exercise main effect would average over tumour status, which the paper treats separately); sex-split primary analyses (paper pooled; per-sex is exploratory).

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "sex", "disposition": "sensitivity: ~ sex + grp; paper pooled sexes without a stated sex term"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 22, "n_columns": 4, "columns": ["Intercept", "grp_C26_SED", "grp_PBS_PoWeR", "grp_PBS_SED"], "rank": 4, "full_rank": true, "residual_df": 18, "levels": {"grp": {"PBS_SED": 6, "PBS_PoWeR": 6, "C26_SED": 5, "C26_PoWeR": 5}}, "cells": [{"cell": ["C26_PoWeR"], "n": 5}, {"cell": ["C26_SED"], "n": 5}, {"cell": ["PBS_PoWeR"], "n": 6}, {"cell": ["PBS_SED"], "n": 6}], "min_cell_size": 5, "missing_values": {}}, "confounding": [{"column": "sex", "n_levels": 2, "status": "crossed", "crosstab": {"C26_PoWeR": {"Female": 3, "Male": 2}, "C26_SED": {"Female": 3, "Male": 2}, "PBS_PoWeR": {"Female": 3, "Male": 3}, "PBS_SED": {"Female": 3, "Male": 3}}}]}

reasoning: Independent animals, one muscle each, single batch (characteristics batch = 1). Sex is roughly balanced across cells (3M/3F, 3M/3F, 2M/3F, 2M/3F) so not confounded with grp. The paper pooled sexes and states no sex covariate, so the primary model is ~ grp; a ~ sex + grp model is run as sensitivity.

### method (valid, not_started)

final: {"matrix_type": "DESeq2 median-ratio normalized counts (linear normalized, non-integer)", "method": "limma (moderated t, empirical Bayes) on log2(x+1) of DESeq2-normalized counts", "formula": "~ grp", "paper_route": {"method": "DESeq2 on raw counts", "status": "blocked", "reason": "only DESeq2 median-ratio normalized (non-integer) counts were deposited; raw counts unavailable and rounding normalized counts is not a documented recipe"}, "deviations": ["limma on log2(normalized+1) instead of DESeq2 Wald on raw counts", "no Partek geometric-mean < 1 independent filter reproduced; the depositor already removed genes with max count < 5"], "transform": "log2(x+1)"}

reasoning: Matrix policy: linear normalized expression -> log2(x+1) then limma. DESeq2 on normalized counts would misstate the mean-variance model and size factors.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "deviation_note": "paper rule (BH FDR < 0.05, no fold-change cutoff) applied to the limma deviation route; audit rule adds |log2FC| > log2(1.5) for comparison only"}

reasoning: S2.7.p1: BH-adjusted P < 0.05 defines DEGs; no fold-change rule stated.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "primary", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 22, "matrix": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\primary\\DEG_results_grp_PBS_PoWeR_vs_PBS_SED.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\primary\\DEG_results_grp_C26_SED_vs_PBS_SED.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\primary\\DEG_results_grp_C26_PoWeR_vs_C26_SED.csv"], "counts": {"primary/grp_PBS_PoWeR_vs_PBS_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17725, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17725, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "primary/grp_C26_SED_vs_PBS_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17725, "n_significant": 2165, "n_up": 1046, "n_down": 1119, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17725, "n_significant": 1362, "n_up": 696, "n_down": 666, "deg_sanity": "ok"}}, "primary/grp_C26_PoWeR_vs_C26_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17725, "n_significant": 255, "n_up": 139, "n_down": 116, "deg_sanity": "ok"}, "audit": {"rule": "padj  ... [130 more characters]

reasoning: one limma model ~ grp on all 22 samples; the paper's three pairwise comparisons

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "sex_adjusted", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 22, "matrix": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell) + C(cov0)", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\sex_adjusted\\DEG_results_grp_PBS_PoWeR_vs_PBS_SED.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\sex_adjusted\\DEG_results_grp_C26_SED_vs_PBS_SED.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\sex_adjusted\\DEG_results_grp_C26_PoWeR_vs_C26_SED.csv"], "counts": {"sex_adjusted/grp_PBS_PoWeR_vs_PBS_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17725, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17725, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "sex_adjusted/grp_C26_SED_vs_PBS_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17725, "n_significant": 2502, "n_up": 1209, "n_down": 1293, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17725, "n_significant": 1539, "n_up": 771, "n_down": 768, "deg_sanity": "ok"}}, "sex_adjusted/grp_C26_PoWeR_vs_C26_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17725, "n_significant": 419, "n_up": 205, "n_down": 2 ... [181 more characters]

reasoning: same contrasts with sex as an additive covariate

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "female_only", "role": "exploratory", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\female_only\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\female_only\\DEG_results_grp_PBS_PoWeR_vs_PBS_SED.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\female_only\\DEG_results_grp_C26_SED_vs_PBS_SED.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\female_only\\DEG_results_grp_C26_PoWeR_vs_C26_SED.csv"], "counts": {"female_only/grp_PBS_PoWeR_vs_PBS_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17716, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17716, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "female_only/grp_C26_SED_vs_PBS_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17716, "n_significant": 1965, "n_up": 934, "n_down": 1031, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17716, "n_significant": 1507, "n_up": 746, "n_down": 761, "deg_sanity": "ok"}}, "female_only/grp_C26_PoWeR_vs_C26_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17716, "n_significant": 620, "n_up": 362, "n_down": 258, "de ... [174 more characters]

reasoning: per-sex split (suitability: per-sex analysis yes; paper Appendix FIG16 stratified by sex); females n=3 per cell

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "male_only", "role": "exploratory", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 10, "matrix": "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\male_only\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\male_only\\DEG_results_grp_PBS_PoWeR_vs_PBS_SED.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\male_only\\DEG_results_grp_C26_SED_vs_PBS_SED.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\male_only\\DEG_results_grp_C26_PoWeR_vs_C26_SED.csv"], "counts": {"male_only/grp_PBS_PoWeR_vs_PBS_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17708, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17708, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "male_only/grp_C26_SED_vs_PBS_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17708, "n_significant": 19, "n_up": 15, "n_down": 4, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17708, "n_significant": 19, "n_up": 15, "n_down": 4, "deg_sanity": "ok"}}, "male_only/grp_C26_PoWeR_vs_C26_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 17708, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule ... [135 more characters]

reasoning: per-sex split; males n=3 in PBS cells, n=2 in C26 cells (small n, exploratory only)

### enrichment (valid, failed)

final: {"organism": "Mouse", "subset": "primary/grp_PBS_PoWeR_vs_PBS_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": [], "summary": "No significant DEGs found with padj < 0.05 and |log2FC| > 0.0 (direction=up). Cannot run enrichment.", "execution_error": "no output written: No significant DEGs found with padj < 0.05 and |log2FC| > 0.0 (direction=up). Cannot run enrichment."}

reasoning: paper reports GO for up/down DEGs (S2.7.p1)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "primary/grp_PBS_PoWeR_vs_PBS_SED", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_PBS_PoWeR_vs_PBS_SED\\gsea\\DEG_results_grp_PBS_PoWeR_vs_PBS_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17641 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 25 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.21 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.49 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_BILE_ACID_METABOLISM | NES=1.97 | NOM p=0.00e+00 | FDR q=2.27e-04 - HALLMARK_PEROXISOME | NES=1.86 | NOM p=0.00e+00 | FDR q=7.27e-04 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.80 | NOM p=0.00e+00 | FDR q=7.58e-04 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.69 | NOM p=3.11e-03 | FDR q=4.16e-03 - HALLMARK_APOPTOSIS | NES=1.55 | NOM p=4.21e-03 | FDR q=2.16e-02 - HALLMARK_COAGULATION | NES=1.47 | NOM p=1.12e-02 | FDR q=4.47e-02 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.46 | NOM p=4.00e-03 | FDR q=4.76e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_PROTEIN_SECRETION | NES=-2.41 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=-1.76 | NOM p=0.00e+00 ... [413 more characters]

reasoning: paper reports GO for up/down DEGs (S2.7.p1)

### enrichment (valid, failed)

final: {"organism": "Mouse", "subset": "primary/grp_PBS_PoWeR_vs_PBS_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": [], "summary": "No significant DEGs found with padj < 0.05 and |log2FC| > 0.0 (direction=down). Cannot run enrichment.", "execution_error": "no output written: No significant DEGs found with padj < 0.05 and |log2FC| > 0.0 (direction=down). Cannot run enrichment."}

reasoning: down-regulated ORA

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "primary/grp_C26_PoWeR_vs_C26_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\ora_up\\DEG_results_grp_C26_PoWeR_vs_C26_SED_GO_Biological_Process_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\ora_up\\DEG_results_grp_C26_PoWeR_vs_C26_SED_GO_Cellular_Component_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\ora_up\\DEG_results_grp_C26_PoWeR_vs_C26_SED_GO_Molecular_Function_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\ora_up\\DEG_results_grp_C26_PoWeR_vs_C26_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 139 Mouse genes (direction=up, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Pyruvate Metabolic Process (GO:0006090) | padj=1.55e-06 | overlap=8/50 | genes=PDHX;TPI1;PKM; ... [1247 more characters]

reasoning: paper FIG8G: up GO terms aerobic respiration / mitochondria

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "primary/grp_C26_PoWeR_vs_C26_SED", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\gsea\\DEG_results_grp_C26_PoWeR_vs_C26_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17641 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 34 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.97 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.57 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.18 | NOM p=0.00e+00 | FDR q=2.66e-04 - HALLMARK_BILE_ACID_METABOLISM | NES=1.50 | NOM p=9.84e-03 | FDR q=2.89e-02 - HALLMARK_MYOGENESIS | NES=1.42 | NOM p=1.35e-02 | FDR q=4.48e-02 - HALLMARK_PEROXISOME | NES=1.30 | NOM p=5.18e-02 | FDR q=1.03e-01 - HALLMARK_GLYCOLYSIS | NES=1.30 | NOM p=4.12e-02 | FDR q=8.84e-02 - HALLMARK_MTORC1_SIGNALING | NES=1.19 | NOM p=7.08e-02 | FDR q=1.88e-01 - HALLMARK_HEME_METABOLISM | NES=1.07 | NOM p=2.58e-01 | FDR q=3.78e-01 - HALLMARK_PI3K_AKT_MTOR_SIGNALING | NES=1.06 | NOM p=3.51e-01 | FDR q=3.58e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=-2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=-2.00 | NOM p=0.00e+00 | FDR q=0.00e+00 ... [413 more characters]

reasoning: paper FIG8G: up GO terms aerobic respiration / mitochondria

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "primary/grp_C26_PoWeR_vs_C26_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\ora_down\\DEG_results_grp_C26_PoWeR_vs_C26_SED_GO_Biological_Process_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\ora_down\\DEG_results_grp_C26_PoWeR_vs_C26_SED_GO_Cellular_Component_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\ora_down\\DEG_results_grp_C26_PoWeR_vs_C26_SED_GO_Molecular_Function_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_10/run/GSE324100\\results\\enrichment_primary_grp_C26_PoWeR_vs_C26_SED\\ora_down\\DEG_results_grp_C26_PoWeR_vs_C26_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 116 Mouse genes (direction=down, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Regulation Of Apoptotic Cell Clearance (GO:2000425) | padj=3.43e-05 | overlap=4/7 ... [1257 more characters]

reasoning: paper FIG8H: down GO terms ECM / macrophage activation

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["paper used DESeq2 on raw counts; only normalized counts deposited, so limma on log2(normalized+1) is used", "n = 5-6 per cell (2-3 per sex); per-sex analyses are exploratory"], "results": {"primary/grp_PBS_PoWeR_vs_PBS_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 0}, "primary/grp_C26_SED_vs_PBS_SED": {"n_deg": 2165, "up": 1046, "down": 1119, "rule": "padj < 0.05", "audit_n": 1362}, "primary/grp_C26_PoWeR_vs_C26_SED": {"n_deg": 255, "up": 139, "down": 116, "rule": "padj < 0.05", "audit_n": 177}, "sex_adjusted/grp_PBS_PoWeR_vs_PBS_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 0}, "sex_adjusted/grp_C26_SED_vs_PBS_SED": {"n_deg": 2502, "up": 1209, "down": 1293, "rule": "padj < 0.05", "audit_n": 1539}, "sex_adjusted/grp_C26_PoWeR_vs_C26_SED": {"n_deg": 419, "up": 205, "down": 214, "rule": "padj < 0.05", "audit_n": 277}, "female_only/grp_PBS_PoWeR_vs_PBS_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 0}, "female_only/grp_C26_SED_vs_PBS_SED": {"n_deg": 1965, "up": 934, "down": 1031, "rule": "padj < 0.05", "audit_n": 1507}, "female_only/grp_C26_PoWeR_vs_C26_SED": {"n_deg": 620, "up": 362, "down": 258, "rule": "padj < 0.05", "audit_n": 507}, "male_only/grp_PBS_PoWeR_vs_PBS_SED": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 0}, "male_only/grp_C26_SED_vs_PBS_SED": {"n_deg": 19, "up": 15, "down": 4, "rule": "padj < 0.05", "audit_n": 19}, "mal ... [1267 more characters]

reasoning: Paper counts and named genes from S3.7.p1.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Covariance | pass | not_required; sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
- | Sex | pass | Sex inference completed on 22 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "input matrix",
    "paper": "DESeq2 on raw counts (S2.7.p1)",
    "data": "only DESeq2 median-ratio normalized counts deposited, samples as rows",
    "disposition": "declared_deviation"
  },
  {
    "item": "matrix orientation",
    "paper": "n/a",
    "data": "deposited file is samples x genes with three label columns; transposed by prep_transpose.py after checking labels against GEO",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID42241015 / GSE324100

Paper: Exercise training prior to and during cancer in mice (PoWeR, C26 cachexia), PMC13370699.
Decision maker: Claude Opus 5.5 (Claude Code session). Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Validator: 19 records, 0 errors. Status: finished, route `declared_deviation`.

## What ran

- Inspect: `inspect_GSE324100.json`. The only matrix is `GSE324100_C26_PoWeR_Prevention_Gastroc_RNA-seq_Normalized_counts.txt.gz`. It holds DESeq2 median-ratio normalized counts: non-integer (integer fraction 0.03), and data_processing says "Normalized with DESeq2 median ratio". The file is **samples x genes** and has 3 label columns.
- Prep: `prep_transpose.py`. It checks the file's own Group/Sex labels against the GEO title/sex for all 22 libraries (all agree), then writes `GSE324100_normalized_counts_genes_x_samples.csv` (17725 x 22).
- Alignment: exact match on library name, which comes from the GEO `description` ("Library name: P1_S25"; one entry has a trailing underscore). 22/22 samples matched. `grp` = tumour (PBS/C26) x intervention (SED/PoWeR): PBS_SED 6, PBS_PoWeR 6, C26_SED 5, C26_PoWeR 5. These are the same n as the FIG8 legend.
- Suitability: analyzable, 7/7 comparisons. Sex inference agreed with the metadata.
- Method: limma on log2(x+1), one model `~ grp` on all 22 samples, with planned pairwise contrasts.
  - The paper's route (DESeq2 on raw counts, Partek) is blocked because raw counts were not deposited. This is a declared deviation.
  - Sensitivity: `~ sex + grp`.
  - Exploratory: separate female-only and male-only fits. The paper's Appendix FIG16 stratifies by sex.
- Threshold: the paper's rule, BH FDR < 0.05 with no fold-change cutoff (S2.7.p1), applied with `paper_on_deviation_route`. Audit rule: also |log2FC| > log2(1.5).
- Enrichment (separate from DE):
  - ORA up/down (Enrichr GO + KEGG) and Hallmark GSEA for PBS PoWeR vs PBS SED and for C26 PoWeR vs C26 SED.
  - ORA for PBS PoWeR vs PBS SED failed by design, because there were 0 DEGs.

## DEG counts vs paper (BH FDR < 0.05, no FC rule)

| Contrast | Paper | Ours, primary ~grp | Sex-adjusted | Female only | Male only |
|---|---|---|---|---|---|
| PBS PoWeR vs PBS SED (exercise, healthy) | 42 | 0 | 0 | 0 | 0 |
| C26 SED vs PBS SED (tumour) | 2740 | 2165 (1046 up / 1119 down) | 2502 | 1965 | 19 |
| C26 PoWeR vs C26 SED (exercise, tumour) | 963 | 255 (139 up / 116 down) | 419 | 620 | 0 |

The paper's named genes go the same direction ... [2048 more characters]
