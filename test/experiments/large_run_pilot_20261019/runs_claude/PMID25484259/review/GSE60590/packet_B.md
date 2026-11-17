# Review packet B (the analysis' decisions): GSE60590

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_T2_vs_T1_pairs | 4076 | 1428 | padj < 0.05 | 1428 | 203 | 19 | 2367 | 3462 | 237 | 28 | 1823 | 0.052 | 0.28 |

## Samples per design level

### `grp`
- **T1** (11): GSM1482934 / 196 / Sample 3; GSM1482940 / 101 / Sample 9; GSM1482944 / 206 / Sample 13; GSM1482946 / 186 / Sample 15; GSM1482948 / 212 / Sample 17; GSM1482950 / 191 / Sample 19; GSM1482952 / 147 / Sample 21; GSM1482954 / 218 / Sample 23; GSM1482956 / 108 / Sample 25; GSM1482958 / 132 / Sample 27; GSM1482961 / 118 / Sample 30
- **T2** (22): GSM1482932 / 219 / Sample 1; GSM1482933 / 182 / Sample 2; GSM1482935 / 201 / Sample 4; GSM1482936 / 121 / Sample 5; GSM1482937 / 177 / Sample 6; GSM1482938 / 202 / Sample 7; GSM1482939 / 207 / Sample 8; GSM1482941 / 109 / Sample 10; GSM1482942 / 138 / Sample 11; GSM1482943 / 213 / Sample 12; GSM1482945 / 208 / Sample 14; GSM1482947 / 194 / Sample 16; GSM1482949 / 214 / Sample 18; GSM1482951 / 104 / Sample 20; GSM1482953 / 155 / Sample 22; GSM1482955 / 220 / Sample 24; GSM1482957 / 116 / Sample 26; GSM1482959 / 140 / Sample 28; GSM1482960 / 165 / Sample 29; GSM1482962 / 126 / Sample 31; GSM1482963 / 180 / Sample 32; GSM1482964 / 160 / Sample 33

### `subject`
- **s01** (2): GSM1482940 / 101 / Sample 9; GSM1482941 / 109 / Sample 10
- **s02** (2): GSM1482956 / 108 / Sample 25; GSM1482957 / 116 / Sample 26
- **s03** (2): GSM1482958 / 132 / Sample 27; GSM1482959 / 140 / Sample 28
- **s04** (1): GSM1482960 / 165 / Sample 29
- **s05** (2): GSM1482961 / 118 / Sample 30; GSM1482962 / 126 / Sample 31
- **s07** (1): GSM1482963 / 180 / Sample 32
- **s09** (1): GSM1482964 / 160 / Sample 33
- **s11** (1): GSM1482932 / 219 / Sample 1
- **s12** (1): GSM1482933 / 182 / Sample 2
- **s14** (2): GSM1482934 / 196 / Sample 3; GSM1482935 / 201 / Sample 4
- **s15** (1): GSM1482936 / 121 / Sample 5
- **s16** (1): GSM1482937 / 177 / Sample 6
- **s18** (1): GSM1482938 / 202 / Sample 7
- **s19** (1): GSM1482939 / 207 / Sample 8
- **s20** (1): GSM1482942 / 138 / Sample 11
- **s21** (1): GSM1482943 / 213 / Sample 12
- **s22** (2): GSM1482944 / 206 / Sample 13; GSM1482945 / 208 / Sample 14
- **s23** (2): GSM1482946 / 186 / Sample 15; GSM1482947 / 194 / Sample 16
- **s24** (2): GSM1482948 / 212 / Sample 17; GSM1482949 / 214 / Sample 18
- **s26** (2): GSM1482950 / 191 / Sample 19; GSM1482951 / 104 / Sample 20
- **s27** (2): GSM1482952 / 147 / Sample 21; GSM1482953 / 155 / Sample 22
- **s28** (2): GSM1482954 / 218 / Sample 23; GSM1482955 / 220 / Sample 24

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE58608", "GSE60590", "GSE60591"], "accession_roles": {"GSE58608": "RNA-seq, pre-training biopsies of both legs (T1 = leg to be trained, U1 = untrained leg) for 12 subjects; S5.4.p2 notes a baseline subset (n=12) analyzed earlier", "GSE60590": "RNA-seq, 22 post-training trained-leg biopsies (T2) plus 11 pre-training T1 biopsies of the other 11 subjects", "GSE60591": "GEO SuperSeries joining GSE58608 + GSE60590 (57 samples); not named in the paper but holds exactly the two cited series", "GSE60655": "DNA methylation 450K (S5.6.p1); not part of this gene-expression request"}, "assay": "bulk RNA-seq, Illumina HiSeq2000, 2x100 bp, vastus lateralis (S5.4.p1, S3.1.p1)", "primary_estimand": "Within-subject change in trained-leg skeletal-muscle gene expression after 3 months of supervised one-legged endurance knee-extension training: T2 (24 h after last session) vs T1 (pre-training), trained leg (S3.1.p1, S3.1.p2, S5.1.p1, S5.4.p2)", "planned_contrasts": ["T2 vs T1, trained leg, individual and library preparation as covariates (S5.4.p2; paper: 4076 DEGs, S3.1.p2)"], "factors": {"group": ["T1 pre-training trained leg", "T2 post-training trained leg"], "individual": "23 subjects (12 M, 11 F; TAB1)", "library_preparation": "covariate named in S5.4.p2; not annotated in GEO"}, "sample_inclusion": "23 sedentary young subjects; biopsies from both legs before and after training (S3.1.p1). RNA-seq DE is trained leg T2 vs T1 (S3.1.p2, S5.4.p2). The untrained leg is an intrain ... [1060 more characters]

