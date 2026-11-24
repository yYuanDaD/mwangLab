# Review packet B (the analysis' decisions): GSE242445

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the 23 osteocyte samples vary only by genotype (FNDC5 KO vs WT), sex and diet (control vs low-calcium). No sample is exercised, trained or sedentary-as-control (paper S4.15-S4.16, GEO treatment_protocol). The requested exercise estimand cannot be identified; manufacturing it from KO vs WT (irisin as an 'exercise myokine') would change the estimand.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE242445"], "assay": "bulk RNA-seq of long-bone osteocyte-enriched fractions, mouse, Illumina NovaSeq 6000 (S4.16.p1, S11.p1)", "factors": {"genotype": ["WT", "FNDC5 global KO"], "sex": ["female", "male"], "diet": ["control (0.6% Ca)", "low-calcium (0.01% Ca) 2 weeks"]}, "sample_inclusion": "3 per genotype x sex x diet cell; KO female control sample 23 excluded for Y-chromosome reads / low Xist (S4.15.p1)", "primary_estimand": "Effect of FNDC5/irisin deletion (KO vs WT) and of sex on the osteocyte transcriptome, under control and low-calcium diet. No exercise intervention: exercise appears only as background on irisin as an exercise-induced myokine (ABS.p1, S1.p1, S1.p5).", "planned_contrasts": ["WT F vs WT M (control diet) (S2.x, Supplementary file 3)", "KO F vs WT F and KO M vs WT M (control diet) (Supplementary file 3)", "KO lc vs WT lc within each sex (Supplementary file 4)"], "exercise_arm": "none", "paper_method": "DESeq2, median-of-ratios normalization, independent filtering (S4.16.p1)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S4.16.p1"}}

reasoning: The paper's transcriptomic estimands are genotype (FNDC5 KO vs WT), sex and low-calcium diet. Exercise is mentioned only as the stimulus that releases irisin in muscle (ABS.p1, S1.p1); no mouse in the study is exercised or kept sedentary as an experimental arm. Threshold: unadjusted p < 0.01 and |log2FC| > 1 (S4.16.p1).

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE242445\\GSE242445_AllnormalizedReadCounts.csv", "owned": true, "checks": ["S11.p1 names GSE242445 as the osteocyte transcriptome deposit", "23 samples = 24 sequenced minus excluded sample 23 (S4.15.p1); KO_F_C_23 is absent from the matrix", "series contributor Shimonty / Bonewald Lab matches authors"], "accession": "GSE242445", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE242445\\GSE242445_metadata.csv"}

reasoning: Paper data-availability statement names GSE242445; sample labels encode genotype/sex/diet exactly as in the paper's design.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 23, "n_metadata": 23, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38661340\\GSE242445\\aligned\\aligned_metadata.csv", "columns": {"geno": {"source": "key", "regex": "^(WT|KO)_"}, "sex": {"source": "key", "regex": "^[A-Z]+_(F|M)_"}, "diet": {"source": "key", "regex": "^[A-Z]+_[FM]_(C|LC)_"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38661340\\GSE242445\\aligned\\design_metadata.csv", "sha256": "e73e56818b78cc8411d0487fc7b360869437cd1d1bf1b4f5eb1cc92a54f7b4a4", "levels": {"geno": {"WT": 12, "KO": 11}, "sex": {"M": 12, "F": 11}, "diet": {"C": 12, "LC": 11}}}}

reasoning: Matrix columns (e.g. WT_F_C_1) sit inside the GEO title in brackets; exact match on that derived key for all 23. Factors parsed from the key. Note: GEO characteristics 'treatment' is constant ('2 weeks of low-calcium-diet') for all samples although titles distinguish control (C) and low-calcium (LC); title is used.

### matrix (valid, not_started)

final: {"source": "GSE242445_AllnormalizedReadCounts.csv", "paper_input": "raw read counts into DESeq2 (S4.16.p1)", "matrix_type": "normalized counts (DESeq2 median-of-ratios)", "recommended_method": "none (no raw integer counts deposited; DESeq2 would need rounding of normalized values)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38661340\\GSE242445\\aligned\\aligned_matrix.csv", "sha256": "f1d9a01bee4e5ce72abc37ecc5210a6493b324348bdf324e7176fd553b9760ba", "n_features": 21402, "n_samples": 23, "annotation_columns_dropped": [], "duplicated_feature_ids": 2, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1479814.41282828, "median": 124.217935519875, "integer_fraction": 0.1959, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File is named AllnormalizedReadCounts; integer fraction 0.20, non-integer values; data_processing says DESeq2 median-of-ratios normalization. It is size-factor-normalized counts, not the raw counts the paper modeled. Recorded for completeness; the case stops at design regardless.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": null, "contrasts": [], "exercise_factor": null, "suitability": {"verdict": "partially_analyzable", "failed": [], "warnings": ["sample_size"], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38661340\\GSE242445\\suitability\\suitability.md", "n_comparisons": 18, "n_analyzable": 12}}

reasoning: Paper-first: the study map has no exercise factor. Refused at design per the skill's stop rule (sequenced sample set with no exercise arm).

