# Review packet B (the analysis' decisions): GSE254368

## Mechanical flags

- none

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| time_post_vs_pre | 34 | 34 | pvalue < 0.05 | 0 | 0 | 0 | 0 | 34 | 22 | 17 | 10 | 0.115 | 0.053 |

## Samples per design level

### `time`
- **post** (10): GSM8041096 / Plasma, post acute, Male 1 / sample.bn6_m1_pwo; GSM8041098 / Plasma, post acute, Male 2 / sample.bn8_m12_pwo; GSM8041100 / Plasma, post acute, Male 3 / sample.bn10_m17_pwo; GSM8041102 / Plasma, post acute, Male 4 / sample.bn12_m33_pwo; GSM8041104 / Plasma, post acute, Male 5 / sample.bn14_m39_pwo; GSM8041106 / Plasma, post acute, Female 1 / sample.bn16_f3_pwo; GSM8041108 / Plasma, post acute, Female 2 / sample.bn18_f2_pwo; GSM8041110 / Plasma, post acute, Female 3 / sample.bn20_f4_pwo; GSM8041112 / Plasma, post acute, Female 4 / sample.bn22_f34_pwo; GSM8041114 / Plasma, post acute, Female 5 / sample.bn24_f35_pwo
- **pre** (10): GSM8041095 / Plasma, pre acute, Male 1 / sample.bn5_m1_pre; GSM8041097 / Plasma, pre acute, Male 2 / sample.bn7_m12_pre; GSM8041099 / Plasma, pre acute, Male 3 / sample.bn9_m17_pre; GSM8041101 / Plasma, pre acute, Male 4 / sample.bn11_m33_pre; GSM8041103 / Plasma, pre acute, Male 5 / sample.bn13_m39_pre; GSM8041105 / Plasma, pre acute, Female 1 / sample.bn15_f3_pre; GSM8041107 / Plasma, pre acute, Female 2 / sample.bn17_f2_pre; GSM8041109 / Plasma, pre acute, Female 3 / sample.bn19_f4_pre; GSM8041111 / Plasma, pre acute, Female 4 / sample.bn21_f34_pre; GSM8041113 / Plasma, pre acute, Female 5 / sample.bn23_f35_pre

### `subject`
- **f2** (2): GSM8041107 / Plasma, pre acute, Female 2 / sample.bn17_f2_pre; GSM8041108 / Plasma, post acute, Female 2 / sample.bn18_f2_pwo
- **f3** (2): GSM8041105 / Plasma, pre acute, Female 1 / sample.bn15_f3_pre; GSM8041106 / Plasma, post acute, Female 1 / sample.bn16_f3_pwo
- **f34** (2): GSM8041111 / Plasma, pre acute, Female 4 / sample.bn21_f34_pre; GSM8041112 / Plasma, post acute, Female 4 / sample.bn22_f34_pwo
- **f35** (2): GSM8041113 / Plasma, pre acute, Female 5 / sample.bn23_f35_pre; GSM8041114 / Plasma, post acute, Female 5 / sample.bn24_f35_pwo
- **f4** (2): GSM8041109 / Plasma, pre acute, Female 3 / sample.bn19_f4_pre; GSM8041110 / Plasma, post acute, Female 3 / sample.bn20_f4_pwo
- **m1** (2): GSM8041095 / Plasma, pre acute, Male 1 / sample.bn5_m1_pre; GSM8041096 / Plasma, post acute, Male 1 / sample.bn6_m1_pwo
- **m12** (2): GSM8041097 / Plasma, pre acute, Male 2 / sample.bn7_m12_pre; GSM8041098 / Plasma, post acute, Male 2 / sample.bn8_m12_pwo
- **m17** (2): GSM8041099 / Plasma, pre acute, Male 3 / sample.bn9_m17_pre; GSM8041100 / Plasma, post acute, Male 3 / sample.bn10_m17_pwo
- **m33** (2): GSM8041101 / Plasma, pre acute, Male 4 / sample.bn11_m33_pre; GSM8041102 / Plasma, post acute, Male 4 / sample.bn12_m33_pwo
- **m39** (2): GSM8041103 / Plasma, pre acute, Male 5 / sample.bn13_m39_pre; GSM8041104 / Plasma, post acute, Male 5 / sample.bn14_m39_pwo

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE254368"], "assay": "small RNA-seq (TruSeq Small RNA) of plasma extracellular-vesicle RNA, STAR to miRBase v22 / Ensembl 101", "sample_inclusion": "10 participants (5 men, 5 women), plasma EVs pre and immediately post AHRET; 20 libraries", "factors": {"time": ["pre", "post"], "subject": "10 participants (repeated measures)", "sex": ["male", "female"]}, "primary_estimand": "within-subject change in plasma EV small-RNA (miRNA) abundance, post- vs pre-acute heavy resistance exercise test (6x10 back squat at 75% 1RM)", "planned_contrasts": ["time post vs pre (Abstract RESULTS; paper: 34 miRNAs altered, P < 0.05)"], "repeated_measure_unit": "participant", "paper_method": "edgeR workflow (GEO data_processing); deposited DE table has limma topTable columns (logFC, CI.L/R, t, B, adj.P.Val), consistent with edgeR-normalised voom/limma; pairing not stated in abstract", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "Abstract RESULTS: '34 miRNAs were altered by AHRET (P < 0.05)'"}, "paper_results": "34 DE miRNAs at P<0.05 -> IPA, 175 canonical pathways (P<0.01); deposited table: 46 features at P.Value<0.05 of 642 tested, 34 of them miRNA biotype, adj.P.Val all >= 0.05"}

