# Review packet B (the analysis' decisions): GSE256152

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "grp", "pairs_or_sets": 3, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_swim_vs_Tnm | 134 | 211 | pvalue < 0.05 and |log2FoldChange| > 1 | 47 | 44 | 20 | 76 | 926 | 472 | 211 | 338 | 0.112 | 0.055 |
| grp_union_vs_Tnm | 445 | 523 | pvalue < 0.05 and |log2FoldChange| > 1 | 908 | 602 | 261 | 1470 | 2977 | 1283 | 523 | 1428 | 0.068 | 0.175 |
| grp_cur_vs_Tnm | 107 | 164 | pvalue < 0.05 and |log2FoldChange| > 1 | 45 | 39 | 14 | 58 | 967 | 409 | 164 | 307 | 0.094 | 0.057 |

## Samples per design level

### `grp`
- **Tnm** (3): GSM8086540 / Tnm-1; GSM8086541 / Tnm-2; GSM8086542 / Tnm-3
- **cur** (3): GSM8086543 / Tnm-cur-1; GSM8086544 / Tnm-cur-2; GSM8086545 / Tnm-cur-3
- **swim** (3): GSM8086546 / Tnm-swim-1; GSM8086547 / Tnm-swim-2; GSM8086548 / Tnm-swim-3
- **union** (3): GSM8086549 / Tnm+union-1; GSM8086550 / Tnm+union-2; GSM8086551 / Tnm+union-3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE256152"], "assay": "bulk RNA-seq (Illumina PE), 4T1-luc orthotopic breast tumour tissue, BALB/c mice; HISAT2 to GRCm39, HTSeq read counts, FPKM for display", "sample_inclusion": "3 tumours per tumour group sequenced (S2.3.p1); 12 samples total (S3.2.p1); CK (no tumour) group not sequenced", "factors": {"group": ["Tnm (tumour, vehicle gavage, no swim)", "Tnm_swim (tumour + 30-min daily swim)", "Tnm_cur (tumour + curcumin 100 mg/kg gavage)", "Tnm_union (tumour + curcumin + swim)"]}, "primary_estimand": "Effect of daily swimming exercise on breast-tumour gene expression: Tnm_swim vs Tnm (both vehicle gavage); secondary: combination (curcumin + swimming) vs Tnm", "planned_contrasts": ["Tnm_swim vs Tnm (S3.2.p3; paper: 134 DEGs, 79 up / 55 down)", "Tnm_union vs Tnm (S3.2.p3; paper: 445 DEGs, 154 up / 291 down)", "Tnm_cur vs Tnm (S3.2.p3; paper: 107 DEGs, 28 up / 79 down; non-exercise contrast)"], "repeated_measure_unit": "none; one tumour per independent mouse", "normalization": "DESeq2 size factors on HTSeq read counts (S2.3.p1; GEO data_processing)", "paper_method": "DESeq2 pairwise vs Tnm (S2.3.p1); GEO data_processing says DESeq 1.30.0", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S2.3.p1"}, "paper_results": "S3.2.p3 counts above; S3.2.p4 union-vs-Tnm KEGG: calcium, Wnt, IL-17 signalling with CAMK1G, WNT5A, IL6"}

reasoning: S2.1.p2 defines four tumour groups (2x2 of swimming x curcumin gavage). S2.3.p1: three tumours per group sequenced, DESeq2, |log2FC| > 1 and P < 0.05 (raw p-value). S3.2.p3 reports DEG counts for cur/swim/union each vs Tnm. The exercise question is Tnm_swim vs Tnm (single factor exercise, both vehicle); union vs Tnm is the combined intervention.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\prep\\GSE256152_read_counts.csv", "owned": true, "checks": ["S7.p1 names GSE256152", "GEO extract_protocol describes Tnm/Tnm+swim/Tnm+cur/Tnm+union groups as in S2.1.p2", "12 GEO samples = 4 groups x 3, matching S2.3.p1 and S3.2.p1", "matrix columns Tnm1-3, Tnm_swim1-3, Tnm_cur1-3, Tnm_union1-3 match GEO titles"], "accession": "GSE256152", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE256152\\GSE256152_metadata.csv"}

