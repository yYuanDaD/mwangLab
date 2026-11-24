# Review packet B (the analysis' decisions): GSE211204

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.1.subject", "n_values": 11, "max_repeat": 3, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Samples per design level

### `time`
- **AR** (9): GSM6456105 / Subj_1 AR [S23]; GSM6456106 / Subj_2 AR [S24]; GSM6456107 / Subj_3 AR [S25]; GSM6456108 / Subj_6 AR [S26]; GSM6456109 / Subj_7 AR [S27]; GSM6456110 / Subj_8 AR [S28]; GSM6456111 / Subj_9 AR [S29]; GSM6456112 / Subj_10 AR [S30]; GSM6456113 / Subj_11 AR [S31]
- **BL** (11): GSM6456083 / Subj_1 baseline [S1]; GSM6456084 / Subj_2 baseline [S2]; GSM6456085 / Subj_3 baseline [S3]; GSM6456086 / Subj_4 baseline [S4]; GSM6456087 / Subj_5 baseline [S5]; GSM6456088 / Subj_6 baseline [S6]; GSM6456089 / Subj_7 baseline [S7]; GSM6456090 / Subj_8 baseline [S8]; GSM6456091 / Subj_9 baseline [S9]; GSM6456092 / Subj_10 baseline [S10]; GSM6456093 / Subj_11 baseline [S11]
- **ULLS** (11): GSM6456094 / Subj_1 ULLS [S12]; GSM6456095 / Subj_2 ULLS [S13]; GSM6456096 / Subj_3 ULLS [S14]; GSM6456097 / Subj_4 ULLS [S15]; GSM6456098 / Subj_5 ULLS [S16]; GSM6456099 / Subj_6 ULLS [S17]; GSM6456100 / Subj_7 ULLS [S18]; GSM6456101 / Subj_8 ULLS [S19]; GSM6456102 / Subj_9 ULLS [S20]; GSM6456103 / Subj_10 ULLS [S21]; GSM6456104 / Subj_11 ULLS [S22]

### `subject`
- **Subj_1** (3): GSM6456083 / Subj_1 baseline [S1]; GSM6456094 / Subj_1 ULLS [S12]; GSM6456105 / Subj_1 AR [S23]
- **Subj_10** (3): GSM6456092 / Subj_10 baseline [S10]; GSM6456103 / Subj_10 ULLS [S21]; GSM6456112 / Subj_10 AR [S30]
- **Subj_11** (3): GSM6456093 / Subj_11 baseline [S11]; GSM6456104 / Subj_11 ULLS [S22]; GSM6456113 / Subj_11 AR [S31]
- **Subj_2** (3): GSM6456084 / Subj_2 baseline [S2]; GSM6456095 / Subj_2 ULLS [S13]; GSM6456106 / Subj_2 AR [S24]
- **Subj_3** (3): GSM6456085 / Subj_3 baseline [S3]; GSM6456096 / Subj_3 ULLS [S14]; GSM6456107 / Subj_3 AR [S25]
- **Subj_4** (2): GSM6456086 / Subj_4 baseline [S4]; GSM6456097 / Subj_4 ULLS [S15]
- **Subj_5** (2): GSM6456087 / Subj_5 baseline [S5]; GSM6456098 / Subj_5 ULLS [S16]
- **Subj_6** (3): GSM6456088 / Subj_6 baseline [S6]; GSM6456099 / Subj_6 ULLS [S17]; GSM6456108 / Subj_6 AR [S26]
- **Subj_7** (3): GSM6456089 / Subj_7 baseline [S7]; GSM6456100 / Subj_7 ULLS [S18]; GSM6456109 / Subj_7 AR [S27]
- **Subj_8** (3): GSM6456090 / Subj_8 baseline [S8]; GSM6456101 / Subj_8 ULLS [S19]; GSM6456110 / Subj_8 AR [S28]
- **Subj_9** (3): GSM6456091 / Subj_9 baseline [S9]; GSM6456102 / Subj_9 ULLS [S20]; GSM6456111 / Subj_9 AR [S29]

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE211204"], "primary_estimand": "Within-subject change in vastus lateralis gene expression across three time points in young healthy men: LS0 (baseline) -> LS10 (10 d unilateral lower-limb suspension, unloading) -> AR21 (21 d resistance-exercise active recovery). The exercise effect is AR21 vs LS10 (21 d of resistance training after unloading); LS10 vs LS0 is the unloading (inactivity) effect; AR21 vs LS0 tests return to baseline.", "planned_contrasts": ["LS10 vs LS0 (S3.3.p1, Fig 4B; paper: 95 of 290 NMJ genes at q<0.05)", "AR21 vs LS10 (S3.3.p1, Fig 4C; paper: 114 of 290 NMJ genes at q<0.05) - exercise contrast", "AR21 vs LS0 (S3.3.p1, Fig 4D; paper: 24 of 290 NMJ genes at q<0.05)"], "factors": {"time": ["LS0 (baseline)", "LS10 (ULLS)", "AR21 (AR)"]}, "repeated_measure_unit": "participant (paired analysis adjusted for subject ID, S2.7.3.p1)", "inclusion": "12 recruited; 1 dropped after baseline, 2 declined the AR21 biopsy (S3.p1) -> GEO has 11 subjects, 31 samples (11 baseline, 11 ULLS, 9 AR)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.3.p1"}, "paper_method": "RSEM counts -> edgeR filterByExpr (20,555 genes) -> voom with quantile normalization -> limma eBayes, adjusted for subject ID (paired) (S2.7.3.p1); DEG counts and volcanoes reported only for a pre-selected set of 290 NMJ genes (12 MSigDB v7.4 pathways, Data S1) and 33 ion-channel genes (S2.9.p1)", "paper_results": "NMJ gen ... [165 more characters]

