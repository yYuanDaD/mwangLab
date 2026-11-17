# Review packet B (the analysis' decisions): GSE125630

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.0.injury type level", "across": "characteristics_ch1.0.injury type", "pairs_or_sets": 4, "samples_linked": 12, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"title": ["Contusion SCI + SWIM, Replicate 1", "Contusion SCI + SWIM, Replicate 2", "Contusion SCI + SWIM, Replicate 3", "Contusion SCI + SWIM, Replicate 4", "Contusion SCI + SWIM, Replicate 5"], "treatment_protocol_ch1": ["Animals were given either T2 complete transection SCI, T2 contusion SCI, or no SCI. A subset of contused SCI animals were exposed to either swimming or shallow water walking exercise."], "supplementary_file_1": ["ftp://ftp.ncbi.nlm.nih.gov/geo/ ... [912 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): Exercise is completely confounded with time of sacrifice / tissue-collection session: every exercised animal (SWIM, SWW) was sacrificed at 13.5 wk post-surgery and every sedentary CONT SCI animal at 11.5 wk (GEO 'weeks after injury', S2.3.p1, S4.3.p1). No sedentary animal shares the exercised animals' collection time, so wpi cannot be adjusted and the exercise contrast cannot be separated from 2 extra weeks post-injury, ~2 weeks of age, and a separate collection session. The data show the confound dominates: on log2 CPM of the 500 most variable genes, PC1 (57% of variance; paper Fig 3b reports 66%) puts CONT (-14.6) with No SCI (-14.3) and puts SWIM (+9.9), SWW (+10.5) together with TX SCI (+10.7), which was collected at yet another time (8.5 wk). Mild swimming/wading and complete transection producing the same dominant shift while contusion vs no injury produces none fits a collection-session effect, not exercise biology. The paper's argument that batch effects are unlikely (S4.3.p1) is an assumption, not a design control. Exercise vs no-exercise is therefore not identifiable from GSE125630. The runner's suitability report independently fails the covariance check (wpi: primary_nested_in_candidate with grp; GSE125630/suitability/suitability.md).

## Samples per design level

### `grp`
- **CONT** (6): GSM3579165 / Contusion SCI, Replicate 1; GSM3579166 / Contusion SCI, Replicate 2; GSM3579167 / Contusion SCI, Replicate 3; GSM3579168 / Contusion SCI, Replicate 4; GSM3579169 / Contusion SCI, Replicate 5; GSM3579170 / Contusion SCI, Replicate 6
- **NoSCI** (4): GSM3579161 / No SCI, Replicate 1; GSM3579162 / No SCI, Replicate 2; GSM3579163 / No SCI, Replicate 3; GSM3579164 / No SCI, Replicate 4
- **SWIM** (5): GSM3579147 / Contusion SCI + SWIM, Replicate 1; GSM3579148 / Contusion SCI + SWIM, Replicate 2; GSM3579149 / Contusion SCI + SWIM, Replicate 3; GSM3579150 / Contusion SCI + SWIM, Replicate 4; GSM3579151 / Contusion SCI + SWIM, Replicate 5
- **SWW** (5): GSM3579152 / Contusion SCI + SWW, Replicate 1; GSM3579153 / Contusion SCI + SWW, Replicate 2; GSM3579154 / Contusion SCI + SWW, Replicate 3; GSM3579155 / Contusion SCI + SWW, Replicate 4; GSM3579156 / Contusion SCI + SWW, Replicate 5
- **TX** (4): GSM3579157 / Complete transection SCI, Replicate 1; GSM3579158 / Complete transection SCI, Replicate 2; GSM3579159 / Complete transection SCI, Replicate 3; GSM3579160 / Complete transection SCI, Replicate 4

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE125630"], "superseries": "GSE129704 (S3.p1; also liver and soleus, not analyzed here)", "paper_type": "Scientific Data Data Descriptor: no differential-expression analysis, no DEG counts, no named DE genes, no threshold are reported", "assay": "bulk polyA RNA-seq, Illumina NextSeq 500 1x75 SE, STAR 2.6 to Rn6, HTSeq 0.10.0 reverse-stranded counts on Ensembl 93 (mito genes removed, 24,613 regions) (S2.5.p1, DA.p7-p8)", "tissue": "pooled bilateral T11-L4 DRG per animal (S2.3.p1)", "organism_sex": "female Sprague Dawley rats, 8-9 weeks at start (S2.1.p1)", "factors": {"group": ["No SCI (n=4)", "TX SCI (n=4)", "CONT SCI (n=6)", "CONT SCI + SWIM (n=5)", "CONT SCI + SWW (n=5)"]}, "inclusion": "all 24 animals (S2.2.p1, Table 1)", "primary_estimand": "effect of exercise training (swimming; shallow water walking) on DRG gene expression in contusion-injured rats housed in locomotor-restricting cages: CONT SCI + SWIM vs CONT SCI and CONT SCI + SWW vs CONT SCI (S1.p2, S1.p3, S4.2.p1 'one appropriate for an examination of the effect of exercise on SCI')", "planned_contrasts": ["CONT SCI + SWIM vs CONT SCI (S4.2.p1 comparison set; paper: no DE result reported)", "CONT SCI + SWW vs CONT SCI (S4.2.p1 comparison set; paper: no DE result reported)"], "secondary_comparison_set": "injury severity: TX SCI vs CONT SCI vs No SCI (S4.2.p1); not exercise", "repeated_measure_unit": "none; one pooled DRG sample per animal, independent animals; rats doubly housed by group (S2.2.p1) b ... [876 more characters]

