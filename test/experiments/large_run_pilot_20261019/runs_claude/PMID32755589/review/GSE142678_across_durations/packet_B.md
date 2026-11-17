# Review packet B (the analysis' decisions): GSE142678_across_durations

## Mechanical flags

- none

## Samples per design level

### `group_raw`
- **Run** (12): GSM4237691 / ra; GSM4237693 / rb; GSM4237695 / rc; GSM4237697 / rd; GSM4237699 / re; GSM4237701 / rf; GSM4237703 / inra; GSM4237705 / inrb; GSM4237707 / inrc; GSM4237709 / inrd; GSM4237711 / inre; GSM4237713 / inrf
- **Sed** (12): GSM4237692 / la; GSM4237694 / lb; GSM4237696 / lc; GSM4237698 / ld; GSM4237700 / le; GSM4237702 / lf; GSM4237704 / inla; GSM4237706 / inlb; GSM4237708 / inlc; GSM4237710 / inld; GSM4237712 / inle; GSM4237714 / inlf

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE142678"], "assay": "RiboTag-seq (bulk RNA-seq, SMARTer Stranded Total RNA-Seq v2, HiSeq 2500 SE100) of HA-tagged ribosome IP (Nestin-CreERT2 lineage: adult-born DG neurons) and matched input (IN, whole dentate gyrus) RNA", "organism": "Mouse (female Nes-CreERT2::RiboTag, C57BL/6)", "primary_estimand": "Effect of voluntary wheel running vs sedentary on translating-mRNA expression in adult-born DG neurons (IP) and in DG tissue (IN), separately at 11, 18 and 27 days of running", "factors": {"group": ["running", "sedentary"], "time": ["11 days", "18 days", "27 days"], "fraction": ["IP (new neurons)", "IN (DG input)"]}, "sample_inclusion": "24 libraries = 2 fractions x 3 durations x 2 conditions x 2 replicates; each replicate is a pool of dentate gyri from 2-4 mice (S4.3.7.p1); 12 IP samples (S2.1.p2)", "planned_contrasts": ["Running vs Sedentary, IP, 11 days (S2.1.p3, Fig 1E; count only in figure)", "Running vs Sedentary, IP, 18 days (S4.3.8.p1: N=460 DEGs at Day-18, used for the IP trajectory)", "Running vs Sedentary, IP, 27 days (S2.1.p3 / Fig 1F: 508 unique + 36 shared = 544 DEGs)", "Running vs Sedentary, IN, 11 days (Fig 1E; count only in figure)", "Running vs Sedentary, IN, 18 days (Fig 1E; count only in figure)", "Running vs Sedentary, IN, 27 days (S2.1.p3: 88 unique + 36 shared = 124; S3.p5: 124 DEGs)", "Running vs Sedentary across all three durations, IP (S2.3.p1 / Fig 3A volcano: Rgs6 top up, Abca8a top down; count not stated)", "Running vs Sedentary  ... [1047 more characters]

reasoning: S2.1.p2 and S4.3.7.p1 define the RiboTag-seq experiment, the per-time running-vs-sedentary comparisons in IP and IN, and the EBSeq PPEE < 0.05 rule. Fig 1B/1E/1F give the 3-time x 2-fraction structure. Counts recoverable from text: IP 27d 544, IN 27d 124, IP 18d 460; the others are only in the Figure 1E bar chart. S2.3.p1 / FIG3 legend add a running-vs-sedentary comparison across all three time points (volcano, Fig 3A) with the top genes Rgs6 (up, IP only) and Abca8a (down, IP and IN).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_TPM_dedup.csv", "owned": true, "checks": ["Key resources table and S4.3.7.p1 name GEO GSE142678", "GEO series: Nes-CreERT2::RiboTag female mice, RiboTag IP and input, 11/18/27 days running vs sedentary, contact Xinyu Zhao (corresponding lab)", "24 samples = 12 IP + 12 IN, matching the 12 IP samples of S2.1.p2", "matrix GSE142678_nes_run_TPM.csv.gz: 24 columns matching GEO titles exactly"], "accession": "GSE142678", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE142678\\GSE142678_metadata.csv"}

