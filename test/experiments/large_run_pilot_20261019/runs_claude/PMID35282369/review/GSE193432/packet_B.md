# Review packet B (the analysis' decisions): GSE193432

## Mechanical flags

- **unused_subject_like_column**: {"column": "source_name_ch1", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "characteristics_ch1.2.treatment", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "source_name_ch1", "pairs_or_sets": 3, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_HFBAIBA_vs_HFSed | 29 | 34 | padj < 0.05 and |log2FoldChange| > 1 | 61 | 45 | 34 | 108 | 1444 | 718 | 429 | 471 | 0.136 | 0.059 |
| pair_baiba | 29 | 28 | padj < 0.05 and |log2FoldChange| > 1 | 34 | 34 | 28 | 53 | 939 | 571 | 351 | 300 | 0.108 | 0.04 |

## Samples per design level

### `grp`
- **HFBAIBA** (3): GSM5800149 / Heart, HF+Med, 1; GSM5800150 / Heart, HF+Med, 2; GSM5800151 / Heart, HF+Med, 3
- **HFExe** (3): GSM5800146 / Heart, HF+Exe, 1; GSM5800147 / Heart, HF+Exe, 2; GSM5800148 / Heart, HF+Exe, 3
- **HFSed** (3): GSM5800143 / Heart, HF+Sed, 1; GSM5800144 / Heart, HF+Sed, 2; GSM5800145 / Heart, HF+Sed, 3
- **Sham** (3): GSM5800140 / Heart, Sham, 1; GSM5800141 / Heart, Sham, 2; GSM5800142 / Heart, Sham, 3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE193432 (RNA-seq, S6.p1)", "MTBLS3927 (metabolomics, not analyzed here)"], "assay": "bulk mRNA-seq of rat left-ventricular myocardium, Illumina NovaSeq 6000, HISAT2 + featureCounts (S2.15.p1)", "organism": "Rattus norvegicus, male Sprague-Dawley, 8 weeks (S2.1.p1)", "factors": {"group": ["Sham operation", "HF (MI by LAD ligation) + sedentary", "HF + treadmill exercise (60 min/day, 5 d/wk, 8 wk, 50-60% max)", "HF + BAIBA 75 mg/kg/day"]}, "sample_inclusion": "n = 3 per group in GEO (12 samples); Fig 5A states n = 3 for BAIBA vs HF", "tissue_note": "anterior LV wall; in the BAIBA group the peri-infarct area was used (S2.15.p1)", "primary_estimand": "Effect of treadmill exercise on the myocardial transcriptome of rats with post-MI heart failure: HF+Exercise vs HF+Sedentary (abstract ABS.p3 compares 'exercised' with 'Sham (non-exercised) HF'). The paper's only reported RNA-seq DEG result is the exercise-mimetic BAIBA arm vs non-exercised HF (S3.4.p1, Fig 5).", "planned_contrasts": ["HF+Exercise vs HF+Sedentary (exercise effect; paper's estimand for exercise, ABS.p3 / S3.1-S3.2; no RNA-seq DEG count reported)", "HF+BAIBA vs HF+Sedentary (S3.4.p1, Fig 5A-C: 11 up, 18 down = 29 DEGs; text says 'compared to the Sham group' but Fig 5A says 'BAIBA vs. HF group' and the paper calls the non-exercised HF group 'Sham (non-exercised) HF' in ABS.p3)"], "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": ... [546 more characters]

