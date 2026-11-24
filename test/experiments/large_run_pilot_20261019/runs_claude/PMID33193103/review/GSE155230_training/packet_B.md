# Review packet B (the analysis' decisions): GSE155230_training

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.0.group", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pvalues_piled_near_1**: {"table": "training_joint/grp_LRTT_vs_LRT", "frac_p_gt_0.9": 0.2, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}
- **other_rule_matches_paper**: {"table": "training_joint/grp_HRTT_vs_HRT", "paper": 90, "applied": 2, "applied_rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "closest_rule": "pvalue<0.01", "closest_n": 85, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **other_rule_matches_paper**: {"table": "training_joint/grp_HRTT_vs_LRTT", "paper": 255, "applied": 34, "applied_rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "closest_rule": "pvalue<0.01", "closest_n": 257, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.0.group level", "across": "characteristics_ch1.0.group", "pairs_or_sets": 3, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| training_joint/grp_LRTT_vs_LRT | 255 | 8 | padj < 0.05 and |log2FoldChange| > 0.584963 | 8 | 8 | 5 | 18 | 634 | 379 | 201 | 176 | 0.2 | 0.03 |
| training_joint/grp_HRTT_vs_HRT | 90 | 2 | padj < 0.05 and |log2FoldChange| > 0.584963 | 3 | 2 | 1 | 3 | 376 | 178 | 84 | 85 | 0.17 | 0.018 |
| training_joint/grp_HRTT_vs_LRTT | 255 | 34 | padj < 0.05 and |log2FoldChange| > 0.584963 | 35 | 34 | 24 | 49 | 834 | 439 | 222 | 257 | 0.164 | 0.039 |
| training_joint/grp_HRT_vs_LRT | 234 | 20 | padj < 0.05 and |log2FoldChange| > 0.584963 | 23 | 20 | 16 | 49 | 1366 | 463 | 189 | 382 | 0.148 | 0.064 |

## Samples per design level

### `grp`
- **HRT** (3): GSM4697801 / High responder to training 1 / HRT_1; GSM4697802 / High responder to training 2 / HRT_2; GSM4697803 / High responder to training 3 / HRT_3
- **HRTT** (3): GSM4697807 / High responder to training -trained 1 / HRTT_1; GSM4697808 / High responder to training -trained 2 / HRTT_2; GSM4697809 / High responder to training -trained 3 / HRTT_3
- **LRT** (3): GSM4697804 / Low responder to training 1 / LRT_1; GSM4697805 / Low responder to training 2 / LRT_2; GSM4697806 / Low responder to training 3 / LRT_3
- **LRTT** (3): GSM4697810 / Low responder to training -trained 1 / LRTT_1; GSM4697811 / Low responder to training -trained 2 / LRTT_2; GSM4697812 / Low responder to training -trained 3 / LRTT_3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE155230"], "assay": "bulk RNA-seq (Illumina HiSeq 2500, 1x50 bp), rat gastrocnemius", "primary_estimand": "Effect of 8-week treadmill endurance training on gastrocnemius gene expression within each selectively bred trainability line (LRTT vs untrained LRT; HRTT vs untrained HRT), plus the paper's Figure 2 line difference in the trained state (HRTT vs LRTT)", "sample_inclusion": "Generation-15 male HRT/LRT rats; n=3 untrained (HRT, LRT) and n=3 trained (HRTT, LRTT) per line, separate animals (S2.1.3.p1). HCR/LCR samples belong to a separate intrinsic-capacity comparison (case GSE155230_capacity).", "factors": {"line": ["LRT (low responder)", "HRT (high responder)"], "training": ["untrained", "8-wk trained"]}, "planned_contrasts": ["HRTT vs LRTT (S3.2.p1, Fig 2C; paper: 255 DEGs, 68 up in HRTT, 187 down)", "LRTT vs LRT, trained vs untrained low responders (S3.2.p3, Supp Fig 2G; deposited GSE155230_lrtt_lrt_deg: 255 DEGs, 174 up / 81 down)", "HRTT vs HRT, trained vs untrained high responders (S3.2.p3, Supp Fig 2G; deposited GSE155230_hrt_hrtt_deg: 90 DEGs, 62 up / 28 down)", "HRT vs LRT untrained baseline (deposited GSE155230_lrt_hrt_deg: 234 DEGs, 64 up / 170 down; used in Fig 4E pre-training comparison)"], "repeated_measure_unit": "none: trained and untrained rats are different animals (S2.1.3.p1)", "normalization": "Cufflinks upper-quartile normalization, Cuffdiff -b -u (GEO data_processing; S2.3.1.p1)", "paper_method": "TopHat2 -> Cufflinks/Cuffdiff (S2.3. ... [337 more characters]

reasoning: S2.1.3.p1 defines four groups of n=3 male rats (untrained LRT/HRT, trained LRTT/HRTT; separate cohorts, not pre/post on the same animals). S3.2.p3 states the exercise-response analysis compares each trained group to its untrained counterpart; this is the within-line training effect, the estimand closest to 'how exercise affects gene expression'. Fig 2C/S3.2.p1 is the headline HRTT vs LRTT contrast (255 DEGs, FC>1.5, FDR<0.05). Exact paper counts for the training contrasts are not stated in the text, so they are taken from the authors' deposited Cuffdiff lists, all of whose rows pass q<0.05 and |log2FC|>log2(1.5) (HRTT/LRTT list reproduces the text's 255 = 68 up / 187 down exactly).

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\prep\\GSE155230_lrt_hrt_counts_clean.csv", "owned": true, "checks": ["S6.p1 names GSE155230 as the dataset generated for this study", "GEO series has the 18 samples (HCR/LCR/HRT/LRT/HRTT/LRTT x3) matching S2.1.1.p1 and S2.1.3.p1", "GSE155230_lrt_hrt_counts.tsv.gz contains exactly the 12 HRT/HRTT/LRT/LRTT libraries (NG-8752 project, GATC)", "deposited Cuffdiff lists reproduce the paper's 255 and 434 DEG counts"], "accession": "GSE155230", "metadata_file": "test/experiments/large_run_pilot_20261019/runs_claude/PMID33193103/prep/GSE155230_metadata_lane.csv"}

