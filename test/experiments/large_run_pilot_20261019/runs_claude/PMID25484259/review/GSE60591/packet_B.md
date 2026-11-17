# Review packet B (the analysis' decisions): GSE60591

## Mechanical flags

- **other_rule_matches_paper**: {"table": "grp_T2_vs_T1_nobatch", "paper": 4076, "applied": 2576, "applied_rule": "padj < 0.05", "closest_rule": "pvalue<0.05", "closest_n": 4198, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_T2_vs_T1 | 4076 | 1608 | padj < 0.05 | 1608 | 205 | 19 | 2440 | 3496 | 233 | 25 | 1901 | 0.054 | 0.282 |
| grp_T2_vs_T1_nobatch | 4076 | 2576 | padj < 0.05 | 2576 | 72 | 8 | 3476 | 4198 | 79 | 11 | 2559 | 0.046 | 0.338 |

## Samples per design level

### `grp`
- **T1** (23): GSM1415126 / 217; GSM1415128 / 174; GSM1415130 / 135; GSM1415132 / 113; GSM1415134 / 169; GSM1415136 / 223; GSM1415138 / 205; GSM1415140 / 130; GSM1415142 / 211; GSM1415144 / 157; GSM1415146 / 172; GSM1415148 / 152; GSM1482934 / 196; GSM1482940 / 101; GSM1482944 / 206; GSM1482946 / 186; GSM1482948 / 212; GSM1482950 / 191; GSM1482952 / 147; GSM1482954 / 218; GSM1482956 / 108; GSM1482958 / 132; GSM1482961 / 118
- **T2** (22): GSM1482932 / 219; GSM1482933 / 182; GSM1482935 / 201; GSM1482936 / 121; GSM1482937 / 177; GSM1482938 / 202; GSM1482939 / 207; GSM1482941 / 109; GSM1482942 / 138; GSM1482943 / 213; GSM1482945 / 208; GSM1482947 / 194; GSM1482949 / 214; GSM1482951 / 104; GSM1482953 / 155; GSM1482955 / 220; GSM1482957 / 116; GSM1482959 / 140; GSM1482960 / 165; GSM1482962 / 126; GSM1482963 / 180; GSM1482964 / 160

### `subject`
- **s01** (2): GSM1482940 / 101; GSM1482941 / 109
- **s02** (2): GSM1482956 / 108; GSM1482957 / 116
- **s03** (2): GSM1482958 / 132; GSM1482959 / 140
- **s04** (2): GSM1415144 / 157; GSM1482960 / 165
- **s05** (2): GSM1482961 / 118; GSM1482962 / 126
- **s07** (2): GSM1415146 / 172; GSM1482963 / 180
- **s09** (2): GSM1415148 / 152; GSM1482964 / 160
- **s11** (2): GSM1415126 / 217; GSM1482932 / 219
- **s12** (2): GSM1415128 / 174; GSM1482933 / 182
- **s13** (1): GSM1415130 / 135
- **s14** (2): GSM1482934 / 196; GSM1482935 / 201
- **s15** (2): GSM1415132 / 113; GSM1482936 / 121
- **s16** (2): GSM1415134 / 169; GSM1482937 / 177
- **s18** (2): GSM1415136 / 223; GSM1482938 / 202
- **s19** (2): GSM1415138 / 205; GSM1482939 / 207
- **s20** (2): GSM1415140 / 130; GSM1482942 / 138
- **s21** (2): GSM1415142 / 211; GSM1482943 / 213
- **s22** (2): GSM1482944 / 206; GSM1482945 / 208
- **s23** (2): GSM1482946 / 186; GSM1482947 / 194
- **s24** (2): GSM1482948 / 212; GSM1482949 / 214
- **s26** (2): GSM1482950 / 191; GSM1482951 / 104
- **s27** (2): GSM1482952 / 147; GSM1482953 / 155
- **s28** (2): GSM1482954 / 218; GSM1482955 / 220

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE58608", "GSE60590", "GSE60591"], "accession_roles": {"GSE58608": "RNA-seq, pre-training biopsies of both legs (T1 = leg to be trained, U1 = untrained leg) for 12 subjects; S5.4.p2 notes a baseline subset (n=12) analyzed earlier", "GSE60590": "RNA-seq, 22 post-training trained-leg biopsies (T2) plus 11 pre-training T1 biopsies of the other 11 subjects", "GSE60591": "GEO SuperSeries joining GSE58608 + GSE60590 (57 samples); not named in the paper but holds exactly the two cited series", "GSE60655": "DNA methylation 450K (S5.6.p1); not part of this gene-expression request"}, "assay": "bulk RNA-seq, Illumina HiSeq2000, 2x100 bp, vastus lateralis (S5.4.p1, S3.1.p1)", "primary_estimand": "Within-subject change in trained-leg skeletal-muscle gene expression after 3 months of supervised one-legged endurance knee-extension training: T2 (24 h after last session) vs T1 (pre-training), trained leg (S3.1.p1, S3.1.p2, S5.1.p1, S5.4.p2)", "planned_contrasts": ["T2 vs T1, trained leg, individual and library preparation as covariates (S5.4.p2; paper: 4076 DEGs, S3.1.p2)"], "factors": {"group": ["T1 pre-training trained leg", "T2 post-training trained leg"], "individual": "23 subjects (12 M, 11 F; TAB1)", "library_preparation": "covariate named in S5.4.p2; not annotated in GEO"}, "sample_inclusion": "23 sedentary young subjects; biopsies from both legs before and after training (S3.1.p1). RNA-seq DE is trained leg T2 vs T1 (S3.1.p2, S5.4.p2). The untrained leg is an intrain ... [1060 more characters]

reasoning: S5.4.p2 gives the RNA-seq DE: edgeR, group T2 vs T1 with library preparation and individual as covariates, FDR<0.05; S3.1.p2 reports 4076 DEGs. Design (one-legged training, biopsies pre/post) from S3.1.p1 and S5.1.p1. S5.6.p1 names GSE58608 and GSE60590 for expression.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["SuperSeries of GSE58608 + GSE60590 (series_id), both cited in S5.6.p1", "57 samples = 24 (GSE58608) + 33 (GSE60590), no overlap", "23 subjects with T1, 22 with T2 (subject 13 has no T2)"], "accession": "GSE60591", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE60591\\GSE60591_metadata.csv"}

reasoning: S5.6.p1 names GSE58608 and GSE60590 as the gene-expression series. GSE60591 metadata: Homo sapiens skeletal muscle, KTH/SciLifeLab, HiSeq2000 RNA-seq, original sample IDs <subject><T|U><1|2> matching the paper's T1/T2 and trained/untrained leg scheme.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 57, "n_metadata": 57, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM1415127": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415129": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415131": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415133": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415135": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415137": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415139": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415141": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415143": "U1 = untrained control leg before training; not part of the paper's RNA-seq T2 vs T1 trained-leg model (S3.1.p2, S5.4.p2)", "GSM1415145": "U1 = untrained control leg before training; not part of the  ... [1593 more characters]

reasoning: Matrix columns are GSM ids. subject and grp parsed from the supplementary_file_1 file name (<subject><T|U><1|2>); batch from the sub-series in series_id (GSE58608 -> b1, GSE60590 -> b2). The 12 U1 samples are excluded. Subject 7 biopsy-location conflict noted; the T/U code is used.

### matrix (valid, not_started)

final: {"source": "GEO per-sample Cufflinks genes.fpkm_tracking files in the _RAW.tar, merged on gene_id (FPKM column)", "paper_input": "gene read counts for edgeR (S5.4.p2); not deposited", "matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\aligned\\aligned_matrix.csv", "sha256": "1c63a50ad1db89abbe94f7bfd9101c91235f8c24c78435beec96cd5ef637a0ca", "n_features": 61779, "n_samples": 45, "annotation_columns_dropped": ["GSM1415127", "GSM1415129", "GSM1415131", "GSM1415133", "GSM1415135", "GSM1415137", "GSM1415139", "GSM1415141", "GSM1415143", "GSM1415145", "GSM1415147", "GSM1415149"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 85707.6, "median": 0.0, "integer_fraction": 0.5865, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample files are Cufflinks genes.fpkm_tracking (FPKM, FPKM_conf_lo/hi, FPKM_status); data_processing: TopHat 2.0.4 + Cufflinks 2.0.2. Values are non-integer (integer fraction about 0.58, almost all zeros), max about 85,700: linear FPKM. No read counts deposited, so edgeR on counts cannot be reproduced; FPKM must not be rounded into counts. Route: log2(FPKM+1), then limma.

### design (valid, not_started)

final: {"analysis_type": "paired", "design_column": "grp", "control": "T1", "treatment": "T2", "contrasts": [{"name": "grp_T2_vs_T1", "control": "T1", "treatment": "T2", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Paper estimand: T2 vs T1, trained leg, all subjects, individual as covariate (S5.4.p2). 45 samples: 23 T1 + 22 T2. Sexes pooled as in the paper; sex is constant within subject.

rejected alternatives: [{"value": "grp with U1 as a third level", "reason_rejected": "U1 is the untrained leg at baseline; the paper's RNA-seq DE is T2 vs T1 only"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "included"}, {"name": "batch", "disposition": "included"}, {"name": "sex", "disposition": "excluded: constant within subject, absorbed by the subject block"}], "design_check": {"formula_equivalent": "~ C(grp) + C(subject)", "n_samples": 45, "n_columns": 24, "columns": ["Intercept", "grp_T2", "subject_s02", "subject_s03", "subject_s04", "subject_s05", "subject_s07", "subject_s09", "subject_s11", "subject_s12", "subject_s13", "subject_s14", "subject_s15", "subject_s16", "subject_s18", "subject_s19", "subject_s20", "subject_s21", "subject_s22", "subject_s23", "subject_s24", "subject_s26", "subject_s27", "subject_s28"], "rank": 24, "full_rank": true, "residual_df": 21, "levels": {"grp": {"T1": 23, "T2": 22}, "subject": {"s11": 2, "s12": 2, "s15": 2, "s16": 2, "s18": 2, "s19": 2, "s20": 2, "s21": 2, "s04": 2, "s07": 2, "s09": 2, "s14": 2, "s01": 2, "s22": 2, "s23": 2, "s24": 2, "s26": 2, "s27": 2, "s28": 2, "s02": 2, "s03": 2, "s05": 2, "s13": 1}}, "cells": [{"cell": ["T1", "s01"], "n": 1}, {"cell": ["T1", "s02"], "n": 1}, {"cell": ["T1", "s03"], "n": 1}, {"cell": ["T1", "s04"], "n": 1}, {"cell": ["T1", "s05"], "n": 1}, {"cell": ["T1", "s07"], "n": 1}, {"cell": ["T1", "s09"], "n": 1}, {"cell": ["T1", "s11"], "n": 1}, {"cell": ["T1", "s12"], "n": 1}, {"cell": ["T1", "s13"], "n": 1}, {"cell": ["T1", "s14"], "n": 1}, {"cell": ["T1", "s15"], "n": 1}, {"cell": ["T1", "s16"], "n": 1}, ... [1793 more characters]

reasoning: The paper includes individual and library preparation (S5.4.p2). Library preparation is not deposited; the sub-series (b1 = GSE58608 baseline samples, b2 = GSE60590) is the only available proxy. All T2 are in b2, but 11 subjects have both T1 and T2 within b2, so batch is estimable alongside subject (not aliased). A sensitivity without batch is run.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (moderated t, eBayes) on log2(FPKM+1) with subject block and series batch", "formula": "~ Treatment + C(subject) + C(batch)", "paper_route": {"method": "edgeR on gene counts, ~ group + library preparation + individual", "status": "blocked", "reason": "GEO holds only Cufflinks FPKM per sample; neither read counts nor library-preparation labels were deposited"}, "deviations": ["limma on log2(FPKM+1) instead of edgeR on counts", "sub-series used as proxy for library preparation"], "transform": "log2(x+1)"}

reasoning: The paper route (edgeR on counts) is blocked: only Cufflinks FPKM is deposited. Validated alternative for linear FPKM: log2(FPKM+1), then limma (moderated t, eBayes) with subject as a fixed block, matching the paper's individual covariate. Genes are filtered to FPKM>=1 in at least as many samples as the smaller arm (analogous to the usual edgeR CPM filter) so the near-zero loci among the 61,779 Cufflinks genes are not tested.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S5.4.p2"}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": false}, "deviation_note": "The paper's FDR<0.05 (no fold-change cutoff) is applied unchanged to limma BH-adjusted p on log2(FPKM+1) because edgeR on counts is blocked. The audit rule adds |log2FC|>log2(1.5) only as a labelled comparison."}

reasoning: S5.4.p2: DEG were selected if FDR<0.05; no effect-size rule stated.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_T2_vs_T1", "role": "primary", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 45, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\grp_T2_vs_T1\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject,batch + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\grp_T2_vs_T1\\DEG_results_T2_vs_T1.csv"], "counts": {"grp_T2_vs_T1": {"applied": {"rule": "padj < 0.05", "n_tested": 12417, "n_significant": 1608, "n_up": 1069, "n_down": 539, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12417, "n_significant": 205, "n_up": 153, "n_down": 52, "deg_sanity": "ok"}}}}

reasoning: Paper estimand: T2 vs T1 trained leg with individual and library-prep (proxy) covariates.

### execution (valid, completed)

final: {"method": "run_limma_analysis", "subset": "grp_T2_vs_T1_nobatch", "role": "sensitivity", "tool": "tools.limma_tools:run_limma_analysis", "n_samples": 45, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\grp_T2_vs_T1_nobatch\\input\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ subject + grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\grp_T2_vs_T1_nobatch\\DEG_results_T2_vs_T1.csv"], "counts": {"grp_T2_vs_T1_nobatch": {"applied": {"rule": "padj < 0.05", "n_tested": 12417, "n_significant": 2576, "n_up": 1583, "n_down": 993, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 0.584963", "n_tested": 12417, "n_significant": 72, "n_up": 53, "n_down": 19, "deg_sanity": "ok"}}}}

reasoning: Sensitivity to the library-prep proxy: subject block only.

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "grp_T2_vs_T1", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\enrichment_grp_T2_vs_T1\\ora\\DEG_results_T2_vs_T1_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\enrichment_grp_T2_vs_T1\\ora\\DEG_results_T2_vs_T1_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\enrichment_grp_T2_vs_T1\\ora\\DEG_results_T2_vs_T1_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\enrichment_grp_T2_vs_T1\\ora\\DEG_results_T2_vs_T1_KEGG_2021_Human.csv"], "summary": "Enrichment analysis complete for 1515 Human genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Respiration (GO:0045333) | padj=5.91e-32 | overlap=51/85 | genes=COX7B;NDUFA13;NDUFA11;NDUFA12;COX4I1;COX4I2;NDUFA10;ETFA;ETFB;MTFR1L;COX6A1;COX7 - Proton Motive Force-Driven AT ... [1152 more characters]

reasoning: The paper reports GO/KEGG enrichment of DEGs (S5.4.p2; S3.5.p1: OXPHOS, ECM, angiogenesis).

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "grp_T2_vs_T1", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID25484259\\GSE60591\\results\\enrichment_grp_T2_vs_T1\\gsea\\DEG_results_T2_vs_T1_GSEA_Hallmark.csv"], "summary": "GSEA complete on 11456 Human genes ranked by 'stat'. 50 Hallmark sets tested, 36 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.28 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=2.63 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=2.44 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ADIPOGENESIS | NES=2.42 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=2.41 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANGIOGENESIS | NES=2.06 | NOM p=0.00e+00 | FDR q=1.67e-04 - HALLMARK_COMPLEMENT | NES=2.04 | NOM p=0.00e+00 | FDR q=1.43e-04 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=2.01 | NOM p=0.00e+00 | FDR q=1.25e-04 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.96 | NOM p=0.00e+00 | FDR q=1.11e-04 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.96 | NOM p=0.00e+00 | FDR q=9.99e-05 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_G2M_CHECKPOINT | NES=-1.58 | NOM p=0.00e+00 | FDR q=8.92e-02 - HALLMARK_E2F_TARGETS | NES=-1.35 | NOM p=5.52e-03 | FDR q=2.62e-01 - HA ... [377 more characters]

reasoning: The paper reports GO/KEGG enrichment of DEGs (S5.4.p2; S3.5.p1: OXPHOS, ECM, angiogenesis).

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["FPKM with limma replaces counts with edgeR; DEG counts are not expected to match exactly", "Library preparation approximated by sub-series; with subject blocking the batch term leaves the training effect informed mainly by the 11 within-series pairs", "Subject 13 has no T2 sample (22 T2 vs 23 T1)"], "results": {"grp_T2_vs_T1": {"n_deg": 1608, "up": 1069, "down": 539, "rule": "padj < 0.05", "audit_n": 205}, "grp_T2_vs_T1_nobatch": {"n_deg": 2576, "up": 1583, "down": 993, "rule": "padj < 0.05", "audit_n": 72}}, "paper_counts": {"grp_T2_vs_T1": 4076, "grp_T2_vs_T1_nobatch": 4076}, "comparison": {"grp_T2_vs_T1": {"ours": 1608, "paper": 4076}, "grp_T2_vs_T1_nobatch": {"ours": 2576, "paper": 4076}}, "paper_gene_check": {"grp_T2_vs_T1": {"COL4A1": {"AveExpr": 3.9886, "log2FoldChange": 1.5962, "padj": 4.47e-05, "pvalue": 1.72e-08}, "COL4A2": {"AveExpr": 3.9919, "log2FoldChange": 1.6112, "padj": 2.64e-06, "pvalue": 2.13e-10}, "A2M": {"AveExpr": 5.6161, "log2FoldChange": 0.734, "padj": 0.000552, "pvalue": 3.56e-06}, "THBS4": {"AveExpr": 4.2757, "log2FoldChange": 1.3822, "padj": 0.000448, "pvalue": 2.52e-06}, "PDGFRB": {"AveExpr": 3.7483, "log2FoldChange": 0.4591, "padj": 0.00491, "pvalue": 0.000167}, "LAMA4": {"AveExpr": 2.3404, "log2FoldChange": 0.8601, "padj": 0.00134, "pvalue": 1.92e-05}, "CS": {"AveExpr": 7.495, "log2FoldChange": 0.2329, "padj": 0.028, "pvalue": 0.00247}, "SDHA": {"AveExpr": 7.1785, "log2FoldChange": 0.2864, "padj": 0.00 ... [3753 more characters]

reasoning: Paper: 4076 DEGs at FDR<0.05 (S3.1.p2); named genes from S3.5.p1-p2 and S4.p10-p11.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 45 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "edgeR on gene counts (S5.4.p2)",
    "data": "only Cufflinks FPKM deposited",
    "disposition": "declared_deviation: limma on log2(FPKM+1)"
  },
  {
    "item": "library preparation covariate",
    "paper": "included (S5.4.p2)",
    "data": "not annotated in GEO",
    "disposition": "proxy: sub-series batch; sensitivity without it"
  },
  {
    "item": "accession",
    "paper": "GSE58608 and GSE60590 (S5.6.p1)",
    "data": "GSE60591 SuperSeries holds both",
    "disposition": "executable_without_change"
  },
  {
    "item": "subject 7 biopsy leg",
    "paper": "publication id 8L for 7T1",
    "data": "GSE58608 biopsy location 'right leg' for 7T1; GSE60590 7T2 'left leg'",
    "disposition": "executable_without_change: T/U code defines the arm"
  },
  {
    "item": "sample count",
    "paper": "23 subjects (TAB1)",
    "data": "23 T1, 22 T2 (subject 13 has no T2)",
    "disposition": "executable_without_change"
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
