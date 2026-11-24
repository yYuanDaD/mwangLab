# Review packet B (the analysis' decisions): GSE161030

## Mechanical flags

- **possible_reversed_contrast**: {"contrast": "grp_EHP_vs_Sed", "control": "Sed", "treatment": "EHP", "note": "the control side reads as exercise or the test side as control"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| grp_EHP_vs_Sed | 2162 | 2163 | pvalue < 0.05 and |log2FoldChange| > 1 | 6143 | 3993 | 1521 | 7463 | 8435 | 5145 | 2163 | 5749 | 0.059 | 0.303 |

## Samples per design level

### `grp`
- **EHP** (3): GSM4888677 / EHP1 / EHP1; GSM4888678 / EHP2 / EHP2; GSM4888679 / EHP3 / EHP3
- **Sed** (3): GSM4888674 / sedentary1 / Sed1; GSM4888675 / sedentary2 / Sed2; GSM4888676 / sedentary3 / Sed3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE161030"], "assay": "rRNA-depleted total RNA-seq ('lncRNA sequencing') of whole mouse heart, Illumina HiSeq 2000; transcript-level quantification (HISAT2 + StringTie)", "sample_inclusion": "3 EHP hearts (swimming 3 weeks + sedentary 1 week) and 3 sedentary hearts, male C57BL/6, collected 1 week after termination of swimming, before TAC/sham (S2.3.p1; GEO extract_protocol)", "factors": {"grp": ["Sed", "EHP"]}, "primary_estimand": "Effect of exercise hypertrophic preconditioning (21 days swimming then 1 week detraining) vs sedentary on cardiac transcript (lncRNA) expression", "planned_contrasts": ["EHP vs Sed (S2.3.p1, FIG4; paper: 2162 DE lncRNAs, 1482 up / 680 down)"], "repeated_measure_unit": "none; independent animals", "paper_method": "DESeq2 (FIG4 legend 'DESeq analysis'; GEO data_processing 'DEseq2'), ~ grp", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S2.3.p1; FIG4 legend"}, "paper_results": {"total": 2162, "up": 1482, "down": 680, "named": ["Mhrt779 up in EHP"]}}

reasoning: S2.3.p1: lncRNA sequencing in 3 EHP and 3 sedentary hearts (GSE161030); 2162 differentially expressed (1482 higher, 680 lower in EHP), |log2 FC| > 1 and P < 0.05. FIG4 legend: DESeq, >=2-fold and P < 0.05. GEO data_processing states a different rule (RPKM > 500, |log2FC| > 1, padj < 0.05) but the paper's count is reproduced exactly from the deposited DESeq2 table with raw P < 0.05 and |log2FC| > 1 (2162/1482), so the paper rule is raw P.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE161030\\GSE161030_lncRNA_EHP_vs_Sed.csv.gz", "owned": true, "checks": ["paper S2.3.p1 names GSE161030", "6 GSMs: sedentary1-3 / EHP1-3 match paper n=3+3", "matrix columns Sed1-3/EHP1-3 equal metadata description", "authors' deposited DESeq2 table has the same 27884 feature IDs as the counts filtered to row sum >= 10"], "accession": "GSE161030", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE161030\\GSE161030_metadata.csv"}

reasoning: Paper names the accession; sample groups and n match.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33757294\\GSE161030\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "description", "regex": "^(Sed|EHP)\\d$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33757294\\GSE161030\\aligned\\design_metadata.csv", "sha256": "0f0cf06c5c1b501c4188ff5c4c361cafcc59d4976b78dc0160f5fe35ae76c97f", "levels": {"grp": {"Sed": 3, "EHP": 3}}}}

reasoning: Matrix columns Sed1..EHP3 equal the metadata description column exactly (6/6). grp derived from the same field; consistent with characteristics treatment (sedentary 4w / swimming 3w +sedentary1w).

### matrix (valid, not_started)

