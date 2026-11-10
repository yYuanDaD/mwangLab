# HANDBACK: GSE178367 / PMC8348158 (SCA3 transgenic mice, IGF-1)

**Status: refused at `design`. The study has no exercise contrast.**

## What ran
- `python -m tools.case_runner inspect GSE178367` (data cached in `E:/agent/mwangLab_pdf/data/GSE178367`): one matrix, `GSE178367_15Q_84Q_IGF1.txt.gz`, 37,816 Ensembl genes x 9 samples, all integer values (featureCounts raw counts).
- `python -m tools.case_runner execute case_spec.json`: gates `paper_reconstruction`, `ownership`, `alignment`, `matrix` valid; `design` refused. Validator: 5 records, 0 errors. No executors or enrichment ran.
- Alignment: exact on a key taken from the bracketed lab id in the GEO title, after `matrix_column_pattern ^counts\.(.+)$`. 9/9 matched. Groups: Q15=3, Q84=3, Q84IGF=3.

## Why refused
Paper (S4.1.p1) and GEO metadata have only two factors: ATXN3 genotype (15Q control vs 84Q SCA3) and weekly i.p. IGF-1 (50 mg/kg) vs PBS in 84Q mice, months 9 to 18. No animal was exercised or trained. "Exercise behavior" (ABS.p1) and the rotarod tests (S1.p3) are behavioral outcomes from an earlier GH study, not an intervention. Calling the genotype or IGF-1 contrast an "exercise" effect would change the estimand. The suitability report rated the 3 genotype/treatment comparisons analyzable, but none of them answers the request.

## DEG counts vs paper
None computed, because the case was refused. For reference, the paper reports:
- 84Q vs 15Q: 521 (62 up / 459 down)
- 84Q+IGF-1 vs 15Q: 588 (45 up / 543 down)
- 84Q+IGF-1 vs 84Q: 6 (1 up / 5 down)

The paper's threshold is DESeq2 Wald with BH, padj < 0.1 and |log2FC| >= log2(1.5) = 0.5849625 (S4.7.p1). The Results (S2.2.p1) say the counts used "adjusted p-value < 0.05", which conflicts with the Methods; this is recorded as a discrepancy.

## Deviations
None. Nothing was executed.

## Tool problems
None blocking. Minor: `inspect` returned `alignment_keys: []` for this series. The matrix names (`counts.18_1_4`) carry a `counts.` prefix and the key sits in brackets inside `title`, so the contained-name detector (`tools/case_runner.py:314` `_contained_keys`) suggested nothing. I had to work out `key_patterns` + `matrix_column_pattern` by hand. A hint that strips a common column prefix would have found it.
