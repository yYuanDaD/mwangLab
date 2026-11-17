# Review packet B (the analysis' decisions): GSE144133

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.1.participant", "n_values": 8, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **other_rule_matches_paper**: {"table": "train_post_vs_pre", "paper": 817, "applied": 16, "applied_rule": "padj < 0.1", "closest_rule": "pvalue<0.05 & |lfc|>0.584963", "closest_n": 811, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| train_post_vs_pre | 817 | 16 | padj < 0.1 | 0 | 0 | 0 | 16 | 1431 | 811 | 185 | 494 | 0.082 | 0.111 |

## Samples per design level

### `train`
- **post** (6): GSM4281953 / P1_2_R1_RNA; GSM4281955 / P2_2_R1_RNA; GSM4281957 / P3_2_R1_RNA; GSM4281959 / P4_2_R1_RNA; GSM4281961 / P5_2_R1_RNA; GSM4281965 / P7_2_R1_RNA
- **pre** (8): GSM4281952 / P1_1_R1_RNA; GSM4281954 / P2_1_R1_RNA; GSM4281956 / P3_1_R1_RNA; GSM4281958 / P4_1_R1_RNA; GSM4281960 / P5_1_R1_RNA; GSM4281962 / P6_1_R1_RNA; GSM4281964 / P7_1_R1_RNA; GSM4281966 / P8_1_R1_RNA

### `subject`
- **P1** (2): GSM4281952 / P1_1_R1_RNA; GSM4281953 / P1_2_R1_RNA
- **P2** (2): GSM4281954 / P2_1_R1_RNA; GSM4281955 / P2_2_R1_RNA
- **P3** (2): GSM4281956 / P3_1_R1_RNA; GSM4281957 / P3_2_R1_RNA
- **P4** (2): GSM4281958 / P4_1_R1_RNA; GSM4281959 / P4_2_R1_RNA
- **P5** (2): GSM4281960 / P5_1_R1_RNA; GSM4281961 / P5_2_R1_RNA
- **P6** (1): GSM4281962 / P6_1_R1_RNA
- **P7** (2): GSM4281964 / P7_1_R1_RNA; GSM4281965 / P7_2_R1_RNA
- **P8** (1): GSM4281966 / P8_1_R1_RNA

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE144134 (SuperSeries, S4.1.p1)", "GSE144133 (RNA-seq SubSeries)"], "assay": "total RNA-seq (Ribo-Zero), human vastus lateralis biopsies (S2.4.p1)", "subjects": "8 young sedentary Caucasian males, biopsy before and after 6 weeks of endurance training (S2.1.p1, S2.2.p1)", "factors": {"training": ["untrained (pre)", "trained (post)"], "participant": "P1-P8 (blocking)"}, "sample_inclusion": "16 biopsies; P6_2 and P8_2 excluded from DE for dermis contamination (S2.4.p1)", "primary_estimand": "within-participant change in skeletal muscle gene expression after 6 weeks endurance training (trained vs untrained), paired by participant", "planned_contrasts": ["trained vs untrained, ~participant + training (S2.4.p1; S3.1.p2: 641 up, 176 down, FDR<0.1, of 13,108 detected genes)"], "repeated_measure_unit": "participant", "normalization": "kallisto v0.46 transcript quantification, summed to genes by sleuth (S2.4.p1)", "paper_method": "sleuth v0.30 likelihood ratio test ~participant vs ~participant + training; fold changes from Wald test (S2.4.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.1.p2; FIG1 (C)"}, "paper_results": {"up": 641, "down": 176, "total": 817, "validated_up_genes_qPCR": ["COL5A1", "EMILIN1", "SLC9C1", "FSCN1", "NID1"], "trend_up": ["COL4A2", "RASSF2"]}}

reasoning: Methods S2.4.p1 define the RNA-seq DE: kallisto + sleuth LRT comparing ~participant to ~participant + training, P6_2 and P8_2 excluded. Results S3.1.p2 report 641 up and 176 down at FDR < 0.1 with no fold-change cutoff. Methods mention 'Bonferroni corrected q-values' but results and Figure 1C state FDR < 0.1; recorded as a discrepancy and the FDR rule is used.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE144133\\GSE144133_abundance_full.csv.gz", "owned": true, "checks": ["paper S4.1.p1 names SuperSeries GSE144134; GSE144133 metadata series_id = 'GSE144133,GSE144134'", "16 samples P1-P8 x {1,2} = 8 participants pre/post, matching S2.1.p1", "data_processing text reproduces S2.4.p1 (kallisto 0.46, sleuth 0.30, ~Participant + Training)", "tissue vastus lateralis, Homo sapiens, total RNA"], "accession": "GSE144133", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE144133\\GSE144133_metadata.csv"}

