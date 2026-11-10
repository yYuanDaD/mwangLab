# Review packet B (the analysis' decisions): GSE198826

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: every sample is dexamethasone-treated and sedentary (GEO treatment constant 'Dexamethasone treated'; S4.3.p2). The only factors are genotype (LSD1-mKO vs WT) and muscle; a genotype contrast under glucocorticoid does not answer how exercise affects gene expression.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE198911 (SuperSeries, S12.p1)", "GSE198826 (Dex sub-series)", "GSE198827 (VWR sub-series)"], "assay": "poly(A) RNA-seq, NextSeq 500 75 bp SE, STAR mm10 (S4.10.p1)", "sample_inclusion": "Dex-treated (1 mg/kg, 7 d) male WT and LSD1-mKO mice; gastrocnemius and soleus (S2.3.p1, S4.3.p2); GEO: WT 3 + mKO 5 per muscle", "factors": [{"name": "genotype", "levels": ["WT", "LSD1-mKO"]}, {"name": "tissue", "levels": ["Gas", "Sol"]}], "primary_estimand": "LSD1-mKO vs WT gene expression in Dex-treated muscle (glucocorticoid atrophy model), separately per muscle; no exercise factor", "planned_contrasts": ["mKO vs WT, Dex Gas (S2.3.p1; paper: 150 up / 117 down = 267 DEGs)", "mKO vs WT, Dex Sol (S2.3.p1, Fig 2E; count not stated in text)"], "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S4.10.p1"}, "paper_method": "edgeR, FDR < 0.05 (S4.10.p1)", "paper_results": "Gas: 150 up, 117 down in mKO (S2.3.p1)"}

reasoning: The paper's only exercise experiment is voluntary wheel running (S2.5, S2.6, S4.4); its RNA-seq is GSE198827. GSE198826 is the dexamethasone experiment (S2.3.p1; S4.10.p1 'For the dataset from Dex administration experiment, Edge R ...'). GEO characteristics treatment = 'Dexamethasone treated' for all 16 samples.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\prep\\GSE198826_counts_merged.csv", "owned": true, "checks": ["GEO series_id lists GSE198911, the SuperSeries named in S12.p1/S12.p3", "contact Araki H, Kumamoto Univ. matches authors", "data_processing repeats the paper's edgeR FDR 0.05 rule", "16 samples: Gas/Sol x WT/mKO, Dex-treated"], "accession": "GSE198826", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE198826\\GSE198826_metadata.csv"}

reasoning: S12.p1 deposits GSE198911; GSE198826 is its sub-series. Counts files are featureCounts outputs whose library labels (araki1.., a1..) match the bracketed labels in GEO titles.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 16, "n_metadata": 16, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\GSE198826\\aligned\\aligned_metadata.csv", "columns": {"geno": {"source": "title", "regex": "^(WT|LSD1-mKO)\\d", "recode": {"WT": "WT", "LSD1-mKO": "KO"}}, "tissue": {"source": "title", "regex": " (Gas|Sol) "}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\GSE198826\\aligned\\design_metadata.csv", "sha256": "6acdf908487a50dce608c3227ae45b3238da585056e735411d758b03dfd5dd46", "levels": {"geno": {"KO": 10, "WT": 6}, "tissue": {"Gas": 8, "Sol": 8}}}}

reasoning: Matrix columns are featureCounts library labels (renamed from BAM paths by prep_GSE198826_counts.py); each GEO title carries the label in brackets, e.g. 'WT3 Gas Dex [araki8]'. Exact match on that derived key; no positional alignment.

### matrix (valid, not_started)

final: {"source": "GSE198826_counts_Gas.txt.gz + GSE198826_counts_Sol.txt.gz (featureCounts v1.5.2, gene level)", "paper_input": "STAR + edgeR on read counts (S4.10.p1)", "matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\GSE198826\\aligned\\aligned_matrix.csv", "sha256": "6f9e404d2fb03dbea34cb013a4cedabf64f64537c0fbc7e3fdaeca5979a2de9a", "n_features": 24421, "n_samples": 16, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1283080.0, "median": 16.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: Integer featureCounts read counts (header names featureCounts v1.5.2); the all_genes_FC files are edgeR result tables, not sample matrices.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\GSE198826\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 2}}

reasoning: Request asks for the exercise effect. The exercise (VWR) RNA-seq is GSE198827; this series has no exercise arm.

rejected alternatives: [{"value": "geno KO vs WT within Gas/Sol (paper's edgeR contrast)", "reason_rejected": "genotype effect under dexamethasone, not an exercise effect"}, {"value": "tissue Sol vs Gas", "reason_rejected": "muscle-type difference, not exercise; not a paper contrast"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 16 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample sizes",
    "paper": "qPCR WT n=8, mKO n=11 (Fig 2C); RNA-seq n not stated",
    "data": "RNA-seq WT 3, mKO 5 per muscle",
    "disposition": "recorded_only"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID36695573 (GSE198826, GSE198827)

Paper: LSD1 defines the fiber type-selective responsiveness to environmental stress in skeletal muscle (PMC9876571). SuperSeries GSE198911 (S12.p1).

## Outcome: refused (both cases, at the design gate)

| Case | What it holds | Paper's DE analysis | Decision |
|---|---|---|---|
| GSE198826 | 16 Dex-treated samples: gastrocnemius and soleus, WT 3 vs LSD1-mKO 5 each (featureCounts raw counts) | edgeR mKO vs WT, FDR < 0.05; Gas 150 up / 117 down (S2.3.p1, S4.10.p1) | refused: no exercise factor (all samples dexamethasone-treated, sedentary) |
| GSE198827 | 6 soleus samples, all VWR-trained: WT 3 vs LSD1-mKO 3 (estimated counts) | DESeq2, then top 1000 MAD genes (mean TPM > 1) with k-means; no DEG count or significance threshold (S2.6.p1, S4.10.p1) | refused: exercise is constant; there is no sedentary RNA-seq arm |

The only exercise experiment in the paper is voluntary wheel running (S2.5, S4.4). Exercise vs sedentary appears only in phenotype and qPCR data (Fig 4B; Fig 5, figure supplement 1A). The RNA-seq covers trained mice only, so the one contrast available is genotype with exercise held constant. A genotype contrast does not tell us how exercise affects gene expression, and the exercise x genotype interaction cannot be estimated.

## What ran

- `inspect` on both series. Data were already cached.
- `prep/prep_GSE198826_counts.py` merges the Gas and Sol featureCounts files. It skips the `#` command line and renames BAM-path columns to the library labels (araki1, a1, ...) found in brackets in the GEO titles. Output: `prep/GSE198826_counts_merged.csv` (24421 x 16).
- `case_runner execute case_spec.json`. Gates recorded: paper_reconstruction, ownership, alignment, matrix, design (refused).
  - Alignment: exact match on a derived key, 16/16 and 6/6.
  - Suitability: "analyzable" for the genotype comparisons only. This verdict does not affect the refusal.
  - The validator ran on 10 records with 0 errors.
- No DE executions and no enrichment were run.

## DEG counts vs paper

None computed, because both cases were refused before execution.
- Paper threshold for Dex (GSE198826): FDR < 0.05 with no fold-change cutoff. Paper count for Gas: 267 (150 up / 117 down).
- Paper threshold for VWR (GSE198827): none. The paper ranks genes by MAD instead of applying a threshold.

## Deviations

- The GSE198826 matrix had to be rebuilt by a prep script (listed in `prep_scripts`) because the deposited file has a featureCoun ... [923 more characters]
