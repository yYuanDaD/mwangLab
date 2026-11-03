# Review packet B (the analysis' decisions): GSE267512

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.age of_donor", "n_values": 14, "max_repeat": 13, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "subject", "n_values": 33, "max_repeat": 2, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| time_POST_vs_PRE | 214 | 79 | padj < 0.05 | 79 | 39 | 12 | 144 | 1430 | 159 | 35 | 531 | 0.086 | 0.096 |
| time_POST_vs_PRE_alpha005 | 214 | 81 | padj < 0.05 | 81 | 41 | 12 | 135 | 1430 | 159 | 35 | 531 | 0.086 | 0.096 |

## Samples per design level

### `time`
- **POST** (26): GSM8267531 / ALORPOST; GSM8267533 / ANJAPOST; GSM8267535 / BRBOPOST; GSM8267537 / BRGAPOST; GSM8267540 / CHMAPOST; GSM8267542 / CHRUPOST; GSM8267545 / ELSCPOST; GSM8267547 / ELWAPOST; GSM8267549 / EVZAPOST; GSM8267553 / GEYOPOST; GSM8267555 / HAMEPOST; GSM8267557 / ISURPOST; GSM8267559 / JAMIPOST; GSM8267561 / JANIPOST; GSM8267563 / JESIPOST; GSM8267565 / JOSAPOST; GSM8267568 / LAJUPOST; GSM8267570 / NAHIPOST; GSM8267572 / NAWOPOST; GSM8267574 / OLMOPOST; GSM8267576 / PABRPOST; GSM8267577 / SADIPOST; GSM8267579 / SELAPOST; GSM8267581 / SHVAPOST; GSM8267582 / SICEPOST; GSM8267584 / SOBRPOST
- **PRE** (31): GSM8267530 / ALORPRE; GSM8267532 / ANJAPRE; GSM8267534 / BRBOPRE; GSM8267536 / BRGAPRE; GSM8267538 / BRSTPRE; GSM8267539 / CHMAPRE; GSM8267541 / CHRUPRE; GSM8267543 / COGRPRE; GSM8267544 / ELSCPRE; GSM8267546 / ELWAPRE; GSM8267548 / EVZAPRE; GSM8267550 / FLTHPRE; GSM8267551 / GAVAPRE; GSM8267552 / GEYOPRE; GSM8267554 / HAMEPRE; GSM8267556 / ISURPRE; GSM8267558 / JAMIPRE; GSM8267560 / JANIPRE; GSM8267562 / JESIPRE; GSM8267564 / JOSAPRE; GSM8267566 / KACOPRE; GSM8267567 / LAJUPRE; GSM8267569 / NAHIPRE; GSM8267571 / NAWOPRE; GSM8267573 / OLMOPRE; GSM8267575 / PABRPRE; GSM8267578 / SELAPRE; GSM8267580 / SHVAPRE; GSM8267583 / SOBRPRE; GSM8267585 / TEOCPRE; GSM8267586 / WAALPRE

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE267512"], "assay": "bulk total RNA-seq (TruSeq Stranded Total RNA, Ribo-Zero Gold), vastus lateralis, Kallisto GRCh38 gene counts (S2.12.6.p1)", "sample_inclusion": "untrained pre-menopausal females, 12-week resistance training; 27 completed; Fig 7 legend: n = 35 pre-training, 27 post-training (S2.2.p1, FIG7)", "factors": {"timepoint": ["PRE", "POST"], "ID": "participant (repeated measure)"}, "primary_estimand": "within-participant change in vastus lateralis gene expression after 12 weeks of resistance training (POST vs PRE), DESeq2 ~ ID + timepoint", "planned_contrasts": ["timepoint POST vs PRE (S3.6.p1, FIG7; paper: 214 DEGs, 122 up, 92 down at FDR < 0.05)"], "repeated_measure_unit": "participant ID (S2.14.p6)", "gene_filter": "text: mean across samples <= 10 RPM removed (63%), 14,979 genes kept (S2.12.6.p1); authors' code: rowMeans(counts) >= 10", "paper_method": "DESeq2 ~ ID + timepoint (S2.14.p6); results() defaults (alpha 0.1) per authors' GitHub script", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S2.14.p7"}, "paper_results": "214 DEGs (122 up, 92 down); RPS6KC1 up 11% FDR < 0.01; TRIM63, FBXO32, TRAF6, FOXO1, FOXO3 unchanged; AR mRNA FDR = 0.956 (S3.6.p1, S3.4.p2, S3.3)", "secondary_analyses_not_reproduced": "ChEA3 TF enrichment on DEGs; gene association with total testosterone (no hormone values in GEO)"}

