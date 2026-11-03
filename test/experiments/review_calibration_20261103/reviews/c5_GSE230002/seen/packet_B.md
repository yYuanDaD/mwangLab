# Review packet B (the analysis' decisions): GSE230002

## Mechanical flags

- **other_rule_matches_paper**: {"table": "time_Post_vs_Pre_arm-EX", "paper": 877, "applied": 122, "applied_rule": "padj < 0.05 and |log2FoldChange| > 0.3", "closest_rule": "pvalue<0.01", "closest_n": 981, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| time_Post_vs_Pre_arm-EX | 877 | 122 | padj < 0.05 and |log2FoldChange| > 0.3 | 122 | 81 | 20 | 504 | 2427 | 440 | 76 | 981 | 0.068 | 0.176 |
| time_Post_vs_Pre_arm-DIET | 1 | 0 | padj < 0.05 and |log2FoldChange| > 0.3 | 0 | 0 | 0 | 0 | 589 | 83 | 15 | 98 | 0.097 | 0.043 |

## Samples per design level

### `time`
- **Post** (13): GSM7182629 / PE-004Post; GSM7182631 / PE-007Post; GSM7182633 / PE-011Post; GSM7182635 / PE-012Post; GSM7182637 / PE-035Post; GSM7182639 / PE-040Post; GSM7182641 / PE-041Post; GSM7182643 / PSQ-0070Post; GSM7182645 / PSQ-0266Post; GSM7182647 / PSQ-0320Post; GSM7182649 / PSQ-0343Post; GSM7182651 / PSQ-0379Post; GSM7182653 / PSQ-0405Post
- **Pre** (13): GSM7182630 / PE-004Pre; GSM7182632 / PE-007Pre; GSM7182634 / PE-011Pre; GSM7182636 / PE-012Pre; GSM7182638 / PE-035Pre; GSM7182640 / PE-040Pre; GSM7182642 / PE-041Pre; GSM7182644 / PSQ-0070Pre; GSM7182646 / PSQ-0266Pre; GSM7182648 / PSQ-0320Pre; GSM7182650 / PSQ-0343Pre; GSM7182652 / PSQ-0379Pre; GSM7182654 / PSQ-0405Pre

### `subject`
- **PE-004** (2): GSM7182629 / PE-004Post; GSM7182630 / PE-004Pre
- **PE-007** (2): GSM7182631 / PE-007Post; GSM7182632 / PE-007Pre
- **PE-011** (2): GSM7182633 / PE-011Post; GSM7182634 / PE-011Pre
- **PE-012** (2): GSM7182635 / PE-012Post; GSM7182636 / PE-012Pre
- **PE-035** (2): GSM7182637 / PE-035Post; GSM7182638 / PE-035Pre
- **PE-040** (2): GSM7182639 / PE-040Post; GSM7182640 / PE-040Pre
- **PE-041** (2): GSM7182641 / PE-041Post; GSM7182642 / PE-041Pre
- **PSQ-0070** (2): GSM7182643 / PSQ-0070Post; GSM7182644 / PSQ-0070Pre
- **PSQ-0266** (2): GSM7182645 / PSQ-0266Post; GSM7182646 / PSQ-0266Pre
- **PSQ-0320** (2): GSM7182647 / PSQ-0320Post; GSM7182648 / PSQ-0320Pre
- **PSQ-0343** (2): GSM7182649 / PSQ-0343Post; GSM7182650 / PSQ-0343Pre
- **PSQ-0379** (2): GSM7182651 / PSQ-0379Post; GSM7182652 / PSQ-0379Pre
- **PSQ-0405** (2): GSM7182653 / PSQ-0405Post; GSM7182654 / PSQ-0405Pre

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE230002"], "assay": "bulk total-RNA RNA-seq of vastus lateralis muscle (S3.10.2.p1, S1.4.p1)", "design": "two parallel arms (concurrent trials NCT02706288 / NCT02706262), each sampled Before and After ~10% weight loss; Diet+EX (calorie restriction + multi-modal exercise) vs Diet-ONLY (calorie restriction alone) (S3.1.p1)", "sample_inclusion": "RNA-seq on Diet-ONLY n=6 and Diet+EX n=7 (one Diet+EX sample excluded for poor RNA quality) (FIG8, S3.10.2.p1)", "factors": {"arm": ["Diet-ONLY", "Diet+EX"], "time": ["Before", "After"]}, "repeated_measure_unit": "participant (paired Before/After biopsies)", "primary_estimand": "Within-arm change in muscle gene expression After vs Before weight loss, in Diet+EX (the exercise-containing arm) and in Diet-ONLY; the exercise contribution is read as the difference between the two arms' responses (S1.4.p1, S3.13.2.1.p1). The paper tested the between-arm difference only for selected genes by ANCOVA (FIG8).", "planned_contrasts": ["Diet+EX After vs Before (S1.4.p1; paper: 877 DEGs, 623 up / 254 down)", "Diet-ONLY After vs Before (S1.4.p1; paper: 1 DEG, HMOX1 down)"], "paper_method": "edgeR 3.40.2, Before vs After within each group (S3.13.2.1.p1); expression presented as log2 CPM (S3.10.2.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.3, "source_locator": "S3.13.2.1.p1; FIG8"}, "paper_results": "877 DEGs in Diet+EX (623 up, 254 down), 1 DEG in Diet-ONLY (HMOX1 d ... [246 more characters]

reasoning: Study map from S3.1.p1 (arms, trials), S3.10.2.p1 (RNA-seq, exclusion), S3.13.2.1.p1 (edgeR, threshold), S1.4.p1 and FIG8 (counts, genes). The exercise question is answered by the Diet+EX within-arm change against the Diet-ONLY within-arm change.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37365374\\prep\\GSE230002_log2cpm_filtered.csv", "owned": true, "checks": ["DA.p1 names GSE230002 as this study's RNA-seq deposit", "GEO: Homo sapiens skeletal muscle, before/after 10% weight loss in people with obesity and prediabetes, Washington University group", "26 samples = 13 participants x 2 timepoints, matching Diet-ONLY n=6 + Diet+EX n=7 (FIG8)"], "accession": "GSE230002", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE230002\\GSE230002_metadata.csv"}

reasoning: Accession named in the paper's data availability; sample structure matches the paper's RNA-seq n.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 26, "n_metadata": 26, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\aligned\\aligned_metadata.csv", "columns": {"arm": {"source": "title", "regex": "^(PE|PSQ)-\\d+(?:Pre|Post)$", "recode": {"PE": "EX", "PSQ": "DIET"}}, "time": {"source": "title", "regex": "^P\\w*-\\d+(Pre|Post)$"}, "subject": {"source": "title", "regex": "^(P\\w*-\\d+)(?:Pre|Post)$"}}, "output": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\aligned\\design_metadata.csv", "sha256": "c7c515d6601d61a4fb183acc26e935045a84f765b710b8b7bfda46abb36a072f", "levels": {"arm": {"EX": 14, "DIET": 12}, "time": {"Post": 13, "Pre": 13}, "subject": {"PE-004": 2, "PE-007": 2, "PE-011": 2, "PE-012": 2, "PE-035": 2, "PE-040": 2, "PE-041": 2, "PSQ-0070": 2, "PSQ-0266": 2, "PSQ-0320": 2, "PSQ-0343": 2, "PSQ-0379": 2, "PSQ-0405": 2}}}}