reasoning: S5.4.p2 gives the RNA-seq DE: edgeR, group T2 vs T1 with library preparation and individual as covariates, FDR<0.05; S3.1.p2 reports 4076 DEGs. Design (one-legged training, biopsies pre/post) from S3.1.p1 and S5.1.p1. S5.6.p1 names GSE58608 and GSE60590 for expression.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60590\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S5.6.p1 cites GSE60590", "22 trained-leg post-training T2 + 11 pre-training T1 samples", "series_id GSE60590,GSE60591"], "accession": "GSE60590", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE60590\\GSE60590_metadata.csv"}

reasoning: S5.6.p1 names GSE58608 and GSE60590 as the gene-expression series. GSE60590 metadata: Homo sapiens skeletal muscle, KTH/SciLifeLab, HiSeq2000 RNA-seq, original sample IDs <subject><T|U><1|2> matching the paper's T1/T2 and trained/untrained leg scheme.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 33, "n_metadata": 33, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60590\\aligned\\aligned_metadata.csv", "columns": {"subject": {"source": "supplementary_file_1", "regex": "_(\\d+)[TU][12]\\.fpkm", "recode": {"1": "s01", "2": "s02", "3": "s03", "4": "s04", "5": "s05", "7": "s07", "9": "s09", "11": "s11", "12": "s12", "14": "s14", "15": "s15", "16": "s16", "18": "s18", "19": "s19", "20": "s20", "21": "s21", "22": "s22", "23": "s23", "24": "s24", "26": "s26", "27": "s27", "28": "s28"}}, "grp": {"source": "supplementary_file_1", "regex": "_\\d+([TU][12])\\.fpkm"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60590\\aligned\\design_metadata.csv", "sha256": "b22107a87034cd433c71a2eac11a6411265d72221f989cfe52807d0497d2674b", "levels": {"subject": {"s14": 2, "s01": 2, "s22": 2, "s23": 2, "s24": 2, "s26": 2, "s27": 2, "s28": 2, "s02": 2, "s03": 2, "s05": 2, "s11": 1, "s12": 1, "s15": 1, "s16": 1, "s18": 1, "s19": 1, "s20": 1, "s21": 1, "s04": 1, "s07": 1, "s09": 1}, "grp": {"T2": 22, "T1": 11}}}}

