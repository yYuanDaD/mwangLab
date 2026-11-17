# HANDBACK: PMID 34705514 / GSE152919

**Status: refused at `design`.** The data cannot answer "how exercise affects gene expression."

## What ran
- `python -m tools.case_runner inspect GSE152919` downloaded the series into `E:/agent/mwangLab_pdf/data/GSE152919`. It found one matrix, `GSE152919_CT4_CT16_SCN_counts.txt.gz`: 24,419 genes x 15 samples, all values integer, with featureCounts annotation columns.
- Wrote `case_spec.json` covering the gates `paper_reconstruction`, `ownership`, `alignment`, `matrix` and `design`. The `design` gate is `refused`.
- `python -m tools.case_runner execute case_spec.json` finished with status completed. The validator wrote 5 records with 0 errors, and the case route is `stopped:design`.
- Alignment matched exactly on `title` for 15/15 samples. Levels: geno WT 8 / KO 7; time CT16 9 / CT4 6.

## Why refused
- GSE152919 has two factors:
  - genotype: SCN-specific REV-ERBalpha/beta double knockout vs floxed control
  - circadian time: CT4 vs CT16, after 3 weeks in constant darkness
- There is no exercised vs sedentary arm. In this paper, wheel running only measures locomotor rhythm and free-running period, and every mouse had it (FIG1 C, FIG2 F, methods). It is not an intervention.
- The paper never presents any transcriptomic comparison as an effect of exercise (S2.3.p1-p2). Running the genotype or time contrast and calling it an exercise result would create an estimand the paper does not have.

## DEG counts vs paper
None were computed, because the case was refused. For reference, the paper's own comparisons and counts:

| Comparison | Paper DEGs | Notes |
|---|---|---|
| CT4 vs CT16, control | 807 | |
| CT4 vs CT16, DKO | 406 | |
| DKO vs control at CT4 | 286 | n = 3 vs 3 |
| DKO vs control at ZT4 | 56 | n = 2 vs 2; these samples are not in this series |

Paper threshold: DESeq2, FDR < 0.05, FC > 1.5 (|log2FC| > 0.5849625), TPM > 0.1. Sources: the FIG4 legend and S4.14.p1.

## Deviations
None. No analysis was run.

## Tool problems
- No tool failed.
- The count matrix contains Excel-mangled gene IDs, such as 4-Mar and 2-Sep. `inspect` correctly reports them under `excel_date_ids`. They would need repair before any gene-level reporting.
- The paper markdown (`PMC8550249.paper.md`) has no data-availability or GEO accession statement. Ownership therefore rests on matching the sample design (tissue, genotype, CT4/CT16, n = 3 vs 3 at CT4, STAR + featureCounts + DESeq2), and confidence is medium.
- With `planned: []` on a refused design, the suitability report still ran and returned `analyzable` (5 comparisons). That is expected, because suitability tests the genotype and time factors and has no notion of the exercise question. Don't read that verdict as support for an exercise contrast.
