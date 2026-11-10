# Review packet B (the analysis' decisions): GSE198652

## Mechanical flags

- **possible_reversed_contrast**: {"contrast": "grp_PoW_vs_Sed_stratum-SolOld", "control": "Sed", "treatment": "PoW", "note": "the control side reads as exercise or the test side as control"}
- **possible_reversed_contrast**: {"contrast": "grp_PoW_vs_Sed_stratum-PlaOld", "control": "Sed", "treatment": "PoW", "note": "the control side reads as exercise or the test side as control"}
- **possible_reversed_contrast**: {"contrast": "grp_PoW_vs_Sed_stratum-SolYoung", "control": "Sed", "treatment": "PoW", "note": "the control side reads as exercise or the test side as control"}
- **possible_reversed_contrast**: {"contrast": "grp_PoW_vs_Sed_stratum-PlaYoung", "control": "Sed", "treatment": "PoW", "note": "the control side reads as exercise or the test side as control"}

## Samples per design level

### `grp`
- **PoW** (16): GSM5954348 / Aged Soleus PoWeR [PoW10_s] / PoW10_s; GSM5954349 / Aged Soleus PoWeR [PoW12_s] / PoW12_s; GSM5954350 / Aged Soleus PoWeR [PoW14_s] / PoW14_s; GSM5954351 / Aged Soleus PoWeR [PoW15_s] / PoW15_s; GSM5954357 / Aged Soleus PoWeR [PoW10_p] / PoW10_p; GSM5954358 / Aged Soleus PoWeR [PoW12_p] / PoW12_p; GSM5954359 / Aged Soleus PoWeR [PoW14_p] / PoW14_p; GSM5954360 / Aged Soleus PoWeR [PoW15_p] / PoW15_p; GSM5954365 / Young Soleus PoWeR [s_3839PV] / s_3839PV; GSM5954366 / Young Soleus PoWeR [s_710PV] / s_710PV; GSM5954367 / Young Soleus PoWeR [s_1327PV] / s_1327PV; GSM5954368 / Young Soleus PoWeR [s_3PV] / s_3PV; GSM5954373 / Young Plantaris PoWeR [PV83_7] / PV83_7; GSM5954374 / Young Plantaris PoWeR [PV810_13] / PV810_13; GSM5954375 / Young Plantaris PoWeR [PV839_43] / PV839_43; GSM5954376 / Young Plantaris PoWeR [PV827_38] / PV827_38
- **Sed** (18): GSM5954343 / Aged Soleus Control [Con12_s] / Con12_s; GSM5954344 / Aged Soleus Control [Con13_s] / Con13_s; GSM5954345 / Aged Soleus Control [Con14_s] / Con14_s; GSM5954346 / Aged Soleus Control [Con15_s] / Con15_s; GSM5954347 / Aged Soleus Control [Con16_s] / Con16_s; GSM5954352 / Aged Soleus Control [Con12_p] / Con12_p; GSM5954353 / Aged Soleus Control [Con13_p] / Con13_p; GSM5954354 / Aged Soleus Control [Con14_p] / Con14_p; GSM5954355 / Aged Soleus Control [Con15_p] / Con15_p; GSM5954356 / Aged Soleus Control [Con16_p] / Con16_p; GSM5954361 / Young Soleus Control [s_15SV] / s_15SV; GSM5954362 / Young Soleus Control [s_1221SV] / s_1221SV; GSM5954363 / Young Soleus Control [s_4244SV] / s_4244SV; GSM5954364 / Young Soleus Control [s_4041SV] / s_4041SV; GSM5954369 / Young Plantaris Control [SV1_5] / SV1_5; GSM5954370 / Young Plantaris Control [SV40_42] / SV40_42; GSM5954371 / Young Plantaris Control [SV41_21] / SV41_21; GSM5954372 / Young Plantaris Control [SV17_44] / SV17_44

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE198652 (bulk RNA-seq, soleus + plantaris, old and young)", "GSE197045 (myonuclear RRBS; not analyzed here)"], "assay": "bulk RNA-seq (Novogene, NovaSeq 6000), STAR in Partek Flow, DESeq2", "primary_estimand": "Effect of 8 wk progressive weighted wheel running (PoWeR) vs age-matched sedentary control on gene expression, within each muscle (soleus, plantaris) and age (old 22->24 mo; young 4-mo-start reference cohort from Englund et al.), each analyzed separately", "factors": {"grp": ["Sedentary", "PoWeR"], "tissue": ["Soleus", "Plantaris"], "age": ["24 mo (old)", "6 mo at GEO / 4 mo at start in paper (young)"]}, "inclusion": "old: Control n=5, PoWeR n=4 for both soleus and plantaris (S2.8.p1); young: n=4/group (S2.8.p1, FIG7 legend); female mice (S2.2.p1, S3.6.p1 sex-matched)", "planned_contrasts": ["Old soleus PoWeR vs Sedentary (S3.6.p1, FIG7 B/D, Supp Table 2)", "Old plantaris PoWeR vs Sedentary (S3.6.p1, FIG7 F/H)", "Young soleus PoWeR vs Sedentary (analyzed separately with same pipeline, S2.8.p1; FIG7 A/C)", "Young plantaris PoWeR vs Sedentary (S2.8.p1; FIG7 E/G)"], "repeated_measure_unit": "none (independent animals; soleus and plantaris come from the same mice but are analyzed per muscle)", "normalization": "DESeq2 median-ratio after excluding genes with max count <= 50 (S2.8.p1 'minimum read cutoff of 50 across all samples'; GEO data_processing)", "paper_method": "DESeq2 (Partek Flow), two-group per muscle per age, BH FDR", "paper_threshold": {"metri ... [430 more characters]

