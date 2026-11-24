# Review packet B (the analysis' decisions): GSE235042

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.2.treatment", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 3, "samples_linked": 9, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_HU_vs_GC | 6628 | 1277 | padj < 0.05 | 1277 | 1277 | 1240 | 2488 | 3761 | 3723 | 2512 | 1798 | 0.048 | 0.298 |
| joint/grp_HUt_vs_HU | 3543 | 361 | padj < 0.05 | 361 | 361 | 361 | 737 | 2552 | 2513 | 1568 | 1005 | 0.061 | 0.202 |
| joint/grp_HUt_vs_GC | 1114 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 169 | 168 | 85 | 23 | 0.111 | 0.013 |

## Samples per design level

### `grp`
- **GC** (3): GSM7493644 / Ground Control sample 1 / MC1_K,no treatment Grounded control mice; GSM7493645 / Ground Control sample 2 / MC3_Kidney,no treatment Grounded control; GSM7493646 / Ground Control sample 3 / MC4_K,no treatment Grounded control mice
- **HU** (3): GSM7493647 / Hindlimb Unloaded sample 1 / U4_K,Hindlimb unloaded mice; GSM7493648 / Hindlimb Unloaded sample 2 / U6_K,Hindlimb unloaded mice; GSM7493649 / Hindlimb Unloaded sample 3 / U7_K,Hindlimb unloaded mice
- **HUt** (3): GSM7493650 / Hindlimb Unloaded/PBA treated Sample 1 / UP1_K,Hindlimb unloaded mice with PBA tr; GSM7493651 / Hindlimb Unloaded/PBA treated Sample 2 / UP3_Kidney,Hindlimb unloaded mice with P; GSM7493652 / Hindlimb Unloaded/PBA treated Sample 3 / UP6_Kidney,Hindlimb unloaded mice with P

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE235042"], "assay": "bulk RNA-seq (Illumina HiSeq 4000, paired-end, HISAT2 mm10), mouse kidney", "organism": "Mus musculus, male C57BL/6J, 4 months old", "sample_inclusion": "3 kidneys per group sequenced (S2.4.p1) out of n=10 mice/group in the animal study (S2.2.p1): GC, HU (vehicle PBS), HU-t (HU + 4-PBA 100 mg/kg/d i.p.)", "factors": {"grp": ["GC (ground control)", "HU (hindlimb unloaded, 3 weeks tail suspension, vehicle)", "HUt (HU + 4-PBA)"]}, "primary_estimand": "Effect of 3 weeks of hindlimb unloading (mechanical disuse / physical inactivity model; the physical-activity axis of this paper, the inverse of loading/exercise) on the kidney transcriptome: HU vs GC. 4-PBA contrasts are drug effects, secondary.", "planned_contrasts": ["HU vs GC (S3.3.p1, Fig. 4a; paper: 6628 DEGs, 4592 up / 2036 down)", "HU-t vs HU (S3.3.p1, Fig. 4b; paper: 3543 DEGs, 1096 up / 2447 down)", "HU-t vs GC (S3.3.p1, Fig. 4c; paper: 1114 DEGs, 890 up / 224 down)"], "repeated_measure_unit": "none; one kidney per mouse, independent animals", "normalization": "read counts -> FPKM for PCA/heatmaps (S2.7.p1); DESeq2 on quantification data (S2.8.p1)", "paper_method": "DESeq2 pairwise comparisons on read counts (S2.8.p1; S2.4.p1 mentions DESeq2/EdgeR)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S2.8.p1"}, "paper_results": "HU vs GC: ECM organization/ECM-receptor interaction, olfactory transduction,  ... [246 more characters]