reasoning: S2.15.p1 describes RNA-seq: HISAT2/featureCounts, DESeq2, DEGs = |log2FC|>1 and Padj<0.05. S3.4.p1 reports 11 up / 18 down for BAIBA vs 'Sham' with 'FC > 2.0, P < 0.05'. Fig 5A legend says OPLS-DA 'BAIBA vs. HF group, n = 3', and S3.4.p1 says sequencing was performed 'in the HF and BAIBA groups', so the reported comparator is the non-exercised HF group. No exercise-arm RNA-seq result is reported, although GEO deposits the HF+Exercise arm; the paper's exercise estimand (ABS.p3, S3.1, S3.2) is exercised HF vs non-exercised HF.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE193432\\GSE193432_gene_count.txt.gz", "owned": true, "checks": ["S6.p1 names GSE193432", "GEO: Rattus norvegicus SD heart, 4 groups x 3 (Sham, HF+Sedentary, HF+Exercise, HF+BAIBA) matches the paper's design", "matrix column names HFExe/HFMed/HFSed/Sham-1..3 match GEO titles Heart, HF+Exe/HF+Med/HF+Sed/Sham, 1..3 (Med = BAIBA per source_name '--BAIBA')", "contact: Dept of Rehabilitation, China-Japan Union Hospital, Changchun (Jilin University), matches S2.1.p1 ethics committee", "data_processing names the Shanghai Applied Protein Technology in-house pipeline, as in S2.15.p1"], "accession": "GSE193432", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE193432\\GSE193432_metadata.csv"}

reasoning: Accession cited in the data availability statement; groups, organism, tissue and pipeline all match.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.2.treatment", "regex": "^(Sham operation|HF\\+Sedentary|HF\\+Exercise|HF\\+BAIBA)$", "recode": {"Sham operation": "Sham", "HF+Sedentary": "HFSed", "HF+Exercise": "HFExe", "HF+BAIBA": "HFBAIBA"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\aligned\\design_metadata.csv", "sha256": "24a9b9b624e13ca0fe807e7e8ed8aef5b13f93bd8daa8ff3c29712f0d401f324", "levels": {"grp": {"Sham": 3, "HFSed": 3, "HFExe": 3, "HFBAIBA": 3}}}}

reasoning: Matrix columns (HFExe-1, HFMed-1, HFSed-1, Sham-1) encode group and replicate exactly as the GEO titles do; deriving the key from title and normalizing separators gives a one-to-one exact mapping, no positional alignment. grp comes from the treatment characteristic; HFMed in the matrix = HF+BAIBA (source_name '--BAIBA').

### matrix (valid, not_started)