reasoning: Paper deposits only GSE142678; the series design, strain, fractions and time points match the paper exactly.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\aligned\\aligned_metadata.csv", "columns": {"group_raw": {"alias_of": "characteristics_ch1.4.group", "recode": {"running mouse": "Run", "sedentary mouse": "Sed"}}, "time_raw": {"alias_of": "characteristics_ch1.3.treatment time", "recode": {"11 days": "D11", "18 days": "D18", "27 days": "D27"}}, "frac_raw": {"alias_of": "description", "recode": {"Ribosome IP sample": "IP", "input sample": "IN"}}, "pair": {"source": "title", "regex": "^(?:in)?[rl]([a-f])$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\aligned\\design_metadata.csv", "sha256": "3c09714d3d0eaf8a8b2eb18f42f164ea10e65265e71335a39e1379d219732c2a", "levels": {"group_raw": {"Run": 12, "Sed": 12}, "time_raw": {"D11": 8, "D18": 8, "D27": 8}, "frac_raw": {"IP": 12, "IN": 12}, "pair": {"a": 4, "b": 4, "c": 4, "d": 4, "e": 4, "f": 4}}}}

reasoning: inspect: metadata title equals the 24 matrix column names (24/24). Group, duration and fraction come from GEO characteristics/description (title prefix agrees: r = running, l = sedentary, in = input). pair = replicate letter a-f (shared by one running and one sedentary pool and by its IP/IN), derived only for the confounding check.

### matrix (valid, not_started)

