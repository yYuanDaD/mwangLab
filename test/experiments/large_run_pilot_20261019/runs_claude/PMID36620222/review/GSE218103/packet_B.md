# Review packet B (the analysis' decisions): GSE218103

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.1.group", "n_values": 4, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pvalues_piled_near_1**: {"table": "joint/time_post_vs_pre_geno-CP", "frac_p_gt_0.9": 0.209, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}
- **other_rule_matches_paper**: {"table": "joint/geno_CP_vs_TD_time-post", "paper": 4, "applied": 1, "applied_rule": "padj < 0.05", "closest_rule": "padj<0.1", "closest_n": 4, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.1.group", "pairs_or_sets": 3, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/time_post_vs_pre_geno-TD | 0 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 10 | 10 | 6 | 4 | 0.199 | 0.034 |
| joint/time_post_vs_pre_geno-CP | 0 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 9 | 9 | 7 | 1 | 0.209 | 0.03 |
| joint/geno_CP_vs_TD_time-pre | 4 | 4 | padj < 0.05 | 4 | 4 | 4 | 4 | 20 | 20 | 17 | 8 | 0.077 | 0.067 |
| joint/geno_CP_vs_TD_time-post | 4 | 1 | padj < 0.05 | 1 | 1 | 1 | 4 | 13 | 13 | 13 | 7 | 0.141 | 0.044 |

## Samples per design level

### `geno`
- **CP** (6): GSM6734690 / Cerebral palsy control 1; GSM6734691 / Cerebral palsy control 2; GSM6734692 / Cerebral palsy control 3; GSM6734696 / Cerebral palsy exercise 1; GSM6734697 / Cerebral palsy exercise 2; GSM6734698 / Cerebral palsy exercise 3
- **TD** (6): GSM6734687 / Typically developed control 1; GSM6734688 / Typically developed control 2; GSM6734689 / Typically developed control 3; GSM6734693 / Typically developed exercise 1; GSM6734694 / Typically developed exercise 2; GSM6734695 / Typically developed exercise 3

### `time`
- **post** (6): GSM6734693 / Typically developed exercise 1; GSM6734694 / Typically developed exercise 2; GSM6734695 / Typically developed exercise 3; GSM6734696 / Cerebral palsy exercise 1; GSM6734697 / Cerebral palsy exercise 2; GSM6734698 / Cerebral palsy exercise 3
- **pre** (6): GSM6734687 / Typically developed control 1; GSM6734688 / Typically developed control 2; GSM6734689 / Typically developed control 3; GSM6734690 / Cerebral palsy control 1; GSM6734691 / Cerebral palsy control 2; GSM6734692 / Cerebral palsy control 3

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE219100 (SuperSeries)", "GSE218103 (EV small-RNA-seq, human)", "GSE219099 (C2C12 miR-486 mimic RNA-seq, mouse)"], "assay": "small RNA-seq of plasma extracellular-vesicle RNA (miRBase v22, featureCounts raw counts)", "primary_estimand": "Effect of one acute aerobic exercise bout (45 min cycling in TD, 45 min Frame Running in CP) on EV microRNA cargo: 30 min post vs pre within TD EX and within CP EX; secondary (associational) CP vs TD at baseline and post-exercise", "sample_inclusion": "Only TD EX (n=10) and CP EX (n=9) participants were sequenced; pre and post samples pooled to N=3 pools per timepoint per group (TD: 2 pools of 3 men, 1 pool of 4 women; CP: 3 pools by GMFCS II/III/IV) (S2.6.p1). TD CON participants (no-exercise controls) were NOT sequenced.", "factors": {"genotype": ["TD", "CP"], "time": ["pre", "post (30 min)"]}, "repeated_measure_unit": "pool of participants; the same pools are sampled pre and post, but which GEO pool index corresponds across timepoints is not documented", "planned_contrasts": ["TD post vs pre (S3.3.p1 'Exercise did not affect EV cargo in any of the groups', Supp Fig S2; paper: 0 DE miRNAs)", "CP post vs pre (S3.3.p1, S4.p7; paper: 0 DE miRNAs)", "CP vs TD at baseline (S3.3.p1, FIG2A/B: miR-486 up; let-7a, let-7b, let-7e down)", "CP vs TD post-exercise (S3.3.p1, FIG2C/D: miR-486, miR-100 up; miR-877, miR-4433 down)"], "normalization": "DESeq2 size factors; miRNAs with < 10 counts removed (S2.9.p2)", "paper_method": "DESeq2  ... [369 more characters]

reasoning: S2.6.p1 describes the pooling (N=3 per timepoint per group for TD EX and CP EX) and names GSE219100. S2.9.p2 gives DESeq2 on raw featureCounts counts, <10-count filter, genotype + activity model, BH-adjusted p < 0.05 with no fold-change rule. S3.3.p1/S4.p7 state exercise did not change EV miRNA cargo; FIG2 gives the CP vs TD miRNAs. The C2C12 miR-486 mimic experiment (S2.8.p1, GSE219099) is a mechanistic follow-up, not an exercise contrast.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["series_id = GSE218103,GSE219100 (sub-series of the SuperSeries the paper names in S2.6.p1/DA.p1)", "12 samples = 2 genotypes (TD, CP) x 2 timepoints x 3 pools, matching S2.6.p1", "source: Extracellular vesicles from plasma; small RNA-seq on NextSeq 500 as in S2.9.p2", "data_processing: miRBase v22 / featureCounts raw counts / DESeq2, matching S2.9.p2"], "accession": "GSE218103", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE218103\\GSE218103_metadata.csv"}

reasoning: GSE218103 is the EV small-RNA-seq sub-series of GSE219100 (named in S2.6.p1 and DA.p1); sample structure and processing match the paper.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\aligned\\aligned_metadata.csv", "columns": {"geno": {"source": "characteristics_ch1.1.group", "regex": "^(TD|CP) (?:CON|EX)$"}, "time": {"source": "characteristics_ch1.1.group", "regex": "^(?:TD|CP) (CON|EX)$", "recode": {"CON": "pre", "EX": "post"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\aligned\\design_metadata.csv", "sha256": "d9b3dad4e61101a4e8c9a2c5fad625f5c51686b56fe6997e9072ecfff750d750", "levels": {"geno": {"TD": 6, "CP": 6}, "time": {"pre": 6, "post": 6}}}}

