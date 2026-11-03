# Review packet B (the analysis' decisions): GSE164890

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| time_post_vs_pre | 4058 | 4243 | padj < 0.1 | 3238 | 876 | 185 | 4243 | 5229 | 1307 | 408 | 3226 | 0.179 | 0.185 |

## Samples per design level

### `time`
- **post** (7): GSM5022470 / Skater 1 - after exercise / 1after; GSM5022472 / Skater 2 - after exercise / 2after; GSM5022474 / Skater 3 - after exercise / 3after; GSM5022476 / Skater 4 - after exercise / 4after; GSM5022478 / Skater 5 - after exercise / 5after; GSM5022480 / Skater 6 - after exercise / 6after; GSM5022482 / Skater 7 - after exercise / 7after
- **pre** (7): GSM5022469 / Skater 1 - before exercise / 1before; GSM5022471 / Skater 2 - before exercise / 2before; GSM5022473 / Skater 3 - before exercise / 3before; GSM5022475 / Skater 4 - before exercise / 4before; GSM5022477 / Skater 5 - before exercise / 5before; GSM5022479 / Skater 6 - before exercise / 6before; GSM5022481 / Skater 7 - before exercise / 7before

### `subject`
- **S1** (2): GSM5022469 / Skater 1 - before exercise / 1before; GSM5022470 / Skater 1 - after exercise / 1after
- **S2** (2): GSM5022471 / Skater 2 - before exercise / 2before; GSM5022472 / Skater 2 - after exercise / 2after
- **S3** (2): GSM5022473 / Skater 3 - before exercise / 3before; GSM5022474 / Skater 3 - after exercise / 3after
- **S4** (2): GSM5022475 / Skater 4 - before exercise / 4before; GSM5022476 / Skater 4 - after exercise / 4after
- **S5** (2): GSM5022477 / Skater 5 - before exercise / 5before; GSM5022478 / Skater 5 - after exercise / 5after
- **S6** (2): GSM5022479 / Skater 6 - before exercise / 6before; GSM5022480 / Skater 6 - after exercise / 6after
- **S7** (2): GSM5022481 / Skater 7 - before exercise / 7before; GSM5022482 / Skater 7 - after exercise / 7after

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE164890"], "assay": "bulk RNA-seq, globin-depleted whole blood, strand-specific polyA, HiSeq 4000 (S2.3.p1)", "sample_inclusion": "7 elite female speed skaters, day 18 of altitude camp (1850 m), whole blood before and after one intense skating bout; 14 samples, none excluded (S2.1.p1, S2.1.p2, S2.3.p1)", "factors": {"time": ["before exercise", "after exercise"], "subject": "7 donors, each sampled twice"}, "primary_estimand": "Within-donor change in whole-blood gene expression after vs before an acute intense exercise bout at altitude (after - before)", "planned_contrasts": ["after vs before exercise, paired by donor (FIG1, S3.2.p2; paper: 2516 up, 1542 down = 4058 DEGs at FDR<0.1)"], "repeated_measure_unit": "donor (skater) (S3.2.p1, FIG1 'donor + exercise' design)", "normalization": "DESeq2 size factors on RSEM per-gene counts (S2.5.p1); rlog + ComBat only for plots", "paper_method": "DESeq2 v1.18.1, design ~ donor + exercise, on RSEM gene-level counts (S2.5.p1, FIG1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.5.p1; FIG1 ('reported at 10% FDR')"}, "paper_results": "2516 up, 1542 down (S3.2.p2); 104 up / 58 down >2-fold; named genes MARC1, PHOSPHO1 up (S3.5.p5-6), MYC and TP53 down (S3.3.p2), PPBP platelet marker up (S3.5.p4)"}

reasoning: Single paired before/after design. S2.5.p1 states DESeq2 on RSEM per-gene table retaining FDR<0.1; FIG1 caption states 'donor + exercise' design and 10% FDR; S3.2.p1 justifies donor covariate. No fold-change cutoff for the headline DEG count (the |log2FC|>=0.5 and TPM>=10 filters in S3.5.p4 are a later prioritization of altitude-specific genes, not the DE threshold).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE164890\\GSE164890_rsem.genes.counts.tsv.gz", "owned": true, "checks": ["S2.3.p1 and S10.p1 name GSE164890", "14 samples = 7 skaters x before/after as in S2.3.p1", "GEO tissue 'whole blood (globin-depleted)', Homo sapiens, RSEM v1.2.31 in data_processing matches S2.4.p1"], "accession": "GSE164890", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE164890\\GSE164890_metadata.csv"}

