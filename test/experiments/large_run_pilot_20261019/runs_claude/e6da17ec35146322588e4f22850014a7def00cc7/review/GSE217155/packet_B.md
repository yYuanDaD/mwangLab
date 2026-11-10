# Review packet B (the analysis' decisions): GSE217155

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.4.treatment", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deseq2_joint/grp_EXE_vs_NASH | 204 | 188 | padj < 0.05 and |log2FoldChange| > 1 | 336 | 309 | 188 | 525 | 2035 | 1264 | 546 | 820 | 0.102 | 0.114 |

## Samples per design level

### `grp`
- **CON** (3): GSM6705771 / musCTR3; GSM6705772 / musCTR4; GSM6705773 / musCTR29
- **EXE** (3): GSM6705774 / musEXE8; GSM6705775 / musEXE18; GSM6705776 / musEXE22
- **NASH** (3): GSM6705777 / musNASH5; GSM6705778 / musNASH19; GSM6705779 / musNASH20

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE217155"], "assay": "bulk RNA-seq of mouse liver (BGISEQ-500; HISAT/Bowtie2/RSEM)", "factors": {"group": ["NCD control (Con)", "Ath diet sedentary (NASH)", "Ath diet + 8 wk treadmill aerobic exercise (EXE)"]}, "sample_inclusion": "paper: n=8/group randomized (S2.1.p1); RNA-seq on liver tissues of each group (S3.2.p1); GEO deposits 3/group", "primary_estimand": "effect of 8 weeks aerobic treadmill exercise on the liver transcriptome of Ath-diet NASH mice: NASH+Exercise vs NASH sedentary (S3.2.p1, FIG3B)", "planned_contrasts": ["EXE+Ath vs Ath sedentary (S3.2.p1; paper: 204 DEGs, 79 up / 125 down; Dio1 up)", "Ath (NASH) vs NCD control (S3.2.p2, FIG3D/E; GO and GSEA only, no DEG count given)"], "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "source_locator": "S2.6.p1"}, "paper_method": "DESeq2 (R); GO via DAVID on up/down DEGs; GSEA Hallmark/GO (S2.6.p1)", "repeated_measure_unit": "none; independent animals", "paper_results": "204 DEGs EXE vs NASH (79 up, 125 down); Dio1 up; GSEA in EXE vs NASH: inflammatory/IFN/TNFa/IL6 negative, OXPHOS positive, TGF-beta negative"}

reasoning: Methods S2.1.p1 define three groups (NCD, Ath sedentary, Ath+exercise); S2.6.p1 states DESeq2 with padj<0.05 and |log2FC|>1. Results S3.2.p1 report 204 DEGs (79 up / 125 down) in aerobic-exercised NASH mice vs NASH mice. The NASH vs control comparison is reported only through GO/GSEA (S3.2.p2, S3.2.p3). S2.7 (T3 RRA meta-analysis) uses other GEO series and is out of scope here.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\prep\\GSE217155_read_count_symbols.csv", "owned": true, "checks": ["S5.p1 names GSE217155", "GEO: mouse liver, male C57BL/6, groups Con / Ath diet / EXE+Ath diet match S2.1.p1", "contact First Affiliated Hospital of Xiamen University matches ethics S6.p1"], "accession": "GSE217155", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE217155\\GSE217155_metadata.csv"}

reasoning: The data availability statement S5.p1 names GSE217155; GEO samples are liver from male mice in the paper's three groups.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.4.treatment", "recode": {"Con": "CON", "Ath diet": "NASH", "EXE+Ath diet": "EXE"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\aligned\\design_metadata.csv", "sha256": "651f51f486e6e6262960507ef2b920abb42868ad76cb862411e2ee10a6e28d76", "levels": {"grp": {"CON": 3, "EXE": 3, "NASH": 3}}}}

