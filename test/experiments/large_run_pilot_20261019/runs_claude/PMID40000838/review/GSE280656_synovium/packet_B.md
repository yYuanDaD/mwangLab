# Review packet B (the analysis' decisions): GSE280656_synovium

## Mechanical flags

- none

## Samples per design level

### `grp`
- **Control** (3): GSM8603229 / Syn_Control_rep1; GSM8603230 / Syn_Control_rep2; GSM8603231 / Syn_Control_rep3
- **R24** (3): GSM8603241 / Syn_Repeated_24hr_rep1; GSM8603242 / Syn_Repeated_24hr_rep2; GSM8603243 / Syn_Repeated_24hr_rep3
- **S1** (3): GSM8603232 / Syn_Single_1hr_rep1; GSM8603233 / Syn_Single_1hr_rep2; GSM8603234 / Syn_Single_1hr_rep3
- **S24** (3): GSM8603238 / Syn_Single_24hr_rep1; GSM8603239 / Syn_Single_24hr_rep2; GSM8603240 / Syn_Single_24hr_rep3
- **S4** (3): GSM8603235 / Syn_Single_4hr_rep1; GSM8603236 / Syn_Single_4hr_rep2; GSM8603237 / Syn_Single_4hr_rep3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE280656"], "primary_estimand": "Effect of overloading exercise (treadmill + 20 g weight) on the synovium transcriptome at 1, 4, 24 h after a single bout (S1, S4, S24) and 24 h after 4 daily bouts (R24), each versus non-running controls; plus adjacent time-point comparisons", "planned_contrasts": ["S1 vs control (Fig 3a/4a)", "S4 vs S1 (Fig 3b/4b)", "S24 vs S4 (Fig 3c/4c)", "S4 vs control (Fig 3d/4d)", "S24 vs control (Fig 3e/4e)", "R24 vs control (Fig 5)", "R24 vs S24 (Fig 8b)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S4.4.p2"}, "factors": {"grp": ["Control", "S1", "S4", "S24", "R24"]}, "inclusion": "male C57BL/6J, 10-13 wk; each RNA-seq sample is a pool (synovium 6 knees, cartilage 9 knees); no exclusions (S4.1.p1, S4.4.p1)", "paper_method": "iDEP web app (default DESeq2 on RSEM counts across all groups), FDR < 0.1 and fold change > 2 (S4.4.p2)", "paper_results": "DEG counts per comparison only in Fig 2b (numbers not in text); overlaps: synovium S1&S4 vs control share 52 DEGs, S4&S24 share 9, common S1/S4/S24 = Clec4d, Calca, Ecel1, Saa3 (S2.3.p2); cartilage S1&S4 share 32, S4&S24 share 5, 11 common incl Wnt1, Tnf, Saa3 (S2.4.p2); R24 vs control >> S24 vs control DEGs (S2.5.p1)"}

reasoning: S2.1.p1 defines groups control/S1/S4/S24/R24; S2.2.p1 and Fig 2b compare time points pairwise; S4.4.p2 states iDEP defaults FDR < 0.1, FC > 2. Each tissue is a separate matrix and separate analysis in the paper (Fig 3 synovium, Fig 4 cartilage).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\prep\\GSE280656_synovium_gene_count_noNaN.csv", "owned": true, "checks": ["S8.p1 names GSE280656", "metadata contact Yusuke Arino (first author Y.A.)", "matrix GSE280656_synovium_gene_count.txt.gz columns equal the synovium sample titles", "data_processing (fastp, STAR 2.7.8a, GRCm39/gencode vM33, RSEM 1.3.1) matches S4.4.p2"], "accession": "GSE280656", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE280656\\GSE280656_metadata.csv"}

reasoning: Accession, processing pipeline and sample groups match the paper.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 15, "n_metadata": 26, "coverage": 0.5769, "unmatched_matrix_columns": [], "unmatched_metadata_samples": ["GSM8603244", "GSM8603245", "GSM8603246", "GSM8603247", "GSM8603248", "GSM8603249", "GSM8603250", "GSM8603251", "GSM8603252", "GSM8603253", "GSM8603254"], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^Syn_(Control|Single_1hr|Single_4hr|Single_24hr|Repeated_24hr)_rep\\d+$", "recode": {"Control": "Control", "Single_1hr": "S1", "Single_4hr": "S4", "Single_24hr": "S24", "Repeated_24hr": "R24"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\aligned\\design_metadata.csv", "sha256": "4ae7ad60c5b83279fc70ef76aa1f6f16c857feedd1a98a0e58a4336a53021a45", "levels": {"grp": {"Control": 3, "S1": 3, "S4": 3, "S24": 3, "R24": 3}}}}

reasoning: Matrix columns equal metadata title exactly (15/15); the other tissue's samples are in a separate matrix. grp parsed from the title.