reasoning: Paper deposits its data under GSE164890 (S2.3.p1, S10.p1); GEO sample titles 'Skater N - before/after exercise' and RSEM processing match the methods.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 14, "n_metadata": 14, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\aligned\\aligned_metadata.csv", "columns": {"subject": {"source": "description", "regex": "^(\\d+)(?:before|after)$", "recode": {"1": "S1", "2": "S2", "3": "S3", "4": "S4", "5": "S5", "6": "S6", "7": "S7"}}, "time": {"source": "description", "regex": "^\\d+(before|after)$", "recode": {"before": "pre", "after": "post"}}}, "output": "E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\aligned\\design_metadata.csv", "sha256": "60fe617e1b25aa18cabf0a0f06e50b29aceb4a8e8f63da86136cddd36b5882dd", "levels": {"subject": {"S1": 2, "S2": 2, "S3": 2, "S4": 2, "S5": 2, "S6": 2, "S7": 2}, "time": {"pre": 7, "post": 7}}}}

reasoning: Matrix columns (1before, 1after, ...) equal the GEO 'description' field exactly for 14/14 samples (inspect alignment_keys). Subject number and time point parsed from that key; consistent with titles 'Skater N - before/after exercise' and the 'time point' characteristic.

### matrix (valid, not_started)

