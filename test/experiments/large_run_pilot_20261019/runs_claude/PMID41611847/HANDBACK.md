# HANDBACK: PMID41611847 / GSE256241

**Status: refused at the `design` gate.** The data contain no exercise contrast.

## What ran
1. `python -m tools.case_runner inspect GSE256241` downloaded the series to `data/GSE256241`. It found one matrix, `GSE256241_raw_count.txt.gz` (55,716 Ensembl genes x 12 samples, plus annotation columns `gene_name`, `description` and `length` and empty `Unnamed:*` columns). Its columns match the GEO `title` field for 12 of 12 samples.
2. I read the paper (PMC13022187.paper.md), mainly S2.7, S2.8, FIG5, S4.6–S4.13 and S9.
3. I wrote `case_spec.json` and ran `python -m tools.case_runner execute`. It recorded these gates:
   - paper_reconstruction: valid
   - ownership: valid
   - alignment: valid (exact match on `title`, 12/12 samples)
   - matrix: valid (estimated counts)
   - design: **refused**

   The contract validator ran on 5 records and found 0 errors. The case route is `stopped`.

## Why it was refused
- The paper is a drug-repositioning study. Its only transcriptome experiment compares gastrocnemius from aged male mice fed rosiglitazone (n=6) with mice fed the control diet (n=6) (S4.6.p1, S2.8.p1).
- GEO has one grouping factor, `characteristics_ch1.1.treatment`, with rosiglitazone/control at 6/6.
- In this paper, exercise is only an outcome measure. The treadmill exhaustion, rotarod and grip-strength tests (S4.7–S4.9) were given to both groups.
- No group was trained or sedentary, so the effect of exercise on gene expression cannot be estimated.
- I did not run the rosiglitazone-vs-control contrast as a substitute. It is recorded as a rejected candidate.

## DEG counts vs paper
- **Paper:** rosiglitazone vs control gave 383 up and 100 down (483 DEGs).
  - Threshold: BH-adjusted P < 0.05 and |log2FC| >= 1 (FIG5 C caption; S4.13.p1 item 3).
  - Method: DESeq2 1.34.0, keeping genes with more than 1 count in every sample and a total above 12.
- **Ours:** none. No exercise contrast exists, so nothing was run (0 contrasts).

## Deviations
None. The case was stopped before any model was fitted.

Notes for anyone who later reproduces the drug contrast:
- The matrix holds StringTie estimated counts (about 21% of expressed entries are fractional), so DESeq2 would need documented rounding.
- WGCNA used 5 rosiglitazone + 6 control samples (FIG5 D). That is not relevant here.

## Tool problems
None blocking.
- Minor: the `inspect` matrix `candidates` for this file was "linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts". It did not separate the two even though 89% of values are integers and GEO says "raw counts". I resolved this by hand.
- Minor: the deposited file ends in six empty `Unnamed: 16..21` columns. `inspect` reported them as annotation columns, and they did no harm.
