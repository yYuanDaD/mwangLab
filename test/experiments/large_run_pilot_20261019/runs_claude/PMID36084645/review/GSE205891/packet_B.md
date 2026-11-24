# Review packet B (the analysis' decisions): GSE205891

## Mechanical flags

- **numeric_blocking_ids**: {"column": "subject", "note": "blocking IDs are all numbers; confirm the executor treated them as categories"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| muscle_ILT_post_vs_pre | 1540 | 1382 | padj < 0.05 and |log2FoldChange| > 0.3 | 1997 | 331 | 51 | 3101 | 4138 | 413 | 61 | 2245 | 0.049 | 0.311 |
| muscle_SC_post_vs_pre | 65 | 0 | padj < 0.05 and |log2FoldChange| > 0.3 | 0 | 0 | 0 | 0 | 922 | 123 | 18 | 217 | 0.089 | 0.07 |

## Samples per design level

### `time`
- **post** (31): GSM6234949 / Muscle_003B; GSM6234951 / Muscle_004B; GSM6234953 / Muscle_008B; GSM6234955 / Muscle_013B; GSM6234957 / Muscle_021B; GSM6234959 / Muscle_025B; GSM6234961 / Muscle_026B; GSM6234963 / Muscle_029B; GSM6234965 / Muscle_030B; GSM6234967 / Muscle_033B; GSM6234969 / Muscle_039B; GSM6234971 / Muscle_040B; GSM6234973 / Muscle_043B; GSM6234975 / Muscle_044B; GSM6234977 / Fat_003B; GSM6234979 / Fat_004B; GSM6234981 / Fat_008B; GSM6234983 / Fat_013B; GSM6234985 / Fat_018B; GSM6234987 / Fat_019B; GSM6234989 / Fat_021B; GSM6234991 / Fat_025B; GSM6234993 / Fat_026B; GSM6234995 / Fat_029B; GSM6234997 / Fat_030B; GSM6234999 / Fat_032B; GSM6235001 / Fat_033B; GSM6235003 / Fat_039B; GSM6235005 / Fat_040B; GSM6235007 / Fat_043B; GSM6235009 / Fat_044B
- **pre** (31): GSM6234948 / Muscle_003A; GSM6234950 / Muscle_004A; GSM6234952 / Muscle_008A; GSM6234954 / Muscle_013A; GSM6234956 / Muscle_021A; GSM6234958 / Muscle_025A; GSM6234960 / Muscle_026A; GSM6234962 / Muscle_029A; GSM6234964 / Muscle_030A; GSM6234966 / Muscle_033A; GSM6234968 / Muscle_039A; GSM6234970 / Muscle_040A; GSM6234972 / Muscle_043A; GSM6234974 / Muscle_044A; GSM6234976 / Fat_003A; GSM6234978 / Fat_004A; GSM6234980 / Fat_008A; GSM6234982 / Fat_013A; GSM6234984 / Fat_018A; GSM6234986 / Fat_019A; GSM6234988 / Fat_021A; GSM6234990 / Fat_025A; GSM6234992 / Fat_026A; GSM6234994 / Fat_029A; GSM6234996 / Fat_030A; GSM6234998 / Fat_032A; GSM6235000 / Fat_033A; GSM6235002 / Fat_039A; GSM6235004 / Fat_040A; GSM6235006 / Fat_043A; GSM6235008 / Fat_044A

### `subject`
- **003** (4): GSM6234948 / Muscle_003A; GSM6234949 / Muscle_003B; GSM6234976 / Fat_003A; GSM6234977 / Fat_003B
- **004** (4): GSM6234950 / Muscle_004A; GSM6234951 / Muscle_004B; GSM6234978 / Fat_004A; GSM6234979 / Fat_004B
- **008** (4): GSM6234952 / Muscle_008A; GSM6234953 / Muscle_008B; GSM6234980 / Fat_008A; GSM6234981 / Fat_008B
- **013** (4): GSM6234954 / Muscle_013A; GSM6234955 / Muscle_013B; GSM6234982 / Fat_013A; GSM6234983 / Fat_013B
- **018** (2): GSM6234984 / Fat_018A; GSM6234985 / Fat_018B
- **019** (2): GSM6234986 / Fat_019A; GSM6234987 / Fat_019B
- **021** (4): GSM6234956 / Muscle_021A; GSM6234957 / Muscle_021B; GSM6234988 / Fat_021A; GSM6234989 / Fat_021B
- **025** (4): GSM6234958 / Muscle_025A; GSM6234959 / Muscle_025B; GSM6234990 / Fat_025A; GSM6234991 / Fat_025B
- **026** (4): GSM6234960 / Muscle_026A; GSM6234961 / Muscle_026B; GSM6234992 / Fat_026A; GSM6234993 / Fat_026B
- **029** (4): GSM6234962 / Muscle_029A; GSM6234963 / Muscle_029B; GSM6234994 / Fat_029A; GSM6234995 / Fat_029B
- **030** (4): GSM6234964 / Muscle_030A; GSM6234965 / Muscle_030B; GSM6234996 / Fat_030A; GSM6234997 / Fat_030B
- **032** (2): GSM6234998 / Fat_032A; GSM6234999 / Fat_032B
- **033** (4): GSM6234966 / Muscle_033A; GSM6234967 / Muscle_033B; GSM6235000 / Fat_033A; GSM6235001 / Fat_033B
- **039** (4): GSM6234968 / Muscle_039A; GSM6234969 / Muscle_039B; GSM6235002 / Fat_039A; GSM6235003 / Fat_039B
- **040** (4): GSM6234970 / Muscle_040A; GSM6234971 / Muscle_040B; GSM6235004 / Fat_040A; GSM6235005 / Fat_040B
- **043** (4): GSM6234972 / Muscle_043A; GSM6234973 / Muscle_043B; GSM6235006 / Fat_043A; GSM6235007 / Fat_043B
- **044** (4): GSM6234974 / Muscle_044A; GSM6234975 / Muscle_044B; GSM6235008 / Fat_044A; GSM6235009 / Fat_044B

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE205891"], "assay": "bulk total RNA-seq (Illumina NovaSeq 6000), human skeletal muscle and subcutaneous abdominal adipose tissue biopsies (S4.3.4.2.p1, key resources table)", "primary_estimand": "Within-group change in skeletal muscle gene expression after vs before 8 months of intensive lifestyle therapy (ILT: dietary energy restriction plus supervised exercise training 4 x 60 min/week) in people with obesity and T2D; the same within-group change in the standard-care (SC) arm is reported alongside (S2.6.p1, FIG3). Exercise is not separable from energy restriction/weight loss in this design: the estimand is the effect of the combined lifestyle intervention.", "factors": {"arm": ["SC", "ILT"], "time": ["before", "after"], "tissue": ["skeletal muscle", "subcutaneous adipose"]}, "repeated_measure_unit": "participant (before and after biopsies from the same person)", "inclusion": "Muscle RNA-seq: SC n=6, ILT n=8 participants (FIG3); adipose: SC n=7, ILT n=10 (FIG4). 9 women + 1 man in ILT, 8 women in SC among completers (S2.1.p1).", "planned_contrasts": ["Muscle ILT after vs before, paired (S2.6.p1, FIG3A; paper: 1,540 DEGs, Table S3)", "Muscle SC after vs before, paired (S2.6.p1, FIG3A; paper: 65 DEGs, Table S2)", "Adipose ILT and SC after vs before: selected-gene results only (S2.7.p1, FIG4; ECM genes SPARC, LOX, LOXL1, TNMD, PDGFA, SEMA3C down after ILT; IL6, TNF, CCL2, CCL5, CD68, CD74 unchanged); no DEG count reported"], "paper_method": "edgeR (P value and ... [737 more characters]

reasoning: S2.6.p1 and FIG3 define the muscle DEG analysis as after-vs-before within each arm with log2|FC|>0.3 and FDR<0.05; S4.4.p1 names edgeR; key resources table names GSE205891 for muscle RNA-seq. S2.7.p1/FIG4 report adipose selected genes only. S1.p3/S4.3.3.p1: ILT = energy restriction + supervised exercise; the transcriptomic effect cannot be attributed to exercise alone.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE205891\\GSE205891_LID_all.gene_moderated_log2cpm.csv", "owned": true, "checks": ["key resources table lists GSE205891 for skeletal muscle RNA-seq", "GEO growth protocol describes muscle and SAT from people with obesity and T2D before/after SC and ILT", "28 muscle samples = 14 subjects x 2 (SC 6 + ILT 8, matches FIG3); 34 adipose samples = 17 x 2 (SC 7 + ILT 10, matches FIG4)"], "accession": "GSE205891", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE205891\\GSE205891_metadata.csv"}

reasoning: Accession, tissues, arms, and per-arm subject counts all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 62, "n_metadata": 62, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\aligned\\aligned_metadata.csv", "columns": {"time": {"alias_of": "characteristics_ch1.0.sample type", "recode": {"Before": "pre", "After": "post"}}, "arm": {"alias_of": "characteristics_ch1.1.treatment"}, "tissue": {"source": "title", "regex": "^(Muscle|Fat)_\\d+[AB]$", "recode": {"Muscle": "muscle", "Fat": "fat"}}, "subject": {"source": "title", "regex": "^(?:Muscle|Fat)_(\\d+)[AB]$"}, "visit": {"source": "title", "regex": "^(?:Muscle|Fat)_\\d+([AB])$", "recode": {"A": "pre", "B": "post"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\aligned\\design_metadata.csv", "sha256": "09fbe0363845404f8d686f577cba3df557efb717ee437326fd64630e55988e17", "levels": {"time": {"pre": 31, "post": 31}, "arm": {"ILT": 36, "SC": 26}, "tissue": {"fat": 34, "muscle": 28}, "subject": {"003": 4, "004": 4, "008": 4, "013": 4, "021": 4, "025": 4, "026": 4, "029": 4, "030": 4, "033": 4, "039": 4, "040": 4, "043": 4, "044": 4, "018": 2, "019": 2, "032": 2}, "visit": {"pre": 31, "post": 31}}}}

