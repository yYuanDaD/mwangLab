# Review packet B (the analysis' decisions): GSE263838

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.3.age of_donor", "n_values": 9, "max_repeat": 10, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **other_rule_matches_paper**: {"table": "joint_blocked/day_D9_vs_D3_cond-NS", "paper": 2962, "applied": 1061, "applied_rule": "padj < 0.05 and |log2FoldChange| > 1", "closest_rule": "pvalue<0.05 & |lfc|>0.584963", "closest_n": 2686, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **other_rule_matches_paper**: {"table": "joint_blocked/day_D9_vs_D3_cond-SR", "paper": 2219, "applied": 777, "applied_rule": "padj < 0.05 and |log2FoldChange| > 1", "closest_rule": "pvalue<0.05 & |lfc|>0.584963", "closest_n": 2237, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint_blocked/day_D9_vs_D3_cond-NS | 2962 | 1061 | padj < 0.05 and |log2FoldChange| > 1 | 4003 | 2259 | 1061 | 5168 | 5775 | 2686 | 1183 | 3736 | 0.046 | 0.372 |
| joint_blocked/day_D9_vs_D3_cond-SR | 2219 | 777 | padj < 0.05 and |log2FoldChange| > 1 | 2943 | 1659 | 777 | 4019 | 5026 | 2237 | 945 | 2990 | 0.052 | 0.323 |
| joint_blocked/cond_SR_vs_NS_day-D3 | 1 | 1 | padj < 0.05 and |log2FoldChange| > 1 | 1 | 1 | 1 | 2 | 876 | 360 | 151 | 214 | 0.094 | 0.056 |
| joint_blocked/cond_SR_vs_NS_day-D9 | 0 | 0 | padj < 0.05 and |log2FoldChange| > 1 | 0 | 0 | 0 | 0 | 1213 | 379 | 133 | 285 | 0.082 | 0.078 |

## Samples per design level

### `cond`
- **NS** (19): GSM8199909 / ANLI5; GSM8199910 / ANLI7; GSM8199913 / ELLI5; GSM8199914 / ELLI7; GSM8199917 / GEDA5; GSM8199918 / GEDA7; GSM8199921 / GEKN5; GSM8199922 / GEKN7; GSM8199925 / HABA5; GSM8199926 / HABA7; GSM8199929 / JEHA5; GSM8199930 / JEHA7; GSM8199933 / KISZ5; GSM8199934 / KISZ7; GSM8199937 / NACR5; GSM8199938 / NACR7; GSM8199940 / SASY7; GSM8199943 / TATU5; GSM8199944 / TATU7
- **SR** (19): GSM8199907 / ANLI1; GSM8199908 / ANLI3; GSM8199911 / ELLI1; GSM8199912 / ELLI3; GSM8199915 / GEDA1; GSM8199916 / GEDA3; GSM8199919 / GEKN1; GSM8199920 / GEKN3; GSM8199923 / HABA1; GSM8199924 / HABA3; GSM8199927 / JEHA1; GSM8199928 / JEHA3; GSM8199931 / KISZ1; GSM8199932 / KISZ3; GSM8199935 / NACR1; GSM8199936 / NACR3; GSM8199939 / SASY1; GSM8199941 / TATU1; GSM8199942 / TATU3

### `day`
- **D3** (19): GSM8199907 / ANLI1; GSM8199909 / ANLI5; GSM8199911 / ELLI1; GSM8199913 / ELLI5; GSM8199915 / GEDA1; GSM8199917 / GEDA5; GSM8199919 / GEKN1; GSM8199921 / GEKN5; GSM8199923 / HABA1; GSM8199925 / HABA5; GSM8199927 / JEHA1; GSM8199929 / JEHA5; GSM8199931 / KISZ1; GSM8199933 / KISZ5; GSM8199935 / NACR1; GSM8199937 / NACR5; GSM8199939 / SASY1; GSM8199941 / TATU1; GSM8199943 / TATU5
- **D9** (19): GSM8199908 / ANLI3; GSM8199910 / ANLI7; GSM8199912 / ELLI3; GSM8199914 / ELLI7; GSM8199916 / GEDA3; GSM8199918 / GEDA7; GSM8199920 / GEKN3; GSM8199922 / GEKN7; GSM8199924 / HABA3; GSM8199926 / HABA7; GSM8199928 / JEHA3; GSM8199930 / JEHA7; GSM8199932 / KISZ3; GSM8199934 / KISZ7; GSM8199936 / NACR3; GSM8199938 / NACR7; GSM8199940 / SASY7; GSM8199942 / TATU3; GSM8199944 / TATU7