reasoning: Tar columns become GSM ids and match the metadata index exactly (12/12). GEO 'CON' (treatment: control) denotes the pre-exercise (rest) sample, not the paper's TD CON no-exercise group: S2.6.p1 says only TD EX and CP EX were sequenced, pre and post, as N=3 pools per timepoint; a 'CP CON' group does not exist in the study design (S2.1.p1), and treatment_protocol reads 'Blood was collected before and 30 minutes after a bout of aerobic exercise'. So CON -> pre, EX -> post.

rejected alternatives: [{"value": "GEO CON = paper's TD CON no-exercise group", "reason_rejected": "the paper has no CP CON group and states only TD EX and CP EX were sequenced (S2.1.p1, S2.6.p1)"}]

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\aligned\\aligned_matrix.csv", "sha256": "da2b05a72ef289470f1539d454b7a5e2ead70d87cc4c90bb10b75fe987ecd2db", "n_features": 399, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 206977.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (integer_fraction 1.0, max 206977); data_processing: 'Raw counts were acquired with featurecounts ... used as input ... using DESeq2'; per-sample files hold miRNA ID + one count column. Matches the paper's stated input (S2.9.p2). Library sizes are small (10k-285k mapped miRNA reads, 399 miRNAs).

### design (valid, not_started)

