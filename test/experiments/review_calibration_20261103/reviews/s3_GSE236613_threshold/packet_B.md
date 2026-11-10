# Review packet B (the analysis' decisions): GSE236613

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.1.treatment", "n_values": 3, "max_repeat": 3, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **possible_reversed_contrast**: {"contrast": "grp_Sham_vs_NE", "control": "NE", "treatment": "Sham", "note": "the control side reads as exercise or the test side as control"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/grp_RE_vs_NE | 4423 | 5 | padj < 0.05 | 5 | 5 | 3 | 9 | 809 | 403 | 199 | 248 | 0.123 | 0.044 |
| joint/grp_Sham_vs_NE | 6697 | 1007 | padj < 0.05 | 1007 | 619 | 261 | 1528 | 3058 | 1235 | 548 | 1507 | 0.091 | 0.166 |

## Samples per design level

### `grp`
- **NE** (3): GSM7566378 / tibias, Ovx_NE_6; GSM7566379 / tibias, Ovx_NE_8; GSM7566380 / tibias, Ovx_NE_9
- **RE** (3): GSM7566381 / tibias, Ovx_RE_3; GSM7566382 / tibias, Ovx_RE_5; GSM7566383 / tibias, Ovx_RE_8
- **Sham** (3): GSM7566375 / tibias, Sham_12; GSM7566376 / tibias, Sham_7; GSM7566377 / tibias, Sham_8

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE236613"], "assay": "bulk total RNA-seq (Ribo-Zero), left tibia, Illumina NovaSeq 6000 (S2.7.p1)", "organism": "Rat (female Sprague-Dawley)", "factors": {"group": ["Sham", "NE/Ovx", "RE/Ovx"]}, "sample_inclusion": "3 left tibias per group sequenced out of 6 rats per group (S2.7.p1); 9 samples total", "primary_estimand": "Effect of 12 weeks of ladder-climbing resistance exercise on tibia gene expression in ovariectomized rats: RE/Ovx vs NE/Ovx (S3.4.p2, S4.p3)", "planned_contrasts": ["RE/Ovx vs NE/Ovx (S3.4.p2; paper: 4423 DEGs, 2227 up / 2196 down) - exercise effect, primary", "NE/Ovx vs Sham (S3.4.p2; paper: 6697 DEGs, 4040 up / 2657 down) - ovariectomy model effect, secondary (not an exercise contrast)"], "repeated_measure_unit": "none; one tibia per independent rat", "normalization": "DESeq2 size factors (S2.8.p1)", "paper_method": "DESeq2 on RNA-seq counts (S2.8.p1); exact design (all 9 samples vs per-pair subset) not stated", "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false, "source_locator": "S2.8.p1"}, "paper_results": "DEG counts S3.4.p2; 401/213 OP-related DEGs after DisGeNET/OMIM intersection (S3.4.p3); RT-qPCR genes Acp5, Fos, Fosb up in NE vs Sham and down in RE vs NE, Calcr opposite, Stat1 up in RE vs NE (S3.7.p1)"}

reasoning: S2.1.p1 three randomized groups; S2.7.p1 3 tibias per group sequenced; S2.8.p1 DESeq2, p < 0.05 and FC > 1.2 or < 0.83; S3.4.p2 reports both pairwise comparisons with counts. Exercise estimand is RE/Ovx vs NE/Ovx; NE/Ovx vs Sham is the model contrast the paper also reports.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\0f65e49e563e3417d3cee92f75eba6244b276201\\GSE236613_counts.csv", "owned": true, "checks": ["GEO series GSE236613: rat tibias, treatment levels sham-operated / non-exercise / resistance exercise, 3 each, matching S2.7.p1", "contact Qing Wang, Nanjing University of Chinese Medicine = first author QW and institution (S2.1.p1, S7.p1)", "paper data availability statement (S5.p1) gives no accession; ownership rests on design, tissue, organism, institution and author match"], "accession": "GSE236613", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE236613\\GSE236613_metadata.csv"}

reasoning: Metadata organism Rattus norvegicus, tissue tibias, 9 samples split 3/3/3 into Sham / Ovx_NE / Ovx_RE titles, submitter Qing Wang at NJUCM, matching the paper. The paper itself names no GEO accession (S5.p1).

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.1.treatment", "recode": {"sham-operated": "Sham", "non-exercise": "NE", "resistance exercise": "RE"}}}, "output": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\aligned\\design_metadata.csv", "sha256": "ccf56fe3576a4b3d38300b17e0a9cb0034cefcfc4485f258fdc818a806825354", "levels": {"grp": {"Sham": 3, "NE": 3, "RE": 3}}}}

