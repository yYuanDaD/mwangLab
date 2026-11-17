# Review packet B (the analysis' decisions): GSE257540_biochem

## Mechanical flags

- none

## Samples per design level

### `grp`
- **C** (5): GSM8107914 / C1; GSM8107915 / C2; GSM8107916 / C3; GSM8107918 / C5; GSM8107919 / C6
- **EX** (4): GSM8107920 / HI1; GSM8107921 / HI2; GSM8107922 / HI3; GSM8107925 / HI6
- **SP** (5): GSM8107908 / LI1; GSM8107909 / LI2; GSM8107910 / LI3; GSM8107911 / LI4; GSM8107912 / LI5

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE257540", "GSE281241"], "primary_estimand": "Transcriptomic effect on HB9::GFP mESC-derived motor neuron spheroids of (a) biochemical stimulation with conditioned medium from optogenetically exercised C2C12 muscle (1 Hz light, 30 min/day) or from spontaneously twitching (unstimulated) muscle, versus unconditioned control medium, and (b) mechanical stimulation by magnetic matrix actuation (MagMA) versus non-actuated MagMA controls (S2.4.p1-p4, FIG7, S4.6, S4.7).", "planned_contrasts": ["Exercise CM vs Control (FIG7c; S2.4.p3)", "Spontaneous-twitch CM vs Control (FIG7d)", "Exercise CM vs Spontaneous-twitch CM (FIG7e)", "Mechanical stimulation vs mechanical control (FIG7i; S2.4.p4: only 2 significant hits, both up)"], "paper_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": "not_reported", "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "FIG7 legend; S4.10.p1"}, "factors": {"biochemical": ["Control", "Spontaneous twitch CM (GEO: Low intensity biochem, NE1-6)", "Exercise CM (GEO: High intensity biochem, S1-6)"], "mechanical": ["Mechanical control (MC1-4)", "Mechanical stimulation (M1-4)"]}, "sample_inclusion": "QC exclusion of samples with <500K reads, rRNA >20% or exon/intron ratio <10 (n = 5, S4.10.p1); final n: control 5, spontaneous 4, exercise 4 (FIG7a); mechanical control 3, mechanical 4 (FIG7i)", "repeated_measure_unit": "not_reported (independent spheroid wells; no pairing described)", "normalization": "DESeq2 size ... [772 more characters]

reasoning: Built from S2.4.p1-p5, FIG7 legend, S4.6-S4.11 and DA.p1. Paper's DE threshold is BH-adjusted p with no stated numeric cutoff or fold-change rule (FIG7 legend: p-values used to determine DEGs were Benjamini-Hochberg adjusted).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE257540\\GSE257540_expression_data_counts.tsv.txt.gz", "owned": true, "checks": ["S4.8.p2 and DA.p1 cite GSE257540", "GEO Series_pubmed_id 39523700", "26 GSMs = HB9::GFP motor neuron spheroids with treatment labels matching the paper's 5 arms", "matrix columns C/L/H/M/MC map 1:1 to GSM titles C/LI/HI/M/MC"], "accession": "GSE257540", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE257540\\GSE257540_metadata.csv"}