final: {"source": "GSE193432_gene_count.txt.gz", "paper_input": "featureCounts read counts -> DESeq2 (S2.15.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\aligned\\aligned_matrix.csv", "sha256": "28e3d46f459629a0aee5be0dc4d70e5534c3bbdcd1b212fa8a5daaeb7bb1f9c6", "n_features": 34700, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2274307.0, "median": 2.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 2.27e6, median 2; file named gene_count; GEO data_processing and S2.15.p1 state featureCounts read counts. FPKM is deposited separately (gene_fpkm, Allgene_info) and is not used for DE.

### design (valid, not_started)

final: {"analysis_type": "one factor, four levels; planned contrasts from one model", "design_column": "grp", "formula": "~ grp", "contrasts": [{"name": "grp_HFExe_vs_HFSed", "control": "HFSed", "treatment": "HFExe", "role": "primary"}, {"name": "grp_HFBAIBA_vs_HFSed", "control": "HFSed", "treatment": "HFBAIBA", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: Exercise estimand is HF+Exercise vs HF+Sedentary (both MI-ligated, n=3 each). The paper's reported RNA-seq contrast HF+BAIBA vs HF+Sedentary is secondary (exercise-mimetic). One DESeq2 model ~ grp on all 12 samples with reference HFSed; other suitability comparisons are exploratory.

rejected alternatives: [{"value": "HF+Exercise vs Sham operation", "reason_rejected": "mixes the MI effect with exercise; the paper's exercise comparison is within HF animals (ABS.p3)"}, {"value": "pool HF+Exercise and HF+BAIBA as 'exercise-like'", "reason_rejected": "BAIBA is a pharmacological mimetic, not exercise; levels are never pooled"}, {"value": "HF+BAIBA vs Sham operation (literal reading of S3.4.p1 'compared to the Sham group')", "reason_rejected": "Fig 5A and S3.4.p1 say the sequencing comparison is BAIBA v ... [63 more characters]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 12, "n_columns": 4, "columns": ["Intercept", "grp_HFExe", "grp_HFSed", "grp_Sham"], "rank": 4, "full_rank": true, "residual_df": 8, "levels": {"grp": {"Sham": 3, "HFSed": 3, "HFExe": 3, "HFBAIBA": 3}}, "cells": [{"cell": ["HFBAIBA"], "n": 3}, {"cell": ["HFExe"], "n": 3}, {"cell": ["HFSed"], "n": 3}, {"cell": ["Sham"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 4, "status": "complete_confounding", "crosstab": {"HFBAIBA": {"rats heart --ligation,  anterior descending coronary artery": 0, "rats heart --ligation,  anterior descending coronary artery--BAIBA": 3, "rats heart --ligation,  anterior descending coronary artery--Exercise": 0, "rats heart --no ligation,  anterior descending coronary artery": 0}, "HFExe": {"rats heart --ligation,  anterior descending coronary artery": 0, "rats heart --ligation,  anterior descending coronar ... [3065 more characters]

reasoning: Independent animals, one heart each; no batch, lane or sex variation recorded (all male, S2.1.p1). No pairing.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2", "status": "reproduced"}, "deviations": ["joint ~grp model on all 12 samples as primary (paper's in-house pipeline probably fit each pair separately; pairwise two-arm DESeq2 runs as sensitivity)", "pydeseq2 rather than R DESeq2"]}

reasoning: Raw featureCounts counts support the paper's DESeq2 route (S2.15.p1).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "deviation_note": "S2.15.p1 defines DEGs as |log2FC|>1 and Padj<0.05 (applied). S3.4.p1 reports the 11/18 counts with 'FC > 2.0, P < 0.05' (raw p); that rule is the audit threshold."}

reasoning: Methods state the DEG rule explicitly; results restate it with raw P. Both are reported, applied = methods rule.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\joint\\DEG_results_grp_HFExe_vs_HFBAIBA.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\joint\\DEG_results_grp_HFBAIBA_vs_HFSed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\joint\\DEG_results_grp_Sham_vs_HFBAIBA.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\joint\\DEG_results_grp_HFExe_vs_HFSed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\joint\\DEG_results_grp_Sham_vs_HFExe.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\joint\\DEG_results_grp_Sham_vs_HFSed.csv"], "counts": {"joint/grp_HFExe_vs_HFBAIBA": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15502, "n_significant": 152, "n_up": 58, "n_down": 94, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 24605, "n_significant": 571, "n_up": 216, "n_down": 355, "deg_sanity": "ok"}}, "joint/grp_HFBAIBA_vs_HFSed": {"applied" ... [1592 more characters]

reasoning: one DESeq2 ~grp model on all 12 samples; planned HFExe vs HFSed (primary) and HFBAIBA vs HFSed (paper's reported contrast), other pairs exploratory

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pair_exe", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\pair_exe\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\pair_exe\\DEG_results_HFExe_vs_HFSed.csv"], "counts": {"pair_exe": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 16453, "n_significant": 20, "n_up": 9, "n_down": 11, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 23254, "n_significant": 278, "n_up": 100, "n_down": 178, "deg_sanity": "ok"}}}}

reasoning: two-arm DESeq2 on the six HF animals, as a commercial pairwise pipeline would fit

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pair_baiba", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\pair_baiba\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\pair_baiba\\DEG_results_HFBAIBA_vs_HFSed.csv"], "counts": {"pair_baiba": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 17121, "n_significant": 28, "n_up": 11, "n_down": 17, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 23553, "n_significant": 351, "n_up": 154, "n_down": 197, "deg_sanity": "ok"}}}}

reasoning: two-arm DESeq2 for the paper's reported BAIBA vs HF contrast, the likely paper route

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "joint/grp_HFExe_vs_HFSed", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\enrichment_joint_grp_HFExe_vs_HFSed\\ora\\DEG_results_grp_HFExe_vs_HFSed_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\enrichment_joint_grp_HFExe_vs_HFSed\\ora\\DEG_results_grp_HFExe_vs_HFSed_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\enrichment_joint_grp_HFExe_vs_HFSed\\ora\\DEG_results_grp_HFExe_vs_HFSed_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\enrichment_joint_grp_HFExe_vs_HFSed\\ora\\DEG_results_grp_HFExe_vs_HFSed_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 11 Rat genes (direction=all, padj<0.05, |log2FC|>1.0). ### GO_Biological_Pro ... [1393 more characters]

