# Review packet B (the analysis' decisions): GSE302867

## Mechanical flags

- **pairing_key_candidate**: {"key": "characteristics_ch1.4.treatment (without characteristics_ch1.3.genotype) + suffix of title", "across": "characteristics_ch1.3.genotype", "pairs_or_sets": 10, "samples_linked": 20, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Samples per design level

### `grp`
- **KOEx** (5): GSM9112675 / KO_Ex_1 / Library name: G4-1; GSM9112676 / KO_Ex_2 / Library name: G4-2; GSM9112677 / KO_Ex_3 / Library name: G4-3; GSM9112678 / KO_Ex_4 / Library name: G4-4; GSM9112679 / KO_Ex_5 / Library name: G4-5
- **KOSed** (5): GSM9112665 / KO_Sed_1 / Library name: G2-1; GSM9112666 / KO_Sed_2 / Library name: G2-2; GSM9112667 / KO_Sed_3 / Library name: G2-3; GSM9112668 / KO_Sed_4 / Library name: G2-4; GSM9112669 / KO_Sed_5 / Library name: G2-5
- **WTEx** (5): GSM9112670 / WT_Ex_1 / Library name: G3-1; GSM9112671 / WT_Ex_2 / Library name: G3-2; GSM9112672 / WT_Ex_3 / Library name: G3-3; GSM9112673 / WT_Ex_4 / Library name: G3-4; GSM9112674 / WT_Ex_5 / Library name: G3-5
- **WTSed** (5): GSM9112660 / WT_Sed_1 / Library name: G1-1; GSM9112661 / WT_Sed_2 / Library name: G1-2; GSM9112662 / WT_Sed_3 / Library name: G1-3; GSM9112663 / WT_Sed_4 / Library name: G1-4; GSM9112664 / WT_Sed_5 / Library name: G1-5

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE302867"], "assay": "bulk polyA RNA-seq of whole mouse heart (Illumina HiSeq2500, Novogene)", "design": "2x2 factorial: genotype (WT vs cardiomyocyte-specific PGC-1a KO) x exercise (sedentary vs 6-week voluntary wheel running), n=5 male mice per group (Fig 2e/f, Fig 4a legends)", "sample_inclusion": "20 hearts, 5 per group; all male", "primary_estimand": "Effect of 6-week voluntary wheel endurance training on the heart transcriptome within each genotype (WT_Ex vs WT_Sed; KO_Ex vs KO_Sed), Fig 2e-f", "planned_contrasts": ["WT_Ex vs WT_Sed (Fig 2e GSEA Hallmark OXPHOS NES=5.14 FDR=8.8e-5; Fig 2f; no DEG count reported)", "KO_Ex vs KO_Sed (Fig 2e GSEA OXPHOS NES=-10.22 FDR=8.2e-5; no DEG count reported)", "KO_Sed vs WT_Sed (Fig 4a volcano, Gdf15 most upregulated; no DEG count reported)", "KO_Ex vs WT_Ex (Fig 4a volcano, Gdf15 most upregulated; no DEG count reported)"], "repeated_measure_unit": "none; each mouse contributes one heart", "normalization": "DESeq2 normalized counts", "paper_method": "DESeq2 (S4.10.p1); GSEA classic mode on Hallmark MH and M8 gene sets", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S4.10.p1"}, "paper_results": "No DEG counts given in text or figure legends; GSEA OXPHOS up in WT training, depleted in KO training (FIG11 e); Gdf15 top upregulated KO vs WT in both states (S2.4.p2, FIG13 a)"}

reasoning: S4.10.p1: DESeq2, DE if |log2FC|>1 and BH-adjusted P<0.05. FIG11 (Fig 2e-f): bulk cardiac RNA-seq n=5/group, WT_Ex vs WT_Sed and KO_Ex vs KO_Sed GSEA. FIG13 (Fig 4a): KO_Sed vs WT_Sed and KO_Ex vs WT_Ex volcano plots, DESeq2 FDR<0.05. S2.4.p2: 4 groups sequenced. DA.p1 names GSE302867. The request is the exercise effect, so the two within-genotype training contrasts are primary; the genotype contrasts are secondary.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE302867\\GSE302867_processed_data_fpkm.txt.gz", "owned": true, "checks": ["DA.p1 deposits bulk heart RNA-seq under GSE302867", "GEO: Heart, Mus musculus, male, HiSeq 2500 (matches S4.10.p1), 20 samples = 4 groups x 5 (matches Fig 2e n=5/group)", "sample titles WT_Sed/KO_Sed/WT_Ex/KO_Ex match the paper's group names"], "accession": "GSE302867", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE302867\\GSE302867_metadata.csv"}

