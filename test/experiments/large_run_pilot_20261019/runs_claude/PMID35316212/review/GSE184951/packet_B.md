# Review packet B (the analysis' decisions): GSE184951

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_POST_vs_PRE | 19 | 55 | pvalue < 0.005 and |log2FoldChange| > 1.5 | 1066 | 355 | 105 | 1811 | 4036 | 1182 | 479 | 1853 | 0.301 | 0.093 |
| grp_PRE_vs_CON | 640 | 1471 | pvalue < 0.005 and |log2FoldChange| > 1.5 | 9745 | 6273 | 3309 | 11416 | 11834 | 7337 | 3995 | 8820 | 0.077 | 0.285 |

## Samples per design level

### `grp`
- **CON** (10): GSM5602348 / Control matched for sample 1; GSM5602349 / Control matched for sample 12; GSM5602350 / Control matched for sample 13; GSM5602351 / Control matched for sample 2; GSM5602352 / Control matched for sample 3; GSM5602353 / Control matched for sample 4; GSM5602354 / Control matched for sample 6; GSM5602355 / Control matched for sample 7; GSM5602356 / Control matched for sample 8; GSM5602357 / Control matched for sample 9
- **POST** (11): GSM5602358 / Sample 1 post treatment; GSM5602359 / Sample 12 post treatment; GSM5602360 / Sample 13 post treatment; GSM5602361 / Sample 2 post treatment; GSM5602362 / Sample 3 post treatment; GSM5602363 / Sample 4 post treatment; GSM5602364 / Sample 5 post treatment; GSM5602365 / Sample 6 post treatment; GSM5602366 / Sample 7 post treatment; GSM5602367 / Sample 8 post treatment; GSM5602368 / Sample 9 post treatment
- **PRE** (11): GSM5602369 / Sample 1 pre treatment; GSM5602370 / Sample 12 pre treatment; GSM5602371 / Sample 13 pre treatment; GSM5602372 / Sample 2 pre treatment; GSM5602373 / Sample 3 pre treatment; GSM5602374 / Sample 4 pre treatment; GSM5602375 / Sample 5 pre treatment; GSM5602376 / Sample 6 pre treatment; GSM5602377 / Sample 7 pre treatment; GSM5602378 / Sample 8 pre treatment; GSM5602379 / Sample 9 pre treatment

