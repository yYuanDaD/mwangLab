# Review packet B (the analysis' decisions): GSE199111

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.1.genotype", "pairs_or_sets": 5, "samples_linked": 10, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast in the sequenced samples. All 10 GSE199111 samples are CTX-injured TA at day 6 from sedentary mice; the only factor is genotype (wild type 5 vs miR-501 -/- 5). The paper's exercise experiment (eccentric treadmill, S2.5.p1, Table 1) was assessed by Evans blue dye histology only and was never sequenced. The request's estimand (effect of exercise on gene expression) cannot be identified from these data; the genotype contrast does not answer it and is not substituted.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE199111"], "other_accessions_not_analyzed": {"GSE200501": "scRNA-seq of pooled TA muscles (3 Pax7Cre + 3 miR-501dMP pooled), CTX regeneration; no exercise arm (S2.17.p1, S11.p1)"}, "assay": "bulk RNA-seq (TruSeq stranded mRNA, NovaSeq 6000, 100 bp SE; STAR + featureCounts), tibialis anterior (S2.18.p1)", "primary_estimand": "Effect of myogenic-progenitor-specific miR-501 deletion (miR-501dMP vs Pax7Cre control) on TA gene expression at day 6 after cardiotoxin injury (S3.3.p1, FIG3 e). This is a genotype effect during injury-induced regeneration, not an exercise effect.", "factors": {"genotype": ["Pax7Cre (control)", "miR-501dMP"]}, "constant_conditions": "12-week-old male mice; all TA muscles CTX-injected and harvested at day 6 (S2.2.p1, FIG3 e)", "sample_inclusion": "n = 5 per genotype (FIG3 e)", "planned_contrasts": ["miR-501dMP vs Pax7Cre, TA day 6 post-CTX (S3.3.p1, FIG3 e; paper: 146 up, 89 down = 235 DEGs at p<0.05)"], "exercise_in_paper": "A single bout of eccentric (downhill) treadmill exercise (S2.5.p1) was applied to naive miR-501dMP and Pax7Cre mice and assessed only histologically (Evans blue dye, Table 1, FIG4 c). No sequencing was performed on exercised muscle.", "repeated_measure_unit": "none (one TA per independent mouse)", "paper_method": "not stated (no DE tool named; S2.18.p1 names STAR alignment and Enrichr GO only)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": " ... [104 more characters]

reasoning: The data availability statement (S11.p1) assigns GSE199111 to the bulk RNA-seq in TA. The only bulk RNA-seq described is miR-501dMP vs Pax7Cre at day 6 after CTX (S3.3.p1, FIG3 e, n = 5). The eccentric exercise experiment (S2.5.p1, S3.3.p1, Table 1) was read out by EBD histology only. The paper therefore never measures how exercise changes gene expression.

### ownership (valid, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36907509\\GSE199111\\input\\merged_from_tar_gsm.csv", "owned": true, "checks": ["S11.p1 names GSE199111 for RNA-seq in TA", "GEO: Tibialis anterior, male, 12 weeks, CTX day 6, wild type 5 / miR-501 -/- 5, matching FIG3 e n = 5", "data_processing: STAR + featureCounts raw counts, matching S2.18.p1"], "accession": "GSE199111", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE199111\\GSE199111_metadata.csv"}

reasoning: Accession, tissue, age, sex, injury, time point, group sizes and processing all match the paper's bulk RNA-seq.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 10, "n_metadata": 10, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36907509\\GSE199111\\aligned\\aligned_metadata.csv", "columns": {"genotype": {"alias_of": "characteristics_ch1.1.genotype", "recode": {"wild type": "WT", "miR-501 -/-": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36907509\\GSE199111\\aligned\\design_metadata.csv", "sha256": "bb2a8ba07a061dffff00c25eafcc72c3ce77664920ac984eda6047414a341065", "levels": {"genotype": {"WT": 5, "KO": 5}}}}

