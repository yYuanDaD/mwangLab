# Review packet B (the analysis' decisions): GSE224900

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.2.age", "n_values": 14, "max_repeat": 6, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **other_rule_matches_paper**: {"table": "pla/time_REC_vs_PRE_trt-Pla", "paper": 3550, "applied": 5764, "applied_rule": "padj < 0.05", "closest_rule": "padj<0.05 & |lfc|>0.584963", "closest_n": 3252, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **other_rule_matches_paper**: {"table": "met/time_REC_vs_PRE_trt-Met", "paper": 1386, "applied": 2668, "applied_rule": "padj < 0.05", "closest_rule": "padj<0.05 & |lfc|>0.584963", "closest_n": 1422, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pla/time_POST_vs_PRE_trt-Pla | 441 | 1872 | padj < 0.05 | 1872 | 964 | 337 | 2757 | 4791 | 2078 | 917 | 2448 | 0.28 | 0.114 |
| pla/time_REC_vs_PRE_trt-Pla | 3550 | 5764 | padj < 0.05 | 5764 | 3252 | 1638 | 7239 | 8349 | 4267 | 2220 | 5459 | 0.232 | 0.199 |
| met/time_POST_vs_PRE_trt-Met | 377 | 276 | padj < 0.05 | 276 | 230 | 123 | 694 | 3662 | 1860 | 840 | 1293 | 0.248 | 0.085 |
| met/time_REC_vs_PRE_trt-Met | 1386 | 2668 | padj < 0.05 | 2668 | 1422 | 671 | 4189 | 6149 | 2986 | 1499 | 3152 | 0.267 | 0.143 |

## Samples per design level

### `time`
- **POST** (17): GSM7035216 / 19565X4 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035222 / 19565X10 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035228 / 19565X16 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035234 / 19565X22 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035240 / 19565X28 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035246 / 19565X34 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035252 / 19565X40 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035257 / 19565X45 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035263 / 19565X51 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035269 / 19565X57 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035275 / 19565X63 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035281 / 19565X69 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035287 / 19565X75 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035299 / 19565X87 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035311 / 19565X99 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035326 / 20063X4 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035339 / 20063X10 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi
- **PRE** (17): GSM7035213 / 19565X1 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035219 / 19565X7 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035225 / 19565X13 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035231 / 19565X19 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035237 / 19565X25 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035243 / 19565X31 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035249 / 19565X37 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035254 / 19565X42 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035260 / 19565X48 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035266 / 19565X54 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035272 / 19565X60 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035278 / 19565X66 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035284 / 19565X72 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035290 / 19565X78 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035296 / 19565X84 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035318 / 20063X1 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035333 / 20063X7 PREbc_Con / Pre intervention, fasted thigh muscle bi
- **REC** (18): GSM7035218 / 19565X6 7d_Con / After 7 days of recovery and no treatmen; GSM7035224 / 19565X12 7d_Con / After 7 days of recovery and no treatmen; GSM7035230 / 19565X18 7d_Con / After 7 days of recovery and no treatmen; GSM7035236 / 19565X24 7d_Con / After 7 days of recovery and no treatmen; GSM7035242 / 19565X30 7d_Con / After 7 days of recovery and no treatmen; GSM7035248 / 19565X36 7d_Con / After 7 days of recovery and no treatmen; GSM7035253 / 19565X41 7d_Con / After 7 days of recovery and no treatmen; GSM7035259 / 19565X47 7d_Met / After 7 days of recovery and no treatmen; GSM7035265 / 19565X53 7d_Met / After 7 days of recovery and no treatmen; GSM7035271 / 19565X59 7d_Met / After 7 days of recovery and no treatmen; GSM7035277 / 19565X65 7d_Met / After 7 days of recovery and no treatmen; GSM7035283 / 19565X71 7d_Met / After 7 days of recovery and no treatmen; GSM7035289 / 19565X77 7d_Met / After 7 days of recovery and no treatmen; GSM7035295 / 19565X83 7d_Met / After 7 days of recovery and no treatmen; GSM7035301 / 19565X89 7d_Met / After 7 days of recovery and no treatmen; GSM7035316 / 19565X101 7d_Met / After 7 days of recovery and no treatmen; GSM7035331 / 20063X6 7d_Con / After 7 days of recovery and no treatmen; GSM7035343 / 20063X12 7d_Con / After 7 days of recovery and no treatmen

