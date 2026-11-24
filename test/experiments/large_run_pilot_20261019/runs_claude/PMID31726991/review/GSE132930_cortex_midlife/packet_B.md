# Review packet B (the analysis' decisions): GSE132930_cortex_midlife

## Mechanical flags

- **possible_reversed_contrast**: {"contrast": "grp_RunHi_vs_Sed", "control": "Sed", "treatment": "RunHi", "note": "the control side reads as exercise or the test side as control"}
- **possible_reversed_contrast**: {"contrast": "grp_RunLow_vs_Sed", "control": "Sed", "treatment": "RunLow", "note": "the control side reads as exercise or the test side as control"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C_mid_RunHi_vs_Sed | 214 | 0 | padj < 0.05 | 0 | 0 | 0 | 1 | 879 | 92 | 20 | 159 | 0.054 | 0.059 |
| C_mid_RunLow_vs_Sed | 67 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 593 | 39 | 7 | 138 | 0.102 | 0.04 |

## Samples per design level

### `grp`
- **RunHi** (6): GSM3896747 / 3494C; GSM3896748 / 3597C; GSM3896750 / 6332C; GSM3896753 / 9926C; GSM3896764 / 7785C; GSM3896765 / 1388C
- **RunLow** (6): GSM3896744 / 0533C; GSM3896745 / 1003C; GSM3896754 / 0304C; GSM3896755 / 1990C; GSM3896758 / 3545C; GSM3896759 / 5581C
- **Sed** (10): GSM3896746 / 23886C; GSM3896749 / 5943C; GSM3896751 / 6967C; GSM3896752 / 9555C; GSM3896756 / 2084C; GSM3896757 / 2747C; GSM3896760 / 5915C; GSM3896761 / 6859C; GSM3896762 / 7182C; GSM3896763 / 7383C

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE132930"], "primary_estimand": "Effect of 12 weeks voluntary wheel running vs age-matched sedentary on brain gene expression, analysed separately per tissue (cortex, hippocampus) and per age cohort (young 1-2 mo start; midlife 12 mo start, runners split into high/low by >10,000 rotations/night)", "planned_contrasts": ["cortex young Run vs Sed (S2.2.p1: 1252 DE; 742 up, 510 down)", "cortex midlife RunHi vs Sed (S2.2.p1: 214; 70 up, 144 down)", "cortex midlife RunLow vs Sed (S2.2.p1: 67; 20 up, 47 down)", "hippocampus young Run vs Sed (S2.2.p1: 2026; 1498 up, 528 down)", "hippocampus midlife RunHi vs Sed (S2.2.p1: 271; 87 up, 184 down)", "hippocampus midlife RunLow vs Sed (S2.2.p1: 172; 80 up, 92 down)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "S5.6.p1"}, "paper_method": "RSEM counts; edgeR 3.20.9, filter CPM>=1 in >1 sample, TMM, quasi-likelihood F-test, per tissue (S5.6.p1)", "factors": {"activity": ["Sed", "Run (young)", "RunLow", "RunHi (midlife)"], "tissue": ["Cortex", "Hippocampus"], "age": ["Young", "Midlife"]}, "inclusion": "male C57BL/6J; young n=5 per activity for RNA-seq (S5.2.p1); midlife n=12 run (6 high, 6 low) + 12 sed (S2.1.p1, S5.2.p1); young and midlife not directly compared (run at separate times, S5.6.p1)", "paper_results": "DEG counts per contrast in S2.2.p1 / Fig 3b,g; named genes S2.3.p1, S2.4.p2"}

reasoning: Methods S5.6.p1 define edgeR QL per tissue and three comparisons per tissue; S2.2.p1 gives counts at FDR<0.05 with no fold-change cutoff. Young and midlife were sequenced at separate times and the authors state they cannot be compared directly, so each tissue x age is its own model.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE132930\\GSE132930_GeneCount_C_midlife.txt.gz", "owned": true, "checks": ["DA.p1 names GSE132930", "matrix GSE132930_GeneCount_C_midlife.txt.gz is deposited in GSE132930 supplementary files; restricted to One Year cortex samples listed in GEO metadata", "deposited edgeR result tables in the same series reproduce the paper's DEG counts exactly at FDR<0.05 (1252/214/67/2026/271/172), confirming the sample sets"], "accession": "GSE132930", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE132930\\GSE132930_metadata.csv"}