reasoning: Data availability statement (S7.p1) deposits RNA-seq as GSE256152; the deposited Gene_exp_with_symbol file is the only supplementary matrix and its sample names equal the paper's group names.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(.+)-\\d+$", "recode": {"Tnm": "Tnm", "Tnm-swim": "swim", "Tnm-cur": "cur", "Tnm+union": "union"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\aligned\\design_metadata.csv", "sha256": "1d5072c279653d5d4508fe021c15aeef767a31d3a08e77e339fb170a73cfe292", "levels": {"grp": {"Tnm": 3, "cur": 3, "swim": 3, "union": 3}}}}

reasoning: prep/extract_read_counts.py keeps the 12 ':read count' columns and renames them by name to the GEO titles (Tnm_swim1 -> Tnm-swim-1, Tnm_union1 -> Tnm+union-1, ...); alignment is then exact on metadata 'title'. grp is extracted from the title prefix. Note: GEO treatment field labels swim samples 'corn oil' (vehicle), consistent with S2.1.p2 where Tnm and Tnm_swim get vehicle gavage.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\aligned\\aligned_matrix.csv", "sha256": "f40e17f618f726e8e654f72c1af9e0d8caaa7a0c14d49b16665eb8d2f9b046c6", "n_features": 21899, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 541131.0, "median": 70.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: The deposited file has paired ':read count' and ':fpkm' columns per sample; the read-count columns are all integers with no missing values (checked in prep script). GEO data_processing: HTSeq 0.9.1 read counts, FPKM only for normalization display. Paper input to DESeq2 is the read counts (S2.3.p1).

rejected alternatives: [{"value": "FPKM columns", "reason_rejected": "linear-normalized; DESeq2 needs counts and the paper used counts"}]

### design (valid, not_started)

final: {"analysis_type": "multi-group, pairwise vs common control", "design_column": "grp", "contrasts": [{"name": "grp_swim_vs_Tnm", "control": "Tnm", "treatment": "swim", "role": "primary"}, {"name": "grp_union_vs_Tnm", "control": "Tnm", "treatment": "union", "role": "secondary"}, {"name": "grp_cur_vs_Tnm", "control": "Tnm", "treatment": "cur", "role": "secondary"}, {"name": "grp_union_vs_cur", "control": "cur", "treatment": "union", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: One control (Tnm) with three treated levels (S3.2.p3 compares each vs Tnm). Exercise effect = swim vs Tnm (primary). Union vs Tnm is the paper's combined-treatment contrast (exercise + curcumin, not an isolated exercise effect). Cur vs Tnm is reported by the paper but is not an exercise contrast; run to compare counts. Union vs cur (exercise effect on a curcumin background) is not in the paper -> exploratory. n=3 per group.

rejected alternatives: [{"value": "2x2 factorial ~ swim + cur + swim:cur", "reason_rejected": "paper does not test main effects or interaction; it compares each group to Tnm"}, {"value": "characteristics_ch1.4.treatment", "reason_rejected": "encodes only curcumin vs corn oil; exercise is only in the title"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 12, "n_columns": 4, "columns": ["Intercept", "grp_cur", "grp_swim", "grp_union"], "rank": 4, "full_rank": true, "residual_df": 8, "levels": {"grp": {"Tnm": 3, "cur": 3, "swim": 3, "union": 3}}, "cells": [{"cell": ["Tnm"], "n": 3}, {"cell": ["cur"], "n": 3}, {"cell": ["swim"], "n": 3}, {"cell": ["union"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.cell line", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.cell type", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.host strain", "n_levels": 1, "status": "constant"}, { ... [1927 more characters]

reasoning: Independent mice, one tumour each, randomized to groups (S2.1.p2). No batch, sex (all female BALB/c implied) or lane field recorded in GEO.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2 pairwise two-group, R", "status": "reproduced_with_python_port"}, "deviations": ["pydeseq2 instead of R DESeq2; GEO data_processing names DESeq 1.30.0 while paper says DESeq2", "Paper's two-group comparisons are run as two-group subsets (only the two groups' samples), as in a standard pairwise DESeq2 pipeline; the exploratory union vs cur also as a subset"]}

reasoning: Raw HTSeq counts support DESeq2, which the paper used (S2.3.p1). Each paper contrast is fit on the two groups' samples only, the typical vendor pipeline behaviour; a joint 4-group model is run as sensitivity for the primary exercise contrast.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}}

reasoning: S2.3.p1: |log2FoldChange| > 1 and P-value < 0.05 (raw p, as also stated in GEO data_processing). Audit: BH padj < 0.05, no fold-change rule.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_swim_vs_Tnm", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\grp_swim_vs_Tnm\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\grp_swim_vs_Tnm\\DEG_results_swim_vs_Tnm.csv"], "counts": {"grp_swim_vs_Tnm": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 16914, "n_significant": 211, "n_up": 73, "n_down": 138, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12649, "n_significant": 47, "n_up": 25, "n_down": 22, "deg_sanity": "ok"}}}}

reasoning: Paper's exercise contrast, two-group DESeq2 as in S2.3.p1

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_union_vs_Tnm", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\grp_union_vs_Tnm\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\grp_union_vs_Tnm\\DEG_results_union_vs_Tnm.csv"], "counts": {"grp_union_vs_Tnm": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 16998, "n_significant": 523, "n_up": 286, "n_down": 237, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13371, "n_significant": 908, "n_up": 520, "n_down": 388, "deg_sanity": "ok"}}}}