### `subject`
- **19565_S001** (3): GSM7035213 / 19565X1 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035216 / 19565X4 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035218 / 19565X6 7d_Con / After 7 days of recovery and no treatmen
- **19565_S007** (3): GSM7035219 / 19565X7 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035222 / 19565X10 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035224 / 19565X12 7d_Con / After 7 days of recovery and no treatmen
- **19565_S013** (3): GSM7035225 / 19565X13 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035228 / 19565X16 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035230 / 19565X18 7d_Con / After 7 days of recovery and no treatmen
- **19565_S019** (3): GSM7035231 / 19565X19 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035234 / 19565X22 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035236 / 19565X24 7d_Con / After 7 days of recovery and no treatmen
- **19565_S025** (3): GSM7035237 / 19565X25 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035240 / 19565X28 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035242 / 19565X30 7d_Con / After 7 days of recovery and no treatmen
- **19565_S031** (3): GSM7035243 / 19565X31 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035246 / 19565X34 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035248 / 19565X36 7d_Con / After 7 days of recovery and no treatmen
- **19565_S037** (3): GSM7035249 / 19565X37 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035252 / 19565X40 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035253 / 19565X41 7d_Con / After 7 days of recovery and no treatmen
- **19565_S042** (3): GSM7035254 / 19565X42 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035257 / 19565X45 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035259 / 19565X47 7d_Met / After 7 days of recovery and no treatmen
- **19565_S048** (3): GSM7035260 / 19565X48 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035263 / 19565X51 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035265 / 19565X53 7d_Met / After 7 days of recovery and no treatmen
- **19565_S054** (3): GSM7035266 / 19565X54 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035269 / 19565X57 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035271 / 19565X59 7d_Met / After 7 days of recovery and no treatmen
- **19565_S060** (3): GSM7035272 / 19565X60 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035275 / 19565X63 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035277 / 19565X65 7d_Met / After 7 days of recovery and no treatmen
- **19565_S066** (3): GSM7035278 / 19565X66 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035281 / 19565X69 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035283 / 19565X71 7d_Met / After 7 days of recovery and no treatmen
- **19565_S072** (3): GSM7035284 / 19565X72 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035287 / 19565X75 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035289 / 19565X77 7d_Met / After 7 days of recovery and no treatmen
- **19565_S078** (2): GSM7035290 / 19565X78 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035295 / 19565X83 7d_Met / After 7 days of recovery and no treatmen
- **19565_S084** (3): GSM7035296 / 19565X84 PREbc_Met / Pre intervention, fasted thigh muscle bi; GSM7035299 / 19565X87 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035301 / 19565X89 7d_Met / After 7 days of recovery and no treatmen
- **19565_S096** (2): GSM7035311 / 19565X99 POSTbc_Met / Post 5d bed rest, fasted thigh muscle bi; GSM7035316 / 19565X101 7d_Met / After 7 days of recovery and no treatmen
- **20063_S001** (3): GSM7035318 / 20063X1 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035326 / 20063X4 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035331 / 20063X6 7d_Con / After 7 days of recovery and no treatmen
- **20063_S007** (3): GSM7035333 / 20063X7 PREbc_Con / Pre intervention, fasted thigh muscle bi; GSM7035339 / 20063X10 POSTbc_Con / Post 5d bed rest, fasted thigh muscle bi; GSM7035343 / 20063X12 7d_Con / After 7 days of recovery and no treatmen

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE224900"], "assay": "bulk total RNA-seq (rRNA-depleted), vastus lateralis, older adults (S2.7.p1)", "primary_estimand": "Within-participant change in muscle gene expression with 5 d bed rest (disuse; POST vs PRE) and after 7 d re-ambulation (REC vs PRE), separately in the placebo and metformin arms (S3.4.p1, Fig 5a-d). Physical-activity axis = disuse/reloading, not structured exercise.", "factors": {"time": ["PRE", "POST", "REC"], "treatment": ["Placebo", "Metformin"]}, "repeated_measure_unit": "participant (biopsies at PRE, DAY1, POST, REC; S2.4.p1)", "inclusion": "fasted biopsies at PRE, POST, REC; N = 9-10/group (Fig 5 legend)", "planned_contrasts": ["Placebo POST vs PRE (S3.4.p1; paper 441 DEGs)", "Metformin POST vs PRE (S3.4.p1; 377)", "Placebo REC vs PRE (S3.4.p1; 3550)", "Metformin REC vs PRE (S3.4.p1; 1386)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S2.7.p1"}, "paper_method": "DESeq2 1.30 via hciR (S2.7.p1); formula not stated", "paper_results": "collagen isoforms highly upregulated in placebo REC (S3.4.p1); CDKN1A, TP53 up in placebo not metformin after bed rest and recovery (S3.5.p1)"}