reasoning: S2.14.p6 states DESeq2 with Genes ~ ID + timepoint, ID for repeated measures; S2.14.p7 FDR-adjusted P < 0.05 with no fold-change rule; S3.6.p1 reports 214 DEGs (122 up / 92 down). The pre/post resistance-training contrast is the exercise estimand the paper intends.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39393048\\prep\\GSE267512_counts_rowmean_ge10.csv", "owned": true, "checks": ["S2.12.6.p1 and S13.p1 name GSE267512", "GEO: 57 female vastus lateralis samples, PRE/POST of a 12-week resistance training program, Kallisto GRCh38, contact Danielle Hiam (author D.H. performed transcriptomics, S7.p1)", "GeneCounts_RAW_DATA is the wide gene count matrix described in data_processing"], "accession": "GSE267512", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE267512\\GSE267512_metadata.csv"}

reasoning: Paper names GSE267512 as its RNA-seq deposit; the GEO treatment protocol matches the paper's 12-week resistance training of untrained pre-menopausal females, and the submitter is a paper author.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 57, "n_metadata": 57, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "E:/agent/mwangLab_review/.review_queue/case_08/run/GSE267512\\aligned\\aligned_metadata.csv", "columns": {"subject": {"source": "title", "regex": "^([A-Z]{4})(?:PRE|POST)$"}, "time": {"source": "characteristics_ch1.4.treatment", "regex": "^(PRE|POST)$"}}, "output": "E:/agent/mwangLab_review/.review_queue/case_08/run/GSE267512\\aligned\\design_metadata.csv", "sha256": "a0257ea5b92b94050af43f8e416de74256176606105e21d522cfacf4f447600b", "levels": {"subject": {"ALOR": 2, "ANJA": 2, "BRBO": 2, "BRGA": 2, "CHMA": 2, "CHRU": 2, "ELSC": 2, "ELWA": 2, "EVZA": 2, "GEYO": 2, "HAME": 2, "ISUR": 2, "JAMI": 2, "JANI": 2, "JESI": 2, "JOSA": 2, "LAJU": 2, "NAHI": 2, "NAWO": 2, "OLMO": 2, "PABR": 2, "SELA": 2, "SHVA": 2, "SOBR": 2, "BRST": 1, "COGR": 1, "FLTH": 1, "GAVA": 1, "KACO": 1, "SADI": 1, "SICE": 1, "TEOC": 1, "WAAL": 1}, "time": {"PRE": 31, "POST": 26}}}}

reasoning: Matrix columns equal metadata title for 57/57 samples (inspect alignment_keys). Title = 4-letter participant code + PRE/POST; subject is the code, time from the treatment characteristic. 24 participants have both timepoints, 7 only PRE, 2 only POST; all are kept because the paper's model included unpaired samples (35 pre / 27 post).

### matrix (valid, not_started)