reasoning: Paper's combination contrast

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_cur_vs_Tnm", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\grp_cur_vs_Tnm\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\grp_cur_vs_Tnm\\DEG_results_cur_vs_Tnm.csv"], "counts": {"grp_cur_vs_Tnm": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 16953, "n_significant": 164, "n_up": 110, "n_down": 54, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14651, "n_significant": 45, "n_up": 35, "n_down": 10, "deg_sanity": "ok"}}}}

reasoning: Paper's curcumin contrast (non-exercise), for count comparison

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_union_vs_cur", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\grp_union_vs_cur\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\grp_union_vs_cur\\DEG_results_union_vs_cur.csv"], "counts": {"grp_union_vs_cur": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 16970, "n_significant": 481, "n_up": 153, "n_down": 328, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14009, "n_significant": 2156, "n_up": 1095, "n_down": 1061, "deg_sanity": "ok"}}}}

reasoning: Exercise effect on curcumin background; not reported in the paper

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\joint\\DEG_results_grp_swim_vs_Tnm.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\joint\\DEG_results_grp_union_vs_Tnm.csv"], "counts": {"joint/grp_swim_vs_Tnm": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 17492, "n_significant": 312, "n_up": 97, "n_down": 215, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13422, "n_significant": 304, "n_up": 144, "n_down": 160, "deg_sanity": "ok"}}, "joint/grp_union_vs_Tnm": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 17492, "n_significant": 563, "n_up": 292, "n_down": 271, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13422, "n_significant": 1629, "n_up": 836, "n_down": 793, "deg_sanity": "ok"}}}}

reasoning: One DESeq2 model on all 12 samples (~ grp) as sensitivity for the exercise contrasts

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_swim_vs_Tnm", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_swim_vs_Tnm\\ora\\DEG_results_swim_vs_Tnm_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_swim_vs_Tnm\\ora\\DEG_results_swim_vs_Tnm_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_swim_vs_Tnm\\ora\\DEG_results_swim_vs_Tnm_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_swim_vs_Tnm\\ora\\DEG_results_swim_vs_Tnm_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 211 Mouse genes (direction=all, pvalue<0.05, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Negative Regulation Of Wound Healing (GO:0061045) | padj=8.12e-03 | overlap=5/28 | genes=SERPINE2;MMRN1;ALOX5;APOE;MYOZ1 - Regulation Of Angiogenesis (GO ... [1184 more characters]