### `subject`
- **ANLI** (4): GSM8199907 / ANLI1; GSM8199908 / ANLI3; GSM8199909 / ANLI5; GSM8199910 / ANLI7
- **ELLI** (4): GSM8199911 / ELLI1; GSM8199912 / ELLI3; GSM8199913 / ELLI5; GSM8199914 / ELLI7
- **GEDA** (4): GSM8199915 / GEDA1; GSM8199916 / GEDA3; GSM8199917 / GEDA5; GSM8199918 / GEDA7
- **GEKN** (4): GSM8199919 / GEKN1; GSM8199920 / GEKN3; GSM8199921 / GEKN5; GSM8199922 / GEKN7
- **HABA** (4): GSM8199923 / HABA1; GSM8199924 / HABA3; GSM8199925 / HABA5; GSM8199926 / HABA7
- **JEHA** (4): GSM8199927 / JEHA1; GSM8199928 / JEHA3; GSM8199929 / JEHA5; GSM8199930 / JEHA7
- **KISZ** (4): GSM8199931 / KISZ1; GSM8199932 / KISZ3; GSM8199933 / KISZ5; GSM8199934 / KISZ7
- **NACR** (4): GSM8199935 / NACR1; GSM8199936 / NACR3; GSM8199937 / NACR5; GSM8199938 / NACR7
- **SASY** (2): GSM8199939 / SASY1; GSM8199940 / SASY7
- **TATU** (4): GSM8199941 / TATU1; GSM8199942 / TATU3; GSM8199943 / TATU5; GSM8199944 / TATU7

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE263838"], "assay": "bulk total RNA-seq (Ribo-Zero), vastus lateralis, Kallisto GRCh38 (S2.8.p1)", "design": "randomised cross-over: 10 resistance-trained females, normal sleep (NS) vs sleep restriction (SR), resistance exercise sessions on days 3,5,7,9; RNA-seq on PRE-exercise biopsies of day 3 and day 9 only (S2.2.p2, S2.7.p1, S3.2.p2)", "factors": {"cond": ["NS", "SR"], "day": ["D3", "D9"]}, "repeated_measure_unit": "participant (each woman sampled in both conditions and both days)", "sample_inclusion": "all RNA sequencing samples (S2.8.p1); 10 participants x 2 conditions x 2 days = 40 planned, 38 deposited", "primary_estimand": "exercise-training effect: pre-exercise day 9 (48 h after the 3rd of three REx sessions on days 3,5,7) vs pre-exercise day 3 (before any session in that condition), within NS and within SR (S3.2.p7); secondary: SR vs NS at day 3 and at day 9 (S3.2.p2)", "planned_contrasts": ["NS day 9 vs NS day 3 (exercise training under normal sleep; paper: 2962 DEGs, up 128 / down 2834, S3.2.p7)", "SR day 9 vs SR day 3 (exercise training under sleep restriction; paper: 2219 DEGs, up 102 / down 2117, S3.2.p7)", "SR vs NS at day 3 (sleep restriction, no exercise; paper: 1 DEG, GGNBP2, S3.2.p2)", "SR vs NS at day 9 (sleep restriction with equal training; paper: 0 DEGs, S3.2.p2)"], "normalization_filter": "keep genes with at least 10 reads on average -> 15,543 transcripts (S2.8.p1)", "paper_method": "DESeq2 (\"DESeq R package v1.40.2\"; design form ... [414 more characters]

reasoning: Methods S2.8.p1 states DESeq2 with padj < 0.05 and log2FC > 1 / < -1 on the mean>=10-reads filtered set. Results S3.2.p7 give exercise DEG counts labelled FDR < 0.05; S3.3.p2 gives the same counts (2834/2117 down, 129/102 up). The exercise estimand is a training/time contrast (day 9 pre vs day 3 pre) because only pre-exercise biopsies were sequenced (S2.7.p1).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\prep\\GSE263838_counts_mean10.csv.gz", "owned": true, "checks": ["GEO treatment_protocol reproduces the paper's abstract design (10 females, 9 nights SR 5 h vs NS, REx days 3,5,7,9, biopsies days 3 and 9)", "contact Danielle Hiam (Deakin IPAN) is an author", "38 vastus lateralis female samples, treatment SLEEP/CON x day 3/9", "filtered matrix size equals the paper's 15,543 transcripts"], "accession": "GSE263838", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE263838\\GSE263838_metadata.csv"}

