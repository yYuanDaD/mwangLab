# Review packet B (the analysis' decisions): GSE272213

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_E_vs_NE | 22 | 0 | padj <= 0.05 and |log2FoldChange| >= 1 | 0 | 0 | 0 | 0 | 757 | 297 | 223 | 77 | 0.09 | 0.042 |
| grp_E_vs_NE_deseq2 | 22 | 0 | padj <= 0.05 and |log2FoldChange| >= 1 | 2 | 0 | 0 | 2 | 835 | 206 | 123 | 194 | 0.127 | 0.048 |

## Samples per design level

### `grp`
- **E** (5): GSM8395840 / E1; GSM8395841 / E2; GSM8395842 / E3; GSM8395843 / E4; GSM8395844 / E5
- **NE** (5): GSM8395845 / NE1; GSM8395846 / NE2; GSM8395847 / NE3; GSM8395848 / NE4; GSM8395849 / NE5

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE272213"], "assay": "bulk mRNA-seq (paired-end TruSeq) of 4T1 subcutaneous mammary tumours", "organism": "Mouse (female BALB/c, 5-6 weeks)", "sample_inclusion": "5 exercise (E, 21 days voluntary wheel running) + 5 non-exercise (NE) tumour-bearing mice; tumours collected at day 21 (S2.2.p1, S3.1.p1)", "factors": {"group": ["NE (non-exercise, reference)", "E (voluntary running)"]}, "primary_estimand": "Effect of 21 days of voluntary wheel running on gene expression in 4T1 breast tumours: E vs NE (S2.2.p1, S3.1.p1, Figure 1B-D)", "planned_contrasts": ["E vs NE in tumour tissue (S3.1.p1; paper: 22 DEGs; Cd300e down, 46% of NE, p = 0.008)"], "repeated_measure_unit": "none; one tumour per animal, animals randomised into two independent groups (S2.2.p1). S3.1.p1 says 'five matched pairs' but no pairing variable exists and animals were randomised independently", "normalization": "HISAT2 -> StringTie FPKM; TMM normalisation for library size (S2.3.p1)", "paper_method": "TMM-normalised differential expression (tool not named; TMM implies edgeR); DEG = fold change >= 2 and FDR <= 0.05 (S2.3.p1-p2)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "inclusive": true, "effect_metric": "fold change", "effect_cutoff": 1.0, "effect_note": "FC >= 2 -> |log2FC| >= 1", "source_locator": "S2.3.p2"}, "paper_results": {"n_deg": 22, "named_genes": {"Cd300e": "down in E, 46% of NE, p = 0.008"}, "pathways": ["KEGG MicroRNAs in cancer", "KEGG Calcium signaling pathway", "GO extra ... [90 more characters]

reasoning: Single exercise RNA-seq experiment in the paper (S2.2.p1, S2.3.p1-p2, S3.1.p1). Pan-cancer and cell experiments use public TCGA/GTEx data or in-vitro assays and are not part of GSE272213. The paper reports mapping to 'Rnor 6.0' (rat) although the mice are BALB/c; the deposited matrix uses ENSMUSG IDs, so this is a methods-text error recorded as a discrepancy.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE272213\\GSE272213_expression-TPL2024031661.txt.gz", "owned": true, "checks": ["S6.p1 names GSE272213", "GEO organism Mus musculus, tissue mammary cancer tissue", "10 GEO samples titled E1-E5 and NE1-NE5 match the paper's 5 E + 5 NE design", "matrix columns E1..E5, NE1..NE5 match GEO titles"], "accession": "GSE272213", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE272213\\GSE272213_metadata.csv"}

reasoning: Data availability statement S6.p1 cites GSE272213; sample names and group sizes match S2.2.p1.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 10, "n_metadata": 10, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(E|NE)\\d+$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\aligned\\design_metadata.csv", "sha256": "52e2ba760041d7b8314fab00f43141f4e3850db6683e68ddf4cd8f08e423ddc0", "levels": {"grp": {"E": 5, "NE": 5}}}}

reasoning: The matrix has paired '<title>:read count' and '<title>:fpkm' columns plus annotation columns; only the read-count columns are kept and their prefix equals GEO title. grp derives from the title prefix (E = exercise, NE = non-exercise), consistent with characteristics treatment (voluntary exercise condition / without intervention).

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\aligned\\aligned_matrix.csv", "sha256": "3ec490b5fb5e2433e39e3faf8cf2481e0170c940c03ef1ee9b289be4367bd451", "n_features": 21959, "n_samples": 10, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 369519.0, "median": 90.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: The kept columns are labelled 'read count'; all values are non-negative integers with no missing values and library sizes 15-23 M. The FPKM columns are dropped. The paper used StringTie FPKM with TMM normalisation (S2.3.p1); raw read counts are the appropriate input for a TMM-based count model.

rejected alternatives: [{"value": "FPKM columns with limma", "reason_rejected": "raw read counts for the same samples are deposited, and the paper's TMM normalisation is a count-based step"}]

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "NE", "treatment": "E", "contrasts": [{"name": "grp_E_vs_NE", "control": "NE", "treatment": "E", "role": "primary"}], "estimand_type": "interventional", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Randomised two-arm intervention (S2.2.p1): E vs NE, NE as reference. All mice female so no sex split. 'Five matched pairs' (S3.1.p1) is not supported by any pairing variable and the design text describes independent random allocation, so no subject block.

rejected alternatives: [{"value": "paired E_i vs NE_i blocking", "reason_rejected": "no pairing key in GEO or the paper; animals were randomised independently (S2.2.p1); pairing by sample number would be positional"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 10, "n_columns": 2, "columns": ["Intercept", "grp_NE"], "rank": 2, "full_rank": true, "residual_df": 8, "levels": {"grp": {"E": 5, "NE": 5}}, "cells": [{"cell": ["E"], "n": 5}, {"cell": ["NE"], "n": 5}], "min_cell_size": 5, "missing_values": {}}, "confounding": []}

reasoning: Independent animals, one tumour each; no batch, lane, or sex variation recorded in GEO.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "edgeR (TMM, QL F-test, inmoose)", "formula": "~ grp", "paper_route": {"method": "TMM-normalised DE (edgeR implied)", "status": "reproduced", "reason": "paper names TMM normalisation; tool not named"}, "deviations": ["No low-count filter (paper states none)", "Raw read counts used instead of StringTie FPKM as input; TMM computed by edgeR"]}

reasoning: S2.3.p1 states TMM normalisation, the edgeR normalisation, so edgeR on raw counts is the closest reproduction. DESeq2 runs as a sensitivity analysis.

rejected alternatives: [{"value": "DESeq2 as primary", "reason_rejected": "paper names TMM; DESeq2 kept as sensitivity"}]

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": true}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": true}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": true, "label": "raw-p audit: the paper names Cd300e as DE with p = 0.008 (S3.1.p1), suggesting its 22 DEGs may rest on raw p; this is a comparison rule, not the paper's stated rule"}}

