# Review packet B (the analysis' decisions): GSE185154

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast in the sequenced samples. GSE185154 contains only genotype (Cdk4 WT/RR/KO, MLC-Cre, E2F3 mKO) x muscle (QA, soleus) groups with n = 3, all without an exercise intervention; the paper's exercise data (S2.5.p1, FIG4A-C, Supplemental Figure 11) are qPCR/western, not RNA-seq. The genotype contrasts the paper did sequence do not answer how exercise affects gene expression, and no column of the metadata defines exercise.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE185154", "GSE101820 (human muscle arrays, separate cohort, not analyzed here)"], "assay": "bulk polyA RNA-seq, quadriceps (QA) and soleus (SOL), mouse, n = 3 per group (S4.11.p1)", "factors": {"genotype": ["Cdk4 WT", "Cdk4 R/R", "Cdk4 KO", "MLC-Cre (E2F3 WT control)", "E2F3 mKO"], "tissue": ["quadriceps", "soleus"], "exercise": "not a factor of the RNA-seq; exercise appears only in qPCR/western experiments (S2.5.p1, FIG4, Supplemental Figure 11)"}, "sample_inclusion": "30 sequenced samples = 5 genotypes x 2 muscles x 3 mice; all sedentary/unexercised as described", "primary_estimand": "Effect of Cdk4/E2F3 genotype on muscle transcriptome (Cdk4 R/R vs WT in QA, FIG2D; Cdk4 KO vs WT in soleus, FIG3B; E2F3 mKO vs MLC-Cre in soleus, FIG5C). No exercise estimand is defined for the RNA-seq.", "planned_contrasts": ["Cdk4 R/R vs Cdk4 WT, quadriceps (FIG2D-F; count not reported)", "Cdk4 KO vs Cdk4 WT, soleus (FIG3B-C; count not reported)", "E2F3 mKO vs E2F3 WT, soleus (FIG5C-D; count not reported)", "Overlaps: 199 genes RR & E2F3mKO, 483 genes KO & E2F3mKO (FIG6A, FIG6D; DEGs at P < 0.05)"], "exercise_contrast": "none in GSE185154; exercise effects (MyoD1, Pgc-1a, E2F3, p16) are measured by qPCR and western blot (S2.5.p1, FIG4A-C)", "repeated_measure_unit": "not_reported (independent mice)", "normalization": "featureCounts, RPKM (S4.11.p1); GEO deposits FPKM only", "paper_method": "DESeq2 (S4.11.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_met ... [178 more characters]

reasoning: S4.11.p1 describes QA and soleus RNA-seq, n = 3 per group, DESeq2, adjusted P < 0.05. S4.15.p1 names GSE185154. The RNA-seq figures (FIG2D, FIG3B, FIG5C, FIG6) compare genotypes only. Exercise in this paper is a phenotype test (treadmill capacity, S4.3.p1) and a qPCR/western experiment in WT and Cdk4 R/R mice (S2.5.p1, FIG4A-C, Supplemental Figure 11); none of it was sequenced.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE185154\\GSE185154_30_samples_QA_SOL_muscle.txt.gz", "owned": true, "checks": ["S4.15.p1 names GSE185154 as the RNA-seq deposit", "metadata series_id = GSE185154; contact at NIH matches the authors' institution", "30 samples = 5 genotypes (Wild Type, CDK4RR, CDK4KO, MLC-Cre, E2F3-mKO) x quadriceps/soleus x 3, matching S4.11.p1 (n = 3 each group) and the genotypes of FIG2/3/5", "matrix file name GSE185154_30_samples_QA_SOL_muscle carries the accession and 30 sample columns"], "accession": "GSE185154", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE185154\\GSE185154_metadata.csv"}

reasoning: The paper names the accession; samples, tissues and genotypes match the paper's RNA-seq description.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 30, "n_metadata": 30, "coverage": 1.0, "unmatched_matrix_columns": ["gene_chr", "gene_start", "gene_end", "gene_length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37395281\\GSE185154\\aligned\\aligned_metadata.csv", "columns": {"genotype": {"alias_of": "characteristics_ch1.3.genotype/variation", "recode": {"Wild Type": "WT", "CDK4RR": "RR", "CDK4KO": "KO", "MLC-Cre": "MLCCre", "E2F3-mKO": "E2F3mKO"}}, "tissue": {"alias_of": "source_name_ch1", "recode": {"Quadriceps": "QA", "Soleus": "SOL"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37395281\\GSE185154\\aligned\\design_metadata.csv", "sha256": "3046e0d04062bc5c939c8040770eeb591ff91aaca3ee46aff1a35b4eee646c2a", "levels": {"genotype": {"WT": 6, "RR": 6, "KO": 6, "MLCCre": 6, "E2F3mKO": 6}, "tissue": {"QA": 15, "SOL": 15}}}}

