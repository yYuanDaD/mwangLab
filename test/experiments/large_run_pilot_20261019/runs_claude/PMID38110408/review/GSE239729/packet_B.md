# Review packet B (the analysis' decisions): GSE239729

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.1.genotype", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all 6 deposited samples are HFD-fed sedentary mice (metadata treatment constant 'HFD feeding 12 weeks'; FIG3 a 'without exercise'), differing only by genotype (3 WT vs 3 Cdo1-LKO). The exercise effect the request asks for cannot be identified from this series; the paper measured exercise effects only by RT-qPCR/western blot. The genotype contrast (LKO vs WT) is a knockout effect, not an exercise effect, and is not run as a substitute.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE239729"], "assay": "bulk RNA-seq, mouse liver (DA.p1: GSE239729 holds the RNA-seq of Fig. 3a,b,f and Supp. Fig. 2o)", "primary_estimand": "Paper's RNA-seq estimand: hepatocyte Cdo1 knockout (Cdo1-LKO) vs WT (Cdo1 flox/flox) liver transcriptome in HFD-fed mice WITHOUT exercise (S2.3.p1, FIG3 a, S4.19.p1). The requested estimand (exercise effect) is not part of the sequenced design.", "sample_inclusion": "n = 3 WT + 3 Cdo1-LKO, HFD-fed, sedentary (FIG3 a: 'HFD-fed mice without exercise', n = 3 mice per group)", "factors": {"genotype": ["WT", "Cdo1-LKO"], "diet": ["HFD (constant)"], "exercise": ["none (constant: sedentary)"]}, "planned_contrasts": ["Cdo1-LKO vs WT, HFD sedentary (FIG3 a; paper: 630 up / 672 down = 1302 DEGs at p < 0.05)"], "exercise_contrasts_in_paper": "Exercise effects (WT/LKO x sedentary/exercise, Fig. 2d design, n = 6) are measured only by RT-qPCR, western blot, mitoDNA and histology (Fig. 1b, 3c-e); none were sequenced.", "repeated_measure_unit": "none (independent mice)", "paper_method": "DESeq2 1.20.0 on Hisat2-aligned reads (S4.19.p1); two-sided Wald test", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "FIG3 a ('p < 0.05'; 'Two-sided Wald tests without adjustment')"}, "paper_results": {"Cdo1-LKO_vs_WT": {"up": 630, "down": 672, "total": 1302}}}

reasoning: DA.p1 ties GSE239729 to Fig. 3a/b/f and Supp. Fig. 2o. S4.19.p1: 'Total RNA was obtained from the liver of HFD-fed control mice and Cdo1LKO mice'; FIG3 a: LKO vs WT 'in the livers of HFD-fed mice without exercise', n = 3/group, p < 0.05, unadjusted two-sided Wald. Exercise contrasts (S2.1, S2.2, S2.3 Fig. 3c) use qPCR/WB, not RNA-seq.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38110408\\GSE239729_fpkm_gsm.csv", "owned": true, "checks": ["GEO series title equals the paper title", "DA.p1 names GSE239729", "series overall design: liver of HFD-fed control and Cdo1LKO mice", "6 GSMs (3 WT, 3 Cdo1 liver KO) match FIG3 a n = 3 per group", "contact institute Shanghai University of Sport matches the paper"], "accession": "GSE239729", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE239729\\GSE239729_metadata.csv"}

reasoning: Single processed file GSE239729_Processed_date_files.txt.gz is the only matrix; it holds 6 sample columns for the 6 GSMs.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38110408\\GSE239729\\aligned\\aligned_metadata.csv", "columns": {"genotype": {"alias_of": "characteristics_ch1.1.genotype", "recode": {"WT": "WT", "Cdo1 liver KO": "LKO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38110408\\GSE239729\\aligned\\design_metadata.csv", "sha256": "4c63d34dcfc5a0c0ed250518306aa4aa945ed852f2f52d11dec25fe384085f28", "levels": {"genotype": {"WT": 3, "LKO": 3}}}}

reasoning: The deposited matrix columns (A,B,C,A1,B1,C1) have no key in the GEO metadata, so the prep script prep_rename_columns.py renames them to GSM ids. Genotype group membership is evidence-based, not positional: Cdo1 (ENSMUSG00000033022) FPKM is 822-1072 in A/B/C and 243-272 in A1/B1/C1 (the hepatocyte KO), and log2 correlations cluster A/B/C vs A1/B1/C1. Within each genotype the replicate order (A->1, B->2, C->3) is an assumption; it does not affect any decision here because no comparison is executed and none would use within-group identity.

rejected alternatives: [{"value": "manual_review at alignment (no exact key)", "reason_rejected": "the missing column key does not bear on the stop: the whole sample set lacks an exercise arm, which the metadata and the paper state independently of column identity"}]

### matrix (valid, not_started)