reasoning: Data availability statement S6.p1; sample titles and group labels match the paper's design.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 12, "n_metadata": 18, "coverage": 0.6667, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM4697795", "GSM4697796", "GSM4697797", "GSM4697798", "GSM4697799", "GSM4697800"], "excluded_samples": {"GSM4697795": "HCR sample, not in this matrix; analysed in case GSE155230_capacity", "GSM4697796": "HCR sample, not in this matrix; analysed in case GSE155230_capacity", "GSM4697797": "HCR sample, not in this matrix; analysed in case GSE155230_capacity", "GSM4697798": "LCR sample, not in this matrix; analysed in case GSE155230_capacity", "GSM4697799": "LCR sample, not in this matrix; analysed in case GSE155230_capacity", "GSM4697800": "LCR sample, not in this matrix; analysed in case GSE155230_capacity"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\aligned\\aligned_metadata_kept.csv", "columns": {"grp": {"source": "description", "regex": "^([A-Z]+)_\\d$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\aligned\\design_metadata.csv", "sha256": "5fc6815b484b74aa4c51ae62e60429a854c5d04e90202117bcbda49c0d1057db", "levels": {"grp": {"HRT": 3, "LRT": 3, "HRTT": 3, "LRTT": 3}}}}

reasoning: Prep script renamed BAM-path columns (bam/NG-8752_HRTT_1_lib...bam) to the sample key that GEO stores in `description` (HRTT_1); alignment is an exact match on that column. grp = the line/training code (LRT, LRTT, HRT, HRTT), consistent with characteristics group labels.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\aligned\\aligned_matrix.csv", "sha256": "6ed1de90508801141954f91ec342be017e488a6ebe71395d20768e7bbc717a6c", "n_features": 32882, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3402977.0, "median": 1.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer fraction 1.0, median 1, max 3.4e6; file header is featureCounts v1.6.4 output against Ensembl Rnor_6.0.91 GTF; GEO data_processing: 'Tab delimited text files containing raw counts'. The paper's own input was BAMs into Cuffdiff, which are not deposited.

### design (valid, not_started)