reasoning: exercise contrast pathways (paper discusses AMPK, fatty acid oxidation, apoptosis)

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "joint/grp_HFExe_vs_HFSed", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35282369\\GSE193432\\results\\enrichment_joint_grp_HFExe_vs_HFSed\\gsea\\DEG_results_grp_HFExe_vs_HFSed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 16966 Rat genes ranked by 'stat'. 50 Hallmark sets tested, 29 significant at FDR q < 0.25. Rat genes matched to mouse Hallmark by symbol: 3883/4291 Hallmark genes present in the ranking. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.78 | NOM p=0.00e+00 | FDR q=6.66e-03 - HALLMARK_MYOGENESIS | NES=1.69 | NOM p=0.00e+00 | FDR q=9.68e-03 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.59 | NOM p=2.53e-03 | FDR q=1.45e-02 - HALLMARK_NOTCH_SIGNALING | NES=1.38 | NOM p=5.28e-02 | FDR q=9.63e-02 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.38 | NOM p=1.09e-02 | FDR q=8.07e-02 - HALLMARK_ANGIOGENESIS | NES=1.33 | NOM p=6.65e-02 | FDR q=1.06e-01 - HALLMARK_MYC_TARGETS_V1 | NES=1.28 | NOM p=3.19e-02 | FDR q=1.51e-01 - HALLMARK_MTORC1_SIGNALING | NES=1.27 | NOM p=2.65e-02 | FDR q=1.38e-01 - HALLMARK_ESTROGEN_RESP ... [550 more characters]

reasoning: exercise contrast pathways (paper discusses AMPK, fatty acid oxidation, apoptosis)

### enrichment (valid, failed)

