# Review packet B (the analysis' decisions): GSE99963

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.0.subject id", "n_values": 13, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ex_Post_vs_Pre/Ex_Post_vs_Pre | 2617 | 4256 | padj < 0.1 | 3114 | 2200 | 1105 | 4256 | 5713 | 3215 | 1583 | 3365 | 0.058 | 0.273 |
| Sed_Post_vs_Pre/Sed_Post_vs_Pre | 412 | 1487 | padj < 0.1 | 873 | 620 | 255 | 1487 | 3563 | 1674 | 695 | 1678 | 0.07 | 0.176 |

## Samples per design level

### `grp`
- **Ex** (14): GSM2666595 / Post_S4; GSM2666597 / Post_S8; GSM2666598 / Post_S9; GSM2666600 / Pre_S12; GSM2666601 / Pre_S14; GSM2666602 / Pre_S1; GSM2666605 / Pre_S7; GSM2666607 / Post_S12; GSM2666608 / Post_S14; GSM2666609 / Post_S1; GSM2666612 / Post_S7; GSM2666616 / Pre_S4; GSM2666618 / Pre_S8; GSM2666619 / Pre_S9
- **Sed** (12): GSM2666592 / Post_S11; GSM2666593 / Post_S13; GSM2666594 / Post_S2; GSM2666596 / Post_S6; GSM2666599 / Pre_S10; GSM2666604 / Pre_S5; GSM2666606 / Post_S10; GSM2666611 / Post_S5; GSM2666613 / Pre_S11; GSM2666614 / Pre_S13; GSM2666615 / Pre_S2; GSM2666617 / Pre_S6

### `time`
- **Post** (13): GSM2666592 / Post_S11; GSM2666593 / Post_S13; GSM2666594 / Post_S2; GSM2666595 / Post_S4; GSM2666596 / Post_S6; GSM2666597 / Post_S8; GSM2666598 / Post_S9; GSM2666606 / Post_S10; GSM2666607 / Post_S12; GSM2666608 / Post_S14; GSM2666609 / Post_S1; GSM2666611 / Post_S5; GSM2666612 / Post_S7
- **Pre** (13): GSM2666599 / Pre_S10; GSM2666600 / Pre_S12; GSM2666601 / Pre_S14; GSM2666602 / Pre_S1; GSM2666604 / Pre_S5; GSM2666605 / Pre_S7; GSM2666613 / Pre_S11; GSM2666614 / Pre_S13; GSM2666615 / Pre_S2; GSM2666616 / Pre_S4; GSM2666617 / Pre_S6; GSM2666618 / Pre_S8; GSM2666619 / Pre_S9