reasoning: Methods S2.3-S2.4 (ULLS, then 21-d resistance-exercise AR: leg press + leg extension 3x10 at 70% 1RM, 3x/week), S2.7.3.p1 (RNA-seq pipeline, limma-voom paired by subject), S2.9.p1 (DE reported within 290 NMJ + 33 ion-channel gene sets), S3.3.p1 (counts per pairwise contrast, q<0.05). DA.p1 names GSE211204.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\prep\\GSE211204_RSEM_counts_symbol.csv", "owned": true, "checks": ["DA.p1 cites GSE211204", "GEO: vastus lateralis, Homo sapiens, 31 samples; 11 subjects x baseline/ULLS/AR matches S3.p1 drop-outs (9 AR biopsies)", "data_processing matches S2.7.3.p1 (Cutadapt, STAR 2.7.0f, RSEM 1.3.0, GENCODE v21)"], "accession": "GSE211204", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE211204\\GSE211204_metadata.csv"}

reasoning: Accession, tissue, time points, sample count and processing chain all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 31, "n_metadata": 31, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\aligned\\aligned_metadata.csv", "columns": {"subject": {"alias_of": "characteristics_ch1.1.subject"}, "time_raw": {"alias_of": "characteristics_ch1.2.treatment", "recode": {"baseline": "BL", "ULLS": "ULLS", "AR": "AR"}}, "time": {"combine": ["time_raw"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\aligned\\design_metadata.csv", "sha256": "e680ab4c137b7820d24e0f02c5c496da94116e6d9a970b68d6d1a61dd6a7304e", "levels": {"subject": {"Subj_1": 3, "Subj_2": 3, "Subj_3": 3, "Subj_6": 3, "Subj_7": 3, "Subj_8": 3, "Subj_9": 3, "Subj_10": 3, "Subj_11": 3, "Subj_4": 2, "Subj_5": 2}, "time_raw": {"BL": 11, "ULLS": 11, "AR": 9}, "time": {"BL": 11, "ULLS": 11, "AR": 9}}}}

reasoning: Matrix columns S1..S31 appear in brackets in the GEO title ('Subj_1 baseline [S1]'); exact match on that extracted key. subject and treatment come from the characteristics fields; treatment recoded to BL/ULLS/AR.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "limma-voom", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\aligned\\aligned_matrix.csv", "sha256": "b03c38b0062c6fe781a8edeb3c7655131e0cedde717f312cd7d50a35ac9c893b", "n_features": 58381, "n_samples": 31, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 39420938.71, "median": 0.0, "integer_fraction": 0.8754, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: 'RSEM raw counts'; 87.5% integer values with fractional entries (RSEM expected counts), max 3.9e7, no negatives. Matches the paper's input (RSEM counts into edgeR/voom). Feature IDs 'ENSG|SYMBOL' re-keyed to symbols by prep_feature_ids.py (values unchanged).

### design (valid, not_started)

