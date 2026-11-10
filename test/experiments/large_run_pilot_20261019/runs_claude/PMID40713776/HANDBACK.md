# HANDBACK: PMID40713776 / GSE283853

## Outcome: refused at the `design` gate

GSE283853 is the paper's in-vitro experiment. Human iPSC-derived (414C2) myotubes were given adenoviral pAV-mCherry (control), pAV-MAFA, pAV-MAFB or pAV-MAF, with n=3 per group and 12 samples in total (S2.10.p1, FIG4, DA.p1). The series has no exercise, training or physical-activity factor, so the requested exercise estimand cannot be identified from it. The paper's only training-related analysis compares endurance-trained with power-trained resting biopsies. That analysis is cross-sectional and uses GSE200398 (Russian cohort) and dbGaP phs001048 (Finnish cohort), not this series (S2.18.p1, S3.4.p3).

## What ran

- `tools.case_runner inspect GSE283853`: the data were already cached in E:/agent/mwangLab_pdf/data.
- `prep/extract_counts.py`: the deposited CLC export (`GSE283853_ProcessedData_quantile_totalcount_normalized_ANOVA.csv`) has 48 columns. Each of the 12 samples has three: Expression values, Normalized expression values and Transformed values. There are also 12 group-mean columns. The script keeps the 12 integer "<lib> - Expression values" columns, which are the total read counts, and renames them to the library names m1..c3. Output: `prep/GSE283853_expression_values.csv`.
- `tools.case_runner execute case_spec.json`: 5 records were written (paper_reconstruction, ownership, alignment, matrix, design). Alignment matched all 12 of 12 samples exactly, using `lib` taken from `description` ("Library name: m1"). The matrix type is raw counts (CLC total counts). The design was refused, and the validator reported 0 errors.

## DEG counts vs the paper

None were computed (refused). For reference, the paper reports these counts for the non-exercise contrasts (FIG4.A), using an edgeR exact test in CLC with FDR < 0.05 and no fold-change cutoff (S2.10.p1):

| Contrast | Paper DEGs |
|---|---|
| MAFA vs mCherry | 3,685 |
| MAFB vs mCherry | 2,289 |
| MAF vs mCherry | 4,446 |

The suitability report rates all 6 MAF/mCherry comparisons as analyzable. They fall outside the exercise request, so they were not run.

## Deviations

- The matrix was repaired with a prep script, which selects the count columns and renames them. The script is listed in `prep_scripts`.

## Tool problems

- Minor: `inspect` profiles every column of a CLC Workbench export as a sample (`tools/case_runner.py:361`). It reports 48 "samples", an integer fraction of 0.78 and a "linear_normalized or estimated_counts" candidate, even though there are 12 clean integer count columns. `alignment_keys` comes back empty (`tools/case_runner.py:367`) because the column names have the form "<lib> - Expression values". It would help if inspect detected the CLC " - Expression values / Normalized / Transformed / Means" column layout. Nothing blocked the run.