reasoning: Paper ran GO/KEGG on each contrast's DEGs (S3.2.p4, Figs. S1-S2)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_swim_vs_Tnm", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_swim_vs_Tnm\\gsea\\DEG_results_swim_vs_Tnm_GSEA_Hallmark.csv"], "summary": "GSEA complete on 16861 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 18 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_HYPOXIA | NES=2.68 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.31 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_GLYCOLYSIS | NES=1.95 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.92 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANDROGEN_RESPONSE | NES=1.82 | NOM p=0.00e+00 | FDR q=1.08e-03 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.74 | NOM p=0.00e+00 | FDR q=3.24e-03 - HALLMARK_MITOTIC_SPINDLE | NES=1.65 | NOM p=0.00e+00 | FDR q=7.71e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.50 | NOM p=0.00e+00 | FDR q=3.34e-02 - HALLMARK_TGF_BETA_SIGNALING | NES=1.49 | NOM p=3.27e-02 | FDR q=3.03e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=-1.36 | NOM p=5.02e-02 | FDR q=5.97e-01 - HALLMARK_MYOGENESIS | NES=-1.29 | NOM p=5.56e-02 | FDR q=5.82e-01 - HALLMARK_COM ... [387 more characters]

reasoning: Paper ran GO/KEGG on each contrast's DEGs (S3.2.p4, Figs. S1-S2)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_union_vs_Tnm", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_union_vs_Tnm\\ora\\DEG_results_union_vs_Tnm_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_union_vs_Tnm\\ora\\DEG_results_union_vs_Tnm_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_union_vs_Tnm\\ora\\DEG_results_union_vs_Tnm_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_union_vs_Tnm\\ora\\DEG_results_union_vs_Tnm_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 523 Mouse genes (direction=all, pvalue<0.05, |log2FC|>1.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Positive Regulation Of Cell Projection Organization (GO:0031346) | padj=5.80e-04 | overlap=15/118 | genes=FZD1;LTK;TENM3;BDNF;AVIL;NTRK3;WNT5A;P ... [1193 more characters]

reasoning: Paper's KEGG result (calcium, Wnt, IL-17) for the combination (S3.2.p4)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_union_vs_Tnm", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38576560\\GSE256152\\results\\enrichment_grp_union_vs_Tnm\\gsea\\DEG_results_union_vs_Tnm_GSEA_Hallmark.csv"], "summary": "GSEA complete on 16941 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 29 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_E2F_TARGETS | NES=3.00 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.89 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.32 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.01 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=1.92 | NOM p=0.00e+00 | FDR q=2.28e-04 - HALLMARK_MYC_TARGETS_V1 | NES=1.83 | NOM p=0.00e+00 | FDR q=1.33e-03 - HALLMARK_MYC_TARGETS_V2 | NES=1.81 | NOM p=1.88e-03 | FDR q=1.46e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.71 | NOM p=0.00e+00 | FDR q=4.27e-03 - HALLMARK_UV_RESPONSE_DN | NES=1.55 | NOM p=1.77e-03 | FDR q=1.97e-02 - HALLMARK_ANDROGEN_RESPONSE | NES=1.55 | NOM p=5.59e-03 | FDR q=1.89e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.51 | NOM p=0.00e+00 | FDR q=1.42e-01 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=-1.49 | NOM p=1.85e-02 | FDR ... [390 more characters]

reasoning: Paper's KEGG result (calcium, Wnt, IL-17) for the combination (S3.2.p4)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["n = 3 tumours per group; raw-p threshold without multiple-testing correction, so DEG lists include many expected false positives", "Union vs Tnm reflects curcumin + exercise combined, not exercise alone", "pydeseq2 vs R DESeq2/DESeq 1.30.0 can change raw-p DEG counts", "Direction balance contradicts the paper: swim vs Tnm ours 73 up / 138 down vs paper 79 up / 55 down; cur vs Tnm ours 110 up / 54 down vs paper 28 up / 79 down; union vs Tnm ours 286 up / 237 down vs paper 154 up / 291 down. Sign convention here is treatment over Tnm; the paper's convention is not stated, and no single sign flip reconciles all three contrasts", "Paper's union-vs-Tnm KEGG pathways: IL-17 signalling reproduced by ORA (adj p 0.031); Wnt (raw p 0.06) and calcium signalling (raw p 0.12) not significant in our ORA"], "results": {"grp_swim_vs_Tnm": {"n_deg": 211, "up": 73, "down": 138, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 47}, "grp_union_vs_Tnm": {"n_deg": 523, "up": 286, "down": 237, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 908}, "grp_cur_vs_Tnm": {"n_deg": 164, "up": 110, "down": 54, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 45}, "grp_union_vs_cur": {"n_deg": 481, "up": 153, "down": 328, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 2156}, "joint/grp_swim_vs_Tnm": {"n_deg": 312, "up": 97, "down": 215, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 304}, "joint/grp_union ... [678 more characters]

