# Review packet B (the analysis' decisions): GSE205907

## Mechanical flags

- **unused_subject_like_column**: {"column": "animal", "n_values": 12, "max_repeat": 4, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "animal", "across": "tissue", "pairs_or_sets": 12, "samples_linked": 48, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Samples per design level

### `grp`
- **EX** (16): E26Cereb; E26Corte; E26Nigra; E26Stria; E27Cereb; E27Corte; E27Nigra; E27Stria; E28Cereb; E28Corte; E28Nigra; E28Stria; E29Cereb; E29Corte; E29Nigra; E29Stria
- **MPTP** (16): M16Cereb; M16Corte; M16Nigra; M16Stria; M21Cereb; M21Corte; M21Nigra; M21Stria; M23Cereb; M23Corte; M23Nigra; M23Stria; M6Cereb; M6Corte; M6Nigra; M6Stria
- **SAL** (16): S1Cereb; S1Cortex; S1Nigra; S1Stria; S2Cereb; S2Cortex; S2Nigra; S2Stria; S3Cereb; S3Cortex; S3Nigra; S3Stria; S4Cereb; S4Cortex; S4Nigra; S4Stria

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE205907"], "assay": "bulk RNA-seq (Illumina NextSeq 500), mouse brain; 4 regions (cerebellum, cortex, SN, striatum)", "organism": "Mouse (C57BL/6J, female) (S2.1.p1)", "factors": {"group": ["Saline", "MPTP", "MPTP+EX"], "region": ["cerebellum", "cortex", "SN", "striatum"]}, "sample_inclusion": "n=4 animals per group for RNA-seq; all 4 regions dissected from each animal (S2.5.p1); a separate cohort of 5/group was used for histology only", "primary_estimand": "Effect of 12-week treadmill exercise in MPTP-induced PD mice: MPTP+EX vs MPTP, within each brain region (S3.2.p1, S3.3.p1, FIG3)", "planned_contrasts": ["MPTP+EX vs MPTP per region (exercise effect in PD; S3.2.p1, FIG2B/D)", "MPTP vs Saline per region (PD model effect; S3.2.p1, FIG2A/D)", "Reversal sets in SN and striatum: genes significant in both contrasts with opposite direction (S3.3.p1, FIG3A/D): SN 155 down / 66 up after exercise; striatum 49 down / 185 up"], "repeated_measure_unit": "animal (4 regions per animal); regions analyzed separately so each animal appears once per fit", "normalization": "Tophat2 + Cufflinks/Cuffquant FPKM, RSEM (S2.7.p1)", "paper_method": "DESeq (v1.14.0), per region; DEG if FPKM > 1 and p < 0.05 (S2.7.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "expression_filter": "FPKM > 1", "source_locator": "S2.7.p1; FIG3 legend"}, "paper_results": {"SN_reversal_after_exercise": {"down": 155, "up": 66}, "str ... [150 more characters]

reasoning: S2.5.p1 gives n=4 per group for RNA-seq across 4 regions; S2.7.p1 gives the method (DESeq) and DEG rule (FPKM>1, p<0.05, raw p, no fold-change cutoff). S3.2.p1 and FIG2 compare MPTP vs saline and MPTP+EX vs MPTP per region. S3.3.p1/FIG3 report counts only for reversal sets (opposite direction in the two contrasts), not per-contrast DEG totals; per-contrast totals are only in FIG2D Venn diagrams, not in the text.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\prep\\GSE205907_fpkm_clean.csv", "owned": true, "checks": ["S6.p1 names GSE205907", "GEO series: 48 samples = 3 treatments x 4 regions x 4 reps, matching S2.5.p1", "matrix GSE205907_fpkm has 48 columns encoding the same 3 groups x 4 regions x 4 animals", "tissue markers match region labels (Pcp2/Gabra6 cerebellum, Satb2/Neurod6 cortex, Th/Slc6a3 SN, Ppp1r1b/Penk striatum)", "Th/Slc6a3 in SN ~4-7x lower in E and M animals than S animals, consistent with MPTP lesion (S3.5.p1: ~70% TH+ loss)", "Xist expressed and no Y-linked genes in every sample: all female as in S2.1.p1"], "accession": "GSE205907", "metadata_file": "E:/agent/mwangLab_pdf/test/experiments/large_run_pilot_20261019/runs_claude/PMID35813950/prep/GSE205907_sample_sheet.csv"}

reasoning: Only supplementary file of the series; the paper's data availability statement names GSE205907. Marker genes corroborate region and lesion labels.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 48, "n_metadata": 48, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\aligned\\aligned_metadata.csv", "columns": {}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\aligned\\design_metadata.csv", "sha256": "b3f6caef3feda3884ca4fd632fe836bef3c39d5a0e3f107f7a88179746b4b596", "levels": {}}}

reasoning: The deposited matrix columns (E26Nigra, M6Stria, S1Cortex, ...) carry animal ID, group and region, while GEO titles carry only '<region>,<treatment>,rep<k>'; no field links animal IDs to rep numbers or GSM IDs except column order, and positional alignment is not allowed. The metadata is therefore a sample sheet derived deterministically from the matrix column names by prep_GSE205907.py (prefix E=MPTP+exercise, M=MPTP, S=Saline; suffix = region), exact-matched on the index. The derived group x region table equals the GEO treatment x tissue table (4 per cell), S=Saline is corroborated by preserved nigral Th/Slc6a3, and E/M are the two MPTP-lesioned groups; E vs M decoding rests on the letters  ... [84 more characters]

rejected alternatives: [{"value": "GEO metadata with key from title", "reason_rejected": "titles hold rep numbers, matrix holds animal IDs; mapping rep k to an animal ID would be positional"}]

### matrix (valid, not_started)

final: {"source": "GSE205907_fpkm.csv (file name 'fpkm')", "paper_input": "FPKM from Cuffquant/RSEM (S2.7.p1)", "matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\aligned\\aligned_matrix.csv", "sha256": "2225bef2ea7721a8152a04abd61357c7ec0c35904c6d20f3d3b50002945a4c5a", "n_features": 23339, "n_samples": 48, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 8911.957031, "median": 2.118468, "integer_fraction": 0.2642, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Values are non-integer (only zeros are integral; 2.4e-6 of non-zero values are integers), column sums 345k-621k (not library sizes, typical of FPKM), the file name says fpkm and the paper says FPKM. GEO data_processing mentions HTSeq counts, but the deposited values are not counts. Linear normalized scale -> log2(x+1) and limma. 27 gene IDs mangled by Excel into dates were dropped (prep script).

### design (valid, not_started)

final: {"analysis_type": "multi-group per stratum", "design_column": "grp", "formula": "~ 0 + grp (within each region)", "contrasts": [{"name": "grp_EX_vs_MPTP_tissue-Cereb", "control": "MPTP", "treatment": "EX", "role": "primary"}, {"name": "grp_EX_vs_MPTP_tissue-Cortex", "control": "MPTP", "treatment": "EX", "role": "primary"}, {"name": "grp_EX_vs_MPTP_tissue-Nigra", "control": "MPTP", "treatment": "EX", "role": "primary"}, {"name": "grp_EX_vs_MPTP_tissue-Stria", "control": "MPTP", "treatment": "EX", "role": "primary"}, {"name": "grp_MPTP_vs_SAL_tissue-Cereb", "control": "SAL", "treatment": "MPTP", "role": "secondary"}, {"name": "grp_MPTP_vs_SAL_tissue-Cortex", "control": "SAL", "treatment": "MPTP", "role": "secondary"}, {"name": "grp_MPTP_vs_SAL_tissue-Nigra", "control": "SAL", "treatment": "MPTP", "role": "secondary"}, {"name": "grp_MPTP_vs_SAL_tissue-Stria", "control": "SAL", "treatment": "MPTP", "role": "secondary"}, {"name": "grp_EX_vs_SAL_tissue-Cereb", "control": "SAL", "treatment": "EX", "role": "exploratory"}, {"name": "grp_EX_vs_SAL_tissue-Cortex", "control": "SAL", "treatment": "EX", "role": "exploratory"}, {"name": "grp_EX_vs_SAL_tissue-Nigra", "control": "SAL", "treatment": "EX", "role": "exploratory"}, {"name": "grp_EX_vs_SAL_tissue-Stria", "control": "SAL", "treatment": "EX", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\sui ... [68 more characters]

reasoning: Three-level group factor (Saline, MPTP, MPTP+EX), analyzed separately in each region as in the paper (S3.2.p1). One limma model per region with planned contrasts, no pooled levels. Exercise estimand = MPTP+EX vs MPTP (the paper has no healthy exercised arm, so this is exercise within PD only). MPTP vs Saline is needed for the paper's reversal sets. EX vs SAL is exploratory. Regions are strata; comparisons never cross them.

rejected alternatives: [{"value": "one model over all 48 samples with animal blocking", "reason_rejected": "paper analyzes each region separately; regions differ massively, so a shared variance model would not match the paper's estimand"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 48, "n_columns": 3, "columns": ["Intercept", "grp_MPTP", "grp_SAL"], "rank": 3, "full_rank": true, "residual_df": 45, "levels": {"grp": {"EX": 16, "MPTP": 16, "SAL": 16}}, "cells": [{"cell": ["EX"], "n": 16}, {"cell": ["MPTP"], "n": 16}, {"cell": ["SAL"], "n": 16}], "min_cell_size": 16, "missing_values": {}}, "confounding": [{"column": "animal", "n_levels": 12, "status": "nested_in_primary", "crosstab": {"EX": {"E26": 4, "E27": 4, "E28": 4, "E29": 4, "M16": 0, "M21": 0, "M23": 0, "M6": 0, "S1": 0, "S2": 0, "S3": 0, "S4": 0}, "MPTP": {"E26": 0, "E27": 0, "E28": 0, "E29": 0, "M16": 4, "M21": 4, "M23": 4, "M6": 4, "S1": 0, "S2": 0, "S3": 0, "S4": 0}, "SAL": {"E26": 0, "E27": 0, "E28": 0, "E29": 0, "M16": 0, "M21": 0, "M23": 0, "M6": 0, "S1": 4, "S2": 4, "S3": 4, "S4": 4}}}, {"column": "tissue", "n_levels": 4, "status": "crossed", "crosstab": {"EX": {"Cereb": 4, "Cortex": 4, "Nigra": 4, "Stria": 4}, "MPTP": {"Cereb": 4, "Cortex": 4, "Nigra": 4, "Stria": 4}, "SAL": {"Cereb": 4, "Cortex": 4, "Nigra": 4, "Stria": 4}}}]}

reasoning: Within a region each animal contributes one sample, so animals are independent units; no batch, sex (all female) or other covariate is recorded. The 4-regions-per-animal structure is not relevant to per-region fits.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (limma-trend on log2(FPKM+1))", "formula": "~ 0 + grp", "paper_route": {"method": "DESeq (v1.14.0) negative binomial", "status": "blocked", "reason": "only FPKM was deposited; DESeq needs raw counts (GEO data_processing mentions HTSeq counts but they are not deposited)"}, "deviations": ["limma on log2(FPKM+1) instead of DESeq on counts", "FPKM>1 filter interpreted as FPKM>=1 in >=4 of the 12 region samples", "27 Excel-mangled gene IDs (Marchf/Septin) dropped"], "transform": "log2(x+1)"}

reasoning: Matrix-method policy: linear FPKM -> log2(x+1) -> limma. Paper's DESeq route cannot run on FPKM; declared deviation.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "paper rule (raw p < 0.05, no fold-change cutoff, FPKM > 1 expression filter) applied to limma p-values; BH FDR < 0.05 reported as audit"}

reasoning: S2.7.p1: 'DEGs which FPKM > 1 and p < 0.05'; FIG3 legend repeats FPKM > 1, P < 0.05. Raw p, no fold-change rule.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_Cereb", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Cereb\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Cereb\\DEG_results_grp_EX_vs_MPTP_tissue-Cereb.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Cereb\\DEG_results_grp_MPTP_vs_SAL_tissue-Cereb.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Cereb\\DEG_results_grp_EX_vs_SAL_tissue-Cereb.csv"], "counts": {"limma_Cereb/grp_EX_vs_MPTP_tissue-Cereb": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13176, "n_significant": 737, "n_up": 434, "n_down": 303, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13176, "n_significant": 2, "n_up": 0, "n_down": 2, "deg_sanity": "ok"}}, "limma_Cereb/grp_MPTP_vs_SAL_tissue-Cereb": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13176, "n_significant": 1469, "n_up": 743, "n_down": 726, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13176, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_Cereb/grp_EX_vs_SAL_tissue-Cereb": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13176, "n_sig ... [185 more characters]

reasoning: Per-region fit (cerebellum) as in the paper (S2.7.p1, S3.2.p1: DEGs per brain region). One limma model on the 12 cerebellum samples (~0+grp); planned EX vs MPTP (exercise effect in PD model, primary) and MPTP vs SAL (PD model effect, needed for the paper's reversal sets); EX vs SAL is an extra exploratory comparison. FPKM>1 expression filter from S2.7.p1 applied as FPKM>=1 in >=4 of the 12 samples (one group's worth).

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_Cortex", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Cortex\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Cortex\\DEG_results_grp_EX_vs_MPTP_tissue-Cortex.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Cortex\\DEG_results_grp_MPTP_vs_SAL_tissue-Cortex.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Cortex\\DEG_results_grp_EX_vs_SAL_tissue-Cortex.csv"], "counts": {"limma_Cortex/grp_EX_vs_MPTP_tissue-Cortex": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13288, "n_significant": 773, "n_up": 421, "n_down": 352, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13288, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_Cortex/grp_MPTP_vs_SAL_tissue-Cortex": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13288, "n_significant": 2586, "n_up": 1235, "n_down": 1351, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13288, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_Cortex/grp_EX_vs_SAL_tissue-Cortex": {"applied": {"rule": "pvalue < 0.05", "n_tested ... [202 more characters]

reasoning: Per-region fit (cortex) as in the paper (S2.7.p1, S3.2.p1: DEGs per brain region). One limma model on the 12 cortex samples (~0+grp); planned EX vs MPTP (exercise effect in PD model, primary) and MPTP vs SAL (PD model effect, needed for the paper's reversal sets); EX vs SAL is an extra exploratory comparison. FPKM>1 expression filter from S2.7.p1 applied as FPKM>=1 in >=4 of the 12 samples (one group's worth).

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_Nigra", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Nigra\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Nigra\\DEG_results_grp_EX_vs_MPTP_tissue-Nigra.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Nigra\\DEG_results_grp_MPTP_vs_SAL_tissue-Nigra.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Nigra\\DEG_results_grp_EX_vs_SAL_tissue-Nigra.csv"], "counts": {"limma_Nigra/grp_EX_vs_MPTP_tissue-Nigra": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13743, "n_significant": 1015, "n_up": 490, "n_down": 525, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13743, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_Nigra/grp_MPTP_vs_SAL_tissue-Nigra": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13743, "n_significant": 1516, "n_up": 771, "n_down": 745, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13743, "n_significant": 83, "n_up": 8, "n_down": 75, "deg_sanity": "ok"}}, "limma_Nigra/grp_EX_vs_SAL_tissue-Nigra": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13743, "n_ ... [192 more characters]

reasoning: Per-region fit (SN) as in the paper (S2.7.p1, S3.2.p1: DEGs per brain region). One limma model on the 12 SN samples (~0+grp); planned EX vs MPTP (exercise effect in PD model, primary) and MPTP vs SAL (PD model effect, needed for the paper's reversal sets); EX vs SAL is an extra exploratory comparison. FPKM>1 expression filter from S2.7.p1 applied as FPKM>=1 in >=4 of the 12 samples (one group's worth).

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_Stria", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Stria\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Stria\\DEG_results_grp_EX_vs_MPTP_tissue-Stria.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Stria\\DEG_results_grp_MPTP_vs_SAL_tissue-Stria.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Stria\\DEG_results_grp_EX_vs_SAL_tissue-Stria.csv"], "counts": {"limma_Stria/grp_EX_vs_MPTP_tissue-Stria": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13470, "n_significant": 509, "n_up": 212, "n_down": 297, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13470, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_Stria/grp_MPTP_vs_SAL_tissue-Stria": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13470, "n_significant": 147, "n_up": 64, "n_down": 83, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13470, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_Stria/grp_EX_vs_SAL_tissue-Stria": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13470, "n_signif ... [180 more characters]

reasoning: Per-region fit (striatum) as in the paper (S2.7.p1, S3.2.p1: DEGs per brain region). One limma model on the 12 striatum samples (~0+grp); planned EX vs MPTP (exercise effect in PD model, primary) and MPTP vs SAL (PD model effect, needed for the paper's reversal sets); EX vs SAL is an extra exploratory comparison. FPKM>1 expression filter from S2.7.p1 applied as FPKM>=1 in >=4 of the 12 samples (one group's worth).

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "limma_Stria_noE29", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 11, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Stria_noE29\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Stria_noE29\\DEG_results_grp_EX_vs_MPTP_tissue-Stria.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\limma_Stria_noE29\\DEG_results_grp_MPTP_vs_SAL_tissue-Stria.csv"], "counts": {"limma_Stria_noE29/grp_EX_vs_MPTP_tissue-Stria": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13429, "n_significant": 1284, "n_up": 595, "n_down": 689, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13429, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "limma_Stria_noE29/grp_MPTP_vs_SAL_tissue-Stria": {"applied": {"rule": "pvalue < 0.05", "n_tested": 13429, "n_significant": 1319, "n_up": 722, "n_down": 597, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13429, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Sensitivity only: E29Stria is a sample-level outlier (mean log2 correlation with the other striatum samples 0.83 vs 0.97 for every other sample; FPKM column sum 621k vs 345-400k; Xist 12 vs 62-80). The paper gives no exclusion, so the primary striatum fit keeps it; this refit drops it (EX n=3).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_Nigra/grp_EX_vs_MPTP_tissue-Nigra", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Nigra_grp_EX_vs_MPTP_tissue-Nigra\\ora\\DEG_results_grp_EX_vs_MPTP_tissue-Nigra_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Nigra_grp_EX_vs_MPTP_tissue-Nigra\\ora\\DEG_results_grp_EX_vs_MPTP_tissue-Nigra_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Nigra_grp_EX_vs_MPTP_tissue-Nigra\\ora\\DEG_results_grp_EX_vs_MPTP_tissue-Nigra_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Nigra_grp_EX_vs_MPTP_tissue-Nigra\\ora\\DEG_results_grp_EX_vs_MPTP_tissue-Nigra_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 1015 Mouse genes (direction=all, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10  ... [1368 more characters]

reasoning: Paper reports GO/KEGG pathways (DAVID) for exercise-affected genes in SN and striatum (S3.3.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_Nigra/grp_EX_vs_MPTP_tissue-Nigra", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Nigra_grp_EX_vs_MPTP_tissue-Nigra\\gsea\\DEG_results_grp_EX_vs_MPTP_tissue-Nigra_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13743 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 9 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=1.79 | NOM p=0.00e+00 | FDR q=6.24e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.66 | NOM p=0.00e+00 | FDR q=1.71e-02 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.63 | NOM p=9.04e-03 | FDR q=1.91e-02 - HALLMARK_ANDROGEN_RESPONSE | NES=1.38 | NOM p=4.48e-02 | FDR q=1.74e-01 - HALLMARK_KRAS_SIGNALING_UP | NES=1.28 | NOM p=7.20e-02 | FDR q=3.39e-01 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.27 | NOM p=1.13e-01 | FDR q=3.14e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.25 | NOM p=7.60e-02 | FDR q=3.09e-01 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.22 | NOM p=1.19e-01 | FDR q=3.63e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=-1.72 | NOM p=0.00e+00 | FDR  ... [450 more characters]

reasoning: Paper reports GO/KEGG pathways (DAVID) for exercise-affected genes in SN and striatum (S3.3.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_Stria/grp_EX_vs_MPTP_tissue-Stria", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Stria_grp_EX_vs_MPTP_tissue-Stria\\ora\\DEG_results_grp_EX_vs_MPTP_tissue-Stria_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Stria_grp_EX_vs_MPTP_tissue-Stria\\ora\\DEG_results_grp_EX_vs_MPTP_tissue-Stria_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Stria_grp_EX_vs_MPTP_tissue-Stria\\ora\\DEG_results_grp_EX_vs_MPTP_tissue-Stria_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Stria_grp_EX_vs_MPTP_tissue-Stria\\ora\\DEG_results_grp_EX_vs_MPTP_tissue-Stria_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 509 Mouse genes (direction=all, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 t ... [1368 more characters]

reasoning: Paper reports GO/KEGG pathways (DAVID) for exercise-affected genes in SN and striatum (S3.3.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "limma_Stria/grp_EX_vs_MPTP_tissue-Stria", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35813950\\GSE205907\\results\\enrichment_limma_Stria_grp_EX_vs_MPTP_tissue-Stria\\gsea\\DEG_results_grp_EX_vs_MPTP_tissue-Stria_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13470 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 15 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_DNA_REPAIR | NES=2.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=1.99 | NOM p=0.00e+00 | FDR q=1.69e-03 - HALLMARK_UV_RESPONSE_UP | NES=1.90 | NOM p=0.00e+00 | FDR q=4.51e-03 - HALLMARK_ADIPOGENESIS | NES=1.86 | NOM p=0.00e+00 | FDR q=5.26e-03 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.76 | NOM p=0.00e+00 | FDR q=9.02e-03 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.58 | NOM p=2.27e-02 | FDR q=3.81e-02 - HALLMARK_MTORC1_SIGNALING | NES=1.48 | NOM p=5.35e-03 | FDR q=6.12e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.29 | NOM p=7.82e-02 | FDR q=2.28e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MITOTIC_SPINDLE | NES=-2.22 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONS ... [450 more characters]

reasoning: Paper reports GO/KEGG pathways (DAVID) for exercise-affected genes in SN and striatum (S3.3.p1).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper reports reversal-set sizes (SN 155 down/66 up, striatum 49 down/185 up after exercise), not per-contrast DEG totals; these are compared from a post-hoc overlap of our MPTP vs SAL and EX vs MPTP tables (reversal_sets.csv), not by the runner.", "Exercise effect is estimated only within MPTP-lesioned mice (no healthy exercise arm).", "n=4 per group; raw p<0.05 without multiplicity control yields many expected false positives (~5% of tested genes).", "Sample-to-GSM mapping not established non-positionally; group labels decoded from matrix column names."], "results": {"limma_Cereb/grp_EX_vs_MPTP_tissue-Cereb": {"n_deg": 737, "up": 434, "down": 303, "rule": "pvalue < 0.05", "audit_n": 2}, "limma_Cereb/grp_MPTP_vs_SAL_tissue-Cereb": {"n_deg": 1469, "up": 743, "down": 726, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_Cereb/grp_EX_vs_SAL_tissue-Cereb": {"n_deg": 2085, "up": 1208, "down": 877, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_Cortex/grp_EX_vs_MPTP_tissue-Cortex": {"n_deg": 773, "up": 421, "down": 352, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_Cortex/grp_MPTP_vs_SAL_tissue-Cortex": {"n_deg": 2586, "up": 1235, "down": 1351, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_Cortex/grp_EX_vs_SAL_tissue-Cortex": {"n_deg": 2154, "up": 1040, "down": 1114, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_Nigra/grp_EX_vs_MPTP_tissue-Nigra": {"n_deg": 1015, "up": 490, "down": 525, "rule": "pvalue < 0.05", "audit_n": 0}, "limma_Ni ... [1400 more characters]

reasoning: Paper's DESeq route blocked (FPKM only); limma deviation runs with the paper threshold.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 48 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "quantification",
    "paper": "Tophat2 + Cufflinks FPKM / RSEM (S2.7.p1)",
    "data": "GEO data_processing: hisat2 + HTSeq counts on mm9; deposited file is FPKM",
    "disposition": "executable_without_change"
  },
  {
    "item": "DE method",
    "paper": "DESeq v1.14 (S2.7.p1)",
    "data": "no counts deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "sample IDs",
    "paper": "n=4 per group",
    "data": "matrix uses animal IDs (E26-29, M6/16/21/23, S1-4); GEO uses rep1-4; no explicit link",
    "disposition": "executable_without_change"
  },
  {
    "item": "reported counts",
    "paper": "only reversal-set sizes in the text",
    "data": "per-contrast tables produced",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 35813950 / GSE205907

Exercise in MPTP-induced Parkinson's disease mice. Bulk RNA-seq of 4 brain regions (cerebellum, cortex, SN, striatum), 3 groups (Saline, MPTP, MPTP+EX), n = 4 female mice per group. 48 samples in total.

## What ran
- Route: case spec (`case_spec.json`), then `python -m tools.case_runner execute`. Status `completed`. The validator checked 18 records and found 0 errors.
- Prep (`prep_GSE205907.py`, run with `-I`):
  - Dropped 27 gene IDs that Excel had turned into dates (`2019-03-xx` for Marchf genes, `2019-09-xx` for Septin genes; 2 of them duplicated).
  - Built a sample sheet from the matrix column names: prefix `E`/`M`/`S` gives the group, the suffix gives the region, and the number gives the animal.
  - The sheet's group x region table equals the GEO treatment x tissue table (4 per cell).
- Why a derived sample sheet: the matrix columns use animal IDs (E26–E29, M6/M16/M21/M23, S1–S4), while GEO titles use `rep1..rep4`. Nothing links the two except column order, and positional alignment is not allowed. The labels are backed by marker genes:
  - Region markers match (Pcp2/Gabra6, Satb2/Neurod6, Th/Slc6a3, Ppp1r1b/Penk).
  - Nigral Th/Slc6a3 is 4–7x lower in E and M animals than in S animals, which fits the MPTP lesion.
  - All samples are female (Xist present, no Y-linked genes).
- Matrix: FPKM (non-integer values, column sums 345k–621k, file named fpkm, paper says FPKM). Transformed with log2(x+1).
- Design: one limma model per region (stratum = tissue), `~ 0 + grp`, no blocking. Each animal contributes only one sample per region.
  - Primary contrast: EX vs MPTP, the effect of exercise within PD mice.
  - Secondary: MPTP vs SAL, the PD-model effect.
  - Exploratory: EX vs SAL.
- Expression filter: the paper's "FPKM > 1", applied as FPKM >= 1 in at least 4 of the 12 samples of each region.
- Threshold: the paper's rule, raw p < 0.05 with no fold-change cutoff (S2.7.p1, FIG3 legend). Source is `paper_on_deviation_route`. Audit rule: BH FDR < 0.05.
- Sensitivity run `limma_Stria_noE29`: striatum refit without E29Stria, a clear outlier (mean correlation 0.83 vs 0.97 for every other striatum sample, FPKM sum 621k, low Xist).
- Enrichment (ORA on GO/KEGG, GSEA on Hallmark) ran for EX vs MPTP in SN and striatum, and completed.
- Post-hoc reversal sets (`reversal_sets.py` -> `reversal_sets_summary.csv`, `reversal_sets.csv`, `reversal_sets_noE29.txt`): genes with p < 0.05 in both MPTP vs SAL and EX vs MPTP, with opposite d ... [3588 more characters]
