# Review packet B (the analysis' decisions): GSE185530

## Mechanical flags

- **pairing_key_candidate**: {"key": "characteristics_ch1.3.treatment (eps) (without characteristics_ch1.2.treatment (lna)) + suffix of title", "across": "characteristics_ch1.2.treatment (lna)", "pairs_or_sets": 18, "samples_linked": 36, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| voom_NCeps0_vs_NCrest | 835 | 1169 | padj < 0.01 and |log2FoldChange| > 1 | 6110 | 3026 | 1260 | 7207 | 7161 | 3133 | 1271 | 5192 | 0.031 | 0.512 |
| voom_NCeps3_vs_NCrest | 1316 | 2154 | padj < 0.01 and |log2FoldChange| > 1 | 7825 | 4806 | 2216 | 8791 | 8480 | 4892 | 2221 | 6709 | 0.025 | 0.606 |

## Samples per design level

### `grp`
- **KDeps0** (6): GSM5617733 / EPS 0h Tug1-KD rep 1 / AT26; GSM5617735 / EPS 0h Tug1-KD rep 2 / AT28; GSM5617737 / EPS 0h Tug1-KD rep 3 / AT30; GSM5617747 / EPS 0h Tug1-KD rep 4 / AT40; GSM5617753 / EPS 0h Tug1-KD rep 5 / AT46; GSM5617759 / EPS 0h Tug1-KD rep 6 / AT52
- **KDeps3** (6): GSM5617739 / EPS 3h Tug1-KD rep 1 / AT32; GSM5617741 / EPS 3h Tug1-KD rep 2 / AT34; GSM5617743 / EPS 3h Tug1-KD rep 3 / AT36; GSM5617749 / EPS 3h Tug1-KD rep 4 / AT42; GSM5617755 / EPS 3h Tug1-KD rep 5 / AT48; GSM5617761 / EPS 3h Tug1-KD rep 6 / AT54
- **KDrest** (6): GSM5617727 / Rest Tug1-KD rep 1 / AT20; GSM5617729 / Rest Tug1-KD rep 2 / AT22; GSM5617731 / Rest Tug1-KD rep 3 / AT24; GSM5617745 / Rest Tug1-KD rep 4 / AT38; GSM5617751 / Rest Tug1-KD rep 5 / AT44; GSM5617757 / Rest Tug1-KD rep 6 / AT50
- **NCeps0** (6): GSM5617732 / EPS 0h Control rep 1 / AT25; GSM5617734 / EPS 0h Control rep 2 / AT27; GSM5617736 / EPS 0h Control rep 3 / AT29; GSM5617746 / EPS 0h Control rep 4 / AT39; GSM5617752 / EPS 0h Control rep 5 / AT45; GSM5617758 / EPS 0h Control rep 6 / AT51
- **NCeps3** (6): GSM5617738 / EPS 3h Control rep 1 / AT31; GSM5617740 / EPS 3h Control rep 2 / AT33; GSM5617742 / EPS 3h Control rep 3 / AT35; GSM5617748 / EPS 3h Control rep 4 / AT41; GSM5617754 / EPS 3h Control rep 5 / AT47; GSM5617760 / EPS 3h Control rep 6 / AT53
- **NCrest** (6): GSM5617726 / Rest Control rep 1 / AT19; GSM5617728 / Rest Control rep 2 / AT21; GSM5617730 / Rest Control rep 3 / AT23; GSM5617744 / Rest Control rep 4 / AT37; GSM5617750 / Rest Control rep 5 / AT43; GSM5617756 / Rest Control rep 6 / AT49

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE185530"], "assay": "bulk RNA-seq, poly-A stranded, NovaSeq 6000, C2C12 mouse myotubes (S5.8.p1)", "primary_estimand": "Transcriptional response of control-LNA C2C12 myotubes to in-vitro simulated exercise (3 h electrical pulse stimulation), immediately after (EPS 0h) and after 3 h recovery (EPS 3h), each versus Rest (S2.5.p2, FIG7)", "factors": {"LNA": ["Negative control", "Tug1 KD"], "EPS": ["Rest", "EPS 0h", "EPS 3h"]}, "sample_inclusion": "36 libraries = 2 LNA x 3 EPS conditions x 6 (triplicate wells from two independent experiments) (S5.8.p1, FIG7 legend)", "planned_contrasts": ["Control EPS 0h vs Control Rest (S2.5.p2; paper: 835 genes UP, log2FC>1, FDR<0.01)", "Control EPS 3h vs Control Rest (S2.5.p2; paper: 1316 genes UP, log2FC>1, FDR<0.01)", "Tug1 KD vs Control at Rest (S2.5.p1; 867 DEGs FDR<0.01) - not an exercise contrast, out of scope", "EPS response in Tug1 KD vs control (FIG7E/F, blunted/augmented genes) - modulation of the exercise response, exploratory here"], "repeated_measure_unit": "none; each library is one well (independent cultures); wells come from two independent experiments (S5.8.p1)", "normalization": "Degust voom/limma; genes with >=1 RPM in >=12 of 36 libraries (S5.8.p2)", "paper_method": "limma-voom in Degust v4.1.5 on the 36 libraries (S5.8.p2)", "paper_threshold": {"metric": "FDR", "adjustment": "BH", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false, "direction": "up only counted", " ... [242 more characters]

reasoning: Exercise question = EPS vs Rest within control-LNA myotubes, the counts the paper reports in S2.5.p2. Threshold stated there: log2FC>1, FDR<0.01, upregulated genes only. FIG7 legend says FDR<0.001 for the volcano colouring and methods (S5.8.p2) give a general FDR<0.05; the text rule matches the reported counts, so it is used. KD-at-rest (867 DEGs) is not an exercise estimand.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE185530\\GSE185530_AT_raw_gene_counts_matrix.txt.gz", "owned": true, "checks": ["S11.p1 names GSE185530", "GEO metadata: C2C12 myotubes, LNA Negative control/Tug1 x EPS Rest/EPS 0h/EPS 3h, 6 per cell, 36 total = paper's 36 libraries", "matrix has 36 count columns AT19-AT54 matching metadata description field"], "accession": "GSE185530", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE185530\\GSE185530_metadata.csv"}

reasoning: Data availability statement S11.p1 cites GSE185530; sample structure matches S5.8.p1/S5.8.p2 (36 libraries).

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 36, "n_metadata": 36, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\aligned\\aligned_metadata.csv", "columns": {"lna": {"alias_of": "characteristics_ch1.2.treatment (lna)", "recode": {"Negative control": "NC", "Tug1": "KD"}}, "eps": {"alias_of": "characteristics_ch1.3.treatment (eps)", "recode": {"Rest": "Rest", "EPS 0h": "EPS0", "EPS 3h": "EPS3"}}, "exp": {"source": "title", "regex": "rep (\\d)$", "recode": {"1": "E1", "2": "E1", "3": "E1", "4": "E2", "5": "E2", "6": "E2"}}, "grp": {"combine": ["lna", "eps"], "separator": "_", "of": "recoded values", "recode": {"NC_Rest": "NCrest", "NC_EPS0": "NCeps0", "NC_EPS3": "NCeps3", "KD_Rest": "KDrest", "KD_EPS0": "KDeps0", "KD_EPS3": "KDeps3"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\aligned\\design_metadata.csv", "sha256": "9429a3db8816ba80e7475433ac95a98f76a3be6c9605dccf5047ec1bb219a2fe", "levels": {"lna": {"NC": 18, "KD": 18}, "eps": {"Rest": 12, "EPS0": 12, "EPS3": 12}, "exp": {"E1": 18, "E2": 18}, "grp": {"NCrest": 6, "KDrest": 6, "NCeps0": 6, "KDeps0": 6, "NCeps3": 6, "KDeps3": 6}}}}

