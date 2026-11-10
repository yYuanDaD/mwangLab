# Review packet B (the analysis' decisions): GSE281849

## Mechanical flags

- **possible_reversed_contrast**: {"contrast": "grp_ACT_vs_SED", "control": "SED", "treatment": "ACT", "note": "the control side reads as exercise or the test side as control"}
- **possible_reversed_contrast**: {"contrast": "grp_AR_vs_SED", "control": "SED", "treatment": "AR", "note": "the control side reads as exercise or the test side as control"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 7, "samples_linked": 21, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_ACT_vs_SED | 71 | 76 | padj < 0.05 and |log2FoldChange| > 0.25 | 152 | 16 | 4 | 268 | 2126 | 489 | 293 | 700 | 0.115 | 0.077 |
| grp_AR_vs_SED | 40 | 45 | padj < 0.05 and |log2FoldChange| > 0.25 | 51 | 20 | 9 | 73 | 1277 | 307 | 155 | 384 | 0.126 | 0.046 |
| grp_AR_vs_ACT | 124 | 134 | padj < 0.05 and |log2FoldChange| > 0.25 | 191 | 39 | 7 | 422 | 2222 | 508 | 281 | 810 | 0.115 | 0.08 |

## Samples per design level

### `grp`
- **ACT** (7): GSM8631060 / Skeletal muscle, trained, replicate 1 / M304; GSM8631061 / Skeletal muscle, trained, replicate 2 / M305; GSM8631062 / Skeletal muscle, trained, replicate 3 / M306; GSM8631064 / Skeletal muscle, trained, replicate 4 / M308; GSM8631065 / Skeletal muscle, trained, replicate 5 / M309; GSM8631068 / Skeletal muscle, trained, replicate 6 / M312; GSM8631075 / Skeletal muscle, trained, replicate 7 / M319
- **AR** (7): GSM8631063 / Skeletal muscle, activity reduction, rep / M307; GSM8631066 / Skeletal muscle, activity reduction, rep / M310; GSM8631070 / Skeletal muscle, activity reduction, rep / M314; GSM8631074 / Skeletal muscle, activity reduction, rep / M318; GSM8631076 / Skeletal muscle, activity reduction, rep / M320; GSM8631077 / Skeletal muscle, activity reduction, rep / M321; GSM8631078 / Skeletal muscle, activity reduction, rep / M322
- **SED** (7): GSM8631067 / Skeletal muscle, inactive, replicate 1 / M311; GSM8631069 / Skeletal muscle, inactive, replicate 2 / M313; GSM8631071 / Skeletal muscle, inactive, replicate 3 / M315; GSM8631072 / Skeletal muscle, inactive, replicate 4 / M316; GSM8631073 / Skeletal muscle, inactive, replicate 5 / M317; GSM8631079 / Skeletal muscle, inactive, replicate 6 / M323; GSM8631080 / Skeletal muscle, inactive, replicate 7 / M325

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE281849"], "assay": "bulk poly(A) RNA-seq, gastrocnemius medial belly, female C57BL/6NJ mice (S2.11.p1, S3.7.p1, FIG3)", "factors": {"group": ["Inactive (inactive control, 6 wk standard housing)", "Active (treadmill 5 d/wk for 6 wk)", "Activity Reduction (treadmill 4 wk then 2 wk inactive)"]}, "sample_inclusion": "RNA-seq on female mice only, n = 7 per group (S3.7.p1, FIG3 legend); males not sequenced", "primary_estimand": "Effect of regular treadmill exercise on the gastrocnemius transcriptome (Active vs Inactive), plus the effect of 2 weeks of activity reduction relative to the inactive and active controls", "planned_contrasts": ["Active vs Inactive (FIG3a; paper: 71 DEGs)", "Activity Reduction vs Inactive (FIG3b; paper: 40 DEGs)", "Activity Reduction vs Active (FIG3c; paper: 124 DEGs)"], "repeated_measure_unit": "none; one sample per independent mouse", "normalization": "DESeq2 median-of-ratios on featureCounts counts (S2.11.p1)", "paper_method": "DESeq2 ~ group, each pairwise comparison fitted on the two groups' samples only (authors' Figure 3.Rmd: subset columns, design ~group, results(contrast=...), no lfcShrink, rowSums>0 prefilter)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.25, "source_locator": "S2.11.p1"}, "paper_results": "71/40/124 DEGs (S3.7.p1); 7 transcripts unique to Activity Reduction (Smyd2, En1, Hoxa11os up; Ostn, Ak4, Srrm4os, Zfhx4 down); Igfbp5 down in Active and AR vs I ... [49 more characters]