reasoning: GEO series metadata (treatment_protocol_ch1, contact) matches the paper ABS.p1 / S2.2 exactly; the gene count after the paper's filter reproduces S2.8.p1's 15,543.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 38, "n_metadata": 38, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\aligned\\aligned_metadata.csv", "columns": {"subject": {"source": "title", "regex": "^([A-Z]{4})[1357]$"}, "cond": {"source": "characteristics_ch1.4.treatment", "regex": "^(SLEEP|CON)$", "recode": {"SLEEP": "SR", "CON": "NS"}}, "day": {"source": "characteristics_ch1.5.day of_collection", "regex": "^([39])$", "recode": {"3": "D3", "9": "D9"}}, "grp": {"combine": ["cond", "day"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\aligned\\design_metadata.csv", "sha256": "9911b6cd7a011f85808ff42795a8abfcf41c9339a90ef988beaa4eb8a0ca49d5", "levels": {"subject": {"ANLI": 4, "ELLI": 4, "GEDA": 4, "GEKN": 4, "HABA": 4, "JEHA": 4, "KISZ": 4, "NACR": 4, "TATU": 4, "SASY": 2}, "cond": {"SR": 19, "NS": 19}, "day": {"D3": 19, "D9": 19}, "grp": {"SR_D3": 10, "NS_D9": 10, "SR_D9": 9, "NS_D3": 9}}}}

reasoning: Matrix columns equal the GEO title (38/38). Title = 4-letter participant code + digit; digit 1/3/5/7 corresponds exactly to SLEEP-d3/SLEEP-d9/CON-d3/CON-d9 in the characteristics columns, so the participant key is the 4-letter prefix (10 participants). Condition and day come from the characteristics columns, not from the digit. Ages differ by one year between conditions for GEKN and KISZ, consistent with a cross-over spanning months.

### matrix (valid, not_started)