reasoning: Data availability statement DA.p1 names GSE302867; platform, tissue, sex, and group structure all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 20, "n_metadata": 20, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^((?:WT|KO)_(?:Sed|Ex))_\\d+$", "recode": {"WT_Sed": "WTSed", "KO_Sed": "KOSed", "WT_Ex": "WTEx", "KO_Ex": "KOEx"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\aligned\\design_metadata.csv", "sha256": "f9b0591c4d85a4d79b3c0b585ef7fd6e387c153441c1c3239afd4512fb4b9503", "levels": {"grp": {"WTSed": 5, "KOSed": 5, "WTEx": 5, "KOEx": 5}}}}

reasoning: Matrix columns G1-1..G4-5 equal the library names in the GEO description field (inspect: 20/20 match). Group comes from the title (WT_Sed_1 etc.), which agrees with the genotype and treatment characteristics columns. Level names recoded to be formula-safe.

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\aligned\\aligned_matrix.csv", "sha256": "82f59ff802abde7ef6a81f2c9528357122732e6a1362474c560e9589831936b4", "n_features": 25851, "n_samples": 20, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 69408.85291, "median": 0.641952291, "integer_fraction": 0.1661, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name processed_data_fpkm; GEO data_processing: featureCounts then FPKM normalization, supplementary file contains FPKM; integer fraction 0.17, max 69409, non-negative. Paper analysed counts with DESeq2, but raw counts were not deposited, so the paper's input is unavailable.

### design (valid, not_started)

