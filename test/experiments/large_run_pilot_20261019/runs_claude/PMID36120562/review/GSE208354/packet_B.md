# Review packet B (the analysis' decisions): GSE208354

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_HFEXT_vs_HF | 690 | 97 | pvalue < 0.05 and |log2FoldChange| > 1 | 0 | 0 | 0 | 27 | 1538 | 367 | 97 | 520 | 0.071 | 0.128 |

## Samples per design level

### `grp`
- **HF** (3): GSM6341818 / HF36-input; GSM6341820 / HF37-input; GSM6341822 / HF43-input
- **HFEXT** (3): GSM6341824 / HFEXT6-input; GSM6341826 / HFEXT7-input; GSM6341828 / HFEXT14-input

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE208354"], "assay": "MeRIP-seq (m6A IP) plus input RNA-seq of mouse heart; the input libraries are the mRNA-expression arm (S2.7.p1, S2.8.p1)", "primary_estimand": "Effect of 8 weeks moderate treadmill exercise on heart mRNA expression in two-hit (HFD + L-NAME) HFpEF mice: HFpEF+EXT vs sedentary HFpEF", "sample_inclusion": "n = 3 male C57BL/6J HFpEF and 3 HFpEF+EXT hearts for RNA-seq (S2.8.p1, S3.4.p1 'n = 3 per group'); IP libraries are the m6A arm, not expression", "factors": {"grp": ["HF (sedentary HFpEF, GEO 'control')", "HFEXT (HFpEF + exercise)"]}, "planned_contrasts": ["HFpEF+EXT vs HFpEF (S3.4.p1; paper: 690 DEGs, 267 up, 423 down)"], "repeated_measure_unit": "none; independent animals", "normalization": "featureCounts then DESeq2 (S2.8.p1); FPKM shown in Fig 3A", "paper_method": "DESeq2 on featureCounts counts, two groups (S2.8.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S3.4.p1 (FC > 2, p < 0.05)"}, "paper_results": "690 DEGs (267 up, 423 down) HFpEF+EXT vs HFpEF; Table 3 mRNA log2FC: Casp12 -1.27, Capn2 -0.31, Fas -1.03, Casp7 -0.54, Jun -0.99, Pdia3 -0.50, Tnnt2 +0.73, Mef2a +0.44, Adrb1 +0.53, Agtr1a +0.53"}

reasoning: Exercise effect within HFpEF mice. The paper's 'control' in GEO is the sedentary HFpEF group (S1.p4 'HFpEF + EXT and control (HFpEF) mice'). The m6A peak / differential methylation results are a different assay and are out of scope for gene expression.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE208354\\GSE208354_All_comparison_mRNA.csv", "owned": true, "checks": ["S5.p1 names GSE208354", "matrix columns HF36/37/43 and HFEXT6/7/14 -input equal GEO titles of the input RNA-seq GSMs", "organism Mus musculus, heart, matches S2.1.p1"], "accession": "GSE208354", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE208354\\GSE208354_metadata.csv"}

reasoning: Data availability statement names GSE208354; the supplementary All_comparison_mRNA file is the series' own input-library expression table.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 6, "n_metadata": 12, "coverage": 0.5, "unmatched_matrix_columns": ["HF40-input"], "unmatched_metadata_samples": ["GSM6341819", "GSM6341821", "GSM6341823", "GSM6341825", "GSM6341827", "GSM6341829"], "excluded_samples": {"GSM6341819": "m6A IP library (RIP-Seq), not an expression sample", "GSM6341821": "m6A IP library (RIP-Seq), not an expression sample", "GSM6341823": "m6A IP library (RIP-Seq), not an expression sample", "GSM6341825": "m6A IP library (RIP-Seq), not an expression sample", "GSM6341827": "m6A IP library (RIP-Seq), not an expression sample", "GSM6341829": "m6A IP library (RIP-Seq), not an expression sample"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\aligned\\aligned_metadata_kept.csv", "columns": {"grp": {"source": "title", "regex": "^(HFEXT|HF)\\d+-"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\aligned\\design_metadata.csv", "sha256": "9125c32e02692cf0cfeb0721ae1231eb3ca822d29a43c434c978b7a962b3ad6d", "levels": {"grp": {"HF": 3, "HFEXT": 3}}}}

reasoning: Exact match of matrix columns to GEO title. Matrix column HF40-input has no GSM in the series (only HF36/37/43 deposited for HFpEF) and the paper states n = 3 per group, so it stays unmatched and is dropped. grp from the title prefix: HF = sedentary HFpEF, HFEXT = HFpEF + exercise.

### matrix (valid, not_started)

final: {"source": "GSE208354_All_comparison_mRNA.csv (supplementary, input libraries)", "paper_input": "featureCounts read counts into DESeq2 (S2.8.p1)", "matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\aligned\\aligned_matrix.csv", "sha256": "b89a3c689d9d80d2530de635bccf20e56de132b096d695b1798ac8dd0aa3bb35", "n_features": 53465, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 847950.467302331, "median": 0.0, "integer_fraction": 0.6018, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Non-integer values (integer fraction 0.60 driven by zeros), small fractional values for low genes, column sums ~0.9-1.3e6 (not exactly 1e6, so FPKM not TPM); paper Fig 3A shows 'FPKM distribution' of these samples (S3.4.p1). Raw counts are not deposited.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "HF", "treatment": "HFEXT", "contrasts": [{"name": "grp_HFEXT_vs_HF", "control": "HF", "treatment": "HFEXT", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Two-arm design, 3 vs 3 independent mice, all male, one tissue (S2.8.p1, S3.4.p1). Exercise is randomized within HFpEF mice, so the contrast is interventional.

rejected alternatives: [{"value": "include HF40-input as a 4th HFpEF sample", "reason_rejected": "no GEO sample record and the paper analyses n = 3 per group"}, {"value": "IP vs input / methylation contrast", "reason_rejected": "m6A enrichment, not gene expression"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 6, "n_columns": 2, "columns": ["Intercept", "grp_HFEXT"], "rank": 2, "full_rank": true, "residual_df": 4, "levels": {"grp": {"HF": 3, "HFEXT": 3}}, "cells": [{"cell": ["HF"], "n": 3}, {"cell": ["HFEXT"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 6, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 6, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 2, "status": "complete_confounding", "crosstab": {"HF": {"control input for m6A": 3, "exercise group input for m6A": 0}, "HFEXT": {"control input for m6A": 0, "exercise group input for m6A": 3}}}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.condition", "n_levels": 2, "status": "complete_confounding", "crosstab":  ... [1519 more characters]

reasoning: Independent animals, single sex, no batch or lane recorded in GEO.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (trend, empirical Bayes) on log2(FPKM+1)", "formula": "~ grp", "paper_route": {"method": "DESeq2 on featureCounts counts", "status": "blocked", "reason": "only FPKM deposited; no raw counts in GEO supplementary or as GSM tables"}, "deviations": ["limma on log2(FPKM+1) instead of DESeq2 on counts", "genes kept with FPKM >= 1 in at least 3 of the 6 samples (paper states no filter; DESeq2 uses independent filtering)"], "transform": "log2(x+1)"}

reasoning: Matrix-method policy: log-transformed FPKM goes to limma. A low-expression filter avoids zero-inflated near-constant genes distorting the limma-trend prior.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "deviation_note": "Paper rule (raw p < 0.05, FC > 2) applied to limma results instead of DESeq2; BH FDR < 0.05 reported as audit."}

reasoning: S3.4.p1 and Fig 3B: fold change > 2 and p < 0.05 (raw p) -> |log2FC| > 1.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_HFEXT_vs_HF", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\grp_HFEXT_vs_HF\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\grp_HFEXT_vs_HF\\DEG_results_HFEXT_vs_HF.csv"], "counts": {"grp_HFEXT_vs_HF": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 12057, "n_significant": 97, "n_up": 47, "n_down": 50, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12057, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Two-group limma on log2(FPKM+1), HFpEF+EXT vs HFpEF.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_HFEXT_vs_HF_nofilter", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\grp_HFEXT_vs_HF_nofilter\\DEG_results_HFEXT_vs_HF.csv"], "counts": {"grp_HFEXT_vs_HF_nofilter": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 26678, "n_significant": 108, "n_up": 49, "n_down": 59, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 26678, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Same contrast without the FPKM >= 1 filter, closer to the paper's unfiltered DEG call; tests how much of the count gap comes from the filter.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_HFEXT_vs_HF", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\ora_up\\DEG_results_HFEXT_vs_HF_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\ora_up\\DEG_results_HFEXT_vs_HF_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\ora_up\\DEG_results_HFEXT_vs_HF_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\ora_up\\DEG_results_HFEXT_vs_HF_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 36 Mouse genes (direction=up, pvalue<0.05, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Glycolytic Process (GO:0006096) | padj=1.66e-01 | overlap=2/29 | genes=ALDOB;ENO3 - Carbohydrate Catabolic Process (GO:0016052) | padj=1.66e-01  ... [1195 more characters]

reasoning: paper reports GO/KEGG of up-regulated mRNAs (Fig 3D)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_HFEXT_vs_HF", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\ora_down\\DEG_results_HFEXT_vs_HF_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\ora_down\\DEG_results_HFEXT_vs_HF_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\ora_down\\DEG_results_HFEXT_vs_HF_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\ora_down\\DEG_results_HFEXT_vs_HF_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 46 Mouse genes (direction=down, pvalue<0.05, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Negative Regulation Of Angiogenesis (GO:0016525) | padj=9.03e-03 | overlap=4/86 | genes=NPPB;CLDN5;SERPINE1;KLF2 - acyl-CoA Metaboli ... [1205 more characters]

reasoning: paper reports GO/KEGG of down-regulated mRNAs (Fig 3E)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_HFEXT_vs_HF", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36120562\\GSE208354\\results\\enrichment_grp_HFEXT_vs_HF\\gsea\\DEG_results_HFEXT_vs_HF_GSEA_Hallmark.csv"], "summary": "GSEA complete on 11855 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 38 significant at FDR q < 0.25. ### Top 8 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.59 | NOM p=0.00e+00 | FDR q=4.08e-02 - HALLMARK_MYOGENESIS | NES=1.47 | NOM p=2.47e-03 | FDR q=6.96e-02 - HALLMARK_KRAS_SIGNALING_DN | NES=1.43 | NOM p=4.32e-02 | FDR q=6.39e-02 - HALLMARK_GLYCOLYSIS | NES=1.24 | NOM p=7.73e-02 | FDR q=2.05e-01 - HALLMARK_SPERMATOGENESIS | NES=1.07 | NOM p=3.42e-01 | FDR q=5.03e-01 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=0.94 | NOM p=5.58e-01 | FDR q=8.03e-01 - HALLMARK_NOTCH_SIGNALING | NES=0.82 | NOM p=7.41e-01 | FDR q=9.74e-01 - HALLMARK_APICAL_SURFACE | NES=0.77 | NOM p=8.23e-01 | FDR q=9.19e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=-2.61 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-2.56 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-2.46 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=-2.19 | NOM p=0.00e+00 | FDR q=0 ... [387 more characters]

reasoning: Hallmark GSEA on full ranking as supporting pathway view

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["n = 3 per group; raw-p threshold with no multiple-testing correction, as in the paper", "limma on FPKM instead of DESeq2 on counts; counts not directly comparable", "Exercise effect is within HFpEF mice only; no healthy exercise arm sequenced"], "results": {"grp_HFEXT_vs_HF": {"n_deg": 97, "up": 47, "down": 50, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 0}, "grp_HFEXT_vs_HF_nofilter": {"n_deg": 108, "up": 49, "down": 59, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 0}}, "paper_counts": {"grp_HFEXT_vs_HF": 690}, "comparison": {"grp_HFEXT_vs_HF": {"ours": 97, "paper": 690}}, "paper_gene_check": {"grp_HFEXT_vs_HF": {"Casp12": {"AveExpr": 2.1758, "log2FoldChange": -0.6949, "padj": 0.509, "pvalue": 0.105}, "Capn2": {"AveExpr": 3.4271, "log2FoldChange": -0.2206, "padj": 0.389, "pvalue": 0.0485}, "Fas": {"AveExpr": 2.6747, "log2FoldChange": -0.4974, "padj": 0.288, "pvalue": 0.0185}, "Casp7": {"AveExpr": 2.2951, "log2FoldChange": -0.3484, "padj": 0.403, "pvalue": 0.0547}, "Jun": {"AveExpr": 4.1604, "log2FoldChange": -0.8721, "padj": 0.133, "pvalue": 0.00134}, "Pdia3": {"AveExpr": 4.8917, "log2FoldChange": -0.3488, "padj": 0.273, "pvalue": 0.0159}, "Tnnt2": {"AveExpr": 10.0406, "log2FoldChange": 0.6466, "padj": 0.129, "pvalue": 0.00128}, "Mef2a": {"AveExpr": 4.0736, "log2FoldChange": 0.3384, "padj": 0.289, "pvalue": 0.019}, "Adrb1": {"AveExpr": 2.9854, "log2FoldChange": 0.3469, "padj": 0.331, "pvalue": 0.02 ... [95 more characters]

reasoning: Paper reports 690 DEGs and Table 3 mRNA log2FC signs for 10 genes (6 down, 4 up).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "HF40-input column",
    "paper": "n = 3 HFpEF mice sequenced",
    "data": "matrix has 4 HFpEF input columns; HF40 has no GSM",
    "disposition": "executable_without_change"
  },
  {
    "item": "matrix type",
    "paper": "DESeq2 on featureCounts counts",
    "data": "only FPKM deposited",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID36120562 / GSE208354

## What ran
- `inspect GSE208354` (downloaded to `data/GSE208354`), then the case spec route: `python -m tools.case_runner execute case_spec.json` (run twice; the first attempt is in `_previous/`). The validator passed: 14 records, 0 errors.
- Study: HFpEF mice (HFD + L-NAME) with 8 weeks of treadmill exercise (HFpEF+EXT) vs sedentary HFpEF. Heart input RNA-seq, 3 vs 3 (S2.8.p1, S3.4.p1). The paper's "control" is sedentary HFpEF, which GEO labels `control`.
- Matrix: `GSE208354_All_comparison_mRNA.csv`, which holds **FPKM** values (fractional; column sums 0.9–1.3e6; Fig 3A shows FPKM). No raw counts were deposited.
- Alignment: exact match on GEO `title`, 6/6 input samples. I excluded the 6 m6A IP (RIP-Seq) GSMs. Matrix column `HF40-input` has no GSM record, and the paper says n = 3, so it was dropped.
- Primary (`grp_HFEXT_vs_HF`): limma-trend on log2(FPKM+1), `~ grp`. I kept genes with FPKM >= 1 in at least 3 samples (12,057 of 53,465).
- Sensitivity (`grp_HFEXT_vs_HF_nofilter`): the same model with no expression filter.
- Enrichment: Enrichr ORA (GO/KEGG) for up and down DEGs separately, plus Hallmark GSEA on the limma t ranking. All three completed.
- Out of scope: the m6A peak and differential-methylation analysis (MeRIP), because it measures a different assay.

## DEG counts vs paper
Paper threshold (S3.4.p1, Fig 3B): FC > 2 and raw p < 0.05, applied here as |log2FC| > 1, p < 0.05.

| Table | Ours (up/down) | Paper (up/down) |
|---|---|---|
| grp_HFEXT_vs_HF (primary, filtered) | 97 (47/50) | 690 (267/423) |
| grp_HFEXT_vs_HF_nofilter (sensitivity) | 108 (49/59) | — |
| audit, BH FDR < 0.05 | 0 | — |

The 10 Table 3 genes all have the same sign as in the paper:
- Down: Casp12, Capn2, Fas, Casp7, Jun, Pdia3.
- Up: Tnnt2, Mef2a, Adrb1, Agtr1a.

Our fold changes are slightly smaller, for example Jun −0.87 vs −0.99 and Tnnt2 +0.65 vs +0.73. Seven of the 10 have p < 0.05; Casp12, Casp7 and Agtr1a do not. No gene passes FDR < 0.05, so with n = 3 the result rests on raw p, as the paper's does.

Pathways are supporting only:
- Down-DEG KEGG: fatty acid elongation, unsaturated fatty acid biosynthesis, Apelin, PPAR.
- Up-DEG KEGG: glycolysis/gluconeogenesis.
- GSEA: OXPHOS is up in EXT (FDR 0.04); myogenesis is up (FDR 0.07).

These broadly fit the paper's "myocardial energy metabolism" theme. Apoptosis is not among our top KEGG terms.

## Deviations
1. **Method.** I used limma on log2(FPKM+1) instead of DESeq2 on feature ... [1265 more characters]