### `subject`
- **S1** (2): GSM2666602 / Pre_S1; GSM2666609 / Post_S1
- **S10** (2): GSM2666599 / Pre_S10; GSM2666606 / Post_S10
- **S11** (2): GSM2666592 / Post_S11; GSM2666613 / Pre_S11
- **S12** (2): GSM2666600 / Pre_S12; GSM2666607 / Post_S12
- **S13** (2): GSM2666593 / Post_S13; GSM2666614 / Pre_S13
- **S14** (2): GSM2666601 / Pre_S14; GSM2666608 / Post_S14
- **S2** (2): GSM2666594 / Post_S2; GSM2666615 / Pre_S2
- **S4** (2): GSM2666595 / Post_S4; GSM2666616 / Pre_S4
- **S5** (2): GSM2666604 / Pre_S5; GSM2666611 / Post_S5
- **S6** (2): GSM2666596 / Post_S6; GSM2666617 / Pre_S6
- **S7** (2): GSM2666605 / Pre_S7; GSM2666612 / Post_S7
- **S8** (2): GSM2666597 / Post_S8; GSM2666618 / Pre_S8
- **S9** (2): GSM2666598 / Post_S9; GSM2666619 / Pre_S9

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE99965 (SuperSeries, S2.5.p1)", "GSE99963 (RNA-seq SubSeries)"], "assay": "total RNA-seq (Ribo-Zero), vastus lateralis biopsies, HiSeq 2500 SE100", "factors": {"group": ["Sed-HFD", "Ex-HFD"], "time": ["Pre", "Post"]}, "sample_inclusion": "13 sedentary middle-aged men: Ex-HFD n=7, Sed-HFD n=6 (TAB1); biopsy Pre and Post 9-day HFD (S2.1.p1)", "repeated_measure_unit": "subject (Pre and Post biopsy per subject)", "primary_estimand": "Within-group Post vs Pre change in muscle gene expression in Ex-HFD (HFD + 3 resistance-exercise bouts), compared with the Post vs Pre change in Sed-HFD (HFD alone); exercise effect inferred from the two lists (S3.1.p1-p2)", "planned_contrasts": ["Ex-HFD Post vs Pre, paired by subject (S2.6.p1, S3.1.p1; paper: 2617 DEGs, 1561 up / 1056 down)", "Sed-HFD Post vs Pre, paired by subject (S2.6.p1, S3.1.p1; paper: 412 DEGs, 264 up / 148 down)"], "normalization": "featureCounts gene coverage; filter rpkm > 0.1 in >= 5 samples (23,373 genes kept) (S2.6.p1, S2.3.p1)", "paper_method": "edgeR glmQLFit/glmQLFTest, y ~ Timepoint + Subject fitted separately in each group (S2.6.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.6.p1"}, "paper_results": "Sed-HFD 412 DEGs; Ex-HFD 2617 DEGs; overlap 240 up / 103 down; CHAC1 up in Ex, down in Sed; ANGPTL4 changed only in Ex (Fig5I); Table 2 Sed-only genes SLPI, IRAK2, NUPR1 up, FGF6, MDH1 down"}

reasoning: S2.1.p1 parallel-group pre/post design; S2.6.p1 gives exact model (edgeR QL, ~Timepoint+Subject per group) and FDR<0.1; S3.1.p1 gives counts. The paper never fits a group x time interaction; the exercise effect is read off the contrast between within-group lists.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE99963\\GSE99963_GeneCoverage.tsv.gz", "owned": true, "checks": ["GSE99963 is a SubSeries of GSE99965 named in S2.5.p1 (metadata series_id GSE99963,GSE99965)", "Homo sapiens muscle, Sed-HFD/Ex-HFD x Pre/Post labels match S2.1.p1", "data_processing: Rsubread + featureCounts + edgeR, matching S2.6.p1"], "accession": "GSE99963", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE99963\\GSE99963_metadata.csv"}

