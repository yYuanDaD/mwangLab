# Review packet B (the analysis' decisions): GSE87748

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.individual", "n_values": 10, "max_repeat": 2, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **other_rule_matches_paper**: {"table": "edgeR_paired/time_Post_vs_Pre", "paper": 165, "applied": 418, "applied_rule": "padj < 0.1", "closest_rule": "padj<0.05 & |lfc|>0.584963", "closest_n": 164, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| edgeR_paired/time_Post_vs_Pre | 165 | 418 | padj < 0.1 | 277 | 164 | 57 | 418 | 983 | 237 | 68 | 496 | 0.108 | 0.157 |

## Samples per design level

### `time`
- **Post** (10): GSM2339828 / 4_1_240; GSM2339830 / 5_1_240; GSM2339832 / 7_1_240; GSM2339834 / 8_1_240; GSM2339836 / 9_1_240; GSM2339838 / 11_1_240; GSM2339840 / 13_1_240; GSM2339842 / 14_1_240; GSM2339844 / 15_1_240; GSM2339846 / 16_1_240
- **Pre** (10): GSM2339829 / 4_1_Basal; GSM2339831 / 5_1_Basal; GSM2339833 / 7_1_Basal; GSM2339835 / 8_1_Basal; GSM2339837 / 9_1_Basal; GSM2339839 / 11_1_Basal; GSM2339841 / 13_1_Basal; GSM2339843 / 14_1_Basal; GSM2339845 / 15_1_Basal; GSM2339847 / 16_1_Basal

### `subject`
- **S04** (2): GSM2339828 / 4_1_240; GSM2339829 / 4_1_Basal
- **S05** (2): GSM2339830 / 5_1_240; GSM2339831 / 5_1_Basal
- **S07** (2): GSM2339832 / 7_1_240; GSM2339833 / 7_1_Basal
- **S08** (2): GSM2339834 / 8_1_240; GSM2339835 / 8_1_Basal
- **S09** (2): GSM2339836 / 9_1_240; GSM2339837 / 9_1_Basal
- **S11** (2): GSM2339838 / 11_1_240; GSM2339839 / 11_1_Basal
- **S13** (2): GSM2339840 / 13_1_240; GSM2339841 / 13_1_Basal
- **S14** (2): GSM2339842 / 14_1_240; GSM2339843 / 14_1_Basal
- **S15** (2): GSM2339844 / 15_1_240; GSM2339845 / 15_1_Basal
- **S16** (2): GSM2339846 / 16_1_240; GSM2339847 / 16_1_Basal

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE87748 (RNA-seq SubSeries of SuperSeries GSE87749, S5.p1)"], "assay": "total RNA-seq (Ribo-Zero), human vastus lateralis, HiSeq 2500 SR100", "primary_estimand": "within-subject change in skeletal-muscle gene expression 4 h after one 15-min bout of cycling at 80% VO2max vs resting basal biopsy, in 10 sedentary young men", "inclusion": "10 male volunteers, biopsies at rest (basal) and 4 h post-exercise (S2.1.p1); all 20 samples deposited", "factors": {"time": ["Basal (pre)", "240 min (post)"], "subject": "10 individuals, each sampled twice"}, "repeated_measure_unit": "subject (paired before/after biopsies)", "planned_contrasts": ["post-exercise (240 min) vs basal (S3.1.p1; paper: 165 DEGs, 72 up / 93 down, of 6,242 genes tested)"], "normalization": "featureCounts gene coverage; filter > 2.5 RPKM in >= 5 samples (S2.3.p1)", "paper_method": "edgeR glmQLFit/glmQLFTest (S2.3.p1; GEO data_processing edgeR v3.12.1); paired vs unpaired design not stated", "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.1.p1 + deposited GSE87748_RNAseq_stats.txt.gz (inferred)"}, "paper_results": "165 DEGs (72 up, 93 down); NR4A3 top up (FC 26, FDR 2.51e-5); Table 1 top-10 up genes"}

reasoning: S2.1.p1 defines the paired pre/4h-post biopsy design; S2.3.p1 the edgeR QL method and RPKM filter; S3.1.p1 the 165-DEG result. The paper never states the DEG cutoff. The authors' deposited result table (6,242 genes) gives exactly 165 genes at FDR < 0.1 (72 up / 93 down, identical to S3.1.p1) and 141 at FDR < 0.05; Table 1 also lists METTL7B with FDR 0.080. So the paper's rule is FDR < 0.1 with no fold-change cutoff (inferred, not stated).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\prep\\GSE87748_counts_paper_universe.csv", "owned": true, "checks": ["S5.p1 names GSE87749 (SuperSeries); GEO series_id lists GSE87748,GSE87749", "20 samples = 10 subjects x {Basal, 240 min}, matches S2.1.p1", "stats file has 6,242 genes = '6,242 genes detected' (S3.1.p1)", "data_processing matches S2.3.p1 (tophat2/featureCounts/edgeR QL)"], "accession": "GSE87748", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE87748\\GSE87748_metadata.csv"}