reasoning: S3.2.p3 counts; S3.2.p4 / Fig. 3C genes in the combination-vs-Tnm enriched pathways.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference completed on 12 samples.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE software",
    "paper": "DESeq2 (S2.3.p1)",
    "data": "GEO data_processing: DESeq 1.30.0",
    "disposition": "executable_without_change"
  },
  {
    "item": "group size",
    "paper": "30 mice in 5 groups of 6 (S2.1.p2)",
    "data": "GEO extract protocol: 5 per group; 3 tumours per group sequenced either way",
    "disposition": "executable_without_change"
  },
  {
    "item": "reference genome",
    "paper": "GRCm39 (S2.3.p1)",
    "data": "GEO protocol text mentions mm9 in one field and GRCm39 assembly in another",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID38576560 / GSE256152

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`); validator: 18 records, 0 errors; status completed, route `paper_aligned`.
- Prep: `prep/extract_read_counts.py` keeps the 12 HTSeq `:read count` columns of `GSE256152_Gene_exp_with_symbol.txt.gz` (drops the paired `:fpkm` and annotation columns). It renames the columns by name to the GEO titles (`Tnm_swim1` -> `Tnm-swim-1`, `Tnm_union1` -> `Tnm+union-1`). It checks for integer counts, no NaN and unique IDs. Alignment is exact on `title`: 12/12.
- Design: there is one factor, `grp` (Tnm, swim, cur, union; n=3 each). Tnm is the reference. There is no blocking, because the tumours come from independent randomized mice.
- Method: pydeseq2 Wald. Each of the paper's contrasts was fit as a two-group subset, the way the paper's pairwise DESeq2 is set up. A joint `~ grp` model on all 12 samples was run as a sensitivity check.
- Threshold (paper, S2.3.p1): raw P < 0.05 and |log2FC| > 1. Audit threshold: padj < 0.05, with no fold-change rule.
- Enrichment: ORA (Enrichr GO/KEGG) and Hallmark GSEA for swim vs Tnm and for union vs Tnm.

## DEG counts vs paper (P < 0.05 & |log2FC| > 1)
| Contrast | Role | Ours (up/down) | Paper (up/down, S3.2.p3) | Audit padj<0.05 |
|---|---|---|---|---|
| swim vs Tnm (exercise) | primary | 211 (73/138) | 134 (79/55) | 47 |
| union (cur+swim) vs Tnm | secondary | 523 (286/237) | 445 (154/291) | 908 |
| cur vs Tnm (non-exercise) | secondary | 164 (110/54) | 107 (28/79) | 45 |
| union vs cur (exercise on curcumin) | exploratory | 481 (153/328) | not reported | 2156 |
| joint model swim vs Tnm | sensitivity | 312 (97/215) | | 304 |
| joint model union vs Tnm | sensitivity | 563 (292/271) | | 1629 |

Our counts are 1.2 to 1.6 times the paper's. The paper's up/down balance does not match ours in any contrast, and no single sign flip reconciles all three; this is recorded in the study caveats. The paper's genes in union vs Tnm: Wnt5a (log2FC 1.21, p≈0), Il6 (log2FC 1.29, p=0.003) and Camk1g (log2FC 1.19, p=0.031) all pass the paper rule. In the KEGG ORA for union vs Tnm, IL-17 signalling is the top term (adj p 0.031). Wnt (raw p 0.06) and calcium signalling (raw p 0.12) are not significant, whereas the paper reports them as enriched (it used GSEA for KEGG).

## Deviations
- pydeseq2 was used instead of R DESeq2. GEO data_processing names DESeq 1.30.0, while the paper says DESeq2. Either can shift raw-p DEG counts.
- Th ... [1029 more characters]