final: {"matrix_type": "FPKM", "recommended_method": "limma on log2(FPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38110408\\GSE239729\\aligned\\aligned_matrix.csv", "sha256": "8f42775cca26fc7956710e03c01cb2e4b5ae399deaf5b429dea84830371bf5a2", "n_features": 54532, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 33436.06181, "median": 0.0, "integer_fraction": 0.6543, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Values are non-integer (integer fraction 0.65, mostly zeros), column sums 384k-524k (not equal library sizes), data_processing: 'FPKM of each gene was calculated based on the length of the gene and reads count'. The paper's DESeq2 input (raw counts) is not deposited as a separate file. Type is unambiguous; recorded for completeness.

### design (refused, not_started)

final: {"suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID38110408\\GSE239729\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: Grouping columns: only characteristics_ch1.1.genotype varies (WT 3, Cdo1 liver KO 3). No exercise/training/sedentary factor in metadata, titles, or series design. Paper S4.19.p1 and FIG3 a confirm the RNA-seq cohort is sedentary HFD WT vs LKO.

rejected alternatives: [{"value": "genotype_LKO_vs_WT (paper's Fig. 3a contrast)", "reason_rejected": "answers the Cdo1 knockout question, not how exercise affects gene expression; running it would substitute a different estimand"}, {"value": "associational exercise comparison", "reason_rejected": "no exercised samples exist in the series"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix type",
    "paper": "DESeq2 on read counts (S4.19.p1)",
    "data": "only FPKM deposited (data_processing mentions counts, but the single supplementary file holds FPKM)",
    "disposition": "not_reached (case refused at design)"
  },
  {
    "item": "aligner / genome",
    "paper": "Hisat2 v2.0.5 (S4.19.p1)",
    "data": "GEO data_processing says bowtie v0.12.2 to mm8 (appears to be template text; extract protocol also mentions 'Retinas')",
    "disposition": "recorded; not_reached"
  },
  {
    "item": "exercise arm",
    "paper": "exercise intervention is the paper's central factor (Fig. 2d)",
    "data": "no exercise samples sequenced",
    "disposition": "blocks the requested estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 38110408 / GSE239729

**Status: refused at `design`.** The series has no exercise contrast.

## What ran
1. `python -m tools.case_runner inspect GSE239729 --data-root E:/agent/mwangLab_pdf/data`: downloaded the series (it was not cached). It holds one processed file, `GSE239729_Processed_date_files.txt.gz`, with 54,532 Ensembl genes and 6 columns named A, B, C, A1, B1, C1.
2. Read the paper (`PMC10728194.paper.md`): DA.p1, S2.3.p1, FIG3 a, S4.19.p1, S2.1/S2.2, S4.2.
3. `prep_rename_columns.py` renamed the matrix columns to GSM ids, giving `GSE239729_fpkm_gsm.csv` (reason under Deviations).
4. `python -m tools.case_runner execute case_spec.json`: recorded paper_reconstruction, ownership, alignment, matrix and design (refused). The validator reported 0 errors on 5 records. No executions or enrichment ran.

## Why it was refused
- GEO metadata: the only field that varies is genotype (3 WT, 3 Cdo1 liver KO). Treatment is the same for every sample ("HFD feeding 12 weeks"). The series overall design is "liver of HFD-fed control mice and Cdo1LKO mice".
- Paper: FIG3 a describes the RNA-seq as Cdo1^LKO vs WT "in the livers of HFD-fed mice without exercise", n = 3 per group (S4.19.p1 agrees). The exercise effects come from the Fig. 2d design (WT/LKO × sedentary/exercise, n = 6). They were measured only by RT-qPCR, western blot, mitoDNA and EM (Fig. 1b, 3c–e), and none of those samples were sequenced.
- I rejected the paper's genotype contrast (LKO vs WT) as a substitute. It measures the effect of the knockout, not of exercise.

## DEG counts vs the paper
- Paper (Fig. 3a, LKO vs WT, HFD sedentary): 630 up and 672 down (1,302 in total). The threshold is p < 0.05 by an unadjusted two-sided Wald test (DESeq2 1.20.0), with no fold-change cutoff (FIG3 legend).
- Ours: none. No exercise contrast exists, and the genotype contrast was not run because it is outside the requested estimand.

## Deviations and caveats
- **Alignment (low confidence):** no metadata field matches the matrix column names A, B, C, A1, B1, C1, so `prep_rename_columns.py` maps them to GSMs.
  - Genotype membership is based on evidence. Cdo1 (ENSMUSG00000033022) FPKM is 822–1072 in A, B, C and 243–272 in A1, B1, C1, and the samples cluster the same way on log2 correlation.
  - The replicate order within each genotype (A→1, B→2, C→3) is assumed. Nothing in this run depends on it.
- **Matrix:** the file holds FPKM (non-integer values, unequal column sums, and data_processing describes a ... [1240 more characters]