final: {"source": "GSE164890_rsem.genes.counts.tsv.gz", "paper_input": "RSEM per-gene expression table (counts) into DESeq2 (S2.5.p1)", "matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\aligned\\aligned_matrix.csv", "sha256": "070aa5aef5c871d3a68d76d37786a42d89f3d9ab6489c7039002a938bc1f715f", "n_features": 58233, "n_samples": 14, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 561674.74, "median": 0.0, "integer_fraction": 0.9451, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File GSE164890_rsem.genes.counts.tsv.gz: RSEM expected counts (S2.4.p1; data_processing RSEM v1.2.31), 94.5% integer values with fractional remainder, max 5.6e5 - consistent with RSEM estimated counts, not TPM (separate TPM file exists). Paper fed this per-gene RSEM table to DESeq2 (S2.5.p1); rounding to integers is the standard way to use RSEM expected counts in DESeq2.

rejected alternatives: [{"value": "GSE164890_rsem.genes.TPM.tsv.gz (TPM)", "reason_rejected": "length-normalized; paper's DESeq2 input was the count table"}]

### design (valid, not_started)

final: {"analysis_type": "paired two-group (repeated measures)", "design_column": "time", "control": "pre", "treatment": "post", "contrasts": [{"name": "time_post_vs_pre", "control": "pre", "treatment": "post", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: One factor (time: before/after exercise) measured twice within each of 7 donors; the paper's estimand is the within-donor exercise effect (FIG1 'donor + exercise'). No other grouping column exists in GEO metadata.

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking factor (donor fixed effect), as in the paper's donor + exercise design"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 14, "n_columns": 8, "columns": ["Intercept", "time_pre", "subject_S2", "subject_S3", "subject_S4", "subject_S5", "subject_S6", "subject_S7"], "rank": 8, "full_rank": true, "residual_df": 6, "levels": {"time": {"pre": 7, "post": 7}, "subject": {"S1": 2, "S2": 2, "S3": 2, "S4": 2, "S5": 2, "S6": 2, "S7": 2}}, "cells": [{"cell": ["post", "S1"], "n": 1}, {"cell": ["post", "S2"], "n": 1}, {"cell": ["post", "S3"], "n": 1}, {"cell": ["post", "S4"], "n": 1}, {"cell": ["post", "S5"], "n": 1}, {"cell": ["post", "S6"], "n": 1}, {"cell": ["post", "S7"], "n": 1}, {"cell": ["pre", "S1"], "n": 1}, {"cell": ["pre", "S2"], "n": 1}, {"cell": ["pre", "S3"], "n": 1}, {"cell": ["pre", "S4"], "n": 1}, {"cell": ["pre", "S5"], "n": 1}, {"cell": ["pre", "S6"], "n": 1}, {"cell": ["pre", "S7"], "n": 1}], "min_cell_size": 1, "missing_values": {}}, "confounding": [{"column": "subject", "n_levels": 7, "status": "crossed", "crosstab": {"post": {"S1": 1, "S2": 1, "S3": 1, "S4": 1, "S5": 1, "S6": 1, "S7": 1}, "pre": {"S1": 1, "S2": 1, "S3": 1, "S4": 1, "S5": 1, "S6": 1, "S7": 1}}}]}

reasoning: S3.2.p1 shows a strong donor effect on PCA and the paper models donor as a covariate (FIG1). Each donor contributes one pre and one post sample, so subject is crossed with, not confounded by, time.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ subject + time", "rounding_documented": true, "paper_route": {"method": "DESeq2 ~ donor + exercise", "status": "reproduced"}, "deviations": ["RSEM expected counts rounded to integers before DESeq2 (paper does not state rounding; DESeq2 requires integers)", "pydeseq2 instead of R DESeq2 v1.18.1"], "transform": "round"}

reasoning: Paper route DESeq2 ~ donor + exercise on RSEM counts is executable on the deposited count table after rounding (S2.5.p1, FIG1).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: S2.5.p1 'retaining genes with FDR < 0.1'; FIG1 'reported at 10% FDR'; no fold-change cutoff for the DEG list. Audit at padj<0.05 is a separate labelled comparison rule.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "time_post_vs_pre", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 14, "matrix": "E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\transformed\\rounded_counts.csv", "transform": "round", "formula": "~ subject + time", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\results\\time_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"time_post_vs_pre": {"applied": {"rule": "padj < 0.1", "n_tested": 15634, "n_significant": 4243, "n_up": 2588, "n_down": 1655, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15634, "n_significant": 3238, "n_up": 2114, "n_down": 1124, "deg_sanity": "ok"}}}}

reasoning: Paper's DESeq2 ~ donor + exercise, post vs pre, FDR 0.1

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\results\\enrichment_time_post_vs_pre\\ora\\DEG_results_post_vs_pre_GO_Biological_Process_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\results\\enrichment_time_post_vs_pre\\ora\\DEG_results_post_vs_pre_GO_Cellular_Component_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\results\\enrichment_time_post_vs_pre\\ora\\DEG_results_post_vs_pre_GO_Molecular_Function_2023.csv", "E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\results\\enrichment_time_post_vs_pre\\ora\\DEG_results_post_vs_pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 4132 Human genes (direction=all, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Phosphorylation (GO:0016310) | padj=1.19e-08 | overlap=150/429 | genes=DGKG;PANK2;PRAG1;MAML1;GMFG;PPP4R1;TBK1;GNPTAB;RPS6KA1;PDK3;PIM2;PRKACA;MAP3K5;A - Positive Regulation Of Intracellular Signal Transduction (GO:1902533) | padj=1.19e ... [1103 more characters]

reasoning: Paper reports Hallmark ORA and fGSEA (S3.3, FIG2); Hallmark only here (CP collection not available in runner).

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "time_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_11/run/GSE164890\\results\\enrichment_time_post_vs_pre\\gsea\\DEG_results_post_vs_pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 23536 Human genes ranked by 'stat'. 50 Hallmark sets tested, 39 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.50 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=2.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.17 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APOPTOSIS | NES=2.11 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.05 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TGF_BETA_SIGNALING | NES=2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=1.99 | NOM p=0.00e+00 | FDR q=1.23e-04 - HALLMARK_PROTEIN_SECRETION | NES=1.96 | NOM p=0.00e+00 | FDR q=1.11e-04 ### Top 7 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=-2.45 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=-1.41 | NOM p=0.00e+00 | FDR q=6.47e-02 - HALLMARK_E2F_TARGETS | NES=-1.33  ... [368 more characters]

reasoning: Paper reports Hallmark ORA and fGSEA (S3.3, FIG2); Hallmark only here (CP collection not available in runner).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["estimated counts rounded", "pydeseq2 vs R DESeq2 1.18 independent filtering/dispersion details may shift counts", "altitude-specific filtering against 7 microarray datasets (S3.5) not reproduced", "no sea-level control: the estimand is exercise at altitude, not altitude itself (S3.5.p1)"], "results": {"time_post_vs_pre": {"n_deg": 4243, "up": 2588, "down": 1655, "rule": "padj < 0.1", "audit_n": 3238}}, "paper_counts": {"time_post_vs_pre": 4058}, "comparison": {"time_post_vs_pre": {"ours": 4243, "paper": 4058}}, "paper_gene_check": {"time_post_vs_pre": {"MARC1": null, "PHOSPHO1": {"baseMean": 12458.2771, "log2FoldChange": 0.5397, "padj": 0.0044, "pvalue": 0.0004}, "PPBP": {"baseMean": 3678.0613, "log2FoldChange": 0.5282, "padj": 0.0001, "pvalue": 0.0}, "MYC": {"baseMean": 1655.3698, "log2FoldChange": -0.3623, "padj": 0.0044, "pvalue": 0.0004}, "TP53": {"baseMean": 1253.9198, "log2FoldChange": -0.2684, "padj": 0.0287, "pvalue": 0.0048}}}}

reasoning: Paper reports 2516 up + 1542 down = 4058 DEGs at FDR<0.1 (S3.2.p2). Named genes: MARC1, PHOSPHO1 up (S3.5.p5-6), PPBP up (S3.5.p4), MYC and TP53 down (S3.3.p2).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 14 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "count rounding",
    "paper": "RSEM per-gene table into DESeq2 (rounding not stated)",
    "data": "RSEM expected counts with fractional values",
    "disposition": "executable_without_change"
  },
  {
    "item": "estimand scope",
    "paper": "title frames 'exercise at altitude'; altitude-specific genes via cross-study filter (S3.5)",
    "data": "only pre/post at altitude; no sea-level arm",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE164890 (PMC9027771, elite speed skaters, whole blood before/after exercise at altitude)

## What ran
- Route: case spec (`case_spec.json`) through `python -m tools.case_runner execute`; validator: 12 records, 0 errors; status completed, route `paper_aligned`.
- Matrix: `GSE164890_rsem.genes.counts.tsv.gz` (RSEM expected counts, 94.5% integer, 58,233 genes x 14 samples), rounded to integers (`transform: round`, documented).
- Alignment: exact on GEO `description` (14/14). `subject` (S1-S7) and `time` (pre/post) parsed from the key.
- Design: paired, 7 donors x pre/post. DESeq2 (pydeseq2 Wald), `~ subject + time`, post vs pre. This is the paper's "donor + exercise" design (S2.5.p1, FIG1).
- Threshold: paper's FDR < 0.1, no fold-change cutoff (S2.5.p1, FIG1). Audit rule: padj < 0.05.
- Enrichment: Hallmark preranked GSEA (stat ranking) plus Enrichr ORA (GO/KEGG). The paper used Hallmark + MSigDB CP with clusterProfiler/fGSEA; the CP collection was not available, so it was not run.

## DEG counts vs the paper (FDR < 0.1)
| Contrast | Ours (up / down / total) | Paper (up / down / total) |
|---|---|---|
| post vs pre, paired | 2588 / 1655 / 4243 | 2516 / 1542 / 4058 (S3.2.p2) |

- Audit at padj < 0.05: 3238 DEGs.
- More than twofold (unshrunk LFC, among FDR < 0.1): 131 up / 93 down. Paper: 104 / 58 (S3.2.p2; the paper's LFC estimator is unknown).
- Named genes, all significant in the paper's direction:
  - MARC1 (ENSG00000186205): LFC +1.23, padj 1e-7
  - PHOSPHO1: +0.54, padj 0.004
  - PPBP: +0.53, padj 1e-4
  - MYC: -0.36, padj 0.004
  - TP53: -0.27, padj 0.029
- GSEA agrees with the paper's FIG2:
  - Up: TNFa/NF-kB, complement, inflammatory, apoptosis, IFN-gamma/alpha, IL6/JAK/STAT3, hypoxia and coagulation, all at FDR ~0.
  - Down: HALLMARK_MYC_TARGETS_V2 is the only strongly significant down set (NES -2.45, FDR 0), as the paper reports.

## Deviations
- RSEM expected counts were rounded before DESeq2. The paper does not state how it handled them.
- pydeseq2 was used instead of R DESeq2 v1.18.1. Differences in dispersion and independent filtering likely explain the roughly 5% higher DEG count.
- The paper's altitude-specific filtering against 7 public microarray datasets (S3.5) and its scRNA-based cell-type deconvolution (S3.4) were not reproduced; they are outside the DE route.
- The estimand is exercise at altitude (pre vs post). There is no sea-level arm, so no altitude effect can be estimated (S3.5.p1).

## Tool problems
- `tools/case_runn ... [605 more characters]