reasoning: Merged tar columns become GSM ids; exact match on the metadata index (10/10). Genotype copied to a formula-safe column.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36907509\\GSE199111\\aligned\\aligned_matrix.csv", "sha256": "04e7cd93a5b0ebd1a52d1cead3c157b1d2171748a883549c85a821e941a8fc55", "n_features": 25700, "n_samples": 10, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 892729.0, "median": 40.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (integer_fraction 1.0, max 892729); GEO data_processing: featureCounts (Rsubread), 'identifiers and raw counts'. Consistent with S2.18.p1.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36907509\\GSE199111\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Design gate: the request asks for exercise effects; the deposited series has no exercise (or any non-genotype) factor. Refused.

rejected alternatives: [{"value": "genotype KO vs WT (paper's planned bulk contrast, S3.3.p1)", "reason_rejected": "answers a genetic-deletion question during CTX regeneration, not an exercise effect; running it would be a manufactured substitute for the requested estimand"}, {"value": "treat CTX injury as an exercise-like insult", "reason_rejected": "CTX is a chemical myotoxin, not exercise; every sample is CTX-injured, so there is no uninjured or exercised reference either"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 10 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "request vs paper estimand",
    "paper": "bulk RNA-seq estimates miR-501dMP vs Pax7Cre after CTX injury; exercise read out by histology only",
    "data": "GSE199111 holds genotype x 5 at CTX day 6; no exercise samples",
    "disposition": "blocks_request"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 36907509 / GSE199111

**Status: refused at the `design` gate.** The sequenced samples contain no exercise contrast.

## What ran
1. Read the paper (`test/experiments/paper_screen_20261027/papers/PMC10033748.paper.md`): S2.2, S2.5, S2.18, S2.19, S3.3, S3.4, FIG3, FIG4, TAB1, S11.
2. `python -m tools.case_runner inspect GSE199111`: GSE199111 was not cached, so it was downloaded to `E:/agent/mwangLab_pdf/data/GSE199111`. The `_RAW.tar` was merged into 25,700 Ensembl genes x 10 samples, all integer values, and featureCounts raw counts. Output is in `inspect_GSE199111.json`.
3. `python -m tools.case_runner execute case_spec.json`:
   - Gates recorded: paper_reconstruction, ownership, alignment (exact on the GSM index, 10/10), matrix (raw counts), and design (refused).
   - The contract validator reported 5 records and 0 errors.
   - Records are in `GSE199111/`; the summary is `summary.csv`.
   - No DE executor or enrichment ran.

## Why refused
- **GSE199111 holds no exercise samples.** S11.p1 assigns GSE199111 to the bulk TA RNA-seq. All 10 samples are 12-week-old male TA muscles harvested at day 6 after cardiotoxin (CTX) injection. The only varying factor is genotype: 5 wild type (Pax7Cre) and 5 miR-501 -/- (miR-501ΔMP). This matches S3.3.p1 and FIG3 e (n = 5).
- **The paper's exercise data are histology only.** The exercise experiment is a single bout of eccentric downhill treadmill running (S2.5.p1). It was read out by Evans blue dye histology only (Table 1, FIG4 c); exercised muscle was never sequenced.
- **The other accession has no exercise arm either.** GSE200501 is scRNA-seq of pooled CTX-regenerating TA muscles.
- **No substitute was run.** The genotype contrast answers a genetic-deletion question during chemical injury, not how exercise changes gene expression. Both the genotype contrast and the idea of treating CTX as an exercise proxy are recorded as rejected candidates.

## DEG counts vs paper
- **Paper:** miR-501ΔMP vs Pax7Cre, CTX day 6, gives 146 up and 89 down (235 DEGs). The threshold is raw p < 0.05 with no fold-change cutoff (S3.3.p1). The paper names no DE tool.
- **Ours:** not run. The request is refused, so there are 0 exercise contrasts against the paper's 0.
- The genotype contrast was not executed because it does not answer the request.

## Deviations
None. No analysis was executed.

## Tool problems
- **Mojibake in the metadata CSV (cosmetic; analysis not affected).** `data/GSE199111/GSE199111_metadata.csv` contains  ... [474 more characters]
