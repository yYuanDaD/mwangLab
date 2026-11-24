# Review packet B (the analysis' decisions): GSE144109

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.group", "n_values": 5, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## Samples per design level

### `grp`
- **MHE** (3): GSM4280413 / F3-4-8; GSM4280415 / F5-3-4; GSM4280421 / F7-4-4
- **MHS** (3): GSM4280418 / F7-1-3; GSM4280419 / F7-2-1; GSM4280420 / F7-2-4
- **NCS** (3): GSM4280407 / F1-3-1; GSM4280408 / F1-3-7; GSM4280416 / F6-1-5
- **PHE** (3): GSM4280409 / F1-4-5; GSM4280410 / F2-1-2; GSM4280417 / F6-3-4
- **PHS** (3): GSM4280411 / F2-3-7; GSM4280412 / F2-4-7; GSM4280414 / F4-1-1

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE144109"], "assay": "bulk RNA-seq (Illumina TruSeq stranded total RNA, HiSeq 2500), quadriceps of adult female offspring", "factors": {"grp": ["NCS (NC-fed parents, sedentary dam)", "MHS (maternal HF, sedentary dam)", "MHE (maternal HF, dam ran voluntarily during gestation)", "PHS (paternal HF, sedentary dam)", "PHE (paternal HF, dam ran during gestation)"]}, "inclusion": "15 female offspring, n=3 per group (GEO overall design: '3 samples per groups'); NC-Sed shared control for maternal (Study 1) and paternal (Study 2) lines (GEO treatment protocol)", "primary_estimand": "Effect of maternal voluntary wheel running during gestation on adult female offspring skeletal-muscle transcriptome under parental high-fat diet: MHE vs MHS (maternal HF line) and PHE vs PHS (paternal HF line)", "planned_contrasts": ["grp_MHE_vs_MHS: maternal exercise within maternal-HF line (abstract: 'maternal exercise resulted in a transcriptional profile similar to offspring from NC-fed parents'; paper count not in abstract)", "grp_PHE_vs_PHS: maternal exercise within paternal-HF line (same abstract sentence)", "grp_MHS_vs_NCS and grp_PHS_vs_NCS: parental HF vs NC (abstract: profiles 'enriched in genes regulating inflammation and immune responses')", "grp_MHE_vs_NCS and grp_PHE_vs_NCS: does exercise bring HF offspring back toward NC (abstract: 'similar to NC')"], "repeated_measure_unit": "none; one muscle per offspring", "paper_method": "DESeq2 v1.11.8 'for maternal and paternal lines  ... [499 more characters]

reasoning: No full text is available; the study map rests on the PubMed abstract (PMID33332990_abstract.txt) and the GEO series/sample records (summary, overall design, treatment_protocol_ch1, data_processing). The paper's DEG threshold and counts are therefore unknown.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE144109\\GSE144109_reconstructed_counts.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 33332990", "GSE144109 is the RNA-Seq SubSeries of GSE144112; same title as paper topic", "matrix columns equal the 15 GSM titles exactly"], "accession": "GSE144109", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE144109\\GSE144109_metadata.csv"}

reasoning: GEO record links PMID 33332990; GSE144109_normalized_counts.tsv.gz is the only supplementary matrix and its 15 columns match the sample titles.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 15, "n_metadata": 15, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.3.group"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\aligned\\design_metadata.csv", "sha256": "775751bce98f0b3f9198e8f13f7bed3b0ece4d2fbce17294ac5b6103347b71e5", "levels": {"grp": {"NCS": 3, "PHE": 3, "PHS": 3, "MHE": 3, "MHS": 3}}}}