### matrix (valid, not_started)

final: {"source": "GSE280656_synovium_gene_count.txt.gz (57 all-NaN rows dropped by prep/drop_nan_rows.py)", "paper_input": "RSEM expression levels analysed in iDEP with DESeq2 normalization (S4.4.p2-p3)", "matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\aligned\\aligned_matrix.csv", "sha256": "31eae4af98fd62acd7553e8a8c5b111612b9f7f36d425b831562ec9e92cd2c05", "n_features": 56923, "n_samples": 15, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 881873.68, "median": 0.0, "integer_fraction": 0.9322, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: 93% integer values with fractional remainder, library sums ~18-26 M, data_processing says RSEM 'gene count': RSEM expected counts, so DESeq2 after rounding (same as the paper's DESeq2 in iDEP).

### design (valid, not_started)

final: {"analysis_type": "multi-group, one model with planned pairwise contrasts", "design_column": "grp", "contrasts": [{"name": "grp_S1_vs_Control", "control": "Control", "treatment": "S1", "role": "primary"}, {"name": "grp_S4_vs_Control", "control": "Control", "treatment": "S4", "role": "primary"}, {"name": "grp_S24_vs_Control", "control": "Control", "treatment": "S24", "role": "primary"}, {"name": "grp_R24_vs_Control", "control": "Control", "treatment": "R24", "role": "primary"}, {"name": "grp_S4_vs_S1", "control": "S1", "treatment": "S4", "role": "secondary"}, {"name": "grp_S24_vs_S4", "control": "S4", "treatment": "S24", "role": "secondary"}, {"name": "grp_R24_vs_S24", "control": "S24", "treatment": "R24", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 12}}

reasoning: Five independent groups of pooled animals (no subject repeated across groups: separate mice per time point, S2.1.p1). One DESeq2 model on all samples of the tissue, as iDEP does, with the paper's pairwise comparisons. Rejected: pooling single-bout time points; tissue as a factor (paper analyzes tissues separately, separate matrices).

rejected alternatives: [{"value": "pool S1/S4/S24 as 'single'", "reason_rejected": "paper treats time points as distinct levels"}, {"value": "tissue x grp joint model", "reason_rejected": "paper analyzes tissues separately; separate deposited matrices"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 15, "n_columns": 5, "columns": ["Intercept", "grp_R24", "grp_S1", "grp_S24", "grp_S4"], "rank": 5, "full_rank": true, "residual_df": 10, "levels": {"grp": {"Control": 3, "S1": 3, "S4": 3, "S24": 3, "R24": 3}}, "cells": [{"cell": ["Control"], "n": 3}, {"cell": ["R24"], "n": 3}, {"cell": ["S1"], "n": 3}, {"cell": ["S24"], "n": 3}, {"cell": ["S4"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 15, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 15, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "molecule_ch1", "n_levels": 1, "status": "constant"}, {"column": "extract_protocol_ch1", "n_levels": 1, "status": "constant"}, {"column": "description", "n_levels": 1, "status": "constant"}, {"column":  ... [1147 more characters]

reasoning: Each sample is an independent pool of different mice; no batch, sex (all male) or subject key recorded in GEO or paper.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (pydeseq2 Wald, joint model)", "formula": "~ grp", "rounding_documented": true, "paper_route": {"method": "DESeq2 via iDEP", "status": "reproduced_approximately", "reason": "iDEP defaults (DESeq2 on all groups); exact iDEP prefilter and version not stated"}, "deviations": ["RSEM expected counts rounded to integers for DESeq2", "low-count filter CPM >= 0.5 in >= 1 sample assumed as the iDEP default (not stated in paper)", "pydeseq2 rather than R DESeq2"]}

reasoning: Paper used iDEP's DESeq2 (S4.4.p2-p3); matrix holds RSEM estimated counts which DESeq2 accepts after rounding.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S4.4.p2"}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: S4.4.p2: default iDEP thresholds FDR < 0.1 and fold change > 2, i.e. padj < 0.1 and |log2FC| > 1. Audit: padj < 0.05 without effect cutoff.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint_all_timepoints", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 15, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\joint_all_timepoints\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\joint_all_timepoints\\DEG_results_grp_S1_vs_Control.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\joint_all_timepoints\\DEG_results_grp_S4_vs_Control.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\joint_all_timepoints\\DEG_results_grp_S24_vs_Control.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\joint_all_timepoints\\DEG_results_grp_R24_vs_Control.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\joint_all_timepoints\\DEG_results_grp_S4_vs_S1.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\joint_all_timepoints\\DEG_results_grp_S24_vs_S4.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\joint_all_timepoints\\DEG_results_grp_R24_vs_S24.csv"], "counts": {"joint_all_timepoints/grp_S1_vs ... [2190 more characters]

reasoning: one DESeq2 model on all groups of this tissue (iDEP style), all planned pairwise contrasts

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint_all_timepoints/grp_S1_vs_Control", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\ora_up\\DEG_results_grp_S1_vs_Control_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\ora_up\\DEG_results_grp_S1_vs_Control_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\ora_up\\DEG_results_grp_S1_vs_Control_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\ora_up\\DEG_results_grp_S1_vs_Control_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 591 Mouse genes (direction=up, padj<0.1, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms  ... [1367 more characters]

reasoning: paper reports GO BP enrichment of up-regulated DEGs (Metascape) for this comparison (Fig 3a/4a, Fig 5)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint_all_timepoints/grp_S1_vs_Control", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\gsea\\DEG_results_grp_S1_vs_Control_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17209 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 43 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.75 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PROTEIN_SECRETION | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.18 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANDROGEN_RESPONSE | NES=2.09 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.09 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.04 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.94 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=1.91 | NOM p=0.00e+00 | FDR q=2.48e-04 - HALLMARK_UV_RESPONSE_DN | NES=1.88 | NOM p=0.00e+00 | FDR q=2.24e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ADIPOGENESIS | NES=-2.45 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES= ... [448 more characters]

reasoning: paper reports GO BP enrichment of up-regulated DEGs (Metascape) for this comparison (Fig 3a/4a, Fig 5)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint_all_timepoints/grp_S1_vs_Control", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\ora_down\\DEG_results_grp_S1_vs_Control_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\ora_down\\DEG_results_grp_S1_vs_Control_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\ora_down\\DEG_results_grp_S1_vs_Control_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_S1_vs_Control\\ora_down\\DEG_results_grp_S1_vs_Control_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 503 Mouse genes (direction=down, padj<0.1, |log2FC|>1.0). ### GO_Biological_Process_2023 — t ... [1377 more characters]

reasoning: paper reports GO BP enrichment of down-regulated DEGs (Metascape) for this comparison (Fig 3a/4a, Fig 5)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint_all_timepoints/grp_R24_vs_Control", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\ora_up\\DEG_results_grp_R24_vs_Control_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\ora_up\\DEG_results_grp_R24_vs_Control_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\ora_up\\DEG_results_grp_R24_vs_Control_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\ora_up\\DEG_results_grp_R24_vs_Control_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 997 Mouse genes (direction=up, padj<0.1, |log2FC|>1.0). ### GO_Biological_Process_2023 — top  ... [1376 more characters]

reasoning: paper reports GO BP enrichment of up-regulated DEGs (Metascape) for this comparison (Fig 3a/4a, Fig 5)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint_all_timepoints/grp_R24_vs_Control", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\gsea\\DEG_results_grp_R24_vs_Control_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17209 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 36 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PROTEIN_SECRETION | NES=2.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.98 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=1.96 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.83 | NOM p=0.00e+00 | FDR q=1.64e-03 - HALLMARK_COMPLEMENT | NES=1.81 | NOM p=0.00e+00 | FDR q=1.81e-03 - HALLMARK_UV_RESPONSE_DN | NES=1.66 | NOM p=1.55e-03 | FDR q=7.39e-03 - HALLMARK_KRAS_SIGNALING_UP | NES=1.65 | NOM p=0.00e+00 | FDR q=7.63e-03 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.55 | NOM p=1.49e-03 | FDR q=1.67e-02 - HALLMARK_ANDROGEN_RESPONSE | NES=1.50 | NOM p=4.79e-03 | FDR q=2.59e-02 - HALLMARK_PANCREAS_BETA_CELLS | NES=1.40 | NOM p=7.46e-02 | FDR q=6.80e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ADIPOGENESIS | NES=-3.25 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATIO ... [451 more characters]

reasoning: paper reports GO BP enrichment of up-regulated DEGs (Metascape) for this comparison (Fig 3a/4a, Fig 5)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint_all_timepoints/grp_R24_vs_Control", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\ora_down\\DEG_results_grp_R24_vs_Control_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\ora_down\\DEG_results_grp_R24_vs_Control_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\ora_down\\DEG_results_grp_R24_vs_Control_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40000838\\GSE280656_synovium\\results\\enrichment_joint_all_timepoints_grp_R24_vs_Control\\ora_down\\DEG_results_grp_R24_vs_Control_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 831 Mouse genes (direction=down, padj<0.1, |log2FC|>1.0). ### GO_Biological_Process ... [1386 more characters]

reasoning: paper reports GO BP enrichment of down-regulated DEGs (Metascape) for this comparison (Fig 3a/4a, Fig 5)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper DEG counts are only in Fig 2b (not in text); count comparison not possible from text", "pooled samples; small n per group"], "results": {"joint_all_timepoints/grp_S1_vs_Control": {"n_deg": 1104, "up": 598, "down": 506, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 4896}, "joint_all_timepoints/grp_S4_vs_Control": {"n_deg": 412, "up": 180, "down": 232, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 1776}, "joint_all_timepoints/grp_S24_vs_Control": {"n_deg": 171, "up": 83, "down": 88, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 500}, "joint_all_timepoints/grp_R24_vs_Control": {"n_deg": 1844, "up": 1008, "down": 836, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 6568}, "joint_all_timepoints/grp_S4_vs_S1": {"n_deg": 1373, "up": 626, "down": 747, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 5114}, "joint_all_timepoints/grp_S24_vs_S4": {"n_deg": 639, "up": 365, "down": 274, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 2510}, "joint_all_timepoints/grp_R24_vs_S24": {"n_deg": 1377, "up": 699, "down": 678, "rule": "padj < 0.1 and |log2FoldChange| > 1", "audit_n": 5261}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"joint_all_timepoints/grp_S1_vs_Control": {"Nr4a3": {"baseMean": 602.2944, "log2FoldChange": 4.8225, "padj": 0.0, "pvalue": 0.0}, "Inhba": {"baseMean": 688.4919, "log2FoldChange": 3.6191, "padj": 0.0, "pvalue": 0.0}, "Il1b": {"baseMean": 45.38 ... [1869 more characters]

reasoning: Paper's own route (DESeq2, all groups, FDR<0.1 & FC>2) reproduced with documented rounding and assumed iDEP prefilter.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE software",
    "paper": "iDEP web app (DESeq2 default)",
    "data": "pydeseq2 joint model",
    "disposition": "executable_without_change"
  },
  {
    "item": "input values",
    "paper": "RSEM expression levels",
    "data": "RSEM expected counts with decimals; 57 all-NaN rows",
    "disposition": "executable_without_change"
  },
  {
    "item": "replicates",
    "paper": "group sizes in figures",
    "data": "synovium: control 3, exercise arms 3",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40000838 / GSE280656

## What ran
- Route: case spec (`case_spec.json`, built by `prep/build_spec.py`; cartilage stop applied by `prep/stop_cartilage.py`). `python -m tools.case_runner execute` finished with status completed and 21 records, 0 validator errors.
- Prep: `prep/drop_nan_rows.py` removed 57 gene rows that are NaN in every sample, in both deposited RSEM matrices. No other values were changed.
- Two cases, one per tissue. The tissues come as separate matrices, and the paper analyses them separately (Fig 3 synovium, Fig 4 cartilage).
  - **GSE280656_synovium** (paper_aligned, completed). There are 15 samples, n=3 in each of Control, S1, S4, S24 and R24. Alignment is exact on `title`. Matrix: RSEM expected counts. The method is one joint pydeseq2 model, `~ grp`, on all 15 samples, which is how iDEP works. Counts were rounded, and the filter kept genes with CPM >= 0.5 in at least 1 sample (the assumed iDEP default). That filter kept 17,315 genes against the paper's 17,316 (S4.4.p3). All 7 planned pairwise contrasts ran. Enrichment: Enrichr ORA up and down plus Hallmark GSEA, for S1 vs control and R24 vs control.
  - **GSE280656_cartilage** (stopped at `design`, `manual_review`). Control has n=3, but each exercise arm has n=2. Because no planned comparison has n >= 3 per arm, the suitability report fails `sample_size` and returns `not_analyzable`, and the contract then refuses to record the design as valid. Nothing was run for cartilage.

## DEG counts (paper threshold: FDR < 0.1 and fold change > 2, i.e. padj < 0.1 and |log2FC| > 1; S4.4.p2, iDEP defaults)
Synovium, our results (up/down). The audit column is padj < 0.05 with no fold-change cutoff.

| Comparison | n (up/down) | audit n |
|---|---|---|
| S1 vs Control | 1104 (598/506) | 4896 |
| S4 vs Control | 412 (180/232) | 1776 |
| S24 vs Control | 171 (83/88) | 500 |
| R24 vs Control | 1844 (1008/836) | 6568 |
| S4 vs S1 | 1373 (626/747) | 5114 |
| S24 vs S4 | 639 (365/274) | 2510 |
| R24 vs S24 | 1377 (699/678) | 5261 |

- The paper gives its DEG counts only as a figure (Fig 2b), and the numbers are not in the text, so no exact count comparison was possible.
- The qualitative pattern matches the paper:
  - S24 vs control has the fewest DEGs in synovium (S2.2.p1).
  - R24 vs control has far more DEGs than S24 vs control (S2.5.p1).
- Named genes match in direction:
  - Nr4a3 is up at S1 (log2FC 4.8) and down from S4 to S24.
  - Inhba is up at S1, at R24 and in R24 vs S24.
  - Saa3, ... [2151 more characters]