reasoning: Data Descriptor (Sci Data). Groups and n from S2.2.p1 and Table 1; exercise comparison set from S4.2.p1; timing from S2.3.p1 / S4.3.p1 / FIG2. The paper reports no DE analysis, so there are no DEG counts or threshold to reproduce.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE125630\\GSE125630_GeneMatrix_RawCounts_InjuryActivity.txt.gz", "owned": true, "checks": ["S3.p1 names GSE125630 and raw HTSeq counts deposited there", "GEO matrix has 24 sample columns = 24 GSMs; 24,613 Ensembl rat gene IDs = 24,613 regions in S2.5.p1", "group sizes in matrix columns (4 Uninjured, 6 Contusion, 5 SWIM, 5 SWW, 4 Transection) match S2.2.p1", "GEO organism Rattus norvegicus, source dorsal root ganglion, data_processing names STAR 2.6 / HTSeq 0.10.0 / Rn6 Ensembl 93"], "accession": "GSE125630", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE125630\\GSE125630_metadata.csv"}

reasoning: File GSE125630_GeneMatrix_RawCounts_InjuryActivity.txt.gz is the paper's deposited raw HTSeq count matrix (S3.p1); metadata is the series' GSM table.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31175296\\GSE125630\\aligned\\aligned_metadata.csv", "columns": {"wpi": {"alias_of": "characteristics_ch1.1.weeks after injury?", "recode": {"8.5": "w8p5", "11.5": "w11p5", "13.5": "w13p5"}}, "injury": {"alias_of": "characteristics_ch1.0.injury type"}, "grp": {"source": "title", "regex": "^(No SCI|Contusion SCI|Complete transection SCI)(?: \\+ (SWIM|SWW))?, Replicate \\d+$", "recode": {"No SCI": "NoSCI", "Contusion SCI": "CONT", "Contusion SCI_SWIM": "SWIM", "Contusion SCI_SWW": "SWW", "Complete transection SCI": "TX"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31175296\\GSE125630\\aligned\\design_metadata.csv", "sha256": "ffc30f65cf49499893cc67f135ae4834081646f5c1313fc82e64fd9d5beee333", "levels": {"wpi": {"w13p5": 10, "w11p5": 10, "w8p5": 4}, "injury": {"T2 Contusion": 16, "T2 Complete transection": 4, "No SCI": 4}, "grp": {"CONT": 6, "SWIM": 5, "SWW": 5, "TX": 4, "NoSCI": 4}}}}

reasoning: Matrix columns (e.g. Contusion_DRG_SWIM_Replicate_2) and GSM titles (e.g. 'Contusion SCI + SWIM, Replicate 2') encode the same group and replicate number but with different words for the naive group (Uninjured vs No SCI). Key = transection/contusion token + exercise token + replicate number (naive animals keyed by replicate number alone); every key is unique on both sides. No positional alignment.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31175296\\GSE125630\\aligned\\aligned_matrix.csv", "sha256": "b0439e506183f46d7e97aa1de792baab88a6379ad8560f5e41d3e7129ade5a07", "n_features": 24613, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 795326.0, "median": 63.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 795,326, median 63, no missing; file named RawCounts; paper S3.p1 and GEO data_processing state raw HTSeq counts. Paper input = raw counts with DESeq2 RLE (S2.5.p1).

### design (refused, not_started)