reasoning: Only the PubMed abstract and GEO series description are available (no full text). Abstract METHODS/RESULTS give 10 participants, pre/post AHRET, DE miRNAs at P<0.05 (raw P; no FDR, no fold-change rule). GEO overall_design: 'Repeated measures study, pre- and immediate-post'. GEO data_processing: edgeR workflow.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE254368\\GSE254368_all_miRNA_counts.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 38377006", "series title equals paper title", "20 GSMs = 10 participants x pre/post, 5 male + 5 female matches abstract", "matrix column names equal metadata description for all 20 samples"], "accession": "GSE254368", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE254368\\GSE254368_metadata.csv"}

reasoning: GSE254368 is the paper's own deposit; miRNA count matrix is the input to the deposited DE table (same sample columns).

rejected alternatives: [{"value": "GSE254368_all_gene_counts.csv", "reason_rejected": "gene-level counts of all biotypes; paper analyses miRNAs, and the deposited DE table derives from the miRNA count file"}, {"value": "GSE254368_all_transcript_counts.csv", "reason_rejected": "transcript level, contains negative values; not the paper's input"}, {"value": "GSE254368_all_miRNA_differential_expression.csv", "reason_rejected": "author result table, used only for comparison"}]

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 20, "n_metadata": 20, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\aligned\\aligned_metadata.csv", "columns": {"sex": {"alias_of": "characteristics_ch1.1.Sex"}, "subject": {"source": "description", "regex": "^sample\\.bn\\d+_([mf]\\d+)_(?:pre|pwo)$"}, "time": {"source": "description", "regex": "^sample\\.bn\\d+_[mf]\\d+_(pre|pwo)$", "recode": {"pre": "pre", "pwo": "post"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\aligned\\design_metadata.csv", "sha256": "5622e795a20a0f2480859bb29036bb77af6217b18f7bac6fa9db535c673cee81", "levels": {"sex": {"male": 10, "female": 10}, "subject": {"m1": 2, "m12": 2, "m17": 2, "m33": 2, "m39": 2, "f3": 2, "f2": 2, "f4": 2, "f34": 2, "f35": 2}, "time": {"pre": 10, "post": 10}}}}