final: {"source": "GSE142678_nes_run_TPM.csv.gz (only deposited matrix; per-sample supplementary files NONE)", "paper_input": "RSEM expected counts into EBSeq (not deposited)", "matrix_type": "TPM (RSEM, linear scale)", "recommended_method": "limma on log2(TPM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\aligned\\aligned_matrix.csv", "sha256": "b84433d5b065ec5df4c68fb52850ad5019a1b353c9ab2cab5000b2672f2e098b", "n_features": 23302, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 173621.87, "median": 7.35, "integer_fraction": 0.1212, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Every column sums to 1,000,000; 12% integer values, median 7.35, max 1.7e5; data_processing states CSV file with TPM values from RSEM. RSEM expected counts used by EBSeq are not deposited, so a count route is impossible; TPM must not be rounded into counts.

### design (valid, not_started)

final: {"analysis_type": "two-group with duration adjustment, per fraction", "formula": "~ 0 + C(cell) + C(time_raw) (cell = group), fitted separately per fraction", "design_column": "group_raw", "control": "Sed", "treatment": "Run", "contrasts": [{"name": "group_raw_Run_vs_Sed_frac_raw-IP", "control": "Sed", "treatment": "Run", "role": "primary"}, {"name": "group_raw_Run_vs_Sed_frac_raw-IN", "control": "Sed", "treatment": "Run", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: Fig 3A / S2.3.p1: one volcano of running vs sedentary in adult-born neurons across all three time points, top genes Rgs6 and Abca8a, with IN shown for comparison (Fig 3B-C). Estimand: running effect averaged over the three durations, with duration as an additive nuisance factor (durations differ in age and housing time), per fraction (IP and IN are different RNA populations). n = 6 Run vs 6 Sed pools per fraction, 8 residual df. The paper's per-duration contrasts are case GSE142678_per_duration (stopped at design by the sample-size gate).

rejected alternatives: [{"value": "pool durations without adjustment (6 vs 6, ~ group)", "reason_rejected": "duration (11/18/27 d, different ages) shifts expression in both arms; additive adjustment keeps it out of the residual"}, {"value": "group x time interaction / per-duration simple effects", "reason_rejected": "every cell n = 2; suitability not_analyzable (see case GSE142678_per_duration)"}, {"value": "one model across IP and IN", "reason_rejected": "different RNA populations; paper analyzes them separately"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": [], "covariates": [{"name": "time_raw", "disposition": "included"}, {"name": "pair", "disposition": "excluded: replicate letter nested in duration; no paper statement that a Run and a Sed pool were processed as a pair or batch, the paper reports no strong batch effect (S2.1.p2) and did not block"}], "design_check": {"formula_equivalent": "~ C(group_raw)", "n_samples": 24, "n_columns": 2, "columns": ["Intercept", "group_raw_Sed"], "rank": 2, "full_rank": true, "residual_df": 22, "levels": {"group_raw": {"Run": 12, "Sed": 12}}, "cells": [{"cell": ["Run"], "n": 12}, {"cell": ["Sed"], "n": 12}], "min_cell_size": 12, "missing_values": {}}, "confounding": [{"column": "time_raw", "n_levels": 3, "status": "crossed", "crosstab": {"Run": {"D11": 4, "D18": 4, "D27": 4}, "Sed": {"D11": 4, "D18": 4, "D27": 4}}}, {"column": "pair", "n_levels": 6, "status": "crossed", "crosstab": {"Run": {"a": 2, "b": 2, "c": 2, "d": 2, "e": 2, "f": 2}, "Sed": {"a": 2, "b": 2, "c": 2, "d": 2, "e": 2, "f": 2}}}]}

reasoning: Duration is a design variable balanced across arms (2 Run + 2 Sed per duration per fraction), so it is not confounded with running and is included as an additive covariate. Each sample is an independent pool of 2-4 mice (S4.3.7.p1); all female.

### method (valid, not_started)

final: {"matrix_type": "TPM (RSEM, linear scale)", "method": "limma (moderated t, empirical Bayes) on log2(TPM+1), group cell-means plus duration, per fraction", "formula": "~ 0 + C(cell) + C(time_raw)", "paper_route": {"method": "EBSeq (RSEM) on expected counts, PPEE < 0.05", "status": "blocked", "reason": "RSEM expected counts are not deposited (only TPM); EBSeq is not an available executor; TPM must not be rounded into counts"}, "deviations": ["limma on log2(TPM+1) instead of EBSeq on expected counts", "BH-adjusted p instead of EBSeq posterior probability of equal expression"], "transform": "log2(x+1)"}

reasoning: Matrix policy: TPM -> log2(x+1) -> limma. This is the validated alternative; the paper's EBSeq count model is blocked.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "adjustment": "EBSeq PPEE (posterior probability of equal expression)", "metric_original": "PPEE", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "effect_cutoff_original": "FC 1.5", "inclusive": false, "label": "Fig 3A volcano display rule (p < 0.05 and |FC| > 1.5)"}, "deviation_note": "EBSeq PPEE < 0.05 is a Bayesian FDR of 0.05 with no fold-change rule; on the limma route it is applied as BH-adjusted p < 0.05 with no fold-change rule. The Fig 3A display rule is recorded only as an audit count."}

reasoning: S2.1.p2 / S4.3.7.p1: cutoff of 0.05 of PPEE; no fold-change cutoff for DEG calls. FIG3 legend gives the volcano coloring rule.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "IP_across", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\results\\IP_across\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell) + C(cov0)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\results\\IP_across\\DEG_results_group_raw_Run_vs_Sed_frac_raw-IP.csv"], "counts": {"IP_across/group_raw_Run_vs_Sed_frac_raw-IP": {"applied": {"rule": "padj < 0.05", "n_tested": 22422, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 22422, "n_significant": 288, "n_up": 74, "n_down": 214, "deg_sanity": "ok"}}}}

reasoning: IP (adult-born neurons): Run vs Sed over all durations, duration-adjusted (Fig 3A).

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "IN_across", "role": "secondary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\results\\IN_across\\input\\matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell) + C(cov0)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\results\\IN_across\\DEG_results_group_raw_Run_vs_Sed_frac_raw-IN.csv"], "counts": {"IN_across/group_raw_Run_vs_Sed_frac_raw-IN": {"applied": {"rule": "padj < 0.05", "n_tested": 22541, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 22541, "n_significant": 214, "n_up": 170, "n_down": 44, "deg_sanity": "ok"}}}}

reasoning: IN (DG tissue): same model, the paper's comparison fraction (Fig 3C).

### enrichment (valid, not_run)

final: {"organism": "Mouse", "subset": "IP_across/group_raw_Run_vs_Sed_frac_raw-IP", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "reason_not_run": "no gene passes the ORA input threshold"}

reasoning: paper reports GO terms for IP DEGs (Fig 1G, 2C)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "IP_across/group_raw_Run_vs_Sed_frac_raw-IP", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\results\\enrichment_IP_across_group_raw_Run_vs_Sed_frac_raw-IP\\gsea\\DEG_results_group_raw_Run_vs_Sed_frac_raw-IP_GSEA_Hallmark.csv"], "summary": "GSEA complete on 22422 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 23 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=3.50 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=1.94 | NOM p=0.00e+00 | FDR q=1.37e-03 - HALLMARK_MTORC1_SIGNALING | NES=1.93 | NOM p=0.00e+00 | FDR q=1.03e-03 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.92 | NOM p=0.00e+00 | FDR q=8.22e-04 - HALLMARK_G2M_CHECKPOINT | NES=1.86 | NOM p=0.00e+00 | FDR q=6.85e-04 - HALLMARK_PI3K_AKT_MTOR_SIGNALING | NES=1.42 | NOM p=0.00e+00 | FDR q=3.87e-02 - HALLMARK_PROTEIN_SECRETION | NES=1.33 | NOM p=1.32e-02 | FDR q=5.44e-02 - HALLMARK_DNA_REPAIR | NES=1.20 | NOM p=5.41e-02 | FDR q=1.55e-01 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.20 | NOM p=1.21e-01 | FDR q=1.52e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-1.65 | NOM p=0.00e+00 | FDR ... [478 more characters]

reasoning: paper reports GO terms for IP DEGs (Fig 1G, 2C)

### enrichment (valid, not_run)

final: {"organism": "Mouse", "subset": "IN_across/group_raw_Run_vs_Sed_frac_raw-IN", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "reason_not_run": "no gene passes the ORA input threshold"}

reasoning: paper reports GO terms for IN DEGs (Fig 1G)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "IN_across/group_raw_Run_vs_Sed_frac_raw-IN", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_across_durations\\results\\enrichment_IN_across_group_raw_Run_vs_Sed_frac_raw-IN\\gsea\\DEG_results_group_raw_Run_vs_Sed_frac_raw-IN_GSEA_Hallmark.csv"], "summary": "GSEA complete on 22541 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 23 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_KRAS_SIGNALING_DN | NES=1.48 | NOM p=4.75e-03 | FDR q=2.05e-01 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.39 | NOM p=1.73e-02 | FDR q=2.43e-01 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.33 | NOM p=3.22e-02 | FDR q=2.59e-01 - HALLMARK_BILE_ACID_METABOLISM | NES=1.29 | NOM p=7.56e-02 | FDR q=2.77e-01 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.29 | NOM p=4.22e-02 | FDR q=2.33e-01 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.19 | NOM p=1.98e-01 | FDR q=4.40e-01 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.14 | NOM p=2.18e-01 | FDR q=5.18e-01 - HALLMARK_G2M_CHECKPOINT | NES=1.13 | NOM p=1.95e-01 | FDR q=4.90e-01 - HALLMARK_PEROXISOME | NES=1.11 | NOM p=2.66e-01 | FDR q=5.03e-01 - HALLMARK_COAGULATION | NES=1.10 | NOM p=2.54e-01 | FDR q=4.75e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_PROTEIN_SECRETION | NES=-2.67 | NOM p=0.00e+00 | FDR ... [478 more characters]

reasoning: paper reports GO terms for IN DEGs (Fig 1G)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper's EBSeq on RSEM expected counts is blocked (only TPM deposited); counts are not expected to match.", "Fig 3A pooling across durations is inferred (one volcano, 'across all three time points'); whether the paper adjusted for or pooled durations is not stated.", "The paper's per-duration DEG counts (IP 18d 460, IP 27d 544, IN 27d 124) are not reproduced: those contrasts were stopped at the design gate (n = 2 per cell).", "Ambiguous Excel-mangled IDs 1-Mar/2-Mar (4 rows) removed; other date-mangled IDs are kept but will not map in enrichment."], "results": {"IP_across/group_raw_Run_vs_Sed_frac_raw-IP": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 288}, "IN_across/group_raw_Run_vs_Sed_frac_raw-IN": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 214}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"IP_across/group_raw_Run_vs_Sed_frac_raw-IP": {"Rgs6": {"AveExpr": 4.8221, "log2FoldChange": 0.7282, "padj": 0.333, "pvalue": 9.99e-05}, "Abca8a": {"AveExpr": 4.2906, "log2FoldChange": -0.839, "padj": 0.333, "pvalue": 0.000209}, "Bdnf": {"AveExpr": 4.936, "log2FoldChange": 0.4531, "padj": 0.376, "pvalue": 0.00233}, "Calb2": {"AveExpr": 7.8503, "log2FoldChange": 1.0125, "padj": 0.376, "pvalue": 0.00217}}, "IN_across/group_raw_Run_vs_Sed_frac_raw-IN": {"Abca8a": {"AveExpr": 3.1242, "log2FoldChange": -0.3726, "padj": 0.956, "pvalue": 0.0139}, "Bdnf": {"AveExpr": 5.5997, "log2FoldChange" ... [132 more characters]

reasoning: Fig 3A comparison on a declared alternative method (limma on log2 TPM); Rgs6 is expected up in IP and unchanged in IN; Abca8a down in both.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE input and method",
    "paper": "EBSeq on RSEM expected counts",
    "data": "only TPM deposited",
    "disposition": "declared_deviation: limma on log2(TPM+1)"
  },
  {
    "item": "threshold metric",
    "paper": "EBSeq PPEE < 0.05",
    "data": "limma gives p-values",
    "disposition": "declared_deviation: BH padj < 0.05"
  },
  {
    "item": "duplicated feature IDs",
    "paper": "not discussed",
    "data": "1-Mar and 2-Mar each appear twice (Excel date conversion)",
    "disposition": "executable_without_change after removing the 4 ambiguous rows (prep script)"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 32755589 / GSE142678 (RGS6, voluntary running, adult-born DG neurons)

Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID32755589` (run label PMID32755589).
Route: case spec (`python -m tools.case_runner execute case_spec.json`). Validator: 24 records, 0 errors. No external LLM calls were made.

## Study and data
- Paper design (S2.1.p2, S4.3.7.p1, Fig 1B/E/F): RiboTag-seq on female Nes-CreERT2::RiboTag mice. There are 2 fractions (IP = adult-born neurons, IN = whole dentate gyrus input), 3 running durations (11, 18 and 27 days) and 2 arms (running, sedentary), with **2 replicates per cell**. Each replicate is a pool of 2-4 mice, so there are 24 libraries.
- Paper DE method: EBSeq inside RSEM on expected counts, called at **PPEE < 0.05** (a posterior-probability FDR) with no fold-change rule. Running and sedentary are compared within each duration, separately for IP and IN. The Fig 3A volcano colours genes at p < 0.05 and |FC| > 1.5; this is a display rule only.
- Data: the only deposited matrix is `GSE142678_nes_run_TPM.csv.gz`. It holds RSEM TPM (each column sums to 1e6) and is aligned exactly to the GEO `title` field (24/24). Expected counts are not deposited, so the EBSeq route is blocked.
- Prep: `prep_drop_ambiguous_ids.py` removed the 4 rows with Excel-mangled duplicate IDs `1-Mar` and `2-Mar`, whose true gene identity is ambiguous. Its output is `GSE142678_TPM_dedup.csv` (23302 x 24).

## Cases
1. **GSE142678_per_duration**: the paper's primary estimand. It covers 6 contrasts, running vs sedentary at 11, 18 and 27 days in IP and in IN. It **stopped at the design gate (`manual_review`)**. Suitability returned `not_analyzable` (sample_size): every cell has n = 2, so 0 of 22 comparisons reach n >= 3, and the decision contract rejects a valid design on that verdict. The paper, ownership, alignment and matrix gates were recorded.
2. **GSE142678_across_durations**: the Fig 3A / S2.3.p1 estimand, running vs sedentary "across all three time points" (Rgs6 top up, Abca8a top down). It **completed** as a declared deviation: limma on log2(TPM+1), `~ 0 + C(cell) + C(time_raw)`, fitted separately for IP and IN. Each fraction has 6 running vs 6 sedentary pools, with duration as an additive covariate and 8 residual df.

## DEG counts vs paper
Applied threshold: BH padj < 0.05 with no fold-change rule (`paper_on_deviation_route`: the paper's PPEE < 0.05 mapped to BH). Audit threshold: p < 0.05 and |log2FC| > log2(1.5) = 0.58 ... [2908 more characters]