reasoning: Matrix columns equal metadata title exactly (inspect: 26/26). GEO carries only a Before/After treatment field; the arm is not labelled. Title prefixes split participants into PE (7) and PSQ (6). The paper's RNA-seq arms are Diet+EX n=7 and Diet-ONLY n=6 (FIG8), so PE = Diet+EX (EX) and PSQ = Diet-ONLY (DIET); this is the only count-consistent assignment. Supporting check on the deposited values: PPARGC1A rises in all 7 PE participants (paper: increased with Diet+EX) and HMOX1 falls in 5/6 PSQ participants (paper's single Diet-ONLY DEG). Time from the Pre/Post suffix agrees with the GEO treatment field (Before/After); subject is the participant ID.

rejected alternatives: [{"value": "PE = Diet-ONLY, PSQ = Diet+EX", "reason_rejected": "arm sizes would be 7 Diet-ONLY / 6 Diet+EX, contradicting FIG8 (Diet-ONLY n=6, Diet+EX n=7)"}]

### matrix (valid, not_started)

final: {"matrix_type": "log2 CPM (edgeR moderated log2CPM, prior count), gene symbols", "recommended_method": "limma", "profile": {"path": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\aligned\\aligned_matrix.csv", "sha256": "dd1063235cb1274a2f7d5936df7feb5fd2c8aa8f2cbdfc43786a708dcf1fdde2", "n_features": 13851, "n_samples": 26, "annotation_columns_dropped": [], "duplicated_feature_ids": 46, "missing_values": 0, "negative_values": 21965, "negative_fraction": 0.060993, "min": -5.55392489695182, "max": 18.4822595811252, "median": 3.32029847013234, "integer_fraction": 0.0, "candidates": ["signed_log_scale (log ratios, M-values, or centered data)"]}}

reasoning: Values are non-integer, range -5.55 to 18.5, median -2.3 with a floor at the prior-count value: log2 CPM. File name 'gene_moderated_log2cpm' and GEO data_processing ('CPM calculated from gene counts ... log-transformed (attached processed data file)') agree. The paper's input to edgeR was raw featureCounts, which are not deposited (the log2CPM table is the only supplementary file).

### design (valid, not_started)

final: {"analysis_type": "paired two-timepoint, per arm", "design_column": "time", "control": "Pre", "treatment": "Post", "contrasts": [{"name": "time_Post_vs_Pre_arm-EX", "control": "Pre", "treatment": "Post", "role": "primary", "stratum": {"arm": "EX"}}, {"name": "time_Post_vs_Pre_arm-DIET", "control": "Pre", "treatment": "Post", "role": "secondary", "stratum": {"arm": "DIET"}}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: The paper analyzes Before vs After within each group (S3.13.2.1.p1); arm is therefore a stratum and time the tested factor, with participant as the repeated-measure unit. The exercise effect proper (difference of changes between arms) is not a paper DE contrast; it is added as an exploratory paired-change model.

rejected alternatives: [{"value": "Post vs Pre pooled across arms", "reason_rejected": "mixes the two interventions; the paper analyzes arms separately"}, {"value": "EX vs DIET at Post only", "reason_rejected": "cross-sectional between-person comparison ignores baseline; not the paper's estimand"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking factor (paired Before/After biopsies)"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 26, "n_columns": 14, "columns": ["Intercept", "time_Pre", "subject_PE-007", "subject_PE-011", "subject_PE-012", "subject_PE-035", "subject_PE-040", "subject_PE-041", "subject_PSQ-0070", "subject_PSQ-0266", "subject_PSQ-0320", "subject_PSQ-0343", "subject_PSQ-0379", "subject_PSQ-0405"], "rank": 14, "full_rank": true, "residual_df": 12, "levels": {"time": {"Post": 13, "Pre": 13}, "subject": {"PE-004": 2, "PE-007": 2, "PE-011": 2, "PE-012": 2, "PE-035": 2, "PE-040": 2, "PE-041": 2, "PSQ-0070": 2, "PSQ-0266": 2, "PSQ-0320": 2, "PSQ-0343": 2, "PSQ-0379": 2, "PSQ-0405": 2}}, "cells": [{"cell": ["Post", "PE-004"], "n": 1}, {"cell": ["Post", "PE-007"], "n": 1}, {"cell": ["Post", "PE-011"], "n": 1}, {"cell": ["Post", "PE-012"], "n": 1}, {"cell": ["Post", "PE-035"], "n": 1}, {"cell": ["Post", "PE-040"], "n": 1}, {"cell": ["Post", "PE-041"], "n": 1}, {"cell": ["Post", "PSQ-0070"], "n": 1}, {"cell": ["Post", "PSQ-0266"], "n": 1}, {"cell": ["Post", "PSQ-0320"], "n": 1}, {"cell": ["Post", "PSQ-0343"], "n": 1}, {"cell": ["Post", "PSQ-0379"], "n": 1}, {"cell": ["Post", "PSQ-0405"], "n": 1}, {"cell": ["Pre", "PE-004"], "n": 1}, {"cell": ["Pre", "PE-007"], "n": 1}, {"cell": ["Pre", "PE-011"], "n": 1}, {"cell": ["Pre", "PE-012"], "n": 1}, {"cell": ["Pre", "PE-035"] ... [381 more characters]

reasoning: Each participant contributes a Before and an After biopsy, so participant is blocked as a fixed effect in each per-arm model. No batch, sex or lane columns are deposited; nothing else is added.

### method (valid, not_started)

final: {"matrix_type": "log2 CPM (edgeR moderated log2CPM, prior count), gene symbols", "method": "limma (moderated t, eBayes) on log2 CPM, paired ~ subject + time, per arm", "formula": "~ subject + time", "paper_route": {"method": "edgeR 3.40.2 on raw counts", "status": "blocked", "reason": "only a moderated log2CPM matrix is deposited; raw counts needed by edgeR's negative-binomial model are unavailable"}, "deviations": ["limma on deposited log2CPM instead of edgeR on counts", "low-expression filter (log2CPM >= 0 in >= 6 samples; 13,851 of 34,259 genes kept) applied by prep/filter_low_expression.py, standing in for the paper's unstated edgeR filtering", "duplicate gene symbols collapsed to the highest-mean row by the limma executor", "paired blocking on participant assumed; the paper does not state whether its edgeR model was paired"]}

reasoning: Matrix is already log2 CPM, so limma is the validated route (matrix-method policy: log-scale -> limma). The edgeR route is blocked by missing counts. Paired design follows the repeated-measure structure.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.3}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.3, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "paper's FDR<0.05 and |log2FC|>0.3 applied to limma results instead of edgeR"}

reasoning: S3.13.2.1.p1 and FIG8: |log2 fold change| > 0.3 and two-sided FDR < 0.05; the cutoff is already on log2 scale.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "time_Post_vs_Pre_arm-EX", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 14, "matrix": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\time_Post_vs_Pre_arm-EX\\input\\matrix.csv", "formula": "~ subject + time", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\time_Post_vs_Pre_arm-EX\\DEG_results_Post_vs_Pre.csv"], "counts": {"time_Post_vs_Pre_arm-EX": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 13805, "n_significant": 122, "n_up": 84, "n_down": 38, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13805, "n_significant": 122, "n_up": 84, "n_down": 38, "deg_sanity": "ok"}}}}

