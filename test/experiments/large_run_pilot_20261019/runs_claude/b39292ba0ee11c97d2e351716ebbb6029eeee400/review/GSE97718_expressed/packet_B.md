# Review packet B (the analysis' decisions): GSE97718_expressed

## Mechanical flags

- **other_rule_matches_paper**: {"table": "joint/grp_HFDpost_vs_CONpost", "paper": 234, "applied": 17, "applied_rule": "padj < 0.05", "closest_rule": "pvalue<0.01", "closest_n": 208, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "grp", "pairs_or_sets": 4, "samples_linked": 16, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_CONpost_vs_CONpre | 401 | 132 | padj < 0.05 | 132 | 87 | 36 | 215 | 1199 | 161 | 50 | 462 | 0.079 | 0.116 |
| joint/grp_HFDpost_vs_HFDpre | 323 | 59 | padj < 0.05 | 59 | 45 | 14 | 88 | 1248 | 128 | 29 | 399 | 0.076 | 0.121 |
| joint/grp_HFDpre_vs_CONpre | 212 | 32 | padj < 0.05 | 32 | 22 | 10 | 63 | 863 | 86 | 23 | 276 | 0.096 | 0.083 |
| joint/grp_HFDpost_vs_CONpost | 234 | 17 | padj < 0.05 | 17 | 14 | 4 | 30 | 658 | 76 | 24 | 208 | 0.103 | 0.064 |

## Samples per design level

### `grp`
- **CONpost** (4): GSM2576101 / CON-post 1; GSM2576102 / CON-post 2; GSM2576103 / CON-post 3; GSM2576104 / CON-post 4
- **CONpre** (4): GSM2576093 / CON-pre 1; GSM2576094 / CON-pre 2; GSM2576095 / CON-pre 3; GSM2576096 / CON-pre 4
- **HFDpost** (4): GSM2576105 / HFD-post 1; GSM2576106 / HFD-post 2; GSM2576107 / HFD-post 3; GSM2576108 / HFD-post 4
- **HFDpre** (4): GSM2576097 / HFD-pre 1; GSM2576098 / HFD-pre 2; GSM2576099 / HFD-pre 3; GSM2576100 / HFD-pre 4

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE97718"], "assay": "bulk RNA-seq (TruSeq stranded mRNA, HiSeq 2500), mouse quadriceps", "factors": {"diet": ["CON (10% fat)", "HFD (60% fat) for 10 weeks"], "exercise": ["pre (basal, acclimatized+fasted)", "post (3 h after one maximal treadmill bout)"]}, "sample_inclusion": "2x2 factorial, n = 4 muscles per group (FIG2/FIG3/FIG4 legends), independent male C57BL/6NTac mice; all 16 GEO samples", "primary_estimand": "Acute maximal exercise effect (post vs pre, 3 h) on quadriceps gene expression within CON-diet mice and within HFD mice (between-animal, not repeated measures)", "planned_contrasts": ["CON-post vs CON-pre (S2.2.p1; paper: 292 up + 109 down = 401 DEGs)", "HFD-post vs HFD-pre (S2.2.p1; paper: 208 up + 115 down = 323 DEGs)", "HFD-pre vs CON-pre (S2.1.p2; paper: 119 up + 93 down = 212 DEGs) - diet effect, secondary", "HFD-post vs CON-post (S2.2.p3; paper: 234 DEGs) - diet effect post-exercise, secondary"], "repeated_measure_unit": "none (pre and post are different animals, S4.4.p1)", "normalization": "Cufflinks FPKM (S4.6.p1)", "paper_method": "TopHat (mm9) + Cufflinks/Cuffdiff pairwise comparisons (S4.6.p1)", "paper_threshold": {"metric": "not_stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "S4.6.p1", "note": "Paper says only that comparisons were done with cufflinks; no FDR/fold-change rule is stated (Cuffdiff's default 'significant' flag is q < 0.05, but that is not written in the paper). S4.9.p1 p < 0.05 re ... [346 more characters]

reasoning: Methods S4.1/S4.4: CON vs HFD for 10 weeks, then basal (pre) or 3 h after a maximal treadmill test (post). RNA-seq S4.6.p1 with Cufflinks; n = 4 per group (FIG3). The paper's question about exercise is the post vs pre comparison within each diet (S2.2.p1); the diet contrasts (S2.1.p2, S2.2.p3) are secondary.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\prep\\GSE97718_FPKM_gene_level_expressed.csv", "owned": true, "checks": ["S4.10.p1 names GSE97718", "16 GEO samples = 4 groups x 4, matching n = 4 per group", "titles CON-pre/HFD-pre/CON-post/HFD-post match the paper's group names", "source quadriceps matches S2.2.p1", "data_processing TopHat mm9 + cufflinks matches S4.6.p1"], "accession": "GSE97718", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE97718\\GSE97718_metadata.csv"}

