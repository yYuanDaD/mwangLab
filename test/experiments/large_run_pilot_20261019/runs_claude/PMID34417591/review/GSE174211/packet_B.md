# Review packet B (the analysis' decisions): GSE174211

## Mechanical flags

- **pairing_key_candidate**: {"key": "characteristics_ch1.3.running or sedentary (without characteristics_ch1.1.genotype) + suffix of title", "across": "characteristics_ch1.1.genotype", "pairs_or_sets": 8, "samples_linked": 16, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| geno_KO_vs_WT | 459 | 784 | pvalue < 0.05 and |log2FoldChange| > 1.5 | 5488 | 1573 | 898 | 6731 | 7102 | 2101 | 1241 | 4969 | 0.065 | 0.37 |

## Samples per design level

### `grp`
- **KO_Run** (4): GSM5289472 / KO-running group mouse 1 / s3080; GSM5289473 / KO-running group mouse 2 / s3090; GSM5289474 / KO-running group mouse 3 / s3092; GSM5289475 / KO-running group mouse 4 / s3273
- **KO_Sed** (5): GSM5289476 / KO-sedentary group mouse 1 / s3035; GSM5289477 / KO-sedentary group mouse 2 / s3040; GSM5289478 / KO-sedentary group mouse 3 / s3091; GSM5289479 / KO-sedentary group mouse 4 / s3346; GSM5289480 / KO-sedentary group mouse 5 / s3386
- **WT_Run** (4): GSM5289464 / WT-running group mouse 1 / s3079; GSM5289465 / WT-running group mouse 2 / s3093; GSM5289466 / WT-running group mouse 3 / s3094; GSM5289467 / WT-running group mouse 4 / s3275
- **WT_Sed** (4): GSM5289468 / WT-sedentary group mouse 1 / s3036; GSM5289469 / WT-sedentary group mouse 2 / s3039; GSM5289470 / WT-sedentary group mouse 3 / s3078; GSM5289471 / WT-sedentary group mouse 4 / s3095

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE174211"], "assay": "FACS-sorted GFP+ newborn-neuron nuclei from hippocampus (RV-SYN-GTRgp), SmartSeq v4 RNA-seq (S2.5.p1, S4.19.p1)", "factors": {"genotype": ["WT", "F5KO"], "exercise": ["Sed", "Run (voluntary wheel)"]}, "sample_inclusion": "WT-sed n=4, WT-run n=4, F5KO-run n=4, F5KO-sed n=5; 6-week-old males (FIG15, S4.1.p2)", "primary_estimand": "Paper's DE estimand in this dataset is F5KO vs WT newborn neurons (459 DEGs) regardless of exercise intervention; the paper states the study was underpowered to detect an exercise effect and reports no exercise DEG count (S2.5.p2). The requested exercise estimand (Run vs Sed) is therefore exploratory.", "planned_contrasts": ["F5KO vs WT, pooled over exercise (S2.5.p2, FIG15c; paper: 459 DEGs)", "Run vs Sed: not reported by paper (S2.5.p2: underpowered)"], "paper_method": "DESeq2 v1.10.1 on gene-level counts (S4.21.p1); GSEA (S4.22.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.5, "source_locator": "S2.5.p2"}, "repeated_measure_unit": "none; one sample per mouse"}

reasoning: S2.5.p2: 459 genes DE between F5KO and WT newborn neurons (log2FC > |1.5|, p-value < 0.05); exercise effect not detected/reported. FIG15 gives group n. S4.27.p1 maps GSE174211 to the super-series.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE174211\\GSE174211_cw2002-WT_Sed_Run_SedSTAR_normalized_Gene_Counts.csv.gz", "owned": true, "checks": ["S4.27.p1 lists GSE174211 under GSE174212", "GEO contact C. Wrann (senior author)", "17 samples with WT/KO x Sed/Run = FIG15 n 4/4/4/5", "tissue/protocol: GFP+ sorted nuclei from hippocampus"], "accession": "GSE174211", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE174211\\GSE174211_metadata.csv"}