reasoning: Series and matrix belong to the paper; sample titles (mouse id + C/H) map to GSM records.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 22, "n_metadata": 65, "coverage": 0.3385, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM3896766", "GSM3896767", "GSM3896768", "GSM3896769", "GSM3896770", "GSM3896771", "GSM3896772", "GSM3896773", "GSM3896774", "GSM3896775", "GSM3896776", "GSM3896777", "GSM3896778", "GSM3896779", "GSM3896780", "GSM3896781", "GSM3896782", "GSM3896783", "GSM3896784", "GSM3896785", "GSM3896786", "GSM3896787", "GSM3896788", "GSM3896789", "GSM3896790", "GSM3896791", "GSM3896792", "GSM3896793", "GSM3896794", "GSM3896795", "GSM3896796", "GSM3896797", "GSM3896798", "GSM3896799", "GSM3896800", "GSM3896801", "GSM3896802", "GSM3896803", "GSM3896804", "GSM3896805", "GSM3896806", "GSM3896807", "GSM3896808"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.3.activity", "regex": "^(Sed|Run|RunLow|RunHi)$"}, "pool": {"source": "title", "regex": "^(\\d+[CH])$", "recode": {"0533C": "L001", "1003C": "L001", "23886C": "L001", "3494C": "L001", "3597C": "L001", "5943C": "L001", "6332C": "L001", "6967C": "L001", "9555C": "L001", "9926C": "L001", "0304C": "L005", "1990C": "L005", "2084C": "L005", "2747C": "L005", "3545C": "L005", "5581C": "L005", "5915C": "L005", "6859C": "L005", "7182C": "L005", "7383C": "L005", "7785C": "L005", "1388C": "L001"}}}, "output": "test\\experim ... [285 more characters]

reasoning: Matrix columns embed the GEO title (mouse id + C/H) followed by GT library id, barcode and lane; matrix_column_pattern extracts the title, exact match on metadata 'title'. grp from the activity characteristic. pool = sequencing lane parsed from the matrix column name (L001/L005), mapped per title, used only as a confounding candidate.

### matrix (valid, not_started)

