# Review packet B (the analysis' decisions): GSE207992

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.2.treatment level", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 7, "samples_linked": 14, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_KO_SVE_vs_KO_nSVE | 223 | 329 | padj < 0.05 | 329 | 273 | 183 | 714 | 2774 | 1952 | 1211 | 1125 | 0.2 | 0.107 |
| joint/grp_WT_SVE_vs_WT_nSVE | 795 | 772 | padj < 0.05 | 772 | 390 | 95 | 1103 | 2343 | 884 | 330 | 1152 | 0.151 | 0.09 |
| joint/grp_KO_nSVE_vs_WT_nSVE | 307 | 457 | padj < 0.05 | 457 | 364 | 239 | 766 | 2696 | 1723 | 1150 | 1177 | 0.19 | 0.104 |
| joint/grp_KO_SVE_vs_WT_nSVE | 557 | 557 | padj < 0.05 | 557 | 378 | 149 | 836 | 2488 | 1430 | 752 | 1087 | 0.156 | 0.096 |

## Samples per design level

### `grp`
- **KO_SVE** (3): GSM6329641 / MUT SVE 1 / AH14; GSM6329642 / MUT SVE 2 / AH15; GSM6329643 / MUT SVE 3 / AH16
- **KO_nSVE** (3): GSM6329638 / MUT non-SVE 1 / AH9; GSM6329639 / MUT non-SVE 2 / AH10; GSM6329640 / MUT non-SVE 3 / AH11
- **WT_SVE** (4): GSM6329634 / WT SVE 1 / AH5; GSM6329635 / WT SVE 2 / AH6; GSM6329636 / WT SVE 3 / AH7; GSM6329637 / WT SVE 4 / AH8
- **WT_nSVE** (4): GSM6329630 / WT non-SVE 1 / AH1; GSM6329631 / WT non-SVE 2 / AH2; GSM6329632 / WT non-SVE 3 / AH3; GSM6329633 / WT non-SVE 4 / AH4

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE207992"], "assay": "bulk RNA-seq (Lexogen Sense total RNA, paired-end HiSeq 4000) of laser-captured SCN, adult male mice (S4.4.2.p1, S4.3.p1)", "factors": {"genotype": ["Vipr2+/+ (WT)", "Vipr2-/- (KO)"], "exercise": ["nSVE (free wheel access)", "SVE (scheduled 6h/24h wheel access)"]}, "sample_inclusion": "WT nSVE CT14 n=4, WT SVE ZT14/CT22 n=4, KO nSVE CT14 n=3, KO SVE ZT14/CT14 n=3 (S4.4.2.p1, S2.2.p1, FIG4); only entrained/rhythmic animals used (S4.4.p2)", "primary_estimand": "Effect of scheduled voluntary exercise (SVE vs nSVE) on the SCN transcriptome, within genotype; the KO comparison is matched for circadian time (CT14), the WT comparison is not (SVE ZT14/CT22 vs nSVE CT14) and the paper states its DEGs mix circadian phase and exercise (S2.4.p1, S2.5.p1)", "planned_contrasts": ["KO SVE vs KO nSVE (S2.5.p1; paper: 223 DEGs, 105 up / 118 down)", "WT SVE vs WT nSVE (S2.4.p1; paper: 795 DEGs, 556 up / 239 down; confounded with circadian time)", "KO nSVE vs WT nSVE (S2.3.p1; genotype; paper: 307 DEGs, 158 up / 149 down)", "KO SVE vs WT nSVE (S2.6.p1; paper: 557 DEGs, 246 up / 311 down)"], "repeated_measure_unit": "none: one SCN sample per animal", "normalization": "DESeq2 size factors (S4.4.2.p1)", "paper_method": "DESeq2 pairwise analyses with default independent filtering and Cook's distance outlier handling; BH FDR (S4.4.2.p1-p2)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2. ... [260 more characters]

reasoning: Four RNA-seq groups (S2.2.p1, S4.4.2.p1). Exercise question is answered by SVE vs nSVE within genotype; the paper treats the KO comparison as the clean exercise effect (both CT14) and flags that the WT comparison also contains an 8h circadian-phase difference (S2.4.p1 last sentence). Genotype contrasts are reported in the paper and run here as secondary comparisons for count comparison. Threshold FDR < 0.05 with no fold-change rule (S2.2.p2, S4.4.2.p2).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992_raw_counts_recovered.csv", "owned": true, "checks": ["S2.2.p2 and S10.p1 name GSE207992", "14 GEO samples = 4+4+3+3 as in S4.4.2.p1", "GEO source SCN, Mus musculus, genotype and treatment fields match the paper's groups", "matrix columns carry the same AH labels as GEO description"], "accession": "GSE207992", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE207992\\GSE207992_metadata.csv"}