reasoning: S2.7.p1 gives DESeq2 + 5% FDR, no fold-change rule; S3.4.p1 gives the four within-arm DEG counts vs PRE. The paper's activity manipulation is bed-rest disuse followed by re-ambulation; there is no exercise-training arm, so the activity estimand is disuse/reloading within each arm.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\prep\\GSE224900_merged_counts.csv.gz", "owned": true, "checks": ["S2.7.p1 and S11.p1 name GSE224900", "GEO contact Drummond lab (senior author)", "timepoint labels PRE/Day1/POST/7d and Placebo/Metformin match the trial design (S2.3.p1)", "10 metformin participants (5F/5M = Table 1) and 9 placebo (paper N=9-10/group)"], "accession": "GSE224900", "metadata_file": "E:/agent/mwangLab_pdf/test/experiments/large_run_pilot_20261019/runs_claude/PMID37486024/prep/GSE224900_metadata_subject.csv"}

reasoning: Both count files (19565R, 20063R sequencing runs) belong to GSE224900 and the paper names it.

### alignment (valid, not_started)

final: {"subject_key": "derived in prep_merge.py from consecutive per-participant biopsy blocks; age/sex/treatment constant within each block", "method": "exact:key", "n_aligned": 113, "n_metadata": 113, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM7035214": "PREac: post hyperinsulinemic-euglycemic clamp biopsy; paper's RNA-seq DE uses fasted PRE/POST/REC biopsies (S2.4.p1, S3.4.p1)", "GSM7035215": "Day1: after 2-wk drug run-in, before bed rest; not part of the paper's PRE/POST/REC DE contrasts (S3.4.p1)", "GSM7035217": "POSTac: post hyperinsulinemic-euglycemic clamp biopsy; paper's RNA-seq DE uses fasted PRE/POST/REC biopsies (S2.4.p1, S3.4.p1)", "GSM7035220": "PREac: post hyperinsulinemic-euglycemic clamp biopsy; paper's RNA-seq DE uses fasted PRE/POST/REC biopsies (S2.4.p1, S3.4.p1)", "GSM7035221": "Day1: after 2-wk drug run-in, before bed rest; not part of the paper's PRE/POST/REC DE contrasts (S3.4.p1)", "GSM7035223": "POSTac: post hyperinsulinemic-euglycemic clamp biopsy; paper's RNA-seq DE uses fasted PRE/POST/REC biopsies (S2.4.p1, S3.4.p1)", "GSM7035226": "PREac: post hyperinsulinemic-euglycemic clamp biopsy; paper's RNA-seq DE uses fasted PRE/POST/REC biopsies (S2.4.p1, S3.4.p1)", "GSM7035227": "Day1: after 2-wk drug run-in, before bed rest; not part of the paper's PRE/POST/REC DE contrasts (S3.4.p1)", "GSM7035229": "POSTac: post hyperinsulinemic-euglycemic clamp biopsy; paper's RNA-seq DE uses fasted PRE/POST/ ... [7816 more characters]

reasoning: Matrix columns (19565X1...) equal the first token of title, written as column `key` by prep_merge.py (two count files merged on identical Ensembl IDs). GEO has no participant ID; prep_merge.py assigns `subject` by sample-number blocks that each start at a PREbc biopsy - every block has one age, one sex and one treatment, giving 9 placebo + 10 metformin participants. Clamp (ac) and Day1 biopsies excluded: the paper's DE uses fasted PRE/POST/REC.

### matrix (valid, not_started)

final: {"source": "GSE224900_19565R_counts.txt.gz + GSE224900_20063R_counts.txt.gz merged", "paper_input": "DESeq2 on counts (S2.7.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\aligned\\aligned_matrix.csv", "sha256": "c7b62057f0aa41552273119d995bd16ce279889d209e48e7390862ce6bb1a44e", "n_features": 60664, "n_samples": 52, "annotation_columns_dropped": ["GSM7035214", "GSM7035215", "GSM7035217", "GSM7035220", "GSM7035221", "GSM7035223", "GSM7035226", "GSM7035227", "GSM7035229", "GSM7035232", "GSM7035233", "GSM7035235", "GSM7035238", "GSM7035239", "GSM7035241", "GSM7035244", "GSM7035245", "GSM7035247", "GSM7035250", "GSM7035251", "GSM7035255", "GSM7035256", "GSM7035258", "GSM7035261", "GSM7035262", "GSM7035264", "GSM7035267", "GSM7035268", "GSM7035270", "GSM7035273", "GSM7035274", "GSM7035276", "GSM7035279", "GSM7035280", "GSM7035282", "GSM7035285", "GSM7035286", "GSM7035288", "GSM7035291", "GSM7035292", "GSM7035293", "GSM7035294", "GSM7035297", "GSM7035298", "GSM7035300", "GSM7035302", "GSM7035303", "GSM7035304", "GSM7035305", "GSM7035306", "GSM7035307", "GSM7035308", "GSM7035309", "GSM7035310", "GSM7035313", "GSM7035320", "GSM7035323", "GSM7035329", "GSM7035335", "GSM7035337", "GSM7035341"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 10529500.0, "median": 0.0, "integer_fraction": 1.0, "can ... [119 more characters]

reasoning: All values integer, median 0, max ~1.2e7; data_processing: STAR two-pass alignment to GRCh38/Ensembl 104 with gene counts; paper used DESeq2.

### design (valid, not_started)

final: {"analysis_type": "repeated-measures, within-arm time contrasts", "formula": "~ subject + time (per arm)", "contrasts": [{"name": "time_POST_vs_PRE_trt-Pla", "control": "PRE", "treatment": "POST", "role": "primary"}, {"name": "time_REC_vs_PRE_trt-Pla", "control": "PRE", "treatment": "REC", "role": "primary"}, {"name": "time_POST_vs_PRE_trt-Met", "control": "PRE", "treatment": "POST", "role": "secondary"}, {"name": "time_REC_vs_PRE_trt-Met", "control": "PRE", "treatment": "REC", "role": "secondary"}], "estimand_type": "within-subject change; no non-bed-rest control arm", "suitability": {"verdict": "partially_analyzable", "failed": [], "warnings": ["sex"], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: Placebo arm isolates disuse/re-ambulation (primary); metformin arm reproduces the paper's second set but mixes drug exposure with disuse (secondary). Each arm fitted separately as the paper reports per-arm volcano plots.

rejected alternatives: [{"value": "treatment x time interaction", "reason_rejected": "the paper's reported DEG counts are within-arm vs PRE; interaction is the drug question, not the activity estimand"}, {"value": "include DAY1", "reason_rejected": "DAY1 reflects 2-wk drug run-in, not disuse; paper's RNA-seq DE uses PRE/POST/REC (S3.4.p1)"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "sex", "disposition": "nested within subject; absorbed by subject block (per-sex fits run as exploratory)"}, {"name": "run", "disposition": "sequencing run nested within subject; absorbed by subject block"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 52, "n_columns": 20, "columns": ["Intercept", "time_PRE", "time_REC", "subject_19565_S007", "subject_19565_S013", "subject_19565_S019", "subject_19565_S025", "subject_19565_S031", "subject_19565_S037", "subject_19565_S042", "subject_19565_S048", "subject_19565_S054", "subject_19565_S060", "subject_19565_S066", "subject_19565_S072", "subject_19565_S078", "subject_19565_S084", "subject_19565_S096", "subject_20063_S001", "subject_20063_S007"], "rank": 20, "full_rank": true, "residual_df": 32, "levels": {"time": {"REC": 18, "PRE": 17, "POST": 17}, "subject": {"19565_S001": 3, "19565_S007": 3, "19565_S013": 3, "19565_S019": 3, "19565_S025": 3, "19565_S031": 3, "19565_S037": 3, "19565_S042": 3, "19565_S048": 3, "19565_S054": 3, "19565_S060": 3, "19565_S066": 3, "19565_S072": 3, "19565_S084": 3, "20063_S001": 3, "20063_S007": 3, "19565_S078": 2, "19565_S096": 2}}, "cells": [{"cell": ["POST", "19565_S001"], "n": 1}, {"cell": ["POST", "19565_S007"], "n": 1}, {"cell": ["POST", "19565_S013"], "n": 1}, {"cell": ["POST", "19565_S019"], "n": 1}, {"cell": ["POST", "19565_S025"], "n": 1}, {"cell": ["POST", "19565_S031"], "n": 1}, {"c ... [2272 more characters]

reasoning: Repeated biopsies per participant -> subject block. Sex and sequencing run are constant within subject, so the subject term absorbs them.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ subject + time", "paper_route": {"method": "DESeq2 1.30 (hciR)", "status": "reproduced_approximately"}, "deviations": ["pydeseq2 instead of R DESeq2 1.30/hciR; hciR default filtering and formula not stated in the paper", "subject derived from sample-number blocks"]}

reasoning: Raw counts support the paper's DESeq2 route; one model per arm with all three timepoints and subject blocking.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S2.7.p1: 5% FDR, no fold-change cutoff; Fig 5 legend: adjusted p < 0.05.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "pla", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 27, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla\\input\\matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla\\DEG_results_time_POST_vs_PRE_trt-Pla.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla\\DEG_results_time_REC_vs_PRE_trt-Pla.csv"], "counts": {"pla/time_POST_vs_PRE_trt-Pla": {"applied": {"rule": "padj < 0.05", "n_tested": 17577, "n_significant": 1872, "n_up": 814, "n_down": 1058, "deg_sanity": "ok"}}, "pla/time_REC_vs_PRE_trt-Pla": {"applied": {"rule": "padj < 0.05", "n_tested": 22464, "n_significant": 5764, "n_up": 3141, "n_down": 2623, "deg_sanity": "ok"}}}}

reasoning: placebo arm: disuse and re-ambulation vs PRE, ~ subject + time

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "met", "role": "secondary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 25, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met\\input\\matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met\\DEG_results_time_POST_vs_PRE_trt-Met.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met\\DEG_results_time_REC_vs_PRE_trt-Met.csv"], "counts": {"met/time_POST_vs_PRE_trt-Met": {"applied": {"rule": "padj < 0.05", "n_tested": 18024, "n_significant": 276, "n_up": 93, "n_down": 183, "deg_sanity": "ok"}}, "met/time_REC_vs_PRE_trt-Met": {"applied": {"rule": "padj < 0.05", "n_tested": 17189, "n_significant": 2668, "n_up": 1365, "n_down": 1303, "deg_sanity": "ok"}}}}

reasoning: metformin arm, same model

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "pla_unpaired", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 27, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_unpaired\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_unpaired\\DEG_results_time_POST_vs_PRE_trt-Pla.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_unpaired\\DEG_results_time_REC_vs_PRE_trt-Pla.csv"], "counts": {"pla_unpaired/time_POST_vs_PRE_trt-Pla": {"applied": {"rule": "padj < 0.05", "n_tested": 19206, "n_significant": 371, "n_up": 195, "n_down": 176, "deg_sanity": "ok"}}, "pla_unpaired/time_REC_vs_PRE_trt-Pla": {"applied": {"rule": "padj < 0.05", "n_tested": 21649, "n_significant": 2740, "n_up": 1807, "n_down": 933, "deg_sanity": "ok"}}}}

reasoning: ~ time without subject: tests whether the paper's (unstated) hciR model ignored pairing

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "met_unpaired", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 25, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_unpaired\\input\\matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_unpaired\\DEG_results_time_POST_vs_PRE_trt-Met.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_unpaired\\DEG_results_time_REC_vs_PRE_trt-Met.csv"], "counts": {"met_unpaired/time_POST_vs_PRE_trt-Met": {"applied": {"rule": "padj < 0.05", "n_tested": 18023, "n_significant": 158, "n_up": 119, "n_down": 39, "deg_sanity": "ok"}}, "met_unpaired/time_REC_vs_PRE_trt-Met": {"applied": {"rule": "padj < 0.05", "n_tested": 20529, "n_significant": 602, "n_up": 417, "n_down": 185, "deg_sanity": "ok"}}}}

reasoning: ~ time without subject: tests whether the paper's (unstated) hciR model ignored pairing

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "pla_F", "role": "exploratory", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 15, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_F\\input\\matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_F\\DEG_results_time_POST_vs_PRE_trt-Pla.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_F\\DEG_results_time_REC_vs_PRE_trt-Pla.csv"], "counts": {"pla_F/time_POST_vs_PRE_trt-Pla": {"applied": {"rule": "padj < 0.05", "n_tested": 18287, "n_significant": 1216, "n_up": 418, "n_down": 798, "deg_sanity": "ok"}}, "pla_F/time_REC_vs_PRE_trt-Pla": {"applied": {"rule": "padj < 0.05", "n_tested": 18287, "n_significant": 1152, "n_up": 601, "n_down": 551, "deg_sanity": "ok"}}}}

reasoning: per-sex exploratory fit (Pla, sex F); paper pooled sexes

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "pla_M", "role": "exploratory", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_M\\input\\matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_M\\DEG_results_time_POST_vs_PRE_trt-Pla.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\pla_M\\DEG_results_time_REC_vs_PRE_trt-Pla.csv"], "counts": {"pla_M/time_POST_vs_PRE_trt-Pla": {"applied": {"rule": "padj < 0.05", "n_tested": 16395, "n_significant": 51, "n_up": 22, "n_down": 29, "deg_sanity": "ok"}}, "pla_M/time_REC_vs_PRE_trt-Pla": {"applied": {"rule": "padj < 0.05", "n_tested": 19300, "n_significant": 3465, "n_up": 2036, "n_down": 1429, "deg_sanity": "ok"}}}}

reasoning: per-sex exploratory fit (Pla, sex M); paper pooled sexes

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "met_F", "role": "exploratory", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 13, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_F\\input\\matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_F\\DEG_results_time_POST_vs_PRE_trt-Met.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_F\\DEG_results_time_REC_vs_PRE_trt-Met.csv"], "counts": {"met_F/time_POST_vs_PRE_trt-Met": {"applied": {"rule": "padj < 0.05", "n_tested": 40947, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}}, "met_F/time_REC_vs_PRE_trt-Met": {"applied": {"rule": "padj < 0.05", "n_tested": 40947, "n_significant": 3, "n_up": 2, "n_down": 1, "deg_sanity": "ok"}}}}

reasoning: per-sex exploratory fit (Met, sex F); paper pooled sexes

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "met_M", "role": "exploratory", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_M\\input\\matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_M\\DEG_results_time_POST_vs_PRE_trt-Met.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\met_M\\DEG_results_time_REC_vs_PRE_trt-Met.csv"], "counts": {"met_M/time_POST_vs_PRE_trt-Met": {"applied": {"rule": "padj < 0.05", "n_tested": 14644, "n_significant": 440, "n_up": 114, "n_down": 326, "deg_sanity": "ok"}}, "met_M/time_REC_vs_PRE_trt-Met": {"applied": {"rule": "padj < 0.05", "n_tested": 18383, "n_significant": 3306, "n_up": 1794, "n_down": 1512, "deg_sanity": "ok"}}}}

reasoning: per-sex exploratory fit (Met, sex M); paper pooled sexes

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "pla/time_REC_vs_PRE_trt-Pla", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\enrichment_pla_time_REC_vs_PRE_trt-Pla\\gsea\\DEG_results_time_REC_vs_PRE_trt-Pla_GSEA_Hallmark.csv"], "summary": "GSEA complete on 32131 Human genes ranked by 'stat'. 50 Hallmark sets tested, 44 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.74 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.21 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.13 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.19 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V ... [423 more characters]

reasoning: paper ran fgsea (KEGG/Reactome) on recovery; Hallmark GSEA as a check of collagen/TGF-beta direction

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "met/time_REC_vs_PRE_trt-Met", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37486024\\GSE224900\\results\\enrichment_met_time_REC_vs_PRE_trt-Met\\gsea\\DEG_results_time_REC_vs_PRE_trt-Met_GSEA_Hallmark.csv"], "summary": "GSEA complete on 32817 Human genes ranked by 'stat'. 50 Hallmark sets tested, 43 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.75 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.39 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.36 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.34 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COMPLEMENT | NES=2.15 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-3.23 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V ... [423 more characters]

reasoning: same for metformin arm

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Activity axis is bed-rest disuse and re-ambulation, not exercise training.", "No time-matched non-bed-rest control: time contrasts include any time/season effect; metformin-arm contrasts also include drug exposure (POST) or withdrawal (REC).", "Participant IDs were derived from sample-number blocks, not given in GEO.", "Expression-inferred sex contradicts GEO labels in 7 metformin-arm biopsies: 5 biopsies excluded, one block relabelled F; the metformin arm therefore differs from the paper's sample set (paper presumably used the labels as deposited)."], "results": {"pla/time_POST_vs_PRE_trt-Pla": {"n_deg": 1872, "up": 814, "down": 1058, "rule": "padj < 0.05"}, "pla/time_REC_vs_PRE_trt-Pla": {"n_deg": 5764, "up": 3141, "down": 2623, "rule": "padj < 0.05"}, "met/time_POST_vs_PRE_trt-Met": {"n_deg": 276, "up": 93, "down": 183, "rule": "padj < 0.05"}, "met/time_REC_vs_PRE_trt-Met": {"n_deg": 2668, "up": 1365, "down": 1303, "rule": "padj < 0.05"}, "pla_unpaired/time_POST_vs_PRE_trt-Pla": {"n_deg": 371, "up": 195, "down": 176, "rule": "padj < 0.05"}, "pla_unpaired/time_REC_vs_PRE_trt-Pla": {"n_deg": 2740, "up": 1807, "down": 933, "rule": "padj < 0.05"}, "met_unpaired/time_POST_vs_PRE_trt-Met": {"n_deg": 158, "up": 119, "down": 39, "rule": "padj < 0.05"}, "met_unpaired/time_REC_vs_PRE_trt-Met": {"n_deg": 602, "up": 417, "down": 185, "rule": "padj < 0.05"}, "pla_F/time_POST_vs_PRE_trt-Pla": {"n_deg": 1216, "up": 418, "down": 798, "rule": "padj < ... [1876 more characters]

reasoning: All four contrasts follow the paper's DESeq2 + FDR 5% route.

## Suitability report lines (sex, confounding, warnings)

- Verdict: **partially_analyzable**; check: sex
- | Check | Status | Detail |
- | Sex | mismatch | Sex inference completed on 52 samples.; mismatch: GSM7035296, GSM7035299, GSM7035301; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "participant ID",
    "paper": "paired design, 9-10/group",
    "data": "GEO lacks participant IDs; derived from biopsy blocks (age/sex constant)",
    "disposition": "executable_without_change"
  },
  {
    "item": "placebo n",
    "paper": "Table 1: 10 placebo (6F/4M)",
    "data": "9 placebo participants sequenced (5F/4M); Fig 5 N = 9-10/group",
    "disposition": "executable_without_change"
  },
  {
    "item": "sample sex labels (metformin arm)",
    "paper": "metformin 5F/5M (Table 1)",
    "data": "XIST/chrY: 19565_S084 block entirely female though GEO says M (label corrected, block kept); single swapped biopsies 19565X81 and 19565X96 excluded; block 19565_S090 switches sex between PREac and Day1, all its PRE/POST/REC biopsies excluded. Metformin arm analysed with 9 participants (PRE 8, POST 8, REC 9).",
    "disposition": "executable_with_exclusions"
  },
  {
    "item": "two sequencing runs",
    "paper": "not mentioned",
    "data": "19565R (17 participants) and 20063R (2 placebo participants)",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 37486024 / GSE224900

**Status: finished** (decision `valid`, execution `completed`, validator 19 records / 0 errors).

## What ran
- Route: case spec (`case_spec.json`, generated by `prep/write_spec.py`), `python -m tools.case_runner execute`.
- Input prep (`prep/prep_merge.py`): merged the two deposited count files (19565R: 101 biopsies, 20063R: 12) on identical Ensembl IDs. Built the participant key `subject` (GEO has none) from sample-number blocks, each starting at a PREbc biopsy. Age, sex and treatment are constant within every block, which gives 9 placebo and 10 metformin participants.
- Activity estimand: bed-rest disuse (POST vs PRE) and 7-day re-ambulation (REC vs PRE), within each arm. There is no exercise-training arm. The placebo arm is primary because it isolates disuse and reloading. The metformin arm is secondary because drug exposure or withdrawal is mixed in.
- Samples: fasted PRE, POST and REC biopsies only (S3.4.p1). The clamp (PREac/POSTac) and Day1 biopsies were excluded.
- Model: DESeq2 (pydeseq2 Wald), `~ subject + time`, one model per arm (`run_joint_deseq2` with a subset per arm).
- Threshold: the paper's rule, padj < 0.05 with no fold-change cutoff (S2.7.p1, Fig 5 legend).
- Sensitivity: `~ time` without the subject term. Exploratory: per-sex fits within each arm.
- Enrichment: Hallmark GSEA (preranked on stat) on the REC tables of both arms. The paper ran fgsea on KEGG/Reactome at 10% FDR, so this run is a direction check only.

## DEG counts vs paper (padj < 0.05, no FC cutoff)
| Contrast | Ours, paired (primary) | Ours, unpaired (sensitivity) | Paper |
|---|---|---|---|
| Placebo POST vs PRE | 1872 (814 up / 1058 down) | 371 | 441 |
| Placebo REC vs PRE | 5764 (3141 / 2623) | 2740 | 3550 |
| Metformin POST vs PRE | 276 (93 / 183) | 158 | 377 |
| Metformin REC vs PRE | 2668 (1365 / 1303) | 602 | 1386 |

- The unpaired counts are much closer to the paper's for placebo. The paper's hciR model may not have blocked on participant, but the paper does not state its formula.
- The qualitative pattern matches the paper: the recovery response is larger than the bed-rest response, and it is larger in placebo than in metformin.
- Named genes in placebo REC vs PRE are all significantly up: COL1A1 log2FC 5.5, COL3A1 4.1, COL1A2 3.3, CDKN1A 2.2, TP53 0.8. CDKN1A and TP53 are also up at placebo POST. This agrees with S3.4.p1 and S3.5.p1.
- GSEA: EMT, inflammatory, TNFα/NF-κB and TGF-β gene sets are up, and OXPHOS is down, at ... [2544 more characters]