final: {"analysis_type": "one factor, five levels; planned contrasts against CONT", "design_column": "grp", "estimand_type": "causal (randomized assignment to exercise, S2.2.p1)", "contrasts": [{"name": "grp_SWIM_vs_CONT", "control": "CONT", "treatment": "SWIM", "role": "primary"}, {"name": "grp_SWW_vs_CONT", "control": "CONT", "treatment": "SWW", "role": "primary"}], "wpi_confounding": {"status": "aliased", "crosstab": "TX: w8p5 only; NoSCI, CONT: w11p5 only; SWIM, SWW: w13p5 only", "covariates": [{"name": "wpi", "disposition": "aliased"}, {"name": "collection session (not recorded; implied by wpi and S2.3.p1)", "disposition": "aliased"}, {"name": "injury", "disposition": "excluded: constant (T2 Contusion) within CONT/SWIM/SWW"}, {"name": "cage pair (doubly housed within group, S2.2.p1)", "disposition": "nested: not recorded in metadata; nested in grp, cannot be blocked"}]}, "suitability": {"verdict": "not_analyzable", "failed": ["covariance"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31175296\\GSE125630\\suitability\\suitability.md", "n_comparisons": 10, "n_analyzable": 10}}

reasoning: S4.2.p1 defines the exercise comparison set as CONT SCI vs CONT SCI + SWIM/SWW. Exercise assignment was random among contused animals (S2.2.p1), so the design estimand is causal.  Confounding check on grp vs wpi: TX only at 8.5, NoSCI and CONT only at 11.5, SWIM and SWW only at 13.5, so each exercise contrast against CONT crosses wpi levels with no overlap. Skill stop condition: treatment completely confounded with a known covariate. The only within-time comparison (SWIM vs SWW) does not answer the exercise question. Sequencing depth also differs (mean library 23.6M SWIM / 26.0M SWW vs 34.0M CONT) but that is handled by size factors and is not the reason for refusal. Refused at design (not c ... [137 more characters]

rejected alternatives: [{"value": "pooled exercise (SWIM+SWW) vs CONT", "reason_rejected": "two distinct exercise levels; skill rule: one model with planned contrasts, never pooled levels"}, {"value": "SWIM vs SWW", "reason_rejected": "same sacrifice time, but compares two exercise modalities; it does not estimate the effect of exercise vs no exercise"}, {"value": "SWIM/SWW vs No SCI", "reason_rejected": "confounds exercise with injury; not the paper's exercise comparison"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: covariance)
- | Check | Status | Detail |
- | Covariance | fail | not_required; wpi: stop (primary_nested_in_candidate with a design factor: its effect cannot be separated) |
- | Sex | no_markers | Sex inference completed on 24 samples.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "time of sacrifice vs exercise",
    "paper": "S4.3.p1 states sacrifice time varied 8.5-13.5 wk by condition and argues batch effects are low because both 11.5 and 13.5 wk are chronic stage and the same person collected tissue",
    "data": "GEO 'weeks after injury' is 13.5 for every SWIM/SWW animal and 11.5 for every CONT animal; PC1 (57%) separates the 11.5-wk groups (NoSCI, CONT) from the other collection times (TX, SWIM, SWW)",
    "disposition": "blocks_estimand"
  },
  {
    "item": "DE analysis",
    "paper": "Data Descriptor; no DE analysis, DEG counts, genes, or threshold reported",
    "data": "raw counts would support DESeq2 had the design been identifiable",
    "disposition": "no_paper_result_to_compare"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 31175296 / GSE125630

Status: **refused at the `design` gate**. Contract validator: 0 errors. Route: `stopped`.

## What ran
- `python -m tools.case_runner inspect GSE125630`: the series was already cached (`data/GSE125630`). It holds one matrix, `GSE125630_GeneMatrix_RawCounts_InjuryActivity.txt.gz`: 24,613 Ensembl rat genes x 24 samples, integer raw HTSeq counts.
- `python -m tools.case_runner execute case_spec.json`, with these gates recorded:
  - `paper_reconstruction`
  - `ownership`
  - `alignment`: 24/24 samples matched by a key derived from the GSM title and from the matrix column name, compared case-insensitively. No positional alignment.
  - `matrix`: raw counts, DESeq2 route.
  - `design`: refused.
- No executions or enrichment ran.
- Earlier attempts are kept in `_previous/`. The first attempt marked the design `valid` and refused at `covariance`. The runner rejected it because the suitability verdict was `not_analyzable`, so the refusal moved to `design`.
- Evidence for the decision: an ad-hoc read-only PCA on log2 CPM of the 500 most variable genes. It was not saved as an artifact; the numbers are recorded in the design `stop_reason`.

## The paper
- The paper is a Scientific Data *Data Descriptor*. It reports no differential-expression analysis, no DEG counts, no DE genes and no threshold.
- It defines an exercise comparison set (S4.2.p1): CONT SCI (n=6) vs CONT SCI + SWIM (n=5) and CONT SCI + SWW (n=5). The planned contrasts were therefore `grp_SWIM_vs_CONT` and `grp_SWW_vs_CONT`, from a single five-level `grp` model.

## Why it was refused
Exercise is completely aliased with the time of sacrifice and the tissue-collection session:
- Every SWIM and SWW animal was sacrificed at 13.5 weeks post-surgery.
- Every sedentary CONT SCI animal (and every No SCI animal) was sacrificed at 11.5 weeks.
- TX SCI animals were sacrificed at 8.5 weeks.
- Sources: GEO `weeks after injury`, S2.3.p1, S4.3.p1, FIG2.

No sedentary contused animal shares the exercised animals' collection time, so the 2-week, age and collection-session difference cannot be adjusted out of the exercise contrast.

The data show this confound dominates. PC1 explains 57% of the variance (the paper's Fig 3b reports 66%). Mean PC1 score by group:

| Group | Weeks post-surgery at sacrifice | Mean PC1 |
|---|---|---|
| No SCI | 11.5 | -14.3 |
| CONT SCI | 11.5 | -14.6 |
| CONT SCI + SWIM | 13.5 | +9.9 |
| CONT SCI + SWW | 13.5 | +10.5 |
| TX SCI | 8.5 | +10.7 |

PC1 split ... [2108 more characters]
