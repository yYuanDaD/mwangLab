# Review packet B (the analysis' decisions): GSE174785

## Mechanical flags

- **pairing_key_candidate**: {"key": "characteristics_ch1.2.genotype (without source_name_ch1) + suffix of title", "across": "source_name_ch1", "pairs_or_sets": 10, "samples_linked": 20, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/muscle_R_vs_W_genotype-WT | 782 | 1177 | padj < 0.05 and |log2FoldChange| > 1 | 3946 | 1941 | 1177 | 4942 | 8184 | 4324 | 2902 | 4823 | 0.208 | 0.085 |

## Samples per design level

### `muscle`
- **R** (10): GSM5328123 / Oxidative mECs ATf4-/- rep1; GSM5328124 / Oxidative mECs ATf4-/- rep2; GSM5328125 / Oxidative mECs ATf4-/- rep3; GSM5328126 / Oxidative mECs ATf4-/- rep4; GSM5328127 / Oxidative mECs ATf4-/- rep5; GSM5328133 / Oxidative mECs WT rep1; GSM5328134 / Oxidative mECs WT rep2; GSM5328135 / Oxidative mECs WT rep3; GSM5328136 / Oxidative mECs WT rep4; GSM5328137 / Oxidative mECs WT rep5
- **W** (10): GSM5328128 / Glycolytic mECs Atf4-/- rep1; GSM5328129 / Glycolytic mECs Atf4-/- rep2; GSM5328130 / Glycolytic mECs Atf4-/- rep3; GSM5328131 / Glycolytic mECs Atf4-/- rep4; GSM5328132 / Glycolytic mECs Atf4-/- rep5; GSM5328138 / Glycolytic mECs WT rep1; GSM5328139 / Glycolytic mECs WT rep2; GSM5328140 / Glycolytic mECs WT rep3; GSM5328141 / Glycolytic mECs WT rep4; GSM5328142 / Glycolytic mECs WT rep5

### `genotype`
- **KO** (10): GSM5328123 / Oxidative mECs ATf4-/- rep1; GSM5328124 / Oxidative mECs ATf4-/- rep2; GSM5328125 / Oxidative mECs ATf4-/- rep3; GSM5328126 / Oxidative mECs ATf4-/- rep4; GSM5328127 / Oxidative mECs ATf4-/- rep5; GSM5328128 / Glycolytic mECs Atf4-/- rep1; GSM5328129 / Glycolytic mECs Atf4-/- rep2; GSM5328130 / Glycolytic mECs Atf4-/- rep3; GSM5328131 / Glycolytic mECs Atf4-/- rep4; GSM5328132 / Glycolytic mECs Atf4-/- rep5
- **WT** (10): GSM5328133 / Oxidative mECs WT rep1; GSM5328134 / Oxidative mECs WT rep2; GSM5328135 / Oxidative mECs WT rep3; GSM5328136 / Oxidative mECs WT rep4; GSM5328137 / Oxidative mECs WT rep5; GSM5328138 / Glycolytic mECs WT rep1; GSM5328139 / Glycolytic mECs WT rep2; GSM5328140 / Glycolytic mECs WT rep3; GSM5328141 / Glycolytic mECs WT rep4; GSM5328142 / Glycolytic mECs WT rep5

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE174785"], "assay": "bulk RNA-seq (Smart-seq2 / TruSeq per GEO), kallisto quantification, FACS-sorted muscle endothelial cells (S4.4.3.p1)", "samples": "20 samples: RmECs (soleus, oxidative) and WmECs (EDL, glycolytic) from WT and Atf4 EC-knockout (Atf4^dEC/dEC) mice, n=5 per group (GEO titles; S2.6.p1, Fig6B-D)", "factors": {"muscle_ec": ["RmEC (soleus)", "WmEC (EDL)"], "genotype": ["WT", "Atf4 EC-KO"]}, "primary_estimand": "Exercise-primed (oxidative, soleus RmEC) vs non-primed (glycolytic, EDL WmEC) capillary ECs, the transcriptional basis of exercise-induced angiogenesis (S2.2.p2).", "planned_contrasts": ["WT RmEC vs WT WmEC (S2.2.p2, Fig2G, S2.6.p1; paper: 782 DEGs)", "Atf4-KO RmEC vs Atf4-KO WmEC (S2.6.p1, Fig6B; paper: 211 remaining of WT DEGs)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S2.6.p1; Fig6C legend; S4.4.3.p2 ('log fold change > 1 and adjusted p-value < 0.05')"}, "paper_method": "DESeq2 on kallisto counts, genes with <=1 count across all samples removed (S4.4.3.p1)"}

reasoning: The paper links exercise-induced angiogenesis to metabolically primed ATF3/4+ ECs that are enriched in oxidative muscle; GSE174785 compares these ECs (soleus) with EDL ECs in WT and Atf4-KO mice.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s4_GSE174785_forced_run\\GSE174785\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["DA.p1 and key resources table name GSE174785 as the bulk RNA-seq of RmECs vs WmECs, WT and Atf4 dEC/dEC", "20 GSM samples = 2 muscles x 2 genotypes x 5 reps, matching Fig6D design", "data_processing: kallisto + DESeq2, matching S4.4.3.p1"], "accession": "GSE174785", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE174785\\GSE174785_metadata.csv"}

reasoning: Paper data-availability statement and GEO metadata agree.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 20, "n_metadata": 20, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s4_GSE174785_forced_run\\GSE174785\\aligned\\aligned_metadata.csv", "columns": {"muscle": {"alias_of": "source_name_ch1", "recode": {"Soleus muscle": "R", "Extensor digitorum longus muscle": "W"}}, "genotype": {"alias_of": "characteristics_ch1.2.genotype", "recode": {"Wild type": "WT", "EC specific Atf4-/-": "KO"}}}, "output": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s4_GSE174785_forced_run\\GSE174785\\aligned\\design_metadata.csv", "sha256": "d666a1e0d9ba2fdb78c9c00119cfe5be31c83f60dbd45558453b0828e7a7d7be", "levels": {"muscle": {"R": 10, "W": 10}, "genotype": {"KO": 10, "WT": 10}}}}