reasoning: S2.3.p1 defines the three randomized groups; S2.11.p1 gives DESeq2 and 'FDR<0.05 and the fold change was >0.25 in either direction'; FIG3 legend says 'q < 0.05 and expression change >= 20%'; S3.7.p1 gives the DEG counts on female gastrocnemius n=7/group. The authors' public Figure 3.Rmd (DA.p1 link) fits each pairwise comparison separately with design ~group and calls DEGs at padj<=0.05 and |log2FC|>=0.27.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE281849\\GSE281849_Gastroc_RawCounts.csv.gz", "owned": true, "checks": ["DA.p1 names GSE281849", "21 GEO samples = 7 per group, female gastrocnemius, matches FIG3 legend n=21", "GEO data_processing (fastp, STAR GRCm39, featureCounts, DESeq2) matches S2.11.p1", "sample IDs M304-M325 match the columns in the authors' Figure 3.Rmd and their group lists"], "accession": "GSE281849", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE281849\\GSE281849_metadata.csv"}

reasoning: DA.p1 names GSE281849; samples, tissue and processing agree with the paper and the authors' code.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 21, "n_metadata": 21, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.2.treatment", "recode": {"Inactive 6 weeks": "SED", "Treadmill trained 6 weeks": "ACT", "Treadmill trained 4 weeks, inactive 2 weeks": "AR"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\aligned\\design_metadata.csv", "sha256": "c7cdddca649ff46f2823a89f61a0728927ae3abe38f8aa37ffa204397b95d76d", "levels": {"grp": {"ACT": 7, "AR": 7, "SED": 7}}}}

reasoning: Matrix columns (M304...) equal the metadata 'description' field for all 21 samples (inspect alignment_keys). Group from characteristics treatment: SED = inactive control, ACT = active control, AR = activity reduction. The resulting sample lists equal the authors' code lists (AR = M307,M310,M314,M318,M320,M321,M322; Active = M304,M305,M306,M308,M309,M312,M319).

### matrix (valid, not_started)

