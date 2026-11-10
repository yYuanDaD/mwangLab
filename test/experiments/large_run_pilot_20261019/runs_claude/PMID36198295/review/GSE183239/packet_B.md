# Review packet B (the analysis' decisions): GSE183239

## Mechanical flags

- **other_rule_matches_paper**: {"table": "scWAT/grp_HFDtr_vs_HFDsed_tissue-scWAT", "paper": 132, "applied": 85, "applied_rule": "padj < 0.05", "closest_rule": "padj<0.1", "closest_n": 133, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pairing_key_candidate**: {"key": "key without the tissue level", "across": "tissue", "pairs_or_sets": 20, "samples_linked": 40, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scWAT/grp_CDtr_vs_CDsed_tissue-scWAT | 3 | 2 | padj < 0.05 | 2 | 2 | 0 | 5 | 191 | 77 | 9 | 52 | 0.107 | 0.059 |
| scWAT/grp_HFDtr_vs_HFDsed_tissue-scWAT | 132 | 85 | padj < 0.05 | 85 | 79 | 32 | 133 | 400 | 175 | 44 | 173 | 0.087 | 0.124 |
| scWAT/grp_HFDsed_vs_CDsed_tissue-scWAT | 492 | 401 | padj < 0.05 | 401 | 331 | 95 | 536 | 759 | 437 | 104 | 450 | 0.062 | 0.235 |
| vWAT/grp_CDtr_vs_CDsed_tissue-vWAT | 47 | 54 | padj < 0.05 | 54 | 37 | 7 | 75 | 335 | 116 | 13 | 150 | 0.104 | 0.095 |
| vWAT/grp_HFDtr_vs_HFDsed_tissue-vWAT | 205 | 206 | padj < 0.05 | 206 | 142 | 33 | 299 | 594 | 209 | 35 | 307 | 0.076 | 0.168 |
| vWAT/grp_HFDsed_vs_CDsed_tissue-vWAT | 478 | 458 | padj < 0.05 | 458 | 281 | 89 | 598 | 838 | 323 | 91 | 507 | 0.067 | 0.237 |
| SkM/grp_CDtr_vs_CDsed_tissue-SkM | 92 | 109 | padj < 0.05 | 109 | 35 | 9 | 151 | 300 | 58 | 10 | 155 | 0.09 | 0.138 |
| SkM/grp_HFDtr_vs_HFDsed_tissue-SkM | 235 | 259 | padj < 0.05 | 259 | 121 | 21 | 350 | 544 | 157 | 21 | 289 | 0.059 | 0.25 |
| SkM/grp_HFDsed_vs_CDsed_tissue-SkM | 0 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 89 | 17 | 2 | 25 | 0.105 | 0.041 |

## Samples per design level

### `grp`
- **CDsed** (15): GSM5553737 / Bulk sedentary standard (chow) diet rep1; GSM5553738 / Bulk sedentary standard (chow) diet rep2; GSM5553739 / Bulk sedentary standard (chow) diet rep3; GSM5553740 / Bulk sedentary standard (chow) diet rep4; GSM5553741 / Bulk sedentary standard (chow) diet rep5; GSM5553757 / Bulk sedentary standard (chow) diet rep1; GSM5553758 / Bulk sedentary standard (chow) diet rep2; GSM5553759 / Bulk sedentary standard (chow) diet rep3; GSM5553760 / Bulk sedentary standard (chow) diet rep4; GSM5553761 / Bulk sedentary standard (chow) diet rep5; GSM5553777 / Bulk sedentary standard (chow) diet rep1; GSM5553778 / Bulk sedentary standard (chow) diet rep2; GSM5553779 / Bulk sedentary standard (chow) diet rep3; GSM5553780 / Bulk sedentary standard (chow) diet rep4; GSM5553781 / Bulk sedentary standard (chow) diet rep5
- **CDtr** (15): GSM5553742 / Bulk training standard (chow) diet rep1 ; GSM5553743 / Bulk training standard (chow) diet rep2 ; GSM5553744 / Bulk training standard (chow) diet rep3 ; GSM5553745 / Bulk training standard (chow) diet rep4 ; GSM5553746 / Bulk training standard (chow) diet rep5 ; GSM5553762 / Bulk training standard (chow) diet rep1 ; GSM5553763 / Bulk training standard (chow) diet rep2 ; GSM5553764 / Bulk training standard (chow) diet rep3 ; GSM5553765 / Bulk training standard (chow) diet rep4 ; GSM5553766 / Bulk training standard (chow) diet rep5 ; GSM5553782 / Bulk training standard (chow) diet rep1 ; GSM5553783 / Bulk training standard (chow) diet rep2 ; GSM5553784 / Bulk training standard (chow) diet rep3 ; GSM5553785 / Bulk training standard (chow) diet rep4 ; GSM5553786 / Bulk training standard (chow) diet rep5 
- **HFDsed** (15): GSM5553747 / Bulk sedentary high-fat diet rep1 [SH3.s; GSM5553748 / Bulk sedentary high-fat diet rep2 [SH4.s; GSM5553749 / Bulk sedentary high-fat diet rep3 [SH7.s; GSM5553750 / Bulk sedentary high-fat diet rep4 [SH8.s; GSM5553751 / Bulk sedentary high-fat diet rep5 [SH12.; GSM5553767 / Bulk sedentary high-fat diet rep1 [SH3.v; GSM5553768 / Bulk sedentary high-fat diet rep2 [SH4.v; GSM5553769 / Bulk sedentary high-fat diet rep3 [SH7.v; GSM5553770 / Bulk sedentary high-fat diet rep4 [SH8.v; GSM5553771 / Bulk sedentary high-fat diet rep5 [SH12.; GSM5553787 / Bulk sedentary high-fat diet rep1 [SH3.T; GSM5553788 / Bulk sedentary high-fat diet rep2 [SH4.T; GSM5553789 / Bulk sedentary high-fat diet rep3 [SH7.T; GSM5553790 / Bulk sedentary high-fat diet rep4 [SH8.T; GSM5553791 / Bulk sedentary high-fat diet rep5 [SH12.
- **HFDtr** (15): GSM5553752 / Bulk training high-fat diet rep1 [TH5.sc; GSM5553753 / Bulk training high-fat diet rep2 [TH6.sc; GSM5553754 / Bulk training high-fat diet rep3 [TH11.s; GSM5553755 / Bulk training high-fat diet rep4 [TH10.s; GSM5553756 / Bulk training high-fat diet rep5 [TH17.s; GSM5553772 / Bulk training high-fat diet rep1 [TH5.vW; GSM5553773 / Bulk training high-fat diet rep2 [TH6.vW; GSM5553774 / Bulk training high-fat diet rep3 [TH11.v; GSM5553775 / Bulk training high-fat diet rep4 [TH10.v; GSM5553776 / Bulk training high-fat diet rep5 [TH17.v; GSM5553792 / Bulk training high-fat diet rep1 [TH5.Tr; GSM5553793 / Bulk training high-fat diet rep2 [TH6.Tr; GSM5553794 / Bulk training high-fat diet rep3 [TH11.T; GSM5553795 / Bulk training high-fat diet rep4 [TH10.T; GSM5553796 / Bulk training high-fat diet rep5 [TH17.T

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE183239"], "superseries": "GSE183290 (bulk GSE183239 + single-cell GSE183288)", "assay": "bulk 3' DGE mRNA-seq (UMI-deduplicated, Salmon 0.14.2 + tximport, Ensembl 98), scWAT, vWAT, triceps (SkM)", "factors": {"diet": ["standard chow (10% fat)", "HFD (60% fat)"], "exercise": ["sedentary", "voluntary wheel running training"], "tissue": ["scWAT", "vWAT", "SkM (triceps)"]}, "sample_inclusion": "5 male C57BL/6N mice per group per tissue (S4.3.2.p1); 4 groups x 3 tissues = 60 libraries; same mice across tissues", "primary_estimand": "Per tissue, effect of 3 weeks of voluntary wheel-running training on tissue gene expression: 'training' (train chow vs sed chow) and 'rescue' (train HFD vs sed HFD); 'obesity' (sed HFD vs sed chow) is the paper's third, diet-only comparison", "planned_contrasts": ["training: train std vs sed std, per tissue (S2.2.p1, TAB1: scWAT 3, vWAT 47, SkM 92)", "rescue: train HFD vs sed HFD, per tissue (S2.2.p1, TAB1: scWAT 132, vWAT 205, SkM 235)", "obesity: sed HFD vs sed std, per tissue (S2.2.p1, TAB1: scWAT 492, vWAT 478, SkM 0)"], "repeated_measure_unit": "none within a tissue (each tissue analysed separately; one library per mouse per tissue)", "normalization": "DESeq2 size factors; per tissue keep genes with count > 10 in all samples (S4.4.1.1.p1)", "paper_method": "DESeq2 per tissue, IHW-adjusted p values, ashr-shrunk fold changes (S4.4.1.1.p1)", "paper_threshold": {"metric": "padj", "adjustment": "IHW", "cutoff": 0.05, "effect_metric" ... [312 more characters]

reasoning: S4.1.3.p1 and TAB2 name GSE183239 as the bulk mRNA-seq; GSE183288 is the single-cell series and is not this case. S4.3.1.p1 describes the 2x2 diet x exercise design; S4.3.2.p1 says 5 mice per group were sequenced for the three tissues. S2.2.p1 defines the three pairwise comparisons; S4.4.1.1.p1 gives the per-tissue filter, DESeq2, IHW and ashr, and adjusted p < 0.05 with no fold-change rule. TAB1 gives the counts.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE183239\\GSE183239_Bulk_gene_count_matrix.txt.gz", "owned": true, "checks": ["paper S4.1.3.p1/TAB2 name GSE183239 for bulk mRNA-seq", "60 GEO samples = 3 tissues x 4 groups x 5, matching S4.3.2.p1", "data_processing matches S4.4.1.1.p1 (UMI dedup, Salmon 0.14.2, Ensembl 98, tximport)", "series_id lists the SuperSeries GSE183290 named in the paper"], "accession": "GSE183239", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE183239\\GSE183239_metadata.csv"}

reasoning: Accession, sample count, processing text and SuperSeries all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 60, "n_metadata": 60, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\aligned\\aligned_metadata.csv", "columns": {"diet": {"source": "characteristics_ch1.3.treatment", "regex": "^6-week (chow|high-fat)-diet", "recode": {"chow": "CD", "high-fat": "HFD"}}, "ex": {"source": "characteristics_ch1.3.treatment", "regex": "3-week (sedentary|training) interventions", "recode": {"sedentary": "SED", "training": "TR"}}, "tissue": {"source": "source_name_ch1", "regex": "^(subcutaneous|visceral|triceps)", "recode": {"subcutaneous": "scWAT", "visceral": "vWAT", "triceps": "SkM"}}, "grp": {"combine": ["diet", "ex"], "separator": "_", "of": "recoded values", "recode": {"CD_SED": "CDsed", "CD_TR": "CDtr", "HFD_SED": "HFDsed", "HFD_TR": "HFDtr"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\aligned\\design_metadata.csv", "sha256": "959123ffb81528c46944606f3b0c4985ce2d0dc216d0d3d14f71abb8b2220e54", "levels": {"diet": {"CD": 30, "HFD": 30}, "ex": {"SED": 30, "TR": 30}, "tissue": {"scWAT": 20, "vWAT": 20, "SkM": 20}, "grp": {"CDsed": 15, "CDtr": 15, "HFDsed": 15, "HFDtr": 15}}}}

reasoning: The matrix holds two column kinds per library (.intCt integer counts and .l2cpm log2CPM); matrix_column_pattern keeps only .intCt and reduces names such as 'SC3.vWAT.d316020.intCt' to 'SC3.vWAT'. The metadata title carries the same label in brackets ('[SC3.vWAT]', one with a trailing space '[TC14.vWAT ]'), extracted by key_patterns; exact match on that key. Diet and exercise come from characteristics treatment, tissue from source_name. The label prefix (SC/TC/SH/TH = sed chow / train chow / sed HFD / train HFD) agrees with the treatment field for every row (checked by eye before the run).

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts (tximport gene-level counts from Salmon, UMI-deduplicated; deposited as integers)", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\aligned\\aligned_matrix.csv", "sha256": "4ed2f88477ce6e1976b966fc83b8054c96dbf8055d74e9a379a935a9fc8ce963", "n_features": 54352, "n_samples": 60, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 60651.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All .intCt values are integers (min 0, max 60651, library sums 0.51-0.74 M, typical of 3' DGE UMI counts). data_processing: Salmon -> tximport, 'Matrix table with raw gene counts and log2CPM values'. Paper ran DESeq2 on these counts (S4.4.1.1.p1). The .l2cpm columns are dropped.

### design (valid, not_started)

final: {"analysis_type": "multi-group (4 diet x exercise cells) per tissue, planned pairwise contrasts from one model per tissue", "design_column": "grp", "contrasts": [{"name": "training", "control": "CDsed", "treatment": "CDtr", "role": "primary"}, {"name": "rescue", "control": "HFDsed", "treatment": "HFDtr", "role": "primary"}, {"name": "obesity", "control": "CDsed", "treatment": "HFDsed", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\suitability\\suitability.md", "n_comparisons": 18, "n_analyzable": 18}}

reasoning: S2.2.p1 defines exactly three pairwise comparisons per tissue; tissues are analysed separately (S4.4.1.1.p1 'for each tissue'), so tissue is a stratum. The 2x2 cells are coded as one 4-level factor grp so the comparisons are simple cell contrasts from one DESeq2 fit per tissue, as in the paper; the diet x exercise interaction is not a paper estimand and is not tested. Training and rescue are the exercise estimands (primary); obesity is diet-only and kept as secondary for comparison with TAB1. Rejected: pooling diets for a main exercise effect (not the paper's estimand); two-factor ~diet+ex additive model (paper compares cells, and an additive model would assume no interaction).

rejected alternatives: [{"value": "~ diet + ex main effects", "reason_rejected": "paper reports within-diet cell comparisons, not a main effect"}, {"value": "all 60 libraries in one model with tissue", "reason_rejected": "paper analyses each tissue separately; tissue effects dwarf treatment"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 60, "n_columns": 4, "columns": ["Intercept", "grp_CDtr", "grp_HFDsed", "grp_HFDtr"], "rank": 4, "full_rank": true, "residual_df": 56, "levels": {"grp": {"CDsed": 15, "CDtr": 15, "HFDsed": 15, "HFDtr": 15}}, "cells": [{"cell": ["CDsed"], "n": 15}, {"cell": ["CDtr"], "n": 15}, {"cell": ["HFDsed"], "n": 15}, {"cell": ["HFDtr"], "n": 15}], "min_cell_size": 15, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 60, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 60, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 3, "status": "crossed", "crosstab": {"CDsed": {"subcutaneous white adipose tissue": 5, "triceps": 5, "visceral white adipose tissue": 5}, "CDtr": {"subcutaneous white adipose tissue": 5, "triceps": 5, "visceral white adipose tissue": 5}, "HFDsed": {"subcutaneous white adipose tissue": 5, "triceps": 5, "visceral white adipose tissue": 5}, "HFDtr": {"subcutaneous white adipose tissue": 5, "triceps": 5, "visceral white adipose tissue": 5}}}, {"column": "organism_ch ... [4048 more characters]

reasoning: Within one tissue each mouse contributes one library, so there is no repeated unit. The same mice appear in all three tissues, but tissues are never compared. Library prep used two sub-pools (S4.3.2.p1) but the pool assignment is not deposited; the paper reports batch was not a major driver (S2.1.p1) and fitted no batch term. No covariate is added.

### method (valid, not_started)

final: {"matrix_type": "estimated counts (tximport gene-level counts from Salmon, UMI-deduplicated; deposited as integers)", "method": "DESeq2 (pydeseq2 Wald, one fit per tissue on all 20 samples, ~ grp)", "formula": "~ grp", "paper_route": {"method": "DESeq2 + IHW p-value adjustment + ashr LFC shrinkage", "status": "blocked", "reason": "IHW (and ashr) are R/Bioconductor-only and not available in the pydeseq2 executor; BH adjustment is used instead. ashr changes only fold-change estimates, not significance, so it does not affect DEG counts under the paper's rule (no effect cutoff)."}, "deviations": ["BH instead of IHW adjusted p values", "no ashr shrinkage (reported log2FC are MLE)", "pydeseq2 instead of R DESeq2"], "rounding_documented": true, "rounding_note": "deposited .intCt values are already integers (rounded tximport counts, 100% integer); no further rounding applied", "filter": "per tissue, keep genes with count > 10 (>= 11, integer counts) in all 20 samples of that tissue (S4.4.1.1.p1)"}

reasoning: Integer estimated counts support DESeq2, the paper's method. The paper's low-count rule is applied per tissue execution with filter_low_counts {min_count: 11, min_samples: 20}. IHW is the only part of the route that changes significance calls and cannot be reproduced here, so this is a declared deviation.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "deviation_note": "Paper's adjusted p < 0.05 is IHW-adjusted; here the same cutoff is applied to BH-adjusted p values. IHW typically gives somewhat more discoveries than BH."}

reasoning: S4.4.1.1.p1: 'significant DEGs at an adjusted p value cutoff of 0.05'; no fold-change rule.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "scWAT", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\scWAT\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\scWAT\\DEG_results_grp_CDtr_vs_CDsed_tissue-scWAT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\scWAT\\DEG_results_grp_HFDtr_vs_HFDsed_tissue-scWAT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\scWAT\\DEG_results_grp_HFDsed_vs_CDsed_tissue-scWAT.csv"], "counts": {"scWAT/grp_CDtr_vs_CDsed_tissue-scWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 3224, "n_significant": 2, "n_up": 0, "n_down": 2, "deg_sanity": "ok"}}, "scWAT/grp_HFDtr_vs_HFDsed_tissue-scWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 3224, "n_significant": 85, "n_up": 53, "n_down": 32, "deg_sanity": "ok"}}, "scWAT/grp_HFDsed_vs_CDsed_tissue-scWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 3098, "n_significant": 401, "n_up": 214, "n_down": 187, "deg_sanity": "ok"}}}}

reasoning: one DESeq2 fit on the 20 scWAT libraries; training, rescue, obesity contrasts

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "vWAT", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\vWAT\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\vWAT\\DEG_results_grp_CDtr_vs_CDsed_tissue-vWAT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\vWAT\\DEG_results_grp_HFDtr_vs_HFDsed_tissue-vWAT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\vWAT\\DEG_results_grp_HFDsed_vs_CDsed_tissue-vWAT.csv"], "counts": {"vWAT/grp_CDtr_vs_CDsed_tissue-vWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 2163, "n_significant": 54, "n_up": 21, "n_down": 33, "deg_sanity": "ok"}}, "vWAT/grp_HFDtr_vs_HFDsed_tissue-vWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 3123, "n_significant": 206, "n_up": 83, "n_down": 123, "deg_sanity": "ok"}}, "vWAT/grp_HFDsed_vs_CDsed_tissue-vWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 3054, "n_significant": 458, "n_up": 212, "n_down": 246, "deg_sanity": "ok"}}}}

reasoning: one DESeq2 fit on the 20 vWAT libraries

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "SkM", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\SkM\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\SkM\\DEG_results_grp_CDtr_vs_CDsed_tissue-SkM.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\SkM\\DEG_results_grp_HFDtr_vs_HFDsed_tissue-SkM.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\SkM\\DEG_results_grp_HFDsed_vs_CDsed_tissue-SkM.csv"], "counts": {"SkM/grp_CDtr_vs_CDsed_tissue-SkM": {"applied": {"rule": "padj < 0.05", "n_tested": 1333, "n_significant": 109, "n_up": 80, "n_down": 29, "deg_sanity": "ok"}}, "SkM/grp_HFDtr_vs_HFDsed_tissue-SkM": {"applied": {"rule": "padj < 0.05", "n_tested": 1629, "n_significant": 259, "n_up": 164, "n_down": 95, "deg_sanity": "ok"}}, "SkM/grp_HFDsed_vs_CDsed_tissue-SkM": {"applied": {"rule": "padj < 0.05", "n_tested": 2178, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: one DESeq2 fit on the 20 triceps libraries

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "scWAT_sumfilter", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\scWAT_sumfilter\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\scWAT_sumfilter\\DEG_results_grp_CDtr_vs_CDsed_tissue-scWAT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\scWAT_sumfilter\\DEG_results_grp_HFDtr_vs_HFDsed_tissue-scWAT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\scWAT_sumfilter\\DEG_results_grp_HFDsed_vs_CDsed_tissue-scWAT.csv"], "counts": {"scWAT_sumfilter/grp_CDtr_vs_CDsed_tissue-scWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 14630, "n_significant": 3, "n_up": 3, "n_down": 0, "deg_sanity": "ok"}}, "scWAT_sumfilter/grp_HFDtr_vs_HFDsed_tissue-scWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 7258, "n_significant": 139, "n_up": 73, "n_down": 66, "deg_sanity": "ok"}}, "scWAT_sumfilter/grp_HFDsed_vs_CDsed_tissue-scWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 10661, "n_significant": 525, "n_up": 290, "n_down": 235, "deg_sanity": "ok"}}}}

reasoning: alternative reading of S4.4.1.1.p1: total count across the tissue's 20 samples > 10 (mean >= 0.55, the DESeq2 rowSums idiom). The literal 'every sample > 10' rule removes the paper's named DEGs Dbp, Tef, Nr1d2, Per3, Thbs1, Cdkn1a, so the paper cannot have applied it literally.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "vWAT_sumfilter", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\vWAT_sumfilter\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\vWAT_sumfilter\\DEG_results_grp_CDtr_vs_CDsed_tissue-vWAT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\vWAT_sumfilter\\DEG_results_grp_HFDtr_vs_HFDsed_tissue-vWAT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\vWAT_sumfilter\\DEG_results_grp_HFDsed_vs_CDsed_tissue-vWAT.csv"], "counts": {"vWAT_sumfilter/grp_CDtr_vs_CDsed_tissue-vWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 5607, "n_significant": 51, "n_up": 22, "n_down": 29, "deg_sanity": "ok"}}, "vWAT_sumfilter/grp_HFDtr_vs_HFDsed_tissue-vWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 6179, "n_significant": 224, "n_up": 85, "n_down": 139, "deg_sanity": "ok"}}, "vWAT_sumfilter/grp_HFDsed_vs_CDsed_tissue-vWAT": {"applied": {"rule": "padj < 0.05", "n_tested": 8752, "n_significant": 506, "n_up": 255, "n_down": 251, "deg_sanity": "ok"}}}}

reasoning: as scWAT_sumfilter

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "SkM_sumfilter", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\SkM_sumfilter\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\SkM_sumfilter\\DEG_results_grp_CDtr_vs_CDsed_tissue-SkM.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\SkM_sumfilter\\DEG_results_grp_HFDtr_vs_HFDsed_tissue-SkM.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36198295\\GSE183239\\results\\SkM_sumfilter\\DEG_results_grp_HFDsed_vs_CDsed_tissue-SkM.csv"], "counts": {"SkM_sumfilter/grp_CDtr_vs_CDsed_tissue-SkM": {"applied": {"rule": "padj < 0.05", "n_tested": 11989, "n_significant": 24, "n_up": 11, "n_down": 13, "deg_sanity": "ok"}}, "SkM_sumfilter/grp_HFDtr_vs_HFDsed_tissue-SkM": {"applied": {"rule": "padj < 0.05", "n_tested": 3622, "n_significant": 244, "n_up": 149, "n_down": 95, "deg_sanity": "ok"}}, "SkM_sumfilter/grp_HFDsed_vs_CDsed_tissue-SkM": {"applied": {"rule": "padj < 0.05", "n_tested": 11989, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: as scWAT_sumfilter

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["IHW replaced by BH; counts expected to be lower than the paper's where IHW gains power", "No ashr shrinkage; fold-change magnitudes are unshrunk MLE", "The paper's literal filter (count > 10 in every sample of the tissue) keeps only 2.2k-3.5k genes and removes the paper's named adipose DEGs Dbp, Tef, Nr1d2, Per3, Thbs1 and Cdkn1a, so the paper cannot have applied it literally. Under the sensitivity reading (total count > 10 across the tissue's samples) all of them are significant in the paper's direction (circadian genes up, Thbs1/Cdkn1a down with rescue in scWAT and vWAT, and with training in vWAT), and adipose counts are closer to Table 1; SkM training falls to 24 vs the paper's 92 under that reading (BH over ~12k genes vs IHW).", "Sparc is down with training/rescue as the paper says, but not significant in scWAT rescue (padj 0.21 / 0.31)."], "results": {"scWAT/grp_CDtr_vs_CDsed_tissue-scWAT": {"n_deg": 2, "up": 0, "down": 2, "rule": "padj < 0.05"}, "scWAT/grp_HFDtr_vs_HFDsed_tissue-scWAT": {"n_deg": 85, "up": 53, "down": 32, "rule": "padj < 0.05"}, "scWAT/grp_HFDsed_vs_CDsed_tissue-scWAT": {"n_deg": 401, "up": 214, "down": 187, "rule": "padj < 0.05"}, "vWAT/grp_CDtr_vs_CDsed_tissue-vWAT": {"n_deg": 54, "up": 21, "down": 33, "rule": "padj < 0.05"}, "vWAT/grp_HFDtr_vs_HFDsed_tissue-vWAT": {"n_deg": 206, "up": 83, "down": 123, "rule": "padj < 0.05"}, "vWAT/grp_HFDsed_vs_CDsed_tissue-vWAT": {"n_deg": 458, "up": 212, "down": 246, "ru ... [5526 more characters]

reasoning: Paper counts from TAB1 (up + down per tissue x comparison). Named genes from S2.2.p2 and S2.2.p3: circadian regulators up and ECM genes down with training/rescue in adipose depots (which depot/comparison each gene reached significance in is not itemised in the text); Pdk4 and Asb2 among SkM rescue/training DEGs (direction for Pdk4/Asb2 not stated explicitly); Cdkn1a down by rescue in scWAT and vWAT.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 60 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "p-value adjustment",
    "paper": "IHW",
    "data": "executor offers BH only",
    "disposition": "declared_deviation"
  },
  {
    "item": "GEO strain",
    "paper": "C57BL/6N (S4.2.p1)",
    "data": "characteristics strain 'C57BL/6JN'",
    "disposition": "executable_without_change"
  },
  {
    "item": "age",
    "paper": "6-week-old at start, 4 weeks of intervention + 3 weeks pre-diet (S4.3.1.p1)",
    "data": "GEO '12-week old', '6-week diet, 3-week exercise'",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID36198295 / GSE183239

## What ran
- Case spec route (`tools.case_runner execute case_spec.json`): status completed, decision contract validator 15 records, 0 errors.
- GSE183239 is the paper's bulk 3' DGE mRNA-seq (S4.1.3.p1, TAB2). GSE183288 is the single-cell series and was not analysed. 60 libraries: 3 tissues (scWAT, vWAT, triceps/SkM) x 4 groups (chow/HFD x sedentary/wheel training) x 5 male mice.
- Matrix: `GSE183239_Bulk_gene_count_matrix.txt.gz`. Kept the `.intCt` columns (100% integer tximport counts) and dropped the `.l2cpm` columns. Alignment was an exact match on the bracketed title label (`SC3.vWAT`, ...): 60/60 aligned.
- Design: a 4-level `grp` factor (CDsed, CDtr, HFDsed, HFDtr), with tissue as a stratum. One pydeseq2 fit `~ grp` per tissue on its 20 samples. Contrasts:
  - training = CDtr vs CDsed (primary)
  - rescue = HFDtr vs HFDsed (primary)
  - obesity = HFDsed vs CDsed (secondary, diet only)
- Covariance: not required. Each mouse gives one library per tissue, and tissues are never compared. The library-prep subpool is not deposited, and the paper reports batch was not a driver (S2.1.p1).
- Threshold: paper rule, adjusted p < 0.05 with no fold-change cutoff (S4.4.1.1.p1), applied to BH-adjusted p values (`paper_on_deviation_route`).
- Primary low-count filter: the paper's literal rule, count > 10 in all 20 samples of the tissue (min_count 11, min_samples 20). A sensitivity run (`*_sumfilter`) keeps genes whose total count across the tissue is > 10 (mean >= 0.55).
- No enrichment was run. The paper's GO results come from Metascape on DEG lists, and the request asked for DE.

## DEG counts vs paper Table 1 (adjusted p < 0.05)
| tissue | contrast | paper | ours, literal filter (primary) | ours, sum filter (sensitivity) |
|---|---|---|---|---|
| scWAT | training | 3 | 2 | 3 |
| scWAT | rescue | 132 | 85 | 139 |
| scWAT | obesity | 492 | 401 | 525 |
| vWAT | training | 47 | 54 | 51 |
| vWAT | rescue | 205 | 206 | 224 |
| vWAT | obesity | 478 | 458 | 506 |
| SkM | training | 92 | 109 | 24 |
| SkM | rescue | 235 | 259 | 244 |
| SkM | obesity | 0 | 0 | 0 |

Genes tested: literal filter 3225 / 3538 / 2178; sum filter 14648 / 14805 / 11991 (scWAT / vWAT / SkM).

Named genes:
- Literal filter: the filter removes Dbp, Tef, Nr1d2, Per3, Thbs1 and Cdkn1a.
- Sum filter: all of them are significant in the paper's direction in scWAT and vWAT rescue. Dbp log2FC is about +2.9 / +2.6, Thbs1 about -2.3 / -2.1, and Cdkn1a about -2.1 / -2.4. ... [1586 more characters]