reasoning: Accession named in data availability; group sizes and protocol match FIG15.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 17, "n_metadata": 17, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\aligned\\aligned_metadata.csv", "columns": {"geno": {"alias_of": "characteristics_ch1.1.genotype", "recode": {"Wild-type": "WT", "Knock-out": "KO"}}, "ex": {"alias_of": "characteristics_ch1.3.running or sedentary", "recode": {"Sedentary group": "Sed", "Voluntery free wheel running group": "Run"}}, "grp": {"combine": ["geno", "ex"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\aligned\\design_metadata.csv", "sha256": "31de77927fe30875f287ede51327f5db1dee37e3ab996585423fbb9c142112a3", "levels": {"geno": {"KO": 9, "WT": 8}, "ex": {"Sed": 9, "Run": 8}, "grp": {"KO_Sed": 5, "WT_Run": 4, "WT_Sed": 4, "KO_Run": 4}}}}

reasoning: Matrix columns (s3079...) equal metadata description exactly (17/17). geno/ex from GEO characteristics; grp = geno_ex for the 4-cell model.

### matrix (valid, not_started)

final: {"source": "GSE174211_cw2002-...STAR_normalized_Gene_Counts.csv.gz", "paper_input": "gene-level counts into DESeq2 (S4.21.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\aligned\\aligned_matrix.csv", "sha256": "056e9a2aed5182ccdb83cc4d9afe9563fc1fc61d93409071809c00dededf9ccf", "n_features": 24982, "n_samples": 17, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1919008.0, "median": 8.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer; column sums vary 1.08M-8.52M (not library-size normalized); data_processing says 'Gene counts were quantified using STAR'; the FPKM (cufflinks) line refers to a separate output; 'normalized' in the filename is VIPER boilerplate (the sister DG file GSE179078 has the same processing text and is named STAR_Gene_Counts). Treated as raw STAR counts.

rejected alternatives: [{"value": "normalized counts", "reason_rejected": "library sizes differ ~8-fold; normalized counts would have near-equal column sums"}]

### design (valid, not_started)

final: {"analysis_type": "multi-group", "design_column": "grp", "contrasts": [{"name": "grp_WT_Run_vs_WT_Sed", "control": "WT_Sed", "treatment": "WT_Run", "role": "primary"}, {"name": "grp_KO_Run_vs_KO_Sed", "control": "KO_Sed", "treatment": "KO_Run", "role": "exploratory"}, {"name": "ex_Run_vs_Sed_adj_geno", "control": "Sed", "treatment": "Run", "role": "exploratory"}, {"name": "geno_KO_vs_WT", "control": "WT", "treatment": "KO", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: 2x2 genotype x exercise. The exercise effect in intact (WT) animals is the cleanest exercise estimand; KO Run vs Sed and the genotype-adjusted exercise main effect are exploratory. The paper's own contrast (KO vs WT pooled) is reproduced as secondary for comparison with the 459 DEGs. n=4-5 per cell.

rejected alternatives: [{"value": "pooled Run vs Sed ignoring genotype", "reason_rejected": "genotype has a large effect (S2.5.p2); ignoring it inflates residual variance"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "geno", "disposition": "model term in the exercise main-effect fit (design factor, not a nuisance covariate)"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 17, "n_columns": 4, "columns": ["Intercept", "grp_KO_Sed", "grp_WT_Run", "grp_WT_Sed"], "rank": 4, "full_rank": true, "residual_df": 13, "levels": {"grp": {"KO_Sed": 5, "WT_Run": 4, "WT_Sed": 4, "KO_Run": 4}}, "cells": [{"cell": ["KO_Run"], "n": 4}, {"cell": ["KO_Sed"], "n": 5}, {"cell": ["WT_Run"], "n": 4}, {"cell": ["WT_Sed"], "n": 4}], "min_cell_size": 4, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 17, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 17, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.genotype", "n_levels": 2, "status": "primary_nested_in_candidate", "crosstab" ... [2636 more characters]

reasoning: Independent mice, one sample each; no batch or sort date recorded in GEO. Genotype is a crossed design factor.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp (joint); ~ geno + ex; ~ geno", "paper_route": {"method": "DESeq2 v1.10.1", "status": "reproduced_approximately", "reason": "pydeseq2 instead of R DESeq2 1.10.1; paper's exact gene filtering is in a supplement not available here"}, "deviations": ["pydeseq2 implementation", "exercise contrasts not run by paper (exploratory)"]}

reasoning: Raw counts -> DESeq2, matching S4.21.p1.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.5, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.5, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: S2.5.p2: log2FC > |1.5|, p-value < 0.05 (raw p, as stated). Audit: BH padj < 0.05.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 17, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\results\\joint\\DEG_results_grp_WT_Run_vs_WT_Sed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\results\\joint\\DEG_results_grp_KO_Run_vs_KO_Sed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\results\\joint\\DEG_results_grp_KO_Sed_vs_WT_Sed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\results\\joint\\DEG_results_grp_WT_Run_vs_KO_Run.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\results\\joint\\DEG_results_grp_KO_Run_vs_WT_Sed.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\results\\joint\\DEG_results_grp_WT_Run_vs_KO_Sed.csv"], "counts": {"joint/grp_WT_Run_vs_WT_Sed": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "n_tested": 19182, "n_significant": 37, "n_up": 8, "n_down": 29, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 19182, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}, "joint/grp_KO_Run_vs_KO_Sed": {"applied": {"rule": "pvalue < 0 ... [1483 more characters]

reasoning: One ~grp model on all 17 samples; WT_Run vs WT_Sed is the requested exercise estimand; other cell contrasts exploratory.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "ex_Run_vs_Sed_adj_geno", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 17, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\aligned\\aligned_matrix.csv", "formula": "~ geno + ex", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\results\\ex_Run_vs_Sed_adj_geno\\DEG_results_Run_vs_Sed.csv"], "counts": {"ex_Run_vs_Sed_adj_geno": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "n_tested": 19182, "n_significant": 20, "n_up": 5, "n_down": 15, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 19182, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Exercise main effect across genotypes, ~ geno + ex.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "geno_KO_vs_WT", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 17, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\aligned\\aligned_matrix.csv", "formula": "~ geno", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174211\\results\\geno_KO_vs_WT\\DEG_results_KO_vs_WT.csv"], "counts": {"geno_KO_vs_WT": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "n_tested": 19182, "n_significant": 784, "n_up": 436, "n_down": 348, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16950, "n_significant": 5488, "n_up": 2809, "n_down": 2679, "deg_sanity": "ok"}}}}

reasoning: Paper's F5KO vs WT pooled comparison (S2.5.p2) for count comparison.

### study (valid, completed)

final: {"route": "exploratory", "caveats": ["Paper reports no exercise DEG set for newborn neurons and states the nuclear RNA-seq was underpowered for an exercise effect (S2.5.p2); exercise contrasts are exploratory.", "Paper threshold uses raw p < 0.05; counts under it are not FDR-controlled.", "FNDC5 gene-level counts are slightly HIGHER in F5KO (log2FC +0.36, padj 1.5e-4) in pooled KO vs WT; a knockout would be expected to lower it. Likely the KO allele deletes only some exons while nuclear (intronic) reads over the locus remain; genotype labels were not re-verified from the data. Paper states Fndc5 as DE only for the DG dataset (S2.5.p2)."], "results": {"joint/grp_WT_Run_vs_WT_Sed": {"n_deg": 37, "up": 8, "down": 29, "rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "audit_n": 0}, "joint/grp_KO_Run_vs_KO_Sed": {"n_deg": 26, "up": 14, "down": 12, "rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "audit_n": 0}, "joint/grp_KO_Sed_vs_WT_Sed": {"n_deg": 422, "up": 180, "down": 242, "rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "audit_n": 2012}, "joint/grp_WT_Run_vs_KO_Run": {"n_deg": 524, "up": 174, "down": 350, "rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "audit_n": 2681}, "joint/grp_KO_Run_vs_WT_Sed": {"n_deg": 361, "up": 181, "down": 180, "rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "audit_n": 1750}, "joint/grp_WT_Run_vs_KO_Sed": {"n_deg": 587, "up": 229, "down": 358, "rule": "pvalue < 0.05 and |log2FoldChange| > 1.5", "audit_n": 3236}, "ex_Run_vs_Sed_adj_g ... [473 more characters]

reasoning: Only the genotype contrast has a paper count; Fndc5 should drop in KO.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 17 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix file name says 'normalized'",
    "paper": "DESeq2 on gene-level counts",
    "data": "integer STAR counts with unequal library sizes",
    "disposition": "executable_without_change"
  },
  {
    "item": "exercise estimand",
    "paper": "no exercise DEG analysis reported (underpowered)",
    "data": "4 Run vs 4 Sed in WT, 4 vs 5 in KO",
    "disposition": "executable_as_exploratory"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 34417591 (Islam et al. 2021, irisin / FNDC5, PMC10317538)

Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`; validator 22 records, 0 errors. Final attempt is the third; earlier ones are in `_previous/`.

## What ran

| Case | Outcome | Why |
|---|---|---|
| GSE174211: newborn-neuron nuclei, WT/F5KO × Sed/Run (4/4/4/5 males) | **completed**, route `exploratory` | This is the only one of the three series with an exercise arm |
| GSE174210: APP/PS1 hippocampus, AAV8-irisin vs AAV8-GFP (5/5) | **refused at design** | There is no exercise arm. Irisin overexpression mimics exercise but is not exercise. The deposited matrix is DESeq2-normalized non-integer counts, and some gene IDs were converted to dates by Excel (`1-Mar` and similar) |
| GSE179078: dentate gyrus, F5KO vs WT (5/5) | **refused at design** | There is no exercise arm. The comparison is genotype only |

GSE174211 model and matrix:

- **Matrix:** raw STAR gene counts. The file is named "normalized", but every value is an integer and the library sizes range from 1.08M to 8.52M.
- **Model:** pydeseq2.
  - A joint `~ grp` model (grp = genotype_exercise, 4 cells) on all 17 samples.
  - Exercise main effect with `~ geno + ex`.
  - The paper's pooled genotype contrast with `~ geno`.
- **Sex check:** passed; all samples are male.
- **Enrichment:** not run. The paper's GSEA is for KO vs WT, not exercise.

## Threshold

The paper's rule (S2.5.p2) is "log2FC > |1.5|, p-value < 0.05": raw p < 0.05 and |log2FC| > 1.5. I applied it exactly. As an audit I also counted genes with BH padj < 0.05.

## DEG counts vs the paper

| Table | Ours (paper rule) | up / down | Audit padj<0.05 | Paper |
|---|---|---|---|---|
| joint/grp_WT_Run_vs_WT_Sed (exercise in WT, primary for the request) | 37 | 8 / 29 | 0 | not reported ("underpowered", S2.5.p2) |
| joint/grp_KO_Run_vs_KO_Sed (exercise in KO) | 26 | 14 / 12 | 0 | not reported |
| ex_Run_vs_Sed_adj_geno (~geno+ex) | 20 | 5 / 15 | 0 | not reported |
| geno_KO_vs_WT (pooled; the paper's contrast, secondary) | 784 | 436 / 348 | 5488 | 459 |
| joint KO_Sed vs WT_Sed, WT_Run vs KO_Run, and the cross-cell contrasts | 422 / 524 / 361 / 587 | — | — | — |

Conclusion on exercise: in this dataset, voluntary running has no FDR-significant effect on newborn-neuron nuclear transcripts in WT or KO mice. This agrees with the paper's statement that the dataset was underpowered for an exercise effect. The 20–37 genes that pass the raw-p rule are ... [1622 more characters]