reasoning: Data availability statement S4.10.p1 cites GSE97718; sample groups, tissue, strain (C57BL/6NTac), age (16 weeks) and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 16, "n_metadata": 16, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(CON|HFD)-(pre|post) \\d$", "recode": {"CON_pre": "CONpre", "CON_post": "CONpost", "HFD_pre": "HFDpre", "HFD_post": "HFDpost"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\aligned\\design_metadata.csv", "sha256": "b5a7dbfdc2edf7cf12a1a14784d26057998bca86b517e17e4101d6eb23bf6f14", "levels": {"grp": {"CONpre": 4, "HFDpre": 4, "CONpost": 4, "HFDpost": 4}}}}

reasoning: Matrix columns 'CONpre_1 (FPKM)' and metadata titles 'CON-pre 1' both reduce to the key CON_pre_1 by name (diet, time, replicate number); no positional matching. grp is the 4-level diet x exercise group taken from the title.

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\aligned\\aligned_matrix.csv", "sha256": "872ceae39130d3783ce38ce7df809f9ea0657220ca23175895af6e91653d4941", "n_features": 10356, "n_samples": 16, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 17377.5, "median": 5.1058900000000005, "integer_fraction": 0.0018, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name GSE97718_FPKM_cufflinks_all_samples, column headers '(FPKM)', data_processing 'cufflinks', 39% integer fraction (mostly zeros) and decimal values; linear FPKM, not counts. The paper's input was Cufflinks/Cuffdiff on aligned reads, which is not deposited (no BAM/counts). Prep script restored 25 Excel-mangled names (Marchf*/Septin*/Selenof) and summed the 262 gene names that Cufflinks reported on several loci into one gene-level row. Sensitivity case: additionally restricted to 10,356 genes with FPKM >= 1 in >= 4 samples (prep/filter_expressed.py), approximating Cuffdiff's exclusion of loci without enough reads; reduces the BH multiple-testing burden from near-zero genes.

### design (valid, not_started)