reasoning: Matrix columns (QW1, SR2, ...) are the bracketed codes at the end of the GEO title (inspect alignment_keys: 30/30). Exact match on that derived key. Genotype and tissue come from the characteristics columns.

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37395281\\GSE185154\\aligned\\aligned_matrix.csv", "sha256": "ebb8184ad06a5325250aa8c2db09173f276d1dfea9a46a60c065e07626c67473", "n_features": 54532, "n_samples": 30, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 122646.2445, "median": 0.0, "integer_fraction": 0.6513, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Values are non-integer (integer fraction 0.65 driven by zeros, Gnai3 = 2.62) and GEO data_processing says the supplementary file holds FPKM values computed from featureCounts. The paper ran DESeq2 on counts (S4.11.p1), which are not deposited; any DE here would need limma on log2(FPKM+1) as a declared deviation.

### design (refused, not_started)

final: {"suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37395281\\GSE185154\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: The request is an exercise effect. The paper's RNA-seq (S4.11.p1, FIG2D, FIG3B, FIG5C, FIG6) compares genotypes in unexercised mice; the metadata has no exercise, training or time column. The estimand cannot be identified from these data.

rejected alternatives: [{"value": "genotype contrasts (RR vs WT in QA; KO vs WT and E2F3mKO vs MLCCre in soleus)", "reason_rejected": "valid paper contrasts but they estimate a genetic effect, not an exercise effect; relabeling them as exercise would misstate the estimand"}, {"value": "soleus vs quadriceps (oxidative vs glycolytic muscle)", "reason_rejected": "tissue comparison, not exercise; not a paper contrast"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix input",
    "paper": "DESeq2 on featureCounts read counts (S4.11.p1)",
    "data": "GEO supplementary file holds FPKM only",
    "disposition": "would require limma on log2(FPKM+1) as a declared deviation; moot because the case stops at design"
  },
  {
    "item": "DEG threshold",
    "paper": "Methods: DESeq2 adjusted P < 0.05 (S4.11.p1)",
    "data": "FIG5C and FIG6A/D legends use P < 0.05 for DEGs and overlaps",
    "disposition": "recorded; moot because the case stops at design"
  },
  {
    "item": "exercise",
    "paper": "exercise effects measured by qPCR/western in WT and Cdk4 R/R mice (S2.5.p1, FIG4)",
    "data": "no exercised samples in GSE185154",
    "disposition": "refused at design"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 37395281 / GSE185154

**Status: refused at the `design` gate.** GSE185154 has no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE185154 --data-root E:/agent/mwangLab_pdf/data`: downloaded the series. It has one matrix, `GSE185154_30_samples_QA_SOL_muscle.txt.gz` (54,532 Ensembl genes x 30 samples, FPKM), plus the metadata.
- Read the paper (`PMC10313363.paper.md`): S4.11.p1 (RNA-seq methods), S4.15.p1 (accession), FIG2/3/5/6 (the RNA-seq figures), S2.5.p1/FIG4 (the exercise experiments).
- Wrote `case_spec.json` with five gates: paper_reconstruction, ownership, alignment, matrix and design. Design is `refused`.
- `python -m tools.case_runner execute case_spec.json` completed. The validator found 5 records and 0 errors. The case route is `stopped:design`.

## Gate decisions
- **paper_reconstruction**
  - The RNA-seq covers quadriceps and soleus, n = 3 per group.
  - It compares genotypes only: Cdk4 R/R vs WT (QA, FIG2D), Cdk4 KO vs WT (soleus, FIG3B) and E2F3 mKO vs MLC-Cre (soleus, FIG5C), plus the overlaps in FIG6.
  - Method: DESeq2 with adjusted P < 0.05 (S4.11.p1).
  - Exercise appears only in treadmill capacity tests (S4.3.p1) and in qPCR/western blots of exercised WT and Cdk4 R/R muscle (S2.5.p1, FIG4A-C, Suppl. Fig. 11). None of that was sequenced.
- **ownership**: owned.
  - S4.15.p1 names GSE185154.
  - The 30 samples are 5 genotypes x 2 muscles x 3 mice, which matches the paper.
- **alignment**: 30/30 exact matches.
  - The key is the bracketed code at the end of the GEO title (e.g. `[QW1]`), which matches the matrix column names.
  - Derived columns: `genotype` (WT/RR/KO/MLCCre/E2F3mKO) and `tissue` (QA/SOL).
- **matrix**: FPKM.
  - The values are non-integer, and GEO `data_processing` says the file holds FPKM values.
  - The paper's DESeq2 input (read counts) is not deposited. Any DE here would need limma on log2(FPKM+1) as a declared deviation.
- **design**: refused.
  - No sample was exercised, and no metadata column records exercise, training or time.
  - The genotype contrasts are real paper contrasts, but they estimate a genetic effect. Relabelling them as an exercise effect would misstate the estimand.
  - Rejected alternatives are listed under `candidates` in the spec.

## DEG counts vs paper
- None computed, because the case stopped at design.
- Paper threshold: DESeq2 adjusted P < 0.05, no fold-change cutoff (S4.11.p1).
- The paper gives no per-contrast DEG counts. It reports only overlap sets ... [1310 more characters]