reasoning: Matrix columns equal metadata title exactly for 62/62 (inspect alignment_keys). Subject = 3-digit participant id in the title; tissue prefix; A/B suffix is cross-checked against the GEO sample type (A=Before, B=After in every row).

### matrix (valid, not_started)

final: {"matrix_type": "log2 CPM (moderated, prior count; edgeR-style log-CPM)", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\aligned\\aligned_matrix.csv", "sha256": "282357715c79077d7cbbbd921eca3befb6840e59f5ccb057be5fb4f43804c506", "n_features": 34259, "n_samples": 62, "annotation_columns_dropped": [], "duplicated_feature_ids": 121, "missing_values": 0, "negative_values": 1243450, "negative_fraction": 0.585412, "min": -5.99472050229905, "max": 18.3755062427738, "median": -1.71672666301264, "integer_fraction": 0.0, "candidates": ["signed_log_scale (log ratios, M-values, or centered data)"]}}

reasoning: File name 'gene_moderated_log2cpm'; data_processing: CPM from featureCounts counts, log-transformed. Values are continuous (integer fraction 0), range -6.0 to 18.4; 2^x sums to ~1e6 per column, confirming log2 CPM. Paper input was raw counts (edgeR); raw counts were not deposited and cannot be recovered without library sizes.

### design (valid, not_started)

final: {"analysis_type": "paired two-timepoint within arm and tissue (+ exploratory arm x time change comparison)", "design_column": "time", "control": "pre", "treatment": "post", "contrasts": [{"name": "muscle_ILT_post_vs_pre", "control": "pre", "treatment": "post", "role": "primary", "subset": {"tissue": "muscle", "arm": "ILT"}}, {"name": "muscle_SC_post_vs_pre", "control": "pre", "treatment": "post", "role": "secondary", "subset": {"tissue": "muscle", "arm": "SC"}}, {"name": "fat_ILT_post_vs_pre", "control": "pre", "treatment": "post", "role": "secondary", "subset": {"tissue": "fat", "arm": "ILT"}}, {"name": "fat_SC_post_vs_pre", "control": "pre", "treatment": "post", "role": "secondary", "subset": {"tissue": "fat", "arm": "SC"}}, {"name": "muscle_change_ILT_vs_SC", "role": "exploratory", "note": "randomized between-arm difference in paired change; not reported as DEGs by the paper"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\suitability\\suitability.md", "n_comparisons": 4, "n_analyzable": 4}}

reasoning: Paper (S2.6.p1, FIG3A) reports after-vs-before DEGs within each arm in muscle. Tissue and arm are strata; time is the tested factor with subject blocking. The randomized arm x time contrast (ILT change minus SC change) is added as exploratory because it best isolates the lifestyle effect from season/time; the paper uses this ANCOVA-type comparison only for selected genes. Estimand note: ILT combines energy restriction (17% weight loss) with exercise training, so effects are of lifestyle therapy, not exercise alone.

rejected alternatives: [{"value": "pooled SC+ILT after vs before", "reason_rejected": "paper analyzes arms separately; pooling mixes intervention and control"}, {"value": "ILT vs SC at follow-up only (unpaired)", "reason_rejected": "ignores baseline and pairing; not the paper's estimand"}, {"value": "muscle and fat in one model", "reason_rejected": "different tissues; paper analyses them separately; tissue is a stratum"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking (paired before/after within participant)"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 62, "n_columns": 18, "columns": ["Intercept", "time_pre", "subject_18", "subject_19", "subject_21", "subject_25", "subject_26", "subject_29", "subject_3", "subject_30", "subject_32", "subject_33", "subject_39", "subject_4", "subject_40", "subject_43", "subject_44", "subject_8"], "rank": 18, "full_rank": true, "residual_df": 44, "levels": {"time": {"pre": 31, "post": 31}, "subject": {"3": 4, "4": 4, "8": 4, "13": 4, "21": 4, "25": 4, "26": 4, "29": 4, "30": 4, "33": 4, "39": 4, "40": 4, "43": 4, "44": 4, "18": 2, "19": 2, "32": 2}}, "cells": [{"cell": ["post", "13"], "n": 2}, {"cell": ["post", "18"], "n": 1}, {"cell": ["post", "19"], "n": 1}, {"cell": ["post", "21"], "n": 2}, {"cell": ["post", "25"], "n": 2}, {"cell": ["post", "26"], "n": 2}, {"cell": ["post", "29"], "n": 2}, {"cell": ["post", "3"], "n": 2}, {"cell": ["post", "30"], "n": 2}, {"cell": ["post", "32"], "n": 1}, {"cell": ["post", "33"], "n": 2}, {"cell": ["post", "39"], "n": 2}, {"cell": ["post", "4"], "n": 2}, {"cell": ["post", "40"], "n": 2}, {"cell": ["post", "43"], "n": 2}, {"cell": ["post", "44"], "n": 2}, {"cell": ["post", "8"], "n": 2}, {"cell": ["pre", "13"], "n": 2}, {"cell": ["pre", "18"], "n": 1}, {"cell": ["pre", "19"], "n": 1}, {"cell": ["pre", "21"], "n": 2}, {"cell": ... [871 more characters]

reasoning: Before and after biopsies come from the same participant, so participant is a blocking factor (paired design; paper uses paired t-tests for within-group changes, S4.4.p1). No batch or sex column in GEO; sex (1 man in ILT) is constant within subject and absorbed by the subject block.

### method (valid, not_started)

final: {"matrix_type": "log2 CPM (moderated, prior count; edgeR-style log-CPM)", "method": "limma (moderated t, eBayes) with subject blocking, on deposited log2 CPM", "formula": "~ C(subject) + Treatment (Treatment = post vs pre)", "paper_route": {"method": "edgeR on featureCounts gene counts", "status": "blocked", "reason": "raw counts not deposited; only moderated log2 CPM available, and library sizes are not provided to back-calculate counts"}, "deviations": ["limma on log2 CPM instead of edgeR on counts", "low-expression filter log2CPM >= 0 (about CPM >= 1) in at least as many samples as the smaller time group of the execution, a standard edgeR/limma step the paper does not describe", "duplicated gene symbols (121 extra rows) collapsed by the executor to the highest-mean row", "pairing by subject explicitly modelled; paper's edgeR pairing unstated"]}

reasoning: Matrix and method policy: log-scale CPM goes to limma. Paired design ~ subject + time within each arm/tissue subset.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.3, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.3, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "paper rule (FDR<0.05 and log2|FC|>0.3) applied unchanged to limma BH-adjusted p and limma log2 fold change"}

reasoning: S4.4.p1: 'log2 |fold change| > 0.3 and FDR < 0.05'.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "muscle_ILT_post_vs_pre", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\muscle_ILT_post_vs_pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\muscle_ILT_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"muscle_ILT_post_vs_pre": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 13285, "n_significant": 1382, "n_up": 906, "n_down": 476, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13285, "n_significant": 1997, "n_up": 1209, "n_down": 788, "deg_sanity": "ok"}}}}

reasoning: paper's primary muscle ILT after-vs-before contrast, paired by participant (8 pairs)

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "muscle_SC_post_vs_pre", "role": "secondary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\muscle_SC_post_vs_pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\muscle_SC_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"muscle_SC_post_vs_pre": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 13215, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13215, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: paper's muscle SC after-vs-before contrast (6 pairs)

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "fat_ILT_post_vs_pre", "role": "secondary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\fat_ILT_post_vs_pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\fat_ILT_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"fat_ILT_post_vs_pre": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 14906, "n_significant": 1764, "n_up": 1122, "n_down": 642, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14906, "n_significant": 3817, "n_up": 2622, "n_down": 1195, "deg_sanity": "ok"}}}}

reasoning: adipose ILT after vs before (10 pairs); paper reports selected genes only

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "fat_SC_post_vs_pre", "role": "secondary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\fat_SC_post_vs_pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\fat_SC_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"fat_SC_post_vs_pre": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 14893, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 14893, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: adipose SC after vs before (7 pairs)

### execution (valid, completed)

final: {"method": "run_multigroup_analysis", "subset": "muscle_change_ILT_vs_SC", "role": "exploratory", "tool": "tools.multigroup_tools:run_multigroup_analysis", "n_samples": 28, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\muscle_change_ILT_vs_SC\\input\\matrix_filtered.csv", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\muscle_change_ILT_vs_SC\\followup_post\\DEG_results_ILT_vs_SC_change.csv"], "counts": {"muscle_change_ILT_vs_SC/ILT_vs_SC_change": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 0.3", "n_tested": 13359, "n_significant": 95, "n_up": 72, "n_down": 23, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13359, "n_significant": 95, "n_up": 72, "n_down": 23, "deg_sanity": "ok"}}}}

reasoning: randomized arm x time estimand: per-subject change (post - pre) compared between ILT (8) and SC (6)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "muscle_ILT_post_vs_pre", "feature_id_type": "gene_symbol", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.3, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\enrichment_muscle_ILT_post_vs_pre\\ora\\DEG_results_post_vs_pre_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\enrichment_muscle_ILT_post_vs_pre\\ora\\DEG_results_post_vs_pre_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\enrichment_muscle_ILT_post_vs_pre\\ora\\DEG_results_post_vs_pre_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\enrichment_muscle_ILT_post_vs_pre\\ora\\DEG_results_post_vs_pre_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 1382 Human genes (direction=all, padj<0.05, |log2FC|>0.3). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Respiration (GO:0045333) | padj=1.34e-12 | overlap=32/85 | genes=COX7B;NDUFB8;NDUFB10;COX15;COX4I1;ETFDH;NDUFB1;C ... [1216 more characters]

reasoning: paper reports IPA pathways on ILT muscle DEGs (FIG3B); ORA (GO/KEGG) and Hallmark GSEA are a substitute (IPA not available)

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "muscle_ILT_post_vs_pre", "feature_id_type": "gene_symbol", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36084645\\GSE205891\\results\\enrichment_muscle_ILT_post_vs_pre\\gsea\\DEG_results_post_vs_pre_GSEA_Hallmark.csv"], "summary": "GSEA complete on 13285 Human genes ranked by 'stat'. 50 Hallmark sets tested, 30 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.29 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.33 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.27 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.09 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=1.84 | NOM p=1.66e-03 | FDR q=6.98e-04 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.79 | NOM p=0.00e+00 | FDR q=1.75e-03 - HALLMARK_MYC_TARGETS_V2 | NES=1.77 | NOM p=1.46e-03 | FDR q=2.16e-03 - HALLMARK_PEROXISOME | NES=1.76 | NOM p=0.00e+00 | FDR q=2.47e-03 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.71 | NOM p=4.84e-03 | FDR q=5.04e-03 - HALLMARK_CHOLESTEROL_HOMEOSTASIS | NES=1.58 | NOM p=5.84e-03 | FDR q=1.92e-02 ### Top 8 DOWN (NES < 0, depleted in treatment): - HALLMARK_G2M_CHECKPOINT | NES=-1.79 | NOM p=0.00e+00 | FDR q=6.33e-03 - HALLMARK_MYOGENESIS | NES=-1.30 | NOM p=8.10e-03 | FDR q=2.39e-01  ... [400 more characters]

reasoning: paper reports IPA pathways on ILT muscle DEGs (FIG3B); ORA (GO/KEGG) and Hallmark GSEA are a substitute (IPA not available)

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Exercise is confounded with dietary energy restriction and ~17% weight loss in ILT; results describe lifestyle therapy, not exercise alone.", "Paper used edgeR on counts; this run uses limma on deposited log2 CPM, so DEG counts are not expected to match exactly.", "Within-arm before/after changes are not randomized comparisons; the arm x time exploratory contrast is the randomized estimand but has low power (6 vs 8 subjects)."], "results": {"muscle_ILT_post_vs_pre": {"n_deg": 1382, "up": 906, "down": 476, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 1997}, "muscle_SC_post_vs_pre": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 0}, "fat_ILT_post_vs_pre": {"n_deg": 1764, "up": 1122, "down": 642, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 3817}, "fat_SC_post_vs_pre": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 0}, "muscle_change_ILT_vs_SC/ILT_vs_SC_change": {"n_deg": 95, "up": 72, "down": 23, "rule": "padj < 0.05 and |log2FoldChange| > 0.3", "audit_n": 95}}, "paper_counts": {"muscle_ILT_post_vs_pre": 1540, "muscle_SC_post_vs_pre": 65}, "comparison": {"muscle_ILT_post_vs_pre": {"ours": 1382, "paper": 1540}, "muscle_SC_post_vs_pre": {"ours": 0, "paper": 65}}, "paper_gene_check": {"muscle_ILT_post_vs_pre": {"NAMPT": {"AveExpr": 5.893, "log2FoldChange": 0.5065, "padj": 0.00358, "pvalue": 3.78e-05}, "SIRT3": {" ... [1858 more characters]

reasoning: Paper-defined contrasts reproduced on a declared deviation route (limma on log2 CPM).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 62 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "input matrix",
    "paper": "edgeR on featureCounts counts",
    "data": "only moderated log2 CPM deposited",
    "disposition": "declared_deviation: limma on log2 CPM"
  },
  {
    "item": "low-expression filtering",
    "paper": "not described",
    "data": "34,259 genes incl. many unexpressed",
    "disposition": "declared_deviation: log2CPM >= 0 in >= n_smaller_group samples per execution"
  },
  {
    "item": "duplicated symbols",
    "paper": "not described",
    "data": "121 repeated gene symbols",
    "disposition": "executable_without_change: executor keeps highest-mean row"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID36084645 / GSE205891

Decision maker: Claude Opus 5.5 (Claude Code session), case-spec route (`python -m tools.case_runner execute case_spec.json`). Preflight skipped as instructed. The run completed in one pass. `validate_decision_contract.py` returned VALID (16 records).

## What ran

- **Paper**: an 8-month randomized trial in people with obesity and T2D. The intensive lifestyle therapy arm (ILT: energy restriction plus supervised exercise 4 x 60 min/week) was compared with standard care (SC). The paper reports muscle RNA-seq DEGs after vs before within each arm (S2.6.p1, FIG3A). Its threshold is log2|FC| > 0.3 and FDR < 0.05 using edgeR (S4.4.p1). For adipose tissue it reports selected genes only (S2.7.p1, FIG4).
- **Data**: GSE205891 has 62 samples: 28 muscle (SC 6 + ILT 8 subjects x pre/post) and 34 subcutaneous fat (SC 7 + ILT 10). These match FIG3 and FIG4. The only deposited matrix is `GSE205891_LID_all.gene_moderated_log2cpm.csv` (34,259 genes, log2 CPM; 2^x sums to about 1e6 per column). There are no raw counts.
- **Alignment**: exact match on `title` (62/62). `subject`, `tissue` and `visit` come from the title. `time` comes from the GEO sample type, and the A/B suffix agrees with it in every row. Sex inferred from X/Y genes gives one male (subject 026, ILT) in both tissues and at both timepoints. This matches the paper's "1 man in ILT".
- **Design**: tissue and arm are strata. `time` (post vs pre) is tested with subject blocking. Suitability verdict: analyzable.
- **Method**: limma (moderated t, eBayes), `~ C(subject) + Treatment`, on the deposited log2 CPM. Each execution has its own low-expression filter.

| Execution | Role | Pairs | Genes tested | DEGs (paper rule) | up / down | padj<0.05 only | Paper |
|---|---|---|---|---|---|---|---|
| muscle_ILT_post_vs_pre | primary | 8 | 13,285 | **1,382** | 906 / 476 | 1,997 | **1,540** |
| muscle_SC_post_vs_pre | secondary | 6 | 13,215 | **0** (min padj 0.24) | 0 / 0 | 0 | **65** |
| fat_ILT_post_vs_pre | secondary | 10 | 14,906 | 1,764 | 1,122 / 642 | 3,817 | not reported |
| fat_SC_post_vs_pre | secondary | 7 | 14,893 | 0 | 0 / 0 | 0 | not reported |
| muscle_change_ILT_vs_SC (paired change, ILT minus SC) | exploratory | 8 vs 6 | ~13.3k | 95 | 72 / 23 | 95 | not reported |

Threshold applied: padj < 0.05 and |log2FC| > 0.3, both strict. Source: `paper_on_deviation_route` (S4.4.p1).

**Named genes.**
- **ILT muscle**: all 10 genes the paper names are up and significant with the same ... [3136 more characters]
