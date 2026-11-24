# Review packet B (the analysis' decisions): GSE228869

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.4.day of_hs", "n_values": 3, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "grp", "n_values": 3, "max_repeat": 4, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "characteristics_ch1.5.day of_differentiation (without characteristics_ch1.4.day of_hs) + suffix of title", "across": "characteristics_ch1.4.day of_hs", "pairs_or_sets": 4, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"characteristics_ch1.3.treatment": ["Hindlimb suspension (HS)"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm, sample_size): No exercise contrast: the study manipulates disuse only (hindlimb suspension 7/14 d vs vivarium control); there is no exercise, training or reloading arm, so the requested exercise effect is not identifiable. Independently, each unloading group is a single pooled isolation of 8 animals (S2.2.p4), so rep1/rep2 are culture replicates and the unloading effect is aliased with the isolation/expansion batch (one biological unit per group, n=2 per group x differentiation cell).
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE228869"], "assay": "bulk RNA-seq (TruSeq stranded mRNA, NextSeq 2000) of in vitro expanded, second-passage FAPs from rat m. soleus", "primary_estimand": "Effect of hindlimb-suspension unloading duration (Contr / HS7 / HS14) on the transcriptome of cultured FAPs (time-course LRT, then degPatterns clustering). This is a disuse/unloading estimand; the study contains no exercise, training or reloading arm.", "factors": {"unloading": ["Contr (0 d)", "HS7", "HS14"], "adipogenic_differentiation_day (GEO only)": ["d0", "d3"]}, "sample_inclusion": "GEO: 12 libraries = 3 unloading groups x 2 differentiation days x 2 replicates. Paper S2.2.p4: at each time point FAPs from the 8 animals were COMBINED before in vitro expansion, so each group is one pooled isolation; rep1/rep2 are culture replicates of that pool.", "planned_contrasts": ["LRT across Contr/HS7/HS14 (S2.8.p1, S3.6.p1; five clusters of >=30 genes at p.adj<0.01; total DEG count not reported in the text)", "HS7 vs Contr and HS14 vs Contr highlighted for PPAR pathway genes (FIG7), no counts reported"], "repeated_measure_unit": "none (independent pooled isolations per group)", "paper_method": "DESeq2 LRT (full ~ unloading time vs reduced ~1; whether differentiation day was in the model is not stated), DEGreport degPatterns, clusterProfiler GSEA", "paper_threshold": {"metric": "padj", "cutoff": 0.01, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.8.p1"}, "paper_results": "Cluster 1 cell cycl ... [244 more characters]

reasoning: S2.1.p1-p2: rat hindlimb suspension 7 and 14 d vs vivarium control; S2.2.p4: cells from 8 animals combined per time point before expansion; S2.8.p1: DESeq2 LRT, DEGs at p.adj < 0.01; S3.6.p1: five clusters. No exercise intervention anywhere in Methods; exercise appears only as background (S1.p2, S3.2.p1, S4.p1).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE228869\\GSE228869_Row_counts_table_faps.txt.gz", "owned": true, "checks": ["S2.8.p2 and S11.p1 name GSE228869", "GEO organism Rattus norvegicus, tissue m. soleus, FAPs, Control vs Hindlimb suspension day 0/7/14 matches S2.1/S2.8", "contact Sorokina = first author (S14.p1)"], "accession": "GSE228869", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE228869\\GSE228869_metadata.csv"}

reasoning: The paper deposits exactly this series; the single count table GSE228869_Row_counts_table_faps.txt.gz holds all 12 GEO samples.

### alignment (valid, not_started)

final: {"method": "exact:source_name_ch1", "n_aligned": 12, "n_metadata": 12, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39639402\\GSE228869\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^(Control|HS7|HS14),", "recode": {"Control": "C", "HS7": "HS7", "HS14": "HS14"}}, "diff": {"source": "title", "regex": "day(\\d)", "recode": {"0": "d0", "3": "d3"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39639402\\GSE228869\\aligned\\design_metadata.csv", "sha256": "9ab98c055d6c4fb07b5b697ccb421eb6275c1941f9baac8d560b1b50ecaeef3c", "levels": {"grp": {"C": 4, "HS7": 4, "HS14": 4}, "diff": {"d0": 6, "d3": 6}}}}

reasoning: inspect: source_name_ch1 equals the 12 matrix column names exactly (12/12). grp = unloading group, diff = adipogenic differentiation day, both parsed from title.

### matrix (valid, not_started)