reasoning: Paper data availability (S10.p1) names GSE207992; group sizes and labels match exactly.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 14, "n_metadata": 14, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\aligned\\aligned_metadata.csv", "columns": {"geno": {"alias_of": "characteristics_ch1.1.genotype", "recode": {"wildtype": "WT", "Vipr2-/-": "KO"}}, "ex": {"alias_of": "characteristics_ch1.2.treatment", "recode": {"non-SVE": "nSVE", "SVE": "SVE"}}, "grp": {"combine": ["geno", "ex"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\aligned\\design_metadata.csv", "sha256": "332c95e193cfb0ce378a9fc91ba3e50ccc6f41a1946845efd325470b6c2f9a60", "levels": {"geno": {"WT": 8, "KO": 6}, "ex": {"nSVE": 7, "SVE": 7}, "grp": {"WT_nSVE": 4, "WT_SVE": 4, "KO_nSVE": 3, "KO_SVE": 3}}}}

reasoning: The prep script renamed matrix columns from 'KO SVE AH14 Gene counts' to the AH label, which equals GEO 'description' (AH1..AH16). The genotype/treatment words embedded in the original column names agree with GEO characteristics for every sample. grp = genotype_exercise.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\aligned\\aligned_matrix.csv", "sha256": "1cd9597bf4949a5cd8bde39494cef3d228f7159b12813d3d317e128ff470faad", "n_features": 55401, "n_samples": 14, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 10645758.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: The deposited file is DESeq2-normalized counts (GEO data_processing: 'tabular file containing normalised counts'; non-integer values). Dividing each sample by its smallest non-zero value returns integers for all 55401 x 14 entries (max deviation < 1e-8), i.e. the original integer counts (StringTie/prepDE) divided by DESeq2 size factors 0.65-1.45. prep_recover_raw_counts.py recovers them. Paper input to DESeq2 is the same integer count matrix (S4.4.2.p1).

rejected alternatives: [{"value": "use DESeq2-normalized counts rounded as estimated counts", "reason_rejected": "rescaling by size factors distorts the count variance; exact raw counts are recoverable"}]

### design (valid, not_started)

