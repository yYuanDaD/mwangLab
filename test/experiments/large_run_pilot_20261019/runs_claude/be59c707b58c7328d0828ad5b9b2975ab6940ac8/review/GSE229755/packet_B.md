# Review packet B (the analysis' decisions): GSE229755

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.1.treatment", "pairs_or_sets": 6, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_Exe_vs_Con | 88 | 0 | padj <= 0.05 and |log2FoldChange| > 1 | 0 | 0 | 0 | 0 | 645 | 30 | 6 | 121 | 0.095 | 0.061 |

## Samples per design level

### `grp`
- **Con** (6): GSM7177389 / Con_L1; GSM7177390 / Con_L2; GSM7177391 / Con_L3; GSM7177392 / Con_L4; GSM7177393 / Con_L5; GSM7177394 / Con_L6
- **Exe** (6): GSM7177395 / Exe_L1; GSM7177396 / Exe_L2; GSM7177397 / Exe_L3; GSM7177398 / Exe_L4; GSM7177399 / Exe_L5; GSM7177400 / Exe_L6

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE229755"], "other_accessions": ["PXD041538 (proteomics/acetylome, not analyzed here)", "MTBLS7609 (metabolomics, not analyzed here)"], "assay": "bulk RNA-seq of liver, DNBseq PE150, HISAT2 to GRCm39", "organism": "Mouse (C57BL/6J male, 8 weeks)", "factors": {"group": ["Con (sedentary)", "Exe (6-week moderate treadmill running)"]}, "sample_inclusion": "12 mice for transcriptomics, n = 6 per group (S2.3.p1); PCA was used to exclude outliers but none are reported excluded from the n = 6 + 6", "primary_estimand": "Effect of 6 weeks of chronic moderate-intensity treadmill exercise on the mouse liver transcriptome (Exe vs Con, independent animals)", "planned_contrasts": ["Exe vs Con (S3.1.p1; paper: 88 DEGs, 28 up / 60 down)"], "repeated_measure_unit": "none (one liver per mouse)", "paper_method": "DESeq (S2.4.p1) on read counts", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": false, "source_locator": "S2.4.p1"}, "paper_results": "88 DEGs (28 up, 60 down); Cyp4a10, Cyp4a14 up at mRNA and protein; Cyp1a1 in retinol metabolism (S3.1.p1, S3.3.p1)"}

reasoning: S2.1.p1: two randomized groups Exe and Con; S2.3.p1: n = 6 per group for transcriptomics; S2.4.p1: DESeq, |log2FC| > 1 and Q-value <= 0.05; S3.1.p1: 88 DEGs (28 up, 60 down); S3.3.p1 and S4.p2: Cyp4a10 and Cyp4a14 upregulated.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE229755\\GSE229755_fpkm_merged.csv", "owned": true, "checks": ["S6.p1 names GSE229755 as the transcriptomics deposit", "GEO: liver, Mus musculus, 12 samples Con_L1-6 and Exe_L1-6, treatment sedentary vs chronic exercise running 6 weeks", "extract_protocol and data_processing match S2.4.p1 (TRIzol, DNBseq PE150, HISAT to GCF_000001635.27_GRCm39)", "sample counts 6 + 6 match S2.3.p1"], "accession": "GSE229755", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE229755\\GSE229755_metadata.csv"}

reasoning: Data availability statement S6.p1 names GSE229755; the 12 GEO samples and processing text match the paper's transcriptomics methods.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(Con|Exe)_L\\d+$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\aligned\\design_metadata.csv", "sha256": "e23ecf1b457ef820be28fcdf47347f020a0d1fce3224d52f5fcdc6249260f0e1", "levels": {"grp": {"Con": 6, "Exe": 6}}}}