reasoning: The prep script renamed each GSM*_SampleN_counts column to its GSM accession, which equals the metadata index (geo_accession). grp copies the treatment characteristic and recodes it to Sham / NE (NE/Ovx) / RE (RE/Ovx); titles (Sham_*, Ovx_NE_*, Ovx_RE_*) agree.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\aligned\\aligned_matrix.csv", "sha256": "b87bc0f211994cdb80c22184524a7fd421bd9fea1ba5cf1d6404eaabd121c761", "n_features": 22589, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 360454.0, "median": 80.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Per-sample *_counts.txt.gz files are 100% integers (library sizes 12.3-16.7 M), described in data_processing as 'counts value (the number of reads for each gene in each sample)' from eXpress. The merged tar interleaved FPKM columns, which the prep script dropped. Paper input is counts for DESeq2 (S2.8.p1).

### design (valid, not_started)

final: {"analysis_type": "multi-group, one factor with three levels", "design_column": "grp", "contrasts": [{"name": "grp_RE_vs_NE", "control": "NE", "treatment": "RE", "role": "primary"}, {"name": "grp_Sham_vs_NE", "control": "NE", "treatment": "Sham", "role": "secondary", "note": "paper reports NE/Ovx vs Sham; sign is flipped relative to the paper (NE vs Sham up = Sham vs NE down)"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: One factor (grp) with three levels; reference NE/Ovx so the exercise contrast RE vs NE is direct (S3.4.p2). NE vs Sham is kept as the paper's secondary model contrast; it is fitted as Sham vs NE from the same model and its sign is reversed when compared with the paper.

rejected alternatives: [{"value": "pool Sham and NE as control", "reason_rejected": "Sham is not ovariectomized; pooling would mix the OVX model effect into the exercise contrast"}, {"value": "RE vs Sham", "reason_rejected": "not a planned paper contrast; confounds exercise with ovariectomy"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 9, "n_columns": 3, "columns": ["Intercept", "grp_RE", "grp_Sham"], "rank": 3, "full_rank": true, "residual_df": 6, "levels": {"grp": {"Sham": 3, "NE": 3, "RE": 3}}, "cells": [{"cell": ["NE"], "n": 3}, {"cell": ["RE"], "n": 3}, {"cell": ["Sham"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 9, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 9, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.treatment", "n_levels": 3, "status": "complete_confounding", "crosstab": {"NE": {"non-exercise": 3, "resistance exercise": 0, "sham-operated": 0}, "RE": {"non-exercise": 0, "resistance exercise": 3, "sham-operated": 0}, "Sham": {"non-exercise": 0, "resistance exercise": 0, "sham-ope ... [1400 more characters]

reasoning: Independent rats, one tibia each, no batch, sex, or lane columns in metadata (all female, S2.1.p1).

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2", "status": "reproduced"}, "deviations": ["exact paper design (all 9 samples vs per-pair subset) unknown; primary uses one model on all 9 samples, sensitivity refits each pair alone", "GEO data_processing names DESeq (2012) nbinomTest with p <= 0.05 and FC >= 2, which contradicts the paper (DESeq2, FC 1.2); paper followed"]}

reasoning: Integer counts -> DESeq2 as in S2.8.p1.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S2.8.p1: DEGs were called with DESeq2 at adjusted p < 0.05.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 9, "matrix": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\aligned\\aligned_matrix.csv", "formula": "~ cell", "outputs": ["E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\results\\joint\\DEG_results_grp_RE_vs_NE.csv", "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\results\\joint\\DEG_results_grp_Sham_vs_NE.csv"], "counts": {"joint/grp_RE_vs_NE": {"applied": {"rule": "padj < 0.05", "n_tested": 18396, "n_significant": 5, "n_up": 4, "n_down": 1, "deg_sanity": "ok"}}, "joint/grp_Sham_vs_NE": {"applied": {"rule": "padj < 0.05", "n_tested": 14468, "n_significant": 1007, "n_up": 340, "n_down": 667, "deg_sanity": "ok"}}}}

reasoning: One DESeq2 model ~ grp on all 9 samples, planned contrasts RE vs NE (primary) and Sham vs NE (secondary).

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pair_RE_vs_NE", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\results\\pair_RE_vs_NE\\input\\matrix.csv", "formula": "~ grp", "outputs": ["E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\results\\pair_RE_vs_NE\\DEG_results_RE_vs_NE.csv"], "counts": {"pair_RE_vs_NE": {"applied": {"rule": "padj < 0.05", "n_tested": 16399, "n_significant": 152, "n_up": 26, "n_down": 126, "deg_sanity": "ok"}}}}

reasoning: Pairwise DESeq2 on the 6 OVX samples only, in case the paper fitted each comparison separately.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "pair_NE_vs_Sham", "role": "sensitivity", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\results\\pair_NE_vs_Sham\\input\\matrix.csv", "formula": "~ grp", "outputs": ["E:\\agent\\mwangLab_review\\test\\experiments\\review_calibration_20261103\\runs\\s3_GSE236613_threshold\\GSE236613\\results\\pair_NE_vs_Sham\\DEG_results_NE_vs_Sham.csv"], "counts": {"pair_NE_vs_Sham": {"applied": {"rule": "padj < 0.05", "n_tested": 14576, "n_significant": 894, "n_up": 633, "n_down": 261, "deg_sanity": "ok"}}}}

reasoning: Pairwise DESeq2 NE vs Sham on 6 samples, paper's orientation.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["n = 3 per group (pilot, S4.p9)", "paper's 401/213 OP-related DEG subsets need DisGeNET/OMIM gene lists not reproduced here", "NE vs Sham fitted as Sham vs NE (sign flipped)"], "results": {"joint/grp_RE_vs_NE": {"n_deg": 5, "up": 4, "down": 1, "rule": "padj < 0.05"}, "joint/grp_Sham_vs_NE": {"n_deg": 1007, "up": 340, "down": 667, "rule": "padj < 0.05"}, "pair_RE_vs_NE": {"n_deg": 152, "up": 26, "down": 126, "rule": "padj < 0.05"}, "pair_NE_vs_Sham": {"n_deg": 894, "up": 633, "down": 261, "rule": "padj < 0.05"}}, "paper_counts": {"joint/grp_RE_vs_NE": 4423, "joint/grp_Sham_vs_NE": 6697}, "comparison": {"joint/grp_RE_vs_NE": {"ours": 5, "paper": 4423}, "joint/grp_Sham_vs_NE": {"ours": 1007, "paper": 6697}}, "paper_gene_check": {"joint/grp_RE_vs_NE": {"Acp5": {"baseMean": 5953.7263, "log2FoldChange": -0.4366, "padj": 0.9999, "pvalue": 0.0772}, "Fos": {"baseMean": 447.9045, "log2FoldChange": -0.9784, "padj": 0.6898, "pvalue": 0.0071}, "Fosb": {"baseMean": 206.29, "log2FoldChange": -1.5501, "padj": null, "pvalue": null}, "Calcr": {"baseMean": 29.4624, "log2FoldChange": 0.9351, "padj": 0.9999, "pvalue": 0.0853}, "Stat1": {"baseMean": 2386.5375, "log2FoldChange": -0.566, "padj": 0.9999, "pvalue": 0.0478}}, "joint/grp_Sham_vs_NE": {"Acp5": {"baseMean": 5953.7263, "log2FoldChange": -0.3647, "padj": 0.4175, "pvalue": 0.14}, "Fos": {"baseMean": 447.9045, "log2FoldChange": -1.0055, "padj": 0.0678, "pvalue": 0.0057}, "Fosb": {"baseMean": 206.29, "log ... [146 more characters]

reasoning: Paper's primary exercise contrast is reproduced with its method and threshold.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference completed on 9 samples.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DE method",
    "paper": "DESeq2 (S2.8.p1)",
    "data": "GEO data_processing: DESeq (2012) estimateSizeFactors + nbinomTest, p <= 0.05 and FC >= 2",
    "disposition": "executable_without_change"
  },
  {
    "item": "Sample titles",
    "paper": "6 rats per group, 3 sequenced (S2.7.p1)",
    "data": "titles Sham_12/7/8, Ovx_NE_6/8/9, Ovx_RE_3/5/8 (animal numbers); counts file headers say Sham_1..; mapping by GSM accession",
    "disposition": "executable_without_change"
  },
  {
    "item": "Matrix layout",
    "paper": "counts for DESeq2",
    "data": "RAW.tar holds FPKM and counts per sample; merged file interleaves them",
    "disposition": "executable_without_change"
  }
]