reasoning: Diet+EX After vs Before, paired on participant (paper's 877-DEG contrast).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "time_Post_vs_Pre_arm-DIET", "role": "secondary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\time_Post_vs_Pre_arm-DIET\\input\\matrix.csv", "formula": "~ subject + time", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\time_Post_vs_Pre_arm-DIET\\DEG_results_Post_vs_Pre.csv"], "counts": {"time_Post_vs_Pre_arm-DIET": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 13805, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13805, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Diet-ONLY After vs Before, paired on participant (paper's 1-DEG contrast).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "unpaired_EX", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 14, "matrix": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\unpaired_EX\\input\\matrix.csv", "formula": "~ time", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\unpaired_EX\\DEG_results_Post_vs_Pre.csv"], "counts": {"unpaired_EX": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 13805, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13805, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: Diet+EX After vs Before without participant blocking, in case the paper's edgeR model was unpaired (S3.13.2.1.p1 does not say).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "unpaired_DIET", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\unpaired_DIET\\input\\matrix.csv", "formula": "~ time", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\unpaired_DIET\\DEG_results_Post_vs_Pre.csv"], "counts": {"unpaired_DIET": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 13805, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13805, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: Diet-ONLY After vs Before without participant blocking.

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "exercise_interaction", "role": "exploratory", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 26, "matrix": "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\aligned\\aligned_matrix.csv", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\exercise_interaction\\followup_Post\\DEG_results_ex_vs_diet_change.csv"], "counts": {"exercise_interaction/ex_vs_diet_change": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 13805, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13805, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Exercise-specific estimand: (Post-Pre) in Diet+EX minus (Post-Pre) in Diet-ONLY; the paper tested this only for selected genes by ANCOVA, so genome-wide it is exploratory.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_Post_vs_Pre_arm-EX", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.3, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\ora_up\\DEG_results_Post_vs_Pre_GO_Biological_Process_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\ora_up\\DEG_results_Post_vs_Pre_GO_Cellular_Component_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\ora_up\\DEG_results_Post_vs_Pre_GO_Molecular_Function_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\ora_up\\DEG_results_Post_vs_Pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 84 Human genes (direction=up, padj<0.05, |log2FC|>0.3). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Proton Motive Force-Driven ATP Synthesis (GO:0015986) | padj=1.22e-07 | overlap=8/60 | genes=NDUFA8;ATP5F1B;ATP5PB;NDUFS2;ATP5MC3;ATP5F1C;SDHB;ATP5MC1 - Oxidative Phosphorylation (GO:0006119) | ... [1148 more characters]

reasoning: paper ran GO-BP enrichment on Diet+EX upregulated DEGs (FIG8b)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_Post_vs_Pre_arm-EX", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.3, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\ora_down\\DEG_results_Post_vs_Pre_GO_Biological_Process_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\ora_down\\DEG_results_Post_vs_Pre_GO_Cellular_Component_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\ora_down\\DEG_results_Post_vs_Pre_GO_Molecular_Function_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\ora_down\\DEG_results_Post_vs_Pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 38 Human genes (direction=down, padj<0.05, |log2FC|>0.3). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Regulation Of Cardiac Conduction (GO:1903779) | padj=1.51e-01 | overlap=2/21 | genes=ATP2A1;ATP2B2 - Heart Morphogenesis (GO:0003007) | padj=1.97e-01 | overlap=2/59 | genes=ACVR1;MY ... [1158 more characters]

reasoning: paper reports two downregulated GO-BP pathways (S1.4.p1)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_Post_vs_Pre_arm-EX", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_02/run/GSE230002\\results\\enrichment_time_Post_vs_Pre_arm-EX\\gsea\\DEG_results_Post_vs_Pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13805 Human genes ranked by 'stat'. 50 Hallmark sets tested, 20 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.43 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.32 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.05 | NOM p=0.00e+00 | FDR q=3.17e-04 - HALLMARK_PEROXISOME | NES=1.86 | NOM p=0.00e+00 | FDR q=2.61e-03 - HALLMARK_ANGIOGENESIS | NES=1.79 | NOM p=7.05e-03 | FDR q=3.04e-03 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.63 | NOM p=5.12e-03 | FDR q=1.38e-02 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.59 | NOM p=2.12e-02 | FDR q=1.70e-02 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.44 | NOM p=1.60e-02 | FDR q=7.03e-02 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.35 | NOM p=8.42e-02 | FDR q=1.36e-01 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.31 | NOM p=4.63e-02 | FDR q=1.76e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_G2M_CHECKPOINT | NES=-1.84 | NOM p=0.00e+00 | FDR q=2.16e-03 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-1.81 | NOM p=0.00e+00 | FDR q=2.70 ... [381 more characters]

reasoning: Hallmark GSEA on the full ranking as a supporting pathway view

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["arm labels inferred from title prefixes by arm size (PE=Diet+EX n=7, PSQ=Diet-ONLY n=6)", "limma on log2CPM replaces edgeR on counts", "gene filter chosen by the agent", "Diet+EX change reflects weight loss plus exercise; the exercise-specific estimand is the exploratory arm-by-time interaction"], "results": {"time_Post_vs_Pre_arm-EX": {"n_deg": 122, "up": 84, "down": 38, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 122}, "time_Post_vs_Pre_arm-DIET": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 0}, "unpaired_EX": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 0}, "unpaired_DIET": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 0}, "exercise_interaction/ex_vs_diet_change": {"n_deg": 1, "up": 1, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 1}}, "paper_counts": {"time_Post_vs_Pre_arm-EX": 877, "time_Post_vs_Pre_arm-DIET": 1}, "comparison": {"time_Post_vs_Pre_arm-EX": {"ours": 122, "paper": 877}, "time_Post_vs_Pre_arm-DIET": {"ours": 0, "paper": 1}}, "paper_gene_check": {"time_Post_vs_Pre_arm-EX": {"PPARGC1A": {"AveExpr": 6.4514, "log2FoldChange": 0.7724, "padj": 0.0443, "pvalue": 0.0}, "MFF": {"AveExpr": 5.1715, "log2FoldChange": 0.277, "padj": 0.1277, "pvalue": 0.0078}, "CS": {"AveExpr": 8.1673, "log2FoldChange": 0.3978, "padj": 0.0639, "pvalue": 0.001 ... [2041 more characters]

reasoning: Paper counts from S1.4.p1; named genes from S1.4.p1 / FIG8 (the 12 genes were reported as increasing more in Diet+EX than Diet-ONLY by ANCOVA).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 26 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "arm label",
    "paper": "Diet-ONLY n=6, Diet+EX n=7 (FIG8)",
    "data": "GEO has no arm field; title prefixes PE (7) and PSQ (6)",
    "disposition": "executable_without_change"
  },
  {
    "item": "matrix",
    "paper": "edgeR on gene counts (S3.13.2.1.p1)",
    "data": "only moderated log2CPM deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "GEO processing note",
    "paper": "Before vs After DE",
    "data": "data_processing mentions Pearson correlation with AT pO2 (P<0.005), text apparently reused from another submission",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID37365374 / GSE230002

Status: finished (case `completed`, decision `valid`, route `declared_deviation`; contract validator 17 records, 0 errors).

## What ran

- `tools.case_runner inspect GSE230002` downloaded the series into `E:/agent/mwangLab_pdf/data/GSE230002`. The only matrix is `GSE230002_PE_all.gene_moderated_log2cpm.csv` (34,259 gene symbols x 26 samples, edgeR-style moderated log2 CPM). No raw counts are deposited.
- Prep: `prep/filter_low_expression.py` keeps genes with log2CPM >= 0 in >= 6 samples. That leaves 13,851 genes and changes no values.
- `tools.case_runner execute case_spec.json` ran with one case and these executions:
  - `time_Post_vs_Pre_arm-EX` (primary): limma, `~ subject + time`, Diet+EX only (7 pairs).
  - `time_Post_vs_Pre_arm-DIET` (secondary): the same model, Diet-ONLY only (6 pairs).
  - `unpaired_EX`, `unpaired_DIET` (sensitivity): limma `~ time` without participant blocking.
  - `exercise_interaction/ex_vs_diet_change` (exploratory): a multigroup `paired_change` model, (Post-Pre) ~ C(arm), Diet+EX vs Diet-ONLY. This tests exercise specifically.
  - Enrichment on the primary table: Enrichr ORA for up and for down DEGs, plus Hallmark GSEA on the full `stat` ranking.

## Key decisions

- Arm labels. GEO records only Before/After. The title prefixes split the 13 participants into PE (7) and PSQ (6). The paper's RNA-seq arms are Diet+EX n=7 and Diet-ONLY n=6 (FIG8), so PE = Diet+EX and PSQ = Diet-ONLY. This is the only assignment that fits the arm sizes. The data agree with it: PPARGC1A rises in 7/7 PE participants, and HMOX1 falls in 5/6 PSQ participants (HMOX1 is the paper's single Diet-ONLY DEG). Confidence: medium.
- Threshold. The paper's rule is FDR < 0.05 and |log2FC| > 0.3 (S3.13.2.1.p1, FIG8). It is applied unchanged on the limma route (`paper_on_deviation_route`). The audit rule is padj < 0.05 with no fold-change cutoff.
- Covariance. Participant is a blocking factor, because each person gave a Before and an After biopsy. The paper does not say whether its edgeR model was paired.

## DEG counts vs paper (FDR < 0.05, |log2FC| > 0.3)

| Contrast | Ours (up/down) | Paper (up/down) |
|---|---|---|
| Diet+EX After vs Before, paired | 122 (84/38) | 877 (623/254) |
| Diet-ONLY After vs Before, paired | 0 | 1 (HMOX1 down) |
| Diet+EX unpaired (sensitivity) | 0 | n/a |
| Diet-ONLY unpaired (sensitivity) | 0 | n/a |
| Exercise interaction, exploratory | 1 (MT-CO1 up) | not tested genome-wide |

Gene-level check ... [2570 more characters]