final: {"source": "GSE281849_Gastroc_RawCounts.csv.gz", "paper_input": "featureCounts read counts into DESeq2 (S2.11.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\aligned\\aligned_matrix.csv", "sha256": "031500ef4f2bd253a0d9df4c0f9ab12e49f5375ac3b013bd56beb95e92dfe4dd", "n_features": 40853, "n_samples": 21, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4681822.0, "median": 1.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer, 0 to 4.7e6; file named RawCounts; GEO data_processing: featureCounts, 'csv file includes raw counts for each sample'. Matches the paper's input.

rejected alternatives: [{"value": "GSE281849_Gastroc_NormalizedCounts.csv.gz", "reason_rejected": "DESeq2-normalized values; DESeq2 needs the raw counts"}]

### design (valid, not_started)

final: {"analysis_type": "multi-group, pairwise planned contrasts", "design_column": "grp", "contrasts": [{"name": "grp_ACT_vs_SED", "control": "SED", "treatment": "ACT", "role": "primary"}, {"name": "grp_AR_vs_SED", "control": "SED", "treatment": "AR", "role": "secondary"}, {"name": "grp_AR_vs_ACT", "control": "ACT", "treatment": "AR", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Three randomized independent groups (S2.3.p1). The exercise effect is Active vs Inactive (primary); Activity Reduction vs Inactive and vs Active are the paper's other planned contrasts (FIG3b,c). All female, so no sex split.

rejected alternatives: [{"value": "pool ACT and AR as 'trained'", "reason_rejected": "the paper keeps three groups and the AR arm is defined by detraining; pooling changes the estimand"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 21, "n_columns": 3, "columns": ["Intercept", "grp_AR", "grp_SED"], "rank": 3, "full_rank": true, "residual_df": 18, "levels": {"grp": {"ACT": 7, "AR": 7, "SED": 7}}, "cells": [{"cell": ["ACT"], "n": 7}, {"cell": ["AR"], "n": 7}, {"cell": ["SED"], "n": 7}], "min_cell_size": 7, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 21, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 21, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.genotype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.treatment", "n_levels": 3, "status": "complete_confounding", "crosstab": {"ACT": {"Inactive 6 weeks": 0, "Treadmill trained 4 weeks, inactive 2 weeks": 0, "Treadmill trained 6 weeks": 7}, "AR": {"I ... [1590 more characters]

reasoning: Independent mice randomized to groups (S2.3.p1); no batch, lane or litter recorded in GEO; the paper models group only.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald), separate fit per pairwise comparison", "formula": "~ grp", "paper_route": {"method": "DESeq2 ~ group, pairwise subsets", "status": "reproduced"}, "deviations": ["pydeseq2 instead of R DESeq2; the authors prefilter rowSums>0, which does not change DESeq2 results for kept genes"]}

reasoning: Raw counts support the paper's DESeq2. The authors' code fits each comparison on its two groups only, so each execution subsets to the two groups. A joint 3-group model is run as a sensitivity analysis.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.25, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.25, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.27, "inclusive": true}, "deviation_note": "Methods text S2.11.p1 ('FDR<0.05 and fold change >0.25 in either direction', read as |log2FC| > 0.25) is applied. FIG3 legend says >=20% change (|log2FC| >= 0.263); the authors' code uses padj<=0.05 and |log2FC|>=0.27, recorded as the audit rule."}

reasoning: S2.11.p1 states the DEG rule; FIG3 legend and the authors' code give near-equal variants, kept as an audit rule.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_ACT_vs_SED", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\grp_ACT_vs_SED\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\grp_ACT_vs_SED\\DEG_results_ACT_vs_SED.csv"], "counts": {"grp_ACT_vs_SED": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.25", "n_tested": 12655, "n_significant": 76, "n_up": 54, "n_down": 22, "deg_sanity": "ok"}, "audit": {"rule": "padj <= 0.05 and |log2FoldChange| >= 0.27", "n_tested": 12655, "n_significant": 71, "n_up": 52, "n_down": 19, "deg_sanity": "ok"}}}}

reasoning: FIG3a Active vs Inactive, fitted on these 14 samples as in the authors' code

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_AR_vs_SED", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\grp_AR_vs_SED\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\grp_AR_vs_SED\\DEG_results_AR_vs_SED.csv"], "counts": {"grp_AR_vs_SED": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.25", "n_tested": 16380, "n_significant": 45, "n_up": 27, "n_down": 18, "deg_sanity": "ok"}, "audit": {"rule": "padj <= 0.05 and |log2FoldChange| >= 0.27", "n_tested": 16380, "n_significant": 41, "n_up": 24, "n_down": 17, "deg_sanity": "ok"}}}}

reasoning: FIG3b Activity Reduction vs Inactive

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_AR_vs_ACT", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\grp_AR_vs_ACT\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\grp_AR_vs_ACT\\DEG_results_AR_vs_ACT.csv"], "counts": {"grp_AR_vs_ACT": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.25", "n_tested": 13697, "n_significant": 134, "n_up": 29, "n_down": 105, "deg_sanity": "ok"}, "audit": {"rule": "padj <= 0.05 and |log2FoldChange| >= 0.27", "n_tested": 13697, "n_significant": 126, "n_up": 24, "n_down": 102, "deg_sanity": "ok"}}}}

reasoning: FIG3c Activity Reduction vs Active

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 21, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\joint\\DEG_results_grp_ACT_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\joint\\DEG_results_grp_AR_vs_SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\joint\\DEG_results_grp_AR_vs_ACT.csv"], "counts": {"joint/grp_ACT_vs_SED": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.25", "n_tested": 11997, "n_significant": 61, "n_up": 43, "n_down": 18, "deg_sanity": "ok"}, "audit": {"rule": "padj <= 0.05 and |log2FoldChange| >= 0.27", "n_tested": 11997, "n_significant": 56, "n_up": 41, "n_down": 15, "deg_sanity": "ok"}}, "joint/grp_AR_vs_SED": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.25", "n_tested": 1990, "n_significant": 15, "n_up": 10, "n_down": 5, "deg_sanity": "ok"}, "audit": {"rule": "padj <= 0.05 and |log2FoldChange| >= 0.27", "n_tested": 1990, "n_significant": 10, "n_up": 7, "n_down": 3, "deg_sanity": "ok"}}, "joint/grp_AR_vs_ACT": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.25", "n_tested": 14220, "n_significant": 115, "n_up": 27, "n_down" ... [179 more characters]

reasoning: one 3-group DESeq2 model on all 21 samples, to check robustness of the pairwise fits

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_ACT_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\enrichment_grp_ACT_vs_SED\\gsea\\DEG_results_ACT_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 27684 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 46 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_COAGULATION | NES=2.75 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.68 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.59 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.46 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.45 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=2.42 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_KRAS_SIGNALING_UP | NES=2.26 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_BILE_ACID_METABOLISM | NES=2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=2.17 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=-2.61 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=-2.53 | NOM p=0.00e+00 |  ... [383 more characters]

reasoning: paper reports GSEA for Active vs Inactive (S3.7.p2)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_AR_vs_ACT", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\enrichment_grp_AR_vs_ACT\\gsea\\DEG_results_AR_vs_ACT_GSEA_Hallmark.csv"], "summary": "GSEA complete on 27620 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 44 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=2.63 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=2.36 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.09 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_DNA_REPAIR | NES=1.81 | NOM p=0.00e+00 | FDR q=1.12e-03 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.76 | NOM p=0.00e+00 | FDR q=1.34e-03 - HALLMARK_HEME_METABOLISM | NES=1.68 | NOM p=0.00e+00 | FDR q=2.98e-03 - HALLMARK_MYOGENESIS | NES=1.54 | NOM p=0.00e+00 | FDR q=9.48e-03 - HALLMARK_TGF_BETA_SIGNALING | NES=1.48 | NOM p=1.81e-02 | FDR q=1.69e-02 - HALLMARK_PROTEIN_SECRETION | NES=1.41 | NOM p=2.73e-02 | FDR q=2.93e-02 - HALLMARK_UV_RESPONSE_UP | NES=1.37 | NOM p=9.71e-03 | FDR q=3.97e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_COAGULATION | NES=-2.70 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.65 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ ... [380 more characters]