reasoning: Prep script renames matrix columns to GSM ids via metadata title (musCTR3 -> GSM6705771 etc.), so the matrix aligns exactly to the metadata index. grp recodes characteristics_ch1.4.treatment: Con -> CON, Ath diet -> NASH, EXE+Ath diet -> EXE; titles (musCTR/musNASH/musEXE) agree.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\aligned\\aligned_matrix.csv", "sha256": "019095543e1e1e73d6c56305d33779c13346d14aa72856e85666014038a38505", "n_features": 17846, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1898042.0, "median": 138.0, "integer_fraction": 0.6869, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample files carry fpkm_, tpm_ and read_count_ columns (GEO data_processing: RSEM v1.2.8; FPKM, TPM and read count). The read_count columns are RSEM expected counts (mostly integer, some fractional such as 6.99), so they are estimated counts, rounded for DESeq2, which is the paper's stated route (S2.6.p1). The runner's tar merge used the rightmost column per file and dropped GSM6705777 (its file holds all nine samples); the prep script rebuilds the 9-sample read_count matrix and checks the eight single-sample files match it exactly.

rejected alternatives: [{"value": "FPKM/TPM columns with limma", "reason_rejected": "read counts are deposited and the paper used DESeq2"}]

### design (valid, not_started)

final: {"analysis_type": "multi-group, one model with planned pairwise contrasts", "design_column": "grp", "contrasts": [{"name": "grp_EXE_vs_NASH", "control": "NASH", "treatment": "EXE", "role": "primary"}, {"name": "grp_NASH_vs_CON", "control": "CON", "treatment": "NASH", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\suitability\\suitability.md", "n_comparisons": 4, "n_analyzable": 4}}

reasoning: The exercise estimand is EXE vs NASH (both Ath diet, differ only in exercise; S2.1.p1, S3.2.p1). NASH vs CON is the diet model check reported in S3.2.p2. EXE vs CON confounds exercise with diet and is not run. One DESeq2 model on all nine samples with planned contrasts, no pooling of levels.

rejected alternatives: [{"value": "EXE vs CON as the exercise effect", "reason_rejected": "differs in both diet and exercise"}, {"value": "pool CON+NASH as sedentary", "reason_rejected": "pools different diets; not the paper's contrast"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 9, "n_columns": 3, "columns": ["Intercept", "grp_EXE", "grp_NASH"], "rank": 3, "full_rank": true, "residual_df": 6, "levels": {"grp": {"CON": 3, "EXE": 3, "NASH": 3}}, "cells": [{"cell": ["CON"], "n": 3}, {"cell": ["EXE"], "n": 3}, {"cell": ["NASH"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 9, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 9, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.genotype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.Sex", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.4.treatment", "n_levels": 3, "status": ... [1570 more characters]

reasoning: Independent animals, one liver sample each; all male, same strain/genotype; no batch, lane or date column in GEO. No repeated measures.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2", "status": "reproduced"}, "deviations": ["RSEM expected counts rounded to integers before DESeq2", "GEO holds 3 of the paper's 8 mice per group; the paper does not say how many were sequenced"], "rounding_documented": true, "transform": "round"}

reasoning: Paper used DESeq2 (S2.6.p1) on RSEM read counts; pydeseq2 Wald test per contrast from a single ~grp model.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: S2.6.p1: adjusted P < 0.05 and |log2FC| > 1. Audit: padj < 0.05 without fold-change rule.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 9, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\transformed\\rounded_counts.csv", "transform": "round", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\deseq2_joint\\DEG_results_grp_EXE_vs_NASH.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\deseq2_joint\\DEG_results_grp_NASH_vs_CON.csv"], "counts": {"deseq2_joint/grp_EXE_vs_NASH": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 13320, "n_significant": 188, "n_up": 68, "n_down": 120, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13320, "n_significant": 336, "n_up": 116, "n_down": 220, "deg_sanity": "ok"}}, "deseq2_joint/grp_NASH_vs_CON": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15045, "n_significant": 2577, "n_up": 2099, "n_down": 478, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15045, "n_significant": 5146, "n_up": 2840, "n_down": 2306, "deg_sanity": "ok"}}}}

reasoning: One DESeq2 ~grp model on all 9 samples; EXE vs NASH primary, NASH vs CON secondary (diet check).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2_joint/grp_EXE_vs_NASH", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\ora_up\\DEG_results_grp_EXE_vs_NASH_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\ora_up\\DEG_results_grp_EXE_vs_NASH_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\ora_up\\DEG_results_grp_EXE_vs_NASH_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\ora_up\\DEG_results_grp_EXE_vs_NASH_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 68 Mouse genes (direction=up, padj<0.05, |log2FC|>1.0). ### GO_Biological_Process_20 ... [1385 more characters]

reasoning: paper S3.2.p1 GO on 79 up DEGs

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2_joint/grp_EXE_vs_NASH", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\ora_down\\DEG_results_grp_EXE_vs_NASH_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\ora_down\\DEG_results_grp_EXE_vs_NASH_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\ora_down\\DEG_results_grp_EXE_vs_NASH_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\ora_down\\DEG_results_grp_EXE_vs_NASH_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 120 Mouse genes (direction=down, padj<0.05, |log2FC|>1.0). ### GO_Biologic ... [1395 more characters]

reasoning: paper S3.2.p1 GO on 125 down DEGs

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2_joint/grp_EXE_vs_NASH", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_EXE_vs_NASH\\gsea\\DEG_results_grp_EXE_vs_NASH_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17810 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 45 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.18 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_BILE_ACID_METABOLISM | NES=2.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V2 | NES=2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.90 | NOM p=0.00e+00 | FDR q=2.55e-04 - HALLMARK_ADIPOGENESIS | NES=1.78 | NOM p=0.00e+00 | FDR q=1.78e-03 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.72 | NOM p=0.00e+00 | FDR q=3.76e-03 - HALLMARK_DNA_REPAIR | NES=1.54 | NOM p=4.65e-03 | FDR q=1.32e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=-2.48 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MES ... [444 more characters]

reasoning: paper S3.2.p3 GSEA Hallmark (inflammatory, IFN, TNFa, IL6, OXPHOS, TGF-beta)

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "deseq2_joint/grp_NASH_vs_CON", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\e6da17ec35146322588e4f22850014a7def00cc7\\GSE217155\\results\\enrichment_deseq2_joint_grp_NASH_vs_CON\\gsea\\DEG_results_grp_NASH_vs_CON_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17810 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 40 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_ALLOGRAFT_REJECTION | NES=2.65 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.52 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.47 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.35 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.25 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_KRAS_SIGNALING_UP | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=2.04 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.38 | NOM p=0.00e+00 | FDR  ... [444 more characters]

reasoning: paper S3.2.p3 GSEA NASH vs control

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["GEO deposits 3 mice/group vs 8 randomized per group in the paper; sequenced n not stated", "estimated counts rounded"], "results": {"deseq2_joint/grp_EXE_vs_NASH": {"n_deg": 188, "up": 68, "down": 120, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 336}, "deseq2_joint/grp_NASH_vs_CON": {"n_deg": 2577, "up": 2099, "down": 478, "rule": "padj < 0.05 and |log2FoldChange| > 1", "audit_n": 5146}}, "paper_counts": {"deseq2_joint/grp_EXE_vs_NASH": 204}, "comparison": {"deseq2_joint/grp_EXE_vs_NASH": {"ours": 188, "paper": 204}}, "paper_gene_check": {"deseq2_joint/grp_EXE_vs_NASH": {"Dio1": {"baseMean": 1512.9604, "log2FoldChange": 1.9453, "padj": 0.0002, "pvalue": 0.0}, "Il1b": {"baseMean": 97.1972, "log2FoldChange": -0.2834, "padj": 0.8559, "pvalue": 0.5375}, "Tnf": {"baseMean": 37.7619, "log2FoldChange": -0.752, "padj": 0.2893, "pvalue": 0.0346}, "Adgre1": {"baseMean": 416.3967, "log2FoldChange": -0.3559, "padj": 0.6097, "pvalue": 0.202}}}}

reasoning: Paper reports 204 DEGs (79 up/125 down) and Dio1 up for EXE vs NASH (S3.2.p1); Il1b, Tnf, F4/80 (Adgre1) lower after exercise by qPCR (S3.1.p3).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample size",
    "paper": "n=8 per group randomized (S2.1.p1)",
    "data": "3 per group in GEO",
    "disposition": "executable_without_change"
  },
  {
    "item": "GEO tar layout",
    "paper": "n/a",
    "data": "GSM6705777 file holds all nine samples; runner merge dropped it; rebuilt by prep script",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE217155 (PMC9807753, aerobic exercise in Ath-diet NASH mice)

Status: finished. Validator: 14 records, 0 errors. Route: paper_aligned.

## What ran
- `case_runner inspect GSE217155`. It downloaded the series and merged the RAW tar into 17846 genes x **8** samples. The metadata lists 9 samples.
- `prep/build_counts.py` rebuilds the matrix with all 9 samples:
  - It takes the `read_count_*` columns, which hold RSEM expected counts.
  - It checks that the 8 single-sample files are identical to the combined file (max abs diff 0).
  - It renames the columns to GSM ids using the metadata `title`.
  - It maps Entrez IDs to MGI symbols with MyGene: 17740 of 17846 mapped. Unmapped IDs keep their Entrez ID, and no symbols were duplicated.
  - Output: `prep/GSE217155_read_count_symbols.csv`.
- `case_runner execute case_spec.json`:
  - Matrix: estimated counts, rounded.
  - Model: one pydeseq2 model `~ grp` on all 9 samples (CON/NASH/EXE, 3 each), using `tools.joint_contrasts:run_joint_deseq2`.
  - Planned contrasts:
    - EXE vs NASH (primary: exercise effect within the Ath diet).
    - NASH vs CON (secondary: diet check).
  - Not run: EXE vs CON, because it confounds diet with exercise.
- Enrichment:
  - ORA (Enrichr GO and KEGG) on the up and down DEGs of EXE vs NASH.
  - Hallmark GSEA (ranked by stat) for both contrasts.

## DEG counts vs paper
Threshold is the paper's own (S2.6.p1): padj < 0.05 and |log2FC| > 1.

| Contrast | Ours (up/down) | Paper (up/down) | Audit padj<0.05 only |
|---|---|---|---|
| EXE vs NASH | 188 (68/120) | 204 (79/125), S3.2.p1 | 336 |
| NASH vs CON | 2577 (2099/478) | no count reported | 5146 |

Paper genes for EXE vs NASH:
- Dio1: log2FC +1.95, padj 2e-4. Up and significant, as the paper reports.
- Il1b (-0.28), Tnf (-0.75) and Adgre1/F4/80 (-0.36): all lower after exercise, matching the direction of the paper's qPCR, but none is significant here. The paper's qPCR used more mice.

Hallmark GSEA directions all match the paper (S3.2.p3):
- EXE vs NASH:
  - Negative: INFLAMMATORY (NES -2.28), IFNG (-2.14), IFNA (-1.96), IL6_JAK_STAT3 (-1.81), TNFA_NFKB (-1.78), TGF_BETA (-1.40, q=0.028).
  - Positive: OXPHOS (+3.03).
- NASH vs CON:
  - Positive: the inflammatory and IFN sets (NES +2.25 to +2.52).
  - Negative: OXPHOS (-3.38).

## Deviations
- Sample size: GEO has 3 mice per group, while the paper randomized 8 per group (S2.1.p1). The paper does not say how many mice were sequenced.
- RSEM expected counts were rounded to integ ... [1210 more characters]