### `subject`
- **Control_1** (1): GSM5602348 / Control matched for sample 1
- **Control_12** (1): GSM5602349 / Control matched for sample 12
- **Control_13** (1): GSM5602350 / Control matched for sample 13
- **Control_2** (1): GSM5602351 / Control matched for sample 2
- **Control_3** (1): GSM5602352 / Control matched for sample 3
- **Control_4** (1): GSM5602353 / Control matched for sample 4
- **Control_6** (1): GSM5602354 / Control matched for sample 6
- **Control_7** (1): GSM5602355 / Control matched for sample 7
- **Control_8** (1): GSM5602356 / Control matched for sample 8
- **Control_9** (1): GSM5602357 / Control matched for sample 9
- **Sample_1** (2): GSM5602358 / Sample 1 post treatment; GSM5602369 / Sample 1 pre treatment
- **Sample_12** (2): GSM5602359 / Sample 12 post treatment; GSM5602370 / Sample 12 pre treatment
- **Sample_13** (2): GSM5602360 / Sample 13 post treatment; GSM5602371 / Sample 13 pre treatment
- **Sample_2** (2): GSM5602361 / Sample 2 post treatment; GSM5602372 / Sample 2 pre treatment
- **Sample_3** (2): GSM5602362 / Sample 3 post treatment; GSM5602373 / Sample 3 pre treatment
- **Sample_4** (2): GSM5602363 / Sample 4 post treatment; GSM5602374 / Sample 4 pre treatment
- **Sample_5** (2): GSM5602364 / Sample 5 post treatment; GSM5602375 / Sample 5 pre treatment
- **Sample_6** (2): GSM5602365 / Sample 6 post treatment; GSM5602376 / Sample 6 pre treatment
- **Sample_7** (2): GSM5602366 / Sample 7 post treatment; GSM5602377 / Sample 7 pre treatment
- **Sample_8** (2): GSM5602367 / Sample 8 post treatment; GSM5602378 / Sample 8 pre treatment
- **Sample_9** (2): GSM5602368 / Sample 9 post treatment; GSM5602379 / Sample 9 pre treatment

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE184951"], "assay": "bulk total RNA-seq (TruSeq Stranded Total RNA), human vastus lateralis biopsies, HISAT2/GRCh37 + HTSeq gene counts", "sample_inclusion": "11 DM1 patients who completed 12 wk cycling (P10, P11 dropped out; S4.1.p1) biopsied pre and post; healthy inactive CON biopsied once at baseline (n = 10 sequenced; Fig 4 legend n = 10-11)", "factors": {"grp": ["CON", "DM1-PRE", "DM1-POST"]}, "primary_estimand": "Within-patient effect of 12 weeks of aerobic cycle training on vastus lateralis gene expression in DM1 patients (DM1-POST vs DM1-PRE, paired by patient) (S2.9.p1, Fig 4C)", "planned_contrasts": ["DM1-POST vs DM1-PRE, paired (S2.9.p1, Fig 4C; paper: 18 up, 1 down)", "DM1-PRE vs CON (S2.8.p1, Fig 4B; paper: 435 up, 205 down) - disease contrast, not an exercise effect"], "repeated_measure_unit": "patient (pre/post biopsies from the same DM1 patient)", "normalization": "DESeq2 library size normalization (S4.16.p1)", "paper_method": "DESeq2 accounting for group and paired sample design (S4.16.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.005, "effect_metric": "log2FoldChange", "effect_cutoff": 1.5, "inclusive": false, "source_locator": "FIG4 legend"}, "paper_results": {"POST_vs_PRE": "18 up, 1 down; ECM remodelling, angiogenesis, inflammation GO terms up", "PRE_vs_CON": "435 up, 205 down; snoRNAs/snRNAs up, splicing/OXPHOS/translation down"}}

reasoning: S2.9.p1 and Fig 4C define the exercise estimand as DM1-PRE vs DM1-POST with 1 down/18 up genes; S4.16.p1 states DESeq2 with group and paired design; Fig 4 legend gives the significance rule |log2(FC)| > 1.5 and P < 0.005 (a raw P, no FDR stated). S2.8.p1 adds the DM1-PRE vs CON disease contrast. Supplemental Table 3 (DEG lists) is not available here.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S4.22.p1 names GSE184951", "GEO series contact Tarnopolsky (senior author), McMaster", "32 GSMs: 10 CON + 11 DM1 pre + 11 DM1 post, matches 11 patients and n=10 CON in Fig 4", "data_processing matches S4.16.p1 (HISAT2 GRCh37, HTSeq, DESeq2)"], "accession": "GSE184951", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE184951\\GSE184951_metadata.csv"}