reasoning: paper reports GSEA for Activity Reduction vs Active (S3.7.p2)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_AR_vs_SED", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39609254\\GSE281849\\results\\enrichment_grp_AR_vs_SED\\gsea\\DEG_results_AR_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 27629 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 21 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYOGENESIS | NES=1.83 | NOM p=0.00e+00 | FDR q=9.75e-03 - HALLMARK_TGF_BETA_SIGNALING | NES=1.78 | NOM p=0.00e+00 | FDR q=6.50e-03 - HALLMARK_NOTCH_SIGNALING | NES=1.75 | NOM p=8.33e-03 | FDR q=4.70e-03 - HALLMARK_UV_RESPONSE_UP | NES=1.73 | NOM p=0.00e+00 | FDR q=4.61e-03 - HALLMARK_HYPOXIA | NES=1.63 | NOM p=0.00e+00 | FDR q=1.19e-02 - HALLMARK_HEME_METABOLISM | NES=1.59 | NOM p=4.02e-03 | FDR q=1.30e-02 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.59 | NOM p=0.00e+00 | FDR q=1.16e-02 - HALLMARK_APICAL_JUNCTION | NES=1.50 | NOM p=2.07e-03 | FDR q=2.56e-02 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.44 | NOM p=2.06e-03 | FDR q=4.12e-02 - HALLMARK_KRAS_SIGNALING_DN | NES=1.39 | NOM p=1.89e-02 | FDR q=6.19e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_FATTY_ACID_METABOLISM | NES=-1.60 | NOM p=0.00e+00 | FDR q=6.64e-02 - HALLMARK_E2F_TARGETS | NES=-1.50 | NOM p=1.87e-03 | FDR q=9.27e-02 - HALLMARK_UV_RESPONSE_DN | NES=-1.46 ... [380 more characters]

reasoning: paper reports no enrichment for AR vs Inactive (S3.7.p2); checked

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Female mice only; the effect of exercise in males is not assessed by this dataset.", "Paper's GSEA used GO BP with fgsea; this run's GSEA uses MSigDB Hallmark, so pathway results are not directly comparable."], "results": {"grp_ACT_vs_SED": {"n_deg": 76, "up": 54, "down": 22, "rule": "padj < 0.05 and |log2FoldChange| > 0.25", "audit_n": 71}, "grp_AR_vs_SED": {"n_deg": 45, "up": 27, "down": 18, "rule": "padj < 0.05 and |log2FoldChange| > 0.25", "audit_n": 41}, "grp_AR_vs_ACT": {"n_deg": 134, "up": 29, "down": 105, "rule": "padj < 0.05 and |log2FoldChange| > 0.25", "audit_n": 126}, "joint/grp_ACT_vs_SED": {"n_deg": 61, "up": 43, "down": 18, "rule": "padj < 0.05 and |log2FoldChange| > 0.25", "audit_n": 56}, "joint/grp_AR_vs_SED": {"n_deg": 15, "up": 10, "down": 5, "rule": "padj < 0.05 and |log2FoldChange| > 0.25", "audit_n": 10}, "joint/grp_AR_vs_ACT": {"n_deg": 115, "up": 27, "down": 88, "rule": "padj < 0.05 and |log2FoldChange| > 0.25", "audit_n": 108}}, "paper_counts": {"grp_ACT_vs_SED": 71, "grp_AR_vs_SED": 40, "grp_AR_vs_ACT": 124}, "comparison": {"grp_ACT_vs_SED": {"ours": 76, "paper": 71}, "grp_AR_vs_SED": {"ours": 45, "paper": 40}, "grp_AR_vs_ACT": {"ours": 134, "paper": 124}}, "paper_gene_check": {"grp_ACT_vs_SED": {"Igfbp5": {"baseMean": 18205.1475, "log2FoldChange": -0.5793, "padj": 0.0106, "pvalue": 0.0}, "Acly": {"baseMean": 1019.5176, "log2FoldChange": 0.5342, "padj": 0.0103, "pvalue": 0.0}, "Elovl6": {"baseMean": 112.8351, " ... [2463 more characters]