final: {"source": "GSE263838_GeneCounts_RAW_DATA.csv.gz filtered by prep/filter_mean10.py (mean count >= 10, 15,543 genes)", "paper_input": "Kallisto counts into DESeq2 (S2.8.p1)", "matrix_type": "estimated counts (Kallisto gene-level counts, deposited as integers)", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\aligned\\aligned_matrix.csv", "sha256": "f1f6c16b95b79bbaeb6c10a481bcd52445631fbd6d3780272aef3944807955ee", "n_features": 15543, "n_samples": 38, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 7313530.0, "median": 187.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer fraction 1.0, max 7.3e6, library sizes 23-29 M; data_processing says Kallisto transcript counts and 'aligned raw gene counts'. Kallisto estimates are non-integer, so the submitter already rounded/summed them to integer gene counts; this is the input the paper gave DESeq2. The 3col.tsv is the long-format copy of the same counts.

### design (valid, not_started)

final: {"analysis_type": "2x2 factorial repeated measures (cell means), simple-effect contrasts", "formula": "~ subject + grp", "contrasts": [{"name": "day_D9_vs_D3_cond-NS", "control": "NS_D3", "treatment": "NS_D9", "role": "primary"}, {"name": "day_D9_vs_D3_cond-SR", "control": "SR_D3", "treatment": "SR_D9", "role": "primary"}, {"name": "cond_SR_vs_NS_day-D3", "control": "NS_D3", "treatment": "SR_D3", "role": "secondary"}, {"name": "cond_SR_vs_NS_day-D9", "control": "NS_D9", "treatment": "SR_D9", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: Paper compares 'NS and SR conditions by day, as well as the same condition by day' (S2.8.p1) using all samples: four simple effects from one model. The exercise estimand is day 9 vs day 3 within each sleep condition; it combines three REx sessions with six more days in the condition and time-of-study, which the design cannot separate (no non-exercise arm), so it is labelled a training/time effect as the paper does. The cond x day interaction (does sleep restriction change the training response) is the paper's verbal claim (S3.3.p2) but it was argued from Euler overlaps, not tested; it runs as exploratory.

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking factor (participant; cross-over, 4 biopsies per woman)"}, {"name": "age", "disposition": "not used: constant within participant, absorbed by subject"}], "design_check": {"formula_equivalent": "~ C(cond) + C(day) + C(subject)", "n_samples": 38, "n_columns": 12, "columns": ["Intercept", "cond_SR", "day_D9", "subject_ELLI", "subject_GEDA", "subject_GEKN", "subject_HABA", "subject_JEHA", "subject_KISZ", "subject_NACR", "subject_SASY", "subject_TATU"], "rank": 12, "full_rank": true, "residual_df": 26, "levels": {"cond": {"SR": 19, "NS": 19}, "day": {"D3": 19, "D9": 19}, "subject": {"ANLI": 4, "ELLI": 4, "GEDA": 4, "GEKN": 4, "HABA": 4, "JEHA": 4, "KISZ": 4, "NACR": 4, "TATU": 4, "SASY": 2}}, "cells": [{"cell": ["NS", "D3", "ANLI"], "n": 1}, {"cell": ["NS", "D3", "ELLI"], "n": 1}, {"cell": ["NS", "D3", "GEDA"], "n": 1}, {"cell": ["NS", "D3", "GEKN"], "n": 1}, {"cell": ["NS", "D3", "HABA"], "n": 1}, {"cell": ["NS", "D3", "JEHA"], "n": 1}, {"cell": ["NS", "D3", "KISZ"], "n": 1}, {"cell": ["NS", "D3", "NACR"], "n": 1}, {"cell": ["NS", "D3", "TATU"], "n": 1}, {"cell": ["NS", "D9", "ANLI"], "n": 1}, {"cell": ["NS", "D9", "ELLI"], "n": 1}, {"cell": ["NS", "D9", "GEDA"], "n": 1}, {"cell": ["NS", "D9", "GEKN"], "n": 1}, {"cell": ["NS", "D9", "HABA"], "n": 1}, {"cell": ["NS", "D9", "JEHA"], "n": 1}, {"cell": ["NS", "D9", "KISZ"], "n": 1}, {"cell": ["NS", "D9", "NACR"], "n": 1},  ... [1210 more characters]

reasoning: Each participant contributes up to four samples (both conditions, both days): samples are not independent, so participant is a blocking term. The paper does not state its DESeq2 formula; an unblocked ~ grp fit runs as a sensitivity analysis to bracket the paper's counts. No sequencing batch is recorded. Estrogen/progesterone were tested and dropped by the paper (S2.12.p1) and are not deposited.

### method (valid, not_started)

final: {"matrix_type": "estimated counts (Kallisto gene-level counts, deposited as integers)", "method": "DESeq2 (pydeseq2 Wald), joint model on all 38 samples", "formula": "~ subject + grp", "rounding_documented": true, "paper_route": {"method": "DESeq2 (R, v1.40.2), formula not stated", "status": "reproduced_with_assumption"}, "deviations": ["participant blocking added (paper formula unstated); unblocked ~ grp run as sensitivity", "pydeseq2 instead of R DESeq2", "counts were already integers as deposited; no further rounding applied (round on integers is the identity)"]}

reasoning: Integer (rounded Kallisto) gene counts support DESeq2, the paper's method. The paper's low-count filter (mean >= 10 reads) is applied before fitting by prep/filter_mean10.py and reproduces its 15,543 genes exactly.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null, "inclusive": false}, "deviation_note": "Methods (S2.8.p1) state padj < 0.05 and |log2FC| > 1; Results (S3.2.p7, S3.3.p2) label the exercise counts 'FDR < 0.05' only. The FDR-only rule is reported as the audit count so both readings can be compared."}

reasoning: S2.8.p1: 'adjusted p-value of < 0.05 and Log2 fold change > 1 and <-1'; figure legends FIG1/FIG3 use the same two cutoffs.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint_blocked", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 38, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\aligned\\aligned_matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_blocked\\DEG_results_cond_SR_vs_NS_day-D3.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_blocked\\DEG_results_cond_SR_vs_NS_day-D9.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_blocked\\DEG_results_day_D9_vs_D3_cond-NS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_blocked\\DEG_results_day_D9_vs_D3_cond-SR.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_blocked\\DEG_results_cond_day_SR_D9_vs_NS_D3.csv"], "counts": {"joint_blocked/cond_SR_vs_NS_day-D3": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15543, "n_significant": 1, "n_up": 0, "n_down": 1, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15543, "n_significant": 1, "n_up": 0, "n_down": 1, "deg_sanity": "ok"}}, "joint_blocked/cond_SR_vs_NS_day-D9": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15543, "n_significant": 0,  ... [1100 more characters]

