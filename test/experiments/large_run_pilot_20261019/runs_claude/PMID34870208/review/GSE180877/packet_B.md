# Review packet B (the analysis' decisions): GSE180877

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pair_PoW6_vs_UT6 | 297 | 298 | padj < 0.05 | 298 | 154 | 42 | 528 | 1897 | 535 | 121 | 796 | 0.072 | 0.155 |

## Samples per design level

### `grp`
- **DT9** (3): GSM5474101 / 9M PoW+DT1 [DT6]; GSM5474102 / 9M PoW+DT2 [DT7]; GSM5474103 / 9M PoW+DT3 [DT8]
- **PoW6** (6): GSM5474095 / 6M PoW1 [PoW13]; GSM5474096 / 6M PoW2 [PoW15]; GSM5474097 / 6M PoW3 [PoW16]; GSM5556584 / 6M POW4 [LD1]; GSM5556585 / 6M POW5 [LD2]; GSM5556586 / 6M POW6 [LD3]
- **UT6** (3): GSM5474092 / 6M UT1 [PoW3]; GSM5474093 / 6M UT2 [PoW12]; GSM5474094 / 6M UT3 [PoW17]
- **UT9** (3): GSM5474098 / 9M UT1 [DT2]; GSM5474099 / 9M UT2 [DT3]; GSM5474100 / 9M UT3 [DT4]

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE180877"], "other_accessions_not_analyzed": {"GSE180433": "RRBS methylation (nucleus-sorted); not gene expression, outside this request"}, "assay": "bulk RNA-seq of whole plantaris muscle, male HSA-GFP mice (S2.5.p1, S4.p2, S4.p3)", "factors": {"group": ["6M UT (untrained, 6 mo)", "6M PoW (8 wk PoWeR, 6 mo)", "9M UT (untrained, 9 mo)", "9M PoW+DT (8 wk PoWeR + 12 wk detraining, 9 mo)"]}, "sample_inclusion": "biological triplicate per group (S4.p2); RNA-seq on the same muscles used for RRBS (S2.5.p1)", "primary_estimand": "effect of 8 wk PoWeR training on whole-muscle gene expression vs age-matched untrained (6M PoW vs 6M UT)", "planned_contrasts": ["6M PoW vs 6M UT (S2.5.p1; paper: 179 up + 118 down = 297 DEGs at FDR < 0.05)", "9M PoW+DT vs 9M UT (S2.5.p1; paper: no PoWeR-altered gene remained DE after detraining; total count not reported)"], "repeated_measure_unit": "none; independent mice per group", "normalization": "Partek Flow: STAR mm10, gene counts, genes with max count <= 50 removed, median-ratio normalization (S4.p3; GEO data_processing)", "paper_method": "DESeq/DESeq2 in Partek Flow with FDR step-up (S4.p3; GEO data_processing)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.5.p1; S4.1.p1"}, "paper_results": {"6M PoW vs 6M UT": {"up": 179, "down": 118, "total": 297, "enrichment": "ECM-related processes up, SMAD signaling genes down (Figure S2)"}, "9M PoW+DT vs 9M UT": "no P ... [31 more characters]

reasoning: DA.p1 names GSE180877 as the RNA-seq deposit. S2.5.p1 gives the PoWeR transcriptome result (179 up / 118 down, FDR<0.05) and the detraining persistence check. S4.p3 states Partek, min read cutoff 50, mm10, DESeq with FDR step-up. S4.1.p1 controls FDR<0.05 for all sequencing; no fold-change rule. S4.p2 says biological triplicate per group.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\input\\matrix_feature_ids.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 34870208", "paper DA.p1 names GSE180877 (RNA-seq)", "series title equals the paper title", "single supplementary matrix GSE180877_Raw_gene_counts_matrix.txt.gz covers all 15 GSMs"], "accession": "GSE180877", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE180877\\GSE180877_metadata.csv"}