reasoning: Paper-aligned DESeq2 pairwise route on the deposited raw counts; compare counts and named genes from S3.7.p1.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 21 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG fold-change rule",
    "paper": "S2.11.p1: fold change >0.25; FIG3 legend: >=20% change",
    "data": "authors' Figure 3.Rmd: |log2FC| >= 0.27, padj <= 0.05",
    "disposition": "executable_without_change"
  },
  {
    "item": "GSEA gene sets",
    "paper": "fgsea on GO Biological Process, FDR<0.25",
    "data": "workflow GSEA uses MSigDB Hallmark",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID39609254 / GSE281849

## What ran
- Case spec route (`case_spec.json`, `python -m tools.case_runner execute`). Status: completed. Contract validator: 16 records, 0 errors.
- Matrix: `GSE281849_Gastroc_RawCounts.csv.gz`, raw featureCounts counts (21 female gastrocnemius samples, 40,853 genes). The NormalizedCounts file was rejected.
- Alignment: exact on the metadata `description` field (M304 to M325), 21/21 matched. grp = SED (Inactive), ACT (Active, treadmill 6 wk), AR (Activity Reduction, 4 wk treadmill then 2 wk inactive), 7 per group. Suitability: analyzable. Sex check: all one sex, consistent with the paper's female-only RNA-seq.
- Method: DESeq2 (pydeseq2 Wald), `~ grp`, one fit per pairwise comparison on that pair's 14 samples. This copies the authors' own Figure 3.Rmd, which is linked from DA.p1 and was read through a web fetch: column subsets, `design = ~group`, no lfcShrink. Primary contrast: ACT vs SED (the exercise effect). Secondary contrasts: AR vs SED and AR vs ACT.
- Sensitivity check: one joint 3-group DESeq2 model on all 21 samples (`joint/*`).
- Enrichment: preranked Hallmark GSEA on the stat ranking for all three pairwise tables, all completed.

## DEG counts vs paper
Paper rule (S2.11.p1): FDR < 0.05 and |log2FC| > 0.25. Audit rule (the authors' code): padj <= 0.05 and |log2FC| >= 0.27. The FIG3 legend's ">= 20%" (log2 0.263) falls between these two.

| Contrast | Paper (S3.7.p1) | Ours, paper rule | Ours, audit rule (code) | Joint model, paper rule |
|---|---|---|---|---|
| Active vs Inactive (primary) | 71 | 76 (54 up / 22 down) | 71 | 61 |
| Activity Reduction vs Inactive | 40 | 45 (27 / 18) | 41 | 15 |
| Activity Reduction vs Active | 124 | 134 (29 / 105) | 126 | 115 |

Under the authors' code threshold the counts match the paper almost exactly: 71/41/126 against 71/40/124.

Named genes from S3.7.p1 were all significant, in the paper's direction:
- Igfbp5 is down in both ACT and AR vs SED.
- Smyd2, En1 and Hoxa11os are up in AR vs both controls.
- Ostn, Ak4, Srrm4os and Zfhx4 are down in AR vs both controls.
- The Active-unique genes Acly, Elovl6, F13a1, Folr2, Gfpt2, Il1r1, Lama4 and Nrp2 are up, and Ctxn3, Dglucy and Gstp2 are down, in ACT vs SED. Acly and Elovl6 are down in AR vs ACT.

The joint 3-group model gives fewer AR vs SED DEGs (15). It pools dispersion across all three groups, which is why the paper's pairwise-subset route was kept as primary.

## Deviations
- pydeseq2 was used instead of R DESeq2. The a ... [1322 more characters]