final: {"source": "GSE132930_GeneCount_C_midlife.txt.gz", "paper_input": "RSEM v1.2.12 gene counts (S5.6.p1)", "matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\aligned\\aligned_matrix.csv", "sha256": "6a5b78422c0c3bf18e95eb2403d855708ae7d266e22483bfd2480445ba9b1aa0", "n_features": 38924, "n_samples": 22, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1336709.0, "median": 1.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, min 0, max ~1.3e6, file named GeneCount; paper quantified with RSEM (S5.6.p1) and analysed them with edgeR, so these are RSEM-derived integer gene counts, the paper's own input.

### design (valid, not_started)

final: {"analysis_type": "multi-group, pairwise per paper", "design_column": "grp", "contrasts": [{"name": "grp_RunHi_vs_Sed", "control": "Sed", "treatment": "RunHi", "role": "primary"}, {"name": "grp_RunLow_vs_Sed", "control": "Sed", "treatment": "RunLow", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Midlife cortex: RunHi vs Sed and RunLow vs Sed (S5.6.p1 comparisons ii, iii). Paper fitted each comparison on the two groups only (deposited tables list only those samples), so each is a separate two-arm edgeR fit on a subset.

rejected alternatives: [{"value": "pooled Run (Hi+Low) vs Sed", "reason_rejected": "paper never pools runners; high/low are its planned levels"}, {"value": "RunHi vs RunLow", "reason_rejected": "not a paper comparison and not an exercise-vs-sedentary estimand"}, {"value": "one 3-level model", "reason_rejected": "paper's deposited results come from pairwise subset fits; kept pairwise to reproduce"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "pool", "disposition": "sensitivity_only"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 22, "n_columns": 3, "columns": ["Intercept", "grp_RunLow", "grp_Sed"], "rank": 3, "full_rank": true, "residual_df": 19, "levels": {"grp": {"Sed": 10, "RunLow": 6, "RunHi": 6}}, "cells": [{"cell": ["RunHi"], "n": 6}, {"cell": ["RunLow"], "n": 6}, {"cell": ["Sed"], "n": 10}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "pool", "n_levels": 2, "status": "crossed", "crosstab": {"RunHi": {"L001": 5, "L005": 1}, "RunLow": {"L001": 2, "L005": 4}, "Sed": {"L001": 4, "L005": 6}}}]}

reasoning: Independent animals, one sample per mouse per tissue; paper used ~group only (S5.6.p1). Sequencing lane (L001/L005) is unbalanced across activity groups; kept out of the primary paper-aligned model and tested as a DESeq2 sensitivity covariate.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "edgeR (TMM + glmQLFit/glmQLFTest via inmoose)", "formula": "~ grp", "paper_route": {"method": "edgeR 3.20.9 QL F-test", "status": "reproduced"}, "deviations": ["inmoose edgepy port rather than R edgeR 3.20.9; TMM factors from repository implementation"]}

reasoning: Paper route (S5.6.p1): filter CPM>=1 in >=2 samples of each comparison, TMM, QL F-test, two-group fit per comparison (deposited tables contain only the two compared groups' samples).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}}

reasoning: S5.6.p1 / S2.2.p1: FDR < 0.05, no fold-change rule. Audit adds |FC|>1.5 for reference only.

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "C_mid_RunHi_vs_Sed", "role": "primary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\results\\C_mid_RunHi_vs_Sed\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\results\\C_mid_RunHi_vs_Sed\\DEG_results_RunHi_vs_Sed.csv"], "counts": {"C_mid_RunHi_vs_Sed": {"applied": {"rule": "padj < 0.05", "n_tested": 14980, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14980, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: paper's edgeR QL two-group comparison

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "C_mid_RunLow_vs_Sed", "role": "primary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\results\\C_mid_RunLow_vs_Sed\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\results\\C_mid_RunLow_vs_Sed\\DEG_results_RunLow_vs_Sed.csv"], "counts": {"C_mid_RunLow_vs_Sed": {"applied": {"rule": "padj < 0.05", "n_tested": 14966, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14966, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: paper's edgeR QL two-group comparison

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "C_mid_RunHi_vs_Sed_poolsens", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\results\\C_mid_RunHi_vs_Sed_poolsens\\input\\matrix_filtered.csv", "formula": "~ pool + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\results\\C_mid_RunHi_vs_Sed_poolsens\\DEG_results_RunHi_vs_Sed.csv"], "counts": {"C_mid_RunHi_vs_Sed_poolsens": {"applied": {"rule": "padj < 0.05", "n_tested": 14980, "n_significant": 1, "n_up": 0, "n_down": 1, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 14980, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: sensitivity: DESeq2 ~ pool + grp, to see whether the unbalanced sequencing lane changes the call set

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "C_mid_RunLow_vs_Sed_poolsens", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\results\\C_mid_RunLow_vs_Sed_poolsens\\input\\matrix_filtered.csv", "formula": "~ pool + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31726991\\GSE132930_cortex_midlife\\results\\C_mid_RunLow_vs_Sed_poolsens\\DEG_results_RunLow_vs_Sed.csv"], "counts": {"C_mid_RunLow_vs_Sed_poolsens": {"applied": {"rule": "padj < 0.05", "n_tested": 13515, "n_significant": 21, "n_up": 12, "n_down": 9, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 13515, "n_significant": 3, "n_up": 2, "n_down": 1, "deg_sanity": "ok"}}}}

reasoning: sensitivity: DESeq2 ~ pool + grp, to see whether the unbalanced sequencing lane changes the call set

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["young and midlife cohorts were sequenced separately; per paper S5.6.p1 they are not compared directly", "midlife high/low split is a post-hoc grouping by running distance (associational within runners)"], "results": {"C_mid_RunHi_vs_Sed": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 0}, "C_mid_RunLow_vs_Sed": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 0}, "C_mid_RunHi_vs_Sed_poolsens": {"n_deg": 1, "up": 0, "down": 1, "rule": "padj < 0.05", "audit_n": 0}, "C_mid_RunLow_vs_Sed_poolsens": {"n_deg": 21, "up": 12, "down": 9, "rule": "padj < 0.05", "audit_n": 3}}, "paper_counts": {"C_mid_RunHi_vs_Sed": 214, "C_mid_RunLow_vs_Sed": 67}, "comparison": {"C_mid_RunHi_vs_Sed": {"ours": 0, "paper": 214}, "C_mid_RunLow_vs_Sed": {"ours": 0, "paper": 67}}, "paper_gene_check": {"C_mid_RunHi_vs_Sed": {"Col8a1": {"log2FoldChange": -0.5617, "padj": 0.624, "pvalue": 0.0261}, "Hif3a": {"log2FoldChange": -1.1291, "padj": 0.539, "pvalue": 0.000432}}}}

reasoning: Counts from S2.2.p1; genes from S2.3.p1/S2.4.p2.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 22 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "running duration",
    "paper": "12 weeks (S2.1.p1, S5.2.p1)",
    "data": "young deposited result file named 'Early_Diet ... 8wkrun ... CD.8weeks'",
    "disposition": "executable_without_change"
  },
  {
    "item": "young matrix scope",
    "paper": "n=5 per activity",
    "data": "young GeneCount matrices hold 56-57 libraries of a larger 'Early_Diet' experiment; only the 10 GEO-registered samples per tissue are used",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID31726991 / GSE132930

Paper: Foley et al. 2019, BMC Genomics (PMC6854620): "Transcriptional profiling predicts running promotes cerebrovascular remodeling in young but not midlife mice". Run label PMID31726991.

## What ran
One spec (`case_spec.json`, built by a small generator script that lived only in the session scratchpad) ran through `python -m tools.case_runner execute`. The run completed and the validator passed on 60 records with 0 errors. It has five cases. Each tissue × age pair has its own matrix and model, because the paper says the young and midlife cohorts were sequenced at separate times (S5.6.p1).

| Case | Matrix | Samples | Executions |
|---|---|---|---|
| cortex_young | GeneCount_C_young | 5 Run, 5 Sed | edgeR QL Run vs Sed (primary) + ORA/GSEA |
| hippocampus_young | GeneCount_H_young | 5 Run, 4 Sed (18606H excluded) | edgeR QL Run vs Sed (primary) + ORA/GSEA |
| hippocampus_young_all10 | GeneCount_H_young | 5 Run, 5 Sed | edgeR QL (sensitivity, exploratory) |
| cortex_midlife | GeneCount_C_midlife | 6 RunHi, 6 RunLow, 10 Sed | edgeR QL RunHi vs Sed and RunLow vs Sed (primary, pairwise subsets); DESeq2 `~ pool + grp` (sensitivity) |
| hippocampus_midlife | GeneCount_H_midlife | 5 RunHi, 6 RunLow, 12 Sed | same as cortex_midlife |

- **Alignment:** matrix columns were matched exactly on the GEO `title` field (regex `^(?:16NGS-002-Howell_)?(\d+[CH])_`). The young matrices hold 56–57 libraries from a larger "Early_Diet" experiment. Only the 10 samples registered for this series were used in each tissue.
- **Matrix:** RSEM integer gene counts (integer fraction 1.0, as stated in S5.6.p1). These are the paper's own input.
- **Method:** the paper route as written in S5.6.p1. Genes were kept if CPM ≥ 1 in at least 2 samples of each comparison, then TMM normalisation and a quasi-likelihood F-test, using the inmoose edgeR port.
- **Threshold:** the paper's rule, FDR < 0.05 with no fold-change cutoff (S5.6.p1, S2.2.p1), source `paper`. The audit rule adds |log2FC| > 0.585 and is for reference only.

## DEG counts vs paper (FDR < 0.05, no FC cutoff)
| Contrast | Ours (up/down) | Paper (up/down) | Overlap with authors' deposited table |
|---|---|---|---|
| Cortex young Run vs Sed | 971 (542/429) | 1252 (742/510) | 920 of 1252 |
| Hippocampus young Run vs Sed | 1950 (1396/554) | 2026 (1498/528) | 1752 of 2026 |
| Cortex midlife RunHi vs Sed | 0 | 214 (70/144) | 0 |
| Cortex midlife RunLow vs Sed | 0 | 67 (20/47) | 0 |
| Hippocampus m ... [4266 more characters]