reasoning: Matrix columns (AT19..AT54) equal metadata 'description' exactly (inspect alignment_keys 36/36). grp combines LNA and EPS into six cells. exp (E1 = rep 1-3, E2 = rep 4-6) is an INFERRED experiment label from replicate numbering and library order (AT19-36 then AT37-54); used only in a sensitivity model.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "limma-voom", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\aligned\\aligned_matrix.csv", "sha256": "66baa13a9e9b108f62546c63e42948508d8b8f2e9b51ed3cbd5620a7b2cbb080", "n_features": 55416, "n_samples": 36, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 386893.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: File named raw_gene_counts_matrix; all values integers 0..386893, median 0 over 55,416 Ensembl genes; data_processing: STAR 2-pass alignment with gene-level quantification; paper analysed with voom which takes raw counts (S5.8.p2).

### design (valid, not_started)

final: {"analysis_type": "multi-group (6 cells, 2 LNA x 3 EPS); planned contrasts within control LNA", "design_column": "grp", "contrasts": [{"name": "grp_NCeps0_vs_NCrest", "control": "NCrest", "treatment": "NCeps0", "role": "primary"}, {"name": "grp_NCeps3_vs_NCrest", "control": "NCrest", "treatment": "NCeps3", "role": "primary"}, {"name": "grp_KDeps0_vs_KDrest", "control": "KDrest", "treatment": "KDeps0", "role": "exploratory"}, {"name": "grp_KDeps3_vs_KDrest", "control": "KDrest", "treatment": "KDeps3", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\suitability\\suitability.md", "n_comparisons": 15, "n_analyzable": 15}}

reasoning: Paper reports EPS 0h and EPS 3h vs Rest in control myotubes (S2.5.p2). One control level with two time points -> planned contrasts against the same Rest reference, never pooled. The EPS response in Tug1 KD myotubes is shown in FIG7E/F; run as exploratory.

rejected alternatives: [{"value": "pool LNA arms for EPS vs Rest", "reason_rejected": "paper's EPS counts are within control myotubes (S2.5.p2); Tug1 KD changes the EPS response"}, {"value": "Tug1 KD vs control at Rest", "reason_rejected": "not an exercise estimand (knockdown effect)"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "exp", "disposition": "excluded: experiment label inferred from replicate numbering, not documented in GEO; paper (Degust) did not adjust; balanced 3+3 in every cell; tested in a DESeq2 sensitivity model"}], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 36, "n_columns": 6, "columns": ["Intercept", "grp_KDeps3", "grp_KDrest", "grp_NCeps0", "grp_NCeps3", "grp_NCrest"], "rank": 6, "full_rank": true, "residual_df": 30, "levels": {"grp": {"NCrest": 6, "KDrest": 6, "NCeps0": 6, "KDeps0": 6, "NCeps3": 6, "KDeps3": 6}}, "cells": [{"cell": ["KDeps0"], "n": 6}, {"cell": ["KDeps3"], "n": 6}, {"cell": ["KDrest"], "n": 6}, {"cell": ["NCeps0"], "n": 6}, {"cell": ["NCeps3"], "n": 6}, {"cell": ["NCrest"], "n": 6}], "min_cell_size": 6, "missing_values": {}}, "confounding": [{"column": "exp", "n_levels": 2, "status": "crossed", "crosstab": {"KDeps0": {"E1": 3, "E2": 3}, "KDeps3": {"E1": 3, "E2": 3}, "KDrest": {"E1": 3, "E2": 3}, "NCeps0": {"E1": 3, "E2": 3}, "NCeps3": {"E1": 3, "E2": 3}, "NCrest": {"E1": 3, "E2": 3}}}]}

reasoning: Each library is a separate well; no subject pairing. Two independent experiments (S5.8.p1) are balanced across all six cells, so they cannot confound EPS; the paper did not block.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "limma-voom (R limma::voom + eBayes), two-arm fits", "formula": "~ grp (two levels per fit)", "paper_route": {"method": "limma-voom in Degust 4.1.5, TMM, one model on 36 libraries", "status": "blocked", "reason": "repository voom executor fits only the two contrast arms and uses colSums library sizes (no TMM; tools/limma_voom.R header); no multi-group voom executor exists"}, "deviations": ["voom fitted per contrast on 12 samples instead of one 36-sample model (variance pooled over 12 samples)", "library sizes = colSums, no TMM", "low-count filter applied as in the paper (>=1 CPM in >=12 of 36 libraries) on all 36 samples before subsetting"]}