final: {"analysis_type": "multi-group (2x2 factorial as a 4-level group factor)", "design_column": "grp", "contrasts": [{"name": "grp_CONpost_vs_CONpre", "control": "CONpre", "treatment": "CONpost", "role": "primary"}, {"name": "grp_HFDpost_vs_HFDpre", "control": "HFDpre", "treatment": "HFDpost", "role": "primary"}, {"name": "grp_HFDpre_vs_CONpre", "control": "CONpre", "treatment": "HFDpre", "role": "secondary"}, {"name": "grp_HFDpost_vs_CONpost", "control": "CONpost", "treatment": "HFDpost", "role": "secondary"}], "estimand_type": "causal (assigned intervention groups)", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: Paper reports pairwise Cuffdiff comparisons among the four groups; a single model with all 16 samples and the four planned contrasts reproduces those comparisons (one control level per contrast, no pooling).

rejected alternatives: [{"value": "pooled exercise effect (post vs pre across diets)", "reason_rejected": "paper analyzes exercise separately within CON and HFD (S2.2.p1); pooling would mix diet-specific responses"}, {"value": "diet x exercise interaction term", "reason_rejected": "paper does not test an interaction; it compares within-diet exercise DEG lists and CON-post vs HFD-post (S2.2.p3)"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 16, "n_columns": 4, "columns": ["Intercept", "grp_CONpre", "grp_HFDpost", "grp_HFDpre"], "rank": 4, "full_rank": true, "residual_df": 12, "levels": {"grp": {"CONpre": 4, "HFDpre": 4, "CONpost": 4, "HFDpost": 4}}, "cells": [{"cell": ["CONpost"], "n": 4}, {"cell": ["CONpre"], "n": 4}, {"cell": ["HFDpost"], "n": 4}, {"cell": ["HFDpre"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 16, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 16, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.age", "n_levels": 1, "status": "constant"}, {"column": "molecule_ch1", "n_levels": 1, "status": "constant"}, { ... [1367 more characters]

reasoning: Each sample is a different mouse (pre group is a separate basal cohort, S4.4.p1); no batch, lane or animal pairing is recorded in GEO. No blocking term.

### method (valid, not_started)

final: {"matrix_type": "FPKM", "method": "limma (moderated t, eBayes) on log2(FPKM+1)", "formula": "~ 0 + grp", "paper_route": {"method": "Cufflinks/Cuffdiff on TopHat alignments", "status": "blocked", "reason": "only the FPKM matrix is deposited; Cuffdiff needs the aligned reads (BAM) or per-sample abundance files"}, "deviations": ["limma on log2(FPKM+1) instead of Cuffdiff", "one model on all 16 samples instead of pairwise Cuffdiff runs", "gene-level rows (multi-locus names summed) instead of Cufflinks loci", "expressed-gene filter FPKM >= 1 in >= 4 samples (sensitivity)"], "transform": "log2(x+1)"}

reasoning: Matrix policy: FPKM -> log2(x+1) -> limma. DESeq2/edgeR/voom are not allowed on FPKM.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "not_stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "workflow_default", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper states no DEG rule (S4.6.p1). Workflow default BH FDR < 0.05 with no fold-change cutoff; it coincides with Cuffdiff's default q < 0.05 'significant' call. Audit raw p < 0.01 shown only to gauge sensitivity of counts."}

reasoning: No threshold in S4.6.p1; S4.9.p1's p < 0.05 refers to physiology statistics, so workflow default is used and marked as a fallback.

### execution (valid, completed)

final: {"method": "run_joint_limma", "subset": "joint", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_limma", "n_samples": 16, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\transformed\\log2_matrix.csv", "transform": "log2(x+1)", "formula": "~ 0 + C(cell)", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\results\\joint\\DEG_results_grp_CONpost_vs_CONpre.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\results\\joint\\DEG_results_grp_HFDpost_vs_HFDpre.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\results\\joint\\DEG_results_grp_HFDpre_vs_CONpre.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\b39292ba0ee11c97d2e351716ebbb6029eeee400\\GSE97718_expressed\\results\\joint\\DEG_results_grp_HFDpost_vs_CONpost.csv"], "counts": {"joint/grp_CONpost_vs_CONpre": {"applied": {"rule": "padj < 0.05", "n_tested": 10356, "n_significant": 132, "n_up": 113, "n_down": 19, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.01", "n_tested": 10356, "n_significant": 462, "n_up": 316, "n_down": 146, "deg_sanity": "ok"}}, "joint/grp_HFDpost_vs_HFDpre": {"applied": {"rule": "padj < 0.05", "n_tested": 10356, "n_significant": 59, "n_up": 52, "n_down": 7,  ... [703 more characters]

reasoning: Same joint limma model as case GSE97718 on the expressed-gene subset; sensitivity of DEG counts to the low-expression filter.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Cuffdiff is blocked (no reads deposited); limma on log2(FPKM+1) is a declared deviation, so DEG counts are not expected to match exactly", "paper DEG threshold not stated; workflow default BH FDR < 0.05 applied", "n = 4 per group; pre and post are different animals (between-animal exercise effect)", "sensitivity case with an expression filter chosen by this session, not stated in the paper"], "results": {"joint/grp_CONpost_vs_CONpre": {"n_deg": 132, "up": 113, "down": 19, "rule": "padj < 0.05", "audit_n": 462}, "joint/grp_HFDpost_vs_HFDpre": {"n_deg": 59, "up": 52, "down": 7, "rule": "padj < 0.05", "audit_n": 399}, "joint/grp_HFDpre_vs_CONpre": {"n_deg": 32, "up": 22, "down": 10, "rule": "padj < 0.05", "audit_n": 276}, "joint/grp_HFDpost_vs_CONpost": {"n_deg": 17, "up": 13, "down": 4, "rule": "padj < 0.05", "audit_n": 208}}, "paper_counts": {"joint/grp_CONpost_vs_CONpre": 401, "joint/grp_HFDpost_vs_HFDpre": 323, "joint/grp_HFDpre_vs_CONpre": 212, "joint/grp_HFDpost_vs_CONpost": 234}, "comparison": {"joint/grp_CONpost_vs_CONpre": {"ours": 132, "paper": 401}, "joint/grp_HFDpost_vs_HFDpre": {"ours": 59, "paper": 323}, "joint/grp_HFDpre_vs_CONpre": {"ours": 32, "paper": 212}, "joint/grp_HFDpost_vs_CONpost": {"ours": 17, "paper": 234}}, "paper_gene_check": {"joint/grp_CONpost_vs_CONpre": {"Egr1": {"AveExpr": 1.66, "log2FoldChange": 1.3034, "padj": 0.0372, "pvalue": 0.0004}, "Klf5": {"AveExpr": 1.4329, "log2FoldChange": 0.9205, "padj": 0 ... [1056 more characters]

reasoning: Paper counts from S2.1.p2, S2.2.p1, S2.2.p3. Named genes from S2.2.p2, S2.2.p3, S3.p4, S2.1.p2.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "Cufflinks/Cuffdiff on TopHat alignments (S4.6.p1)",
    "data": "only FPKM matrix in GEO",
    "disposition": "declared_deviation"
  },
  {
    "item": "threshold",
    "paper": "not stated",
    "data": "n/a",
    "disposition": "workflow_default"
  },
  {
    "item": "gene identifiers",
    "paper": "mm9 gene names",
    "data": "25 names Excel-mangled to date serials; 262 names on several Cufflinks loci",
    "disposition": "repaired by prep/fix_matrix.py (restored names; multi-locus rows summed)"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE97718 / PMC5647435 (exercise x high-fat diet, mouse quadriceps)

## What ran
- Case spec route (`case_spec.json`), `python -m tools.case_runner execute`. Run status completed. The validator returned 24 records and 0 errors.
- Design: 2x2 (CON/HFD diet x pre/post acute maximal exercise, 3 h). n = 4 independent mice per group, 16 samples, all aligned by name (`CONpre_1 (FPKM)` <-> title `CON-pre 1`, key `CON_pre_1`).
- Matrix: Cufflinks FPKM (`GSE97718_FPKM_cufflinks_all_samples.txt.gz`). The prep script `prep/fix_matrix.py` restored 25 gene names that Excel had turned into date serials (36951 -> Marchf1, ..., Septin1-14, 42248 -> Selenof/Sep15). It also summed the 262 gene names that appear on several Cufflinks loci, leaving 23,995 genes.
- Method: limma on log2(FPKM+1). One model `~ 0 + grp` on all 16 samples, 4 planned contrasts. Cuffdiff (the paper's method) is blocked because only FPKM was deposited, so this is a declared deviation.
- Threshold: the paper states none (S4.6.p1 only says "cufflinks"). Applied the workflow default, BH FDR < 0.05 with no fold-change cutoff; this matches Cuffdiff's default q < 0.05. Audit rule: raw p < 0.01.
- Sensitivity case `GSE97718_expressed`: the same model restricted to 10,356 genes with FPKM >= 1 in >= 4 samples (`prep/filter_expressed.py`). The filter was my choice, to approximate Cuffdiff testing only loci with enough reads.
- Enrichment (case GSE97718, both exercise contrasts): Enrichr ORA and Hallmark GSEA completed.

## DEG counts vs paper (BH FDR < 0.05; paper = Cuffdiff, rule not stated)
| Contrast | Paper | Ours (all genes) | Ours (expressed filter) | Audit p<0.01 (all) |
|---|---|---|---|---|
| CON-post vs CON-pre (primary) | 401 (292 up / 109 down) | 122 (102 / 20) | 132 (113 / 19) | 628 |
| HFD-post vs HFD-pre (primary) | 323 (208 / 115) | 36 (34 / 2) | 59 (52 / 7) | 548 |
| HFD-pre vs CON-pre (secondary) | 212 (119 / 93) | 33 (21 / 12) | 32 (22 / 10) | 420 |
| HFD-post vs CON-post (secondary) | 234 | 9 (9 / 0) | 17 (13 / 4) | 310 |

Direction agrees with the paper. Exercise gives more DEGs in CON than in HFD (blunted response under HFD), mostly up-regulated. Our FDR counts are 3-25x lower than Cuffdiff's. Expected reasons: limma on log FPKM with n = 4 is more conservative than Cuffdiff, and Cuffdiff's lenient per-locus calls are known to be liberal.

Named genes (CON exercise, all-genes case): Nr4a3 (log2FC 2.70, padj 3e-4), Ppargc1a (1.91, 5e-4), Klf5 (0.92, 0.012), Cited2 (1.00, 0.016) an ... [1885 more characters]
