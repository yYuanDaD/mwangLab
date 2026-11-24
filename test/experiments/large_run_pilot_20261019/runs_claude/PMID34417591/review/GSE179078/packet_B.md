# Review packet B (the analysis' decisions): GSE179078

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "source_name_ch1", "pairs_or_sets": 5, "samples_linked": 10, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all samples are sedentary WT or F5KO dentate gyrus; genotype (loss of the exercise-induced hormone) is not an exercise intervention.

## Samples per design level

### `geno`
- **KO** (5): GSM5406102 / Fndc5 knock-out mouse 1 / 20190116_KO1_CW6530_S2; GSM5406103 / Fndc5 knock-out mouse 2 / 20190116_KO2_CW6530_S4; GSM5406104 / Fndc5 knock-out mouse 3 / 20190116_KO3_CW6530_S6; GSM5406105 / Fndc5 knock-out mouse 4 / 20190116_KO4_CW6530_S8; GSM5406106 / Fndc5 knock-out mouse 5 / 20190116_KO5_CW6530_S10
- **WT** (5): GSM5406097 / Wild-type mouse 1 / 20190116_WT1_CW6530_S1; GSM5406098 / Wild-type mouse 2 / 20190116_WT2_CW6530_S3; GSM5406099 / Wild-type mouse 3 / 20190116_WT3_CW6530_S5; GSM5406100 / Wild-type mouse 4 / 20190116_WT4_CW6530_S7; GSM5406101 / Wild-type mouse 5 / 20190116_WT5_CW6530_S9

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE179078"], "primary_estimand": "Microdissected dentate gyrus F5KO vs WT, n=5 each (S2.5.p2, FIG4c); no exercise arm", "planned_contrasts": ["F5KO vs WT (paper: 2 genes + Fndc5)"], "paper_method": "DESeq2 (FIG4c)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "source_locator": "S2.5.p2"}}

reasoning: S2.5.p2: only two genes plus Fndc5 DE (log2FC > |0.5|, p<0.05).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE179078\\GSE179078_cw2001-WT_F5KO_DG_STAR_Gene_Counts.csv.gz", "owned": true, "checks": ["S4.27.p1 lists GSE179078", "WT 5 / KO 5 = FIG4c n", "dentate gyrus"], "accession": "GSE179078", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE179078\\GSE179078_metadata.csv"}

reasoning: matches

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 10, "n_metadata": 10, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE179078\\aligned\\aligned_metadata.csv", "columns": {"geno": {"alias_of": "characteristics_ch1.1.genotype/variation", "recode": {"Wild-type": "WT", "Global Fndc5 Knock out": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE179078\\aligned\\design_metadata.csv", "sha256": "fe15128a61f9f83179806516c6c18b00f70adc8e87964cab7d1f71696fd0dd3a", "levels": {"geno": {"WT": 5, "KO": 5}}}}

reasoning: description 20190116_WT1_CW6530_S1 contains matrix column WT1.

### matrix (valid, not_started)

final: {"source": "GSE179078_cw2001-WT_F5KO_DG_STAR_Gene_Counts.csv.gz", "paper_input": "DESeq2 counts", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE179078\\aligned\\aligned_matrix.csv", "sha256": "b585677a7cb72e73804d5b180999dc7aeded3587174e9e798dd1c3d5521ce708", "n_features": 24982, "n_samples": 10, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 617447.0, "median": 69.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integers, unequal library sizes (26-44M), STAR gene counts.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "geno", "control": "WT", "treatment": "KO", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34417591\\GSE179078\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: S2.5.p2, FIG4c. The request is the exercise effect.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 10 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

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