reasoning: Paper data availability (S4.22.p1) names GSE184951; the sample set and processing match the methods. The per-sample HTSeq geneCounts files in GSE184951_RAW.tar are the gene count matrix; the *.SE.MATS.JC.txt.gz files are rMATS splicing outputs, not gene expression.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 32, "n_metadata": 32, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "(Control|pre|post)", "recode": {"Control": "CON", "pre": "PRE", "post": "POST"}}, "subject": {"source": "title", "regex": "^(Control|Sample)\\D*(\\d+)"}, "sex": {"source": "title", "regex": "^(Control|Sample)\\D*(\\d+)", "recode": {"Sample_1": "M", "Sample_12": "M", "Sample_13": "F", "Sample_2": "F", "Sample_3": "M", "Sample_4": "M", "Sample_5": "F", "Sample_6": "F", "Sample_7": "M", "Sample_8": "F", "Sample_9": "F", "Control_1": "M", "Control_12": "M", "Control_13": "F", "Control_2": "F", "Control_3": "M", "Control_4": "M", "Control_6": "F", "Control_7": "M", "Control_8": "F", "Control_9": "F"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\aligned\\design_metadata.csv", "sha256": "6c6472b7f0ef4c4c792b8a3f10f3c855e6b063f4d3d63d0c17c6b1c88c510cfc", "levels": {"grp": {"POST": 11, "PRE": 11, "CON": 10}, "subject": {"Sample_1": 2, "Sample_12": 2, "Sample_13": 2, "Sample_2": 2, "Sample_3": 2, "Sample_4": 2, "Sample_5": 2, "Sample_6": 2, "Sample_7": 2, "Sample_8": 2, "Sample_9": 2, "Control_1": 1, "Control_12": 1, "Control_13": 1, "Control_2": 1, "Control_3": 1, "Con ... [105 more characters]

reasoning: Merged tar columns are GSM ids, matching the metadata index exactly. grp from title ('Control matched for sample N' / 'Sample N pre|post treatment'). subject keeps the Control/Sample prefix so that a control matched to patient N is NOT treated as the same person as patient N (they are different individuals, S4.1.p1). sex: metadata has no sex field; each subject is recoded to the sex inferred from Y-gene/XIST expression in the first run's suitability sex check (all high confidence; consistent within every pre/post pair and every control matches its patient's sex).

### matrix (valid, not_started)

final: {"source": "GSE184951_RAW.tar per-sample *.geneCounts.txt.gz merged", "paper_input": "HTSeq gene read counts into DESeq2 (S4.16.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\aligned\\aligned_matrix.csv", "sha256": "72f7f74a5b21682454fd32db86b28aa2101ff3e67adf8dd3954b8bebe4139a17", "n_features": 63677, "n_samples": 32, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 13467575.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (fraction 1.0), min 0, max 1.3e7, Ensembl gene IDs; files named geneCounts; data_processing: 'Gene read count abundance determined by HTSeq'. Matches the paper's DESeq2 input.

### design (valid, not_started)

final: {"analysis_type": "paired two-group (primary) + independent two-group (secondary disease contrast)", "design_column": "grp", "contrasts": [{"name": "grp_POST_vs_PRE", "control": "PRE", "treatment": "POST", "role": "primary"}, {"name": "grp_PRE_vs_CON", "control": "CON", "treatment": "PRE", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Exercise effect is the within-patient POST vs PRE change (S2.9.p1). DM1-PRE vs CON (S2.8.p1) is a disease association contrast reported in the paper; run as secondary and described as associational, not an exercise effect.

rejected alternatives: [{"value": "treatment column (12-weeks of cycle ergometry vs untreated)", "reason_rejected": "pools CON with DM1-PRE in 'untreated', mixing disease with exercise"}, {"value": "DM1-POST vs CON as an exercise effect", "reason_rejected": "between-subject, confounded by disease; paper does not test it transcriptomically"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "blocking term in the POST vs PRE model (paired design, S4.16.p1); not used in PRE vs CON where each subject has one sample"}], "design_check": {"formula_equivalent": "~ C(grp) + C(subject)", "n_samples": 32, "n_columns": 23, "columns": ["Intercept", "grp_POST", "grp_PRE", "subject_Control_12", "subject_Control_13", "subject_Control_2", "subject_Control_3", "subject_Control_4", "subject_Control_6", "subject_Control_7", "subject_Control_8", "subject_Control_9", "subject_Sample_1", "subject_Sample_12", "subject_Sample_13", "subject_Sample_2", "subject_Sample_3", "subject_Sample_4", "subject_Sample_5", "subject_Sample_6", "subject_Sample_7", "subject_Sample_8", "subject_Sample_9"], "rank": 22, "full_rank": false, "residual_df": 10, "levels": {"grp": {"POST": 11, "PRE": 11, "CON": 10}, "subject": {"Sample_1": 2, "Sample_12": 2, "Sample_13": 2, "Sample_2": 2, "Sample_3": 2, "Sample_4": 2, "Sample_5": 2, "Sample_6": 2, "Sample_7": 2, "Sample_8": 2, "Sample_9": 2, "Control_1": 1, "Control_12": 1, "Control_13": 1, "Control_2": 1, "Control_3": 1, "Control_4": 1, "Control_6": 1, "Control_7": 1, "Control_8": 1, "Control_9": 1}}, "cells": [{"cell": ["CON", "Control_1"], "n": 1}, {"cell": ["CON", "Control_12"], "n": 1}, {"cell": ["CON", "Control_13"], "n": 1}, {"cell": ["CON", "Control_2"], "n": 1}, {"cell": ["CON", "Control_3"], "n": 1}, {"cell": ["CON", "Control_4"], "n": 1}, {"cell": ... [2174 more characters]

reasoning: Pre/post biopsies come from the same 11 patients, so patient is a blocking factor for the exercise contrast. S4.16.p1 notes extraction batches (P6 pilot pair; other PRE, POST and CON samples 'extracted in individual batches'); no batch column is deposited, so this cannot be modelled and is recorded as a caveat. No sex/age in metadata; controls were age- and sex-matched (S4.1.p1).

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ subject + grp (POST vs PRE, DM1 samples only); ~ grp (PRE vs CON)", "paper_route": {"method": "DESeq2 with group and paired design", "status": "reproduced"}, "deviations": ["pydeseq2 instead of R DESeq2; each contrast fitted on its own subset (paper did not specify whether one model held all 32 samples)"]}

reasoning: Raw HTSeq counts support DESeq2, the paper's method (S4.16.p1). Pairing via subject term. A single model with subject blocking cannot estimate CON vs PRE (each control is its own subject), so the two contrasts are fitted separately.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.005, "effect_metric": "log2FoldChange", "effect_cutoff": 1.5, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.005, "effect_metric": "log2FoldChange", "effect_cutoff": 1.5, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: Fig 4 legend: significant = |log2(FC)| > 1.5 and P < 0.005 (raw P, as written; no FDR). Audit: BH padj < 0.05, no FC cutoff.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_POST_vs_PRE", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 22, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_POST_vs_PRE\\input\\paired\\paired_matrix.csv", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_POST_vs_PRE\\DEG_results_POST_vs_PRE.csv"], "counts": {"grp_POST_vs_PRE": {"applied": {"rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "n_tested": 43385, "n_significant": 55, "n_up": 46, "n_down": 9, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17310, "n_significant": 1066, "n_up": 479, "n_down": 587, "deg_sanity": "ok"}}}}

reasoning: Paper's paired DESeq2 exercise contrast (S2.9.p1, S4.16.p1).

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_PRE_vs_CON", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 21, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_PRE_vs_CON\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_PRE_vs_CON\\DEG_results_PRE_vs_CON.csv"], "counts": {"grp_PRE_vs_CON": {"applied": {"rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "n_tested": 41529, "n_significant": 1471, "n_up": 1156, "n_down": 315, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 27036, "n_significant": 9745, "n_up": 5434, "n_down": 4311, "deg_sanity": "ok"}}}}

reasoning: Paper's DM1-PRE vs CON disease contrast (S2.8.p1); associational.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_POST_vs_PRE_filtered", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 22, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_POST_vs_PRE_filtered\\input\\matrix_filtered.csv", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_POST_vs_PRE_filtered\\DEG_results_POST_vs_PRE.csv"], "counts": {"grp_POST_vs_PRE_filtered": {"applied": {"rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "n_tested": 16857, "n_significant": 27, "n_up": 25, "n_down": 2, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16203, "n_significant": 1075, "n_up": 490, "n_down": 585, "deg_sanity": "ok"}}}}

reasoning: Paper states no low-count filter; iDEP (S4.16.p1) filters low-expressed genes by default. Tests whether low-count genes explain our excess DEGs.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_PRE_vs_CON_filtered", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 21, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_PRE_vs_CON_filtered\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_PRE_vs_CON_filtered\\DEG_results_PRE_vs_CON.csv"], "counts": {"grp_PRE_vs_CON_filtered": {"applied": {"rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "n_tested": 17386, "n_significant": 664, "n_up": 440, "n_down": 224, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17386, "n_significant": 8589, "n_up": 4414, "n_down": 4175, "deg_sanity": "ok"}}}}

reasoning: Same low-count sensitivity for the disease contrast.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_POST_vs_PRE_male", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_POST_vs_PRE_male\\input\\paired\\paired_matrix.csv", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_POST_vs_PRE_male\\DEG_results_POST_vs_PRE.csv"], "counts": {"grp_POST_vs_PRE_male": {"applied": {"rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "n_tested": 37865, "n_significant": 74, "n_up": 58, "n_down": 16, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 18778, "n_significant": 12, "n_up": 10, "n_down": 2, "deg_sanity": "ok"}}}}

reasoning: Per-sex exploratory (5 male pairs); paper pooled sexes.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_POST_vs_PRE_female", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_POST_vs_PRE_female\\input\\paired\\paired_matrix.csv", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\grp_POST_vs_PRE_female\\DEG_results_POST_vs_PRE.csv"], "counts": {"grp_POST_vs_PRE_female": {"applied": {"rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "n_tested": 40533, "n_significant": 49, "n_up": 37, "n_down": 12, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 22459, "n_significant": 36, "n_up": 20, "n_down": 16, "deg_sanity": "ok"}}}}

reasoning: Per-sex exploratory (6 female pairs); paper pooled sexes.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "grp_POST_vs_PRE", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "pvalue", "cutoff": 0.005, "effect_metric": "log2FoldChange", "effect_cutoff": 1.5, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\enrichment_grp_POST_vs_PRE\\ora_up\\DEG_results_POST_vs_PRE_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\enrichment_grp_POST_vs_PRE\\ora_up\\DEG_results_POST_vs_PRE_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\enrichment_grp_POST_vs_PRE\\ora_up\\DEG_results_POST_vs_PRE_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\enrichment_grp_POST_vs_PRE\\ora_up\\DEG_results_POST_vs_PRE_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 41 Human genes (direction=up, pvalue<0.005, |log2FC|>1.5). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Extracellular Structure Organization (GO:0043062) | padj=3.10e-04 | overlap=5/109 | genes=ADAMTS16;COL1A1;ADAMTS14;COL3A1;ADAMTS18 - External  ... [1196 more characters]

reasoning: Paper reports GO BP terms up with training (Fig 4E).

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "grp_POST_vs_PRE", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35316212\\GSE184951\\results\\enrichment_grp_POST_vs_PRE\\gsea\\DEG_results_POST_vs_PRE_GSEA_Hallmark.csv"], "summary": "GSEA complete on 33226 Human genes ranked by 'stat'. 50 Hallmark sets tested, 42 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.60 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_APICAL_JUNCTION | NES=2.14 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=2.08 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.05 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=2.03 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=1.95 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MITOTIC_SPINDLE | NES=1.91 | NOM p=0.00e+00 | FDR q=2.85e-04 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.89 | NOM p=0.00e+00 | FDR q=2.49e-04 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.89 | NOM p=0.00e+00 | FDR q=2.22e-04 - HALLMARK_IL6_JAK_STAT3_SIGNALING | NES=1.83 | NOM p=0.00e+00 | FDR q=1.99e-04 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.70 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_DNA_REPAIR | NES=-1.97 | NOM p=0.00e+00 | FDR q=0.00e+0 ... [387 more characters]

reasoning: Full-ranking Hallmark GSEA for the exercise contrast.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["PRE vs CON is associational (disease), not an exercise effect", "Extraction batches (S4.16.p1) may coincide with group (PRE/POST/CON extracted in individual batches); batch not deposited and cannot be adjusted", "Paper threshold uses raw P < 0.005 without multiple-testing correction", "Paper's DEG lists (Supplemental Table 3) unavailable; only counts compared", "Per-sex POST vs PRE runs are exploratory (5 male / 6 female pairs); sex inferred from expression, not deposited"], "results": {"grp_POST_vs_PRE": {"n_deg": 55, "up": 46, "down": 9, "rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "audit_n": 1066}, "grp_PRE_vs_CON": {"n_deg": 1471, "up": 1156, "down": 315, "rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "audit_n": 9745}, "grp_POST_vs_PRE_filtered": {"n_deg": 27, "up": 25, "down": 2, "rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "audit_n": 1075}, "grp_PRE_vs_CON_filtered": {"n_deg": 664, "up": 440, "down": 224, "rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "audit_n": 8589}, "grp_POST_vs_PRE_male": {"n_deg": 74, "up": 58, "down": 16, "rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "audit_n": 12}, "grp_POST_vs_PRE_female": {"n_deg": 49, "up": 37, "down": 12, "rule": "pvalue < 0.005 and |log2FoldChange| > 1.5", "audit_n": 36}}, "paper_counts": {"grp_POST_vs_PRE": 19, "grp_PRE_vs_CON": 640}, "comparison": {"grp_POST_vs_PRE": {"ours": 55, "paper": 19}, "grp_PRE_vs_CON": {"ours": 1471, "paper": 640}}, "paper_ ... [433 more characters]

reasoning: Counts from S2.9.p1 (1 down + 18 up) and S2.8.p1 (205 down + 435 up). Named upregulated small RNAs from S2.8.p1.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 32 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "CON n",
    "paper": "11 controls recruited (S4.1.p1); Fig 4 n = 10-11",
    "data": "10 CON samples in GEO (no control matched to patient 5)",
    "disposition": "executable_without_change"
  },
  {
    "item": "extraction batch",
    "paper": "P6 pilot pair and per-group extraction batches (S4.16.p1)",
    "data": "no batch annotation",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID35316212 / GSE184951

Paper: *Aerobic exercise elicits clinical adaptations in myotonic dystrophy type 1 patients independently of pathophysiological changes* (PMC9106360). Decision maker: Claude Opus 5.5 session (case-spec route). Status: **finished**. Contract validator: 17 records, 0 errors.

## What ran

- **Inputs:** per-sample HTSeq `*.geneCounts.txt.gz` from `GSE184951_RAW.tar` (63,677 Ensembl genes × 32 samples, all integers). The three `*.SE.MATS.JC.txt.gz` files are rMATS splicing tables and were not used as expression matrices.
- **Samples:** 11 DM1 patients sampled before and after training (S1–S9, S12, S13; P10 and P11 dropped out, S4.1.p1), plus 10 healthy controls (CON). Alignment was an exact match on the GSM ids.
- **Grouping and pairing:** `grp` (CON/PRE/POST) and `subject` come from the sample title. Each control gets its own subject id (`Control_N`), so a control matched to patient N is not counted as the same person.
- **Sex check:** sex inferred from Y-chromosome and XIST expression is consistent within every pre/post pair, and every control matches its patient's sex (DM1 5 M / 6 F; CON 5 M / 5 F). Metadata has no sex field, so `sex` was recoded from this check.
- **Method:** DESeq2 (pydeseq2 Wald), the paper's method (S4.16.p1).
  - Primary: `~ subject + grp`, POST vs PRE, 11 complete pairs.
  - Secondary: `~ grp`, PRE vs CON. This is a disease comparison (associational), not an exercise effect.
- **Threshold:** the paper's own rule from the Fig 4 legend: |log2FC| > 1.5 and raw P < 0.005, with no FDR. Source: `paper`. A separate audit rule is BH padj < 0.05 with no fold-change cutoff.
- **Enrichment:** ORA (Enrichr GO/KEGG) on POST vs PRE up-regulated genes, and Hallmark GSEA on the full POST vs PRE ranking.

## DEG counts vs the paper (|log2FC| > 1.5, P < 0.005)

| Table | Role | Ours (up/down) | Paper (up/down) | Audit padj<0.05 |
|---|---|---|---|---|
| grp_POST_vs_PRE | primary (paper_aligned) | 55 (46/9) | 19 (18/1) | 1066 |
| grp_PRE_vs_CON | secondary (associational) | 1471 (1156/315) | 640 (435/205) | 9745 |
| grp_POST_vs_PRE_filtered (mean count ≥ 10) | sensitivity | 27 (25/2) | 19 (18/1) | 1075 |
| grp_PRE_vs_CON_filtered (mean count ≥ 10) | sensitivity | 664 (440/224) | 640 (435/205) | 8589 |
| grp_POST_vs_PRE_male (5 pairs) | exploratory | 74 (58/16) | – | 12 |
| grp_POST_vs_PRE_female (6 pairs) | exploratory | 49 (37/12) | – | 36 |

- **Unfiltered runs:** the extra DEGs are mostly low-count genes (baseMe ... [2591 more characters]
