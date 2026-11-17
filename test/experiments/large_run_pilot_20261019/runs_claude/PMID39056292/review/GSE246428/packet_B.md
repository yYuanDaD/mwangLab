# Review packet B (the analysis' decisions): GSE246428

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: every sequenced sample is a sedentary gastrocnemius from WT or SPAG7 KO mice (only factor genotype, 5 WT / 4 KO). The paper's exercise data are treadmill endurance phenotypes (S2.3.p1, S4.12.p1), not sequenced conditions, so an exercise effect on gene expression cannot be identified. Relabelling the KO-vs-WT genotype contrast as an exercise effect would change the estimand.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE246428"], "assay": "bulk RNA-seq (polyA, NovaSeq 2x150), gastrocnemius muscle, 28-week-old female mice (S4.17.p1, S4.18.p1, S4.1.p2)", "factors": {"genotype": ["WT", "SPAG7 KO"]}, "sample_inclusion": "WT and SPAG7 KO gastrocnemius; Fig 3K legend says n=7; two samples removed for a batch effect and a label mismatch (S4.19.p1); GEO deposits 9 samples (5 WT, 4 KO)", "primary_estimand": "genotype effect (SPAG7 KO vs WT) on sedentary gastrocnemius transcriptome; no exercise intervention in the sequenced samples. Exercise appears only as a phenotype readout (treadmill endurance test, S2.3.p1, S4.12.p1) and no exercised animals were sequenced", "planned_contrasts": ["SPAG7 KO vs WT gastrocnemius (S2.3.p2; paper: 1,848 up / 2,291 down = 4,139 DEGs)"], "exercise_contrast": "not_reported", "repeated_measure_unit": "not_reported (independent animals)", "normalization": "Salmon -> tximport gene-level counts rounded to integers (S4.19.p1; GEO data_processing)", "paper_method": "DESeq2 v1.34.0 (~ genotype implied); apeglm shrinkage for GSEA; clusterProfiler ORA/GSEA (S4.19.p1)", "paper_threshold": {"metric": "not_reported", "cutoff": "not_reported", "effect_metric": "not_reported", "effect_cutoff": "not_reported", "source_locator": "S2.3.p2 says 'significantly' without a stated rule; S4.19.p1 states no cutoff"}, "paper_results": {"up": 1848, "down": 2291, "named_genes": ["Hsd17b10 (most downregulated)"], "pathways": "mitochondrial function GO terms down (Fig 3L)"}}

reasoning: The only sequencing dataset (DA.p1 -> GSE246428) is gastrocnemius RNA-seq from WT vs germline SPAG7 KO females (S4.17.p1, Fig 3K). The paper's exercise content is a treadmill endurance test used as a functional readout (S2.3.p1, S4.12.p1, Fig 3A-B); no exercise-trained or acutely exercised group was sequenced. The DEG threshold is not stated.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE246428\\GSE246428_Spag7_raw_counts.txt.gz", "owned": true, "checks": ["DA.p1 names GSE246428", "GEO source/tissue = gastrocnemius muscle, Mus musculus, matches S4.17.p1", "GEO data_processing (STAR/Salmon, GRCm39 Ens106, tximport rounded, DESeq2 v1.34.0) matches S4.19.p1", "genotype WT/Spag7 KO matches the paper's RNA-seq contrast"], "accession": "GSE246428", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE246428\\GSE246428_metadata.csv"}

reasoning: Series is cited in the data availability statement and its processing text matches the methods verbatim.

### alignment (valid, not_started)

final: {"method": "exact:description", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39056292\\GSE246428\\aligned\\aligned_metadata.csv", "columns": {"genotype": {"alias_of": "characteristics_ch1.1.genotype", "recode": {"WT": "WT", "Spag7 KO": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39056292\\GSE246428\\aligned\\design_metadata.csv", "sha256": "608dd51ad4c4627a2a59a845eecece5f5e30d413bae410bbd63dd2ca272c515d", "levels": {"genotype": {"WT": 5, "KO": 4}}}}