reasoning: Series is linked to the PMID and named in the data availability statement; the matrix column names follow the paper's group labels (6M UT, 6M PoW, 9M UT, 9M PoW+DT).

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 15, "n_metadata": 15, "coverage": 1.0, "unmatched_matrix_columns": ["chromosome", "start", "stop"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^\\d+M (UT|PoW\\+DT|PoW|POW)\\d+ \\[([A-Za-z]+)\\d+\\]$", "recode": {"UT_PoW": "UT6", "PoW_PoW": "PoW6", "POW_LD": "PoW6", "UT_DT": "UT9", "PoW+DT_DT": "DT9"}}, "grpx": {"source": "title", "regex": "^\\d+M (UT|PoW\\+DT|PoW|POW)\\d+ \\[([A-Za-z]+)\\d+\\]$", "recode": {"UT_PoW": "UT6", "PoW_PoW": "PoW6", "POW_LD": "LD6", "UT_DT": "UT9", "PoW+DT_DT": "DT9"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\aligned\\design_metadata.csv", "sha256": "d9356b031330baee2b93d077688905bcf5a34443fb13ab9e106782dc8713c97c", "levels": {"grp": {"PoW6": 6, "UT6": 3, "UT9": 3, "DT9": 3}, "grpx": {"UT6": 3, "PoW6": 3, "UT9": 3, "DT9": 3, "LD6": 3}}}}

reasoning: Matrix columns ('6M UT 1', '9M PoW+DT 1', '6M PoW 4') equal the GEO title prefix before the bracketed mouse ID ('6M UT1 [PoW3]', '9M PoW+DT1 [DT6]', '6M POW4 [LD1]') after ignoring case and spaces; key derived from title, exact normalized match, no positional alignment. Group labels come from the title, which agrees with the matrix headers and the paper's group names. characteristics_ch1.1.treatment is unreliable: it labels 9M UT 'Detrained' and 9M PoW+DT 'Sedentary' (swapped), and 6M POW4-6 'Sedentary'. The three later-deposited samples 6M POW4-6 [LD1-3] (Sep 03 2021) are PoW by title and by matrix header ('6M PoW 4-6'), and trained-like on ECM markers (Col3a1 CPM 72/103/81 vs UT 25/44/48), ... [97 more characters]