final: {"analysis_type": "multi-group", "design_column": "grp", "estimand_type": "causal for training contrasts (randomly assigned subset trained within line, S2.1.3.p1); associational for line contrasts (selectively bred lines)", "contrasts": [{"name": "grp_LRTT_vs_LRT", "control": "LRT", "treatment": "LRTT", "role": "primary"}, {"name": "grp_HRTT_vs_HRT", "control": "HRT", "treatment": "HRTT", "role": "primary"}, {"name": "grp_HRTT_vs_LRTT", "control": "LRTT", "treatment": "HRTT", "role": "secondary"}, {"name": "grp_HRT_vs_LRT", "control": "LRT", "treatment": "HRT", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: One 4-level grp factor fitted on all 12 samples, with the paper's pairwise contrasts. Training contrasts are the exercise effect; HRTT vs LRTT and HRT vs LRT compare bred lines and are associational.

rejected alternatives: [{"value": "pool trained vs untrained across lines", "reason_rejected": "paper analyses each line's training response separately (S3.2.p3); pooling mixes line-specific responses"}, {"value": "line x training interaction", "reason_rejected": "not tested in the paper; with n=3 per cell it would be exploratory only and is not needed for the paper's estimands"}, {"value": "paired pre/post", "reason_rejected": "trained and untrained rats are separate animals (S2.1.3.p1)"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "lane", "disposition": "not modelled: completely aliased with grp in all four training-case contrasts (HRT L2x3, HRTT L3x3, LRTT L2x3, LRT L3/L1/L1); a sequencing lane inside one GATC run (4266) with libraries prepared in one batch (consecutive lib IDs 99119-99130), not a library-prep batch; its size is checked in the capacity case where it is balanced; recorded as a caveat"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 12, "n_columns": 4, "columns": ["Intercept", "grp_HRTT", "grp_LRT", "grp_LRTT"], "rank": 4, "full_rank": true, "residual_df": 8, "levels": {"grp": {"HRT": 3, "LRT": 3, "HRTT": 3, "LRTT": 3}}, "cells": [{"cell": ["HRT"], "n": 3}, {"cell": ["HRTT"], "n": 3}, {"cell": ["LRT"], "n": 3}, {"cell": ["LRTT"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "lane", "n_levels": 3, "status": "crossed", "crosstab": {"HRT": {"L1": 0, "L2": 3, "L3": 0}, "HRTT": {"L1": 0, "L2": 0, "L3": 3}, "LRT": {"L1": 2, "L2": 0, "L3": 1}, "LRTT": {"L1": 0, "L2": 3, "L3": 0}}}]}

reasoning: Independent animals, no subject blocking; all male (S2.1.3.p1); no batch, age or sex column. Lane (parsed from FASTQ names by prep_counts.py into the metadata copy) is completely aliased with grp for every contrast. Under a strict reading this would stop the case, but lane here is a flow-cell lane of one sequencing run, not a separate library preparation, and technical lane-to-lane variation for RNA-seq is small; the paper's own Cuffdiff results carry the same aliasing. I keep the case and label every training contrast with the caveat; the exploratory lane_check execution in GSE155230_capacity (lane balanced 2:1 within HCR and LCR) measures the lane effect directly.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald), joint model on all 12 samples", "formula": "~ grp", "paper_route": {"method": "Cufflinks/Cuffdiff (upper-quartile, bias-corrected) on TopHat2 BAMs", "status": "blocked", "reason": "BAM/FASTQ-level transcript quantification is not deposited in GEO; only featureCounts gene counts are available"}, "deviations": ["DESeq2 on featureCounts gene counts instead of Cuffdiff on BAMs; GEO data_processing says normalized counts were obtained with featureCounts and DESeq2, so DESeq2 is the authors' own count route"]}

reasoning: Raw counts support DESeq2; Cuffdiff cannot be reproduced from deposited files.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper rule (FC > 1.5, FDR/q < 0.05) applied to DESeq2 BH-adjusted p instead of Cuffdiff q."}

reasoning: S3.2.p1 and S3.1.p1: fold change > 1.5 and FDR (q) < 0.05; log2(1.5) = 0.5849625.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "training_joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\training_joint\\DEG_results_grp_LRTT_vs_LRT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\training_joint\\DEG_results_grp_HRTT_vs_HRT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\training_joint\\DEG_results_grp_HRTT_vs_LRTT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\training_joint\\DEG_results_grp_HRT_vs_LRT.csv"], "counts": {"training_joint/grp_LRTT_vs_LRT": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 17991, "n_significant": 8, "n_up": 4, "n_down": 4, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17991, "n_significant": 8, "n_up": 4, "n_down": 4, "deg_sanity": "ok"}}, "training_joint/grp_HRTT_vs_HRT": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 21300, "n_significant": 2, "n_up": 1, "n_down": 1, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 21300, "n_significant": 3, "n_up": ... [658 more characters]

reasoning: One DESeq2 model on all 12 HRT/LRT-line samples; training effect per line plus the paper's line contrasts.

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "training_joint/grp_LRTT_vs_LRT", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\enrichment_training_joint_grp_LRTT_vs_LRT\\ora\\DEG_results_grp_LRTT_vs_LRT_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\enrichment_training_joint_grp_LRTT_vs_LRT\\ora\\DEG_results_grp_LRTT_vs_LRT_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\enrichment_training_joint_grp_LRTT_vs_LRT\\ora\\DEG_results_grp_LRTT_vs_LRT_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\enrichment_training_joint_grp_LRTT_vs_LRT\\ora\\DEG_results_grp_LRTT_vs_LRT_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 6 Rat genes (dir ... [1453 more characters]

reasoning: paper reports GO terms for low-responder training genes (S3.2.p3)

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "training_joint/grp_LRTT_vs_LRT", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\enrichment_training_joint_grp_LRTT_vs_LRT\\gsea\\DEG_results_grp_LRTT_vs_LRT_GSEA_Hallmark.csv"], "summary": "GSEA complete on 16507 Rat genes ranked by 'stat'. 50 Hallmark sets tested, 17 significant at FDR q < 0.25. Rat genes matched to mouse Hallmark by symbol: 3846/4291 Hallmark genes present in the ranking. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.71 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.79 | NOM p=0.00e+00 | FDR q=4.59e-03 - HALLMARK_MTORC1_SIGNALING | NES=1.78 | NOM p=0.00e+00 | FDR q=4.20e-03 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.78 | NOM p=0.00e+00 | FDR q=3.93e-03 - HALLMARK_ANGIOGENESIS | NES=1.73 | NOM p=3.57e-03 | FDR q=4.44e-03 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.69 | NOM p ... [568 more characters]

reasoning: paper reports GO terms for low-responder training genes (S3.2.p3)

### enrichment (valid, failed)

final: {"organism": "Rat", "subset": "training_joint/grp_HRTT_vs_HRT", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "execution_error": "Only 2 valid genes after filtering / ID conversion. Enrichment requires at least ~5 genes for meaningful results."}

reasoning: paper reports GO terms for high-responder training genes (S3.2.p3)

### enrichment (valid, completed)

final: {"organism": "Rat", "subset": "training_joint/grp_HRTT_vs_HRT", "ortholog_mapping": "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); overlap reported by the tool", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33193103\\GSE155230_training\\results\\enrichment_training_joint_grp_HRTT_vs_HRT\\gsea\\DEG_results_grp_HRTT_vs_HRT_GSEA_Hallmark.csv"], "summary": "GSEA complete on 16507 Rat genes ranked by 'stat'. 50 Hallmark sets tested, 20 significant at FDR q < 0.25. Rat genes matched to mouse Hallmark by symbol: 3846/4291 Hallmark genes present in the ranking. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_KRAS_SIGNALING_DN | NES=1.89 | NOM p=0.00e+00 | FDR q=2.26e-03 - HALLMARK_MYOGENESIS | NES=1.84 | NOM p=0.00e+00 | FDR q=1.88e-03 - HALLMARK_TGF_BETA_SIGNALING | NES=1.39 | NOM p=6.55e-02 | FDR q=1.34e-01 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.35 | NOM p=5.15e-02 | FDR q=1.42e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.25 | NOM p=1.35e-01 | FDR q=2.85e-01 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.23 | NOM p=7.10e-02 | FDR q=2.69e-01 - HALLMARK_MITOTIC_SPINDLE | NES=1.20 | NOM p=7.26e-02 | FDR q=2.79e-01 - HALLMARK_P53_PATHWAY | NES=1.19 | NOM p=1.15e-01 | FDR q=2.71e-01 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.13 | NOM p=2.61e-01 | FDR q=3.73e-01 - HALLMA ... [568 more characters]

reasoning: paper reports GO terms for high-responder training genes (S3.2.p3)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Trained vs untrained are different animals (n=3 each); training effect is between-animal.", "Sequencing lane is completely aliased with group in every training contrast (HRT/LRTT lane 2, HRTT lane 3, LRT lanes 1/3) and could not be modelled; see lane_check in GSE155230_capacity for the size of the lane effect.", "Paper counts for the training contrasts come from the authors' deposited Cuffdiff lists, not from the article text.", "Lane check (capacity case, L3 vs L1, ~grp+lane): 36 lane DEGs. Overlap with training-case DEG sets is 0 (LRTT vs LRT), 0 (HRTT vs HRT), 1 (HRTT vs LRTT), 1 (HRT vs LRT), but lane-DEG log2FC correlate with the lane effect at r=0.59/0.41/-0.47/-0.17 in those contrasts, so a lane or processing-order contribution cannot be excluded.", "Paper-named gene directions in HRTT vs LRTT agree with S3.2.p1 (Sln, Adcy1, Kcna10, Lgi3 up; Rcan3, Wnt16, Vat1l, Myh6 down; Per1/Bhlhe40/Dbp higher and Nfil3 lower in LRTT); only Lgi3 passes padj<0.05."], "results": {"training_joint/grp_LRTT_vs_LRT": {"n_deg": 8, "up": 4, "down": 4, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 8}, "training_joint/grp_HRTT_vs_HRT": {"n_deg": 2, "up": 1, "down": 1, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 3}, "training_joint/grp_HRTT_vs_LRTT": {"n_deg": 34, "up": 18, "down": 16, "rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "audit_n": 35}, "training_joint/grp_HRT_vs_LRT": {"n_deg": 20, "up":  ... [1902 more characters]

reasoning: Paper's Cuffdiff route is blocked; DESeq2 runs as a declared deviation with the paper threshold. Gene directions per S3.2.p1: Sln, Adcy1, Kcna10, Lgi3 up in HRTT; Rcan3, Wnt16, Vat1l, Myh6 up in LRTT; Per1/Bhlhe40/Dbp induced and Nfil3 repressed in the low-response signature.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "Cuffdiff on TopHat2 BAMs (S2.3.1.p1)",
    "data": "featureCounts raw gene counts only",
    "disposition": "declared_deviation"
  },
  {
    "item": "Training DEG counts",
    "paper": "not stated in text (only n=193 unique low-response genes, S3.2.p3)",
    "data": "deposited Cuffdiff lists: LRTT/LRT 255, HRTT/HRT 90",
    "disposition": "executable_without_change"
  },
  {
    "item": "S2.1.2.p1 defines response as DIST1 - DIST2",
    "paper": "sign appears reversed (post minus pre intended)",
    "data": "no effect on transcriptome contrasts",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID33193103 / GSE155230

Paper: Comparative Analysis of Skeletal Muscle Transcriptional Signatures Associated With Aerobic Exercise Capacity or Response to Training in Humans and Rats (PMC7649134).
Decision maker: Claude Opus 5.5 session. Route: case spec (`case_spec.json`) → `python -m tools.case_runner execute`. Run status: **completed**. Contract validator: 25 records, 0 errors.

## What ran

The data are 18 rat gastrocnemius bulk RNA-seq samples, all male, n=3 per group. The paper's own route (TopHat2 → Cufflinks/Cuffdiff on BAMs, S2.3.1.p1) is blocked because only featureCounts gene counts were deposited. Every table below is therefore a **declared deviation**: DESeq2 (pydeseq2 Wald) on raw counts, using the paper's threshold.

**Threshold (paper, S3.1.p1 / S3.2.p1):** fold change > 1.5 and FDR/q < 0.05, applied as `padj < 0.05 & |log2FC| > 0.5849625`. The source is recorded as `paper_on_deviation_route`. An audit rule (padj < 0.05, no fold-change cutoff) is also recorded.

**Case `GSE155230_training`** (exercise estimand, 12 samples): one joint model `~ grp` with 4 levels (LRT, LRTT, HRT, HRTT). Trained and untrained rats are separate animals (S2.1.3.p1), so the design is unpaired.
- Training effect: `grp_LRTT_vs_LRT` and `grp_HRTT_vs_HRT` (primary, S3.2.p3). These are causal within each line.
- `grp_HRTT_vs_LRTT` (Fig 2C headline) and `grp_HRT_vs_LRT` (untrained baseline) are secondary. They compare selectively bred lines, so they are associational.

**Case `GSE155230_capacity`** (6 samples): `hcr_vs_lcr`, untrained HCR vs LCR (Fig 1C). This is associational intrinsic capacity, not an exercise effect. It also holds an exploratory `lane_check` model (L3 vs L1, `~ grp + lane`).

### Paper counts

The text gives counts only for HCR/LCR (434) and HRTT/LRTT (255). The training-contrast counts come from the authors' deposited Cuffdiff lists (`GSE155230_*_deg.csv.gz`). Under the paper rule those lists reproduce the text exactly: 434 = 257/177 and 255 = 68/187.

| table | ours n (up/down) | paper n (up/down) | audit n (padj<0.05) |
|---|---|---|---|
| training_joint/grp_LRTT_vs_LRT | 8 (4/4) | 255 (174/81), deposited list | 8 |
| training_joint/grp_HRTT_vs_HRT | 2 (1/1) | 90 (62/28), deposited list | 3 |
| training_joint/grp_HRTT_vs_LRTT | 34 (18/16) | 255 (68/187), S3.2.p1 | 35 |
| training_joint/grp_HRT_vs_LRT | 20 (9/11) | 234 (64/170), deposited list | 23 |
| hcr_vs_lcr | 81 (46/35) | 434 (257/177), S3.1.p1 | 81 |

Our counts are 3–45× lowe ... [5521 more characters]
