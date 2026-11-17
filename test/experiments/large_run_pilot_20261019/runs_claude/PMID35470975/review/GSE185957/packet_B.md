# Review packet B (the analysis' decisions): GSE185957

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.0.subject", "n_values": 8, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "characteristics_ch1.1.group", "n_values": 4, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lean_post_vs_pre | 551 | 554 | padj < 0.05 and |log2FoldChange| > 0.5 | 559 | 478 | 164 | 954 | 2265 | 608 | 174 | 1101 | 0.073 | 0.165 |
| obese_post_vs_pre | 104 | 0 | padj < 0.05 and |log2FoldChange| > 0.5 | 0 | 0 | 0 | 0 | 1120 | 222 | 46 | 332 | 0.092 | 0.083 |

## Samples per design level

### `time`
- **post** (8): GSM5627811 / subject1post; GSM5627812 / subject2post; GSM5627813 / subject3post; GSM5627814 / subject4post; GSM5627819 / subject5post; GSM5627820 / subject6post; GSM5627821 / subject7post; GSM5627822 / subject8post
- **pre** (8): GSM5627815 / subject1pre; GSM5627816 / subject2pre; GSM5627817 / subject3pre; GSM5627818 / subject4pre; GSM5627823 / subject5pre; GSM5627824 / subject6pre; GSM5627825 / subject7pre; GSM5627826 / subject8pre