reasoning: S2.2.p1/S2.4.p1 define the three groups and 3 sequenced replicates each; S2.8.p1 states DESeq2 with BH-adjusted p < 0.05 (the 'log2FoldChange > 0' clause only splits up vs down, no magnitude cutoff); S3.3.p1 gives the three DEG counts. No exercise arm exists; the paper's physical-activity manipulation is hindlimb unloading (disuse), which S5.p1 frames as a model of bed rest and lack of physical activity. HU vs GC is therefore the activity estimand (direction: inactivity relative to normal cage activity).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE235042\\GSE235042_Processed_data.txt.gz", "owned": true, "checks": ["S10.p1 names GSE235042", "metadata series_id GSE235042, 9 GSMs, kidney, male C57BL/6J, HiSeq 4000, 3 per group (Ground control / Hindlimb Unloaded / Hindlimb Unloaded/PBA Treated) as in S2.4.p1", "GEO data_processing text is identical to paper S2.6-S2.7 (HISAT2, FPKM)"], "accession": "GSE235042", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE235042\\GSE235042_metadata.csv"}

reasoning: Paper data availability S10.p1 cites GSE235042; group sizes, tissue, strain and processing text match.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": ["gene_chr", "gene_start", "gene_end", "gene_length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.2.treatment", "regex": "^(Ground control|Hindlimb Unloaded/PBA Treated|Hindlimb Unloaded)$", "recode": {"Ground control": "GC", "Hindlimb Unloaded": "HU", "Hindlimb Unloaded/PBA Treated": "HUt"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\aligned\\design_metadata.csv", "sha256": "50ea393014f3cd59f18aa1d37b96c9333b6c44db890335febe2a4a7493565a89", "levels": {"grp": {"GC": 3, "HU": 3, "HUt": 3}}}}

reasoning: Matrix columns (MC1_K, U4_K, UP3_Kidney, ...) are the first comma field of GEO 'description' (inspect alignment_keys: 9/9). Group from characteristics treatment; MC=control, U=unloaded, UP=unloaded+PBA prefixes agree.

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\aligned\\aligned_matrix.csv", "sha256": "25a5b28e491dc819d566deb42494e32e821f7ff4edcce0b76a604d2e5ac3ddd4", "n_features": 54532, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 396303.0625, "median": 0.0, "integer_fraction": 0.6587, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Only deposited matrix is GSE235042_Processed_data.txt.gz: non-integer values (integer fraction 0.66 is driven by zeros), column sums differ 0.29M-1.9M, data_processing and S2.7.p1 say read counts were normalized to FPKM and the file holds 'normalized abundance'. No raw counts and no RAW tar (supplementary_file NONE). Paper ran DESeq2 on counts; that input is not available.

### design (valid, not_started)

