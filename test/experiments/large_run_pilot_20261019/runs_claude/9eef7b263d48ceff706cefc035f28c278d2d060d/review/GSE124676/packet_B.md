# Review packet B (the analysis' decisions): GSE124676

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| time_after_vs_before | 1873 | 1984 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 1984 | 53 | 14 | 584 | 0.078 | 0.093 |

## Samples per design level

### `time`
- **after** (21): GSM3539273 / a9f_after / q2_0; GSM3539274 / a30f_after / q2_1; GSM3539275 / a23f_after / q2_2; GSM3539276 / a7f_after / q2_3; GSM3539277 / a19f_after / q2_4; GSM3539278 / a35f_after / q2_5; GSM3539279 / a6f_after / q2_6; GSM3539280 / a2f_after / q2_7; GSM3539281 / a8f_after / q2_8; GSM3539282 / a28f_after / q2_9; GSM3539283 / a22f_after / q2_10; GSM3539284 / a4f_after / q2_11; GSM3539285 / a3f_after / q2_12; GSM3539286 / a14f_after / q2_13; GSM3539287 / a38f_after / q2_14; GSM3539288 / a27f_after / q2_15; GSM3539289 / a21f_after / q2_16; GSM3539290 / a33f_after / q2_17; GSM3539291 / a5f_after / q2_18; GSM3539292 / a37f_after / q2_19; GSM3539293 / a29f_after / q2_20
- **before** (21): GSM3539252 / a19_before / q1_0; GSM3539253 / a28_before / q1_1; GSM3539254 / a8_before / q1_2; GSM3539255 / a21_before / q1_3; GSM3539256 / a38_before / q1_4; GSM3539257 / a6_before / q1_5; GSM3539258 / a30_before / q1_6; GSM3539259 / a37_before / q1_7; GSM3539260 / a9_before / q1_8; GSM3539261 / a4_before / q1_9; GSM3539262 / a7_before / q1_10; GSM3539263 / a2_before / q1_11; GSM3539264 / a27_before / q1_12; GSM3539265 / a5_before / q1_13; GSM3539266 / a23_before / q1_14; GSM3539267 / a35_before / q1_15; GSM3539268 / a33_before / q1_16; GSM3539269 / a29_before / q1_17; GSM3539270 / a14_before / q1_18; GSM3539271 / a3_before / q1_19; GSM3539272 / a22_before / q1_20

