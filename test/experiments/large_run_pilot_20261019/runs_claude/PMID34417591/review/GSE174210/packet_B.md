# Review packet B (the analysis' decisions): GSE174210

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.1.treatment level", "across": "characteristics_ch1.1.treatment", "pairs_or_sets": 5, "samples_linked": 10, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all mice are sedentary APP/PS1 receiving AAV8-irisin or AAV8-GFP. Irisin overexpression is a mimetic, not exercise; analysing it as an exercise effect would change the estimand.

## Samples per design level

### `trt`
- **GFP** (5): GSM5289454 / GFP group mouse 1 / GFP-3106; GSM5289455 / GFP group mouse 2 / GFP-3108; GSM5289456 / GFP group mouse 3 / GFP-3110; GSM5289457 / GFP group mouse 4 / GFP-3121; GSM5289458 / GFP group mouse 5 / GFP-3124
- **Irisin** (5): GSM5289459 / Irisin group mouse 1 / Irisin-3111; GSM5289460 / Irisin group mouse 2 / Irisin-3114; GSM5289461 / Irisin group mouse 3 / Irisin-3117; GSM5289462 / Irisin group mouse 4 / Irisin-3127; GSM5289463 / Irisin group mouse 5 / Irisin-3129

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE174210"], "primary_estimand": "Hippocampus of APP/PS1 mice: AAV8-irisin-FLAG vs AAV8-GFP (tail vein) (S2.7.p1, S4.20.p1, FIG17c-d); no exercise arm", "planned_contrasts": ["Irisin vs GFP (GSEA and glia-gene ORA only; no DEG count reported)"], "paper_method": "DESeq2 (S4.21.p1), GSEA (FIG17c)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S4.29.p1 (general p<0.05; no DEG rule given for this dataset)"}}

reasoning: S4.20.p1 / FIG17: n=5 GFP vs 5 irisin. Intervention is hepatic irisin overexpression, not exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE174210\\GSE174210_cw2036-APP_PS1NormalisedCounts_DESeq2.txt.gz", "owned": true, "checks": ["S4.27.p1 lists GSE174210", "10 samples GFP 5 / Irisin 5 = FIG17 n", "APP/PS1 hippocampus"], "accession": "GSE174210", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE174210\\GSE174210_metadata.csv"}

reasoning: matches

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 10, "n_metadata": 10, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174210\\aligned\\aligned_metadata.csv", "columns": {"trt": {"alias_of": "characteristics_ch1.1.treatment", "recode": {"tail vein injected AAV8-GFP": "GFP", "tail vein injected AAV8-Irisin-FLAG": "Irisin"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174210\\aligned\\design_metadata.csv", "sha256": "d05360f44f62fcecf803fe0c6304bef184c895e292c6a1f05d8665581ba9263b", "levels": {"trt": {"GFP": 5, "Irisin": 5}}}}

reasoning: Matrix columns equal description (10/10).

### matrix (valid, not_started)

final: {"source": "GSE174210_cw2036-APP_PS1NormalisedCounts_DESeq2.txt.gz", "paper_input": "DESeq2 on raw counts; only normalized counts deposited", "matrix_type": "DESeq2-normalized counts (non-integer, linear scale)", "recommended_method": "none for exercise question", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174210\\aligned\\aligned_matrix.csv", "sha256": "35eadbd632497949d5d08bc4a8d9008a3a402d48cb1c82efbed6f21fe7609112", "n_features": 31510, "n_samples": 10, "annotation_columns_dropped": [], "duplicated_feature_ids": 2, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 610487.7128, "median": 24.51020921, "integer_fraction": 0.2779, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name and 28% integer fraction: DESeq2 size-factor-normalized counts; also Excel-mangled gene IDs (1-Mar, ...).

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "trt", "control": "GFP", "treatment": "Irisin", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE174210\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: S4.20.p1, FIG17. The request is the exercise effect.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 10 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[]

## HANDBACK.md (start)

# HANDBACK — PMID 34417591 (Islam et al. 2021, irisin / FNDC5, PMC10317538)

Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`; validator 22 records, 0 errors. Final attempt is the third; earlier ones are in `_previous/`.

## What ran

| Case | Outcome | Why |
|---|---|---|
| GSE174211: newborn-neuron nuclei, WT/F5KO × Sed/Run (4/4/4/5 males) | **completed**, route `exploratory` | This is the only one of the three series with an exercise arm |
| GSE174210: APP/PS1 hippocampus, AAV8-irisin vs AAV8-GFP (5/5) | **refused at design** | There is no exercise arm. Irisin overexpression mimics exercise but is not exercise. The deposited matrix is DESeq2-normalized non-integer counts, and some gene IDs were converted to dates by Excel (`1-Mar` and similar) |
| GSE179078: dentate gyrus, F5KO vs WT (5/5) | **refused at design** | There is no exercise arm. The comparison is genotype only |

GSE174211 model and matrix:

- **Matrix:** raw STAR gene counts. The file is named "normalized", but every value is an integer and the library sizes range from 1.08M to 8.52M.
- **Model:** pydeseq2.
  - A joint `~ grp` model (grp = genotype_exercise, 4 cells) on all 17 samples.
  - Exercise main effect with `~ geno + ex`.
  - The paper's pooled genotype contrast with `~ geno`.
- **Sex check:** passed; all samples are male.
- **Enrichment:** not run. The paper's GSEA is for KO vs WT, not exercise.

## Threshold

The paper's rule (S2.5.p2) is "log2FC > |1.5|, p-value < 0.05": raw p < 0.05 and |log2FC| > 1.5. I applied it exactly. As an audit I also counted genes with BH padj < 0.05.

## DEG counts vs the paper

| Table | Ours (paper rule) | up / down | Audit padj<0.05 | Paper |
|---|---|---|---|---|
| joint/grp_WT_Run_vs_WT_Sed (exercise in WT, primary for the request) | 37 | 8 / 29 | 0 | not reported ("underpowered", S2.5.p2) |
| joint/grp_KO_Run_vs_KO_Sed (exercise in KO) | 26 | 14 / 12 | 0 | not reported |
| ex_Run_vs_Sed_adj_geno (~geno+ex) | 20 | 5 / 15 | 0 | not reported |
| geno_KO_vs_WT (pooled; the paper's contrast, secondary) | 784 | 436 / 348 | 5488 | 459 |
| joint KO_Sed vs WT_Sed, WT_Run vs KO_Run, and the cross-cell contrasts | 422 / 524 / 361 / 587 | — | — | — |

Conclusion on exercise: in this dataset, voluntary running has no FDR-significant effect on newborn-neuron nuclear transcripts in WT or KO mice. This agrees with the paper's statement that the dataset was underpowered for an exercise effect. The 20–37 genes that pass the raw-p rule are ... [1622 more characters]