reasoning: Raw-count matrix columns (X2..X10) equal the metadata 'description' field exactly for all 9 samples (inspect alignment_keys: 9/9). Genotype is the only grouping column.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts (Salmon/tximport, rounded to integers)", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39056292\\GSE246428\\aligned\\aligned_matrix.csv", "sha256": "539237b8f0c3bf1f2e74024ea2ab2a99ddc9eb5668a67fb0de1d77d44a523d52", "n_features": 52367, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3349097.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: GSE246428_Spag7_raw_counts.txt.gz is 100% integer; GEO data_processing states tximport gene-level estimates 'rounded to the nearest integer'; paper used DESeq2 on these (S4.19.p1). The other file holds DESeq2-normalized counts plus the authors' DE results and is not an input matrix.

rejected alternatives: [{"value": "GSE246428_Spag7_norm_counts_and_DE_results.txt.gz", "reason_rejected": "DESeq2-normalized counts mixed with authors' DE result columns; not raw input"}]

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39056292\\GSE246428\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: The request asks how exercise affects gene expression. GEO metadata has one grouping column (genotype) and the paper's RNA-seq estimand is KO vs WT (S2.3.p2). KO mice have reduced exercise capacity, but that is a genotype phenotype, not an exercise intervention.

rejected alternatives: [{"value": "genotype KO vs WT as exercise proxy", "reason_rejected": "genetic knockout, not exercise; different estimand"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample count",
    "paper": "Fig 3K legend n=7; two samples removed (batch effect, label mismatch) per S4.19.p1",
    "data": "GEO deposits 9 samples (5 WT, 4 KO); removed samples not identified",
    "disposition": "not_needed_after_refusal"
  },
  {
    "item": "requested estimand",
    "paper": "genotype (SPAG7 KO vs WT) transcriptome",
    "data": "genotype only; no exercise factor",
    "disposition": "refused"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID39056292 / GSE246428

**Status: refused at `design`.** The data cannot answer the exercise question.

## What ran
- `python -m tools.case_runner inspect GSE246428`: downloaded the series into `data/GSE246428` (it was not cached). Found two files: `GSE246428_Spag7_raw_counts.txt.gz` (9 samples, all integers) and `GSE246428_Spag7_norm_counts_and_DE_results.txt.gz` (DESeq2-normalized counts plus the authors' DE columns).
- `python -m tools.case_runner execute case_spec.json`: recorded the gates `paper_reconstruction`, `ownership`, `alignment` (exact match on `description`, 9 of 9 samples), `matrix` (Salmon/tximport estimated counts, rounded) and `design` (refused). The contract validator found 0 errors, and no external LLM call was attempted. The suitability report rated the only comparison, genotype KO vs WT, as analyzable. We did not run it, because it is not the estimand that was requested.

## Why it was refused
- The paper sequenced gastrocnemius muscle from sedentary female WT and germline SPAG7 KO mice (S4.17.p1, S2.3.p2, Fig 3K).
- GEO has one grouping column, genotype: WT 5, Spag7 KO 4.
- The paper's only exercise content is a treadmill endurance test, used as a phenotype readout (S2.3.p1, S4.12.p1, Fig 3A–B). No exercised animals were sequenced.
- So the data contain no exercise contrast. Presenting KO vs WT as an exercise effect would change the estimand.

## DEG counts compared with the paper
- **Ours:** none. No contrast was run.
- **Paper:** KO vs WT had 1,848 genes up and 2,291 down, 4,139 in total (S2.3.p2). This is a genotype contrast, not an exercise one. The most downregulated gene was Hsd17b10, and the downregulated GO terms were mitochondrial.
- **Paper's threshold:** not stated. The text only says "significantly", and the methods give no cutoff. It is recorded as `not_reported`.

## Deviations and discrepancies
- **Sample count:** the paper gives n=7 and says two samples were removed (one for a batch effect, one for a label mismatch, S4.19.p1). GEO deposits 9 samples and does not say which ones were removed. This did not matter here because the case was refused.

## Tool problems
- **Garbled text in the metadata:** the metadata CSV written at download shows mojibake in `extract_protocol_ch1` (`manufacturer鈥檚`, which should be "manufacturer's"). A UTF-8 curly apostrophe appears to have been decoded as GBK somewhere in the GEO download and metadata write path. I did not locate the line. It is cosmetic and did not affect thi ... [321 more characters]