reasoning: GSE144133 is the RNA-seq SubSeries of the paper's SuperSeries GSE144134; its processing description is the paper's methods text.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 16, "n_metadata": 16, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM4281963": "P6_2: excluded by the paper for high dermis-gene expression (S2.4.p1)", "GSM4281967": "P8_2: excluded by the paper for high dermis-gene expression (S2.4.p1)"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\aligned\\aligned_metadata_kept.csv", "columns": {"subject": {"alias_of": "characteristics_ch1.1.participant"}, "train": {"alias_of": "characteristics_ch1.2.training", "recode": {"Untrained": "pre", "Trained": "post"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\aligned\\design_metadata.csv", "sha256": "05faa22b18c143945c5c3562ba5bebf56aed3cdec401f7b9ac0cde59a3b6e988", "levels": {"subject": {"P1": 2, "P2": 2, "P3": 2, "P4": 2, "P5": 2, "P7": 2, "P6": 1, "P8": 1}, "train": {"pre": 8, "post": 6}}}}

reasoning: Matrix columns (P1_1 ... P8_2) equal the title prefix before _R1_RNA; exact match on that derived key. Suffix _1/_2 agrees with the training column (Untrained/Trained) for every sample. Participant and training state come from the GEO characteristics.

### matrix (valid, not_started)

final: {"matrix_type": "linear normalized abundance (sleuth-normalized gene-level kallisto estimates, scaled reads per base)", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\aligned\\aligned_matrix.csv", "sha256": "9d87166c1b02b28d906ec54ffe9441e63047c8d1b18310ca1eb94af38bd323ff", "n_features": 12900, "n_samples": 14, "annotation_columns_dropped": ["GSM4281963", "GSM4281967"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 59451.19008, "median": 6.0826752705, "integer_fraction": 0.0061, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: GEO: 'csv file with estimated abundances' from kallisto 0.46 summed to genes by sleuth 0.30; semicolon-delimited, 12,900 Ensembl genes (paper: 13,108 detected), already filtered. Profile: 1.3% integer values; median-of-ratios size factors across the 16 samples are 0.93-1.17, i.e. already normalized; within the 8 pre samples the variance/mean ratio is 0.21 (mean 0.5-1), 0.32 (1-2), 0.52 (2-5), 0.88 (5-10): sub-Poisson, impossible for read counts, so the values are scaled abundances, not counts. Column sums up to 1.65e6 on a gene subset rule out TPM. Sleuth itself models log(x+0.5) of these normalized values, so a log-scale linear model is the matching route.

rejected alternatives: [{"value": "estimated counts (round -> DESeq2)", "reason_rejected": "sub-Poisson variance at low means and size factors ~1 show the values are normalized/scaled, not read counts; a first attempt with this reading (moved to _previous/) gave 15 DEGs with baseMean ~1-5 for well-expressed muscle genes, consistent with the count scale being wrong"}, {"value": "TPM", "reason_rejected": "column sums exceed 1e6 on a filtered gene subset"}]

### design (valid, not_started)

final: {"analysis_type": "paired two-group (repeated measures, participant blocking)", "design_column": "train", "control": "pre", "treatment": "post", "contrasts": [{"name": "train_post_vs_pre", "control": "pre", "treatment": "post", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Paper estimand: trained vs untrained within participant (S2.4.p1 ~participant + training). Interventional pre/post design; no control group, so the effect is a within-subject pre-post change. Single male sex; no sex split.

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking term for repeated biopsies (paper ~participant)"}], "design_check": {"formula_equivalent": "~ C(train) + C(subject)", "n_samples": 14, "n_columns": 9, "columns": ["Intercept", "train_pre", "subject_P2", "subject_P3", "subject_P4", "subject_P5", "subject_P6", "subject_P7", "subject_P8"], "rank": 9, "full_rank": true, "residual_df": 5, "levels": {"train": {"pre": 8, "post": 6}, "subject": {"P1": 2, "P2": 2, "P3": 2, "P4": 2, "P5": 2, "P7": 2, "P6": 1, "P8": 1}}, "cells": [{"cell": ["post", "P1"], "n": 1}, {"cell": ["post", "P2"], "n": 1}, {"cell": ["post", "P3"], "n": 1}, {"cell": ["post", "P4"], "n": 1}, {"cell": ["post", "P5"], "n": 1}, {"cell": ["post", "P7"], "n": 1}, {"cell": ["pre", "P1"], "n": 1}, {"cell": ["pre", "P2"], "n": 1}, {"cell": ["pre", "P3"], "n": 1}, {"cell": ["pre", "P4"], "n": 1}, {"cell": ["pre", "P5"], "n": 1}, {"cell": ["pre", "P6"], "n": 1}, {"cell": ["pre", "P7"], "n": 1}, {"cell": ["pre", "P8"], "n": 1}], "min_cell_size": 1, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 14, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 14, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": ... [2546 more characters]

reasoning: Each participant contributes pre and post biopsies; the paper blocks on participant (S2.4.p1). P6 and P8 keep only their pre sample after the paper's exclusion; as in the paper's ~participant model they absorb their own participant term and do not inform the training effect.

### method (valid, not_started)

final: {"matrix_type": "linear normalized abundance (sleuth-normalized gene-level kallisto estimates, scaled reads per base)", "method": "limma (moderated t, empirical Bayes) on log2(x+0.5) sleuth-normalized abundances", "formula": "~ subject + train", "paper_route": {"method": "sleuth LRT ~participant + training vs ~participant", "status": "blocked", "reason": "sleuth needs per-sample kallisto abundance.h5 with bootstraps, which are not deposited; only the gene-level normalized abundance table is available"}, "deviations": ["limma moderated t on log2(x+0.5) replaces the sleuth LRT on log(x+0.5) with bootstrap-informed technical variance; same model terms (~participant + training) and same pseudocount"], "transform": "log2(x+1)"}

reasoning: sleuth fits a linear model on log(x+0.5) of normalized abundances with shrunken variance; limma on log2(x+0.5) with participant blocking is the closest available executor. DESeq2 rejected because the values are not counts.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "paper FDR < 0.1 applied to limma BH-adjusted p; audit at workflow default padj < 0.05"}

reasoning: S3.1.p2 and Figure 1C: FDR < 0.1, no fold-change cutoff.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "train_post_vs_pre", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + train", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\results\\train_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"train_post_vs_pre": {"applied": {"rule": "padj < 0.1", "n_tested": 12900, "n_significant": 16, "n_up": 16, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12900, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: paper's ~participant + training contrast on the paper's 14-sample set, limma in place of sleuth

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "train_post_vs_pre_complete_pairs", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\results\\train_post_vs_pre_complete_pairs\\input\\paired\\paired_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + train", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\results\\train_post_vs_pre_complete_pairs\\DEG_results_post_vs_pre.csv"], "counts": {"train_post_vs_pre_complete_pairs": {"applied": {"rule": "padj < 0.1", "n_tested": 12900, "n_significant": 16, "n_up": 16, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 12900, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: restrict to the 6 complete pre/post pairs to check that the unpaired P6_1/P8_1 singletons do not drive dispersion estimates

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "train_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\results\\enrichment_train_post_vs_pre\\ora_up\\DEG_results_post_vs_pre_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\results\\enrichment_train_post_vs_pre\\ora_up\\DEG_results_post_vs_pre_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\results\\enrichment_train_post_vs_pre\\ora_up\\DEG_results_post_vs_pre_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\results\\enrichment_train_post_vs_pre\\ora_up\\DEG_results_post_vs_pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 16 Human genes (direction=up, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Endodermal Cell Differentiation (GO:0035987) | padj=1.46e-02 | overlap=2/31 | genes=COL4A2;ITGA5 - Actin Filament Bundle Assembly (GO:00510 ... [1203 more characters]

reasoning: paper runs GO enrichment on upregulated genes (S2.4.p2, FIG1 D)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "train_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34252634\\GSE144133\\results\\enrichment_train_post_vs_pre\\gsea\\DEG_results_post_vs_pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 12426 Human genes ranked by 'stat'. 50 Hallmark sets tested, 35 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.52 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.17 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=1.98 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.97 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.97 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=1.93 | NOM p=0.00e+00 | FDR q=1.25e-04 - HALLMARK_APOPTOSIS | NES=1.93 | NOM p=0.00e+00 | FDR q=1.10e-04 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.88 | NOM p=0.00e+00 | FDR q=1.95e-04 - HALLMARK_KRAS_SIGNALING_UP | NES=1.87 | NOM p=0.00e+00 | FDR q=1.76e-04 ### Top 8 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-1.81 | NOM p=0.00e+00 | FDR q=1.05e-02 - HALLMARK_MYC_TARGETS_V2 | NES=-1.64 | NOM p=2.56e-02 | FDR ... [391 more characters]

reasoning: full-ranking Hallmark GSEA as supporting pathway view

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["sleuth LRT replaced by limma on log2(x+0.5) sleuth-normalized abundances (sleuth bootstraps not deposited)", "pre-post design without a non-exercising control: change includes time effects", "matrix scale inferred from value profile (normalized abundances, not counts)"], "results": {"train_post_vs_pre": {"n_deg": 16, "up": 16, "down": 0, "rule": "padj < 0.1", "audit_n": 0}, "train_post_vs_pre_complete_pairs": {"n_deg": 16, "up": 16, "down": 0, "rule": "padj < 0.1", "audit_n": 0}}, "paper_counts": {"train_post_vs_pre": 817}, "comparison": {"train_post_vs_pre": {"ours": 16, "paper": 817}}, "paper_gene_check": {"train_post_vs_pre": {"COL5A1": {"AveExpr": 1.6165, "log2FoldChange": 2.1223, "padj": 0.131, "pvalue": 0.000309}, "EMILIN1": {"AveExpr": 0.6252, "log2FoldChange": 1.1049, "padj": 0.162, "pvalue": 0.0013}, "SLC9C1": {"AveExpr": 1.0132, "log2FoldChange": 1.0282, "padj": 0.145, "pvalue": 0.000564}, "FSCN1": {"AveExpr": 1.1029, "log2FoldChange": 1.4347, "padj": 0.086, "pvalue": 3.78e-05}, "NID1": {"AveExpr": 1.679, "log2FoldChange": 1.1143, "padj": 0.119, "pvalue": 0.000229}, "COL4A2": {"AveExpr": 4.9763, "log2FoldChange": 1.5623, "padj": 0.086, "pvalue": 4.67e-05}, "RASSF2": {"AveExpr": 0.6153, "log2FoldChange": 0.807, "padj": 0.145, "pvalue": 0.000576}, "LTBP2": {"AveExpr": 1.8927, "log2FoldChange": 0.6412, "padj": 0.171, "pvalue": 0.00151}, "FBN1": {"AveExpr": 4.302, "log2FoldChange": 1.2653, "padj": 0.22, "pvalue": 0.00612}, "C ... [90 more characters]

reasoning: Paper: 641 up + 176 down = 817 at FDR < 0.1; qPCR-validated upregulated genes and enhancer-linked genes (S3.1.p2, S3.3.p2).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 14 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "multiple-testing correction",
    "paper": "Methods S2.4.p1: 'Bonferroni corrected q-values'; Results S3.1.p2 / FIG1: FDR < 0.1",
    "data": "not checkable from deposited data",
    "disposition": "executable_without_change"
  },
  {
    "item": "DE method",
    "paper": "sleuth LRT on kallisto bootstrapped estimates",
    "data": "only gene-level sleuth-normalized abundances deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "gene universe",
    "paper": "13,108 detected genes",
    "data": "12,900 genes in deposited matrix",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 34252634 / GSE144133

Paper: Epigenetic rewiring of skeletal muscle enhancers after exercise training (PMC8355925). GSE144133 is the RNA-seq SubSeries of the SuperSeries GSE144134 that the paper names (S4.1.p1).

## What ran
- Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Status: completed, contract validator 13 records, 0 errors. Route label: `declared_deviation`.
- Design: 8 participants (P1-P8), vastus lateralis biopsies before and after 6 weeks of endurance training. P6_2 (GSM4281963) and P8_2 (GSM4281967) were excluded as the paper did for dermis contamination (S2.4.p1). That leaves 14 samples: 8 pre and 6 post, 6 complete pairs.
- Alignment: matrix columns `P1_1..P8_2` matched exactly to the title prefix (`key_patterns`); 16/16 matched.
- Matrix: deposited `GSE144133_abundance_full.csv.gz` (semicolon-delimited, 12,900 Ensembl genes; the paper reports 13,108 detected). I read it as **sleuth-normalized linear abundances, not counts**, for three reasons:
  - median-of-ratios size factors are 0.93-1.17;
  - variance/mean in the pre samples is 0.21-0.88 for means under 10, which is sub-Poisson;
  - only 1.3% of values are integers.
- Method: limma (moderated t) on log2(x+0.5), `~ subject + train`, contrast post vs pre. Pseudocount 0.5 matches sleuth's log(x+0.5). The paper's sleuth LRT is blocked because the kallisto bootstraps / abundance.h5 files were not deposited.
- Sensitivity run: the same model on the 6 complete pairs only (12 samples).
- Enrichment: ORA (Enrichr GO/KEGG) on the up genes, plus Hallmark GSEA on the full ranking.

## DEG counts vs paper (paper threshold FDR < 0.1, no fold-change cutoff; S3.1.p2, Fig 1C)
| contrast | ours (up/down) | paper (up/down) |
|---|---|---|
| post vs pre, 14 samples (primary) | 16 (16/0) | 817 (641/176) |
| post vs pre, 6 complete pairs (sensitivity) | 16 (16/0) | - |
| audit padj < 0.05 | 0 | - |

- Direction agrees with the paper. At raw p < 0.01 there are 494 genes, 464 of them up; the paper also reports mostly up-regulation.
- The qPCR-validated paper genes are all up with p of 4e-5 to 1.3e-3 (log2FC 0.8-2.1), but padj is 0.086-0.17:
  - padj < 0.1: FSCN1 (0.086) and COL4A2 (0.086);
  - padj 0.1-0.17: COL5A1, NID1, SLC9C1, RASSF2, EMILIN1.
- The gap is power: limma on 6 informative pairs (residual df 5) versus sleuth's LRT with bootstrap technical variance.
- GSEA themes agree with the paper's GO themes (ECM, immune, angiogenesis): EMT NES 2.52, coagulation 2. ... [1499 more characters]
