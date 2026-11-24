# Review packet B (the analysis' decisions): GSE75919

## Mechanical flags

- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"source_name_ch1": ["gastrocnemius muscles of 3 month old mice after exercise"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all 9 sequenced mice (5 Gprc6a fl/fl, 4 Gprc6a_Mck-/-) were sampled after exercise and no sedentary/rest arm was sequenced, so the effect of exercise on gene expression is not identifiable. The only available contrast is genotype within exercised mice (the paper's RNA-seq estimand), which is not an exercise effect.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE75919"], "assay": "bulk RNA-seq (Illumina HiSeq 2500), gastrocnemius, 3-month-old mice", "primary_estimand": "Genotype effect (Gprc6a_Mck-/- vs Gprc6a fl/fl) on muscle gene expression after a single bout of treadmill exercise; all sequenced mice were exercised", "planned_contrasts": ["Gprc6a_Mck-/- vs Gprc6a fl/fl, both after exercise (S2.5.p1, S4.3.p1; paper reports no DEG count, names Il6 as most decreased (80%) and a modest decrease of Il6ra, Figure 6A/S6A)"], "factors": {"genotype": ["Gprc6a fl/fl", "Gprc6a fl/fl;Mck-Cre"], "exercise": ["after exercise only (no sedentary arm sequenced)"]}, "exercise_protocol": "single bout, 40 min treadmill at 30 cm/s (S2.1.p1)", "paper_threshold": {"metric": "not stated", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "S4.3.p1 (RNA-seq details deferred to supplemental information, not available)"}, "paper_method": "not stated in main text (supplemental information)", "paper_results": "Il6 most decreased (~80%) in Gprc6a_Mck-/- muscle after exercise; Il6ra modestly decreased; other myokines unaffected"}

reasoning: S2.5.p1: 'we performed a transcriptomic analysis in muscles of control and Gprc6a_Mck-/- mice after exercise'. S4.3.p1: 'The genome-wide differential expression of Gprc6a_Mck-/- vs. Gprc6af/f in muscle was measured by RNASeq'. The RNA-seq is a genotype comparison within exercised mice; the exercise-vs-rest effect was studied only by qPCR/ELISA, not sequenced.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27304508\\GSE75919_counts.csv", "owned": true, "checks": ["GEO source_name: gastrocnemius muscles of 3 month old mice after exercise", "genotype Grpc6afl/fl (5) vs Grpc6afl/fl;Mck-Cre (4) matches the paper's Gprc6a_Mck-/- vs Gprc6af/f", "contact lab Karsenty (Columbia), the paper's lab", "matrix column names equal GEO description field for all 9 GSMs"], "accession": "GSE75919", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE75919\\GSE75919_metadata.csv"}

reasoning: Series, tissue, genotypes and lab match the paper's RNA-seq (S2.5.p1, S4.3.p1); the paper does not cite the accession in the main text but no other series is plausible.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27304508\\GSE75919\\aligned\\aligned_metadata.csv", "columns": {"geno": {"alias_of": "characteristics_ch1.0.genotype/variation", "recode": {"Grpc6afl/fl": "WT", "Grpc6afl/fl;Mck-Cre": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27304508\\GSE75919\\aligned\\design_metadata.csv", "sha256": "dfd2742a2b17dc87456417edb894b358f8bffd7b0409cb15f3cf49e112bf6b27", "levels": {"geno": {"WT": 5, "KO": 4}}}}

reasoning: Matrix columns (e.g. a1.wt.Gprc6a.fl/fl.GP2) equal the GEO 'description' field exactly; genotype from characteristics. No exercise column exists: every sample is post-exercise.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27304508\\GSE75919\\aligned\\aligned_matrix.csv", "sha256": "2862f8836ab49605db557ab1cc35fbc278338f37c9af5766f2178b60c3c35b50", "n_features": 23284, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1269876.0, "median": 30.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All-integer values; data_processing: 'Reads in each gene were counted with HTSeq-0.6.1', 'Xlsx file with raw counts for each gene'. Converted xlsx to CSV without changing values (prep_counts.py).

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": null, "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID27304508\\GSE75919\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: GEO source_name is constant ('after exercise') for every sample; paper S2.5.p1 confirms the transcriptome was taken only after exercise. The request asks for the exercise effect; the data hold one factor (genotype) only.

rejected alternatives: [{"value": "geno_KO_vs_WT (Gprc6a_Mck-/- vs fl/fl after exercise)", "reason_rejected": "Estimates a genotype effect under exercise, not how exercise affects gene expression; without a rested group neither the exercise effect nor a genotype x exercise interaction can be estimated."}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "Exercise contrast",
    "paper": "Exercise effect on muscle Il6 assessed by qPCR/ELISA in rested vs exercised mice (Figure 6B-G)",
    "data": "RNA-seq contains only exercised mice",
    "disposition": "blocks_exercise_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID27304508 / GSE75919

**Status: refused at `design`** (validator: 5 records, 0 errors).

## What ran
- `case_runner inspect GSE75919` (series downloaded into `data/GSE75919`): 9 GSMs, one grouping column (genotype: Gprc6a fl/fl = 5, Gprc6a fl/fl;Mck-Cre = 4). `source_name_ch1` is the same for every sample: "gastrocnemius muscles of 3 month old mice after exercise".
- `prep_counts.py` converted the deposited `GSE75919_Gpc6arna_seq_raw.xlsx.gz` (sheet `Gpc6acounts.txt`, 23,284 genes × 9, integer HTSeq counts) to `GSE75919_counts.csv`. Values were not changed.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment (exact match on `description`, 9/9), matrix (raw counts), and design, where the case was refused. Suitability rated the only possible comparison (genotype KO vs WT) analyzable, but I refused it on scope.

## Why refused
The paper's RNA-seq (S2.5.p1, S4.3.p1) compares Gprc6a_Mck−/− with Gprc6a fl/fl mice, and all of them were sampled after a single treadmill bout. No rested or sedentary group was sequenced. That means the effect of exercise on gene expression, and any genotype × exercise interaction, cannot be estimated from this series. The only contrast available is genotype within exercised mice, and that is not an exercise effect. The paper studied the exercise effect itself (Il6 induction) only by qPCR and ELISA (Fig 6B–G), not by RNA-seq.

## DEG counts vs paper
- No DE was run. The paper gives no DEG count and no threshold in the main text: the RNA-seq methods are in the supplemental information, which was not available. Its named results are Il6 (most decreased, about 80%, in KO after exercise) and Il6ra (modest decrease), Fig 6A/S6A.
- Paper threshold: not stated. No threshold was applied.

## Deviations
- None executed. The genotype-under-exercise contrast was rejected as a candidate (recorded in design `candidates`) because it does not answer the exercise question.

## Tool problems
- `tools/case_runner.py:54` / `:360-363`: `inspect` reported `matrices: []` for this series. `_EXTENSIONS` lists `.xlsx` and `.xls.gz` but not `.xlsx.gz`, so GEO's gzipped Excel supplement (`*_raw.xlsx.gz`) is never profiled. I needed a manual prep script to get the matrix. Fix: add `.xlsx.gz` and read it through gzip + `pd.read_excel`.
- Minor: the GEO title/genotype strings have typos ("Gprc5a-/-", "Grpc6a", "b3Gprc5a-/-" with no dot). Alignment used `description`, which is clean, so nothing was ... [11 more characters]