reasoning: inspect alignment_keys: title matches 15/15 matrix columns exactly. grp is taken from the GEO 'group' characteristic (NCS/MHS/MHE/PHS/PHE), consistent with the diet/treatment/parent columns.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\aligned\\aligned_matrix.csv", "sha256": "ed40d0a3cf08240cf8896d4d0d2879b5c3ad01d689d6998c0bbf5974782db615", "n_features": 50686, "n_samples": 15, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3160799.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Deposited file is DESeq2-normalized featureCounts counts (data_processing: 'gene coverages in units of normalized read counts'; 61.6% integer). Each column is exactly integer counts / size factor: multiplying by 1/(smallest positive value) gives integers with max deviation 1e-8 on all 50,686 genes x 15 samples (prep_counts.py). This is an exact inversion, not rounding of estimated counts; recovered library sizes 18-27M reads are plausible for 100-bp SE HiSeq. The reconstructed integers equal the featureCounts counts up to one per-sample constant, which DESeq2's size-factor estimation removes. Paper input: DESeq2 on featureCounts counts, so the matrix agrees with the paper.

rejected alternatives: [{"value": "linear normalized -> log2(x+1) + limma", "reason_rejected": "the matrix is exactly invertible to counts, so the paper's count route is available"}]

### design (valid, not_started)