reasoning: S2.3.p2: fold change >= 2 and FDR <= 0.05 -> BH padj <= 0.05 and |log2FC| >= 1 (inclusive). Audit: raw p <= 0.05 and |log2FC| >= 1, labelled as a comparison with the paper's apparent raw-p reporting (Cd300e p = 0.008 in S3.1.p1).

### execution (valid, completed)

final: {"method": "run_edger_analysis", "subset": "grp_E_vs_NE", "role": "primary", "tool": "tools.edger_tools:run_edger_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\results\\grp_E_vs_NE\\DEG_results_E_vs_NE.csv"], "counts": {"grp_E_vs_NE": {"applied": {"rule": "padj <= 0.05 and |log2FoldChange| >= 1", "n_tested": 17925, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue <= 0.05 and |log2FoldChange| >= 1", "n_tested": 17925, "n_significant": 223, "n_up": 78, "n_down": 145, "deg_sanity": "ok"}}}}

reasoning: Paper's TMM-normalised two-group comparison, E vs NE.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_E_vs_NE_deseq2", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\aligned\\aligned_matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\results\\grp_E_vs_NE_deseq2\\DEG_results_E_vs_NE.csv"], "counts": {"grp_E_vs_NE_deseq2": {"applied": {"rule": "padj <= 0.05 and |log2FoldChange| >= 1", "n_tested": 17479, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue <= 0.05 and |log2FoldChange| >= 1", "n_tested": 17479, "n_significant": 123, "n_up": 48, "n_down": 75, "deg_sanity": "ok"}}}}

reasoning: Method sensitivity: the paper's DE tool is not named.

### enrichment (valid, not_run)

final: {"organism": "Mouse", "subset": "grp_E_vs_NE", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": true}, "direction": "all", "input_threshold_source": "applied", "reason_not_run": "no gene passes the ORA input threshold"}

reasoning: Paper reports KEGG/GO on DEGs and GSEA (S2.3.p2, S3.1.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "grp_E_vs_NE", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39144140\\GSE272213\\results\\enrichment_grp_E_vs_NE\\gsea\\DEG_results_E_vs_NE_GSEA_Hallmark.csv"], "summary": "GSEA complete on 17864 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 34 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.80 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.76 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TGF_BETA_SIGNALING | NES=2.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.13 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.10 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.07 | NOM p=0.00e+00 | FDR q=2.63e-04 - HALLMARK_ANGIOGENESIS | NES=1.90 | NOM p=0.00e+00 | FDR q=1.15e-03 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.80 | NOM p=0.00e+00 | FDR q=2.05e-03 - HALLMARK_KRAS_SIGNALING_UP | NES=1.78 | NOM p=0.00e+00 | FDR q=2.03e-03 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.84 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.58 | NOM p=0.00e+00 | F ... [375 more characters]

reasoning: Paper reports KEGG/GO on DEGs and GSEA (S2.3.p2, S3.1.p1).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper says reads were mapped to Rnor 6.0 (rat) but the deposited matrix uses mouse Ensembl IDs; we use the deposited mouse matrix.", "Paper's DE tool is not named; edgeR is inferred from 'TMM'.", "Paper reports Cd300e p = 0.008, which is a raw p-value; it is not clear whether Cd300e passed the paper's FDR rule.", "At the paper's stated rule (FDR <= 0.05, |log2FC| >= 1) no gene is DE in our edgeR or DESeq2 fit (paper: 22). Cd300e direction and size agree with the paper (log2FC -1.09, about 47% of NE; edgeR p = 0.0035, FDR 0.82), but it does not pass FDR. The paper's 22 DEGs are not reproducible under its stated FDR rule and likely used raw p."], "results": {"grp_E_vs_NE": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj <= 0.05 and |log2FoldChange| >= 1", "audit_n": 223}, "grp_E_vs_NE_deseq2": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj <= 0.05 and |log2FoldChange| >= 1", "audit_n": 123}}, "paper_counts": {"grp_E_vs_NE": 22, "grp_E_vs_NE_deseq2": 22}, "comparison": {"grp_E_vs_NE": {"ours": 0, "paper": 22}, "grp_E_vs_NE_deseq2": {"ours": 0, "paper": 22}}, "paper_gene_check": {"grp_E_vs_NE": {"Cd300e": {"log2FoldChange": -1.0891, "padj": 0.823, "pvalue": 0.00346}}, "grp_E_vs_NE_deseq2": {"Cd300e": {"baseMean": 122.1312, "log2FoldChange": -1.0936, "padj": 0.302, "pvalue": 0.000346}}}}

reasoning: Primary edgeR contrast compared with the paper's 22 DEGs and Cd300e direction (down in E).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 10 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "reference genome",
    "paper": "Rnor 6.0 (rat) per S2.3.p1",
    "data": "ENSMUSG mouse gene IDs; GEO organism Mus musculus",
    "disposition": "executable_without_change"
  },
  {
    "item": "pairing",
    "paper": "'five matched pairs' (S3.1.p1)",
    "data": "no pairing variable; S2.2.p1 random allocation into two groups",
    "disposition": "executable_without_change"
  },
  {
    "item": "input scale",
    "paper": "StringTie FPKM, TMM-normalised",
    "data": "read count and FPKM columns both deposited; read counts used",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 39144140 / GSE272213

Paper: "Exercise-downregulated CD300E acted as a negative prognostic implication and tumor-promoted role in pan-cancer" (PMC11321962).
Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID39144140`. Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Validator: 13 records, 0 errors. Case status: valid / completed, route `paper_aligned`.

## What ran

- **Study map (paper):** female BALB/c mice with subcutaneous 4T1 tumours. They were randomised into exercise (E, 21 days of voluntary wheel running, n=5) and non-exercise (NE, n=5) groups, and tumours were sequenced at day 21 (S2.2.p1, S3.1.p1). The pan-cancer (TCGA/GTEx) and cell-line parts are not in GSE272213.
- **Ownership:** S6.p1 names GSE272213. The 10 GEO samples E1-E5 and NE1-NE5 match the matrix columns.
- **Matrix:** `GSE272213_expression-TPL2024031661.txt.gz` has side-by-side `<sample>:read count` and `<sample>:fpkm` columns plus annotations. I kept only the read-count columns (`matrix_column_pattern "^(.+):read count$"`) and aligned them exactly on GEO `title`. They are raw integer counts: no missing values, libraries of 15-23 M reads, mouse Ensembl IDs.
- **Design:** two groups, `~ grp`, NE as reference. No blocking (see deviations). The suitability report says analyzable.
- **Method:**
  - Primary: edgeR (TMM, QL F-test, inmoose). The paper names TMM normalisation (S2.3.p1) but not the DE tool.
  - Sensitivity: DESeq2 (pydeseq2 Wald).
  - No low-count filter, because the paper states none.
- **Threshold:**
  - Paper rule (S2.3.p2): FDR ≤ 0.05 and fold change ≥ 2, applied as BH padj ≤ 0.05 and |log2FC| ≥ 1, both inclusive.
  - Audit rule, labelled: raw p ≤ 0.05 and |log2FC| ≥ 1. I added it because the paper reports Cd300e with a raw p = 0.008.
- **Enrichment:**
  - GSEA (Hallmark, preranked on edgeR sign·sqrt(F)) completed.
  - ORA was not run: 0 genes pass the applied rule.

## DEG counts vs paper (paper rule: FDR ≤ 0.05, |log2FC| ≥ 1)

| Table | Ours, paper rule | Audit (raw p ≤ 0.05, \|log2FC\| ≥ 1) | Paper |
|---|---|---|---|
| grp_E_vs_NE (edgeR, primary) | 0 | 223 | 22 |
| grp_E_vs_NE_deseq2 (sensitivity) | 0 | 123 | 22 |

- **Lowest FDR:** edgeR min FDR = 0.82. DESeq2 has 2 genes at padj < 0.05, both with |log2FC| < 1.
- **Cd300e (ENSMUSG00000048498):**
  - edgeR: log2FC −1.09 (E/NE ≈ 0.47; the paper says 46%), p = 0.0035, FDR 0.82.
  - DESeq2: log2FC −1.09, p = 3.5e-4, padj 0.30.
  - The direction and siz ... [2691 more characters]