final: {"source": "GSE161030_lncRNA_EHP_vs_Sed.csv.gz (GEO supplementary)", "paper_input": "DESeq2 on read counts", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33757294\\GSE161030\\aligned\\aligned_matrix.csv", "sha256": "1add49fda4c6a0ab19fd975e83eba5cead038e6d3f88584ac20b386aa073070d", "n_features": 46746, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 448482.0, "median": 5.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (0-448482, median 5); GEO data_processing 'Supplementary_files_format_and_content: raw counts'; StringTie transcript quantification. Authors' DESeq2 table baseMean values are consistent with these counts.

### design (valid, not_started)

final: {"analysis_type": "two-group", "design_column": "grp", "control": "Sed", "treatment": "EHP", "estimand_type": "causal", "contrasts": [{"name": "grp_EHP_vs_Sed", "control": "Sed", "treatment": "EHP", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33757294\\GSE161030\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Randomized two-arm exercise vs sedentary design, n=3 per arm, all male; single grouping column. Note the exercise arm was measured 1 week after training stopped (detraining memory estimand), as the paper intends.

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [], "design_check": {"formula_equivalent": "~ C(grp)", "n_samples": 6, "n_columns": 2, "columns": ["Intercept", "grp_Sed"], "rank": 2, "full_rank": true, "residual_df": 4, "levels": {"grp": {"Sed": 3, "EHP": 3}}, "cells": [{"cell": ["EHP"], "n": 3}, {"cell": ["Sed"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 6, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 6, "status": "sample_identifier"}, {"column": "status", "n_levels": 1, "status": "constant"}, {"column": "submission_date", "n_levels": 1, "status": "constant"}, {"column": "last_update_date", "n_levels": 1, "status": "constant"}, {"column": "type", "n_levels": 1, "status": "constant"}, {"column": "channel_count", "n_levels": 1, "status": "constant"}, {"column": "source_name_ch1", "n_levels": 1, "status": "constant"}, {"column": "organism_ch1", "n_levels": 1, "status": "constant"}, {"column": "taxid_ch1", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.0.strain", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.1.Sex", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.2.tissue", "n_levels": 1, "status": "constant"}, {"column": "characteristics_ch1.3.treatment", "n_levels": 2, "status": "complete_confounding", "crosstab": {"EHP": {"sedentary 4w": 0, "swimming 3w +sedentary1w": 3}, "Sed": {"sedentary 4w": 3, "swimming  ... [1830 more characters]

reasoning: Independent animals, one per sample; no batch, sex (all male) or lane variable recorded.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp", "paper_route": {"method": "DESeq2 ~ group", "status": "reproduced"}, "deviations": ["pydeseq2 instead of R DESeq2", "pre-filter genes with row-sum >= 10 (mean >= 10/6) to match the 27884 features in the authors' DESeq2 table; the paper does not state the filter"]}

reasoning: Paper and GEO both use DESeq2 on raw counts; the matrix supports it.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": false}}

reasoning: S2.3.p1: |log2 FC| > 1 and P < 0.05 (raw P). Audit: BH padj < 0.05 with the same fold change (closer to the GEO data_processing rule, without its RPKM > 500 filter, which cannot be applied: no RPKM deposited).

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "grp_EHP_vs_Sed", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 6, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33757294\\GSE161030\\results\\grp_EHP_vs_Sed\\input\\matrix_filtered.csv", "formula": "~ grp", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33757294\\GSE161030\\results\\grp_EHP_vs_Sed\\DEG_results_EHP_vs_Sed.csv"], "counts": {"grp_EHP_vs_Sed": {"applied": {"rule": "pvalue < 0.05 and |log2FoldChange| > 1", "n_tested": 27882, "n_significant": 2163, "n_up": 1498, "n_down": 665, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05 and |log2FoldChange| > 1", "n_tested": 20854, "n_significant": 1521, "n_up": 1031, "n_down": 490, "deg_sanity": "ok"}}}}

reasoning: Paper's two-group DESeq2; filter row-sum >= 10 to match the authors' deposited feature set.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Features are StringTie transcripts (transcript:ENSMUST...), not only lncRNAs; the paper's 2162 'lncRNAs' equal the authors' full deposited table at P<0.05 & |log2FC|>1, so all transcripts are counted.", "Paper's significance rule uses raw P with n=3 per group; many calls are not FDR-controlled (see audit count).", "Mhrt779 is not an Ensembl-annotated transcript ID in this matrix, so the paper's named gene cannot be looked up."], "results": {"grp_EHP_vs_Sed": {"n_deg": 2163, "up": 1498, "down": 665, "rule": "pvalue < 0.05 and |log2FoldChange| > 1", "audit_n": 1521}}, "paper_counts": {"grp_EHP_vs_Sed": 2162}, "comparison": {"grp_EHP_vs_Sed": {"ours": 2163, "paper": 2162}}, "paper_gene_check": {}}

reasoning: Paper-aligned reproduction of the single planned contrast.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "DEG threshold",
    "paper": "P < 0.05 and |log2FC| > 1 (S2.3.p1)",
    "data": "GEO data_processing: RPKM > 500 & |log2FC| > 1 & padj < 0.05",
    "disposition": "executable_without_change"
  },
  {
    "item": "feature set",
    "paper": "'lncRNAs'",
    "data": "all StringTie transcripts (46746; 27884 with row-sum >= 10 in the authors' table)",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID33757294 / GSE161030

**Status: finished (paper_aligned).** The validator ran on 10 records and reported 0 errors.

## What ran
- `inspect` GSE161030 found two files. The first is a raw integer count matrix of StringTie transcripts: `GSE161030_lncRNA_EHP_vs_Sed.csv.gz`, 46,746 transcripts × 6 samples (Sed1–3, EHP1–3). The second is the authors' own DESeq2 table, with 27,884 transcripts.
- Paper (S2.3.p1, FIG4) compares 3 EHP hearts with 3 sedentary hearts. EHP means 21 days of swimming followed by 1 week of detraining. The method is DESeq2, and a transcript counts as differentially expressed at P < 0.05 and |log2FC| > 1 (raw P).
- Case spec: `case_spec.json`.
  - Samples were matched exactly on the metadata `description` column (6/6), and `grp` was derived from it (Sed / EHP).
  - Raw counts were analysed with pydeseq2 using the design `~ grp`.
  - Low-count transcripts were filtered at row sum >= 10, which reproduces the authors' 27,884 features exactly.
  - No enrichment was run. The paper only ran GO on cis-target genes of the lncRNAs, and the IDs here are transcript IDs.

## DEG counts vs paper
| Contrast | Rule | Ours (up/down) | Paper (up/down) |
|---|---|---|---|
| EHP vs Sed | P<0.05 & \|log2FC\|>1 (paper, S2.3.p1) | 2163 (1498/665) | 2162 (1482/680) |
| EHP vs Sed (audit) | padj<0.05 & \|log2FC\|>1 | 1521 | – |

Compared with the authors' deposited DESeq2 table:
- log2FC correlation is r = 0.99999999 across the 27,884 shared transcripts.
- 2,139 of the paper's 2,162 calls are also in our set.
- Applying the paper rule to the deposited table gives exactly 2162 (1482/680), which confirms the threshold is raw P.

## Deviations
- We used pydeseq2, not R DESeq2. This explains the small count differences: the deposited table splits 1482/680, ours 1498/665.
- The pre-filter (row sum >= 10) is not stated in the paper. It was inferred from the size of the deposited table.
- GEO `data_processing` states a different rule: RPKM > 500, |log2FC| > 1 and padj < 0.05. That rule does not reproduce the paper's count, and no RPKM values were deposited. We applied the paper's rule and report padj < 0.05 only as the audit rule.
- The paper calls all 2162 features "lncRNAs", but the table contains every StringTie transcript, not only lncRNAs. We counted them the same way the paper did.
- The paper's key gene, Mhrt779, cannot be looked up because it has no Ensembl transcript ID in this matrix.

## Tool problems
- No blocking problems.
- Minor: `filter_l ... [158 more characters]
