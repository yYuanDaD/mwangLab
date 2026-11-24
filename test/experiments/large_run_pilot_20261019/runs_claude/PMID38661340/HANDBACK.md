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
- **Suitability report data type:** the "Required data" row in `GSE242445/suitability/suitability.md` describes the matrix as "FPKM/RPKM/TPM", but I declared it as normalized counts. The suitability input type is cosmetic here.
- No tool failures.