final: {"analysis_type": "factorial (genotype x time), one model on all 12 pooled samples", "formula": "~ grp (4 cells: geno x time)", "contrasts": [{"name": "TD post vs pre", "role": "primary"}, {"name": "CP post vs pre", "role": "primary"}, {"name": "CP vs TD at pre", "role": "secondary", "estimand_type": "associational"}, {"name": "CP vs TD at post", "role": "secondary", "estimand_type": "associational"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\suitability\\suitability.md", "n_comparisons": 5, "n_analyzable": 5}}

reasoning: The exercise estimand is the within-genotype time effect (post vs pre), which the paper reports as null (S3.3.p1, S4.p7). The paper's model includes genotype and activity (S2.9.p2) and reports between-genotype comparisons at each time (FIG2), so one model over the four geno x time cells with the four pairwise contrasts reproduces it. CP vs TD is a cross-sectional comparison (associational), not an exercise effect. n = 3 pools per cell.

rejected alternatives: [{"value": "additive ~ geno + time", "reason_rejected": "the paper reports group-specific exercise and time-specific genotype comparisons, which need the cell-means (interaction) parameterisation"}, {"value": "pool exercise samples of TD and CP vs all pre samples", "reason_rejected": "pools biologically distinct groups; the paper analyses exercise within group"}]

### covariance (valid, not_started)

final: {"status": "not_required", "blocking_terms": [], "covariates": [{"name": "pool (repeated pre/post)", "disposition": "excluded: the pre and post samples come from the same participant pools, but GEO does not document which pre pool matches which post pool (titles are only 'control 1..3' / 'exercise 1..3'; no sex/GMFCS label per pool) and the profiles show no index correspondence (pre/post log-CPM correlations do not peak on the diagonal); the paper's DESeq2 model has no pool term (S2.9.p2). Ignoring positive within-pool correlation makes the post-vs-pre test conservative, not anti-conservative."}, {"name": "sex", "disposition": "excluded: pooled by sex in TD only (2 male pools, 1 female pool) and not labelled per pool; not recorded in metadata"}, {"name": "GMFCS level", "disposition": "excluded: defines the CP pools only, not labelled per sample"}], "design_check": {"formula_equivalent": "~ C(geno) + C(time)", "n_samples": 12, "n_columns": 3, "columns": ["Intercept", "geno_TD", "time_pre"], "rank": 3, "full_rank": true, "residual_df": 9, "levels": {"geno": {"TD": 6, "CP": 6}, "time": {"pre": 6, "post": 6}}, "cells": [{"cell": ["CP", "post"], "n": 3}, {"cell": ["CP", "pre"], "n": 3}, {"cell": ["TD", "post"], "n": 3}, {"cell": ["TD", "pre"], "n": 3}], "min_cell_size": 3, "missing_values": {}}, "confounding": [{"column": "title", "n_levels": 12, "status": "sample_identifier"}, {"column": "geo_accession", "n_levels": 12, "status": "sample_identifier"}, {"column": "status", "n_leve ... [2614 more characters]

reasoning: The paper's model (S2.9.p2) has genotype and activity only. A pool blocking term would be preferable, but the cross-timepoint pool mapping is not identifiable from GEO, and guessing it by index would risk a wrong subject mapping. The unpaired fit follows the paper and is conservative for the exercise contrasts; this is recorded as a caveat.

rejected alternatives: [{"value": "~ pool + grp with pool = index within genotype", "reason_rejected": "pool correspondence across timepoints is undocumented and not supported by the expression correlations; a wrong mapping would invalidate the blocking"}]

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, one model on all 12 samples)", "formula": "~ grp (geno x time cells)", "paper_route": {"method": "DESeq2 (R 3.6.2) genotype + activity model, rows with < 10 counts removed", "status": "reproduced", "reason": "pydeseq2 instead of R DESeq2; low-count filter applied as total count >= 10 across the 12 samples"}, "deviations": ["pydeseq2 port instead of Bioconductor DESeq2", "'less than 10 counts' read as row total < 10 (the DESeq2 vignette idiom rowSums >= 10), encoded as mean count >= 0.8333 over 12 samples"]}

reasoning: Raw integer counts support DESeq2, which is the paper's method (S2.9.p2).

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": false}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_cutoff": null, "inclusive": false}}

reasoning: S2.9.p2: 'statistically significant at an adjusted p < 0.05 (FDR: Benjamini-Hochberg)'; no fold-change rule. Raw p < 0.05 is reported only as a labelled audit count.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 12, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\results\\joint\\input\\matrix_filtered.csv", "formula": "~ cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\results\\joint\\DEG_results_geno_CP_vs_TD_time-post.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\results\\joint\\DEG_results_geno_CP_vs_TD_time-pre.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\results\\joint\\DEG_results_time_post_vs_pre_geno-CP.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\results\\joint\\DEG_results_time_post_vs_pre_geno-TD.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36620222\\GSE218103\\results\\joint\\DEG_results_geno_time_CP_post_vs_TD_pre.csv"], "counts": {"joint/geno_CP_vs_TD_time-post": {"applied": {"rule": "padj < 0.05", "n_tested": 297, "n_significant": 1, "n_up": 1, "n_down": 0, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested": 297, "n_significant": 13, "n_up": 7, "n_down": 6, "deg_sanity": "ok"}}, "joint/geno_CP_vs_TD_time-pre": {"applied": {"rule": "padj < 0.05", "n_tested": 297, "n_significant": 4, "n_up": 1, "n_down": 3, "deg_sanity": "ok"}, "audit": {"rule": "pvalue < 0.05", "n_tested" ... [889 more characters]

reasoning: One DESeq2 model over the four geno x time cells, all pairwise comparisons the suitability report lists; the within-genotype time contrasts are the exercise estimand, the between-genotype ones are associational.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["Pre and post samples are the same participant pools; pool correspondence is undocumented, so the model treats them as independent (as the paper's model does). The exercise tests are conservative.", "Each cell has only 3 pools of 3-4 participants; library sizes are small (10k-285k miRNA reads; CPE2 has ~10k).", "CP vs TD contrasts are associational (cross-sectional genotype difference), not exercise effects.", "Post-exercise CP vs TD: miR-100-5p (up), miR-877-5p and miR-4433b-5p (down) match the paper's direction but have padj 0.056-0.067, just above the paper's FDR 0.05."], "results": {"joint/geno_CP_vs_TD_time-post": {"n_deg": 1, "up": 1, "down": 0, "rule": "padj < 0.05", "audit_n": 13}, "joint/geno_CP_vs_TD_time-pre": {"n_deg": 4, "up": 1, "down": 3, "rule": "padj < 0.05", "audit_n": 20}, "joint/time_post_vs_pre_geno-CP": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 9}, "joint/time_post_vs_pre_geno-TD": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 10}, "joint/geno_time_CP_post_vs_TD_pre": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05", "audit_n": 4}}, "paper_counts": {"joint/time_post_vs_pre_geno-TD": 0, "joint/time_post_vs_pre_geno-CP": 0, "joint/geno_CP_vs_TD_time-pre": 4, "joint/geno_CP_vs_TD_time-post": 4}, "comparison": {"joint/time_post_vs_pre_geno-TD": {"ours": 0, "paper": 0}, "joint/time_post_vs_pre_geno-CP": {"ours": 0, "paper": 0}, "joint/geno_CP_vs_TD_time-pre": {"ours": 4 ... [1107 more characters]

reasoning: Method, model, filter and threshold follow S2.9.p2; the pool-pairing limitation is shared with the paper. Paper counts: 0 exercise-responsive miRNAs in TD and CP (S3.3.p1, S4.p7); CP vs TD counts are the miRNAs the paper names (ABS.p1, S3.3.p1: 4 at baseline - miR-486 up, let-7a/b/e down; 4 post - miR-486, miR-100 up, miR-877, miR-4433(b) down); the complete lists are in Supplementary Table S1, which is not available here. The 5th suitability comparison geno_time_CP_post_vs_TD_pre is the geno x time interaction (difference in exercise response CP vs TD), run as exploratory; the paper does not report it.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "meaning of GEO 'control' samples",
    "paper": "TD CON = separate no-exercise participants (S2.1.p1), not sequenced (S2.6.p1)",
    "data": "GEO 'TD CON'/'CP CON' with treatment 'control' = pre-exercise pools",
    "disposition": "executable_without_change"
  },
  {
    "item": "pre/post pool pairing",
    "paper": "same participants pooled at each timepoint (S2.6.p1); model without pool term (S2.9.p2)",
    "data": "pool index correspondence not documented",
    "disposition": "executable_without_change"
  },
  {
    "item": "accession naming",
    "paper": "S2.8.p1 says the C2C12 data are also in GSE219100",
    "data": "GSE219100 is a SuperSeries; C2C12 data are in sub-series GSE219099, EV data in GSE218103",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 36620222 (PMC9811128)

**Run label:** PMID36620222  
**Decision maker:** Claude Code session (claude-opus-5-5) using the bioinformatics-workflow skill, case-spec route.  
**Spec:** `case_spec.json`. **Runner output:** `_execute_out.json`, `case_runner.log`, `summary.csv`. The decision contract validator passed: 20 records, 0 errors. The first attempt is kept in `_previous/`.

## What ran

| Case | Outcome | Why |
|---|---|---|
| GSE218103: plasma-EV small RNA-seq, human, 12 pooled samples | **completed**, paper_aligned | This is the only accession that contains an exercise contrast. |
| GSE219099: C2C12 cells, miR-486 mimic vs scramble, mouse, 6 samples | **refused at design** | No exercise factor. It is an in-vitro test of what one miRNA does. |
| GSE219100: SuperSeries of the two above, 18 samples | **refused at design** | Its samples are the union of GSE218103 (human miRNA) and GSE219099 (mouse mRNA). No single design spans the two species and assays, and its exercise contrast is the same as GSE218103's. |

### GSE218103: decisions
- **Sample groups.** In GEO, "CON" (treatment: control) means the **pre-exercise sample**, not the paper's separate TD CON no-exercise group. Evidence: only TD EX and CP EX were sequenced, as 3 pools per timepoint (S2.6.p1); the study has no "CP CON" group (S2.1.p1); and treatment_protocol reads "before and 30 minutes after a bout". So CON is pre and EX is post.
- **Model.** One DESeq2 model (pydeseq2) over the 4 genotype x time cells, 3 pools per cell. This matches the paper's genotype + activity model (S2.9.p2).
  - Planned: post vs pre within TD; post vs pre within CP.
  - Associational: CP vs TD at pre; CP vs TD at post.
  - Exploratory: the genotype x time interaction.
- **Low-count filter.** "MicroRNAs with less than 10 counts were removed" was read as a row total of at least 10 across the 12 samples. It was encoded as `min_mean_count` 0.8333 and keeps 298 of 399 miRNAs.
- **Covariance.** No pool blocking. The pre and post pools come from the same participants, but GEO does not say which pre pool matches which post pool. The pre/post correlations do not peak on matching indices, and the paper's model has no pool term. Ignoring this positive pairing makes the exercise tests conservative. It is recorded as a caveat and was not guessed.
- **Threshold.** The paper's own rule (S2.9.p2): BH-adjusted p < 0.05, no fold-change cutoff. Raw p < 0.05 is reported only as a labelled audit count.
- **Enrichment.** Not ... [2552 more characters]
