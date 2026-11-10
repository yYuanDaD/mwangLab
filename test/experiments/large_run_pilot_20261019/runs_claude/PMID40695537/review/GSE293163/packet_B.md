# Review packet B (the analysis' decisions): GSE293163

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| young_post_vs_pre | 53 | 99 | padj < 0.01 | 179 | 72 | 7 | 227 | 1165 | 249 | 83 | 456 | 0.115 | 0.049 |
| old_post_vs_pre | 1026 | 3613 | padj < 0.01 | 5740 | 2602 | 1804 | 7124 | 8280 | 3404 | 2237 | 5556 | 0.057 | 0.331 |
| baseline_old_vs_young | 665 | 1589 | padj < 0.01 | 3634 | 2306 | 1541 | 5225 | 7271 | 4116 | 2698 | 4043 | 0.052 | 0.29 |

## Samples per design level

### `age`
- **Old** (16): GSM8877704 / 22719X43 08 Pre Old / Library name: 22719X43; GSM8877705 / 22719X44 08 Post Old / Library name: 22719X44; GSM8877706 / 22719X45 09 Pre Old / Library name: 22719X45; GSM8877707 / 22719X46 09 Post Old / Library name: 22719X46; GSM8877708 / 22719X47 10 Pre Old / Library name: 22719X47; GSM8877709 / 22719X48 10 Post Old / Library name: 22719X48; GSM8877710 / 22719X49 11 Pre Old / Library name: 22719X49; GSM8877711 / 22719X50 11 Post Old / Library name: 22719X50; GSM8877712 / 22719X51 12 Pre Old / Library name: 22719X51; GSM8877713 / 22719X52 12 Post Old / Library name: 22719X52; GSM8877714 / 22719X53 13 Pre Old / Library name: 22719X53; GSM8877715 / 22719X54 13 Post Old / Library name: 22719X54; GSM8877716 / 22719X55 14 Pre Old / Library name: 22719X55; GSM8877717 / 22719X56 14 Post Old / Library name: 22719X56; GSM8877720 / 22719X59 19 Pre Old / Library name: 22719X59; GSM8877721 / 22719X60 19 Post Old / Library name: 22719X60
- **Young** (14): GSM8877692 / 22719X31 01 Pre Young / Library name: 22719X31; GSM8877693 / 22719X32 01 Post Young / Library name: 22719X32; GSM8877694 / 22719X33 02 Pre Young / Library name: 22719X33; GSM8877695 / 22719X34 02 Post Young / Library name: 22719X34; GSM8877696 / 22719X35 03 Pre Young / Library name: 22719X35; GSM8877697 / 22719X36 03 Post Young / Library name: 22719X36; GSM8877698 / 22719X37 04 Pre Young / Library name: 22719X37; GSM8877699 / 22719X38 04 Post Young / Library name: 22719X38; GSM8877700 / 22719X39 05 Pre Young / Library name: 22719X39; GSM8877701 / 22719X40 05 Post Young / Library name: 22719X40; GSM8877702 / 22719X41 06 Pre Young / Library name: 22719X41; GSM8877703 / 22719X42 06 Post Young / Library name: 22719X42; GSM8877718 / 22719X57 18 Pre Young / Library name: 22719X57; GSM8877719 / 22719X58 18 Post Young / Library name: 22719X58