reasoning: Accession, groups, tissue and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 28, "n_metadata": 28, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM2666603": "Pre_S3: library of 102,811 assigned reads (median ~7.9M; S2.3.p1 reports ~8.5M/sample) - failed library; the paper's Sed-HFD n=6 (TAB1) vs 7 deposited subjects implies one Sed subject was dropped, and S3 is the only failed one", "GSM2666610": "Post_S3: its Pre partner is excluded, so subject S3 contributes nothing to a within-subject Post vs Pre estimate; dropped to match the paper's 13 subjects"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\aligned\\aligned_metadata_kept.csv", "columns": {"subject": {"alias_of": "characteristics_ch1.0.subject id"}, "time": {"source": "title", "regex": "^(Pre|Post)_S\\d+$"}, "grp": {"source": "characteristics_ch1.1.group", "regex": "^(Sedentary|Exercise);", "recode": {"Sedentary": "Sed", "Exercise": "Ex"}}, "ex_post": {"combine": ["grp", "time"], "separator": "_", "of": "recoded values", "recode": {"Ex_Post": "1", "Ex_Pre": "0", "Sed_Post": "0", "Sed_Pre": "0"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\aligned\\design_metadata.csv", "sha256": "e6d89475d18e2a49fbc0cbb6c8f6171d55c4034b34c8140f090a91cae8cb9c9f", "levels": {"subject": {"S11": 2, "S13": 2, "S2": 2, "S4": 2, "S6": 2, "S8": 2, "S9": 2, "S10": 2, "S12": 2, "S14": 2, "S1": 2, "S5": 2, "S ... [102 more characters]

reasoning: Matrix columns equal metadata title (28/28). time from title prefix, grp from group characteristic, subject from subject id (each subject has Pre and Post). Subject S3 removed (see exclude_samples).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\aligned\\aligned_matrix.csv", "sha256": "bb04f35184183e37cd55b729f9180ec4816ad13e3c175f58d77a9beb51d81b3c", "n_features": 60675, "n_samples": 26, "annotation_columns_dropped": ["GSM2666603", "GSM2666610"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 7055510.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 7.06e6, column sums 3-19M (one 0.1M) consistent with per-gene read counts; file GeneCoverage, data_processing 'gene read coverages were computed with featureCounts'; paper uses edgeR on these counts (S2.6.p1).

### design (valid, not_started)

final: {"analysis_type": "repeated measures, two parallel groups: paired Post vs Pre within each group (paper route) plus exploratory group x time interaction", "formula": "~ subject + time (within each grp)", "contrasts": [{"name": "Ex_Post_vs_Pre", "control": "Pre", "treatment": "Post", "role": "primary"}, {"name": "Sed_Post_vs_Pre", "control": "Pre", "treatment": "Post", "role": "secondary"}, {"name": "ExVsSed_change_interaction", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: Paper analyses each group's Post vs Pre with subject blocking (S2.6.p1). The Ex-HFD change mixes HFD and exercise; the exercise-specific effect is the difference in change (interaction), which the paper approximates by comparing lists (S3.1.p2). Interaction run as exploratory since the paper did not test it. grp is treated as a stratum for the paper-route paired contrasts.

rejected alternatives: [{"value": "Ex-HFD Post vs Sed-HFD Post (cross-sectional)", "reason_rejected": "ignores baseline and pairing; paper does not do it and S3.1.p1 PCA shows no group separation"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp) + C(time) + C(subject)", "n_samples": 26, "n_columns": 15, "columns": ["Intercept", "grp_Sed", "time_Pre", "subject_S10", "subject_S11", "subject_S12", "subject_S13", "subject_S14", "subject_S2", "subject_S4", "subject_S5", "subject_S6", "subject_S7", "subject_S8", "subject_S9"], "rank": 14, "full_rank": false, "residual_df": 12, "levels": {"grp": {"Ex": 14, "Sed": 12}, "time": {"Post": 13, "Pre": 13}, "subject": {"S11": 2, "S13": 2, "S2": 2, "S4": 2, "S6": 2, "S8": 2, "S9": 2, "S10": 2, "S12": 2, "S14": 2, "S1": 2, "S5": 2, "S7": 2}}, "cells": [{"cell": ["Ex", "Post", "S1"], "n": 1}, {"cell": ["Ex", "Post", "S12"], "n": 1}, {"cell": ["Ex", "Post", "S14"], "n": 1}, {"cell": ["Ex", "Post", "S4"], "n": 1}, {"cell": ["Ex", "Post", "S7"], "n": 1}, {"cell": ["Ex", "Post", "S8"], "n": 1}, {"cell": ["Ex", "Post", "S9"], "n": 1}, {"cell": ["Ex", "Pre", "S1"], "n": 1}, {"cell": ["Ex", "Pre", "S12"], "n": 1}, {"cell": ["Ex", "Pre", "S14"], "n": 1}, {"cell": ["Ex", "Pre", "S4"], "n": 1}, {"cell": ["Ex", "Pre", "S7"], "n": 1}, {"cell": ["Ex", "Pre", "S8"], "n": 1}, {"cell": ["Ex", "Pre", "S9"], "n": 1}, {"cell": ["Sed", "Post", "S10"], "n": 1}, {"cell": ["Sed", "Post", "S11"], "n": 1}, {"cell": ["Sed", "Post", "S13"], "n": 1}, {"cell": ["Sed", "Post", "S2"], "n": 1}, {"cell": ["Sed", "Post", "S5"], "n": 1}, {"cell": ["Sed", "Post", "S6"], "n": 1}, {"cell": ["Sed", "Pre ... [4411 more characters]

reasoning: Pre and Post biopsies from the same man: subject as a fixed blocking effect, as in the paper (y ~ Timepoint + Subject). No batch column in GEO; no other covariates added.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "edgeR QL F-test (R edgeR glmQLFit/glmQLFTest, TMM)", "formula": "~ subject + time", "paper_route": {"method": "edgeR glmQLFit/glmQLFTest ~ Timepoint + Subject per group", "status": "reproduced"}, "deviations": ["Low-expression filter: paper keeps genes with rpkm > 0.1 in >= 5 samples; gene lengths are not deposited, so CPM >= 0.15 in >= 5 of the execution's samples is used (gives ~23k genes across all samples, close to the paper's 23,373), applied per group", "Annotation: GEO counts use Ensembl v84 (data_processing) while the paper text says Gencode; used as deposited", "glmQLFit robust=TRUE / estimateDisp robust=TRUE (executor default); paper does not state robust settings", "Exploratory interaction (~ subject + time + ex_post) is not in the paper"]}

reasoning: Raw counts; the paper's own edgeR QL route can be run with tools.r_de_tools (engine edger_ql) with subject as fixed effect.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S2.6.p1: genes with FDR below 0.1 considered DE; no fold-change rule. Audit at workflow default FDR<0.05.

### execution (valid, completed)

final: {"method": "edgeR QL (R) ~ subject + time, Ex-HFD only", "subset": "Ex_Post_vs_Pre", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\Ex_Post_vs_Pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\Ex_Post_vs_Pre\\DEG_results_Ex_Post_vs_Pre.csv"], "counts": {"Ex_Post_vs_Pre/Ex_Post_vs_Pre": {"applied": {"rule": "padj < 0.1", "n_tested": 20940, "n_significant": 4256, "n_up": 2292, "n_down": 1964, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 20940, "n_significant": 3114, "n_up": 1749, "n_down": 1365, "deg_sanity": "ok"}}}}

reasoning: Paper route S2.6.p1 for HFD + resistance exercise group (7 subjects paired).

### execution (valid, completed)

final: {"method": "edgeR QL (R) ~ subject + time, Sed-HFD only", "subset": "Sed_Post_vs_Pre", "role": "secondary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\Sed_Post_vs_Pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\Sed_Post_vs_Pre\\DEG_results_Sed_Post_vs_Pre.csv"], "counts": {"Sed_Post_vs_Pre/Sed_Post_vs_Pre": {"applied": {"rule": "padj < 0.1", "n_tested": 20230, "n_significant": 1487, "n_up": 802, "n_down": 685, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 20230, "n_significant": 873, "n_up": 472, "n_down": 401, "deg_sanity": "ok"}}}}

reasoning: Paper route S2.6.p1 for HFD-alone group (6 subjects paired); reference for the exercise comparison.

### execution (valid, completed)

final: {"method": "edgeR QL (R) ~ subject + time + ex_post (group x time interaction)", "subset": "ExVsSed_change_interaction", "role": "exploratory", "tool": "tools.r_de_tools:run_r_de", "n_samples": 26, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\ExVsSed_change_interaction\\input\\matrix_filtered.csv", "formula": "~ subject + time + ex_post", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\ExVsSed_change_interaction\\DEG_results_ExVsSed_change_interaction.csv"], "counts": {"ExVsSed_change_interaction/ExVsSed_change_interaction": {"applied": {"rule": "padj < 0.1", "n_tested": 23198, "n_significant": 2, "n_up": 1, "n_down": 1, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 23198, "n_significant": 2, "n_up": 1, "n_down": 1, "deg_sanity": "ok"}}}}

reasoning: Exercise-specific effect: (Ex Post-Pre) - (Sed Post-Pre). ex_post = 1 for Ex-HFD Post samples; with subject fixed effects grp main effect is absorbed. Not in the paper.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "Ex_Post_vs_Pre/Ex_Post_vs_Pre", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\ora_up\\DEG_results_Ex_Post_vs_Pre_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\ora_up\\DEG_results_Ex_Post_vs_Pre_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\ora_up\\DEG_results_Ex_Post_vs_Pre_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\ora_up\\DEG_results_Ex_Post_vs_Pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 2250 Human genes (direction=up, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Extracellular Matrix Organization (GO:0030198) | padj=3.75e-14 | over ... [1271 more characters]

reasoning: S3.1.p2 GO on Ex-HFD up genes

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "Ex_Post_vs_Pre/Ex_Post_vs_Pre", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\ora_down\\DEG_results_Ex_Post_vs_Pre_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\ora_down\\DEG_results_Ex_Post_vs_Pre_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\ora_down\\DEG_results_Ex_Post_vs_Pre_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\ora_down\\DEG_results_Ex_Post_vs_Pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 1804 Human genes (direction=down, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Aerobic Electron Transport Chain (GO:0019646) | padj=9.34 ... [1281 more characters]

reasoning: S3.1.p2 GO on Ex-HFD down genes (circadian rhythm top)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "Ex_Post_vs_Pre/Ex_Post_vs_Pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID29123172\\GSE99963\\results\\enrichment_Ex_Post_vs_Pre_Ex_Post_vs_Pre\\gsea\\DEG_results_Ex_Post_vs_Pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 18699 Human genes ranked by 'stat'. 50 Hallmark sets tested, 43 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=3.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.67 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=2.61 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.55 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.53 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.41 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.25 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.50 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES= ... [417 more characters]

reasoning: Hallmark GSEA as a full-ranking complement

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Subject S3 excluded (failed Pre library) to match the paper's n=13; the paper does not name the excluded subject", "Low-expression filter approximated by CPM because gene lengths are not deposited", "The Ex-HFD Post vs Pre change includes the HFD effect; the exercise-specific effect is only addressed by the exploratory interaction"], "results": {"Ex_Post_vs_Pre/Ex_Post_vs_Pre": {"n_deg": 4256, "up": 2292, "down": 1964, "rule": "padj < 0.1", "audit_n": 3114}, "Sed_Post_vs_Pre/Sed_Post_vs_Pre": {"n_deg": 1487, "up": 802, "down": 685, "rule": "padj < 0.1", "audit_n": 873}, "ExVsSed_change_interaction/ExVsSed_change_interaction": {"n_deg": 2, "up": 1, "down": 1, "rule": "padj < 0.1", "audit_n": 2}}, "paper_counts": {"Ex_Post_vs_Pre/Ex_Post_vs_Pre": 2617, "Sed_Post_vs_Pre/Sed_Post_vs_Pre": 412}, "comparison": {"Ex_Post_vs_Pre/Ex_Post_vs_Pre": {"ours": 4256, "paper": 2617}, "Sed_Post_vs_Pre/Sed_Post_vs_Pre": {"ours": 1487, "paper": 412}}, "paper_gene_check": {"Ex_Post_vs_Pre/Ex_Post_vs_Pre": {"ENSG00000167772": {"baseMean": 6.2844, "log2FoldChange": 3.1956, "padj": 0.000204, "pvalue": 5.13e-06}, "ENSG00000128965": {"baseMean": 0.6711, "log2FoldChange": 1.7651, "padj": 0.0197, "pvalue": 0.00206}}, "Sed_Post_vs_Pre/Sed_Post_vs_Pre": {"ENSG00000124107": {"baseMean": 1.4965, "log2FoldChange": 2.7519, "padj": 0.000372, "pvalue": 9.56e-07}, "ENSG00000134070": {"baseMean": 5.7632, "log2FoldChange": 1.0075, "padj": 0.00141, "pvalue": 7.03e-06}, "ENSG ... [410 more characters]

reasoning: Ex genes: ANGPTL4 (up, Fig5I/S3.4.p2), CHAC1 (up in Ex, S3.2.p1). Sed genes: Table 2 SLPI/IRAK2/NUPR1 up, FGF6/MDH1 down; CHAC1 down in Sed.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); grp: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
- | Sex | pass | Sex inference completed on 26 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample size",
    "paper": "13 subjects (Ex 7, Sed 6), TAB1",
    "data": "14 subjects deposited (7+7); Pre_S3 has 0.1M reads",
    "disposition": "subject S3 excluded; recorded as assumption"
  },
  {
    "item": "gene filter",
    "paper": "rpkm > 0.1 in >= 5 samples (23,373 genes)",
    "data": "no gene lengths deposited",
    "disposition": "CPM >= 0.15 in >= 5 samples as approximation (declared deviation)"
  },
  {
    "item": "annotation",
    "paper": "Gencode (S2.6.p1)",
    "data": "Ensembl v84 per GEO data_processing",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID29123172 / GSE99963

**Status: finished.** The case-spec route ran through `tools.case_runner execute`. The decision-contract validator passed: 15 records, 0 errors. Final route: `paper_aligned`.

## What ran
- **Data:** `GSE99963_GeneCoverage.tsv.gz`. This holds featureCounts raw integer counts for 60,675 Ensembl genes × 28 samples, from 14 men at Pre and Post. Columns were aligned exactly on `title` (28/28).
- **Exclusion:** subject **S3** (GSM2666603 Pre_S3 and GSM2666610 Post_S3) was dropped. Pre_S3 has 102,811 assigned reads, against a median of about 7.9M. The paper reports 13 subjects (Ex 7 / Sed 6, Table 1) while GEO deposits 7+7, so one Sed subject must have been dropped. S3 is the only failed library. This is an assumption: the paper does not name the dropped subject. Analysed: Ex 7 subjects, Sed 6 subjects.
- **Method:** the paper's route (S2.6.p1), run through `tools.r_de_tools:run_r_de` with engine `edger_ql`. That is R edgeR with TMM, `glmQLFit`/`glmQLFTest`, and the design `~ subject + time`, fitted separately in each group.
  - Primary: Ex-HFD Post vs Pre.
  - Secondary: Sed-HFD Post vs Pre.
  - Exploratory (not in the paper): the group × time interaction, `~ subject + time + ex_post` with coefficient `ex_post`. It estimates the exercise-specific change, (Ex Post−Pre) − (Sed Post−Pre).
- **Threshold:** the paper's rule, FDR < 0.1 with no fold-change cutoff (S2.6.p1). Audit rule: FDR < 0.05.
- **Enrichment** on the Ex-HFD table: GO/KEGG ORA up and down, plus Hallmark GSEA. All three completed.

## DEG counts vs paper (FDR < 0.1)
| Contrast | Ours (up/down) | Paper (up/down) | Audit FDR<0.05 |
|---|---|---|---|
| Ex-HFD Post vs Pre | 4256 (2292/1964) | 2617 (1561/1056) | 3114 |
| Sed-HFD Post vs Pre | 1487 (802/685) | 412 (264/148) | 873 |
| Interaction (exploratory) | 2 (1/1) | not tested | 2 |

- **Named genes:** every gene the paper names agrees in direction and is significant.
  - Sed: SLPI +2.75, IRAK2 +1.01, NUPR1 +0.76, MDH1 −0.80, FGF6 −1.04. These log2FC values almost exactly match Table 2.
  - CHAC1 goes up in Ex (+1.77) and down in Sed (−3.04), as S3.2.p1 reports.
  - ANGPTL4 goes up in Ex (+3.20; Fig 5I).
- **Interaction:** the formal test finds only 2 genes, and CHAC1 is the top one (FDR 0.013). So the paper's claim that thousands of genes respond to exercise rests on comparing two within-group lists. The data do not back it as a group × time difference at this n.
- **Ex-HFD enrichment:** genes going up are enric ... [2035 more characters]