rejected alternatives: [{"value": "characteristics_ch1.1.treatment as group", "reason_rejected": "contradicts title and matrix headers for all 9M samples and for 6M POW4-6"}, {"value": "exclude 6M POW4-6 [LD] (paper S4.p2 says triplicates)", "reason_rejected": "title + matrix header both say PoW; S4.p2 triplicate statement describes the RRBS mice; first attempt (see _previous) showed the 6-vs-3 fit reproduces the paper's 179/118 almost exactly (180/118) while 3-vs-3 gives 61/34, so the paper's RNA-seq used n=6 PoW. Ke ... [21 more characters]

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts (Partek Flow gene-level quantification; non-integer values)", "recommended_method": "DESeq2 on rounded estimated counts", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\aligned\\aligned_matrix.csv", "sha256": "2eb19cf3c3e31458a00c4fa7190a224d8da559ca20777b0f4a9f5d40fc321449", "n_features": 20406, "n_samples": 15, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2100000.0, "median": 72.0, "integer_fraction": 0.7107, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: STAR to mm10, 'quantified for gene counts', median-ratio normalized and tested with DESeq2; supplementary file described as raw gene counts. Profile: 71% integers, values like 11.0147 and 2.56E-07 (EM-style fractional assignment), column sums 19-28 M reads, max 2.1e6, no negatives - count scale, not FPKM/TPM. The paper's input is the same count matrix (S4.p3). Rounding to integers for DESeq2 is the standard treatment of estimated counts.

### design (valid, not_started)

final: {"analysis_type": "multi-group, planned age-matched contrasts", "design_column": "grp", "contrasts": [{"name": "grp_PoW6_vs_UT6", "control": "UT6", "treatment": "PoW6", "role": "primary"}, {"name": "grp_DT9_vs_UT9", "control": "UT9", "treatment": "DT9", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: S2.p1/S2.5.p1: each trained group is compared with its age-matched untrained control (6M PoW vs 6M UT; 9M PoW+DT vs 9M UT). Cross-age comparisons are not sensible estimands and are not run. 6M PoW arm = 6 mice (PoW1-3 + POW4-6 [LD]) by title/matrix header; 6M UT, 9M UT, 9M PoW+DT = 3 each. Re-decided after attempt 1: the triplicate-only primary gave 64/55 (joint) and 61/34 (pair) vs paper 179/118, the pooled run gave 180/118; this, plus the label evidence, identifies the paper's sample set. Estimand is causal (training vs untrained age-matched mice).

rejected alternatives: [{"value": "6M PoW triplicate only (exclude LD)", "reason_rejected": "does not match the paper's sample set; run as sensitivity"}, {"value": "2x2 factorial age x training with interaction", "reason_rejected": "detrained is not the same treatment as trained; the paper only asks age-matched contrasts"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 15, "n_columns": 4, "columns": ["Intercept", "grp_PoW6", "grp_UT6", "grp_UT9"], "rank": 4, "full_rank": true, "residual_df": 11, "levels": {"grp": {"PoW6": 6, "UT6": 3, "UT9": 3, "DT9": 3}}, "cells": [{"cell": ["DT9"], "n": 3}, {"cell": ["PoW6"], "n": 6}, {"cell": ["UT6"], "n": 3}, {"cell": ["UT9"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "submission_date", "n_levels": 2, "status": "crossed", "crosstab": {"DT9": {"Jul 26 2021": 3, "Sep 03 2021": 0}, "PoW6": {"Jul 26 2021": 3, "Sep 03 2021": 3}, "UT6": {"Jul 26 2021": 3, "Sep 03 2021": 0}, "UT9": {"Jul 26 2021": 3, "Sep 03 2021": 0}}}]}

reasoning: Independent mice, one muscle each; no repeated measures; all male. The only recorded batch-like variable is the deposit date: the 3 LD mice (Sep 2021 deposit) all sit in the PoW6 arm together with 3 Jul-deposit PoW mice, so deposit is not aliased with treatment, but it may mark a sequencing batch inside the PoW arm. A deposit term would be estimated only from within the PoW arm and the paper adjusts for nothing, so it is not added; the triplicate-only fit is run as sensitivity instead. Age is handled by within-age contrasts.

### method (valid, not_started)

final: {"matrix_type": "estimated counts (Partek Flow gene-level quantification; non-integer values)", "method": "DESeq2 (pydeseq2 Wald) on rounded estimated counts, two-arm fit per age-matched contrast", "formula": "~ grp", "rounding_documented": true, "paper_route": {"method": "DESeq2 in Partek Flow, genes with max count <= 50 removed, median-ratio normalization, FDR step-up", "status": "reproduced_with_minor_differences"}, "deviations": ["pydeseq2 instead of Partek Flow's DESeq2 implementation", "fractional estimated counts rounded to integers before DESeq2", "low-count filter 'max count > 50' applied within each execution's samples", "Partek model scope not stated; two-arm fits are primary (they match the paper's counts), a single 5-sample-group model is run as sensitivity"], "transform": "round"}

reasoning: Matrix supports the paper's count route. Filter reproduces GEO data_processing 'maximum count of less than or equal to 50' excluded (implemented as count >= 50.0001 in at least 1 sample, i.e. max > 50, on unrounded values).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}}

reasoning: S2.5.p1 and S4.1.p1: FDR (BH-adjusted p) < 0.05, no fold-change rule. Audit rule adds |FC| > 1.5 (log2 0.5849625) for reference only.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pair_PoW6_vs_UT6", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\pair_PoW6_vs_UT6\\input\\rounded_counts.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\pair_PoW6_vs_UT6\\DEG_results_PoW6_vs_UT6.csv"], "counts": {"pair_PoW6_vs_UT6": {"applied": {"rule": "padj < 0.05", "n_tested": 12212, "n_significant": 298, "n_up": 180, "n_down": 118, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12212, "n_significant": 154, "n_up": 114, "n_down": 40, "deg_sanity": "ok"}}}}

reasoning: Paper's PoWeR contrast: 6 PoW vs 3 UT, DESeq2, max-count>50 filter.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pair_DT9_vs_UT9", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\pair_DT9_vs_UT9\\input\\rounded_counts.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\pair_DT9_vs_UT9\\DEG_results_DT9_vs_UT9.csv"], "counts": {"pair_DT9_vs_UT9": {"applied": {"rule": "padj < 0.05", "n_tested": 11653, "n_significant": 66, "n_up": 11, "n_down": 55, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 11653, "n_significant": 56, "n_up": 11, "n_down": 45, "deg_sanity": "ok"}}}}

reasoning: Paper's detraining contrast, 3 vs 3.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint_all", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 15, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\joint_all\\input\\rounded_counts.csv", "transform": "round", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\joint_all\\DEG_results_grp_PoW6_vs_UT6.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\joint_all\\DEG_results_grp_DT9_vs_UT9.csv"], "counts": {"joint_all/grp_PoW6_vs_UT6": {"applied": {"rule": "padj < 0.05", "n_tested": 12290, "n_significant": 386, "n_up": 215, "n_down": 171, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12290, "n_significant": 175, "n_up": 127, "n_down": 48, "deg_sanity": "ok"}}, "joint_all/grp_DT9_vs_UT9": {"applied": {"rule": "padj < 0.05", "n_tested": 12290, "n_significant": 19, "n_up": 2, "n_down": 17, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12290, "n_significant": 19, "n_up": 2, "n_down": 17, "deg_sanity": "ok"}}}}

reasoning: One model ~ grp over all 15 samples, in case Partek fitted all groups together.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "triplicate_PoW6_vs_UT6", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\triplicate_PoW6_vs_UT6\\input\\rounded_counts.csv", "transform": "round", "formula": "~ grpx", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\triplicate_PoW6_vs_UT6\\DEG_results_PoW6_vs_UT6.csv"], "counts": {"triplicate_PoW6_vs_UT6": {"applied": {"rule": "padj < 0.05", "n_tested": 12015, "n_significant": 95, "n_up": 61, "n_down": 34, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12015, "n_significant": 68, "n_up": 44, "n_down": 24, "deg_sanity": "ok"}}}}

reasoning: Original Jul-deposit triplicate only (3 vs 3), matching S4.p2's triplicate statement.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "pair_PoW6_vs_UT6", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\enrichment_pair_PoW6_vs_UT6\\ora\\DEG_results_PoW6_vs_UT6_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\enrichment_pair_PoW6_vs_UT6\\ora\\DEG_results_PoW6_vs_UT6_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\enrichment_pair_PoW6_vs_UT6\\ora\\DEG_results_PoW6_vs_UT6_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\enrichment_pair_PoW6_vs_UT6\\ora\\DEG_results_PoW6_vs_UT6_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 298 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Extracellular Matrix Organization (GO:0030198) | padj=2.32e-06 | overlap=17/176 | genes=COL15A1;ECM2;LUM;MMP2;LOXL2;COL1A1;SMOC2;COL3A1;BMP1;COL1A2;COL4 ... [1187 more characters]

reasoning: Paper reports pathway enrichment of the PoWeR transcriptome (ECM up, SMAD signaling down; Figure S2).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "pair_PoW6_vs_UT6", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34870208\\GSE180877\\results\\enrichment_pair_PoW6_vs_UT6\\gsea\\DEG_results_PoW6_vs_UT6_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12226 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 35 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.61 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.42 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_KRAS_SIGNALING_UP | NES=2.26 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.15 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=2.08 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.05 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.95 | NOM p=0.00e+00 | FDR q=3.10e-04 - HALLMARK_COMPLEMENT | NES=1.87 | NOM p=0.00e+00 | FDR q=1.24e-03 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.87 | NOM p=0.00e+00 | FDR q=1.24e-03 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=-1.98 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=-1.93 | NOM p=0.00e+00 | FDR q=9 ... [388 more characters]

reasoning: Paper reports pathway enrichment of the PoWeR transcriptome (ECM up, SMAD signaling down; Figure S2).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["GEO characteristics 'treatment' is inconsistent with titles/matrix headers; groups taken from titles", "6M PoW arm includes 3 later-deposited mice (POW4-6 [LD]); the paper's 'biological triplicate per group' (S4.p2) does not hold for its RNA-seq PoW arm; the sample-set decision was revised after the first attempt", "paper gives no total DEG count for 9M PoW+DT vs 9M UT; its claim is only that no PoWeR-altered gene stayed DE", "Persistence check: of our 298 PoWeR DEGs, one (Dusp7) is also DE in 9M PoW+DT vs 9M UT (FDR<0.05) but with opposite sign (log2FC -0.64 trained, +0.91 detrained), so no change persists in the same direction; strictly, the paper's 'no genes altered by PoWeR remained differentially expressed' has this one opposite-sign exception in our fit."], "results": {"pair_PoW6_vs_UT6": {"n_deg": 298, "up": 180, "down": 118, "rule": "padj < 0.05", "audit_n": 154}, "pair_DT9_vs_UT9": {"n_deg": 66, "up": 11, "down": 55, "rule": "padj < 0.05", "audit_n": 56}, "joint_all/grp_PoW6_vs_UT6": {"n_deg": 386, "up": 215, "down": 171, "rule": "padj < 0.05", "audit_n": 175}, "joint_all/grp_DT9_vs_UT9": {"n_deg": 19, "up": 2, "down": 17, "rule": "padj < 0.05", "audit_n": 19}, "triplicate_PoW6_vs_UT6": {"n_deg": 95, "up": 61, "down": 34, "rule": "padj < 0.05", "audit_n": 68}}, "paper_counts": {"pair_PoW6_vs_UT6": 297}, "comparison": {"pair_PoW6_vs_UT6": {"ours": 298, "paper": 297}}, "paper_gene_check": {}}

reasoning: Primary reproduces the paper's estimand, sample set (as identified from labels and counts), method family and threshold; differences are implementation-level.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "GEO treatment characteristic",
    "paper": "9M UT = untrained, 9M PoW+DT = trained then detrained",
    "data": "characteristics_ch1.1.treatment: 9M UT samples 'Detrained', 9M PoW+DT samples 'Sedentary', 6M POW4-6 'Sedentary'",
    "disposition": "executable_without_change"
  },
  {
    "item": "sample count",
    "paper": "biological triplicate per group (S4.p2)",
    "data": "6M PoW arm has 6 RNA-seq samples (PoW1-3 + POW4-6 [LD1-3], deposited Sep 03 2021); other arms 3",
    "disposition": "executable_without_change"
  },
  {
    "item": "detraining DEG count",
    "paper": "no PoWeR-altered genes remained DE (no total)",
    "data": "computed count reported without a paper number",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID34870208 / GSE180877

## What ran
- Case-spec route (`tools.case_runner execute case_spec.json`). There were three re-executions; earlier attempts are under `_previous/`. The contract validator passed with 15 records and 0 errors.
- Data: GSE180877 is whole-plantaris RNA-seq. The matrix is `GSE180877_Raw_gene_counts_matrix.txt.gz`: 20406 genes x 15 samples of Partek estimated counts, with feature IDs taken from `Gene Symbol`. The companion RRBS series GSE180433 was not analyzed because it is methylation, not expression.
- Alignment: each sample's key is its GEO title before the `[mouse id]`. Keys were matched to the matrix headers after normalization: 15/15 exact, no positional matching. Groups also come from the title.
- Method: DESeq2 (pydeseq2 Wald) on rounded estimated counts, with the paper's low-count filter (drop genes whose max count is <= 50). Threshold: padj < 0.05 with no fold-change cutoff, as the paper states (S2.5.p1, S4.1.p1).
- Enrichment ran on the primary contrast. ORA top terms are collagen-containing ECM and ECM organization. GSEA Hallmark top hits are EMT, coagulation and angiogenesis (up). Both agree with the paper's "ECM-related processes" (S2.5.p1).

## DEG counts vs paper (padj < 0.05, no FC cutoff)
| Table | Role | Ours (up/down) | Paper |
|---|---|---|---|
| pair_PoW6_vs_UT6 (6 PoW vs 3 UT) | primary | 298 (180/118) | 297 (179/118) |
| pair_DT9_vs_UT9 (3 vs 3) | secondary | 66 (11/55) | no total given; paper says no PoWeR gene persisted |
| joint_all/grp_PoW6_vs_UT6 (one model, 15 samples) | sensitivity | 386 (215/171) | - |
| joint_all/grp_DT9_vs_UT9 | sensitivity | 19 (2/17) | - |
| triplicate_PoW6_vs_UT6 (3 vs 3, July deposit only) | sensitivity | 95 (61/34) | - |

Persistence: of the 298 PoWeR DEGs, only Dusp7 is also DE after detraining, and its sign is opposite (-0.64 trained, +0.91 detrained). No gene persists in the same direction. This is recorded in the study caveats.

## Deviations and decisions
- The GEO `characteristics: treatment` field is unreliable. It calls 9M UT "Detrained", 9M PoW+DT "Sedentary", and 6M POW4-6 "Sedentary". Groups were taken from the titles, which agree with the matrix headers and with the paper.
- The 6M PoW arm has 6 samples: PoW1-3 plus POW4-6 [LD1-3], which were deposited on Sep 03 2021. The paper says "biological triplicate per group" (S4.p2). My first attempt excluded the LD samples, which gave 95 (61/34) DEGs. I revised the decision because the title and the matrix header  ... [1155 more characters]