reasoning: One DESeq2 model ~ subject + cell on all 38 samples; extracts the four planned simple effects plus the exploratory cond x day interaction.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint_unblocked", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 38, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_unblocked\\DEG_results_day_D9_vs_D3_cond-NS.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_unblocked\\DEG_results_day_D9_vs_D3_cond-SR.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_unblocked\\DEG_results_cond_SR_vs_NS_day-D3.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\joint_unblocked\\DEG_results_cond_SR_vs_NS_day-D9.csv"], "counts": {"joint_unblocked/day_D9_vs_D3_cond-NS": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15540, "n_significant": 1136, "n_up": 1006, "n_down": 130, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15540, "n_significant": 2965, "n_up": 1964, "n_down": 1001, "deg_sanity": "ok"}}, "joint_unblocked/day_D9_vs_D3_cond-SR": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 15540, "n_significant": 807, "n_up": 705, "n_down": 102, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15540, "n_significant": 2224, ... [658 more characters]

reasoning: Unblocked ~ cell, the likely paper formula (no pairing mentioned), to bracket the paper's DEG counts.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "joint_blocked/day_D9_vs_D3_cond-NS", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "log2FoldChange", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\enrichment_joint_blocked_day_D9_vs_D3_cond-NS\\gsea\\DEG_results_day_D9_vs_D3_cond-NS_GSEA_Hallmark.csv"], "summary": "GSEA complete on 14333 Human genes ranked by 'log2FoldChange'. 50 Hallmark sets tested, 41 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.44 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.30 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=2.22 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INFLAMMATORY_RESPONSE | NES=2.09 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=2.07 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=2.01 | NOM p=0.00e+00 | FDR q=1.55e-04 - HALLMARK_ANGIOGENESIS | NES=2.01 | NOM p=1.30e-03 | FDR q=1.32e-04 - HALLMARK_MITOTIC_SPINDLE | NES=1.96 | NOM p=0.00e+00 | FDR q=1.16e-04 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.94 | NOM p=0.00e+00 | FDR q=1.03e-04 - HALLMARK_COMPLEMENT | NES=1.88 | NOM p=0.00e+00 | FDR q=9.27e-05 ### Top 7 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.57 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLM ... [444 more characters]

reasoning: Paper ran fgsea ranked by log2FC on each contrast (S2.9.p2); our tool uses MSigDB Hallmark, not Reactome. Paper: oxidative metabolism up with training (S3.2.p8).

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "joint_blocked/day_D9_vs_D3_cond-SR", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "log2FoldChange", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38766755\\GSE263838\\results\\enrichment_joint_blocked_day_D9_vs_D3_cond-SR\\gsea\\DEG_results_day_D9_vs_D3_cond-SR_GSEA_Hallmark.csv"], "summary": "GSEA complete on 14333 Human genes ranked by 'log2FoldChange'. 50 Hallmark sets tested, 26 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.36 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_G2M_CHECKPOINT | NES=2.16 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_E2F_TARGETS | NES=2.12 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.96 | NOM p=0.00e+00 | FDR q=9.57e-04 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.90 | NOM p=0.00e+00 | FDR q=7.98e-04 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.89 | NOM p=0.00e+00 | FDR q=6.84e-04 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.86 | NOM p=0.00e+00 | FDR q=8.38e-04 - HALLMARK_COAGULATION | NES=1.75 | NOM p=0.00e+00 | FDR q=2.77e-03 - HALLMARK_COMPLEMENT | NES=1.72 | NOM p=0.00e+00 | FDR q=3.35e-03 ### Top 5 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.58 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMAR ... [451 more characters]

reasoning: As above for the SR training contrast.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Exercise contrast = day 9 pre-exercise vs day 3 pre-exercise: training effect confounded with time in the condition (no non-exercise arm); not an acute exercise response.", "Paper DEG counts may use FDR only (Results) or FDR + |log2FC| > 1 (Methods); compare against both our applied and audit counts.", "Participant blocking is our assumption; the paper's formula is unstated.", "SASY contributes only SR day 3 and NS day 9 (SASY3 and SASY5 not deposited).", "Paper totals are reproduced by the UNBLOCKED fit with FDR < 0.05 only (2965 vs 2962 NS; 2224 vs 2219 SR), so the paper's counts used FDR only (Results wording), not its Methods |log2FC| > 1 rule, and no participant blocking.", "Paper's up/down split (128/2834 NS, 102/2117 SR) is not a sign split: its 'up' equals our padj < 0.05 and log2FC(D9/D3) < -1 (130 NS, 102 SR) and its 'down' equals the remaining FDR genes (2835, 2122). Our FDR-only sign split for D9 vs D3 is 1964 up / 1001 down (NS) and 1346 / 878 (SR).", "Direction contradicts the paper's text: paper says oxidative metabolism is UP with training and cell cycle DOWN; our D9 vs D3 GSEA (Hallmark) has OXIDATIVE_PHOSPHORYLATION NES -2.57 (NS) / -2.58 (SR) and E2F/G2M NES +2.1 to +2.3. Paper's GGNBP2 is 'upregulated' by SR at day 3; ours log2FC(SR/NS) = -2.27. Both are consistent with the paper's contrasts being written reference-over-test (NS3_vs_NS9 = day 3 / day 9; NS3_vs_SR3 = NS / SR), i.e. the paper's stated directions are si ... [2102 more characters]