reasoning: Methods S2.8.p1 describe RNA-seq of old soleus and plantaris (5 control, 4 PoWeR) and separate analysis of the young Englund cohort with the same DESeq2 pipeline; S2.10.p1 sets sequencing FDR < 0.10, no fold-change rule. Each muscle x age is a separate two-group comparison (FIG7 panels A-H).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\prep\\GSE198652_counts_by_symbol.csv", "owned": true, "checks": ["S11.p1 names GSE198652 as the RNA-seq deposit", "34 samples = 9+9 old + 8+8 young, matching S2.8.p1 and FIG7 legend", "GEO treatment_protocol and data_processing (STAR, Partek, DESeq2, max count <= 50 filter) match S2.8.p1"], "accession": "GSE198652", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE198652\\GSE198652_metadata.csv"}

reasoning: Paper data availability (S11.p1) lists GSE198652 for RNA-seq; sample structure matches the paper.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 34, "n_metadata": 34, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\aligned\\aligned_metadata.csv", "columns": {"tissue": {"alias_of": "source_name_ch1", "recode": {"Soleus": "Sol", "Plantaris": "Pla"}}, "age": {"alias_of": "characteristics_ch1.2.tag", "recode": {"24 mo": "Old", "6 mo": "Young"}}, "grp": {"alias_of": "characteristics_ch1.1.group", "recode": {"Sedentary": "Sed", "Progressive weighted wheel run (PoWeR)": "PoW"}}, "stratum": {"combine": ["tissue", "age"], "separator": "_", "of": "recoded values", "recode": {"Sol_Old": "SolOld", "Pla_Old": "PlaOld", "Sol_Young": "SolYoung", "Pla_Young": "PlaYoung"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\aligned\\design_metadata.csv", "sha256": "784cecfd4052cadd93f1b1241f17d567f71d3e97bafab7a16c5537cd10ca82ae", "levels": {"tissue": {"Sol": 17, "Pla": 17}, "age": {"Old": 18, "Young": 16}, "grp": {"Sed": 18, "PoW": 16}, "stratum": {"SolOld": 9, "PlaOld": 9, "SolYoung": 8, "PlaYoung": 8}}}}

reasoning: Matrix column names equal metadata `description` (e.g. Con12_s); two differ only by case (Pow12_s/Pow15_p vs PoW12_s/PoW15_p), so normalize_keys. Tissue from source_name_ch1 (title says 'Aged Soleus' for aged plantaris samples, but description suffix _p and source_name say Plantaris), age from tag, group from characteristics group.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\aligned\\aligned_matrix.csv", "sha256": "79542ca64d34715488486bedc6144712e02f7a5d0064887764373ff48bc14aef", "n_features": 23011, "n_samples": 34, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1454880.0, "median": 36.0, "integer_fraction": 0.7434, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO data_processing: STAR + Partek gene counts, 'Matrix table with raw gene counts'; 74% integer values with fractional values (Partek EM-style estimated counts), median 36, max 1.45e6, no normalization. Paper input is the same counts to DESeq2. Rounded to integers for DESeq2 (documented).

### design (valid, not_started)