reasoning: Paper used voom on raw counts (S5.8.p2); raw counts allow it, so the paper's method family is reproduced with declared executor deviations. DESeq2 joint model on all 36 samples (with and without exp) runs as sensitivity.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}, "deviation_note": "Paper counts only upregulated genes; compare with our 'up' count. Audit = methods' general FDR<0.05 (S5.8.p2)."}

reasoning: S2.5.p2: 'log2FC>1, FDR<0.01' for the EPS counts.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "voom_NCeps0_vs_NCrest", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\voom_NCeps0_vs_NCrest\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\voom_NCeps0_vs_NCrest\\DEG_results_NCeps0_vs_NCrest.csv"], "counts": {"voom_NCeps0_vs_NCrest": {"applied": {"rule": "padj < 0.01 and |log2FoldChange| > 1", "n_tested": 13995, "n_significant": 1169, "n_up": 778, "n_down": 391, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13995, "n_significant": 6110, "n_up": 2419, "n_down": 3691, "deg_sanity": "ok"}}}}

reasoning: paper's voom route, control myotubes EPS 0h vs Rest

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "voom_NCeps3_vs_NCrest", "role": "primary", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\voom_NCeps3_vs_NCrest\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\voom_NCeps3_vs_NCrest\\DEG_results_NCeps3_vs_NCrest.csv"], "counts": {"voom_NCeps3_vs_NCrest": {"applied": {"rule": "padj < 0.01 and |log2FoldChange| > 1", "n_tested": 13995, "n_significant": 2154, "n_up": 1130, "n_down": 1024, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13995, "n_significant": 7825, "n_up": 2513, "n_down": 5312, "deg_sanity": "implausible_sig_fraction=56%(7825/13995)"}}}}