reasoning: Counts from S3.2.p7 (128 up + 2834 down; 102 up + 2117 down) and S3.2.p2 (1 and 0).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample count",
    "paper": "10 participants x 2 conditions x 2 days (40 pre-exercise biopsies)",
    "data": "38 samples; SASY lacks SR day 9 and NS day 3",
    "disposition": "executable_without_change"
  },
  {
    "item": "DEG threshold",
    "paper": "Methods: padj < 0.05 and |log2FC| > 1; Results: counts labelled FDR < 0.05",
    "data": "n/a",
    "disposition": "executable_without_change"
  },
  {
    "item": "DESeq2 design formula",
    "paper": "not stated",
    "data": "participant key derivable from title",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID38766755 / GSE263838

Status: finished (case route `paper_aligned`, validator 13 records, 0 errors).

## What ran
- Case-spec route (`python -m tools.case_runner execute case_spec.json`), preflight skipped as instructed.
- Matrix: `GSE263838_GeneCounts_RAW_DATA.csv.gz` (Kallisto gene counts deposited as integers, 40,514 genes x 38 samples), filtered with `prep/filter_mean10.py` to genes with mean count >= 10. This keeps **15,543 genes, the exact number in the paper** (S2.8.p1).
- Alignment: exact match on GEO `title` (38/38). The participant key is the 4-letter title prefix (10 women; SASY has only SR-D3 and NS-D9). `cond` (NS/SR) and `day` (D3/D9) come from the characteristics columns. `grp` = cond_day.
- Design: 2x2 cross-over with repeated measures. All pre-exercise biopsies go into one model. The exercise estimand is pre-exercise day 9 vs pre-exercise day 3 within each sleep condition. This is a training/time effect of three REx sessions measured 48 h after the last one, not an acute response.
- Primary: joint DESeq2 (pydeseq2) `~ subject + grp`, with 4 planned simple effects plus the exploratory cond x day interaction.
- Sensitivity: joint DESeq2 `~ grp` (unblocked). The paper does not state its formula.
- GSEA (Hallmark, ranked by log2FC as in the paper) on both exercise contrasts of the blocked fit.

## DEG counts vs paper
Paper threshold (Methods S2.8.p1) = padj < 0.05 and |log2FC| > 1; audit = padj < 0.05 only.

| Contrast | Paper | Blocked, paper rule | Blocked, FDR only | Unblocked, paper rule | Unblocked, FDR only |
|---|---|---|---|---|---|
| NS D9 vs D3 (exercise) | 2962 (128 "up" / 2834 "down") | 1061 | 4003 | 1136 | **2965** |
| SR D9 vs D3 (exercise) | 2219 (102 / 2117) | 777 | 2943 | 807 | **2224** |
| SR vs NS, day 3 | 1 (GGNBP2) | 1 (GGNBP2) | 1 | 1 | 1 |
| SR vs NS, day 9 | 0 | 0 | 0 | 0 | 0 |
| cond x day interaction (exploratory) | not tested | 0 | 0 | - | - |

- The paper's totals are reproduced almost exactly by the **unblocked, FDR-only** fit. The paper therefore counted at FDR < 0.05 only, as its Results say, not with its Methods |log2FC| > 1 rule, and it did not block on participant. Our primary (blocked, paper rule) gives fewer DEGs.
- The paper's up/down split is not a sign split. Its "up" (128 / 102) matches our padj < 0.05 with log2FC(D9/D3) < -1 (130 / 102). Its "down" matches the remaining FDR genes (2835 / 2122). Our real FDR-only sign split for D9 vs D3 is 1964 up / 1001 down (NS) and 1346 / 878 (SR).
- * ... [1556 more characters]