final: {"analysis_type": "two-group, stratified by muscle x age (separate fits)", "design_column": "grp", "control": "Sed", "treatment": "PoW", "contrasts": [{"name": "grp_PoW_vs_Sed_stratum-SolOld", "control": "Sed", "treatment": "PoW", "role": "primary"}, {"name": "grp_PoW_vs_Sed_stratum-PlaOld", "control": "Sed", "treatment": "PoW", "role": "primary"}, {"name": "grp_PoW_vs_Sed_stratum-SolYoung", "control": "Sed", "treatment": "PoW", "role": "secondary"}, {"name": "grp_PoW_vs_Sed_stratum-PlaYoung", "control": "Sed", "treatment": "PoW", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\suitability\\suitability.md", "n_comparisons": 4, "n_analyzable": 4}}

reasoning: Paper FIG7 panels A-H are PoWeR vs age-matched control per muscle per age. Old contrasts are the paper's new data (primary); young are the re-analyzed comparison cohort (secondary).

rejected alternatives: [{"value": "one model ~ tissue*age*grp", "reason_rejected": "paper analyzed each muscle/age separately (S2.8.p1); young cohort is a different study (Englund et al., Pax7-DTA vehicle), so age is confounded with cohort/batch"}, {"value": "old vs young comparison", "reason_rejected": "not an exercise estimand and confounded with cohort/sequencing batch"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 34, "n_columns": 2, "columns": ["Intercept", "grp_Sed"], "rank": 2, "full_rank": true, "residual_df": 32, "levels": {"grp": {"Sed": 18, "PoW": 16}}, "cells": [{"cell": ["PoW"], "n": 16}, {"cell": ["Sed"], "n": 18}], "min_cell_size": 16, "missing_values": {}}, "confounding": []}

reasoning: Independent animals within each stratum; each fit uses one muscle from each mouse, so no repeated measures within a fit. No batch variable recorded within strata.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "rounding_documented": true, "paper_route": {"method": "DESeq2 in Partek Flow", "status": "reproduced"}, "deviations": ["Partek DESeq2 replaced by pydeseq2 Wald test", "fractional estimated counts rounded to integers", "max-count > 50 filter applied within each stratum's samples (paper wording 'across all samples' is ambiguous about the sample set)"], "transform": "round"}

reasoning: Paper used DESeq2 on Partek counts (S2.8.p1); counts are estimated (fractional) so rounded for the negative-binomial model.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S2.10.p1 'FDR for sequencing experiments was set at < 0.10'; S2.8.p1 BH FDR; no fold-change rule. Audit at FDR<0.05 for the Aldh1l1/Lrrn1 statement (S3.7.p1).

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_PoW_vs_Sed_stratum-SolOld", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\grp_PoW_vs_Sed_stratum-SolOld\\input\\rounded_counts.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\grp_PoW_vs_Sed_stratum-SolOld\\DEG_results_PoW_vs_Sed.csv"], "counts": {"grp_PoW_vs_Sed_stratum-SolOld": {"applied": {"rule": "padj < 0.1", "n_tested": 11723, "n_significant": 1088, "n_up": 509, "n_down": 579, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 11723, "n_significant": 775, "n_up": 339, "n_down": 436, "deg_sanity": "ok"}}}}

reasoning: old soleus PoWeR vs control, paper DESeq2, max count > 50 filter

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_PoW_vs_Sed_stratum-PlaOld", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\grp_PoW_vs_Sed_stratum-PlaOld\\input\\rounded_counts.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\grp_PoW_vs_Sed_stratum-PlaOld\\DEG_results_PoW_vs_Sed.csv"], "counts": {"grp_PoW_vs_Sed_stratum-PlaOld": {"applied": {"rule": "padj < 0.1", "n_tested": 11778, "n_significant": 88, "n_up": 61, "n_down": 27, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 11778, "n_significant": 62, "n_up": 44, "n_down": 18, "deg_sanity": "ok"}}}}

reasoning: old plantaris PoWeR vs control

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_PoW_vs_Sed_stratum-SolYoung", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\grp_PoW_vs_Sed_stratum-SolYoung\\input\\rounded_counts.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\grp_PoW_vs_Sed_stratum-SolYoung\\DEG_results_PoW_vs_Sed.csv"], "counts": {"grp_PoW_vs_Sed_stratum-SolYoung": {"applied": {"rule": "padj < 0.1", "n_tested": 11961, "n_significant": 2601, "n_up": 1238, "n_down": 1363, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 11961, "n_significant": 1764, "n_up": 821, "n_down": 943, "deg_sanity": "ok"}}}}