rejected alternatives: [{"value": "geno KO vs WT as an exercise proxy", "reason_rejected": "Irisin deletion is a genetic loss of one myokine, not an exercise intervention; it does not estimate the effect of exercise on gene expression."}, {"value": "diet LC vs C", "reason_rejected": "Calcium deficiency, not exercise."}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **partially_analyzable**; check: sample_size
- | Check | Status | Detail |
- | Grouping | pass | geno: 2 levels; sex: 2 levels; diet: 2 levels |
- | Sample size | partial | 12/18 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 23 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |
- | geno_KO_vs_WT_sex-F_diet-C | simple | F/C/KO (3), F/C/WT (3) | yes |
- | geno_KO_vs_WT_sex-F_diet-LC | simple | F/LC/KO (2), F/LC/WT (3) | no |
- | geno_KO_vs_WT_sex-M_diet-C | simple | M/C/KO (3), M/C/WT (3) | yes |
- | geno_KO_vs_WT_sex-M_diet-LC | simple | M/LC/KO (3), M/LC/WT (3) | yes |
- | sex_F_vs_M_geno-KO_diet-C | simple | KO/C/F (3), KO/C/M (3) | yes |
- | sex_F_vs_M_geno-KO_diet-LC | simple | KO/LC/F (2), KO/LC/M (3) | no |
- | sex_F_vs_M_geno-WT_diet-C | simple | WT/C/F (3), WT/C/M (3) | yes |
- | sex_F_vs_M_geno-WT_diet-LC | simple | WT/LC/F (3), WT/LC/M (3) | yes |
- | diet_LC_vs_C_geno-KO_sex-F | simple | KO/F/LC (2), KO/F/C (3) | no |
- | diet_LC_vs_C_geno-KO_sex-M | simple | KO/M/LC (3), KO/M/C (3) | yes |
- | diet_LC_vs_C_geno-WT_sex-F | simple | WT/F/LC (3), WT/F/C (3) | yes |
- | diet_LC_vs_C_geno-WT_sex-M | simple | WT/M/LC (3), WT/M/C (3) | yes |
- | geno_sex_KO_F_vs_WT_M_diet-C | interaction | C/KO/F (3), C/WT/F (3), C/KO/M (3), C/WT/M (3) | yes |
- | geno_sex_KO_F_vs_WT_M_diet-LC | interaction | LC/KO/F (2), LC/WT/F (3), LC/KO/M (3), LC/WT/M (3) | no |
- | geno_diet_KO_LC_vs_WT_C_sex-F | interaction | F/KO/LC (2), F/WT/LC (3), F/KO/C (3), F/WT/C (3) | no |
- | geno_diet_KO_LC_vs_WT_C_sex-M | interaction | M/KO/LC (3), M/WT/LC (3), M/KO/C (3), M/WT/C (3) | yes |
- | sex_diet_F_LC_vs_M_C_geno-KO | interaction | KO/F/LC (2), KO/M/LC (3), KO/F/C (3), KO/M/C (3) | no |
- | sex_diet_F_LC_vs_M_C_geno-WT | interaction | WT/F/LC (3), WT/M/LC (3), WT/F/C (3), WT/M/C (3) | yes |

## Recorded paper-data discrepancies

[
  {
    "item": "GEO treatment characteristic",
    "paper": "control diet and low-calcium diet groups (S2.3.p1)",
    "data": "characteristics_ch1.5.treatment = '2 weeks of low-calcium-diet' for all 23 samples; titles carry C/LC",
    "disposition": "executable_without_change"
  },
  {
    "item": "matrix scale",
    "paper": "raw read counts into DESeq2 (S4.16.p1)",
    "data": "only DESeq2-normalized counts deposited",
    "disposition": "recorded; not acted on because the case is refused at design"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID38661340 / GSE242445

**Status: refused at `design`. The study has no exercise contrast.**

## What ran
1. `python -m tools.case_runner inspect GSE242445 --data-root E:/agent/mwangLab_pdf/data` used the cached series. It has 23 samples and one matrix, `GSE242445_AllnormalizedReadCounts.csv` (21,402 gene symbols × 23).
2. Paper read: PMC11045224.paper.md, sections ABS, S1, S2.1–S2.3, S4.15 and S4.16.
3. `python -m tools.case_runner execute case_spec.json` recorded the gates `paper_reconstruction`, `ownership`, `alignment`, `matrix` and `design`. The `design` gate is refused.
   - The validator returned 5 records and 0 errors.
   - Alignment matched exactly on the bracketed key in the GEO title: 23/23.
   - The suitability report says sex is consistent for all 23 samples.

## Why it was refused
- The paper's RNA-seq estimands are FNDC5/irisin KO vs WT, female vs male, and low-calcium diet vs control diet. These appear in S4.16.p1 and Supplementary files 3–4.
- Exercise is mentioned only as background: irisin is a myokine released from exercised muscle (ABS.p1, S1.p1). No mouse was exercised, trained or used as a sedentary control.
- The GEO treatment protocol confirms the design: diet × genotype × sex, 5-month-old mice.
- Using KO vs WT as a stand-in for "exercise" would change the estimand, so the case was refused.
- No DE, threshold or enrichment ran.

## DEG counts vs the paper
- No counts were produced, because the case was refused.
- The paper's threshold is unadjusted p < 0.01 and |log2FC| > 1, with DESeq2 and independent filtering (S4.16.p1).
- The text gives no single DEG count to compare against; the gene lists are in Supplementary files 3 and 4.

## Deviations and observations
- **GEO annotation error:** the `characteristics_ch1.5.treatment` field reads "2 weeks of low-calcium-diet" for all 23 samples. The titles (C vs LC) carry the real diet labels, so I used the titles.
- **Matrix:** only DESeq2 median-of-ratios normalized counts were deposited (20% of values are integers). The paper modelled raw counts. This was recorded at the `matrix` gate and not acted on.
- **Excluded sample:** the paper excluded KO female control sample 23 (S4.15.p1), and it is absent from the matrix. The KO female low-calcium cell therefore has n=2 (samples 5 and 6).

## Tool problems
- **Inspect / runner duplicate IDs:** inspect reported `duplicated_feature_ids: 2` in the matrix. This did not matter because nothing was executed.
- **Suitability report dat ... [222 more characters]
