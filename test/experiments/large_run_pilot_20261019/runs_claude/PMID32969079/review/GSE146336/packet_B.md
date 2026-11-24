# Review packet B (the analysis' decisions): GSE146336

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the sequenced samples differ only by genotype (WT vs muscle TRa1 loss-of-function) and treatment (T3 vs vehicle). Exercise (treadmill, wheel running) was a phenotyping readout in unsequenced cohorts (S2.4, S3.1.p1). An exercise effect on gene expression cannot be identified from GSE146336.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE146336"], "assay": "bulk polyA RNA-seq, soleus muscle, male mice (S2.5.p1, S3.3.p1)", "factors": {"genotype": ["WT", "TRa1 HSACre (L400R dominant-negative, 'TRa1 KO' in GEO)"], "treatment": ["vehicle", "T3 100 nmol/kg s.c. daily, 7 days"]}, "sample_inclusion": "WT and TRa-HSACre SOL, vehicle n=5-6/4-6, T3 n=5-6/7 (FIG3); GEO has 22 samples (11 WT/11 KO; 9 vehicle/13 T3)", "primary_estimand": "Effect of muscle TRa1 loss-of-function (genotype) on the soleus transcriptome under vehicle, and the T3 response by genotype (S3.3.p1). No exercise factor in the RNA-seq.", "planned_contrasts": ["KO vs WT, vehicle (S3.3.p1/FIG3A; paper: 788 DEGs)", "WT-T3 vs KO-T3 (FIG3B/C; GO enrichment, no DEG count)"], "exercise_component": "Treadmill exhaustion and 6-week voluntary wheel running were phenotyping endpoints only (S2.4, S3.1.p1, FIG1E/F); no exercised samples were sequenced.", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S2.11.p1 (FDR-adjusted P; cutoff assumed 0.05 from P < .05 significance rule)"}, "paper_method": "edgeR QL, ~0 + group (group = genotype x treatment), contrasts per edgeR manual (S2.6.p1)", "paper_results": {"KO_vs_WT_vehicle": 788}}

reasoning: S2.5/S2.6 describe RNA-seq of SOL from WT and TRa-HSACre mice treated with T3 or vehicle; S3.3.p1 reports 788 DEGs KO vs WT. Exercise appears only in S2.4/S3.1 as phenotyping (treadmill capacity, wheel running) of separate cohorts; none of those mice were sequenced.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE146336\\GSE146336_counts.csv.gz", "owned": true, "checks": ["DA.p1 names GSE146336", "GEO tissue Soleus muscle, male, genotype WT/TRa1 KO, treatment T3/vehicle matches S3.3.p1", "data_processing STAR/featureCounts/edgeR matches S2.6.p1"], "accession": "GSE146336", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE146336\\GSE146336_metadata.csv"}

reasoning: Data availability statement DA.p1 cites GSE146336; metadata factors match the paper's RNA-seq design.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 22, "n_metadata": 22, "coverage": 1.0, "unmatched_matrix_columns": ["start", "end", "length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32969079\\GSE146336\\aligned\\aligned_metadata.csv", "columns": {}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32969079\\GSE146336\\aligned\\design_metadata.csv", "sha256": "a572200a89f1965c7a33f5ce17ea7470e12c255e08a4a15a0f35596ce0adb397", "levels": {}}}

reasoning: Matrix columns (033_1 ...) are the prefix of the GEO title ('033_1: Sample 1'); inspect matched 22/22.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32969079\\GSE146336\\aligned\\aligned_matrix.csv", "sha256": "e39d70c250fb6c327a3e3c30d54a51bb8659fe25bb4fd8d473d91107c044ede4", "n_features": 55487, "n_samples": 22, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 4575446.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All-integer values up to 4.6e6, featureCounts per data_processing and S2.6.p1; paper input is raw counts to edgeR.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_contrast_available": false, "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32969079\\GSE146336\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: The request is for an exercise effect; GEO grouping columns are only genotype and treatment (T3/vehicle). Running a T3 or genotype contrast would answer a different question than the one asked.

rejected alternatives: [{"value": "characteristics_ch1.3.treatment T3 vs vehicle", "reason_rejected": "Pharmacological T3 treatment, not exercise."}, {"value": "characteristics_ch1.0.genotype TRa1 KO vs WT", "reason_rejected": "Genotype contrast, not exercise."}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 22 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample counts",
    "paper": "FIG3: vehicle WT/KO n=5-6/4-6, T3 n=5-6/7",
    "data": "22 samples: 11 WT/11 KO, 9 vehicle/13 T3",
    "disposition": "not_evaluated_case_refused"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID32969079 / GSE146336

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE146336` (data cached): 1 matrix, `GSE146336_counts.csv.gz`, 55,487 Ensembl genes × 22 samples, all integers (featureCounts). The metadata has two grouping columns: genotype (WT 11 / TRa1 KO 11) and treatment (T3 13 / vehicle 9). All samples are male soleus.
- `case_spec.json` was executed. Gates recorded: paper_reconstruction, ownership, alignment (exact key from the title prefix, 22/22), matrix (raw counts), and design (refused). The validator passed with 0 errors and 5 records. No DE executions or enrichment ran.

## Why refused
The RNA-seq design is genotype (WT vs muscle TRα1 L400R loss-of-function) × T3 vs vehicle, given for 7 days (S2.6.p1, S3.3.p1, FIG3). Exercise (treadmill to exhaustion, 6-week voluntary wheel running; S2.4, S3.1.p1, FIG1E/F) was only measured as a phenotype in separate cohorts that were not sequenced. The data therefore contain no exercise effect on gene expression to estimate. I rejected the T3 contrast because it is a pharmacological treatment, and the genotype contrast because it is not exercise.

## DEG counts vs paper
- Paper threshold: FDR-adjusted P (S2.11.p1). The cutoff is taken as 0.05 from the paper's general P < .05 rule, with no fold-change rule.
- Paper: 788 DEGs for KO vs WT under vehicle (S3.3.p1). There is no exercise contrast in the paper's RNA-seq.
- Ours: none run (refused). 0/0 exercise contrasts.

## Deviations
- None executed. The GEO group sizes (vehicle 9, T3 13) differ slightly from FIG3 (vehicle n=5-6/4-6, T3 n=5-6/7). This was recorded as a discrepancy and not evaluated.

## Tool problems
- Minor: when the design gate is refused without `factors`, the runner still runs the suitability report. It returns `not_analyzable` with `failed: ["sample_size"]` and 0 comparisons, which is misleading because the actual stop reason is the absence of an exercise factor, not sample size. See `GSE146336/suitability/suitability.md`. The suitability check should be skipped, or labelled as `no factors given`, when design is refused.
- Inspect: the GEO metadata spellings "T3 treatmant" and "vechicle" are kept verbatim. This caused no problem here.