reasoning: young soleus, analyzed separately with the same pipeline (S2.8.p1)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_PoW_vs_Sed_stratum-PlaYoung", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\grp_PoW_vs_Sed_stratum-PlaYoung\\input\\rounded_counts.csv", "transform": "round", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\grp_PoW_vs_Sed_stratum-PlaYoung\\DEG_results_PoW_vs_Sed.csv"], "counts": {"grp_PoW_vs_Sed_stratum-PlaYoung": {"applied": {"rule": "padj < 0.1", "n_tested": 12432, "n_significant": 668, "n_up": 360, "n_down": 308, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12432, "n_significant": 415, "n_up": 240, "n_down": 175, "deg_sanity": "ok"}}}}

reasoning: young plantaris, analyzed separately

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_PoW_vs_Sed_stratum-SolOld", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-SolOld\\ora_up\\DEG_results_PoW_vs_Sed_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-SolOld\\ora_up\\DEG_results_PoW_vs_Sed_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-SolOld\\ora_up\\DEG_results_PoW_vs_Sed_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-SolOld\\ora_up\\DEG_results_PoW_vs_Sed_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 509 Mouse genes (direction=up, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Positive Regulation Of DNA-templated Transcription (GO:0045893) | padj=2.00e-06 | o ... [1258 more characters]

reasoning: paper FIG7B ORA on up genes FDR<0.10

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_PoW_vs_Sed_stratum-SolOld", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-SolOld\\ora_down\\DEG_results_PoW_vs_Sed_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-SolOld\\ora_down\\DEG_results_PoW_vs_Sed_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-SolOld\\ora_down\\DEG_results_PoW_vs_Sed_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-SolOld\\ora_down\\DEG_results_PoW_vs_Sed_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 579 Mouse genes (direction=down, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Respiration (GO:0045333) | padj=1.57e-60 | overlap=55/85 | gen ... [1268 more characters]

reasoning: paper FIG7D ORA on down genes

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_PoW_vs_Sed_stratum-PlaOld", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-PlaOld\\ora_up\\DEG_results_PoW_vs_Sed_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-PlaOld\\ora_up\\DEG_results_PoW_vs_Sed_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-PlaOld\\ora_up\\DEG_results_PoW_vs_Sed_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-PlaOld\\ora_up\\DEG_results_PoW_vs_Sed_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 61 Mouse genes (direction=up, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Leukocyte Aggregation (GO:0070486) | padj=3.95e-02 | overlap=2/7 | genes=S100A9;S100 ... [1258 more characters]

reasoning: paper FIG7F

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_PoW_vs_Sed_stratum-PlaOld", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-PlaOld\\ora_down\\DEG_results_PoW_vs_Sed_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-PlaOld\\ora_down\\DEG_results_PoW_vs_Sed_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-PlaOld\\ora_down\\DEG_results_PoW_vs_Sed_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35774589\\GSE198652\\results\\enrichment_grp_PoW_vs_Sed_stratum-PlaOld\\ora_down\\DEG_results_PoW_vs_Sed_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 27 Mouse genes (direction=down, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Neurotransmitter Biosynthetic Process (GO:0042136) | padj=1.59e-02 | ove ... [1268 more characters]

reasoning: paper FIG7H

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper DEG counts are only in Supplemental Tables 2A-D, not available; comparison is by named genes", "Young cohort is a different study (Pax7-DTA vehicle mice, 4 mo at start; GEO tag says 6 mo), analyzed separately as in the paper", "'Ccnt' in S3.8.p1 interpreted as Ccnt1"], "results": {"grp_PoW_vs_Sed_stratum-SolOld": {"n_deg": 1088, "up": 509, "down": 579, "rule": "padj < 0.1", "audit_n": 775}, "grp_PoW_vs_Sed_stratum-PlaOld": {"n_deg": 88, "up": 61, "down": 27, "rule": "padj < 0.1", "audit_n": 62}, "grp_PoW_vs_Sed_stratum-SolYoung": {"n_deg": 2601, "up": 1238, "down": 1363, "rule": "padj < 0.1", "audit_n": 1764}, "grp_PoW_vs_Sed_stratum-PlaYoung": {"n_deg": 668, "up": 360, "down": 308, "rule": "padj < 0.1", "audit_n": 415}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"grp_PoW_vs_Sed_stratum-SolOld": {"Aldh1l1": {"baseMean": 107.4882, "log2FoldChange": 0.6217, "padj": 0.0392, "pvalue": 0.00229}, "Lrrn1": {"baseMean": 723.0836, "log2FoldChange": 0.7789, "padj": 1.16e-05, "pvalue": 6.03e-08}, "Agrn": {"baseMean": 318.0016, "log2FoldChange": 0.4055, "padj": 0.0225, "pvalue": 0.00103}, "Kat2a": {"baseMean": 271.6586, "log2FoldChange": 0.3232, "padj": 0.0561, "pvalue": 0.00391}, "Samd1": {"baseMean": 147.0955, "log2FoldChange": 0.5841, "padj": 0.0305, "pvalue": 0.00158}, "Zfp598": {"baseMean": 436.0041, "log2FoldChange": 0.4096, "padj": 0.0127, "pvalue": 0.000449}, "Ccnt1": {"baseMean": 380.1411, "log2FoldChange": -0.1378,  ... [1014 more characters]

