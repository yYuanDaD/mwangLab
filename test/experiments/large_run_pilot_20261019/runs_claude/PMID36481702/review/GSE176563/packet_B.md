# Review packet B (the analysis' decisions): GSE176563

## Mechanical flags

- **other_rule_matches_paper**: {"table": "grp_EPS_vs_CTRL", "paper": 774, "applied": 218, "applied_rule": "pvalue < 0.01 and |log2FoldChange| > 1", "closest_rule": "pvalue<0.01", "closest_n": 794, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_EPS_vs_CTRL | 774 | 218 | pvalue < 0.01 and |log2FoldChange| > 1 | 9 | 9 | 9 | 72 | 2392 | 1123 | 332 | 794 | 0.066 | 0.125 |

## Samples per design level

### `grp`
- **CTRL** (3): GSM5369067 / CL1_RNA-seq; GSM5369068 / CL3_RNA-seq; GSM5369069 / CL4_RNA-seq
- **EPS** (4): GSM5369070 / L1_RNA-seq; GSM5369071 / L2_RNA-seq; GSM5369072 / L3_RNA-seq; GSM5369073 / L4_RNA-seq

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE176563", "GSE126001"], "assay": "bulk RNA-seq (HiSeq 2500, 2x100 PE, STAR to GRCm38), C2C12 myotubes", "primary_estimand": "Effect of 24 h electrical pulse stimulation (in vitro exercise model) vs unstimulated control on C2C12 myotube gene expression", "factors": {"grp": ["CTRL (unstimulated, n=3)", "EPS (24 h EPS, n=4)"]}, "sample_inclusion": "all 7 deposited samples; control n=3, EPS n=4 (FIG1 legend b,c)", "planned_contrasts": ["EPS vs control (S2.1.p1, FIG1; paper: 774 DEGs, 406 up / 368 down)"], "paper_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S2.1.p1; FIG1"}, "paper_threshold_methods_variant": {"metric": "pvalue", "cutoff": 0.001, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": true, "source_locator": "S4.6.p1"}, "paper_method": "edgeR negative-binomial test on count data (S4.6.p1, S4.8.p1); CPM log2-transformed and quantile-normalized for expression display", "repeated_measure_unit": "none (independent culture wells)", "paper_results": "774 DEGs (406 up, 368 down); Table 2 up-regulated secreted genes incl. Prl2c2 logFC 8.80, Areg 2.99, Cxcl1, Cxcl5, Il1b, Gdf15; exercise signature up: Mt1, Mt2, Atf3; down: Myh4, Fam78a, Ppapdc3, Chrne, Kctd12, Il12a (FIG3a,b, S2.2.p3)", "secondary_use_of_GSE126001": "public in vivo dataset (TAB1: 20-week WT C57BL/6J male, 5 weeks treadmill, gastrocnemius) used only as classifier test se ... [99 more characters]

reasoning: S2.1.p1 and FIG1 define the primary contrast (control n=3 vs EPS n=4) and the 774-DEG count with 'P < 0.01, fold change > 2'. S4.6.p1 states edgeR on counts but a different rule (P < 0.001, fold difference >= 2). The Results/Figure rule is the one tied to the reported 774 count, so it is the paper_threshold; the Methods rule is carried as audit_threshold. DA.p1 names GSE176563 as the paper's own data.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["DA.p1 and S4.6.p1 name GSE176563", "GEO source C2C12 cell, EPS vs No treatment, 3+4 samples matches FIG1 n", "contact Seon-Kyu Kim, KRIBB = author S.K.K. (BK2.p1)", "submission Jun 2021, public Dec 2022 = paper publication"], "accession": "GSE176563", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE176563\\GSE176563_metadata.csv"}

reasoning: Own deposit of the paper; sample counts and treatment labels match FIG1.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 7, "n_metadata": 7, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.1.electrical pulse stimulation", "regex": "^(No treatment|treated by electrical pulse stimulation)$", "recode": {"No treatment": "CTRL", "treated by electrical pulse stimulation": "EPS"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\aligned\\design_metadata.csv", "sha256": "c392f3c6288bf593911c1f75f7038e1cf7034ccf3e124dbdbf2ef3bf4f4eb02c", "levels": {"grp": {"EPS": 4, "CTRL": 3}}}}

reasoning: Tar-merged matrix columns become GSM ids and match the metadata index exactly (7/7). Group from the EPS characteristic; titles CL* = control, L* = EPS agree.

### matrix (valid, not_started)