reasoning: The merged matrix columns are GSM ids taken from the _RAW.tar member names (GSM7177389_Con_L1.txt.gz ...), which equal the metadata index. Group derived from title (Con_L# / Exe_L#), consistent with characteristics treatment (sedentary / chronic exercise).

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\aligned\\aligned_matrix.csv", "sha256": "b61e11679f222b67a476852dfe679c134d1d3784ad650d083f1af1c7e2f3ace1", "n_features": 16821, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 48014.79, "median": 2.38, "integer_fraction": 0.1272, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: The only deposited expression data are per-sample files with a single value column named fpkm_<title> holding non-integer values (median 2.3, max 3.8e4) indexed by Entrez gene_id and gene_symbol; no read-count file exists in GEO. The paper's DESeq input (raw counts) was not deposited. Merged by prep_merge_fpkm.py (16,821 genes, duplicated symbols resolved by highest mean).

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "Con", "treatment": "Exe", "contrasts": [{"name": "grp_Exe_vs_Con", "control": "Con", "treatment": "Exe", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: S2.1.p1 randomizes mice to Exe and Con; S3.1.p1 compares Exe with Con. One two-level factor, independent animals, all male.

rejected alternatives: [{"value": "description column", "reason_rejected": "identical split to title/treatment; title gives short formula-safe levels"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 12, "n_columns": 2, "columns": ["Intercept", "grp_Exe"], "rank": 2, "full_rank": true, "residual_df": 10, "levels": {"grp": {"Con": 6, "Exe": 6}}, "cells": [{"cell": ["Con"], "n": 6}, {"cell": ["Exe"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.treatment", "n_levels": 2, "status": "complete_confounding", "crosstab": {"Con": {"chronic exercise, running for 6 weeks": 0, "sedentary": 6}, "Exe": {"chronic exercise, running for 6 weeks": 6, "sedentary": 0}}}, {"column": "molecule_ch1", "n_levels": 1, "status": "constant"}, {"column": "extract_protocol_ch1", "n_levels": ... [1375 more characters]

reasoning: Independent animals, one sample each; no batch, sex (all male, S2.1.p1) or lane covariate recorded in GEO; the paper models group only.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (limma-trend on log2(FPKM+1))", "formula": "~ grp", "paper_route": {"method": "DESeq on read counts", "status": "blocked", "reason": "GEO GSE229755 deposits only per-sample FPKM; no raw counts are available, and FPKM must not be rounded into counts"}, "deviations": ["limma on log2(FPKM+1) instead of DESeq on counts", "genes with FPKM < 1 in more than 9 of 12 samples removed (FPKM >= 1 in at least 3 samples) before limma, replacing DESeq's independent filtering; unfiltered run kept as sensitivity"], "transform": "log2(x+1)"}

reasoning: Matrix policy: FPKM -> log2(x+1) -> limma. DESeq is blocked because counts are not deposited; run limma as a declared deviation with the paper's threshold.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper's Q-value <= 0.05 and |log2FC| > 1 applied to limma BH-adjusted p and log2FC of log2(FPKM+1) instead of DESeq on counts."}

reasoning: S2.4.p1 and S3.1.p1: |log2FC| > 1 and Q-value <= 0.05 (Q-value read as BH-adjusted p). Audit rule: BH < 0.05 with no fold-change cutoff.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_Exe_vs_Con", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\results\\grp_Exe_vs_Con\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\results\\grp_Exe_vs_Con\\DEG_results_Exe_vs_Con.csv"], "counts": {"grp_Exe_vs_Con": {"applied": {"rule": "padj <= 0.05 and |log2FoldChange| > 1", "n_tested": 10558, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 10558, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paper's Exe vs Con contrast on the deviation route (limma on log2(FPKM+1)); unexpressed genes removed (FPKM >= 1 in at least 3 of 12 samples, the smallest group size being 6).

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_Exe_vs_Con_unfiltered", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\results\\grp_Exe_vs_Con_unfiltered\\DEG_results_Exe_vs_Con.csv"], "counts": {"grp_Exe_vs_Con_unfiltered": {"applied": {"rule": "padj <= 0.05 and |log2FoldChange| > 1", "n_tested": 16804, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16804, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Same contrast without the expression filter, to show the filter's effect on counts.

### enrichment (valid, not_run)

final: {"organism": "Mouse", "subset": "grp_Exe_vs_Con", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "inclusive": true, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": false}, "direction": "all", "input_threshold_source": "applied", "reason_not_run": "no gene passes the ORA input threshold"}

reasoning: Paper reports GO/KEGG enrichment of the DEGs (S2.4.p1, S3.1.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_Exe_vs_Con", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\be59c707b58c7328d0828ad5b9b2975ab6940ac8\\GSE229755\\results\\enrichment_grp_Exe_vs_Con\\gsea\\DEG_results_Exe_vs_Con_GSEA_Hallmark.csv"], "summary": "GSEA complete on 10558 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 29 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=1.80 | NOM p=0.00e+00 | FDR q=1.86e-03 - HALLMARK_XENOBIOTIC_METABOLISM | NES=1.60 | NOM p=0.00e+00 | FDR q=2.31e-02 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.51 | NOM p=1.21e-03 | FDR q=4.74e-02 - HALLMARK_ADIPOGENESIS | NES=1.37 | NOM p=3.09e-02 | FDR q=1.55e-01 - HALLMARK_UNFOLDED_PROTEIN_RESPONSE | NES=1.26 | NOM p=1.09e-01 | FDR q=2.98e-01 - HALLMARK_MYC_TARGETS_V2 | NES=1.26 | NOM p=1.26e-01 | FDR q=2.62e-01 - HALLMARK_GLYCOLYSIS | NES=1.24 | NOM p=9.18e-02 | FDR q=2.69e-01 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.12 | NOM p=2.95e-01 | FDR q=5.22e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=-1.98 | NOM p=0.00e+00 | FDR q=2.84e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=-1.83 | NOM  ... [411 more characters]

reasoning: Paper reports GO/KEGG enrichment of the DEGs (S2.4.p1, S3.1.p1).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Counts not deposited: limma-trend on log2(FPKM+1) replaces DESeq on counts, so DEG numbers are not directly comparable", "Fold changes on log2(FPKM+1) are shrunk toward zero for low-expressed genes compared with DESeq count fold changes"], "results": {"grp_Exe_vs_Con": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj <= 0.05 and |log2FoldChange| > 1", "audit_n": 0}, "grp_Exe_vs_Con_unfiltered": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj <= 0.05 and |log2FoldChange| > 1", "audit_n": 0}}, "paper_counts": {"grp_Exe_vs_Con": 88}, "comparison": {"grp_Exe_vs_Con": {"ours": 0, "paper": 88}}, "paper_gene_check": {"grp_Exe_vs_Con": {"Cyp4a10": {"AveExpr": 6.8307, "log2FoldChange": 1.1732, "padj": 0.6935, "pvalue": 0.0012}, "Cyp4a14": {"AveExpr": 5.0026, "log2FoldChange": 2.1261, "padj": 0.7274, "pvalue": 0.0018}, "Cyp1a1": null}}}

reasoning: Paper reports 88 DEGs (28 up, 60 down) and names Cyp4a10/Cyp4a14 (up) and Cyp1a1 among retinol metabolism DEGs.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE input",
    "paper": "DESeq on read counts (S2.4.p1)",
    "data": "GEO deposits only per-sample FPKM",
    "disposition": "declared_deviation"
  },
  {
    "item": "reference genome",
    "paper": "GRCm39 (S2.4.p1)",
    "data": "GEO data_processing also says 'Assembly: mm10' and mentions Bowtie2 to reference gene sequences",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE229755 (PMC10318136, chronic exercise and mouse liver)

## What ran
- `case_runner inspect GSE229755`: GEO holds only `GSE229755_RAW.tar` with 12 per-sample files (`GSM*_Con_L1..6`, `GSM*_Exe_L1..6`). Each file has one value column, `fpkm_<title>`, plus Entrez `gene_id` and `gene_symbol`. No read counts are deposited.
- `prep_merge_fpkm.py` (listed in `prep_scripts`) merged the 12 FPKM files into `data/GSE229755/GSE229755_fpkm_merged.csv`: 16,821 genes x 12 GSM columns, indexed by symbol, with duplicate symbols resolved by highest mean.
- `case_runner execute case_spec.json`: completed. The validator checked 13 records and found 0 errors.
  - Alignment: exact match on the metadata index, 12/12 samples.
  - Groups: grp from title, Con 6, Exe 6. Suitability verdict: analyzable.
  - Primary: limma-trend on log2(FPKM+1), `~ grp`, Exe vs Con. Genes kept only if FPKM >= 1 in at least 3 samples (10,558 genes).
  - Sensitivity: the same model without the filter (16,804 genes).
  - Enrichment: Hallmark GSEA on the primary table completed. ORA was not run because there were 0 DEGs.

## DEG counts vs paper
Paper threshold (S2.4.p1, S3.1.p1): Q-value <= 0.05 and |log2FC| > 1. The paper reports 88 DEGs (28 up, 60 down) from DESeq on counts.

| Table | Ours, paper rule | Ours, BH < 0.05 only | Paper |
|---|---|---|---|
| grp_Exe_vs_Con (primary, filtered) | 0 | 0 | 88 (28 up / 60 down) |
| grp_Exe_vs_Con_unfiltered (sensitivity) | 0 | 0 | 88 |

- In the primary table the smallest BH-adjusted p is 0.58. 645 genes have nominal p < 0.05, and 6 genes pass nominal p < 0.05 with |log2FC| > 1.
- Named genes:
  - Cyp4a10 is up, log2FC 1.17, p = 0.0012, padj 0.69.
  - Cyp4a14 is up, log2FC 2.13, p = 0.0018, padj 0.73.
  - Both have the same direction as the paper, but neither survives FDR.
  - Cyp1a1 was removed by the expression filter (FPKM < 1 in most samples). In the unfiltered table it is log2FC +0.39, p = 0.20.
- Sample correlations on log2 FPKM are uniformly 0.98–0.99. There is no outlier and no visible group separation.

## Deviations
- The paper's route is blocked: DESeq on read counts needs counts, and GEO deposits only FPKM. The run used limma-trend on log2(FPKM+1) instead, recorded as a declared deviation with `threshold_source: paper_on_deviation_route`. FPKM was not rounded into counts.
- An FPKM >= 1 in at least 3 samples filter stands in for DESeq's independent filtering. This is my choice; the unfiltered run is kept as a sensitivity check.
- "Q-va ... [824 more characters]