### `subject`
- **a14** (2): GSM3539270 / a14_before / q1_18; GSM3539286 / a14f_after / q2_13
- **a19** (2): GSM3539252 / a19_before / q1_0; GSM3539277 / a19f_after / q2_4
- **a2** (2): GSM3539263 / a2_before / q1_11; GSM3539280 / a2f_after / q2_7
- **a21** (2): GSM3539255 / a21_before / q1_3; GSM3539289 / a21f_after / q2_16
- **a22** (2): GSM3539272 / a22_before / q1_20; GSM3539283 / a22f_after / q2_10
- **a23** (2): GSM3539266 / a23_before / q1_14; GSM3539275 / a23f_after / q2_2
- **a27** (2): GSM3539264 / a27_before / q1_12; GSM3539288 / a27f_after / q2_15
- **a28** (2): GSM3539253 / a28_before / q1_1; GSM3539282 / a28f_after / q2_9
- **a29** (2): GSM3539269 / a29_before / q1_17; GSM3539293 / a29f_after / q2_20
- **a3** (2): GSM3539271 / a3_before / q1_19; GSM3539285 / a3f_after / q2_12
- **a30** (2): GSM3539258 / a30_before / q1_6; GSM3539274 / a30f_after / q2_1
- **a33** (2): GSM3539268 / a33_before / q1_16; GSM3539290 / a33f_after / q2_17
- **a35** (2): GSM3539267 / a35_before / q1_15; GSM3539278 / a35f_after / q2_5
- **a37** (2): GSM3539259 / a37_before / q1_7; GSM3539292 / a37f_after / q2_19
- **a38** (2): GSM3539256 / a38_before / q1_4; GSM3539287 / a38f_after / q2_14
- **a4** (2): GSM3539261 / a4_before / q1_9; GSM3539284 / a4f_after / q2_11
- **a5** (2): GSM3539265 / a5_before / q1_13; GSM3539291 / a5f_after / q2_18
- **a6** (2): GSM3539257 / a6_before / q1_5; GSM3539279 / a6f_after / q2_6
- **a7** (2): GSM3539262 / a7_before / q1_10; GSM3539276 / a7f_after / q2_3
- **a8** (2): GSM3539254 / a8_before / q1_2; GSM3539281 / a8f_after / q2_8
- **a9** (2): GSM3539260 / a9_before / q1_8; GSM3539273 / a9f_after / q2_0

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE124676"], "assay": "Ion Proton total RNA-seq (globin-depleted) of blood leukocytes; Tophat2/bowtie2 to hg19; Cuffquant + Cuffnorm normalized FPKM (S2.3.p1, S2.4.p1)", "sample_inclusion": "Group 1 only: 21 PD patients (10 tai chi, 11 MET), each sampled before and 48-72 h after a 12-week exercise program = 42 RNA-seq samples (S3.1.p1, S3.3.p1). Group 2 (19 patients) is qPCR/immunoassay validation only, not in GEO.", "factors": {"time": ["before", "after"], "exercise_type": ["Tai chi", "MET"], "subject": "21 patients"}, "primary_estimand": "Within-patient change in leukocyte gene expression after 12 weeks of exercise (after vs before), tai chi and MET pooled (S3.3.p1: exercise type gave no transcriptomic difference, so groups combined)", "planned_contrasts": ["time after vs before, paired by patient, both exercise types pooled (S2.4.p1, S3.3.p1; paper: 1,873 DEGs, 417 higher after, 1,453 higher before)"], "repeated_measure_unit": "patient (before/after pair)", "normalization": "Cuffnorm normalized FPKM", "paper_method": "paired Student t-test on Cuffnorm FPKM, before vs after (S2.4.p1); scale of the tested values (linear or log) not stated", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.4.p1"}, "paper_results": "1,873 DEGs (S3.3.p1; 1,453 + 417 = 1,870, internal mismatch of 3). Down after: ODC1 (most down), CD3E, GRAP2, FOS, ZAP70, IL2RA/B, TNFRSF18, RTP5, CCL5, CD28; up after: TRAF ... [117 more characters]

reasoning: Methods S2.4.p1 define a paired t-test before vs after exercise with raw P < 0.05 and no fold-change cutoff; S3.3.p1 pools tai chi and MET. No sedentary control arm exists: the estimand is a within-subject pre/post change in PD patients.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE124676\\GSE124676_genes.fpkm_table.txt.gz", "owned": true, "checks": ["S6.p1 names GSE124676", "42 samples = 21 patients x before/after (S3.3.p1)", "metadata exercise counts at baseline 11 MET / 10 tai chi match S3.1.p1", "data_processing matches S2.4.p1 (Cuffquant [-b,-u] + Cuffnorm FPKM, RefGene 2015 Feb, hg19)"], "accession": "GSE124676", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE124676\\GSE124676_metadata.csv"}

reasoning: Accession, sample count, arm sizes and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 42, "n_metadata": 42, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\aligned\\aligned_metadata.csv", "columns": {"time": {"alias_of": "characteristics_ch1.2.time"}, "extype": {"alias_of": "characteristics_ch1.1.exercise"}, "subject": {"source": "title", "regex": "^(a\\d+)f?_(?:before|after)$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\aligned\\design_metadata.csv", "sha256": "7fe28b05d1b012a5a0cbf5039ce74f294571077ee0df011d4bd403ea45eeaccd", "levels": {"time": {"before": 21, "after": 21}, "extype": {"MET": 21, "Tai chi": 21}, "subject": {"a19": 2, "a28": 2, "a8": 2, "a21": 2, "a38": 2, "a6": 2, "a30": 2, "a37": 2, "a9": 2, "a4": 2, "a7": 2, "a2": 2, "a27": 2, "a5": 2, "a23": 2, "a35": 2, "a33": 2, "a29": 2, "a14": 2, "a3": 2, "a22": 2}}}}

reasoning: Matrix columns q1_*/q2_* equal metadata 'description' exactly (42/42, inspect alignment_keys). Subject = patient code in title (a19_before / a19f_after); 'f' suffix marks follow-up. time copied from characteristics time. extype kept as annotation only (subject a22 is labelled MET before but Tai chi after, a metadata inconsistency).

### matrix (valid, not_started)