reasoning: Merged-tar columns are GSM ids that equal the metadata index exactly (inspect: 20/20). Muscle (source_name_ch1) and genotype define the groups.

### matrix (valid, not_started)

final: {"feature_level": "transcript (ENSMUST), kallisto est_counts column per sample (sums 8.5e6-1.6e7, not TPM which sums to 1e6)", "paper_input": "kallisto counts to DESeq2 (S4.4.3.p1)", "matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s4_GSE174785_forced_run\\GSE174785\\aligned\\aligned_matrix.csv", "sha256": "34e990ca8bcb71e62f2d5b097f68b9581d94da5e47b63ae5d66f3b8f8bf228e3", "n_features": 129439, "n_samples": 20, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2263230.0, "median": 0.0, "integer_fraction": 0.6186, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Per-sample kallisto abundance files have est_counts and tpm; the merged matrix holds est_counts (column sum of GSM5328123 = 1.411e7 equals its est_counts sum). Fractional estimated counts at transcript level; a gene-level summary would be needed before DESeq2.

### design (valid, not_started)

final: {"analysis_type": "two factors, muscle contrast within each genotype", "formula": "~ cell", "contrasts": [{"name": "muscle_R_vs_W_genotype-WT", "control": "W", "treatment": "R", "role": "primary", "note": "exercise-primed vs non-primed ECs, WT"}, {"name": "muscle_R_vs_W_genotype-KO", "control": "W", "treatment": "R", "role": "secondary", "note": "same in Atf4 EC-KO"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s4_GSE174785_forced_run\\GSE174785\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: The exercise question of the paper is carried by the oxidative (exercise-primed) vs glycolytic EC comparison; run it within each genotype (S2.2.p2, S2.6.p1).

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(muscle) + C(genotype)", "n_samples": 20, "n_columns": 3, "columns": ["Intercept", "muscle_W", "genotype_WT"], "rank": 3, "full_rank": true, "residual_df": 17, "levels": {"muscle": {"R": 10, "W": 10}, "genotype": {"KO": 10, "WT": 10}}, "cells": [{"cell": ["R", "KO"], "n": 5}, {"cell": ["R", "WT"], "n": 5}, {"cell": ["W", "KO"], "n": 5}, {"cell": ["W", "WT"], "n": 5}], "min_cell_size": 5, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 20, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 20, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 2, "status": "complete_confounding", "crosstab": {"R": {"Extensor digitorum longus muscle": 0, "Soleus muscle": 10}, "W": {"Extensor digitorum longus muscle": 10, "Soleus muscle": 0}}}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.celltype", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.strain", "n_levels": 1, " ... [1792 more characters]

reasoning: One sample per sorted EC pool; no batch column.

### method (valid, not_started)

final: {"matrix_type": "estimated counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ cell", "paper_route": {"method": "DESeq2 on kallisto counts", "status": "reproduced"}, "deviations": ["pydeseq2 instead of R DESeq2"], "rounding_documented": true}

reasoning: kallisto estimated counts rounded for DESeq2 (S4.4.3.p1).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}}

reasoning: S4.4.3.p2: log fold change > 1 and adjusted p-value < 0.05.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 20, "matrix": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s4_GSE174785_forced_run\\GSE174785\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s4_GSE174785_forced_run\\GSE174785\\results\\joint\\DEG_results_muscle_R_vs_W_genotype-WT.csv", "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s4_GSE174785_forced_run\\GSE174785\\results\\joint\\DEG_results_muscle_R_vs_W_genotype-KO.csv"], "counts": {"joint/muscle_R_vs_W_genotype-WT": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 42294, "n_significant": 1177, "n_up": 945, "n_down": 232, "deg_sanity": "ok"}}, "joint/muscle_R_vs_W_genotype-KO": {"applied": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 29260, "n_significant": 510, "n_up": 254, "n_down": 256, "deg_sanity": "ok"}}}}

reasoning: one model, planned muscle contrasts within genotype

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["exercise priming inferred from muscle type"], "results": {"joint/muscle_R_vs_W_genotype-WT": {"n_deg": 1177, "up": 945, "down": 232, "rule": "padj < 0.05 and |log2FoldChange| > 1"}, "joint/muscle_R_vs_W_genotype-KO": {"n_deg": 510, "up": 254, "down": 256, "rule": "padj < 0.05 and |log2FoldChange| > 1"}}, "paper_counts": {"joint/muscle_R_vs_W_genotype-WT": 782}, "comparison": {"joint/muscle_R_vs_W_genotype-WT": {"ours": 1177, "paper": 782}}, "paper_gene_check": {}}

reasoning: Paper reports 782 DEGs for WT RmEC vs WmEC (S2.6.p1).

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "library protocol",
    "paper": "Smart-seq2 (S4.4.3.p1)",
    "data": "GEO extract_protocol says Illumina TruSeq stranded mRNA",
    "disposition": "recorded_not_blocking"
  }
]