final: {"analysis_type": "multi-group (2x2 factorial as four cell means, one model)", "design_column": "grp", "formula": "~ 0 + grp", "contrasts": [{"name": "grp_WTEx_vs_WTSed", "control": "WTSed", "treatment": "WTEx", "role": "primary"}, {"name": "grp_KOEx_vs_KOSed", "control": "KOSed", "treatment": "KOEx", "role": "primary"}, {"name": "grp_KOSed_vs_WTSed", "control": "WTSed", "treatment": "KOSed", "role": "secondary"}, {"name": "grp_KOEx_vs_WTEx", "control": "WTEx", "treatment": "KOEx", "role": "secondary"}], "suitability": {"verdict": "partially_analyzable", "failed": [], "warnings": ["sample_size"], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: Paper's exercise estimands are simple effects of training within genotype (FIG11 e); genotype effects within state are Fig 4a. One cell-means model with four planned contrasts keeps every factor level separate.

rejected alternatives: [{"value": "pooled Ex vs Sed across genotypes", "reason_rejected": "paper analyses training within each genotype and the genotypes respond in opposite directions (Fig 2e); pooling would average opposite effects"}, {"value": "separate two-group fits per genotype", "reason_rejected": "one model on all 20 samples gives a shared variance estimate and is the paper's 4-group layout"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 20, "n_columns": 4, "columns": ["Intercept", "grp_KOSed", "grp_WTEx", "grp_WTSed"], "rank": 4, "full_rank": true, "residual_df": 16, "levels": {"grp": {"WTSed": 5, "KOSed": 5, "WTEx": 5, "KOEx": 5}}, "cells": [{"cell": ["KOEx"], "n": 5}, {"cell": ["KOSed"], "n": 5}, {"cell": ["WTEx"], "n": 5}, {"cell": ["WTSed"], "n": 5}], "min_cell_size": 5, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 20, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 20, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.Sex", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.age", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.genotype", "n_levels": 2, "status": "primary_nested_in_c ... [2061 more characters]

reasoning: Independent mice, one heart each; GEO batch field is a single date for all samples, sex constant male, age constant 14-16 weeks. No blocking unit.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (lmFit + contrasts.fit + eBayes, cell-means model on log2(FPKM+1))", "formula": "~ 0 + grp", "paper_route": {"method": "DESeq2 on raw counts", "status": "blocked", "reason": "GEO deposits FPKM only; raw featureCounts counts were not deposited, and FPKM must not be rounded into counts"}, "deviations": ["limma on log2(FPKM+1) instead of DESeq2 on counts; fold changes are on the log2(FPKM+1) scale and are compressed for low-expression genes"], "transform": "log2(x+1)"}

reasoning: Matrix-method policy: FPKM -> log2(x+1) -> limma. Paper route DESeq2 blocked by missing counts.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper rule applied to limma on log2(FPKM+1); log2FC from log FPKM is not identical to DESeq2 shrunken/MLE log2FC"}

reasoning: S4.10.p1: up if log2FC>1, down if log2FC<-1, BH-adjusted P<0.05. Audit rule padj<0.05 without fold-change cutoff for comparison with Fig 4a (FDR<0.05).

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "joint", "role": "primary", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(grp)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\results\\joint\\DEG_results_grp_WTEx_vs_WTSed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\results\\joint\\DEG_results_grp_KOEx_vs_KOSed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\results\\joint\\DEG_results_grp_KOSed_vs_WTSed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\results\\joint\\DEG_results_grp_KOEx_vs_WTEx.csv"], "counts": {"joint/grp_WTEx_vs_WTSed": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 25851, "n_significant": 24, "n_up": 22, "n_down": 2, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 25851, "n_significant": 466, "n_up": 252, "n_down": 214, "deg_sanity": "ok"}}, "joint/grp_KOEx_vs_KOSed": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 25851, "n_significant": 164, "n_up": 130, "n_down": 34, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 25851, "n_significant": 4061, "n_up": 1947, "n_down": 2114, "deg_sanity": "ok"}}, " ... [605 more characters]

reasoning: one limma cell-means model on all 20 samples with the four planned contrasts in the paper's direction (run_joint_limma only offers KOSed_vs_KOEx / WTEx_vs_KOEx for the non-reference pairs, i.e. reversed sign); the two training contrasts are the primary exercise estimands, genotype contrasts secondary

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_WTEx_vs_WTSed", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\results\\enrichment_joint_grp_WTEx_vs_WTSed\\gsea\\DEG_results_grp_WTEx_vs_WTSed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25171 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 45 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.37 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.27 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.17 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.13 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_P53_PATHWAY | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=2.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APOPTOSIS | NES=2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.94 | NOM p=0.00e+00 | FDR q=4.14e-04 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.93 | NOM p=0.00e+00 | FDR q=3.68e-04 - HALLMARK_UV_RESPONSE_UP | NES=1.84 | NOM p=0.00e+00 | FDR q=8.29e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.64 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=-2.15 | NOM p=0.00e+00 |  ... [409 more characters]

reasoning: paper Fig 2e: Hallmark GSEA for WT training (OXPHOS up)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_KOEx_vs_KOSed", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40993371\\GSE302867\\results\\enrichment_joint_grp_KOEx_vs_KOSed\\gsea\\DEG_results_grp_KOEx_vs_KOSed_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25171 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 47 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=3.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.66 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.64 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_KRAS_SIGNALING_UP | NES=2.41 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.38 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.37 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=2.35 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.34 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.54 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=- ... [409 more characters]

reasoning: paper Fig 2e: Hallmark GSEA for KO training (OXPHOS depleted)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["paper reports no DEG counts for any contrast, so counts cannot be compared", "limma on log2(FPKM+1) replaces the paper's DESeq2 on counts", "paper's GSEA used DESeq2 normalized expression with phenotype permutation; ours is preranked on the limma t statistic"], "results": {"joint/grp_WTEx_vs_WTSed": {"n_deg": 24, "up": 22, "down": 2, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 466}, "joint/grp_KOEx_vs_KOSed": {"n_deg": 164, "up": 130, "down": 34, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 4061}, "joint/grp_KOSed_vs_WTSed": {"n_deg": 111, "up": 74, "down": 37, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 1676}, "joint/grp_KOEx_vs_WTEx": {"n_deg": 318, "up": 191, "down": 127, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 4215}}, "paper_counts": {}, "comparison": {}, "paper_gene_check": {"joint/grp_KOSed_vs_WTSed": {"Gdf15": {"AveExpr": 2.8898, "log2FoldChange": 2.9416, "padj": 0.0001, "pvalue": 0.0}, "Ppargc1a": {"AveExpr": 4.2064, "log2FoldChange": 0.8572, "padj": 0.0111, "pvalue": 0.0003}}, "joint/grp_KOEx_vs_WTEx": {"Gdf15": {"AveExpr": 2.8898, "log2FoldChange": 3.4427, "padj": 0.0, "pvalue": 0.0}, "Ppargc1a": {"AveExpr": 4.2064, "log2FoldChange": 0.5304, "padj": 0.0702, "pvalue": 0.0127}}}}

reasoning: S2.4.p2/FIG13: Gdf15 the most upregulated gene in KO vs WT in both states; Ppargc1a is the knocked-out gene (expected down). Training contrasts have only pathway-level claims (OXPHOS GSEA), checked through enrichment.

## Suitability report lines (sex, confounding, warnings)

- Verdict: **partially_analyzable**; check: sample_size
- | Check | Status | Detail |
- | Sample size | partial | 6/6 comparisons have >= 3 per group; planned names not found: grp_KOEx_vs_KOSed, grp_KOEx_vs_WTEx |
- | Sex | pass | Sex inference completed on 20 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE input and method",
    "paper": "DESeq2 on counts (S4.10.p1; GEO data_processing)",
    "data": "only FPKM deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "training duration",
    "paper": "6 weeks voluntary wheel running for molecular analyses (S4.4.p1, FIG11)",
    "data": "GEO age 14-16 weeks, treatment 'exercised'; consistent",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40993371 / GSE302867

Paper: Cardiac adaptation to endurance exercise training requires suppression of GDF15 via PGC-1α (PMC13158892).
Run status: completed (case_runner `execute`, validator 12 records, 0 errors). Route: `declared_deviation`.

## What ran

- Data: GSE302867 (downloaded to `E:/agent/mwangLab_pdf/data/GSE302867`): 20 male mouse hearts, 2x2 genotype (WT vs cardiomyocyte PGC-1a KO) x exercise (sedentary vs 6-week voluntary wheel running), n=5 per group. It matches the paper's Fig 2e-f and Fig 4a (n=5/group) and DA.p1.
- The only deposited matrix is `GSE302867_processed_data_fpkm.txt.gz` (FPKM; GEO data_processing: featureCounts, then FPKM). The paper used DESeq2 on counts (S4.10.p1). Raw counts are not on GEO, so the DESeq2 route is blocked.
- Alignment: matrix columns G1-1..G4-5 match the GEO `description` library names exactly (20/20). The group comes from the title: WTSed, KOSed, WTEx, KOEx.
- Method (declared deviation): limma on log2(FPKM+1), one cell-means model `~ 0 + grp` on all 20 samples, with 4 planned contrasts (`tools.multigroup_tools:run_multigroup_analysis`). No covariates: the batch, sex and age fields each hold a single value for all samples.
- Threshold: the paper's rule (S4.10.p1), BH padj < 0.05 and |log2FC| > 1, applied on the deviation route (`paper_on_deviation_route`). Audit rule: padj < 0.05 with no fold-change cutoff.
- Enrichment: preranked GSEA on MSigDB Hallmark (ranked by the limma t statistic) for the two exercise contrasts, as in the paper's Fig 2e.

## DEG counts vs paper (padj<0.05 & |log2FC|>1; audit padj<0.05 only)

| Contrast | Role | DEGs (up/down) | audit n | Paper |
|---|---|---|---|---|
| WT_Ex vs WT_Sed | primary (exercise) | 24 (22/2) | 466 | no count reported |
| KO_Ex vs KO_Sed | primary (exercise) | 164 (130/34) | 4061 | no count reported |
| KO_Sed vs WT_Sed | secondary (genotype) | 111 (74/37) | 1676 | no count reported (Fig 4a volcano) |
| KO_Ex vs WT_Ex | secondary (genotype) | 318 (191/127) | 4215 | no count reported (Fig 4a volcano) |

The paper gives no DEG counts in its text or figure legends, so the counts cannot be compared with it.

Named-gene and pathway checks:
- Gdf15 KO vs WT: log2FC +2.94 (padj 1e-4) in the sedentary state and +3.44 (padj <1e-4) after exercise. This agrees with the paper's claim that Gdf15 is the most upregulated gene in KO hearts in both states (S2.4.p2, Fig 4a).
- Hallmark OXPHOS, KO_Ex vs KO_Sed: NES -3.54, FDR ~0. This agrees in direction with th ... [2624 more characters]