final: {"organism": "Rat", "subset": "joint/grp_HFBAIBA_vs_HFSed", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": [], "summary": "Enrichr returned no results. Possible network issue or no enriched terms.", "execution_error": "no output written: Enrichr returned no results. Possible network issue or no enriched terms."}

reasoning: paper reports KEGG enrichment (AMPK) for BAIBA vs HF (S3.5, Fig 6F)

### enrichment (valid, failed)

final: {"organism": "Rat", "subset": "joint/grp_HFBAIBA_vs_HFSed", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "execution_error": "GSEA analysis failed. Error: LookupError: No gene sets passed through filtering condition !!! Hint 1: Try to lower min_size or increase max_size ! Hint 2: Check gene symbols are identifiable to your gmt input. Hint 3: Gene symbols curated in Enrichr web services are all upcases."}

reasoning: paper reports KEGG enrichment (AMPK) for BAIBA vs HF (S3.5, Fig 6F)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["The paper reports no RNA-seq DEG result for the exercise arm; the exercise contrast has no paper count to compare.", "n = 3 per group.", "BAIBA hearts were sampled from the peri-infarct area while other groups used the anterior LV wall (S2.15.p1): the BAIBA vs HF contrast confounds treatment with sampling site.", "Paper threshold is internally inconsistent (Padj in methods, raw P in results)."], "results": {"joint/grp_HFExe_vs_HFBAIBA": {"n_deg": 152, "up": 58, "down": 94, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 571}, "joint/grp_HFBAIBA_vs_HFSed": {"n_deg": 34, "up": 13, "down": 21, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 429}, "joint/grp_Sham_vs_HFBAIBA": {"n_deg": 34, "up": 17, "down": 17, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 385}, "joint/grp_HFExe_vs_HFSed": {"n_deg": 16, "up": 7, "down": 9, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 349}, "joint/grp_Sham_vs_HFExe": {"n_deg": 34, "up": 17, "down": 17, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 380}, "joint/grp_Sham_vs_HFSed": {"n_deg": 12, "up": 8, "down": 4, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 376}, "pair_exe": {"n_deg": 20, "up": 9, "down": 11, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 278}, "pair_baiba": {"n_deg": 28, "up": 11, "down": 17, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 351}}, "paper_counts": {"joint/grp_HFBAIBA_vs_HFSed":  ... [672 more characters]

reasoning: Paper counts: 11 up + 18 down BAIBA vs HF (S3.4.p1). Mir208b (ENSRNOG00000041381) up with BAIBA (Fig 5B) and altered by exercise by qPCR (Supplementary File 2A).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG threshold",
    "paper": "S2.15.p1 |log2FC|>1 & Padj<0.05; S3.4.p1 FC>2 & P<0.05",
    "data": "both computable",
    "disposition": "executable_without_change"
  },
  {
    "item": "comparator of the reported DEG count",
    "paper": "S3.4.p1 text 'BAIBA ... compared to the Sham group'; Fig 5A 'BAIBA vs. HF group'",
    "data": "GEO has distinct Sham operation and HF+Sedentary groups",
    "disposition": "executable_without_change"
  },
  {
    "item": "exercise arm in RNA-seq",
    "paper": "no DEG result reported for exercise",
    "data": "HF+Exercise n=3 deposited",
    "disposition": "executable_without_change"
  },
  {
    "item": "sampling site",
    "paper": "BAIBA group: peri-infarct area; others: anterior LV wall (S2.15.p1)",
    "data": "not recorded in GEO",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID35282369 / GSE193432

**Status: finished.** The case ran on the case-spec route (`case_spec.json`). The decision-contract validator passed: 16 records, 0 errors.

## What ran
- **Data.** `GSE193432_gene_count.txt.gz` holds raw featureCounts integers (rat heart, 34,700 features, 12 samples). There are four groups of n=3: Sham, HF+Sedentary, HF+Exercise and HF+BAIBA. In the matrix, HF+BAIBA is labelled `HFMed`.
- **Alignment.** The key was taken from the GEO title (`Heart, HF+Exe, 1` becomes `HF_Exe_1`) and matched exactly to the matrix columns (`HFExe-1`), ignoring case and punctuation. All 12 samples matched, with no positional alignment. The sex check found all 12 male, as the paper states.
- **Design.** One factor, `grp`, with reference HFSed. The suitability report rated all 6 pairwise comparisons analyzable. Covariance was not required: independent animals and no batch recorded.
- **Method.** DESeq2 (pydeseq2 Wald), the paper's method (S2.15.p1). Three executions:
  - **Primary:** a joint `~ grp` model on all 12 samples, all 6 comparisons.
  - **Sensitivity 1:** pairwise two-arm DESeq2 for HFExe vs HFSed.
  - **Sensitivity 2:** pairwise two-arm DESeq2 for HFBAIBA vs HFSed.
- **Thresholds.**
  - Applied rule: padj < 0.05 and |log2FC| > 1. This is the paper's methods rule (S2.15.p1).
  - Audit rule: raw P < 0.05 and |log2FC| > 1. This is the rule the results section gives next to the counts (S3.4.p1, "FC > 2.0, P < 0.05").

## DEG counts vs the paper (rule: padj < 0.05, |log2FC| > 1)
| Contrast | Ours (up/down) | Paper | Audit, raw P |
|---|---|---|---|
| HF+Exercise vs HF+Sed (primary exercise estimand), joint model | 16 (7/9) | not reported | 349 |
| HF+Exercise vs HF+Sed, pairwise | 20 (9/11) | not reported | 278 |
| HF+BAIBA vs HF+Sed (paper's reported contrast), pairwise | 28 (11/17) | 29 (11/18) | 351 |
| HF+BAIBA vs HF+Sed, joint model | 34 (13/21) | 29 (11/18) | 429 |

The other joint-model comparisons are exploratory:
- Sham vs HFSed: 12
- Sham vs HFExe: 34
- Sham vs HFBAIBA: 34
- HFExe vs HFBAIBA: 152

**Reading the BAIBA row.**
- The pairwise BAIBA run nearly reproduces the paper: 11 up and 17 down, against 11 up and 18 down.
- The paper's counts therefore match the Padj rule. The raw-P rule written in S3.4.p1 would give about 350 DEGs.
- Named gene: Mir208b (ENSRNOG00000041381) goes up with BAIBA in both runs (joint: log2FC 1.76, padj 7e-4; pairwise: log2FC 1.76, padj 1.3e-3). That is the direction the paper reports.
- Under e ... [3448 more characters]