final: {"analysis_type": "repeated-measures three-level time course", "formula": "~ subject + time", "contrasts": [{"name": "time_ULLS_vs_BL", "control": "BL", "treatment": "ULLS", "role": "secondary"}, {"name": "time_AR_vs_ULLS", "control": "ULLS", "treatment": "AR", "role": "primary"}, {"name": "time_AR_vs_BL", "control": "BL", "treatment": "AR", "role": "secondary"}], "estimand_type": "within-subject change", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\suitability\\suitability.md", "n_comparisons": 4, "n_analyzable": 4}}

reasoning: One model with time (3 levels) and subject, the three pairwise contrasts the paper reports (Fig 4B-D). Exercise effect = AR vs ULLS. There is no non-exercising recovery arm, so AR vs ULLS cannot separate resistance training from spontaneous reloading after the suspension; recorded as a caveat.

rejected alternatives: [{"value": "pool ULLS and AR vs baseline", "reason_rejected": "paper compares the three time points pairwise; pooling mixes unloading and exercise"}, {"value": "unpaired comparison", "reason_rejected": "paper's analysis is paired on subject ID (S2.7.3.p1)"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "fixed-effect blocking term (paired analysis, S2.7.3.p1)"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 31, "n_columns": 13, "columns": ["Intercept", "time_BL", "time_ULLS", "subject_Subj_10", "subject_Subj_11", "subject_Subj_2", "subject_Subj_3", "subject_Subj_4", "subject_Subj_5", "subject_Subj_6", "subject_Subj_7", "subject_Subj_8", "subject_Subj_9"], "rank": 13, "full_rank": true, "residual_df": 18, "levels": {"time": {"BL": 11, "ULLS": 11, "AR": 9}, "subject": {"Subj_1": 3, "Subj_2": 3, "Subj_3": 3, "Subj_6": 3, "Subj_7": 3, "Subj_8": 3, "Subj_9": 3, "Subj_10": 3, "Subj_11": 3, "Subj_4": 2, "Subj_5": 2}}, "cells": [{"cell": ["AR", "Subj_1"], "n": 1}, {"cell": ["AR", "Subj_10"], "n": 1}, {"cell": ["AR", "Subj_11"], "n": 1}, {"cell": ["AR", "Subj_2"], "n": 1}, {"cell": ["AR", "Subj_3"], "n": 1}, {"cell": ["AR", "Subj_6"], "n": 1}, {"cell": ["AR", "Subj_7"], "n": 1}, {"cell": ["AR", "Subj_8"], "n": 1}, {"cell": ["AR", "Subj_9"], "n": 1}, {"cell": ["BL", "Subj_1"], "n": 1}, {"cell": ["BL", "Subj_10"], "n": 1}, {"cell": ["BL", "Subj_11"], "n": 1}, {"cell": ["BL", "Subj_2"], "n": 1}, {"cell": ["BL", "Subj_3"], "n": 1}, {"cell": ["BL", "Subj_4"], "n": 1}, {"cell": ["BL", "Subj_5"], "n": 1}, {"cell": ["BL", "Subj_6"], "n": 1}, {"cell": ["BL", "Subj_7"], "n": 1}, {"cell": ["BL", "Subj_8"], "n": 1}, {"cell": ["BL", "Subj_9"], "n": 1}, {"cell":  ... [4381 more characters]

reasoning: Repeated biopsies from the same 11 men; paper adjusts for subject ID. Subjects 4 and 5 lack AR and contribute only to BL/ULLS within-subject estimates. All samples are from one sequencing pool (2 lanes, GEO description), so no batch term.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "limma-voom (R limma/edgeR via tools.r_de_tools, engine voom)", "formula": "~ subject + time", "rounding_documented": true, "rounding_note": "No rounding: voom/edgeR take the fractional RSEM expected counts as-is (tools/r_de_tools.py:48,100 rounds only for deseq2/deseq1), as the paper did.", "paper_route": {"method": "edgeR filterByExpr + voom(normalize.method='quantile') + limma eBayes ~ subject + time", "status": "partially_reproduced", "reason": "executor's voom path applies calcNormFactors (TMM) and does not expose voom's quantile normalization"}, "deviations": ["TMM normalization instead of voom quantile normalization (executor limitation, tools/r_de.R:192,214)", "DE reported transcriptome-wide; the paper reports counts only inside its 290-gene NMJ set (gene list in Data S1, not available here)"]}

reasoning: Paper's own route is limma-voom on RSEM counts with filterByExpr and subject adjustment; the R voom executor reproduces it except for the normalization step.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "audit_threshold": {"metric": "padj", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "deviation_note": "Paper q<0.05 (also reports q<0.01, used here as the audit rule). Paper's q is reported within 290 NMJ genes; ours is BH over all filterByExpr-retained genes."}

reasoning: S3.3.p1: 'differentially regulated at q < 0.05 (70 genes at q < 0.01)'; no fold-change cutoff.

### execution (valid, completed)

final: {"method": "limma-voom (R), TMM, filterByExpr, ~ subject + time", "subset": "voom_paired", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 31, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\aligned\\aligned_matrix.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\results\\voom_paired\\DEG_results_time_ULLS_vs_BL.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\results\\voom_paired\\DEG_results_time_AR_vs_ULLS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\results\\voom_paired\\DEG_results_time_AR_vs_BL.csv"], "counts": {"voom_paired/time_ULLS_vs_BL": {"applied": {"rule": "padj < 0.05", "n_tested": 23336, "n_significant": 4559, "n_up": 2294, "n_down": 2265, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.01", "n_tested": 23336, "n_significant": 2370, "n_up": 1057, "n_down": 1313, "deg_sanity": "ok"}}, "voom_paired/time_AR_vs_ULLS": {"applied": {"rule": "padj < 0.05", "n_tested": 23336, "n_significant": 5400, "n_up": 2543, "n_down": 2857, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.01", "n_tested": 23336, "n_significant": 3088, "n_up": 1490, "n_down": 1598, "deg_sanity": "ok"}}, "voom_paired/time_AR_vs_BL": {"applied": {"rule": "padj < 0.05", "n_tested": 23336, "n_significant": 734, "n_up": 356, "n_down": 378, "deg_sanity": "ok"}, "audit": { ... [112 more characters]

reasoning: Paper's paired limma-voom: one model over all 31 samples, three pairwise time contrasts; AR vs ULLS is the exercise contrast.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "voom_paired/time_AR_vs_ULLS", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36071599\\GSE211204\\results\\enrichment_voom_paired_time_AR_vs_ULLS\\gsea\\DEG_results_time_AR_vs_ULLS_GSEA_Hallmark.csv"], "summary": "GSEA complete on 23336 Human genes ranked by 'stat'. 50 Hallmark sets tested, 37 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.57 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.68 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.35 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYOGENESIS | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=2.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.83 | NOM p=0.00e+00 | FDR q=1.21e-03 - HALLMARK_ANGIOGENESIS | NES=1.82 | NOM p=8.32e-03 | FDR q=1.41e-03 - HALLMARK_PEROXISOME | NES=1.81 | NOM p=0.00e+00 | FDR q=1.56e-03 - HALLMARK_COAGULATION | NES=1.76 | NOM p=0.00e+00 | FDR q=2.95e-03 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_PROTEIN_SECRETION | NES=-1.95 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=-1.71 | NOM p=0.00e+00 | ... [414 more characters]

reasoning: Paper ran GSEA (custom NMJ sets, not reproducible); Hallmark GSEA on the exercise contrast as exploratory pathway context.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper DEG counts (95/114/24) are within a 290-gene NMJ set whose list is not available; our transcriptome-wide counts are not directly comparable.", "AR vs ULLS confounds resistance training with natural reloading/recovery after suspension (no non-exercise recovery control).", "TMM instead of voom quantile normalization."], "results": {"voom_paired/time_ULLS_vs_BL": {"n_deg": 4559, "up": 2294, "down": 2265, "rule": "padj < 0.05", "audit_n": 2370}, "voom_paired/time_AR_vs_ULLS": {"n_deg": 5400, "up": 2543, "down": 2857, "rule": "padj < 0.05", "audit_n": 3088}, "voom_paired/time_AR_vs_BL": {"n_deg": 734, "up": 356, "down": 378, "rule": "padj < 0.05", "audit_n": 122}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"voom_paired/time_ULLS_vs_BL": {"COLQ": {"baseMean": 6.068, "AveExpr": 2.6012, "log2FoldChange": -2.1701, "padj": 5.71e-07, "pvalue": 3.43e-10}, "CHRNA1": {"baseMean": 8.9792, "AveExpr": 3.1666, "log2FoldChange": 2.3419, "padj": 4.3e-05, "pvalue": 3.78e-07}, "CHRND": {"baseMean": 24.2522, "AveExpr": 4.6, "log2FoldChange": 1.3338, "padj": 0.00664, "pvalue": 0.000576}, "GDNF": {"baseMean": 16.3795, "AveExpr": 4.0338, "log2FoldChange": 1.8062, "padj": 7.48e-05, "pvalue": 8.82e-07}, "NTF4": {"baseMean": 1.4722, "AveExpr": 0.5579, "log2FoldChange": -1.7129, "padj": 0.000204, "pvalue": 4.06e-06}}, "voom_paired/time_AR_vs_ULLS": {"COLQ": {"baseMean": 6.068, "AveExpr": 2.6012, "log2FoldChange": 1.7379, "padj": 4.07e-06, ... [606 more characters]

reasoning: Expected directions (S3.3.p2/Fig 5): COLQ down at LS10, up at AR21; CHRNA1/CHRND up at LS10, down at AR21.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 31 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "gene universe of reported DEG counts",
    "paper": "290 NMJ genes (Data S1)",
    "data": "full RSEM matrix, 58,381 genes; NMJ list not deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "normalization",
    "paper": "voom quantile normalization",
    "data": "executor offers TMM only",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID36071599 / GSE211204

## What ran
- Paper: Monti et al., 10-d unilateral lower-limb suspension (ULLS) then 21-d resistance-exercise active recovery (AR), vastus lateralis biopsies from young men at LS0 / LS10 / AR21.
- Data: `GSE211204_RawCountFile_RSEM_genes.txt.gz`, RSEM expected counts. Feature IDs were re-keyed from `ENSG|SYMBOL` to symbols by `prep_feature_ids.py`; values are unchanged, and 1,733 rows whose symbol appears more than once kept their Ensembl IDs. 31 samples (11 subjects: 11 BL, 11 ULLS, 9 AR) aligned 31/31 by exact match on the `[S#]` key in the GEO title.
- Design: one model, `~ subject + time`, on all samples. Subject is a fixed blocking term, matching the paper's "adjusted for subject ID (paired)". Three pairwise contrasts as in Fig 4B–D. **The exercise contrast is AR vs ULLS** (primary).
- Method: limma-voom in R (`tools.r_de_tools:run_r_de`, engine voom). edgeR `filterByExpr` kept 23,336 of the 40,611 non-zero genes (the paper kept 20,555), then TMM, voom, lmFit and eBayes. The R versions are edgeR 4.10.7 / limma 3.67.3; the paper used edgeR 3.32.1 / limma 3.46.0.
- Threshold: the paper's own rule, q (BH FDR) < 0.05 with no fold-change cutoff (S3.3.p1). The audit rule is q < 0.01, which the paper also reports.
- Enrichment (exploratory): Hallmark GSEA on AR vs ULLS. The top sets were up with training: OXPHOS (NES 3.57), fatty-acid metabolism, adipogenesis and myogenesis. The paper's custom NMJ GSEA could not be reproduced.

## DEG counts vs paper (q < 0.05; q < 0.01 in brackets)
| Contrast | Ours (transcriptome-wide) | Paper (within 290 NMJ genes only) |
|---|---|---|
| LS10 vs LS0 (unloading) | 4,559 (2,370) | 95 (70) |
| AR21 vs LS10 (exercise) | 5,400 (3,088) | 114 (81) |
| AR21 vs LS0 | 734 (122) | 24 (7) |

The counts cannot be compared directly. The paper reports DE only within a 290-gene NMJ set built from 12 MSigDB v7.4 pathways (list in Data S1, not available here). The pattern does match: large changes at LS10, reversed at AR21, and little difference between AR21 and LS0.

Named genes go in the paper's directions (S3.3.p2, Fig 5):
- **COLQ:** −2.17 at LS10, +1.74 at AR vs LS10.
- **CHRNA1:** +2.34 at LS10, −2.24 at AR vs LS10.
- **CHRND:** +1.33 at LS10, −2.35 at AR vs LS10.
- All three are significant in both contrasts and none in AR vs LS0.
- GDNF and NTF4 are DE with unloading (the paper gives no direction for them).

## Deviations
1. TMM normalization instead of the paper's voom quantile normalization. ... [1199 more characters]