### `subject`
- **subject1** (2): GSM5627811 / subject1post; GSM5627815 / subject1pre
- **subject2** (2): GSM5627812 / subject2post; GSM5627816 / subject2pre
- **subject3** (2): GSM5627813 / subject3post; GSM5627817 / subject3pre
- **subject4** (2): GSM5627814 / subject4post; GSM5627818 / subject4pre
- **subject5** (2): GSM5627819 / subject5post; GSM5627823 / subject5pre
- **subject6** (2): GSM5627820 / subject6post; GSM5627824 / subject6pre
- **subject7** (2): GSM5627821 / subject7post; GSM5627825 / subject7pre
- **subject8** (2): GSM5627822 / subject8post; GSM5627826 / subject8pre

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE185957"], "assay": "bulk RNA-seq (polyA, Illumina HiSeq 4000), human vastus lateralis biopsies (S2.4.p1)", "sample_inclusion": "4 lean + 4 obese adults, each biopsied at rest (pre) and 3.5 h after 30 min single-leg cycling at 70% VO2peak (post); 16 libraries (ABS.p2, S2.1.p1, S2.3.p1)", "factors": {"status": ["lean", "obese"], "time": ["pre", "post"]}, "repeated_measure_unit": "subject (pre and post biopsy from the same person; rest biopsy right leg, post biopsy exercised left leg, separate days) (S2.3.p1)", "primary_estimand": "Within-person transcriptional response to a single bout of endurance exercise (post vs pre), estimated separately in lean and in obese participants (S3.2.p1, FIG2)", "planned_contrasts": ["lean: post vs pre (S3.2.p1; paper: 419 up, 132 down = 551 DEGs)", "obese: post vs pre (S3.2.p1; paper: 82 up, 22 down = 104 DEGs)", "baseline obese vs lean pre (S3.1.p1; 97 up, 65 down) - not an exercise contrast, out of scope"], "paper_method": "edgeR negative-binomial GLM on featureCounts gene counts (S2.4.p1); design terms and subject blocking not stated", "paper_normalization": "edgeR (deposited file is edgeR-normalized CPM, GEO data_processing)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "source_locator": "S3.1.p1 (adjusted p < 0.05, log2(fold-change) > +/-0.5); FIG2/FIG7 report FDR / adjusted p = 0.05"}, "paper_results": {"lean_post_vs_pre": {"up": 419, "down": 132}, "obese ... [300 more characters]

reasoning: Paper-first reconstruction. The exercise estimand is the paired pre/post change within each BMI group (S3.2.p1, FIG2 volcano plots per group). The explicit DE threshold (adjusted p<0.05 and |log2FC|>0.5) is stated in S3.1.p1 for the baseline comparison and is the only stated threshold; FIG2 uses FDR on the y-axis, so the same rule is taken for the exercise contrasts (medium confidence). edgeR GLM on counts is the paper's method; whether subject was blocked is not stated.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE185957\\GSE185957_norm_cpm.txt.gz", "owned": true, "checks": ["S2.4.p1 names GSE185957", "GEO: Homo sapiens skeletal muscle, Mayo Clinic, STAR/hg38/featureCounts/edgeR matches S2.4.p1", "16 samples = 8 subjects x pre/post, groups leanpre/leanpost/obesepre/obesepost 4 each matches N=4+4 (ABS.p2)"], "accession": "GSE185957", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE185957\\GSE185957_metadata.csv"}

reasoning: Accession cited in the paper; processing description and sample structure match the paper's RNA-seq cohort.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 16, "n_metadata": 16, "coverage": 1.0, "unmatched_matrix_columns": ["Start", "End", "Length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\aligned\\aligned_metadata.csv", "columns": {"subject": {"alias_of": "characteristics_ch1.0.subject"}, "status": {"source": "characteristics_ch1.1.group", "regex": "^(lean|obese)(?:pre|post)$"}, "time": {"source": "characteristics_ch1.1.group", "regex": "^(?:lean|obese)(pre|post)$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\aligned\\design_metadata.csv", "sha256": "b9f37bb04815e8224ebc0daa28562f67b8c3c2a19c6d43117a0263ae0708802d", "levels": {"subject": {"subject1": 2, "subject2": 2, "subject3": 2, "subject4": 2, "subject5": 2, "subject6": 2, "subject7": 2, "subject8": 2}, "status": {"lean": 8, "obese": 8}, "time": {"post": 8, "pre": 8}}}}

reasoning: Matrix columns (subject5post, ...) equal the metadata title column exactly for 16/16 samples (inspect alignment_keys). status and time are parsed from the GEO group field; subject from the subject characteristic (each subject has exactly one pre and one post).

### matrix (valid, not_started)

final: {"matrix_type": "linear normalized CPM (edgeR-normalized counts per million)", "recommended_method": "limma on log2(CPM+1) with subject blocking", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\aligned\\aligned_matrix.csv", "sha256": "e3be79bdc3e9c756af21ad7309a51313b58f992edd5ee09e8433644e645eff62", "n_features": 64253, "n_samples": 16, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 45724.4252646432, "median": 0.0, "integer_fraction": 0.636, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File is GSE185957_norm_cpm.txt.gz; data_processing says 'Supplementary_files_format_and_content: norm_cpm.txt'. Values are non-integer (integer fraction 0.636 driven by zeros), column sums 0.84-1.12 million (CPM on TMM-adjusted library sizes). The paper's input (raw featureCounts counts for edgeR) was not deposited, and library sizes are not given, so counts cannot be recovered.

rejected alternatives: [{"value": "raw counts", "reason_rejected": "non-integer, column sums ~1e6: CPM, not counts"}]

### design (valid, not_started)

final: {"analysis_type": "paired two-timepoint, stratified by BMI group", "design_column": "time", "control": "pre", "treatment": "post", "contrasts": [{"name": "time_post_vs_pre_status-lean", "control": "pre", "treatment": "post", "role": "primary", "stratum": {"status": "lean"}}, {"name": "time_post_vs_pre_status-obese", "control": "pre", "treatment": "post", "role": "primary", "stratum": {"status": "obese"}}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: The paper reports exercise effects separately per BMI group (S3.2.p1, FIG2 A/B), so status is a stratum and time (post vs pre) is the factor, with subject as the repeated-measure key. n=4 pairs per group (small; paper calls itself preliminary, S5.p1). The baseline obese-vs-lean and obesity-by-exercise interaction are not exercise-effect contrasts asked for here and were not separately quantified as DEG counts for the interaction in the paper; they are left out. Suitability split_plan proposes a female-only exploratory comparison; within strata it is either identical to the lean analysis (all lean are female) or has 2 pairs (obese females), so it is not run.

rejected alternatives: [{"value": "pooled post vs pre across all 8 subjects", "reason_rejected": "paper analyzes lean and obese separately (S3.2.p1); pooling changes the estimand"}, {"value": "one model ~ subject + status:time", "reason_rejected": "equivalent fixed-effect estimand to per-stratum paired fits but pools residual variance across groups; paper's per-group reporting favors separate fits"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 16, "n_columns": 9, "columns": ["Intercept", "time_pre", "subject_subject2", "subject_subject3", "subject_subject4", "subject_subject5", "subject_subject6", "subject_subject7", "subject_subject8"], "rank": 9, "full_rank": true, "residual_df": 7, "levels": {"time": {"post": 8, "pre": 8}, "subject": {"subject1": 2, "subject2": 2, "subject3": 2, "subject4": 2, "subject5": 2, "subject6": 2, "subject7": 2, "subject8": 2}}, "cells": [{"cell": ["post", "subject1"], "n": 1}, {"cell": ["post", "subject2"], "n": 1}, {"cell": ["post", "subject3"], "n": 1}, {"cell": ["post", "subject4"], "n": 1}, {"cell": ["post", "subject5"], "n": 1}, {"cell": ["post", "subject6"], "n": 1}, {"cell": ["post", "subject7"], "n": 1}, {"cell": ["post", "subject8"], "n": 1}, {"cell": ["pre", "subject1"], "n": 1}, {"cell": ["pre", "subject2"], "n": 1}, {"cell": ["pre", "subject3"], "n": 1}, {"cell": ["pre", "subject4"], "n": 1}, {"cell": ["pre", "subject5"], "n": 1}, {"cell": ["pre", "subject6"], "n": 1}, {"cell": ["pre", "subject7"], "n": 1}, {"cell": ["pre", "subject8"], "n": 1}], "min_cell_size": 1, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 16, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 16, "status": "sample_identifier"}, {"column": "status", "n_levels": 2, "status": "crossed", "crosstab": {"post": {"le ... [2734 more characters]

reasoning: Each subject contributes a pre and a post biopsy (S2.3.p1); subject is the blocking unit. Sex is not in GEO metadata and is not added as a covariate (it is constant within subject and absorbed by the subject block). Leg (rest right / exercise left) and day are completely aliased with time by design (S2.2.p1, S2.3.p1: not randomized) and cannot be separated; recorded as a caveat, not a covariate.

### method (valid, not_started)

final: {"matrix_type": "linear normalized CPM (edgeR-normalized counts per million)", "method": "limma (limma-trend on log2(CPM+1), subject blocking)", "formula": "~ subject + time", "paper_route": {"method": "edgeR negative-binomial GLM on featureCounts counts", "status": "blocked", "reason": "Only edgeR-normalized CPM is deposited (GSE185957_norm_cpm.txt.gz); raw counts and library sizes are not available, so a count-based NB GLM cannot be fitted. CPM must not be rounded into counts."}, "deviations": ["limma on log2(CPM+1) instead of edgeR NB GLM on counts", "low-expression filter CPM >= 1 in >= 4 of the 8 samples per stratum (paper's filter not stated; paper reports 13,175 transcripts identified)", "subject blocking assumed (paper does not state its GLM design)"], "transform": "log2(x+1)"}

reasoning: Matrix policy: linear normalized expression -> log2(x+1) then limma. Paired design via subject term. Filter on deposited CPM values approximates the usual edgeR filterByExpr/CPM filter.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper rule applied to the limma-on-log2CPM deviation route; rule stated in S3.1.p1 and assumed to carry to the exercise contrasts (FIG2 uses FDR)."}

reasoning: S3.1.p1: adjusted p-value < 0.05, log2(fold-change) > +/-0.5. Audit: BH < 0.05 without fold-change cutoff.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "lean_post_vs_pre", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\lean_post_vs_pre\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\lean_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"lean_post_vs_pre": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 13693, "n_significant": 554, "n_up": 432, "n_down": 122, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13693, "n_significant": 559, "n_up": 435, "n_down": 124, "deg_sanity": "ok"}}}}

reasoning: Paired exercise effect in lean (S3.2.p1, FIG2A).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "obese_post_vs_pre", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\obese_post_vs_pre\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\obese_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"obese_post_vs_pre": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 13518, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13518, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paired exercise effect in obese (S3.2.p1, FIG2B).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "lean_post_vs_pre_unpaired", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\lean_post_vs_pre_unpaired\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\lean_post_vs_pre_unpaired\\DEG_results_post_vs_pre.csv"], "counts": {"lean_post_vs_pre_unpaired": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 13693, "n_significant": 62, "n_up": 55, "n_down": 7, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13693, "n_significant": 62, "n_up": 55, "n_down": 7, "deg_sanity": "ok"}}}}

reasoning: Paper does not state whether its edgeR GLM blocked on subject; unpaired fit tests that alternative. Not the primary estimand (ignores pairing).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "obese_post_vs_pre_unpaired", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\obese_post_vs_pre_unpaired\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\obese_post_vs_pre_unpaired\\DEG_results_post_vs_pre.csv"], "counts": {"obese_post_vs_pre_unpaired": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 13518, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13518, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: As above for obese; checks whether the paper's 104 obese DEGs could come from an unblocked model.

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "joint_paired_change", "role": "sensitivity", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\joint_paired_change\\input\\log2_matrix.csv", "transform": "log2(x+1)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\joint_paired_change\\followup_post\\DEG_results_lean_post_vs_pre.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\joint_paired_change\\followup_post\\DEG_results_obese_post_vs_pre.csv"], "counts": {"joint_paired_change/lean_post_vs_pre": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 13492, "n_significant": 452, "n_up": 343, "n_down": 109, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13492, "n_significant": 487, "n_up": 366, "n_down": 121, "deg_sanity": "ok"}}, "joint_paired_change/obese_post_vs_pre": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.5", "n_tested": 13492, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13492, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Within-subject post-pre differences for all 8 subjects in one limma model with a group mean per BMI status: same paired estimand per group but residual variance pooled across both groups (6 df instead of 3), closer to a single edgeR GLM fitted on all 16 libraries.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "lean_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\enrichment_lean_post_vs_pre\\gsea\\DEG_results_post_vs_pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12893 Human genes ranked by 'stat'. 50 Hallmark sets tested, 40 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_UV_RESPONSE_DN | NES=2.04 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.82 | NOM p=0.00e+00 | FDR q=3.81e-03 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.81 | NOM p=0.00e+00 | FDR q=3.72e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.80 | NOM p=2.61e-03 | FDR q=3.20e-03 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.73 | NOM p=0.00e+00 | FDR q=7.43e-03 - HALLMARK_TGF_BETA_SIGNALING | NES=1.73 | NOM p=5.93e-03 | FDR q=6.53e-03 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.72 | NOM p=0.00e+00 | FDR q=6.00e-03 - HALLMARK_HYPOXIA | NES=1.70 | NOM p=0.00e+00 | FDR q=7.62e-03 - HALLMARK_ANGIOGENESIS | NES=1.67 | NOM p=2.37e-02 | FDR q=1.06e-02 ### Top 6 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.84 | NOM p=0.00e+00 | FDR q=1.58e-03 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-1.59 | NOM p=0.00e+00 | F ... [392 more characters]

reasoning: Paper ran GSEA on the exercise comparison (S2.7.p1, S3.2.p2); Hallmark used here as available gene-set library.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "obese_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35470975\\GSE185957\\results\\enrichment_obese_post_vs_pre\\gsea\\DEG_results_post_vs_pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12710 Human genes ranked by 'stat'. 50 Hallmark sets tested, 15 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ANDROGEN_RESPONSE | NES=1.62 | NOM p=4.96e-03 | FDR q=9.36e-02 - HALLMARK_HYPOXIA | NES=1.53 | NOM p=1.56e-03 | FDR q=1.24e-01 - HALLMARK_MTORC1_SIGNALING | NES=1.49 | NOM p=3.12e-03 | FDR q=1.24e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.49 | NOM p=4.84e-02 | FDR q=9.53e-02 - HALLMARK_APICAL_SURFACE | NES=1.46 | NOM p=4.02e-02 | FDR q=9.76e-02 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.46 | NOM p=9.52e-03 | FDR q=8.14e-02 - HALLMARK_HEME_METABOLISM | NES=1.46 | NOM p=1.58e-03 | FDR q=7.05e-02 - HALLMARK_ANGIOGENESIS | NES=1.45 | NOM p=5.15e-02 | FDR q=7.07e-02 - HALLMARK_UV_RESPONSE_DN | NES=1.43 | NOM p=1.16e-02 | FDR q=7.58e-02 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.41 | NOM p=1.81e-02 | FDR q=8.22e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=-1.88 | NOM p=0.00e+00 | FDR q=5.85e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=-1.53 | NOM p=2.87e-03 | FDR q=7.21e-02 - HALLMA ... [391 more characters]

reasoning: Paper ran GSEA on the exercise comparison (S2.7.p1, S3.2.p2).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper's edgeR-on-counts route blocked: only normalized CPM deposited; limma on log2(CPM+1) runs instead.", "Exercise is aliased with leg (rest right leg, exercise left leg) and with day; not randomized (S2.2.p1, S2.3.p1). The post-vs-pre contrast estimates exercise + leg + day.", "n = 4 pairs per group; preliminary study (S5.p1). Results are low-powered.", "Sex: X/Y inference (suitability sex check) gives lean subjects 1-4 all female and obese subjects 5,6 male / 7,8 female; paper text says lean 2F/2M and obese 4F (S2.1.p1) or 2F/2M each (Table 1). Pre/post of every subject agree in sex, and our lean count matches the paper's lean count, so GEO group labels are taken as the labels the paper analyzed. Per-sex exploratory split not run: female-only lean equals the lean analysis, female-only obese has 2 pairs (< 3), males have 2 pairs (< 3).", "Obese post vs pre: 0 DEGs (padj<0.05 & |log2FC|>0.5) in paired, unpaired and pooled-variance paired-change limma fits, vs 104 in the paper; min padj 0.32. Paper's count not reproduced on the deposited CPM; the paper's edgeR NB GLM on raw counts may have more power, and its exact model is not stated.", "GSEA (Hallmark, not the paper's library): lean shows OXIDATIVE_PHOSPHORYLATION negatively enriched, consistent with the paper's lean mitochondrial/OXPHOS downregulation (S3.2.p2); obese shows one set (INTERFERON_ALPHA_RESPONSE, negative) where the paper reports none."], "results": {"lean_post_vs_ ... [980 more characters]

reasoning: Paper counts from S3.2.p1 (lean 419 up + 132 down; obese 82 up + 22 down). No individual transcripts are named for the exercise contrasts in the text.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "method input",
    "paper": "edgeR NB GLM on featureCounts counts (S2.4.p1)",
    "data": "only edgeR-normalized CPM deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "participant sex",
    "paper": "S2.1.p1: lean 2M/2F, obese 4F; Table 1: 2F/2M in each group",
    "data": "no sex in GEO metadata; X/Y inference: lean 4F, obese 2M/2F; each subject's pre/post agree",
    "disposition": "executable_without_change"
  },
  {
    "item": "low-expression filter",
    "paper": "not stated; 13,175 transcripts identified (S3.1.p1)",
    "data": "64,253 features in CPM file",
    "disposition": "declared_deviation"
  },
  {
    "item": "obese exercise DEG count",
    "paper": "104 (82 up, 22 down) (S3.2.p1)",
    "data": "0 under the paper rule on every limma route tried",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 35470975 / GSE185957

**Status: finished.** The run completed as a declared deviation, and the decision-contract validator found no errors (16 records).

## What ran
- **Route:** the case spec route (`tools.case_runner execute case_spec.json`). Preflight was skipped as instructed.
- **Data:** `GSE185957_norm_cpm.txt.gz`, 64,253 Ensembl genes x 16 samples. The paper's sample set is 8 subjects (4 lean, 4 obese), each with a pre and a post biopsy.
- **Alignment:** exact match on the GEO `title` column, 16/16. `status` and `time` come from `characteristics_ch1.1.group`; `subject` comes from `characteristics_ch1.0.subject`.
- **Matrix:** edgeR-normalized CPM. It is linear and non-integer, column sums are 0.84-1.12e6, and GEO `data_processing` says `norm_cpm.txt`. It is not raw counts.
- **Design:** paired post vs pre (subject blocking, `~ subject + time`), with BMI status as a stratum. There is one fit per group: lean and obese. Suitability verdict: analyzable, 2/2 comparisons.
- **Method:** limma-trend on log2(CPM+1). Genes are filtered to CPM >= 1 in >= 4 of the stratum's 8 samples, which keeps about 13.5-13.7k genes; the paper reports 13,175 transcripts identified.
- **Threshold:** the paper's rule, BH-adjusted p < 0.05 and |log2FC| > 0.5 (S3.1.p1), applied on the deviation route. The audit rule is padj < 0.05 with no fold-change cutoff.
- **Sensitivity fits:**
  - unpaired limma within each group;
  - one pooled-variance paired-change limma on all 8 subjects (`~ 0 + C(status)` on the post-pre differences).
- **Enrichment:** GSEA preranked on MSigDB Hallmark for both primary tables.

## DEG counts vs the paper (padj < 0.05 and |log2FC| > 0.5)

| Contrast | Ours (up/down) | Paper (up/down) |
|---|---|---|
| Lean post vs pre, paired (primary) | 554 (432/122) | 551 (419/132) |
| Obese post vs pre, paired (primary) | 0 (0/0); minimum padj 0.32 | 104 (82/22) |
| Lean, unpaired (sensitivity) | 62 | - |
| Obese, unpaired (sensitivity) | 0 | - |
| Joint paired-change, lean (sensitivity) | 452 | - |
| Joint paired-change, obese (sensitivity) | 0 | - |

- **Lean:** reproduced closely. The top genes are NR4A3, PPARGC1A and NR4A1, all up.
- **Obese:** not reproduced on any limma route. The top obese hits are HBB and HBD, which suggests blood content varies between biopsies.
- **GSEA:**
  - Lean: OXIDATIVE_PHOSPHORYLATION is negatively enriched (FDR 0.002). This matches the paper's lean mitochondrial/OXPHOS downregulation, although the paper used a diffe ... [2129 more characters]