final: {"analysis_type": "multigroup", "design_column": "grp", "contrasts": [{"name": "grp_HU_vs_GC", "control": "GC", "treatment": "HU", "role": "primary"}, {"name": "grp_HUt_vs_HU", "control": "HU", "treatment": "HUt", "role": "secondary"}, {"name": "grp_HUt_vs_GC", "control": "GC", "treatment": "HUt", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: One factor with three levels and one control; one model on all 9 samples with the paper's three pairwise contrasts (S3.3.p1, Fig. 4a-c), never pooling levels. HU vs GC is the primary activity (unloading/disuse) estimand; 4-PBA contrasts are drug effects kept as secondary. n=3 per group (small; reported as such). Estimand is causal (randomized, S2.2.p1) but it is disuse, not exercise.

rejected alternatives: [{"value": "pool HU and HUt vs GC as 'unloaded'", "reason_rejected": "4-PBA changes the kidney transcriptome per paper; pooling mixes drug and unloading."}, {"value": "refuse: no exercise arm", "reason_rejected": "the paper's physical-activity manipulation (hindlimb unloading vs ground control) is present with 3 vs 3 animals; analyzed as the inactivity side of the activity axis, as done for other HU studies in this run."}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 9, "n_columns": 3, "columns": ["Intercept", "grp_HU", "grp_HUt"], "rank": 3, "full_rank": true, "residual_df": 6, "levels": {"grp": {"GC": 3, "HU": 3, "HUt": 3}}, "cells": [{"cell": ["GC"], "n": 3}, {"cell": ["HU"], "n": 3}, {"cell": ["HUt"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 9, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 9, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.treatment", "n_levels": 3, "status": "complete_confounding", "crosstab": {"GC": {"Ground control": 3, "Hindlimb Unloaded": 0, "Hindlimb Unloaded/PBA Treated": 0}, "HU": {"Ground control": 0, "Hindlimb Unlo ... [1851 more characters]

reasoning: Independent animals, one kidney each; no batch, sex (all male) or lane information in GEO; nothing to block on. Sex genes: Xist ~0 and Ddx3y expressed in all 9, consistent with all-male.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (empirical Bayes, trend) on log2(FPKM+1)", "formula": "~ grp", "paper_route": {"method": "DESeq2 on read counts", "status": "blocked", "reason": "only FPKM deposited; no raw counts or RAW tar in GEO; DESeq2 requires counts"}, "deviations": ["limma on log2(FPKM+1) instead of DESeq2 on counts", "low-expression filter FPKM >= 1 in >= 3 samples (not stated in paper)"], "transform": "log2(x+1)"}

reasoning: Matrix policy: FPKM -> log2(x+1) -> limma. One joint model over the three groups so all contrasts share the variance estimate. Filter genes with FPKM >= 1 in at least 3 samples (one group's worth) to remove the many all-zero genes in a 54k-feature table.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "deviation_note": "Paper rule BH FDR < 0.05 applied to limma on log2(FPKM+1) instead of DESeq2 on counts. Audit adds |log2FC| > 1 for comparison only."}

reasoning: S2.8.p1: 'Genes with an adjusted p < 0.05 were assigned as significantly differentially expressed genes'; the 'log2 Fold change > 0' clause classifies direction, no magnitude cutoff.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\joint\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\joint\\DEG_results_grp_HU_vs_GC.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\joint\\DEG_results_grp_HUt_vs_HU.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\joint\\DEG_results_grp_HUt_vs_GC.csv"], "counts": {"joint/grp_HU_vs_GC": {"applied": {"rule": "padj < 0.05", "n_tested": 12642, "n_significant": 1277, "n_up": 669, "n_down": 608, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 12642, "n_significant": 1240, "n_up": 641, "n_down": 599, "deg_sanity": "ok"}}, "joint/grp_HUt_vs_HU": {"applied": {"rule": "padj < 0.05", "n_tested": 12642, "n_significant": 361, "n_up": 151, "n_down": 210, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 12642, "n_significant": 361, "n_up": 151, "n_down": 210, "deg_sanity": "ok"}}, "joint/grp_HUt_vs_GC": {"applied": {"rule": "padj < 0.05", "n_tested": 12642, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": " ... [124 more characters]

reasoning: One limma model ~grp on log2(FPKM+1), three pairwise contrasts as in the paper; HU vs GC is the primary activity contrast.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_HU_vs_GC", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\enrichment_joint_grp_HU_vs_GC\\ora\\DEG_results_grp_HU_vs_GC_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\enrichment_joint_grp_HU_vs_GC\\ora\\DEG_results_grp_HU_vs_GC_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\enrichment_joint_grp_HU_vs_GC\\ora\\DEG_results_grp_HU_vs_GC_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\enrichment_joint_grp_HU_vs_GC\\ora\\DEG_results_grp_HU_vs_GC_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 1256 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Nitrogen Compound Transport (GO:0071705) | padj=3.12e-04 | overlap=30/163 | genes=SCARB2;SLC22A4;SLC22A5;LMAN2L;SLC43A2;SLC22A2;SLC22A1; ... [1202 more characters]

reasoning: paper reports GO/KEGG/Reactome for HU vs GC (ECM up, mitochondria/OXPHOS down); GSEA Hallmark gives the signed comparison

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_HU_vs_GC", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\enrichment_joint_grp_HU_vs_GC\\gsea\\DEG_results_grp_HU_vs_GC_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12528 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 34 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.67 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_DN | NES=2.13 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=1.81 | NOM p=0.00e+00 | FDR q=5.84e-03 - HALLMARK_KRAS_SIGNALING_UP | NES=1.79 | NOM p=0.00e+00 | FDR q=4.38e-03 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.76 | NOM p=0.00e+00 | FDR q=5.15e-03 - HALLMARK_MYOGENESIS | NES=1.69 | NOM p=0.00e+00 | FDR q=7.89e-03 - HALLMARK_PI3K_AKT_MTOR_SIGNALING | NES=1.62 | NOM p=3.75e-03 | FDR q=1.59e-02 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.54 | NOM p=7.52e-03 | FDR q=3.15e-02 - HALLMARK_TGF_BETA_SIGNALING | NES=1.51 | NOM p=2.22e-02 | FDR q=3.70e-02 - HALLMARK_COMPLEMENT | NES=1.46 | NOM p=1.31e-02 | FDR q=4.84e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.48 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=-2.09 | NOM p=0.00e+00 | ... [394 more characters]

reasoning: paper reports GO/KEGG/Reactome for HU vs GC (ECM up, mitochondria/OXPHOS down); GSEA Hallmark gives the signed comparison

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_HUt_vs_HU", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41946794\\GSE235042\\results\\enrichment_joint_grp_HUt_vs_HU\\gsea\\DEG_results_grp_HUt_vs_HU_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12528 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 23 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.94 | NOM p=0.00e+00 | FDR q=3.09e-03 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.92 | NOM p=0.00e+00 | FDR q=2.06e-03 - HALLMARK_PEROXISOME | NES=1.92 | NOM p=0.00e+00 | FDR q=1.37e-03 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.90 | NOM p=0.00e+00 | FDR q=1.03e-03 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.85 | NOM p=0.00e+00 | FDR q=1.65e-03 - HALLMARK_ADIPOGENESIS | NES=1.83 | NOM p=0.00e+00 | FDR q=1.72e-03 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.71 | NOM p=2.15e-03 | FDR q=5.59e-03 - HALLMARK_BILE_ACID_METABOLISM | NES=1.64 | NOM p=2.02e-03 | FDR q=9.39e-03 - HALLMARK_KRAS_SIGNALING_DN | NES=1.52 | NOM p=1.61e-02 | FDR q=2.82e-02 - HALLMARK_MYC_TARGETS_V2 | NES=1.52 | NOM p=2.74e-02 | FDR q=2.57e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-2.39 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_DN | NES=-2.13 | NO ... [397 more characters]

reasoning: secondary drug contrast; signed pathway check against paper's ECM down / peroxisome-PPAR up

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["No exercise arm: the activity contrast is hindlimb unloading (disuse) vs ground control, i.e. the inactivity direction; do not read it as an exercise effect.", "Paper's DESeq2-on-counts route blocked (FPKM only); limma on log2(FPKM+1) is a declared deviation, so counts are not expected to match.", "n = 3 per group.", "Paper text 'control mice vs. hindlimb unloaded mice ... 4592 upregulated' is ambiguous in direction; compared assuming up = higher in HU (Fig. 4a 'HU vs. GC').", "Paper's DEG totals (6628 of the expressed genome at n=3) are unusually large.", "Pathway signs agree with the paper (HU vs GC: Hallmark EMT/ECM and myogenesis up, OXPHOS/fatty-acid/peroxisome down; HUt vs HU reverses them), but the paper's central claim of elevated ER stress in HU is not seen: Hallmark UNFOLDED_PROTEIN_RESPONSE NES -1.12 (FDR 0.34) in HU vs GC, i.e. not up.", "HUt vs GC gives 0 DEGs at FDR < 0.05 vs paper 1114."], "results": {"joint/grp_HU_vs_GC": {"n_deg": 1277, "up": 669, "down": 608, "rule": "padj < 0.05", "audit_n": 1240}, "joint/grp_HUt_vs_HU": {"n_deg": 361, "up": 151, "down": 210, "rule": "padj < 0.05", "audit_n": 361}, "joint/grp_HUt_vs_GC": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 0}}, "paper_counts": {"joint/grp_HU_vs_GC": 6628, "joint/grp_HUt_vs_HU": 3543, "joint/grp_HUt_vs_GC": 1114}, "comparison": {"joint/grp_HU_vs_GC": {"ours": 1277, "paper": 6628}, "joint/grp_HUt_vs_HU": {"ours": 361, "paper": 3543},  ... [75 more characters]

reasoning: Counts from S3.3.p1; the paper names no individual genes, only pathways.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "input matrix",
    "paper": "DESeq2 on read counts (S2.8.p1)",
    "data": "only FPKM deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "sample size",
    "paper": "n=10 mice/group in animal study (S2.2.p1); GEO treatment_protocol says n=6-8",
    "data": "3 per group sequenced, consistent with S2.4.p1",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE235042 / PMID 41946794 (4-PBA, hindlimb unloading, mouse kidney)

## What ran
- Case-spec route: `inspect` → `case_spec.json` → `python -m tools.case_runner execute` (twice; the second run only added study caveats, and the first attempt is in `_previous/`). Validator: 13 records, 0 errors. Status: completed, route `declared_deviation`.
- Data: `GSE235042_Processed_data.txt.gz` (FPKM, 54,532 genes × 9 kidneys). Samples were aligned exactly on the first comma field of GEO `description` (9/9). Groups: GC 3, HU 3, HUt (HU + 4-PBA) 3. All animals are male; the sex genes agree (Xist ≈ 0, Ddx3y expressed in all 9).
- Model: one limma model (`~ grp`) on log2(FPKM+1), fitted to all 9 samples. Genes were filtered to FPKM ≥ 1 in ≥ 3 samples (12,642 kept). The paper's three pairwise contrasts were run.
- Enrichment: for HU vs GC, ORA (Enrichr GO/KEGG) and Hallmark GSEA; for HUt vs HU, Hallmark GSEA only.

## Scientific framing
The study has no exercise arm. Its only physical-activity manipulation is 3 weeks of hindlimb unloading (disuse) against ground controls. The paper itself frames this in S5.p1 as a model of bed rest and lack of physical activity. I analyzed HU vs GC as the primary estimand, the inactivity direction of the activity axis, and did not refuse the case. The two 4-PBA contrasts are drug effects and are kept as secondary.

## DEG counts vs paper (paper threshold: BH FDR < 0.05, no fold-change cutoff; S2.8.p1)
| Contrast | Ours (up/down) | Paper (up/down) |
|---|---|---|
| HU vs GC (primary) | 1277 (669/608) | 6628 (4592/2036) |
| HUt vs HU | 361 (151/210) | 3543 (1096/2447) |
| HUt vs GC | 0 | 1114 (890/224) |

The audit rule (FDR < 0.05 and |log2FC| > 1) gives 1240 / 361 / 0.

Pathway signs match the paper:
- HU vs GC: Hallmark EMT/ECM is up (NES 2.67) and myogenesis is up. Oxidative phosphorylation, fatty-acid metabolism and peroxisome are down.
- HUt vs HU: these signs reverse. EMT is down; OXPHOS, peroxisome and fatty-acid metabolism are up, which matches the paper's PPAR/peroxisome result.
- Not reproduced: the paper's central claim of elevated ER stress in HU. Hallmark UNFOLDED_PROTEIN_RESPONSE has NES −1.12 (FDR 0.34) for HU vs GC. This is recorded in the study caveats.

## Deviations
- The paper ran DESeq2 on read counts (S2.8.p1), but only FPKM is deposited (no counts, no RAW tar). That route is blocked, and limma on log2(FPKM+1) runs as a declared deviation. This probably accounts for much of the gap in counts. The paper's coun ... [935 more characters]