reasoning: paper's voom route, control myotubes EPS 3h vs Rest

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_joint", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\deseq2_joint\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\deseq2_joint\\DEG_results_grp_NCeps0_vs_NCrest.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\deseq2_joint\\DEG_results_grp_NCeps3_vs_NCrest.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\deseq2_joint\\DEG_results_grp_KDeps0_vs_KDrest.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\deseq2_joint\\DEG_results_grp_KDeps3_vs_KDrest.csv"], "counts": {"deseq2_joint/grp_NCeps0_vs_NCrest": {"applied": {"rule": "padj < 0.01 and |log2FoldChange| > 1", "n_tested": 13995, "n_significant": 1221, "n_up": 908, "n_down": 313, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13995, "n_significant": 5677, "n_up": 3066, "n_down": 2611, "deg_sanity": "ok"}}, "deseq2_joint/grp_NCeps3_vs_NCrest": {"applied": {"rule": "padj < 0.01 and |log2FoldChange| > 1", "n_tested": 13995, "n_significant": 2014, "n_up": 1377, "n_down": 637, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13995, "n_significant": 743 ... [765 more characters]

reasoning: one DESeq2 model on all 36 libraries (closer to the paper's single-model variance pooling); KD EPS contrasts exploratory

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "deseq2_joint_exp", "role": "sensitivity", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 36, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\deseq2_joint_exp\\input\\matrix_filtered.csv", "formula": "~ exp + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\deseq2_joint_exp\\DEG_results_grp_NCeps0_vs_NCrest.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35850762\\GSE185530\\results\\deseq2_joint_exp\\DEG_results_grp_NCeps3_vs_NCrest.csv"], "counts": {"deseq2_joint_exp/grp_NCeps0_vs_NCrest": {"applied": {"rule": "padj < 0.01 and |log2FoldChange| > 1", "n_tested": 13995, "n_significant": 1239, "n_up": 913, "n_down": 326, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13995, "n_significant": 6942, "n_up": 3540, "n_down": 3402, "deg_sanity": "ok"}}, "deseq2_joint_exp/grp_NCeps3_vs_NCrest": {"applied": {"rule": "padj < 0.01 and |log2FoldChange| > 1", "n_tested": 13995, "n_significant": 2033, "n_up": 1384, "n_down": 649, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 13995, "n_significant": 8488, "n_up": 4271, "n_down": 4217, "deg_sanity": "implausible_sig_fraction=61%(8488/13995)"}}}}

reasoning: adds the inferred independent-experiment label as a covariate

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["paper counts are upregulated genes only", "voom executor without TMM and fitted on two arms", "exp batch label inferred, sensitivity only"], "results": {"voom_NCeps0_vs_NCrest": {"n_deg": 1169, "up": 778, "down": 391, "rule": "padj < 0.01 and |log2FoldChange| > 1", "audit_n": 6110}, "voom_NCeps3_vs_NCrest": {"n_deg": 2154, "up": 1130, "down": 1024, "rule": "padj < 0.01 and |log2FoldChange| > 1", "audit_n": 7825}, "deseq2_joint/grp_NCeps0_vs_NCrest": {"n_deg": 1221, "up": 908, "down": 313, "rule": "padj < 0.01 and |log2FoldChange| > 1", "audit_n": 5677}, "deseq2_joint/grp_NCeps3_vs_NCrest": {"n_deg": 2014, "up": 1377, "down": 637, "rule": "padj < 0.01 and |log2FoldChange| > 1", "audit_n": 7439}, "deseq2_joint/grp_KDeps0_vs_KDrest": {"n_deg": 1524, "up": 1173, "down": 351, "rule": "padj < 0.01 and |log2FoldChange| > 1", "audit_n": 6607}, "deseq2_joint/grp_KDeps3_vs_KDrest": {"n_deg": 2203, "up": 1602, "down": 601, "rule": "padj < 0.01 and |log2FoldChange| > 1", "audit_n": 7389}, "deseq2_joint_exp/grp_NCeps0_vs_NCrest": {"n_deg": 1239, "up": 913, "down": 326, "rule": "padj < 0.01 and |log2FoldChange| > 1", "audit_n": 6942}, "deseq2_joint_exp/grp_NCeps3_vs_NCrest": {"n_deg": 2033, "up": 1384, "down": 649, "rule": "padj < 0.01 and |log2FoldChange| > 1", "audit_n": 8488}}, "paper_counts": {"voom_NCeps0_vs_NCrest": 835, "voom_NCeps3_vs_NCrest": 1316}, "comparison": {"voom_NCeps0_vs_NCrest": {"ours": 1169, "paper": 835}, "voom_NCeps3_vs_NC ... [859 more characters]

reasoning: Paper genes given as Ensembl IDs (matrix IDs); symbols resolved in HANDBACK from Gene_name column.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 36 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "threshold",
    "paper": "S2.5.p2 log2FC>1 FDR<0.01; FIG7 legend FDR<0.001; S5.8.p2 FDR<0.05",
    "data": "n/a",
    "disposition": "text rule used (matches the reported counts); FDR<0.05 as audit"
  },
  {
    "item": "model",
    "paper": "Degust voom, TMM, all 36 libraries",
    "data": "executor: two-arm voom, no TMM",
    "disposition": "declared deviation; DESeq2 36-sample joint model as sensitivity"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID35850762 / GSE185530

The paper is Trewin et al., "Long non-coding RNA Tug1 modulates mitochondrial and myogenic responses to exercise in skeletal muscle" (PMC9295458). The case ran to completion through the case-spec route. The decision-contract validator reported 13 records and 0 errors.

## What ran

- **Data:** C2C12 myotubes, 36 libraries. The design is 2 LNA arms (negative control, Tug1 knockdown) x 3 EPS states (Rest, EPS 0h, EPS 3h), with n = 6 per cell. The matrix is `GSE185530_AT_raw_gene_counts_matrix.txt.gz`: integer STAR gene counts, 55,416 Ensembl genes. Columns were aligned exactly on the metadata `description` field (AT19..AT54), 36/36.
- **Estimand (paper S2.5.p2):** simulated exercise (3 h electrical pulse stimulation) versus Rest in control-LNA myotubes, at EPS 0h and at EPS 3h. These are the primary contrasts. The Tug1-knockdown EPS contrasts run as exploratory, and the knockdown-at-rest contrast is out of scope because it is not about exercise.
- **Low-count filter:** the paper's rule (at least 1 CPM in at least 12 of the 36 libraries, S5.8.p2) was applied to all 36 samples. 13,995 genes were kept.
- **Primary:** limma-voom (R), fitted separately for each contrast on its 12 samples.
- **Sensitivity:**
  - one DESeq2 model on all 36 samples (`~grp`, 6 levels);
  - the same model plus an inferred experiment covariate `exp` (rep 1-3 = E1, rep 4-6 = E2).
- **Threshold:** the paper's text rule, FDR < 0.01 and log2FC > 1 (S2.5.p2). The paper counts **upregulated genes only**. The audit rule is FDR < 0.05 with no fold-change cutoff.
- **Enrichment:** not run. The paper gives no pathway result for the EPS contrasts; its PANTHER GO analysis is for the knockdown-at-rest contrast.

## DEGs vs paper (FDR < 0.01, log2FC > 1, upregulated)

| Contrast | Paper (up) | voom primary (up / down) | DESeq2 joint (up) | DESeq2 + exp (up) |
|---|---|---|---|---|
| Control EPS 0h vs Rest | 835 | 778 / 391 | 908 | 913 |
| Control EPS 3h vs Rest | 1316 | 1130 / 1024 | 1377 | 1384 |
| Tug1 KD EPS 0h vs Rest (exploratory) | not reported | - | 1173 | - |
| Tug1 KD EPS 3h vs Rest (exploratory) | not reported | - | 1602 | - |

The paper's named genes agree with our results:

- At EPS 0h, Hspa1a, Atf3 and Nr4a3 are up (log2FC 3.18, 1.30 and 2.48; padj ≤ 2e-6).
- At EPS 3h, Gabpa is up but just under the fold-change rule (log2FC 0.99, padj 6e-6).
- At EPS 3h, Ppargc1a is not differentially expressed (padj 0.99), and Tfam is not up (padj 0.07).
- At EPS  ... [1898 more characters]