reasoning: Paper names GSE257540 as its RNA-seq deposit; samples and arms match FIG7.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 26, "n_metadata": 26, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM8107917": "QC (S4.10.p1): rRNA fraction 0.78 of counts (>20%)", "GSM8107913": "QC (S4.10.p1): 1,536 assigned reads (<500K)", "GSM8107923": "QC (S4.10.p1): 243,510 assigned reads (<500K)", "GSM8107924": "QC (S4.10.p1): 495,044 assigned reads (<500K)", "GSM8107906": "QC (S4.10.p1): 613K reads, 10x below other mechanical libraries, with 31.7K detected genes (highest of all samples), consistent with the low exon/intron coverage criterion; paper keeps 3 mechanical controls (FIG7i)", "GSM8107900": "mechanical-stimulation experiment with its own controls, analyzed in case GSE257540_mech (paper analyzes the two experiments separately, FIG7a vs FIG7i)", "GSM8107901": "mechanical-stimulation experiment with its own controls, analyzed in case GSE257540_mech (paper analyzes the two experiments separately, FIG7a vs FIG7i)", "GSM8107902": "mechanical-stimulation experiment with its own controls, analyzed in case GSE257540_mech (paper analyzes the two experiments separately, FIG7a vs FIG7i)", "GSM8107903": "mechanical-stimulation experiment with its own controls, analyzed in case GSE257540_mech (paper analyzes the two experiments separately, FIG7a vs FIG7i)", "GSM8107904": "mechanical-stimulation experiment with its own controls, analyzed in case GSE257540_mech (paper analyzes the two experiments separately, FIG7a vs FIG ... [1013 more characters]

reasoning: Matrix columns abbreviate titles (L1 = LI1, H1 = HI1). key_patterns strips the I and normalize_keys matches L_1 to L1; exact otherwise, never positional. GEO Low intensity biochem = NE1-6 (media from unstimulated, spontaneously twitching optogenetic muscle) and High intensity biochem = S1-6 (media from optically stimulated, exercised muscle) per Series_overall_design, recoded SP and EX. QC exclusions follow S4.10.p1 criteria computed from the deposited counts. FIG7a reports 4 spontaneous replicates; only LI6 fails a criterion computable from the counts, so 5 SP samples are kept (see discrepancies).

### matrix (valid, not_started)

final: {"source": "GSE257540_expression_data_counts.tsv.txt.gz (GEO supplementary)", "paper_input": "Gene-level expression tables from STAR/Salmon (S4.10.p1), tested with DESeq2", "rounding_documented": true, "matrix_type": "estimated counts (nf-core STAR/Salmon gene-level counts, deposited as integers)", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\aligned\\aligned_matrix.csv", "sha256": "ed2ca93c0e2aedc66c8c69a31f080045707553734f2bfd6bf83539b80cb07aac", "n_features": 56941, "n_samples": 14, "annotation_columns_dropped": ["GSM8107900", "GSM8107901", "GSM8107902", "GSM8107903", "GSM8107904", "GSM8107905", "GSM8107906", "GSM8107907", "GSM8107913", "GSM8107917", "GSM8107923", "GSM8107924"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 332035.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values are non-negative integers (integer fraction 1.0), max 1.1M, Ensembl gene rows with GeneSymbol/Biotype annotation. GEO data_processing: nf-core/rnaseq 3.11.1, gene-level raw counts and TPM generated by Salmon. Salmon gene counts are estimated counts; the submitter deposited them already rounded to integers, which is the count input the paper gave DESeq2 (S4.10.p1). The deposited integers are used unchanged (no further rounding). The companion _tpms file is TPM and is not used for DE.

rejected alternatives: [{"value": "GSE257540_expression_data_tpms.tsv.txt.gz", "reason_rejected": "TPM, used by the paper for visualization only; DESeq2 needs counts"}]

### design (valid, not_started)

final: {"analysis_type": "multi-group (one control, two stimulation arms)", "design_column": "grp", "contrasts": [{"name": "grp_EX_vs_C", "control": "C", "treatment": "EX", "role": "primary"}, {"name": "grp_SP_vs_C", "control": "C", "treatment": "SP", "role": "secondary"}, {"name": "grp_EX_vs_SP", "control": "SP", "treatment": "EX", "role": "secondary"}], "estimand_type": "causal (randomized in vitro treatment)", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\suitability\\suitability.md", "n_comparisons": 4, "n_analyzable": 4}}

reasoning: FIG7c-e: three pairwise comparisons among Control, Spontaneous and Exercise CM. One 3-level DESeq2 model with planned contrasts (not pooled levels). Exercise CM vs Control is the primary exercise estimand; Exercise vs Spontaneous isolates contraction intensity.

rejected alternatives: [{"value": "pool SP+EX vs C", "reason_rejected": "paper reports the arms separately"}, {"value": "single model with mechanical samples", "reason_rejected": "separate experiment with its own controls; paper shows separate PCA and analyses"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 14, "n_columns": 3, "columns": ["Intercept", "grp_EX", "grp_SP"], "rank": 3, "full_rank": true, "residual_df": 11, "levels": {"grp": {"SP": 5, "C": 5, "EX": 4}}, "cells": [{"cell": ["C"], "n": 5}, {"cell": ["EX"], "n": 4}, {"cell": ["SP"], "n": 5}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 14, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 14, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.cell line", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.cell type", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.genotype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.4.treatment", "n_levels": 3, "status": ... [2165 more characters]

reasoning: Independent spheroid wells per arm; no donor/subject, pairing, batch or lane variable in GEO metadata or paper. Nothing to block on.

### method (valid, not_started)

final: {"matrix_type": "estimated counts (nf-core STAR/Salmon gene-level counts, deposited as integers)", "method": "DESeq2 (pydeseq2 Wald, one model ~ grp)", "formula": "~ grp", "rounding_documented": true, "paper_route": {"method": "DESeq2 Wald with normal-prior/ashr LFC shrinkage (R 4.2.0)", "status": "reproduced_without_shrinkage", "reason": "pydeseq2 has no ashr; shrinkage changes LFC estimates only, not the Wald p/padj used for DEG calls"}, "deviations": ["no ashr/normal-prior LFC shrinkage", "pydeseq2 instead of R DESeq2", "biochemical samples fitted without the mechanical samples (paper's model composition not stated)"]}

reasoning: Paper's method (S4.10.p1) on the deposited counts.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": "not_reported", "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "FIG7 legend; S4.10.p1"}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper defines DEGs by BH-adjusted p without stating the cutoff; the workflow default BH padj < 0.05 with no fold-change rule is applied (same metric and adjustment). Nominal p < 0.05 is reported as an audit count because the paper used nominal p for its FIG7j mechanical heatmap."}

reasoning: FIG7 legend and S4.10.p1 name BH-adjusted p-values but no numeric cutoff; no effect-size rule stated.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\joint\\DEG_results_grp_EX_vs_C.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\joint\\DEG_results_grp_SP_vs_C.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\joint\\DEG_results_grp_EX_vs_SP.csv"], "counts": {"joint/grp_EX_vs_C": {"applied": {"rule": "padj < 0.05", "n_tested": 13905, "n_significant": 106, "n_up": 70, "n_down": 36, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 34803, "n_significant": 1849, "n_up": 1099, "n_down": 750, "deg_sanity": "ok"}}, "joint/grp_SP_vs_C": {"applied": {"rule": "padj < 0.05", "n_tested": 11887, "n_significant": 128, "n_up": 94, "n_down": 34, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 34803, "n_significant": 1760, "n_up": 1039, "n_down": 721, "deg_sanity": "ok"}}, "joint/grp_EX_vs_SP": {"applied": {"rule": "padj < 0.05", "n_tested": 4450, "n_significant": 14, "n_up": 5, "n_down": 9, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 34803, "n_significant": 752, "n_up":  ... [42 more characters]

reasoning: One DESeq2 model on C/SP/EX, three planned contrasts (FIG7c-e).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_EX_vs_C", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\enrichment_joint_grp_EX_vs_C\\ora\\DEG_results_grp_EX_vs_C_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\enrichment_joint_grp_EX_vs_C\\ora\\DEG_results_grp_EX_vs_C_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\enrichment_joint_grp_EX_vs_C\\ora\\DEG_results_grp_EX_vs_C_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\enrichment_joint_grp_EX_vs_C\\ora\\DEG_results_grp_EX_vs_C_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 106 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Extracellular Matrix Organization (GO:0030198) | padj=4.02e-04 | overlap=9/176 | genes=APP;COL18A1;MMP2;APLP1;SERP ... [1225 more characters]

reasoning: Paper reports GSEA on Wald stat (S4.11.p1, FIG7f); Hallmark used here, paper used c2-c6.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_EX_vs_C", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\enrichment_joint_grp_EX_vs_C\\gsea\\DEG_results_grp_EX_vs_C_GSEA_Hallmark.csv"], "summary": "GSEA complete on 33475 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 46 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.90 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.70 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=2.65 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=2.00 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TGF_BETA_SIGNALING | NES=1.94 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_DN | NES=1.90 | NOM p=0.00e+00 | FDR q=1.29e-04 - HALLMARK_MYOGENESIS | NES=1.87 | NOM p=0.00e+00 | FDR q=2.30e-04 - HALLMARK_APOPTOSIS | NES=1.85 | NOM p=0.00e+00 | FDR q=2.07e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.87 | NOM p=0.00e+00 | FDR q=4.58e-03 - HALLMARK_PANCREAS_BETA_CELLS | NES=-1.79 | NOM p=5.46e-03 | FDR q=3.66e-03 - HALLM ... [399 more characters]

reasoning: Paper reports GSEA on Wald stat (S4.11.p1, FIG7f); Hallmark used here, paper used c2-c6.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_SP_vs_C", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\enrichment_joint_grp_SP_vs_C\\gsea\\DEG_results_grp_SP_vs_C_GSEA_Hallmark.csv"], "summary": "GSEA complete on 33475 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 41 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_G2M_CHECKPOINT | NES=2.79 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.77 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=2.75 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.71 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.52 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=2.34 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.32 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=2.21 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYOGENESIS | NES=2.21 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=2.19 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 5 DOWN (NES < 0, depleted in treatment): - HALLMARK_PANCREAS_BETA_CELLS | NES=-1.25 | NOM p=1.28e-01 | FDR q=3.31e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=-1.23 | NOM p=1.57e-01 | FDR q=2.04e-01 - HALLMARK_S ... [408 more characters]

reasoning: FIG7g

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_EX_vs_SP", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39523700\\GSE257540_biochem\\results\\enrichment_joint_grp_EX_vs_SP\\gsea\\DEG_results_grp_EX_vs_SP_GSEA_Hallmark.csv"], "summary": "GSEA complete on 33475 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 31 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.59 | NOM p=0.00e+00 | FDR q=3.24e-02 - HALLMARK_NOTCH_SIGNALING | NES=1.42 | NOM p=5.84e-02 | FDR q=1.10e-01 - HALLMARK_APICAL_JUNCTION | NES=1.29 | NOM p=4.07e-02 | FDR q=2.76e-01 - HALLMARK_ANGIOGENESIS | NES=1.20 | NOM p=1.99e-01 | FDR q=4.19e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.16 | NOM p=2.45e-01 | FDR q=4.71e-01 - HALLMARK_UV_RESPONSE_DN | NES=1.15 | NOM p=1.68e-01 | FDR q=4.04e-01 - HALLMARK_G2M_CHECKPOINT | NES=1.12 | NOM p=2.03e-01 | FDR q=4.32e-01 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.08 | NOM p=3.07e-01 | FDR q=4.95e-01 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.04 | NOM p=3.47e-01 | FDR q=5.42e-01 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.00 | NOM p=4.80e-01 | FDR q=6.05e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MTORC1_SIGNALING | NES=-2.71 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=-2.61 | NOM p=0.00e ... [402 more characters]

reasoning: FIG7h

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper's 194 DEGs is a union over the three biochemical comparisons; per-contrast counts are not reported.", "Spontaneous arm keeps 5 samples vs paper's 4 (second excluded sample not identifiable from deposited counts)."], "results": {"joint/grp_EX_vs_C": {"n_deg": 106, "up": 70, "down": 36, "rule": "padj < 0.05", "audit_n": 1849}, "joint/grp_SP_vs_C": {"n_deg": 128, "up": 94, "down": 34, "rule": "padj < 0.05", "audit_n": 1760}, "joint/grp_EX_vs_SP": {"n_deg": 14, "up": 5, "down": 9, "rule": "padj < 0.05", "audit_n": 752}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"joint/grp_EX_vs_C": {"Ntn1": {"baseMean": 152.4292, "log2FoldChange": 0.9973, "padj": 0.0246, "pvalue": 9.15e-05}, "Iqgap1": {"baseMean": 345.7587, "log2FoldChange": 1.037, "padj": 0.00318, "pvalue": 3.31e-06}, "Wls": {"baseMean": 115.7602, "log2FoldChange": 1.2146, "padj": 0.00994, "pvalue": 1.54e-05}, "Lamb1": {"baseMean": 310.5686, "log2FoldChange": 1.3774, "padj": 0.00237, "pvalue": 8.94e-07}, "Itgb1": {"baseMean": 755.5403, "log2FoldChange": 0.6726, "padj": 0.0246, "pvalue": 9.59e-05}, "Sema3b": {"baseMean": 13.7524, "log2FoldChange": 2.3065, "padj": 0.0403, "pvalue": 0.000243}, "Sema3d": {"baseMean": 23.7958, "log2FoldChange": 2.4001, "padj": 0.024, "pvalue": 8.45e-05}, "Cdh1": {"baseMean": 11.6122, "log2FoldChange": 3.1576, "padj": 0.0246, "pvalue": 9.9e-05}, "Lamc1": {"baseMean": 668.1478, "log2FoldChange": 0.6309, "padj": 0.00843, "pvalue": 1.15e-05} ... [1259 more characters]

reasoning: Paper reports a union count (194) and named up-regulated genes; union computed separately for HANDBACK.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 14 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "QC exclusions",
    "paper": "n = 5 excluded (S4.10.p1) but FIG7a/i imply 6 (18->13 biochemical, 8->7 mechanical)",
    "data": "5 samples fail criteria computable from counts (C4, LI6, HI4, HI5, MC3); no second spontaneous sample fails",
    "disposition": "executable_with_deviation: keep 5 SP samples"
  },
  {
    "item": "Group naming",
    "paper": "spontaneous twitch / exercised muscle CM",
    "data": "GEO Low / High intensity biochem (NE / S in overall design)",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 39523700 (PMC11874633)

Paper: *Actuating Extracellular Matrices Decouple the Mechanical and Biochemical Effects of Muscle Contraction on Motor Neurons.*
Decision maker: Claude Opus 5.5 (Claude Code session), bioinformatics-workflow skill, case-spec route. I skipped the preflight because the request said to.
Spec: `case_spec.json`. Runner output: `summary.csv`, `run_status.json`, per-case folders. Validator: 30 records, 0 errors.

## What ran

| Case | Outcome | Route |
|---|---|---|
| GSE257540_biochem | completed | paper_aligned. One DESeq2 model `~ grp` on Control (C, n=5), spontaneous-twitch CM (SP, n=5) and exercised-muscle CM (EX, n=4). Three planned contrasts (FIG7c-e). |
| GSE257540_mech | completed | paper_aligned. DESeq2 `~ grp` on MagMA-actuated (MS, n=4) vs non-actuated control (MC, n=3) (FIG7i). |
| GSE281241 | refused at `design` | Unstimulated ChR2::tdTomato C2C12 vs WT C2C12 myotubes. This is a genotype or cell-line characterization with no exercise or contraction arm. The paper does not cite this series: it cites only GSE257540 (S4.8.p2, DA.p1). The link comes only from GEO (Series_pubmed_id, SuperSeries GSE281242). |

How the decisions were made:
- **Group identity.** GEO's "Low intensity biochem" is the NE samples: medium from unstimulated, spontaneously twitching muscle. "High intensity biochem" is the S samples: medium from optically stimulated (exercised) muscle. Both come from the GSE257540 Series_overall_design.
- **Alignment.** Matrix columns L1 and H1 correspond to titles LI1 and HI1. I matched them by deriving a key with `key_patterns` and setting `normalize_keys`. The match is exact; nothing was aligned by position.
- **Matrix.** The counts are nf-core STAR/Salmon gene counts that the submitter deposited already rounded to integers. They went into DESeq2 unchanged, which is the paper's input. The TPM file was not used.
- **QC exclusions (S4.10.p1 criteria, computed from the deposited counts):**
  - C4: rRNA fraction 0.78.
  - LI6: 1,536 reads.
  - HI4: 243K reads.
  - HI5: 495K reads, just under the 500K cutoff.
  - MC3: 613K reads with the most detected genes of any sample, which fits the low exon/intron criterion.

  That makes 5 exclusions, matching the paper's "n = 5".
- **Threshold.** The paper says only that DEGs used BH-adjusted p-values and gives no cutoff and no fold-change rule. I applied `workflow_default` (padj < 0.05, no LFC rule) and labelled it as such. As an audit I also counted genes at nominal  ... [3990 more characters]