reasoning: Paper-aligned two-group DESeq2 per muscle x age at FDR<0.10.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 34 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "young age",
    "paper": "4-mo-old at start (S2.8.p1, S3.6.p1)",
    "data": "GEO tag 6 mo (age at harvest after 8 wk)",
    "disposition": "executable_without_change"
  },
  {
    "item": "aged plantaris titles",
    "paper": "plantaris samples",
    "data": "titles read 'Aged Soleus' for Con*_p/PoW*_p but source_name says Plantaris",
    "disposition": "executable_without_change"
  },
  {
    "item": "matrix row ID",
    "paper": "gene-level counts",
    "data": "deposited first column is Chromosome; re-indexed by unique Gene Symbol in prep_matrix.py",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID35774589 / GSE198652

Paper: Muscle-Specific Cellular and Molecular Adaptations to Late-Life Voluntary Concurrent Exercise (PMC9233305).

## What ran

- Route: case spec (`case_spec.json`) through `python -m tools.case_runner execute`. Status: completed, validator found 17 records and 0 errors.
- Input: `GSE198652_Raw_gene_counts_matrix.txt.gz` (Partek/STAR gene counts, 23,011 genes x 34 samples). `prep_matrix.py` re-indexed it by the unique `Gene Symbol` column and wrote `prep/GSE198652_counts_by_symbol.csv`. The deposited first column is `Chromosome`.
- Alignment: matched on metadata `description` with `normalize_keys`, 34/34 samples. Two samples differ only in case (`Pow12_s` and `Pow15_p`).
- Matrix: estimated counts (74% integers, the rest fractional), rounded for DESeq2 (documented).
- Design: four separate two-group fits, PoWeR vs Sedentary, one per muscle x age stratum, as the paper describes (S2.8.p1, FIG7 A-H):
  - old soleus and old plantaris, 5 vs 4 each (primary);
  - young soleus and young plantaris, 4 vs 4 each (secondary; the re-analyzed Englund et al. cohort).
- Method: pydeseq2 Wald `~ grp`. Within each stratum, genes with a maximum count of 50 or less were dropped, matching the paper's and GEO's filter.
- Threshold: the paper's own rule, BH FDR < 0.10 with no fold-change cutoff (S2.10.p1, S2.8.p1). An audit count at FDR < 0.05 was also recorded.
- Enrichment: Enrichr ORA (GO + KEGG 2019) on up and down genes for the two old contrasts.

## DEG counts (FDR < 0.10; FDR < 0.05 audit in brackets)

| Contrast | n | up | down | paper |
|---|---|---|---|---|
| Old soleus PoW vs Sed | 1088 [775] | 509 | 579 | count only in Supp Table 2 (not available) |
| Old plantaris PoW vs Sed | 88 [62] | 61 | 27 | not available; paper says "very few" genes were down |
| Young soleus PoW vs Sed | 2601 [1764] | 1238 | 1363 | not available |
| Young plantaris PoW vs Sed | 668 [415] | 360 | 308 | not available |

## Named-gene check

- **Aldh1l1 and Lrrn1** (S3.7.p1): up in all four contrasts. Both pass FDR < 0.05 in three of the four. In old plantaris, Aldh1l1 has padj 0.086, which passes FDR < 0.10 but not the paper's stated FDR < 0.05.
- **Old soleus, genes the paper reports as up** (S3.8.p1): Agrn, Samd1 and Zfp598 are up and significant. Kat2a is up but only borderline (padj 0.056).
- **Old soleus, genes the paper reports as down**:
  - Gng5, Mylpf and Slc25a20 are down and significant.
  - "Ccnt", read as Ccnt1, is down but not significant ( ... [1833 more characters]