reasoning: Matrix columns 'sample.bnNN_<sex><id>_<pre|pwo>' equal metadata 'description' exactly; the pattern drops the numeric annotation column transcript_count. Subject = m1/m12/.../f35 token (each appears once pre, once pwo); time from suffix (pwo = post-workout), consistent with characteristics 'time point'.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\aligned\\aligned_matrix.csv", "sha256": "39cd73e5f539baa06dd74e1012a59ad5576ef6d125c494e92e08829c638410b2", "n_features": 7009, "n_samples": 20, "annotation_columns_dropped": [], "duplicated_feature_ids": 2, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 2775696.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values non-negative integers; GEO data_processing: STAR alignment then edgeR workflow and 'raw counts for each sample'. Paper input is raw counts to edgeR. Library sizes vary 0.12M-15.6M (one large library), handled by size-factor normalisation.

### design (valid, not_started)

final: {"analysis_type": "paired two-group (repeated measures)", "design_column": "time", "control": "pre", "treatment": "post", "contrasts": [{"name": "time_post_vs_pre", "control": "pre", "treatment": "post", "role": "primary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Abstract: DE miRNAs between pre- and post-AHRET EVs; GEO: repeated measures. Single within-subject contrast post vs pre. Sex is constant within subject and absorbed by subject blocking; per-sex analyses (5 pairs each) are exploratory.

rejected alternatives: [{"value": "characteristics_ch1.4.treatment", "reason_rejected": "same split as time point, redundant"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "sex", "disposition": "absorbed by subject (between-subject, constant within pair)"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 20, "n_columns": 11, "columns": ["Intercept", "time_pre", "subject_f3", "subject_f34", "subject_f35", "subject_f4", "subject_m1", "subject_m12", "subject_m17", "subject_m33", "subject_m39"], "rank": 11, "full_rank": true, "residual_df": 9, "levels": {"time": {"pre": 10, "post": 10}, "subject": {"m1": 2, "m12": 2, "m17": 2, "m33": 2, "m39": 2, "f3": 2, "f2": 2, "f4": 2, "f34": 2, "f35": 2}}, "cells": [{"cell": ["post", "f2"], "n": 1}, {"cell": ["post", "f3"], "n": 1}, {"cell": ["post", "f34"], "n": 1}, {"cell": ["post", "f35"], "n": 1}, {"cell": ["post", "f4"], "n": 1}, {"cell": ["post", "m1"], "n": 1}, {"cell": ["post", "m12"], "n": 1}, {"cell": ["post", "m17"], "n": 1}, {"cell": ["post", "m33"], "n": 1}, {"cell": ["post", "m39"], "n": 1}, {"cell": ["pre", "f2"], "n": 1}, {"cell": ["pre", "f3"], "n": 1}, {"cell": ["pre", "f34"], "n": 1}, {"cell": ["pre", "f35"], "n": 1}, {"cell": ["pre", "f4"], "n": 1}, {"cell": ["pre", "m1"], "n": 1}, {"cell": ["pre", "m12"], "n": 1}, {"cell": ["pre", "m17"], "n": 1}, {"cell": ["pre", "m33"], "n": 1}, {"cell": ["pre", "m39"], "n": 1}], "min_cell_size": 1, "missing_values": {}}, "confounding": [{"column": "sex", "n_levels": 2, "status": "crossed", "crosstab": {"post": {"female": 5, "male": 5}, "pre": {"f ... [25 more characters]

reasoning: Each participant contributes pre and post; subject is the blocking unit (GEO overall_design: repeated measures). Sex is nested in subject, not added separately.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald), ~ subject + time", "formula": "~ subject + time", "paper_route": {"method": "edgeR workflow / limma topTable (likely voom), pairing unknown", "status": "blocked", "reason": "Repository edgeR and limma-voom executors take a single design column (no subject blocking), and the abstract does not state the exact model or low-count filter; the paired model is run with DESeq2 and an unpaired limma-voom run is kept as sensitivity."}, "deviations": ["DESeq2 paired model instead of edgeR/limma workflow", "low-count filter CPM >= 1 in >= 10 samples, recovered from the data: it reproduces exactly the 642 features in the authors' deposited DE table (abstract does not state the filter)", "all small-RNA biotypes kept in the model as in the deposited table; miRNA-only counts reported separately"]}

reasoning: Raw counts support DESeq2; paired design needs subject blocking which only the DESeq2 executor offers among count routes.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: Abstract RESULTS: 'P < 0.05' (raw p, no FC). Audit FDR < 0.05 labelled separately.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "time_post_vs_pre", "role": "primary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\results\\time_post_vs_pre\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\results\\time_post_vs_pre\\DEG_results_post_vs_pre.csv"], "counts": {"time_post_vs_pre": {"applied": {"rule": "pvalue < 0.05", "n_tested": 642, "n_significant": 34, "n_up": 15, "n_down": 19, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 642, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paired post vs pre, subject blocking.

### execution (valid, completed)

final: {"method": "run_limma_voom_analysis", "subset": "time_post_vs_pre_voom_unpaired", "role": "sensitivity", "tool": "tools.limma_voom_tools:run_limma_voom_analysis", "n_samples": 20, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\results\\time_post_vs_pre_voom_unpaired\\input\\matrix_filtered.csv", "formula": "~ time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\results\\time_post_vs_pre_voom_unpaired\\DEG_results_post_vs_pre.csv"], "counts": {"time_post_vs_pre_voom_unpaired": {"applied": {"rule": "pvalue < 0.05", "n_tested": 642, "n_significant": 10, "n_up": 3, "n_down": 7, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 642, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Closest available to the authors' limma-style output; unpaired because the executor has no blocking.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "time_post_vs_pre_male", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\results\\time_post_vs_pre_male\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\results\\time_post_vs_pre_male\\DEG_results_post_vs_pre.csv"], "counts": {"time_post_vs_pre_male": {"applied": {"rule": "pvalue < 0.05", "n_tested": 627, "n_significant": 26, "n_up": 3, "n_down": 23, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 627, "n_significant": 1, "n_up": 0, "n_down": 1, "deg_sanity": "ok"}}}}

reasoning: Per-sex exploratory (5 pairs); paper pooled sexes.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "time_post_vs_pre_female", "role": "exploratory", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 10, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\results\\time_post_vs_pre_female\\input\\matrix_filtered.csv", "formula": "~ subject + time", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38377006\\GSE254368\\results\\time_post_vs_pre_female\\DEG_results_post_vs_pre.csv"], "counts": {"time_post_vs_pre_female": {"applied": {"rule": "pvalue < 0.05", "n_tested": 714, "n_significant": 11, "n_up": 5, "n_down": 6, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 714, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Per-sex exploratory (5 pairs); paper pooled sexes.

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Paper comparison rests on the abstract and GEO description only (no full text).", "Paper counts 34 miRNAs; our tables count all small-RNA features passing the filter, miRNA-only count reported in HANDBACK.", "Raw P < 0.05 with no multiple-testing control; the deposited author table has no feature at adj.P < 0.05.", "Sign convention: the deposited author table's logFC equals pre minus post (r = -0.94 with mean(post)-mean(pre) of its own per-sample values), so e.g. MIR23B logFC -0.37 there is an increase after exercise; our post-vs-pre log2FC agrees with the negated author logFC (r = 0.87 over the 642 shared features). Directions quoted from the author table (and possibly in the paper) are inverted relative to post-vs-pre; cannot be checked against the full text.", "Primary result: 34 features at P<0.05 of which 20 are miRNA biotype (paper: 34 miRNAs; author table: 46 features); 12 of our 20 miRNAs are among the authors' 34."], "results": {"time_post_vs_pre": {"n_deg": 34, "up": 15, "down": 19, "rule": "pvalue < 0.05", "audit_n": 0}, "time_post_vs_pre_voom_unpaired": {"n_deg": 10, "up": 3, "down": 7, "rule": "pvalue < 0.05", "audit_n": 0}, "time_post_vs_pre_male": {"n_deg": 26, "up": 3, "down": 23, "rule": "pvalue < 0.05", "audit_n": 1}, "time_post_vs_pre_female": {"n_deg": 11, "up": 5, "down": 6, "rule": "pvalue < 0.05", "audit_n": 0}}, "paper_counts": {"time_post_vs_pre": 34}, "comparison": {"time_post_vs_pre": {"ours": 34, "paper" ... [1160 more characters]

reasoning: Named miRNAs are from the deposited author DE table (P.Value < 0.05), not the abstract.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Covariance | pass | required; subject: block (same subject sampled at several levels: repeated measures); sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it); sex: omit (makes the design rank deficient) |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "pairing",
    "paper": "abstract silent; GEO: repeated measures",
    "data": "subject derivable for all 10 pairs",
    "disposition": "executable_without_change"
  },
  {
    "item": "method",
    "paper": "edgeR workflow (limma-style output)",
    "data": "raw counts",
    "disposition": "declared_deviation"
  },
  {
    "item": "feature set",
    "paper": "34 miRNAs counted; deposited table tested 642 small-RNA features",
    "data": "7009 small-RNA features before filtering",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID38377006 / GSE254368

**The comparison with the paper rests on the abstract only.** No full text was available; I used the PubMed abstract (`abstract_PMID38377006.txt`, NCBI efetch), the GEO series description (summary, overall design, data_processing), and the authors' deposited DE table `GSE254368_all_miRNA_differential_expression.csv`.

## What ran
- Route: case spec (`case_spec.json`) → `python -m tools.case_runner execute`. Status `completed`, decision contract validator 0 errors. Earlier attempts are in `_previous/`.
- Data: `GSE254368_all_miRNA_counts.csv` (raw integer counts, STAR → miRBase v22, 7009 small-RNA features × 20 plasma-EV libraries). That's 10 participants (5 M, 5 F), each sampled before and immediately after AHRET.
- Alignment: exact match of matrix columns to metadata `description`. Subject (`m1`…`f35`) and time (`pre`/`pwo` → post) come from the sample name, giving 10 complete pairs.
- Design: post vs pre within subject, with subject blocking (GEO: "Repeated measures"). Suitability verdict: analyzable.
- Low-count filter: CPM ≥ 1 in ≥ 10 samples. The abstract doesn't state a filter; I recovered this rule from the data because it keeps exactly the same 642 features as the authors' table. A first attempt used CPM ≥ 20, kept only 277 features and dropped 25 of the authors' 46 hits, so I replaced it.
- Executions:
  - **Primary:** DESeq2 `~ subject + time`.
  - **Sensitivity:** limma-voom, unpaired.
  - **Exploratory:** paired DESeq2 for each sex separately (5 pairs each).
- Enrichment: not run. The paper uses IPA target prediction on miRNAs, and running our GO/Hallmark tools on miRNA host-gene IDs would not mean the same thing.

## DEG counts vs paper (threshold: raw P < 0.05, no fold-change rule — abstract RESULTS)
| Table | Ours, all features (up/down) | Ours, miRNA biotype | Paper / author table |
|---|---|---|---|
| time_post_vs_pre (primary, paired DESeq2) | 34 (15/19) | 20 | 34 miRNAs (author table: 46 features, 34 miRNA) |
| time_post_vs_pre_voom_unpaired (sensitivity) | 10 (3/7) | 6 | — |
| time_post_vs_pre_male (exploratory) | 26 (3/23) | 11 | not reported |
| time_post_vs_pre_female (exploratory) | 11 (5/6) | 3 | not reported |

- Overlap with the authors' hits:
  - Primary: 18 of our 34 features are among the authors' 46. 12 of our 20 miRNAs are among their 34.
  - limma-voom: 9 of 10 are among the authors' hits.
- Agreement in effect size: our post-vs-pre log2FC vs the negated author logFC gives r = 0.87 ove ... [2193 more characters]