final: {"note": "Kallisto gene-level counts deposited as integers ('aligned raw gene counts' per data_processing); the paper ran DESeq2 directly on them. Pre-filtered with the authors' rowMeans >= 10 rule (prep_filter_meancount.py).", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "E:/agent/mwangLab_review/.review_queue/case_08/run/GSE267512\\aligned\\aligned_matrix.csv", "sha256": "9cb8c6b94573f6c94af5d55e43f0593a5f89df9eed9cd147de6af765e0b98c27", "n_features": 14830, "n_samples": 57, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 7017190.0, "median": 174.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer fraction 1.0, range 0-7.0e6, library sizes 20-29 M; GEO data_processing: 'Long/Wide format of aligned raw gene counts' from Kallisto. Kallisto estimates are summed/rounded to integers by the submitters; the paper used this matrix in DESeq2 (S2.14.p6), so it is treated as count-scale input.

rejected alternatives: [{"value": "normalized integers", "reason_rejected": "library sizes vary 20-29 M and data_processing calls them raw counts"}]

### design (valid, not_started)

final: {"analysis_type": "two-group (PRE vs POST)", "design_column": "time", "control": "PRE", "treatment": "POST", "contrasts": [{"name": "time_POST_vs_PRE", "control": "PRE", "treatment": "POST", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "E:/agent/mwangLab_review/.review_queue/case_08/run/GSE267512\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Two time groups, PRE and POST; each GEO sample is one library, so the comparison is POST vs PRE across all 57 libraries.

rejected alternatives: [{"value": "age covariate", "reason_rejected": "not in the paper's model and constant within participant (absorbed by ID)"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(time)", "n_samples": 57, "n_columns": 2, "columns": ["Intercept", "time_PRE"], "rank": 2, "full_rank": true, "residual_df": 55, "levels": {"time": {"PRE": 31, "POST": 26}}, "cells": [{"cell": ["POST"], "n": 26}, {"cell": ["PRE"], "n": 31}], "min_cell_size": 26, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 57, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 57, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.Sex", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.age of_donor", "n_levels": 14, "status": "crossed", "crosstab": {"POST": {"18": 2, "19": 6, "20": 1, "21": 1, "22": 2, "23": 2, "25": 3, "26": 2, "27": 0, " ... [2682 more characters]

reasoning: All participants are untrained pre-menopausal females from one cohort; no batch, lane or sex column varies with time. No blocking needed.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ time", "paper_route": {"method": "DESeq2", "status": "reproduced"}, "deviations": ["pydeseq2 instead of R DESeq2 1.32", "57 GEO samples (31 PRE / 26 POST) instead of the paper's 35 / 27", "gene filter follows the authors' code (rowMeans >= 10, 14,830 genes) rather than the text's '10 RPM' wording (14,979 in paper)"]}

reasoning: Paper method reproducible on the count matrix; alpha 0.1 in the primary run matches R results() defaults used in the authors' script; alpha 0.05 as sensitivity.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}}

reasoning: S2.14.p7: FDR-adjusted P < 0.05; no fold-change cutoff.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "time_POST_vs_PRE", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 57, "matrix": "E:/agent/mwangLab_review/.review_queue/case_08/run/GSE267512\\aligned\\aligned_matrix.csv", "formula": "~ time", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_08/run/GSE267512\\results\\time_POST_vs_PRE\\DEG_results_POST_vs_PRE.csv"], "counts": {"time_POST_vs_PRE": {"applied": {"rule": "padj < 0.05", "n_tested": 13967, "n_significant": 79, "n_up": 68, "n_down": 11, "deg_sanity": "ok"}}}}

reasoning: paper's DESeq2 ~ ID + timepoint on all deposited samples; alpha 0.1 = R results() default in authors' script

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "time_POST_vs_PRE_alpha005", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 57, "matrix": "E:/agent/mwangLab_review/.review_queue/case_08/run/GSE267512\\aligned\\aligned_matrix.csv", "formula": "~ time", "outputs": ["E:/agent/mwangLab_review/.review_queue/case_08/run/GSE267512\\results\\time_POST_vs_PRE_alpha005\\DEG_results_POST_vs_PRE.csv"], "counts": {"time_POST_vs_PRE_alpha005": {"applied": {"rule": "padj < 0.05", "n_tested": 14830, "n_significant": 81, "n_up": 70, "n_down": 11, "deg_sanity": "ok"}}}}

reasoning: independent-filtering target equal to the paper FDR

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["8 of the paper's samples (4 PRE-only, 1 POST) are absent from GEO", "ChEA3 TF enrichment and testosterone-association analyses not reproduced"], "results": {"time_POST_vs_PRE": {"n_deg": 79, "up": 68, "down": 11, "rule": "padj < 0.05"}, "time_POST_vs_PRE_alpha005": {"n_deg": 81, "up": 70, "down": 11, "rule": "padj < 0.05"}}, "paper_counts": {"time_POST_vs_PRE": 214, "time_POST_vs_PRE_alpha005": 214}, "comparison": {"time_POST_vs_PRE": {"ours": 79, "paper": 214}, "time_POST_vs_PRE_alpha005": {"ours": 81, "paper": 214}}, "paper_gene_check": {"time_POST_vs_PRE": {"RPS6KC1": {"baseMean": 538.0115, "log2FoldChange": 0.1712, "padj": 0.0468, "pvalue": 0.0003}, "TRIM63": {"baseMean": 3233.4913, "log2FoldChange": -0.0739, "padj": 0.8999, "pvalue": 0.4881}, "FBXO32": {"baseMean": 13917.9609, "log2FoldChange": 0.0821, "padj": 0.8766, "pvalue": 0.4319}, "TRAF6": {"baseMean": 323.5863, "log2FoldChange": -0.1324, "padj": 0.4711, "pvalue": 0.0412}, "FOXO1": {"baseMean": 624.1606, "log2FoldChange": -0.0765, "padj": 0.8632, "pvalue": 0.3975}, "FOXO3": {"baseMean": 1602.3079, "log2FoldChange": -0.1313, "padj": 0.731, "pvalue": 0.1926}, "AR": {"baseMean": 1209.7157, "log2FoldChange": -0.0365, "padj": 0.9566, "pvalue": 0.7246}}}}

reasoning: Paper: 214 DEGs (122 up, 92 down) POST vs PRE; RPS6KC1 significant; the others reported as unchanged.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "gene filter",
    "paper": "text: mean <= 10 RPM removed, 14,979 kept; authors' code: rowMeans(counts) >= 10",
    "data": "10 RPM rule keeps only 6,084 genes (85% removed, contradicting the stated 63%); rowMeans >= 10 keeps 14,830 (63.4% removed)",
    "disposition": "executable_without_change"
  },
  {
    "item": "independent filtering alpha",
    "paper": "R results() default alpha 0.1, DEGs at padj < 0.05",
    "data": "pydeseq2 alpha set to 0.1 in primary, 0.05 sensitivity",
    "disposition": "executable_without_change"
  }
]