final: {"analysis_type": "multigroup (one DESeq2 model ~ grp on all 14 samples, planned pairwise contrasts)", "design_column": "grp", "contrasts": [{"name": "grp_KO_SVE_vs_KO_nSVE", "control": "KO_nSVE", "treatment": "KO_SVE", "role": "primary"}, {"name": "grp_WT_SVE_vs_WT_nSVE", "control": "WT_nSVE", "treatment": "WT_SVE", "role": "secondary"}, {"name": "grp_KO_nSVE_vs_WT_nSVE", "control": "WT_nSVE", "treatment": "KO_nSVE", "role": "secondary"}, {"name": "grp_KO_SVE_vs_WT_nSVE", "control": "WT_nSVE", "treatment": "KO_SVE", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\suitability\\suitability.md", "n_comparisons": 7, "n_analyzable": 7}}

reasoning: Four groups (2 genotypes x 2 exercise conditions, S2.2.p1). The paper reports pairwise comparisons (S4.4.2.p1) without saying whether each pair was fitted alone or from one model; the skill rule for one design with several levels is one model with planned contrasts. A first attempt with separate per-pair fits (kept as sensitivity) gave KO exercise 33 / WT exercise 2047 DEGs vs paper 223 / 795, while the joint model gives 329 / 772 and reproduces KO SVE vs WT nSVE exactly (557 vs 557), so the joint model is the paper-aligned route. Primary exercise estimand: KO SVE vs KO nSVE, both sampled at CT14 (S2.2.p1, S2.5.p1). WT SVE vs nSVE is an exercise comparison confounded by design with circadian ... [168 more characters]

rejected alternatives: [{"value": "separate DESeq2 fit per pair of groups", "reason_rejected": "skill rule prefers one model for a multi-level design; per-pair fits reproduce the paper worse (KO exercise 33 vs 223, WT exercise 2047 vs 795); kept as sensitivity"}, {"value": "genotype x exercise factorial with interaction", "reason_rejected": "paper does not fit an interaction; WT SVE sampled at a different circadian time so the interaction would not be an exercise-by-genotype estimand"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 14, "n_columns": 4, "columns": ["Intercept", "grp_KO_nSVE", "grp_WT_SVE", "grp_WT_nSVE"], "rank": 4, "full_rank": true, "residual_df": 10, "levels": {"grp": {"WT_nSVE": 4, "WT_SVE": 4, "KO_nSVE": 3, "KO_SVE": 3}}, "cells": [{"cell": ["KO_SVE"], "n": 3}, {"cell": ["KO_nSVE"], "n": 3}, {"cell": ["WT_SVE"], "n": 4}, {"cell": ["WT_nSVE"], "n": 4}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 14, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 14, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.genotype", "n_levels": 2, "status": "primary_nested_in_candidate", "crosstab": {"KO_SVE": {"Vipr2-/-": 3, "wildtype": 0}, "KO_nSVE": {"Vipr2-/-": 3, "wildtype": 0}, "WT_SVE": {"Vipr2-/-": 0, ... [2484 more characters]

reasoning: Independent animals, one sample each; no batch, lane, or sex variable recorded (all male, S4.3.p1). Circadian sampling time is not a metadata column: it is fixed by group (WT SVE = CT22, others CT14) and is aliased with the WT exercise contrast by design; this is recorded as a caveat rather than a covariate.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, default independent filtering and Cook's outlier handling)", "formula": "~ grp", "deviations": ["pydeseq2 instead of R DESeq2 (Bioconductor 3.14)"]}

reasoning: Paper method DESeq2 on integer counts (S4.4.2.p1); raw counts recovered exactly, so the paper route runs as one ~ grp model with Wald contrasts.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": false}}

reasoning: S2.2.p2: DEGs with FDR < 0.05; S4.4.2.p2: BH-corrected p. No fold-change rule.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\joint\\DEG_results_grp_KO_SVE_vs_KO_nSVE.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\joint\\DEG_results_grp_WT_SVE_vs_WT_nSVE.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\joint\\DEG_results_grp_KO_nSVE_vs_WT_nSVE.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\joint\\DEG_results_grp_KO_SVE_vs_WT_nSVE.csv"], "counts": {"joint/grp_KO_SVE_vs_KO_nSVE": {"applied": {"rule": "padj < 0.05", "n_tested": 17059, "n_significant": 329, "n_up": 190, "n_down": 139, "deg_sanity": "ok"}}, "joint/grp_WT_SVE_vs_WT_nSVE": {"applied": {"rule": "padj < 0.05", "n_tested": 10540, "n_significant": 772, "n_up": 542, "n_down": 230, "deg_sanity": "ok"}}, "joint/grp_KO_nSVE_vs_WT_nSVE": {"applied": {"rule": "padj < 0.05", "n_tested": 17521, "n_significant": 457, "n_up": 187, "n_down": 270, "deg_sanity": "ok"}}, "joint/grp_KO_SVE_v ... [139 more characters]

reasoning: One DESeq2 model ~ grp on all 14 samples; the paper's four planned contrasts (S2.3-S2.6). The KO exercise contrast is the primary estimand.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint_extra", "role": "exploratory", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 14, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\joint_extra\\DEG_results_grp_WT_SVE_vs_KO_SVE.csv"], "counts": {"joint_extra/grp_WT_SVE_vs_KO_SVE": {"applied": {"rule": "padj < 0.05", "n_tested": 10540, "n_significant": 532, "n_up": 285, "n_down": 247, "deg_sanity": "ok"}}}}

reasoning: Same model; WT SVE vs KO SVE is listed among the paper's pairwise analyses (S4.4.2.p1, 10488 genes tested) and used in Fig 4, but no DEG count is reported. Genotype contrast, not exercise; phases differ (CT22 vs CT14).

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pairwise_grp_KO_SVE_vs_KO_nSVE", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\pairwise_grp_KO_SVE_vs_KO_nSVE\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\pairwise_grp_KO_SVE_vs_KO_nSVE\\DEG_results_KO_SVE_vs_KO_nSVE.csv"], "counts": {"pairwise_grp_KO_SVE_vs_KO_nSVE": {"applied": {"rule": "padj < 0.05", "n_tested": 16714, "n_significant": 33, "n_up": 18, "n_down": 15, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: separate two-group DESeq2 fit on these two groups only. Paper S2.5.p1: KO SVE vs KO nSVE, both CT14; separate pairwise DESeq2 fit.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pairwise_grp_WT_SVE_vs_WT_nSVE", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 8, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\pairwise_grp_WT_SVE_vs_WT_nSVE\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\pairwise_grp_WT_SVE_vs_WT_nSVE\\DEG_results_WT_SVE_vs_WT_nSVE.csv"], "counts": {"pairwise_grp_WT_SVE_vs_WT_nSVE": {"applied": {"rule": "padj < 0.05", "n_tested": 13172, "n_significant": 2047, "n_up": 1235, "n_down": 812, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: separate two-group DESeq2 fit on these two groups only. Paper S2.4.p1: WT SVE (ZT14/CT22) vs WT nSVE (CT14); exercise confounded with circadian phase.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pairwise_grp_KO_nSVE_vs_WT_nSVE", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 7, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\pairwise_grp_KO_nSVE_vs_WT_nSVE\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\pairwise_grp_KO_nSVE_vs_WT_nSVE\\DEG_results_KO_nSVE_vs_WT_nSVE.csv"], "counts": {"pairwise_grp_KO_nSVE_vs_WT_nSVE": {"applied": {"rule": "padj < 0.05", "n_tested": 17830, "n_significant": 326, "n_up": 137, "n_down": 189, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: separate two-group DESeq2 fit on these two groups only. Paper S2.3.p1: genotype at CT14 under nSVE.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pairwise_grp_KO_SVE_vs_WT_nSVE", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 7, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\pairwise_grp_KO_SVE_vs_WT_nSVE\\input\\matrix.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\pairwise_grp_KO_SVE_vs_WT_nSVE\\DEG_results_KO_SVE_vs_WT_nSVE.csv"], "counts": {"pairwise_grp_KO_SVE_vs_WT_nSVE": {"applied": {"rule": "padj < 0.05", "n_tested": 13045, "n_significant": 594, "n_up": 242, "n_down": 352, "deg_sanity": "ok"}}}}

reasoning: Sensitivity: separate two-group DESeq2 fit on these two groups only. Paper S2.6.p1: KO SVE vs WT nSVE at CT14.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_KO_SVE_vs_KO_nSVE", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": false}, "direction": "up", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\ora_up\\DEG_results_grp_KO_SVE_vs_KO_nSVE_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\ora_up\\DEG_results_grp_KO_SVE_vs_KO_nSVE_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\ora_up\\DEG_results_grp_KO_SVE_vs_KO_nSVE_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\ora_up\\DEG_results_grp_KO_SVE_vs_KO_nSVE_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 189 Mouse genes (direction=up, padj<0.05, |log2FC|>0.0). ### GO_Biological_ ... [1394 more characters]

reasoning: Paper reports KEGG terms up by exercise in KO SCN (Fig 3F, S2.5.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_KO_SVE_vs_KO_nSVE", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": false}, "direction": "down", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\ora_down\\DEG_results_grp_KO_SVE_vs_KO_nSVE_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\ora_down\\DEG_results_grp_KO_SVE_vs_KO_nSVE_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\ora_down\\DEG_results_grp_KO_SVE_vs_KO_nSVE_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\ora_down\\DEG_results_grp_KO_SVE_vs_KO_nSVE_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 139 Mouse genes (direction=down, padj<0.05, |log2FC|>0.0). ### GO ... [1404 more characters]

reasoning: Paper reports KEGG terms down by exercise in KO SCN (mTOR signaling; S2.5.p1).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_KO_SVE_vs_KO_nSVE", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_KO_SVE_vs_KO_nSVE\\gsea\\DEG_results_grp_KO_SVE_vs_KO_nSVE_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25626 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 18 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_UV_RESPONSE_DN | NES=1.65 | NOM p=0.00e+00 | FDR q=2.43e-02 - HALLMARK_MITOTIC_SPINDLE | NES=1.59 | NOM p=0.00e+00 | FDR q=3.04e-02 - HALLMARK_G2M_CHECKPOINT | NES=1.52 | NOM p=3.12e-03 | FDR q=4.44e-02 - HALLMARK_TGF_BETA_SIGNALING | NES=1.43 | NOM p=3.37e-02 | FDR q=8.68e-02 - HALLMARK_E2F_TARGETS | NES=1.27 | NOM p=6.15e-02 | FDR q=3.20e-01 - HALLMARK_IL2_STAT5_SIGNALING | NES=1.26 | NOM p=3.99e-02 | FDR q=2.86e-01 - HALLMARK_SPERMATOGENESIS | NES=1.24 | NOM p=9.78e-02 | FDR q=2.99e-01 - HALLMARK_MYOGENESIS | NES=1.22 | NOM p=7.11e-02 | FDR q=2.95e-01 - HALLMARK_P53_PATHWAY | NES=1.21 | NOM p=8.08e-02 | FDR q=3.00e-01 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.18 | NOM p=1.26e-01 | FDR q=3.32e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=-2.45 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=-1.99 | NOM  ... [449 more characters]

reasoning: Hallmark GSEA on the full ranking of the primary exercise contrast.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/grp_WT_SVE_vs_WT_nSVE", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\463ad4ee2ce52e09b589fa8ce48a64d7c595a849\\GSE207992\\results\\enrichment_joint_grp_WT_SVE_vs_WT_nSVE\\gsea\\DEG_results_grp_WT_SVE_vs_WT_nSVE_GSEA_Hallmark.csv"], "summary": "GSEA complete on 25626 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 28 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_HEDGEHOG_SIGNALING | NES=2.13 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.75 | NOM p=3.43e-03 | FDR q=8.23e-03 - HALLMARK_MYOGENESIS | NES=1.72 | NOM p=0.00e+00 | FDR q=9.03e-03 - HALLMARK_APICAL_JUNCTION | NES=1.58 | NOM p=1.34e-03 | FDR q=3.48e-02 - HALLMARK_COAGULATION | NES=1.41 | NOM p=2.50e-02 | FDR q=1.50e-01 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.41 | NOM p=5.61e-03 | FDR q=1.28e-01 - HALLMARK_KRAS_SIGNALING_DN | NES=1.38 | NOM p=2.81e-02 | FDR q=1.38e-01 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.32 | NOM p=3.18e-02 | FDR q=2.18e-01 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.31 | NOM p=4.01e-02 | FDR q=2.06e-01 - HALLMARK_NOTCH_SIGNALING | NES=1.30 | NOM p=1.34e-01 | FDR q=2.05e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-2.56 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_PR ... [449 more characters]

reasoning: Hallmark GSEA on the WT exercise (phase-confounded) contrast; paper reports KEGG for it (Fig 3D).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["WT SVE vs WT nSVE compares ZT14/CT22 with CT14: the exercise effect is confounded with an 8h circadian-phase difference (paper S2.4.p1); it is not a pure exercise effect.", "KO SVE vs WT nSVE crosses genotype and exercise and is not an exercise estimand.", "pydeseq2 rather than R DESeq2; counts recovered from the deposited normalized matrix. Whether the paper fitted one 4-group model or separate pairs is not stated; the joint model reproduces 2/4 counts closely, KO-nSVE contrasts are ~1.5x the paper's.", "Pathway direction, KO SVE vs KO nSVE: our KEGG ORA puts Parkinson disease / Huntington disease / oxidative phosphorylation in the DOWN genes (Parkinson adj p 0.003) and Hallmark GSEA gives OXPHOS NES -2.4, with mTOR signaling among up genes (n.s.). This contradicts paper S2.5.p1 (Parkinson and Chemical carcinogenesis-ROS up, mTOR down) but agrees with paper S1.p4 ('pathways associated with neurodegeneration are downregulated by timed exercise in the Vipr2-/- SCN') and with the paper's named down genes Cox16/Ndufa4. The paper is internally inconsistent; our direction follows the data.", "Joint model: KO nSVE contrasts exceed the paper's counts (KO exercise 329 vs 223; KO vs WT nSVE 457 vs 307) while WT exercise (772 vs 795) and KO SVE vs WT nSVE (557 vs 557) match; separate per-pair fits give 33 / 2047 / 326 / 594. All paper-named KO exercise genes (Kdr, Banp, Syk, Naif1, Kctd18, Ncor1 up; Cox16, Ndufa4 down) are significant in the pape ... [6886 more characters]

reasoning: Paper-aligned DESeq2 route (one ~ grp model, planned contrasts) at the paper's FDR rule. Expected directions: KO exercise up Kdr/Banp/Syk/Naif1/Kctd18/Ncor1, down Cox16/Ndufa4, no core clock genes DE (S2.5.p1, S2.7.p2); WT exercise up Nr1d1/Rgs16/Miat/Serpine1/Syngap1, down Cry1/Per2/Slc2a13 (S2.4.p1).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 14 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "genome build",
    "paper": "GRCm38 (S4.4.2.p1)",
    "data": "GEO data_processing: GRCm39, GENCODE vM27",
    "disposition": "executable_without_change"
  },
  {
    "item": "WT SVE sampling phase",
    "paper": "ZT14/CT22 (S2.2.p1, S4.4.p4) vs ZT14/CT24 (S4.4.2.p1)",
    "data": "GEO: culled at ZT14",
    "disposition": "executable_without_change"
  },
  {
    "item": "deposited matrix",
    "paper": "DESeq2 on counts",
    "data": "only DESeq2-normalized counts deposited; integer counts recovered exactly by per-sample rescaling (prep_recover_raw_counts.py)",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: GSE207992 / PMC9971895 (paper_id 463ad4ee2ce52e09b589fa8ce48a64d7c595a849)

Paper: Timed exercise stabilizes behavioral rhythms but not molecular programs in the brain's suprachiasmatic clock (iScience 2023, PMID 36866044).
Status: finished. Route: paper_aligned (case spec route, `tools.case_runner execute`, validator 0 errors).

## What ran
- Data: GEO deposits only `GSE207992_DESeq2_normcounts.csv` (DESeq2-normalized counts, 55401 genes x 14 SCN samples). Exact integer raw counts were recovered by dividing each sample by its smallest non-zero value (all entries integer within 1e-8; size factors 0.65-1.45): `prep_recover_raw_counts.py` -> `GSE207992_raw_counts_recovered.csv` (Ensembl IDs without version) + `GSE207992_gene_symbols.csv`.
- Alignment: matrix columns renamed to AH labels = GEO `description`; exact match 14/14. grp = genotype (WT / KO = Vipr2-/-) x exercise (nSVE / SVE): WT_nSVE 4, WT_SVE 4, KO_nSVE 3, KO_SVE 3 (= paper S4.4.2.p1).
- Suitability: analyzable; all male (sex check passed); no batch/subject covariates.
- Primary route: one DESeq2 (pydeseq2 Wald) model `~ grp` on all 14 samples, the paper's 4 planned contrasts (`joint`), plus WT SVE vs KO SVE (`joint_extra`, exploratory, no paper count).
- Sensitivity: separate two-group DESeq2 fit per pair (`pairwise_*`) - my first attempt; it reproduced the paper worse, so the joint model became primary (skill rule: one model for one multi-level design).
- Enrichment: KEGG/GO ORA (up, down) and Hallmark GSEA on KO SVE vs KO nSVE; Hallmark GSEA on WT SVE vs WT nSVE. All completed.

## DEG counts vs paper (paper threshold: FDR (BH) < 0.05, no fold-change rule; S2.2.p2, S4.4.2.p2)
| Contrast | Role | Joint model (primary) up/down | Pairwise fit (sensitivity) | Paper up/down |
|---|---|---|---|---|
| KO SVE vs KO nSVE (exercise, both CT14) | primary | 329 (190/139) | 33 | 223 (105/118) |
| WT SVE vs WT nSVE (exercise + 8h phase shift) | secondary | 772 (542/230) | 2047 | 795 (556/239) |
| KO nSVE vs WT nSVE (genotype) | secondary | 457 (187/270) | 326 | 307 (158/149) |
| KO SVE vs WT nSVE | secondary | 557 (242/315) | 594 | 557 (246/311) |
| WT SVE vs KO SVE | exploratory | 532 (285/247) | - | not reported |

Gene-level agreement (joint model): KO exercise - Kdr, Banp, Syk, Naif1, Kctd18, Gm1848, Ncor1 up; Cox16, Ndufa4 down; Per2/Arntl/Nr1d1/Cry1 not DE - all as in the paper (S2.5.p1, S2.7.p2). WT exercise - Nr1d1, Rgs16, Miat, Serpine1, Syngap1 up; Cry1, Per2, Slc2a13 down - as in S2.4. ... [2533 more characters]
