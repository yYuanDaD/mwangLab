# Review packet B (the analysis' decisions): GSE198827

## Mechanical flags

- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"characteristics_ch1.2.treatment": ["VWR training"], "treatment_protocol_ch1": ["Eight-week-old control or LSD1-mKO mice were single-housed in cages with free access to a vertical running wheel (Shinano Seisakusho) for 38 days. After three days of familiarization,  LSD1-KO was induced by  tamoxifen injection at a dose of 75 mg/kg for five consecutive days, and running distance was measured during the next 30 days."]}, "note": "the stop reason says no exercise arm, ... [40 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all 6 sequenced soleus samples are VWR-trained (GEO treatment constant 'VWR training'); no sedentary RNA-seq arm was deposited. The only contrast is genotype (LSD1-mKO vs WT) within exercised mice, which does not estimate how exercise affects gene expression, and the exercise x genotype interaction is not estimable.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE198911 (SuperSeries, S12.p1)", "GSE198827 (VWR sub-series)"], "assay": "poly(A) RNA-seq, NextSeq 500 75 bp SE, STAR mm10 (S4.10.p1)", "sample_inclusion": "Soleus from VWR-trained (38 d) male WT (n=3) and LSD1-mKO (n=3) mice (S2.6.p1, Fig 5C); no sedentary RNA-seq samples (sedentary Esrrg only by qPCR, Fig 5-figure supplement 1A)", "factors": [{"name": "genotype", "levels": ["WT", "LSD1-mKO"]}], "primary_estimand": "LSD1-mKO vs WT soleus expression among VWR-trained mice (LSD1-dependent genes under exercise); exercise itself is constant", "planned_contrasts": ["mKO vs WT, VWR soleus (S2.6.p1; paper: top 1000 MAD-ranked genes among mean TPM > 1, k-means cluster 6; no DEG count)"], "paper_threshold": {"metric": "none", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "note": "top 1000 genes by median absolute deviation among genes with mean TPM > 1; no significance cutoff", "source_locator": "S4.10.p1"}, "paper_method": "DESeq2 (S4.10.p1); MAD top-1000 + k-means (ComplexHeatmap)", "paper_results": "cluster 6 up in mKO, mitochondrial/OXPHOS GO; Esrrg up in mKO (S2.6.p1, Fig 5A-C)"}

reasoning: S4.4.p1 and S2.5.p1 define the exercise experiment: VWR vs sedentary for phenotypes, but RNA-seq (S2.6.p1, Fig 5A/C) used only trained WT and mKO soleus. GEO characteristics treatment = 'VWR training' for all 6 samples.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE198827\\GSE198827_GeneMat_Count.txt.gz", "owned": true, "checks": ["GEO series_id lists GSE198911 (S12.p1)", "data_processing repeats the paper's DESeq2 + top-1000 MAD rule", "6 soleus samples, WT 3 / mKO 3, matching Fig 5C n=3"], "accession": "GSE198827", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE198827\\GSE198827_metadata.csv"}

reasoning: Sub-series of the paper's SuperSeries; metadata and design match S2.6.p1 and Fig 5C.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\GSE198827\\aligned\\aligned_metadata.csv", "columns": {"geno": {"source": "title", "regex": "^\\d+_(WT|LSD1-mKO)\\d", "recode": {"WT": "WT", "LSD1-mKO": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\GSE198827\\aligned\\design_metadata.csv", "sha256": "f2793740ea934b69b9e4a8eda4654bffdf570e2a0f734d6735bb808e58ed4abe", "levels": {"geno": {"WT": 3, "KO": 3}}}}

reasoning: Matrix columns 1..6 equal the numeric prefix of each GEO title ('1_WT1 Sol VWR'); exact match on that derived key.

### matrix (valid, not_started)

final: {"source": "GSE198827_GeneMat_Count.txt.gz", "paper_input": "DESeq2 on counts (S4.10.p1)", "matrix_type": "estimated counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\GSE198827\\aligned\\aligned_matrix.csv", "sha256": "0e974e8d98db703e54e06a2e677e3024f1af11674d86397d82d6133878d88cfc", "n_features": 24411, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 2, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 509308.71, "median": 16.0, "integer_fraction": 0.9067, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Column sums 8.9-13.8 M (library sizes), 14% of nonzero values fractional (e.g. 1149.70): expected counts from a quantifier, not TPM. All_gene_FC is a DESeq2 result table.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36695573\\GSE198827\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Request asks for the exercise effect; exercise is not a varying factor in the sequenced samples.

rejected alternatives: [{"value": "geno KO vs WT among VWR-trained soleus (paper's DESeq2 contrast)", "reason_rejected": "genotype effect with exercise held constant; a genotype contrast does not answer an exercise question"}, {"value": "VWR vs sedentary", "reason_rejected": "no sedentary samples in the RNA-seq (sedentary only in qPCR/phenotype data, Fig 4B, Fig 5-figure supplement 1A)"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise arm",
    "paper": "VWR vs sedentary for phenotypes (Fig 4B: sedentary WT n=8, mKO n=7)",
    "data": "RNA-seq only VWR-trained WT 3 / mKO 3",
    "disposition": "blocks_estimand"
  },
  {
    "item": "DE output",
    "paper": "top 1000 MAD genes + k-means, no DEG count",
    "data": "DESeq2 table deposited",
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