final: {"analysis_type": "multi-group, fitted per parental line", "design_column": "grp", "contrasts": [{"name": "grp_MHE_vs_MHS", "control": "MHS", "treatment": "MHE", "role": "primary"}, {"name": "grp_PHE_vs_PHS", "control": "PHS", "treatment": "PHE", "role": "primary"}, {"name": "grp_MHS_vs_NCS", "control": "NCS", "treatment": "MHS", "role": "secondary"}, {"name": "grp_PHS_vs_NCS", "control": "NCS", "treatment": "PHS", "role": "secondary"}, {"name": "grp_MHE_vs_NCS", "control": "NCS", "treatment": "MHE", "role": "secondary"}, {"name": "grp_PHE_vs_NCS", "control": "NCS", "treatment": "PHE", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 12}}

reasoning: The exercise estimand is maternal running vs sedentary within the same parental-HF exposure: MHE vs MHS and PHE vs PHS (primary). HF vs NC and HF-Ex vs NC test the abstract's 'inflammation' and 'similar to NC' statements (secondary). There is no NC-Ex arm, so the exercise effect under normal chow and an exercise x diet interaction cannot be estimated; the five groups are levels of one factor, not a full factorial. Following GEO data_processing ('DESeq2 ... for maternal and paternal lines separately'), each line is fitted on its own three groups with the shared NCS controls. n=3 per arm.

rejected alternatives: [{"value": "diet x treatment factorial", "reason_rejected": "no NC-Ex group; diet and treatment are not crossed"}, {"value": "pooled MHE+PHE vs MHS+PHS", "reason_rejected": "pools different parental exposures; the paper analyzes lines separately"}, {"value": "one 5-group model on all samples", "reason_rejected": "paper fits lines separately; kept as possible sensitivity only, not run"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 15, "n_columns": 5, "columns": ["Intercept", "grp_MHS", "grp_NCS", "grp_PHE", "grp_PHS"], "rank": 5, "full_rank": true, "residual_df": 10, "levels": {"grp": {"NCS": 3, "PHE": 3, "PHS": 3, "MHE": 3, "MHS": 3}}, "cells": [{"cell": ["MHE"], "n": 3}, {"cell": ["MHS"], "n": 3}, {"cell": ["NCS"], "n": 3}, {"cell": ["PHE"], "n": 3}, {"cell": ["PHS"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 15, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 15, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.diet", "n_levels": 2, "status": "primary_nested_in_candidate", "crosstab": {"MHE": {"high-fat diet": 3, "normal chow": 0}, "MHS": {"high-fat diet": 3, "normal chow": 0}, "NCS": {"high-fat diet": 0, "normal chow": 3}, "PHE": {"high-fat diet": 3, "normal chow": 0} ... [2578 more characters]

reasoning: Each sample is a different offspring; no batch, litter or lane column is deposited. Litter (dam) is a plausible clustering unit (offspring of the same dam share the gestational exposure) but dam IDs are not in GEO; titles such as F7-2-1/F7-2-4 hint at shared family codes, but the code is undocumented, so it is not used as a blocking term. Recorded as a caveat.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald), separate fit per parental line", "formula": "~ grp", "paper_route": {"method": "DESeq2 v1.11.8 per line", "status": "reproduced", "reason": "counts reconstructed exactly from the normalized matrix"}, "deviations": ["pydeseq2 instead of R DESeq2 v1.11.8", "paper's low-count filtering and LFC shrinkage unknown (abstract only); none applied"]}

reasoning: Paper used DESeq2 per line (GEO data_processing); counts are available after exact inversion.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "not stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Abstract states no DE threshold; workflow default BH padj < 0.05 with no fold-change rule. Raw p < 0.05 is an audit count only."}

reasoning: No full text; abstract gives no threshold.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "maternal_line", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\maternal_line\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\maternal_line\\DEG_results_grp_MHE_vs_MHS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\maternal_line\\DEG_results_grp_MHS_vs_NCS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\maternal_line\\DEG_results_grp_MHE_vs_NCS.csv"], "counts": {"maternal_line/grp_MHE_vs_MHS": {"applied": {"rule": "padj < 0.05", "n_tested": 26040, "n_significant": 2, "n_up": 1, "n_down": 1, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26040, "n_significant": 1249, "n_up": 518, "n_down": 731, "deg_sanity": "ok"}}, "maternal_line/grp_MHS_vs_NCS": {"applied": {"rule": "padj < 0.05", "n_tested": 16930, "n_significant": 11, "n_up": 11, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26040, "n_significant": 658, "n_up": 489, "n_down": 169, "deg_sanity": "ok"}}, "maternal_line/grp_MHE_vs_NCS": {"applied": {"rule": "padj < 0.05", "n_tested": 26040, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_te ... [87 more characters]

reasoning: Study 1 (maternal HF line) fitted separately as in GEO data_processing; holds primary MHE vs MHS.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "paternal_line", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\paternal_line\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\paternal_line\\DEG_results_grp_PHE_vs_PHS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\paternal_line\\DEG_results_grp_PHS_vs_NCS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\paternal_line\\DEG_results_grp_PHE_vs_NCS.csv"], "counts": {"paternal_line/grp_PHE_vs_PHS": {"applied": {"rule": "padj < 0.05", "n_tested": 26101, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26101, "n_significant": 528, "n_up": 274, "n_down": 254, "deg_sanity": "ok"}}, "paternal_line/grp_PHS_vs_NCS": {"applied": {"rule": "padj < 0.05", "n_tested": 26101, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 26101, "n_significant": 436, "n_up": 207, "n_down": 229, "deg_sanity": "ok"}}, "paternal_line/grp_PHE_vs_NCS": {"applied": {"rule": "padj < 0.05", "n_tested": 12427, "n_significant": 121, "n_up": 76, "n_down": 45, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_t ... [88 more characters]

reasoning: Study 2 (paternal HF line) fitted separately; holds primary PHE vs PHS.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "maternal_line/grp_MHE_vs_MHS", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\enrichment_maternal_line_grp_MHE_vs_MHS\\gsea\\DEG_results_grp_MHE_vs_MHS_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25361 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 39 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_UV_RESPONSE_DN | NES=2.31 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.25 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PROTEIN_SECRETION | NES=2.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=2.15 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=1.84 | NOM p=0.00e+00 | FDR q=4.34e-04 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.83 | NOM p=0.00e+00 | FDR q=7.24e-04 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.80 | NOM p=0.00e+00 | FDR q=7.76e-04 - HALLMARK_TGF_BETA_SIGNALING | NES=1.70 | NOM p=2.16e-03 | FDR q=2.58e-03 - HALLMARK_MITOTIC_SPINDLE | NES=1.65 | NOM p=0.00e+00 | FDR q=3.26e-03 - HALLMARK_E2F_TARGETS | NES=1.65 | NOM p=0.00e+00 | FDR q=2.93e-03 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_XENOBIOTIC_METABOLISM | NES=-2.88 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_BILE_ACID_METABOLISM | NES=-2.46 | ... [416 more characters]

reasoning: abstract reports pathway-level (inflammation/immune) differences

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "paternal_line/grp_PHE_vs_PHS", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\enrichment_paternal_line_grp_PHE_vs_PHS\\gsea\\DEG_results_grp_PHE_vs_PHS_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25388 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 34 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=2.32 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PROTEIN_SECRETION | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HEME_METABOLISM | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.00 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=1.96 | NOM p=0.00e+00 | FDR q=4.01e-04 - HALLMARK_G2M_CHECKPOINT | NES=1.89 | NOM p=0.00e+00 | FDR q=5.01e-04 - HALLMARK_MITOTIC_SPINDLE | NES=1.85 | NOM p=0.00e+00 | FDR q=5.72e-04 - HALLMARK_MTORC1_SIGNALING | NES=1.71 | NOM p=0.00e+00 | FDR q=2.50e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.61 | NOM p=4.43e-03 | FDR q=7.35e-03 - HALLMARK_E2F_TARGETS | NES=1.60 | NOM p=0.00e+00 | FDR q=7.31e-03 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.34 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.33 | NOM p=0. ... [416 more characters]

reasoning: as above

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "maternal_line/grp_MHS_vs_NCS", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\enrichment_maternal_line_grp_MHS_vs_NCS\\gsea\\DEG_results_grp_MHS_vs_NCS_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25361 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 37 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_XENOBIOTIC_METABOLISM | NES=2.89 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_BILE_ACID_METABOLISM | NES=2.64 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.37 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PEROXISOME | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.31 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.31 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.90 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=1.82 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.77 | NOM p=0.00e+00 | FDR q=5.53e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-1.47 | NOM p=0.00e+00 | FDR q=9.62e-02 - HALLMARK_UV_RESPONSE_DN | NES=-1.28 | NOM p=3.35e ... [416 more characters]

reasoning: abstract: HF offspring enriched in inflammation/immune genes

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "paternal_line/grp_PHS_vs_NCS", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33332990\\GSE144109\\results\\enrichment_paternal_line_grp_PHS_vs_NCS\\gsea\\DEG_results_grp_PHS_vs_NCS_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25388 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 41 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PROTEIN_SECRETION | NES=1.85 | NOM p=0.00e+00 | FDR q=5.28e-03 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.79 | NOM p=0.00e+00 | FDR q=5.81e-03 - HALLMARK_ANGIOGENESIS | NES=1.64 | NOM p=1.17e-02 | FDR q=2.18e-02 - HALLMARK_G2M_CHECKPOINT | NES=1.63 | NOM p=0.00e+00 | FDR q=1.64e-02 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.62 | NOM p=0.00e+00 | FDR q=1.54e-02 - HALLMARK_UV_RESPONSE_DN | NES=1.61 | NOM p=1.73e-03 | FDR q=1.32e-02 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.53 | NOM p=1.81e-03 | FDR q=2.85e-02 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.53 | NOM p=5.34e-03 | FDR q=2.62e-02 - HALLMARK_E2F_TARGETS | NES=1.52 | NOM p=0.00e+00 | FDR q=2.42e-02 - HALLMARK_MYC_TARGETS_V1 | NES=1.50 | NOM p=0.00e+00 | FDR q=2.45e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYOGENESIS | NES=-1.98 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_KRAS_SIGNALING_DN | NES=-1.77 | NOM p=0.00e+00 | FDR q=2. ... [416 more characters]

reasoning: as above

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Comparison with the paper rests on the PubMed abstract only; paper DEG counts and threshold unknown.", "Counts were reconstructed from DESeq2-normalized values by exact per-sample inversion (prep_counts.py).", "n=3 per group; offspring may share dams (litter not recorded), so tests may be anti-conservative.", "No NC-Ex group: exercise effect is only estimable under parental HF.", "Liver-transcript contamination in the deposited data: Alb normalized counts 39,506 (F7-2-1, MHS) and 4,225 (F7-2-4, MHS), 2,074 (F2-3-7, PHS), 1,156 (F1-3-7, NCS) vs 3-260 elsewhere (Apoa1/Ttr/Fgb/Apoh follow). Hallmark XENOBIOTIC_METABOLISM and COAGULATION (lead genes Apoe, Fabp1, Crp, Hnf4a) are top in MHS vs NCS (NES +2.9) and reversed in MHE vs MHS (NES -2.9); these are likely contamination, not biology. Samples were kept (no paper basis to exclude; n would fall to 2).", "Direction agrees with the abstract: HALLMARK_INTERFERON_GAMMA/ALPHA up in MHS vs NCS (NES 2.31/2.31, FDR<0.001) and PHS vs NCS (IFNG NES 1.62, FDR 0.015); maternal exercise lowers them in the maternal line (MHE vs MHS IFNA NES -2.01, IFNG -1.67) but not clearly in the paternal line (PHE vs PHS IFNG -1.03, FDR 0.42). The 11 MHS vs NCS DEGs include interferon genes (Ensembl IDs of Gbp2/Gbp3/Nlrc5/Cd274 family)."], "results": {"maternal_line/grp_MHE_vs_MHS": {"n_deg": 2, "up": 1, "down": 1, "rule": "padj < 0.05", "audit_n": 1249}, "maternal_line/grp_MHS_vs_NCS": {"n_deg": 11, "up": 11, "down ... [534 more characters]

reasoning: Paper's planned route (DESeq2 per line on counts) is reproduced; threshold from workflow default.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "offspring age",
    "paper": "abstract: metabolic phenotype at 9 mo",
    "data": "GEO: euthanized at 10 months",
    "disposition": "executable_without_change"
  },
  {
    "item": "offspring sex",
    "paper": "abstract: transcriptomics in female offspring",
    "data": "GEO does not state sex; checked by X/Y genes in suitability",
    "disposition": "executable_without_change"
  },
  {
    "item": "matrix",
    "paper": "DESeq2 on featureCounts counts",
    "data": "only DESeq2-normalized counts deposited; inverted exactly to integers",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID33332990 / GSE144109

**The comparison with the paper rests on the abstract only.** No full text was available. The paper source is the PubMed abstract (`PMID33332990_abstract.txt`, fetched with NCBI efetch) plus the GEO series and sample records. The abstract states no DEG counts, no DE threshold and no DE gene names.

## What ran
- Route: case spec (`case_spec.json`) → `tools.case_runner execute`. Status: completed. Decision-contract validator: 15 records, 0 errors. The second execute superseded the first; the first is kept in `_previous/20261124T200521Z`, and the only change was added study caveats.
- Data: GSE144109 holds quadriceps RNA-seq from 15 adult female offspring. There are 5 groups, n=3 each: NCS (NC-fed parents, sedentary dam), MHS/MHE (maternal HF, dam sedentary or running during gestation), and PHS/PHE (paternal HF, dam sedentary or running). The sex check passed: one sex only.
- Matrix: only `GSE144109_normalized_counts.tsv.gz` (DESeq2-normalized counts) is deposited. `prep_counts.py` rebuilt the integer counts by multiplying each column by 1/(smallest positive value).
  - The inversion is exact: max deviation from an integer is 1e-8 across all 50,686 × 15 values.
  - Recovered library sizes are 18–27 M reads.
  - Each sample is off from the original counts by at most one constant factor, which DESeq2's size factors remove.
- Design: the paper's GEO processing note says "DESeq2 for maternal and paternal lines separately". So I fitted pydeseq2 Wald with `~ grp` once per line, each on {NCS, xHS, xHE}.
- Threshold: `workflow_default` (BH padj < 0.05, no fold-change rule), because the abstract states none. The audit rule is raw p < 0.05.
- Enrichment: Hallmark GSEA (ranked by stat) on the two exercise contrasts and the two HF-vs-NC contrasts.

## DEG counts (padj < 0.05) vs paper
| Contrast | Role | DEGs (up/down) | audit p<0.05 | Paper |
|---|---|---|---|---|
| MHE vs MHS (maternal exercise, maternal-HF line) | primary | 2 (1/1) | 1249 | not in abstract |
| PHE vs PHS (maternal exercise, paternal-HF line) | primary | 0 | 528 | not in abstract |
| MHS vs NCS | secondary | 11 (11/0) | 658 | not in abstract |
| PHS vs NCS | secondary | 1 (1/0) | 436 | not in abstract |
| MHE vs NCS | secondary | 0 | 1089 | not in abstract |
| PHE vs NCS | secondary | 121 (76/45) | 1758 | not in abstract |

Pathway-level comparison with the abstract's qualitative claims:
- **Parental HF raises inflammation/immune signals: agrees.** Interferon-γ a ... [2903 more characters]