reasoning: The paper cites the SuperSeries GSE87749; GSE87748 is its RNA-seq SubSeries with the human biopsies. Sample count, tested-gene count and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 20, "n_metadata": 20, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\aligned\\aligned_metadata.csv", "columns": {"subject": {"source": "title", "regex": "^(\\d+)_1_(?:Basal|240)$", "recode": {"4": "S04", "5": "S05", "7": "S07", "8": "S08", "9": "S09", "11": "S11", "13": "S13", "14": "S14", "15": "S15", "16": "S16"}}, "time": {"source": "title", "regex": "^\\d+_1_(Basal|240)$", "recode": {"Basal": "Pre", "240": "Post"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\aligned\\design_metadata.csv", "sha256": "7b2a43fe2d0792b5893f3984425d1f203fededb557454d89f8f97cc1b5345147", "levels": {"subject": {"S04": 2, "S05": 2, "S07": 2, "S08": 2, "S09": 2, "S11": 2, "S13": 2, "S14": 2, "S15": 2, "S16": 2}, "time": {"Post": 10, "Pre": 10}}}}

reasoning: Matrix columns equal metadata title exactly (20/20). Subject and time parsed from the title; they agree with characteristics individual/time. Subject recoded to strings so R treats it as a factor.

### matrix (valid, not_started)