final: {"source": "GSE228869_Row_counts_table_faps.txt.gz", "paper_input": "featureCounts counts into DESeq2 (S2.8.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39639402\\GSE228869\\aligned\\aligned_matrix.csv", "sha256": "a93f3a9fb53a2d8be223ab9c3a5d0c4eb9bdfa272f6296833a4b91f3dec04512", "n_features": 32622, "n_samples": 12, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 835198.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 835198, Ensembl rat gene IDs; data_processing: STAR + featureCounts v1.6.4 then DESeq2. Consistent with the paper's input.

### design (refused, not_started)

final: {"analysis_type": "none (refused)", "design_column": null, "contrasts": [], "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39639402\\GSE228869\\suitability\\suitability.md", "n_comparisons": 11, "n_analyzable": 0}}

reasoning: S2.1.p2 groups are Contr/HS7/HS14 only; GEO treatment column has Control and Hindlimb suspension only. The paper's own framing (S1.p3, S4.p3) is functional unloading. Exercise appears only in cited background. Per the skill, a sample set without an exercise arm is refused at design. The pooling (S2.2.p4) would additionally make any unloading inference pseudoreplicated.

rejected alternatives: [{"value": "LRT ~ diff + grp (paper's unloading time course)", "reason_rejected": "estimand is unloading/disuse, not exercise; and group is aliased with the single pooled isolation per group"}, {"value": "HS7 vs C and HS14 vs C Wald contrasts treated as 'inactivity vs exercise'", "reason_rejected": "the control is ordinary cage activity, not exercise; relabelling the sign would manufacture an exercise contrast the study did not run"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/11 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 12 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "differentiation day",
    "paper": "RNA-seq described on second-passage FAPs (S2.8.p1); d0/d3 differentiation not mentioned for RNA-seq",
    "data": "GEO has d0 and d3 adipogenic-differentiation samples for each group",
    "disposition": "recorded; not acted on because the case stops at design"
  },
  {
    "item": "reference genome",
    "paper": "STAR v2.604a, mRatBN7.2 (S2.8.p1)",
    "data": "GEO data_processing: STAR 2.7, Rnor_6.0 Ensembl 104",
    "disposition": "recorded; not acted on"
  },
  {
    "item": "biological replication",
    "paper": "8 animals per group combined before expansion (S2.2.p4)",
    "data": "2 replicates per group x day labelled rep1/rep2",
    "disposition": "replicates are technical/culture replicates of one pool; contributes to the refusal"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID39639402 / GSE228869

**Outcome: refused at `design`.** No differential-expression model was run.

## What ran
- `python -m tools.case_runner inspect GSE228869` downloaded the series into `data/GSE228869`. It found one count table: `GSE228869_Row_counts_table_faps.txt.gz`, 32,622 rat Ensembl genes × 12 samples, all integers, from featureCounts.
- `python -m tools.case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment, matrix and design (refused). Alignment was exact on `source_name_ch1` and matched 12/12 samples. The contract validator returned 0 errors on 5 records. The case status is `stopped:design`.

## Why it was refused
1. **There is no exercise contrast.** The study only reduces muscle use. Its groups are a vivarium control, 7 days of hindlimb suspension (HS7) and 14 days (HS14) (S2.1.p2). There is no exercise, training or reloading arm. Exercise comes up only as cited background (S1.p2, S3.2.p1, S4.p1). The requested exercise effect cannot be estimated from these data.
2. **There is only one biological unit per group.** The paper says that at each time point, FAPs from the 8 animals were combined before in vitro expansion (S2.2.p4). So `rep1` and `rep2` are culture replicates of one pool, and any group effect is aliased with that group's isolation and expansion batch. The design is also 3 groups × 2 differentiation days × 2 replicates. The suitability report (`GSE228869/suitability/suitability.md`) therefore finds 0 of 11 comparisons with at least 3 samples per group (`not_analyzable`, failing on sample size).

## DEG counts vs the paper
- **Paper:** DESeq2 likelihood-ratio test across Contr/HS7/HS14, DEGs at **p.adj < 0.01** with no fold-change cutoff (S2.8.p1). The paper reports five degPatterns clusters of at least 30 genes each, but gives no total DEG count or per-contrast count.
- **Ours:** none, because the case stopped at design. There are 0 executed contrasts to compare.

## Deviations and discrepancies (recorded in the spec)
- **Differentiation day:** GEO includes day-0 and day-3 adipogenic-differentiation samples. The paper's RNA-seq methods describe only second-passage FAPs and do not say whether differentiation day was in the LRT model.
- **Reference genome:** the paper says STAR v2.604a with mRatBN7.2. GEO `data_processing` says STAR 2.7 with Rnor_6.0 (Ensembl 104).
- **Replication:** pooled animals, so the replicates are technical (see above).

## Tool problems
- **None bl ... [462 more characters]