final: {"matrix_type": "linear_normalized (CPM)", "recommended_method": "limma on log2(x+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\aligned\\aligned_matrix.csv", "sha256": "031fbb0f0c6115ccbf881a84c87749de5a8b3d18149286a1809033801fbeebde", "n_features": 26607, "n_samples": 7, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 80884.37836, "median": 0.406859819, "integer_fraction": 0.3877, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample files are named *_CPM.txt.gz; GEO Supplementary_files_format_and_content: 'CPM values of mRNA'; every column sums to exactly 1e6; values non-integer (integer fraction 0.39 from zeros). No raw counts or library sizes deposited, so the paper's edgeR input is unavailable. Paper input is counts for edgeR (S4.6.p1).

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "CTRL", "treatment": "EPS", "estimand_type": "causal (randomized in vitro stimulation)", "contrasts": [{"name": "grp_EPS_vs_CTRL", "control": "CTRL", "treatment": "EPS", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Single two-level factor exactly as in FIG1; no other varying metadata column.

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 7, "n_columns": 2, "columns": ["Intercept", "grp_EPS"], "rank": 2, "full_rank": true, "residual_df": 5, "levels": {"grp": {"EPS": 4, "CTRL": 3}}, "cells": [{"cell": ["CTRL"], "n": 3}, {"cell": ["EPS"], "n": 4}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 7, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 7, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.electrical pulse stimulation", "n_levels": 2, "status": "complete_confounding", "crosstab": {"CTRL": {"No treatment": 3, "treated by electrical pulse stimulation": 0}, "EPS": {"No treatment": 0, "treated by electrical pulse stimulation": 4}}}, {"column": "molecule_ch1", "n_levels": 1, "status": "constant"}, {"column": "extrac ... [1358 more characters]

reasoning: Independent culture wells; no batch, lane or pairing recorded in GEO or paper.

### method (valid, not_started)

final: {"matrix_type": "linear_normalized (CPM)", "method": "limma (moderated t, empirical Bayes) on log2(CPM+1)", "formula": "~ grp", "paper_route": {"method": "edgeR negative-binomial on counts", "status": "blocked", "reason": "only CPM deposited in GSE176563 (no counts, no library sizes); CPM cannot be converted back to counts and must not be rounded"}, "deviations": ["limma-trend style limma on log2(CPM+1) instead of edgeR on counts", "no quantile normalization (paper S4.6.p1 mentions log2 + quantile for expression data; limma run on log2 CPM only)"], "transform": "log2(x+1)"}

reasoning: Matrix policy: linear normalized expression -> log2(x+1) -> limma. Since values are CPM, log2(x+1) = log2(CPM+1).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.001, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "effect_inclusive": true}, "deviation_note": "Paper rule applied on the limma deviation route. Methods (S4.6.p1) rule P < 0.001 and FC >= 2 is the audit rule."}

reasoning: S2.1.p1/FIG1: P < 0.01, fold change > 2 -> raw p < 0.01 and |log2FC| > 1, tied to the 774 count. S4.6.p1 alternative is recorded as audit.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_EPS_vs_CTRL", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 7, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\results\\grp_EPS_vs_CTRL\\DEG_results_EPS_vs_CTRL.csv"], "counts": {"grp_EPS_vs_CTRL": {"applied": {"rule": "pvalue < 0.01 and |log2FoldChange| > 1", "n_tested": 19144, "n_significant": 218, "n_up": 143, "n_down": 75, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.001 and |log2FoldChange| >= 1", "n_tested": 19144, "n_significant": 79, "n_up": 50, "n_down": 29, "deg_sanity": "ok"}}}}

reasoning: Paper's EPS vs control contrast on the deviation route (limma, log2(CPM+1)).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_EPS_vs_CTRL_cpmfilt", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 7, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\results\\grp_EPS_vs_CTRL_cpmfilt\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36481702\\GSE176563\\results\\grp_EPS_vs_CTRL_cpmfilt\\DEG_results_EPS_vs_CTRL.csv"], "counts": {"grp_EPS_vs_CTRL_cpmfilt": {"applied": {"rule": "pvalue < 0.01 and |log2FoldChange| > 1", "n_tested": 12360, "n_significant": 310, "n_up": 216, "n_down": 94, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.001 and |log2FoldChange| >= 1", "n_tested": 12360, "n_significant": 172, "n_up": 112, "n_down": 60, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: drop genes with CPM < 1 in fewer than 3 samples (edgeR-style expression filter), since near-zero genes can produce large log2FC with few reads.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["edgeR on counts blocked (CPM only); limma on log2(CPM+1) used", "paper reports two different thresholds (S2.1.p1 vs S4.6.p1); Results rule applied, Methods rule audited", "n=3 vs 4"], "results": {"grp_EPS_vs_CTRL": {"n_deg": 218, "up": 143, "down": 75, "rule": "pvalue < 0.01 and |log2FoldChange| > 1", "audit_n": 79}, "grp_EPS_vs_CTRL_cpmfilt": {"n_deg": 310, "up": 216, "down": 94, "rule": "pvalue < 0.01 and |log2FoldChange| > 1", "audit_n": 172}}, "paper_counts": {"grp_EPS_vs_CTRL": 774}, "comparison": {"grp_EPS_vs_CTRL": {"ours": 218, "paper": 774}}, "paper_gene_check": {"grp_EPS_vs_CTRL": {"Prl2c2": {"AveExpr": 0.763, "log2FoldChange": 1.3353, "padj": 0.539, "pvalue": 0.115}, "Prl2c3": {"AveExpr": 1.3387, "log2FoldChange": 2.2459, "padj": 0.34, "pvalue": 0.0317}, "F13a1": {"AveExpr": 1.4696, "log2FoldChange": 1.8143, "padj": 0.137, "pvalue": 0.00151}, "Areg": {"AveExpr": 0.6638, "log2FoldChange": 0.8545, "padj": 0.332, "pvalue": 0.0294}, "Cxcl1": {"AveExpr": 1.0488, "log2FoldChange": 0.965, "padj": 0.329, "pvalue": 0.0289}, "Cxcl5": {"AveExpr": 2.3943, "log2FoldChange": 1.5408, "padj": 0.492, "pvalue": 0.0899}, "Il1b": {"AveExpr": 2.9895, "log2FoldChange": 1.9133, "padj": 0.143, "pvalue": 0.00168}, "Gdf15": {"AveExpr": 2.195, "log2FoldChange": 1.4401, "padj": 0.233, "pvalue": 0.00857}, "Mt1": {"AveExpr": 7.8655, "log2FoldChange": 2.0779, "padj": 0.164, "pvalue": 0.00279}, "Mt2": {"AveExpr": 7.1641, "log2FoldChange": 2.6288, "padj ... [669 more characters]

reasoning: Up expected: Prl2c2..Gdf15 (TAB2), Mt1, Mt2, Atf3 (FIG3a); down expected: Myh4, Fam78a, Ppapdc3, Chrne, Kctd12, Il12a (FIG3b).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 7 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG threshold",
    "paper": "S2.1.p1/FIG1: P < 0.01 and FC > 2 (774 DEGs); S4.6.p1: P < 0.001 and FC >= 2",
    "data": "n/a",
    "disposition": "Results rule applied (tied to 774); Methods rule as audit_threshold"
  },
  {
    "item": "DE input",
    "paper": "edgeR on count data (S4.6.p1)",
    "data": "GEO holds CPM only (columns sum to 1e6)",
    "disposition": "declared deviation: limma on log2(CPM+1)"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 36481702 (EPS cellular exercise model; GSE176563 + GSE126001)

Route: case spec (`case_spec.json`) run with `python -m tools.case_runner execute`. Run status: completed. Contract validator: 22 records, 0 errors. Preflight skipped as instructed. No enrichment was run, because the paper's pathway work is IPA only and the request asks about gene expression.

## What ran

| Case | Contrast | Role | Method | Threshold (source) | Ours (up/down) | Paper |
|---|---|---|---|---|---|---|
| GSE176563 | EPS (n=4) vs CTRL (n=3), C2C12 myotubes | primary | limma on log2(CPM+1) | raw P < 0.01 and \|log2FC\| > 1 (paper, S2.1.p1/FIG1, applied on the deviation route) | **218** (143/75) | **774** (406/368) |
| GSE176563 | same, audit rule | audit | same | raw P < 0.001 and \|log2FC\| >= 1 (Methods S4.6.p1) | 79 | n/a |
| GSE176563 | same, CPM >= 1 in >= 3 samples (12,360 genes kept) | sensitivity | same | paper rule | 310 (216/94); audit 172 | 774 |
| GSE126001 | WT trained vs untrained (4 vs 4), gastrocnemius | primary | limma on log2(RPKM+1) | BH < 0.05 (workflow_default; the paper gives no DE rule for this public dataset) | 6 (6/0); 11 under the audit rule P < 0.01 and \|log2FC\| > 1 | none reported |
| GSE126001 | Il13-/- trained vs untrained (4 vs 4) | exploratory | same | workflow_default | 3 (2/1) | not used by the paper |

Paper genes in GSE176563: all 17 checked genes move in the paper's direction. Up: Prl2c2, Prl2c3, F13a1, Areg (log2FC 0.85, p 0.029), Cxcl1, Cxcl5, Il1b, Gdf15, Mt1 (+2.08), Mt2 (+2.63) and Atf3. Down: Myh4 (-2.48), Fam78a, Ppapdc3, Chrne, Kctd12 and Il12a. Several of these pass the paper rule, for example Mt1, Mt2, Myh4, Fam78a, Chrne, Kctd12, Il1b and F13a1, as long as their log2FC is above 1. Areg, Cxcl1 and Prl2c2 do not reach p < 0.01. Our log2FC values are much smaller than the paper's edgeR logFC for low-CPM genes: Prl2c2 is 1.34 here against 8.80 in the paper. The cause is the +1 offset on log2(CPM), which compresses low-expression fold changes.

Paper genes in GSE126001 (WT): Myh4 (log2FC -0.26, p 0.007), Il12a (-0.34, p 0.03), Fam78a, Ppapdc3 and Chrne go down, which agrees with the paper's direction. None are significant after BH. Mt1, Mt2 and Kctd12 do not go up as the signature expects: they are flat or slightly the other way. Atf3 is slightly up and not significant. Areg is zero in all 16 samples, so limma's zero-variance filter dropped it. This fits the paper's claim, which was about agreement across at least six da ... [3048 more characters]