final: {"source": "GSE124676_genes.fpkm_table.txt.gz; data_processing: Cuffnorm normalized FPKM", "paper_input": "Cuffnorm FPKM (S2.4.p1)", "matrix_type": "FPKM", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\aligned\\aligned_matrix.csv", "sha256": "9a4ad92ed2ca8fc0fa22961c9478233bee31ab2f68767db6d9da90588e45c5cc", "n_features": 26111, "n_samples": 42, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 84329.4, "median": 0.25298750000000003, "integer_fraction": 0.4047, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name, data_processing and paper all say normalized FPKM; values non-integer (integer fraction 0.40 driven by zeros), max 84,329 = linear scale. Not counts, so count methods are invalid.

### design (valid, not_started)

final: {"analysis_type": "paired two-group (repeated measures)", "design_column": "time", "control": "before", "treatment": "after", "contrasts": [{"name": "time_after_vs_before", "control": "before", "treatment": "after", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Paper's estimand is the paired pre/post change pooling both exercise modes (S3.3.p1). Exercise type is not a factor of the paper's DE analysis; tai chi vs MET is a between-subject comparison the paper reports as non-different and does not test for DEGs.

rejected alternatives: [{"value": "extype (MET vs Tai chi) as factor", "reason_rejected": "Not the paper's estimand; paper pooled the modes (S3.3.p1); a22 has conflicting labels across time points."}, {"value": "time within each exercise type separately", "reason_rejected": "Paper did not do it; would require resolving a22's conflicting label; ~10-11 pairs per arm."}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "extype", "disposition": "not_included: constant within subject (except a22 label error), absorbed by subject block; paper pooled modes"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 42, "n_columns": 22, "columns": ["Intercept", "time_before", "subject_a19", "subject_a2", "subject_a21", "subject_a22", "subject_a23", "subject_a27", "subject_a28", "subject_a29", "subject_a3", "subject_a30", "subject_a33", "subject_a35", "subject_a37", "subject_a38", "subject_a4", "subject_a5", "subject_a6", "subject_a7", "subject_a8", "subject_a9"], "rank": 22, "full_rank": true, "residual_df": 20, "levels": {"time": {"before": 21, "after": 21}, "subject": {"a19": 2, "a28": 2, "a8": 2, "a21": 2, "a38": 2, "a6": 2, "a30": 2, "a37": 2, "a9": 2, "a4": 2, "a7": 2, "a2": 2, "a27": 2, "a5": 2, "a23": 2, "a35": 2, "a33": 2, "a29": 2, "a14": 2, "a3": 2, "a22": 2}}, "cells": [{"cell": ["after", "a14"], "n": 1}, {"cell": ["after", "a19"], "n": 1}, {"cell": ["after", "a2"], "n": 1}, {"cell": ["after", "a21"], "n": 1}, {"cell": ["after", "a22"], "n": 1}, {"cell": ["after", "a23"], "n": 1}, {"cell": ["after", "a27"], "n": 1}, {"cell": ["after", "a28"], "n": 1}, {"cell": ["after", "a29"], "n": 1}, {"cell": ["after", "a3"], "n": 1}, {"cell": ["after", "a30"], "n": 1}, {"cell": ["after", "a33"], "n": 1}, {"cell": ["after", "a35"], "n": 1}, {"cell": ["after", "a37"], "n": 1}, {"cell": ["after", "a38" ... [1198 more characters]

reasoning: Each patient contributes one before and one after sample; paper used a paired test to remove individual differences (S2.4.p1). Subject enters the model as a blocking factor.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (moderated t, ~ C(subject) + time) on log2(FPKM+1)", "formula": "~ C(subject) + Treatment", "paper_route": {"method": "paired Student t-test on Cuffnorm FPKM", "status": "blocked", "reason": "No validated paired-t executor in the repository and the paper does not state whether FPKM was log-transformed; a hand-written t-test is not allowed. limma with a subject block is the validated paired equivalent (adds variance moderation)."}, "deviations": ["limma moderated paired t (subject block) instead of ordinary paired t-test", "log2(FPKM+1) scale (paper scale unstated)", "no expression filter (paper states none)"], "transform": "log2(x+1)"}

reasoning: FPKM -> log2(x+1) -> limma is the policy route; subject as a block reproduces the pairing.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper's raw P < 0.05, no fold change, applied to the limma paired route; BH FDR < 0.05 reported as audit."}

reasoning: S2.4.p1: 'Significantly differentially expressed genes (DEGs, P < 0.05)'; no multiple-testing correction or FC cutoff stated.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "time_after_vs_before", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 42, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\time_after_vs_before\\DEG_results_after_vs_before.csv"], "counts": {"time_after_vs_before": {"applied": {"rule": "pvalue < 0.05", "n_tested": 21248, "n_significant": 1984, "n_up": 529, "n_down": 1455, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 21248, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paired after vs before, subject block, log2(FPKM+1).

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_after_vs_before", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\ora_up\\DEG_results_after_vs_before_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\ora_up\\DEG_results_after_vs_before_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\ora_up\\DEG_results_after_vs_before_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\ora_up\\DEG_results_after_vs_before_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 529 Human genes (direction=up, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjus ... [1348 more characters]

reasoning: Paper ran KEGG/GO (DAVID) on up- and down-regulated DEGs separately (S3.4.p1, S3.4.p3).

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_after_vs_before", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\ora_down\\DEG_results_after_vs_before_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\ora_down\\DEG_results_after_vs_before_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\ora_down\\DEG_results_after_vs_before_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\ora_down\\DEG_results_after_vs_before_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 1455 Human genes (direction=down, pvalue<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (so ... [1358 more characters]

reasoning: Down-regulated ORA (paper: TCR signaling down) plus Hallmark GSEA on the full ranking.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_after_vs_before", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\9eef7b263d48ceff706cefc035f28c278d2d060d\\GSE124676\\results\\enrichment_time_after_vs_before\\gsea\\DEG_results_after_vs_before_GSEA_Hallmark.csv"], "summary": "GSEA complete on 21248 Human genes ranked by 'stat'. 50 Hallmark sets tested, 29 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.31 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.07 | NOM p=0.00e+00 | FDR q=1.01e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.96 | NOM p=0.00e+00 | FDR q=1.34e-03 - HALLMARK_NOTCH_SIGNALING | NES=1.69 | NOM p=1.64e-02 | FDR q=1.11e-02 - HALLMARK_PROTEIN_SECRETION | NES=1.63 | NOM p=0.00e+00 | FDR q=1.29e-02 - HALLMARK_MITOTIC_SPINDLE | NES=1.48 | NOM p=0.00e+00 | FDR q=2.95e-02 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.45 | NOM p=0.00e+00 | FDR q=3.31e-02 - HALLMARK_HEME_METABOLISM | NES=1.45 | NOM p=0.00e+00 | FDR q=3.09e-02 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.32 | NOM p=6.32e-02 | FDR q=7.71e-02 - HALLMARK_PI3K_AKT_MTOR_SIGNALING | NES=1.31 | NOM p=2.70e-02 | FDR q=7.57e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC ... [428 more characters]

reasoning: Down-regulated ORA (paper: TCR signaling down) plus Hallmark GSEA on the full ranking.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Pre/post design without a non-exercise control: changes include season, time and medication drift (paper S4.p7 notes climate).", "Raw P < 0.05 threshold without multiple-testing correction, as in the paper.", "Subject a22 exercise label differs between before (MET) and after (Tai chi) samples in GEO; irrelevant to the pooled contrast."], "results": {"time_after_vs_before": {"n_deg": 1984, "up": 529, "down": 1455, "rule": "pvalue < 0.05", "audit_n": 0}}, "paper_counts": {"time_after_vs_before": 1873}, "comparison": {"time_after_vs_before": {"ours": 1984, "paper": 1873}}, "paper_gene_check": {"time_after_vs_before": {"ODC1": {"AveExpr": 3.1637, "log2FoldChange": -0.391, "padj": 0.1524, "pvalue": 0.0}, "CD3E": {"AveExpr": 5.2295, "log2FoldChange": -0.7554, "padj": 0.1524, "pvalue": 0.0002}, "GRAP2": {"AveExpr": 2.1226, "log2FoldChange": -0.5429, "padj": 0.216, "pvalue": 0.0009}, "FOS": {"AveExpr": 8.6575, "log2FoldChange": -1.421, "padj": 0.216, "pvalue": 0.001}, "ZAP70": {"AveExpr": 5.5647, "log2FoldChange": -0.5723, "padj": 0.3111, "pvalue": 0.0041}, "IL2RA": {"AveExpr": 0.6009, "log2FoldChange": -0.1809, "padj": 0.4073, "pvalue": 0.0155}, "IL2RB": {"AveExpr": 4.0524, "log2FoldChange": -0.4282, "padj": 0.5181, "pvalue": 0.0448}, "TNFRSF18": {"AveExpr": 1.3196, "log2FoldChange": -0.6055, "padj": 0.1619, "pvalue": 0.0003}, "RTP5": {"AveExpr": 0.5175, "log2FoldChange": -0.3966, "padj": 0.1907, "pvalue": 0.0005}, "CCL5": {"AveExpr": 6.6 ... [422 more characters]

reasoning: Paper direction: ODC1, CD3E, GRAP2, FOS, ZAP70, IL2RA/B, TNFRSF18, RTP5, CCL5, CD28 down after; TRAF3, TNF, AGAP2 up after.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 42 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise label of subject a22",
    "paper": "arm fixed per randomized patient (S2.1.p2)",
    "data": "a22_before = MET, a22f_after = Tai chi",
    "disposition": "executable_without_change"
  },
  {
    "item": "DEG direction totals",
    "paper": "1,873 DEGs but 1,453 + 417 = 1,870 (S3.3.p1)",
    "data": "n/a",
    "disposition": "executable_without_change"
  },
  {
    "item": "test",
    "paper": "ordinary paired t-test on FPKM (scale unstated)",
    "data": "FPKM deposited",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE124676 / PMC6997272 (exercise in Parkinson's disease leukocytes)

## What ran
- Case spec route (`tools.case_runner execute case_spec.json`); validator: 13 records, 0 errors. Status: completed, route `declared_deviation`.
- Data: `GSE124676_genes.fpkm_table.txt.gz` (Cuffnorm FPKM, 26,111 genes x 42 samples); matrix columns aligned exactly to metadata `description` (42/42).
- Design: 21 PD patients, before vs after 12 weeks of exercise. Tai chi and MET pooled as in the paper (S3.3.p1). Subject (patient code from title, e.g. a19 / a19f) is a blocking factor.
- Method: log2(FPKM+1), then limma `~ C(subject) + Treatment` (moderated paired test). limma removed 4,863 zero-variance (all-constant) genes, leaving 21,248 tested.
- Threshold: the paper's rule, raw P < 0.05 with no fold-change cutoff (S2.4.p1), source `paper_on_deviation_route`. BH FDR < 0.05 is recorded as the audit threshold.
- Enrichment: Enrichr ORA (GO BP/MF/CC, KEGG 2021) separately for up and down DEGs, plus Hallmark GSEA on the limma t ranking.

## DEG counts vs paper (raw P < 0.05, no FC)
| Contrast | Ours | Paper |
|---|---|---|
| after vs before (all) | 1,984 | 1,873 |
| higher after (up) | 529 | 417 |
| higher before (down) | 1,455 | 1,453 |

- Audit rule (BH FDR < 0.05): 0 genes; the minimum padj is 0.14. The paper's DEG list rests on uncorrected P values.
- All 14 named genes change in the paper's direction. Down after exercise: ODC1 (our 3rd-smallest P), CD3E, GRAP2, FOS, ZAP70, IL2RA, IL2RB, TNFRSF18, RTP5, CCL5, CD28. Up after: TRAF3, TNF, AGAP2.
- 13 of the 14 genes pass P < 0.05. AGAP2 does not (P = 0.065), although the paper calls it significantly upregulated.
- KEGG ORA reproduces the paper's headline pathways. Down DEGs: T cell receptor signaling pathway is top (adj P 3.8e-4), then primary immunodeficiency (adj P 0.044). Up DEGs: osteoclast differentiation is top (adj P 2.6e-7). Paper S3.4.p1 reports the same.
- Hallmark GSEA (exploratory, not in the paper): interferon alpha/gamma, IL6-JAK-STAT3 and inflammatory response are shifted up after exercise.

## Deviations
- The paper used an ordinary paired Student t-test on FPKM and did not state the scale. We ran a limma moderated paired test on log2(FPKM+1). There is no paired-t executor, and a hand-written test is not allowed. The paper route is recorded as blocked.
- No expression filter was applied, because the paper states none. limma's own drop of zero-variance genes is the only filtering.
- The paper's numbers d ... [638 more characters]