reasoning: Matrix columns are GSM ids. subject and grp (T1/T2) parsed from the per-sample file name in supplementary_file_1, equal to 'original sample id'. grp T2 = trained / post-training period 1, T1 = untrained / pre-training period 1 for all 33.

### matrix (valid, not_started)

final: {"source": "GEO per-sample Cufflinks genes.fpkm_tracking files in the _RAW.tar, merged on gene_id (FPKM column)", "paper_input": "gene read counts for edgeR (S5.4.p2); not deposited", "matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60590\\aligned\\aligned_matrix.csv", "sha256": "ba072c57cd4c7bba1ae576c7b849b3a528267f693aba41374d75841ce1fa6c5b", "n_features": 61779, "n_samples": 33, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 85707.6, "median": 0.0, "integer_fraction": 0.5911, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample files are Cufflinks genes.fpkm_tracking (FPKM, FPKM_conf_lo/hi, FPKM_status); data_processing: TopHat 2.0.4 + Cufflinks 2.0.2. Values are non-integer (integer fraction about 0.58, almost all zeros), max about 85,700: linear FPKM. No read counts deposited, so edgeR on counts cannot be reproduced; FPKM must not be rounded into counts. Route: log2(FPKM+1), then limma.

### design (valid, not_started)

final: {"analysis_type": "paired", "design_column": "grp", "control": "T1", "treatment": "T2", "contrasts": [{"name": "grp_T2_vs_T1", "control": "T1", "treatment": "T2", "role": "sensitivity"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60590\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Within-series sensitivity: only 11 subjects have both T1 and T2 in GSE60590 (the other 11 T2 baselines are in GSE58608). Paired T2 vs T1 on the 11 complete pairs avoids any cross-series (library-prep) effect. The full paper estimand runs in the GSE60591 case.

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "included"}, {"name": "library_preparation", "disposition": "excluded: not deposited; single series in this case"}, {"name": "sex", "disposition": "excluded: constant within subject, absorbed by the subject block"}], "design_check": {"formula_equivalent": "~ C(grp) + C(subject)", "n_samples": 33, "n_columns": 23, "columns": ["Intercept", "grp_T2", "subject_s02", "subject_s03", "subject_s04", "subject_s05", "subject_s07", "subject_s09", "subject_s11", "subject_s12", "subject_s14", "subject_s15", "subject_s16", "subject_s18", "subject_s19", "subject_s20", "subject_s21", "subject_s22", "subject_s23", "subject_s24", "subject_s26", "subject_s27", "subject_s28"], "rank": 23, "full_rank": true, "residual_df": 10, "levels": {"grp": {"T2": 22, "T1": 11}, "subject": {"s14": 2, "s01": 2, "s22": 2, "s23": 2, "s24": 2, "s26": 2, "s27": 2, "s28": 2, "s02": 2, "s03": 2, "s05": 2, "s11": 1, "s12": 1, "s15": 1, "s16": 1, "s18": 1, "s19": 1, "s20": 1, "s21": 1, "s04": 1, "s07": 1, "s09": 1}}, "cells": [{"cell": ["T1", "s01"], "n": 1}, {"cell": ["T1", "s02"], "n": 1}, {"cell": ["T1", "s03"], "n": 1}, {"cell": ["T1", "s05"], "n": 1}, {"cell": ["T1", "s14"], "n": 1}, {"cell": ["T1", "s22"], "n": 1}, {"cell": ["T1", "s23"], "n": 1}, {"cell": ["T1", "s24"], "n": 1}, {"cell": ["T1", "s26"], "n": 1}, {"cell": ["T1", "s27"], "n": 1}, {"cell": ["T1", "s28"], "n": 1}, {"cell": ["T2", "s01"], "n": 1},  ... [1283 more characters]

reasoning: The paper models individual (S5.4.p2). Subject is the blocking term for repeated biopsies.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (moderated t, eBayes) on log2(FPKM+1) with subject block", "formula": "~ Treatment + C(subject)", "paper_route": {"method": "edgeR on gene counts, ~ group + library preparation + individual", "status": "blocked", "reason": "GEO holds only Cufflinks FPKM per sample; neither read counts nor library-preparation labels were deposited"}, "deviations": ["limma on log2(FPKM+1) instead of edgeR on counts", "no library-prep covariate (single series)", "11 complete pairs only"], "transform": "log2(x+1)"}

reasoning: The paper route (edgeR on counts) is blocked: only Cufflinks FPKM is deposited. Validated alternative for linear FPKM: log2(FPKM+1), then limma (moderated t, eBayes) with subject as a fixed block, matching the paper's individual covariate. Genes are filtered to FPKM>=1 in at least as many samples as the smaller arm (analogous to the usual edgeR CPM filter) so the near-zero loci among the 61,779 Cufflinks genes are not tested.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S5.4.p2"}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "deviation_note": "The paper's FDR<0.05 (no fold-change cutoff) is applied unchanged to limma BH-adjusted p on log2(FPKM+1) because edgeR on counts is blocked. The audit rule adds |log2FC|>log2(1.5) only as a labelled comparison."}

reasoning: S5.4.p2: DEG were selected if FDR<0.05; no effect-size rule stated.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_T2_vs_T1_pairs", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 22, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60590\\results\\grp_T2_vs_T1_pairs\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60590\\results\\grp_T2_vs_T1_pairs\\DEG_results_T2_vs_T1.csv"], "counts": {"grp_T2_vs_T1_pairs": {"applied": {"rule": "padj < 0.05", "n_tested": 12376, "n_significant": 1428, "n_up": 899, "n_down": 529, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12376, "n_significant": 203, "n_up": 150, "n_down": 53, "deg_sanity": "ok"}}}}

reasoning: Paired T2 vs T1 within GSE60590 only (no cross-series batch); FPKM>=1 in >=11 samples (one arm).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Sensitivity on 11 within-series pairs, not the paper's full cohort", "FPKM with limma instead of counts with edgeR"], "results": {"grp_T2_vs_T1_pairs": {"n_deg": 1428, "up": 899, "down": 529, "rule": "padj < 0.05", "audit_n": 203}}, "paper_counts": {"grp_T2_vs_T1_pairs": 4076}, "comparison": {"grp_T2_vs_T1_pairs": {"ours": 1428, "paper": 4076}}, "paper_gene_check": {"grp_T2_vs_T1_pairs": {"COL4A1": {"AveExpr": 4.0562, "log2FoldChange": 1.5962, "padj": 0.000405, "pvalue": 1.31e-07}, "COL4A2": {"AveExpr": 4.0581, "log2FoldChange": 1.6112, "padj": 0.000405, "pvalue": 1.01e-07}, "A2M": {"AveExpr": 5.5829, "log2FoldChange": 0.734, "padj": 0.00201, "pvalue": 7.92e-06}, "THBS4": {"AveExpr": 4.2214, "log2FoldChange": 1.3822, "padj": 0.000788, "pvalue": 5.73e-07}, "PDGFRB": {"AveExpr": 3.7534, "log2FoldChange": 0.4591, "padj": 0.025, "pvalue": 0.00174}, "LAMA4": {"AveExpr": 2.3194, "log2FoldChange": 0.8601, "padj": 0.00604, "pvalue": 9.86e-05}, "CS": {"AveExpr": 7.4963, "log2FoldChange": 0.2329, "padj": 0.0442, "pvalue": 0.00466}, "SDHA": {"AveExpr": 7.1638, "log2FoldChange": 0.2864, "padj": 0.0132, "pvalue": 0.000548}, "HADHA": {"AveExpr": 6.6009, "log2FoldChange": 0.3661, "padj": 0.00689, "pvalue": 0.00013}, "COX7A2": {"AveExpr": 6.6931, "log2FoldChange": 0.5196, "padj": 0.00751, "pvalue": 0.00016}, "ATP5B": null, "MDH1": {"AveExpr": 8.1381, "log2FoldChange": 0.4999, "padj": 0.0045, "pvalue": 5.44e-05}, "NDUFA8": {"AveExpr": 6.3997, "log2 ... [1144 more characters]

reasoning: The paper's 4076 DEGs come from the full cohort; compared for scale only.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 33 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "edgeR on counts (S5.4.p2)",
    "data": "Cufflinks FPKM only",
    "disposition": "declared_deviation: limma on log2(FPKM+1)"
  },
  {
    "item": "sample set",
    "paper": "23 subjects T1 + 22 T2 trained leg",
    "data": "11 complete pairs in this series",
    "disposition": "sensitivity; full set in GSE60591"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 25484259 (Lindholm et al. 2014, Epigenetics; PMC4622000)

Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID25484259` (run label PMID25484259)
Spec: `case_spec.json` (built from a scratch script, not a driver). Runner: `python -m tools.case_runner execute`.
Validator: 28 records, 0 errors. Evaluator `audit_run.py --no-write`: verdict pass, score 100, coverage 90.2, no blocking findings.

## Paper (what it intends)
- Design: 23 sedentary young adults (12 M, 11 F) did 3 months of supervised one-legged knee-extension endurance training. Vastus lateralis biopsies were taken from both legs before (T1/U1) and 24 h after the last session (T2) (S3.1.p1, S5.1.p1).
- RNA-seq DE (S5.4.p2): edgeR on gene counts, with group (T2 vs T1, trained leg), library preparation and individual as covariates. Threshold **FDR < 0.05, no fold-change cutoff**. Result: **4076 DEGs** (S3.1.p2, S4.p2).
- Data (S5.6.p1): GSE58608 and GSE60590 are the expression series; GSE60655 is methylation and was not requested. GSE60591 is the GEO SuperSeries of the two expression series.

## Data facts
- All three series deposit only Cufflinks `genes.fpkm_tracking` files per sample (TopHat 2.0.4 + Cufflinks 2.0.2). There are **no read counts**, and there is no library-preparation annotation.
- GSE58608 (24 samples): 12 subjects x {T1, U1}, all taken before training.
- GSE60590 (33 samples): 22 T2 samples, plus 11 T1 samples from the 11 other subjects.
- GSE60591 (57 samples) = GSE58608 + GSE60590. It has T1 for 23 subjects and T2 for 22; subject 13 has no T2.
- Subject, arm (T1/T2/U1) and series batch were parsed from the per-sample file name in `supplementary_file_1` (`<subject><T|U><1|2>.fpkm`). This file name equals `original sample id`.

## What ran

| Case | Gate outcome | Model | Samples | DEGs at the paper's rule (padj<0.05) | Up / down | Paper |
|---|---|---|---|---|---|---|
| GSE58608 | **refused at design**: baseline only (T1/U1), no post-training sample | - | - | - | - | - |
| GSE60591 (primary) | declared deviation | limma on log2(FPKM+1), `~ Treatment + C(subject) + C(batch)` | 23 T1 + 22 T2 | **1608** | 1069 / 539 | 4076 |
| GSE60591 (sensitivity, no batch term) | declared deviation | limma, `~ Treatment + C(subject)` | 23 T1 + 22 T2 | **2576** | 1583 / 993 | 4076 |
| GSE60590 (sensitivity, pairs within the series) | declared deviation | limma, `~ Treatment + C(subject)`, complete pairs | 11 pairs | **1428** | 899 / 529 | 4076 |

- Gene filter:  ... [3623 more characters]