final: {"source": "GSE87748_RNAseq_Readcoverage_v3.txt.gz restricted to the authors' 6,242 tested genes", "paper_input": "featureCounts gene coverage (S2.3.p1)", "matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\aligned\\aligned_matrix.csv", "sha256": "60b0a470311f8d8c370d2a017f6f60ce97be72c383a31d58396a1fe23538f3af", "n_features": 6242, "n_samples": 20, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 5705050.0, "median": 260.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (0 to 5.7e6), file named Readcoverage, data_processing says featureCounts gene coverages: raw read counts, the input edgeR expects. The gene set is restricted to the authors' tested genes because the RPKM filter needs exon lengths that are not deposited (prep script).

### design (valid, not_started)

final: {"analysis_type": "paired two-group", "design_column": "time", "control": "Pre", "treatment": "Post", "contrasts": [{"name": "time_Post_vs_Pre", "control": "Pre", "treatment": "Post", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: One exercise bout, two time points per subject (S2.1.p1). The estimand is the within-subject change Post vs Pre; subject is the repeated-measure unit. GEO treatment exercise/control is the same split as time, so it is not a separate factor.

rejected alternatives: [{"value": "characteristics_ch1.1.treatment exercise vs control", "reason_rejected": "identical split to time; time is used"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "fixed blocking effect (~ subject + time)"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 20, "n_columns": 11, "columns": ["Intercept", "time_Pre", "subject_S05", "subject_S07", "subject_S08", "subject_S09", "subject_S11", "subject_S13", "subject_S14", "subject_S15", "subject_S16"], "rank": 11, "full_rank": true, "residual_df": 9, "levels": {"time": {"Post": 10, "Pre": 10}, "subject": {"S04": 2, "S05": 2, "S07": 2, "S08": 2, "S09": 2, "S11": 2, "S13": 2, "S14": 2, "S15": 2, "S16": 2}}, "cells": [{"cell": ["Post", "S04"], "n": 1}, {"cell": ["Post", "S05"], "n": 1}, {"cell": ["Post", "S07"], "n": 1}, {"cell": ["Post", "S08"], "n": 1}, {"cell": ["Post", "S09"], "n": 1}, {"cell": ["Post", "S11"], "n": 1}, {"cell": ["Post", "S13"], "n": 1}, {"cell": ["Post", "S14"], "n": 1}, {"cell": ["Post", "S15"], "n": 1}, {"cell": ["Post", "S16"], "n": 1}, {"cell": ["Pre", "S04"], "n": 1}, {"cell": ["Pre", "S05"], "n": 1}, {"cell": ["Pre", "S07"], "n": 1}, {"cell": ["Pre", "S08"], "n": 1}, {"cell": ["Pre", "S09"], "n": 1}, {"cell": ["Pre", "S11"], "n": 1}, {"cell": ["Pre", "S13"], "n": 1}, {"cell": ["Pre", "S14"], "n": 1}, {"cell": ["Pre", "S15"], "n": 1}, {"cell": ["Pre", "S16"], "n": 1}], "min_cell_size": 1, "missing_values": {}}, "confounding": [{"column": "subject", "n_levels": 10, "status": "crossed", "crosstab": {"Post": {"S04": 1, "S05": 1, "S07": 1,  ... [182 more characters]

reasoning: Each subject contributes both arms, so subject is blocked as a fixed effect (standard edgeR paired design). The paper does not say whether it paired; an unpaired ~ time fit runs as sensitivity.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "edgeR QL F-test (R edgeR, TMM)", "formula": "~ subject + time", "paper_route": {"method": "edgeR glmQLFit/glmQLFTest after > 2.5 RPKM in >= 5 samples", "status": "partially_reproduced", "reason": "RPKM filter replaced by the authors' deposited tested-gene list (no exon lengths deposited); pairing not stated in paper, paired design chosen"}, "deviations": ["gene universe = authors' 6,242 tested genes instead of recomputed RPKM filter", "edgeR 4.x (R 4.6) instead of 3.12.1", "pairing by subject assumed (not stated)"]}

reasoning: Raw counts support the paper's edgeR QL route; run it in R edgeR (tools.r_de_tools engine edger_ql, TMM) to match the paper's software. DESeq2 paired and edgeR unpaired are sensitivity runs.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "FDR < 0.1 inferred from the deposited author table (exactly 165 = 72 up/93 down); paper text does not state the cutoff. FDR < 0.05 kept as audit rule."}

reasoning: See paper_reconstruction: the deposited table reproduces S3.1.p1 exactly at FDR < 0.1, not 0.05.

### execution (valid, completed)

final: {"method": "run_r_de", "subset": "edgeR_paired", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\aligned\\aligned_matrix.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\results\\edgeR_paired\\DEG_results_time_Post_vs_Pre.csv"], "counts": {"edgeR_paired/time_Post_vs_Pre": {"applied": {"rule": "padj < 0.1", "n_tested": 6242, "n_significant": 418, "n_up": 205, "n_down": 213, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 6242, "n_significant": 277, "n_up": 142, "n_down": 135, "deg_sanity": "ok"}}}}

reasoning: paper's edgeR QL, paired by subject

### execution (valid, completed)

final: {"method": "run_r_de", "subset": "edgeR_unpaired", "role": "sensitivity", "tool": "tools.r_de_tools:run_r_de", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\aligned\\aligned_matrix.csv", "formula": "~ time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\results\\edgeR_unpaired\\DEG_results_time_Post_vs_Pre.csv"], "counts": {"edgeR_unpaired/time_Post_vs_Pre": {"applied": {"rule": "padj < 0.1", "n_tested": 6242, "n_significant": 257, "n_up": 118, "n_down": 139, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 6242, "n_significant": 181, "n_up": 88, "n_down": 93, "deg_sanity": "ok"}}}}

reasoning: the paper does not state pairing; tests which model the authors used

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "DESeq2_paired", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\aligned\\aligned_matrix.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID28066330\\GSE87748\\results\\DESeq2_paired\\DEG_results_Post_vs_Pre.csv"], "counts": {"DESeq2_paired": {"applied": {"rule": "padj < 0.1", "n_tested": 6242, "n_significant": 559, "n_up": 279, "n_down": 280, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 6242, "n_significant": 431, "n_up": 212, "n_down": 219, "deg_sanity": "ok"}}}}

reasoning: method robustness

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["threshold FDR < 0.1 is inferred from the authors' deposited table, not stated in text", "pairing of the original edgeR model is not stated", "gene universe taken from the authors' tested-gene list"], "results": {"edgeR_paired/time_Post_vs_Pre": {"n_deg": 418, "up": 205, "down": 213, "rule": "padj < 0.1", "audit_n": 277}, "edgeR_unpaired/time_Post_vs_Pre": {"n_deg": 257, "up": 118, "down": 139, "rule": "padj < 0.1", "audit_n": 181}, "DESeq2_paired": {"n_deg": 559, "up": 279, "down": 280, "rule": "padj < 0.1", "audit_n": 431}}, "paper_counts": {"edgeR_paired/time_Post_vs_Pre": 165}, "comparison": {"edgeR_paired/time_Post_vs_Pre": {"ours": 418, "paper": 165}}, "paper_gene_check": {"edgeR_paired/time_Post_vs_Pre": {"NR4A3": {"baseMean": 236.494, "log2FoldChange": 5.0145, "padj": 0.00239, "pvalue": 2.41e-05}, "PRKAG2": {"baseMean": 45.6241, "log2FoldChange": 2.603, "padj": 3.83e-06, "pvalue": 1.23e-09}, "RTN4RL1": {"baseMean": 3.7891, "log2FoldChange": 2.0623, "padj": 0.000139, "pvalue": 2.42e-07}, "WNT9A": {"baseMean": 17.9206, "log2FoldChange": 2.0719, "padj": 0.000264, "pvalue": 6.69e-07}, "CHST15": {"baseMean": 19.401, "log2FoldChange": 1.9788, "padj": 2.8e-05, "pvalue": 1.8e-08}, "FCN3": {"baseMean": 1.5362, "log2FoldChange": 1.8735, "padj": 0.000586, "pvalue": 2.25e-06}, "FKBP5": {"baseMean": 177.4604, "log2FoldChange": 1.7943, "padj": 0.00212, "pvalue": 1.94e-05}, "KCNQ4": {"baseMean": 4.6683, "log2FoldChange": 1.7423, "padj": 0. ... [143 more characters]

reasoning: Paper's method and contrast reproduced with declared deviations in filter, software version and assumed pairing.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 20 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "accession",
    "paper": "GSE87749 (SuperSeries)",
    "data": "GSE87748 RNA-seq SubSeries",
    "disposition": "executable_without_change"
  },
  {
    "item": "low-expression filter",
    "paper": "> 2.5 RPKM in >= 5 samples",
    "data": "no exon lengths deposited; authors' 6,242-gene tested list deposited",
    "disposition": "declared_deviation"
  },
  {
    "item": "DEG threshold",
    "paper": "not stated; 165 DEGs",
    "data": "authors' table gives 165 at FDR < 0.1",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID28066330 / GSE87748

**Status: finished** (decision `valid`, execution `completed`, route `declared_deviation`, validator: 12 records, 0 errors)

## What ran
- Paper (PMC5179501): 10 sedentary young men. Vastus lateralis biopsies were taken at rest and 4 h after a 15-min cycling bout at 80% VO2max (S2.1.p1). Total RNA-seq, featureCounts, genes with > 2.5 RPKM in ≥ 5 samples, edgeR glmQLFit/glmQLFTest (S2.3.p1). Result: 165 DEGs (72 up, 93 down) out of 6,242 genes; NR4A3 was the top up gene at 26-fold (S3.1.p1, Table 1). The paper cites the SuperSeries GSE87749. GSE87748 is its RNA-seq SubSeries.
- Matrix: `GSE87748_RNAseq_Readcoverage_v3.txt.gz`, integer featureCounts counts, 57,820 genes × 20 samples. Matched to metadata by exact `title`, 20/20. `subject` and `time` (Pre/Post) were parsed from the title.
- Gene universe: the RPKM filter needs exon lengths, which were not deposited. I restricted the matrix to the authors' own 6,242 tested genes from `GSE87748_RNAseq_stats.txt.gz` (script: `prep/restrict_to_paper_universe.py`). Counts are unchanged.
- Primary: R edgeR QL F-test with TMM, `~ subject + time`, coefficient `timePost` (`tools.r_de_tools:run_r_de`, engine `edger_ql`).
- Sensitivity runs: edgeR QL unpaired (`~ time`) and pydeseq2 paired (`~ subject + time`).
- Enrichment: not run. The paper reports no pathway analysis.

## Threshold
The paper's text never states the DEG cutoff. In the authors' deposited table, FDR < 0.1 gives exactly **165 (72 up / 93 down)**, which matches S3.1.p1. FDR < 0.05 gives 141. Table 1 also includes METTL7B at FDR 0.080. I therefore applied **FDR (BH) < 0.1 with no fold-change cutoff** as the paper's rule. This is inferred, not stated. FDR < 0.05 is kept as the audit rule.

## DEG counts vs paper (FDR < 0.1)
| Table | Ours (up/down) | Audit FDR<0.05 | Paper | Overlap with authors' 165 | logFC r vs authors |
|---|---|---|---|---|---|
| edgeR paired (primary) | 418 (205/213) | 277 | 165 (72/93) | 162/165 | 0.992 |
| edgeR unpaired | 257 (118/139) | 181 | — | 151/165 | 0.981 |
| DESeq2 paired | 559 (279/280) | 431 | — | 165/165 | 0.985 |

- All 10 genes in Table 1 go up in our primary table. NR4A3: log2FC 5.01 (≈ 32-fold vs the paper's 26), FDR 0.0024. PRKAG2: 2.60 (authors' 2.605). The other 7 found genes all have FDR < 0.001. METTL7B (ENSG00000170439) is also up: log2FC 1.52, FDR 0.049. It shows as `null` in the runner's gene check only because of the lookup problem described under Tool problems.
- Effect  ... [1501 more characters]
