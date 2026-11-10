# HANDBACK: PMID42268956 / GSE315575

**Status: refused at `design`.** GSE315575 has no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE315575`: this downloaded the series into `E:/agent/mwangLab_pdf/data/GSE315575`. It holds one counts matrix, `GSE315575_Nox4_RNAseq_counts.csv.gz` (32390 features x 8 samples, all integers, gene symbols, 412 duplicated IDs), and 8 GSMs. The only grouping column is genotype: 4 Nox4 fl/fl and 4 MckCre:Nox4 fl/fl.
- I read the paper sections S2.3.p4, FIG4, S4.12.p1 and S4.4.3.p1, plus the passages that mention wheel running and the treadmill.
- `python -m tools.case_runner execute case_spec.json` recorded these gates in order: paper_reconstruction, ownership, alignment (exact on a key taken from `title`, 8/8), matrix (raw counts, STAR feature counts) and design. Design was `refused`. The validator reported 0 errors across 5 records, and suitability was `analyzable`, with only the genotype comparison listed.

## Why refused
- All 8 sequenced samples are gastrocnemius from 20–21-month-old, chow-fed, sedentary-housed male mice. They differ only by genotype.
- The paper's RNA-seq estimand is NOX4 deficiency (KO vs fl/fl), not exercise.
- The exercise-training experiment (5 weeks of treadmill training in 12-month-old mice, S4.4.3.p1 and Fig. 6) was measured by qPCR and immunoblot only. It was not sequenced.
- The voluntary wheel running cited for these mice (fig. S14C) was measured in metabolic cages. It was not an intervention, and it is not in the GEO metadata.
- Reporting the genotype DEG list as an exercise result would misstate the estimand.

## DEG counts vs paper
- **Paper:** 1023 DEGs for KO vs control (443 up, 580 down). Rule: |logFC| > 0.5 and FDR < 0.05, pydeseq2 v0.4.2 (S4.12.p1).
- **Ours:** none. Nothing was executed because the case stopped at design.
- The genotype contrast itself could be analyzed (4 vs 4, raw counts, DESeq2). If someone wants it as a non-exercise analysis, it needs a separate request. The 412 duplicated gene symbols would have to be handled first.

## Deviations
- None were executed. The paper says the mice were 20 months old in S2.3.p4 and 21 months in the FIG4 legend and GEO. This is recorded as a discrepancy and does not block the analysis.

## Tool problems
- None observed.