### `time`
- **Post** (15): GSM8877693 / 22719X32 01 Post Young / Library name: 22719X32; GSM8877695 / 22719X34 02 Post Young / Library name: 22719X34; GSM8877697 / 22719X36 03 Post Young / Library name: 22719X36; GSM8877699 / 22719X38 04 Post Young / Library name: 22719X38; GSM8877701 / 22719X40 05 Post Young / Library name: 22719X40; GSM8877703 / 22719X42 06 Post Young / Library name: 22719X42; GSM8877705 / 22719X44 08 Post Old / Library name: 22719X44; GSM8877707 / 22719X46 09 Post Old / Library name: 22719X46; GSM8877709 / 22719X48 10 Post Old / Library name: 22719X48; GSM8877711 / 22719X50 11 Post Old / Library name: 22719X50; GSM8877713 / 22719X52 12 Post Old / Library name: 22719X52; GSM8877715 / 22719X54 13 Post Old / Library name: 22719X54; GSM8877717 / 22719X56 14 Post Old / Library name: 22719X56; GSM8877719 / 22719X58 18 Post Young / Library name: 22719X58; GSM8877721 / 22719X60 19 Post Old / Library name: 22719X60
- **Pre** (15): GSM8877692 / 22719X31 01 Pre Young / Library name: 22719X31; GSM8877694 / 22719X33 02 Pre Young / Library name: 22719X33; GSM8877696 / 22719X35 03 Pre Young / Library name: 22719X35; GSM8877698 / 22719X37 04 Pre Young / Library name: 22719X37; GSM8877700 / 22719X39 05 Pre Young / Library name: 22719X39; GSM8877702 / 22719X41 06 Pre Young / Library name: 22719X41; GSM8877704 / 22719X43 08 Pre Old / Library name: 22719X43; GSM8877706 / 22719X45 09 Pre Old / Library name: 22719X45; GSM8877708 / 22719X47 10 Pre Old / Library name: 22719X47; GSM8877710 / 22719X49 11 Pre Old / Library name: 22719X49; GSM8877712 / 22719X51 12 Pre Old / Library name: 22719X51; GSM8877714 / 22719X53 13 Pre Old / Library name: 22719X53; GSM8877716 / 22719X55 14 Pre Old / Library name: 22719X55; GSM8877718 / 22719X57 18 Pre Young / Library name: 22719X57; GSM8877720 / 22719X59 19 Pre Old / Library name: 22719X59

### `subject`
- **S01** (2): GSM8877692 / 22719X31 01 Pre Young / Library name: 22719X31; GSM8877693 / 22719X32 01 Post Young / Library name: 22719X32
- **S02** (2): GSM8877694 / 22719X33 02 Pre Young / Library name: 22719X33; GSM8877695 / 22719X34 02 Post Young / Library name: 22719X34
- **S03** (2): GSM8877696 / 22719X35 03 Pre Young / Library name: 22719X35; GSM8877697 / 22719X36 03 Post Young / Library name: 22719X36
- **S04** (2): GSM8877698 / 22719X37 04 Pre Young / Library name: 22719X37; GSM8877699 / 22719X38 04 Post Young / Library name: 22719X38
- **S05** (2): GSM8877700 / 22719X39 05 Pre Young / Library name: 22719X39; GSM8877701 / 22719X40 05 Post Young / Library name: 22719X40
- **S06** (2): GSM8877702 / 22719X41 06 Pre Young / Library name: 22719X41; GSM8877703 / 22719X42 06 Post Young / Library name: 22719X42
- **S08** (2): GSM8877704 / 22719X43 08 Pre Old / Library name: 22719X43; GSM8877705 / 22719X44 08 Post Old / Library name: 22719X44
- **S09** (2): GSM8877706 / 22719X45 09 Pre Old / Library name: 22719X45; GSM8877707 / 22719X46 09 Post Old / Library name: 22719X46
- **S10** (2): GSM8877708 / 22719X47 10 Pre Old / Library name: 22719X47; GSM8877709 / 22719X48 10 Post Old / Library name: 22719X48
- **S11** (2): GSM8877710 / 22719X49 11 Pre Old / Library name: 22719X49; GSM8877711 / 22719X50 11 Post Old / Library name: 22719X50
- **S12** (2): GSM8877712 / 22719X51 12 Pre Old / Library name: 22719X51; GSM8877713 / 22719X52 12 Post Old / Library name: 22719X52
- **S13** (2): GSM8877714 / 22719X53 13 Pre Old / Library name: 22719X53; GSM8877715 / 22719X54 13 Post Old / Library name: 22719X54
- **S14** (2): GSM8877716 / 22719X55 14 Pre Old / Library name: 22719X55; GSM8877717 / 22719X56 14 Post Old / Library name: 22719X56
- **S18** (2): GSM8877718 / 22719X57 18 Pre Young / Library name: 22719X57; GSM8877719 / 22719X58 18 Post Young / Library name: 22719X58
- **S19** (2): GSM8877720 / 22719X59 19 Pre Old / Library name: 22719X59; GSM8877721 / 22719X60 19 Post Old / Library name: 22719X60

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE293163"], "assay": "bulk total RNA-seq (rRNA-depleted, stranded) of human PBMCs; STAR + featureCounts (S2.7.p2)", "sample_inclusion": "Young n=7 (2M/5F, 18-30 y) and Old n=8 (4M/4F, 55-80 y); PBMC sampled immediately before and within 1 min after a 60-min interval single-leg knee-extension bout (S2.2.p1, S2.3.p1, S2.5.p1, S2.6.p1); 30 libraries", "factors": {"age": ["Young", "Old"], "time": ["Pre", "Post"]}, "repeated_measure_unit": "participant (pre and post sample from the same person)", "primary_estimand": "acute-exercise effect (Post vs Pre) on PBMC gene expression, estimated separately within Young and within Old (S3.2.p1; S4.2.p1 'analyses were conducted separately for each age group'); secondary: baseline Old vs Young at Pre (S3.1.p1)", "planned_contrasts": ["Young Post vs Pre (S3.2.p1; paper: 53 DEGs, 52 up / 1 down, of 13,695 genes)", "Old Post vs Pre (S3.2.p1; paper: 1,026 DEGs, text lists 359 up / 572 down, of 19,101 genes)", "Baseline Old vs Young at Pre (S3.1.p1; paper: 665 DEGs, 446 up / 199 down, of 19,762 genes)"], "normalization": "DESeq2 size factors; genes with zero counts in all samples or fewer than 5 reads in every sample removed (S2.7.p2)", "paper_method": "DESeq2 1.40.2, apeglm LFC shrinkage (S2.7.p2); design formula and whether pairing was modelled are not stated", "paper_threshold": {"metric": "FDR", "cutoff": 0.01, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.8.p1", "note": "S2.8.p1: DEGs at p < 0.01 and FD ... [393 more characters]

reasoning: Study map from Methods S2.2-S2.8 and Results S3.1-S3.2. The paper fits separate DESeq2 analyses per age group (different gene universes 13,695 vs 19,101; S4.2.p1). The DEG threshold in S2.8.p1 is FDR < 0.01 (p < 0.01 is implied by it); S2.7.p2's 5% FDR is kept as an audit rule.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE293163\\GSE293163_PBMC_raw_counts.txt.gz", "owned": true, "checks": ["DA.p1 names GSE293163", "30 samples = 15 participants x pre/post, matches Young n=7 + Old n=8", "data_processing (STAR 2.7.9a, Ensembl 110, clumpify, cutadapt 1.16, featureCounts 1.6.3) matches S2.7.p2", "single deposited matrix GSE293163_PBMC_raw_counts.txt.gz"], "accession": "GSE293163", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE293163\\GSE293163_metadata.csv"}

reasoning: Accession, sample count, age split (7 Young subjects 01-06,18; 8 Old subjects 08-14,19) and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 30, "n_metadata": 30, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\aligned\\aligned_metadata.csv", "columns": {"subject": {"source": "title", "regex": "^\\S+ (\\d+) (?:Pre|Post) (?:Young|Old)$", "recode": {"01": "S01", "02": "S02", "03": "S03", "04": "S04", "05": "S05", "06": "S06", "08": "S08", "09": "S09", "10": "S10", "11": "S11", "12": "S12", "13": "S13", "14": "S14", "18": "S18", "19": "S19"}}, "time": {"source": "title", "regex": "^\\S+ \\d+ (Pre|Post) (?:Young|Old)$"}, "age": {"source": "title", "regex": "^\\S+ \\d+ (?:Pre|Post) (Young|Old)$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\aligned\\design_metadata.csv", "sha256": "50db3a1205b05fc78119783dea2f3f61dfb5e1e56713daea6344b9aa0077edb3", "levels": {"subject": {"S01": 2, "S02": 2, "S03": 2, "S04": 2, "S05": 2, "S06": 2, "S08": 2, "S09": 2, "S10": 2, "S11": 2, "S12": 2, "S13": 2, "S14": 2, "S18": 2, "S19": 2}, "time": {"Pre": 15, "Post": 15}, "age": {"Old": 16, "Young": 14}}}}

reasoning: Matrix columns (22719X31..60) are the library names that open each GEO title ('22719X31 01 Pre Young'); exact match on the derived key. Subject number, time and age are parsed from the same title; characteristics group (Pre/Post exercise) agrees with the parsed time.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\aligned\\aligned_matrix.csv", "sha256": "f3726ac976527cb2c5ff20e94d19313b64e4175cb7423f48328259ea6faa0335", "n_features": 62754, "n_samples": 30, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 391352.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: 100% integers, max 391,352, median 0; data_processing says featureCounts output combined into one matrix; paper ran DESeq2 on these counts (S2.7.p2).

### design (valid, not_started)

final: {"analysis_type": "repeated-measures two-group within strata plus a cross-sectional baseline contrast", "design_column": "time", "contrasts": [{"name": "young_post_vs_pre", "control": "Pre", "treatment": "Post", "subset": {"age": ["Young"]}, "role": "primary"}, {"name": "old_post_vs_pre", "control": "Pre", "treatment": "Post", "subset": {"age": ["Old"]}, "role": "primary"}, {"name": "baseline_old_vs_young", "design_column": "age", "control": "Young", "treatment": "Old", "subset": {"time": ["Pre"]}, "role": "secondary", "estimand_type": "associational"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: Paper reports exercise response separately in Young and in Old and a baseline Old vs Young comparison (S3.1.p1, S3.2.p1, S4.2.p1). Pre and Post come from the same person, so subject is the repeated-measure unit. The baseline comparison is cross-sectional (associational), not an exercise effect.

rejected alternatives: [{"value": "one joint model ~ subject + age:time with all 30 samples", "reason_rejected": "paper fits separate analyses per age group (S4.2.p1, separate gene universes); kept the paper's separate fits"}, {"value": "pooled Post vs Pre across ages", "reason_rejected": "paper's estimand is age-specific (S3.2.p1); pooling is not reported"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking term for the within-age Post vs Pre fits (paired pre/post samples)"}, {"name": "sex", "disposition": "not in GEO metadata; not modelled (paper did not adjust)"}], "design_check": {"formula_equivalent": "~ C(age) + C(time) + C(subject)", "n_samples": 30, "n_columns": 17, "columns": ["Intercept", "age_Young", "time_Pre", "subject_S02", "subject_S03", "subject_S04", "subject_S05", "subject_S06", "subject_S08", "subject_S09", "subject_S10", "subject_S11", "subject_S12", "subject_S13", "subject_S14", "subject_S18", "subject_S19"], "rank": 16, "full_rank": false, "residual_df": 14, "levels": {"age": {"Old": 16, "Young": 14}, "time": {"Pre": 15, "Post": 15}, "subject": {"S01": 2, "S02": 2, "S03": 2, "S04": 2, "S05": 2, "S06": 2, "S08": 2, "S09": 2, "S10": 2, "S11": 2, "S12": 2, "S13": 2, "S14": 2, "S18": 2, "S19": 2}}, "cells": [{"cell": ["Old", "Post", "S08"], "n": 1}, {"cell": ["Old", "Post", "S09"], "n": 1}, {"cell": ["Old", "Post", "S10"], "n": 1}, {"cell": ["Old", "Post", "S11"], "n": 1}, {"cell": ["Old", "Post", "S12"], "n": 1}, {"cell": ["Old", "Post", "S13"], "n": 1}, {"cell": ["Old", "Post", "S14"], "n": 1}, {"cell": ["Old", "Post", "S19"], "n": 1}, {"cell": ["Old", "Pre", "S08"], "n": 1}, {"cell": ["Old", "Pre", "S09"], "n": 1}, {"cell": ["Old", "Pre", "S10"], "n": 1}, {"cell": ["Old", "Pre", "S11"], "n": 1}, {"cell": ["Old", "Pre", "S12"], "n": 1}, {"cell": [" ... [3821 more characters]

reasoning: Each participant contributes Pre and Post; blocking on subject is the correct covariance for the within-age contrasts. The paper does not state its formula; a paired fit is the standard DESeq2 route for this design and an unpaired sensitivity fit is run to see which matches the paper. The baseline fit has one sample per subject, so no blocking.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ subject + time (within each age group); ~ age (Pre samples only)", "paper_route": {"method": "DESeq2 1.40.2 with apeglm LFC shrinkage", "status": "reproduced_with_pydeseq2", "reason": "pydeseq2 Wald test reproduces the DESeq2 test; pydeseq2 lfc_shrink (apeGLM-type prior) is written as log2FoldChange_shrunk; padj is unaffected by shrinkage"}, "deviations": ["Paper low-count filter (drop genes with < 5 reads in every sample) approximated per execution as CPM >= 0.4 in at least 1 sample (5 reads / 12.7M median library size)", "Paper does not state pairing; paired (~ subject + time) is primary, unpaired (~ time) is a sensitivity run", "pydeseq2 instead of R DESeq2 1.40.2; shrunken LFC from pydeseq2 lfc_shrink in log2FoldChange_shrunk, MLE in log2FoldChange"]}

reasoning: Raw featureCounts integers support DESeq2, the paper's method.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "S2.8.p1 DEG rule p < 0.01 and FDR < 0.01 (FDR < 0.01 implies p < 0.01). Audit rule = S2.7.p2's 5% FDR. The mean-log2FC subset used for g:Profiler/IPA is not applied to the DEG counts."}

reasoning: S2.8.p1 states the DEG threshold; S2.7.p2 gives a conflicting 5% FDR, recorded as the audit rule.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "young_post_vs_pre", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\young_post_vs_pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\young_post_vs_pre\\DEG_results_Post_vs_Pre.csv"], "counts": {"young_post_vs_pre": {"applied": {"rule": "padj < 0.01", "n_tested": 14178, "n_significant": 99, "n_up": 97, "n_down": 2, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14178, "n_significant": 179, "n_up": 166, "n_down": 13, "deg_sanity": "ok"}}}}

reasoning: Paper's Young pre vs post DESeq2, paired by subject

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "old_post_vs_pre", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\old_post_vs_pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\old_post_vs_pre\\DEG_results_Post_vs_Pre.csv"], "counts": {"old_post_vs_pre": {"applied": {"rule": "padj < 0.01", "n_tested": 24541, "n_significant": 3613, "n_up": 1195, "n_down": 2418, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 24541, "n_significant": 5740, "n_up": 2266, "n_down": 3474, "deg_sanity": "ok"}}}}

reasoning: Paper's Old pre vs post DESeq2, paired by subject

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "baseline_old_vs_young", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 15, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\baseline_old_vs_young\\input\\matrix_filtered.csv", "formula": "~ age", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\baseline_old_vs_young\\DEG_results_Old_vs_Young.csv"], "counts": {"baseline_old_vs_young": {"applied": {"rule": "padj < 0.01", "n_tested": 21665, "n_significant": 1589, "n_up": 1063, "n_down": 526, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 21665, "n_significant": 3634, "n_up": 2258, "n_down": 1376, "deg_sanity": "ok"}}}}

reasoning: Paper's baseline Old vs Young (Pre samples, one per subject)

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "young_post_vs_pre_unpaired", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\young_post_vs_pre_unpaired\\input\\matrix_filtered.csv", "formula": "~ time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\young_post_vs_pre_unpaired\\DEG_results_Post_vs_Pre.csv"], "counts": {"young_post_vs_pre_unpaired": {"applied": {"rule": "padj < 0.01", "n_tested": 23913, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 23913, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paper does not state pairing; unpaired ~ time sensitivity

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "old_post_vs_pre_unpaired", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\old_post_vs_pre_unpaired\\input\\matrix_filtered.csv", "formula": "~ time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\old_post_vs_pre_unpaired\\DEG_results_Post_vs_Pre.csv"], "counts": {"old_post_vs_pre_unpaired": {"applied": {"rule": "padj < 0.01", "n_tested": 24054, "n_significant": 2274, "n_up": 561, "n_down": 1713, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 24054, "n_significant": 3927, "n_up": 1290, "n_down": 2637, "deg_sanity": "ok"}}}}

reasoning: Paper does not state pairing; unpaired ~ time sensitivity

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "young_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_young_post_vs_pre\\ora\\DEG_results_Post_vs_Pre_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_young_post_vs_pre\\ora\\DEG_results_Post_vs_Pre_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_young_post_vs_pre\\ora\\DEG_results_Post_vs_Pre_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_young_post_vs_pre\\ora\\DEG_results_Post_vs_Pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 99 Human genes (direction=all, padj<0.01, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Regulation Of Type II Interferon Production (GO:0032649) | padj=2.88e-02 | overlap=5/87 | genes=PDE4D;LGALS9C;CD244;IL18R1;IL12RB2 - Natural Killer ... [1193 more characters]

reasoning: paper reports GO processes for the Young exercise response (S3.2.p1)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "young_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_young_post_vs_pre\\gsea\\DEG_results_Post_vs_Pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 19709 Human genes ranked by 'stat'. 50 Hallmark sets tested, 35 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=2.96 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.34 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APOPTOSIS | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.20 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.13 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PROTEIN_SECRETION | NES=2.09 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL2_STAT5_SIGNALING | NES=2.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_TGF_BETA_SIGNALING | NES=2.06 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MTORC1_SIGNALING | NES=1.95 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_HYPOXIA | NES=1.94 | NOM p=0.00e+00 | FDR q=0.00e+00 ### Top 6 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V2 | NES=-2.14 | NOM p=0.00e+00 | FDR q=2.87e-04 - HALLMARK_APICAL_JUNCTION | NES=-1.44 | NOM p=7.33e-03 | FDR q=5.59e-02 - HALLMAR ... [396 more characters]

reasoning: paper reports GO processes for the Young exercise response (S3.2.p1)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "old_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_old_post_vs_pre\\ora\\DEG_results_Post_vs_Pre_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_old_post_vs_pre\\ora\\DEG_results_Post_vs_Pre_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_old_post_vs_pre\\ora\\DEG_results_Post_vs_Pre_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_old_post_vs_pre\\ora\\DEG_results_Post_vs_Pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 3116 Human genes (direction=all, padj<0.01, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Macrophage Activation (GO:0042116) | padj=4.78e-01 | overlap=15/35 | genes=EDN2;IFNGR1;IL13;AZU1;CLU;TNF;FOXP1;TLR1;FCER2;FCGR3A;SBNO2;MYO1C;PLCG2;JAK2;TLR ... [1183 more characters]

reasoning: paper reports GO processes for the Old exercise response (S3.2.p1)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "old_post_vs_pre", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40695537\\GSE293163\\results\\enrichment_old_post_vs_pre\\gsea\\DEG_results_Post_vs_Pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 20503 Human genes ranked by 'stat'. 50 Hallmark sets tested, 27 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_PROTEIN_SECRETION | NES=2.47 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.15 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.90 | NOM p=0.00e+00 | FDR q=1.14e-03 - HALLMARK_MTORC1_SIGNALING | NES=1.81 | NOM p=0.00e+00 | FDR q=2.85e-03 - HALLMARK_TGF_BETA_SIGNALING | NES=1.73 | NOM p=3.38e-03 | FDR q=5.71e-03 - HALLMARK_COMPLEMENT | NES=1.70 | NOM p=0.00e+00 | FDR q=6.42e-03 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.67 | NOM p=0.00e+00 | FDR q=8.88e-03 - HALLMARK_ANDROGEN_RESPONSE | NES=1.58 | NOM p=0.00e+00 | FDR q=1.68e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYOGENESIS | NES=-2.18 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=-1.79 | NOM p=0.00e+00 | FDR q=3.69e-03 - H ... [387 more characters]

reasoning: paper reports GO processes for the Old exercise response (S3.2.p1)

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Paper's design formula/pairing is not stated; paired fit is primary", "Paper's up/down split for Old (359+572=931) does not sum to its 1,026 total; baseline 446+199=645 vs 665", "Baseline Old vs Young is associational (cross-sectional), not an exercise effect", "No sex covariate available in GEO metadata", "Paper's reported counts (665/53/1026) most likely are the post-hoc subset of FDR<0.01 genes with log2FC beyond the direction-specific mean (FIG1 legend colours '>mean Log2 fold-change'). Applying that subset to our tables gives Young 44 (43 up/1 down SH2D3A), Old 1,301 (376/925), baseline 634 (459/175) with MLE LFC; 42/1, 386/881, 467/172 with shrunken LFC. The runner's applied counts are the plain FDR<0.01 rule (99 / 3,613 / 1,589).", "Unpaired Young sensitivity fit gives 0 DEGs at FDR<0.01, so the paper's 53 Young DEGs imply a paired (subject-blocked) model."], "results": {"young_post_vs_pre": {"n_deg": 99, "up": 97, "down": 2, "rule": "padj < 0.01", "audit_n": 179}, "old_post_vs_pre": {"n_deg": 3613, "up": 1195, "down": 2418, "rule": "padj < 0.01", "audit_n": 5740}, "baseline_old_vs_young": {"n_deg": 1589, "up": 1063, "down": 526, "rule": "padj < 0.01", "audit_n": 3634}, "young_post_vs_pre_unpaired": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.01", "audit_n": 0}, "old_post_vs_pre_unpaired": {"n_deg": 2274, "up": 561, "down": 1713, "rule": "padj < 0.01", "audit_n": 3927}}, "paper_counts": {"young_post_vs_pre": 53, "old_post_ ... [351 more characters]

reasoning: Counts from S3.1.p1 and S3.2.p1; SH2D3A is the single down-regulated gene in Young (S3.2.p1).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); data_processing: omit (constant: carries no batch information); library_selection: omit (constant: carries no batch information); library_source: omit (constant: carries no batch information); library_strategy: omit (constant: carries no batch information); age: between_subjects (constant within each subject: fit within-subject differences (paired_change) or a mixed model; not subject + factor in one fixed model) |
- | Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG FDR threshold",
    "paper": "S2.7.p2: 5% FDR; S2.8.p1: FDR < 0.01",
    "data": "both computable",
    "disposition": "executable_without_change"
  },
  {
    "item": "Old up/down split",
    "paper": "1,026 total but 359 up + 572 down = 931",
    "data": "n/a",
    "disposition": "executable_without_change"
  },
  {
    "item": "Pairing",
    "paper": "not stated",
    "data": "subject IDs available for all 30 samples",
    "disposition": "executable_without_change"
  },
  {
    "item": "Low-count filter",
    "paper": "drop genes with <5 reads in every sample",
    "data": "runner filter is CPM-based",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40695537 / GSE293163

## What ran
- Case spec route (`case_spec.json`, `python -m tools.case_runner execute`), run completed, decision-contract validator: 18 records, 0 errors. (Executed twice: the second run fixed the method record and added study caveats. The first attempt is in `_previous/`.)
- Data: `GSE293163_PBMC_raw_counts.txt.gz` (featureCounts integers, 62,754 Ensembl genes x 30 libraries). Aligned exactly on the library ID from the GEO title (30/30). Subject, time (Pre/Post) and age (Young/Old) come from the title: 7 Young + 8 Old participants, each with Pre and Post.
- DESeq2 (pydeseq2 Wald), one fit per contrast, as the paper describes (S4.2.p1 says the age groups were analysed separately):
  - `young_post_vs_pre`: `~ subject + time`, 7 complete pairs (primary)
  - `old_post_vs_pre`: `~ subject + time`, 8 complete pairs (primary)
  - `baseline_old_vs_young`: `~ age` on the Pre samples (secondary, associational)
  - Unpaired `~ time` sensitivity fits for Young and for Old
- Low-count filter: the paper drops genes with fewer than 5 reads in every sample. Here it is approximated per execution as CPM >= 0.4 in at least 1 sample (5 reads / 12.7M median library size).
- Enrichment: ORA (Enrichr GO/KEGG) and Hallmark GSEA on both exercise tables, all completed.

## Threshold
- Paper threshold (S2.8.p1): DEGs at p < 0.01 and FDR < 0.01, which is applied as padj < 0.01. The paper then keeps, for g:Profiler/IPA, only the genes whose log2FC is beyond the mean log2FC of their direction.
- S2.7.p2 states 5% FDR, which conflicts with S2.8.p1. It is used here as the audit rule (padj < 0.05).

## DEG counts vs paper
| Contrast | Ours padj<0.01 (up/down) | Ours padj<0.05 | Ours mean-LFC subset (MLE / shrunk) | Paper |
|---|---|---|---|---|
| Young Post vs Pre | 99 (97/2) | 179 | 44 (43/1) / 43 (42/1) | 53 (52/1), of 13,695 genes |
| Old Post vs Pre | 3,613 (1,195/2,418) | 5,740 | 1,301 (376/925) / 1,267 (386/881) | 1,026 (359 up / 572 down as printed) |
| Baseline Old vs Young | 1,589 (1,063/526) | 3,634 | 634 (459/175) / 639 (467/172) | 665 (446/199) |

- The paper's counts match our padj < 0.01 genes after its mean-log2FC subset step (the FIG1 legend colours genes ">mean Log2 fold-change"). The plain FDR rule overcounts by 2-3.5x. The runner's recorded counts are the plain rule. The subset comparison is recorded in the study caveats.
- Direction agrees with the paper:
  - Young is almost all up, with 1 down gene. That gene is SH2D3A (ENSG00000 ... [1925 more characters]
