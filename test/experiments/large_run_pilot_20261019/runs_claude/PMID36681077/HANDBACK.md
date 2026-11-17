# HANDBACK: PMID 36681077 / GSE216094

**Outcome: refused at the `design` gate.** No exercise contrast exists in GSE216094.

## What ran
- `python -m tools.case_runner inspect GSE216094` downloaded the series into `data/GSE216094`. It holds 8 GSMs, `GSE216094_STAR_Gene_TPM.csv.gz` (23,637 genes x 8 samples) and `GSE216094_PSAPvGFP.deseq_star.csv.gz` (the authors' DESeq2 result table).
- Paper read: `PMC9998376.paper.md` (S2.2, S5.1.3.p1, S5.3.1, S5.3.11, S5.3.20.2, FIG5, TAB1).
- `python -m tools.case_runner execute case_spec.json` recorded `paper_reconstruction`, `ownership`, `alignment` (exact on a key built from the title, 8/8), `matrix` (TPM) and `design` (refused). The validator found 5 records and 0 errors, and the route is `stopped:design`.

## Why refused
- GSE216094 is "RNAseq of pAd transduced iWAT cells" (S5.1.3.p1, TAB1). The samples are primary inguinal white adipocytes transduced in vitro with a GFP or a PSAP adenovirus, n=4 per arm (Fig 5G-H).
- The paper's exercise experiment (acute treadmill run vs sedentary, gastrocnemius extracellular fluid) is TMT proteomics. It is in PRIDE PXD031982/PXD037731 (S2.2, S5.3.11), not in this GEO series.
- The only contrast these data support is PSAP vs GFP. It does not answer the exercise question and was not relabelled as one.

## DEG counts vs paper
- None computed, because the case was refused.
- The paper reports no DEG count for this RNA-seq. It reports only GSEA Hallmark results, with OXPHOS at q < 0.001 (Fig 5H), from DESeq2 on STAR counts (S5.3.20.2.p1).
- The paper's exercise threshold is the proteomics rule q < 0.05 (permutation FDR, Perseus t-test; S5.3.11.p1), with 1322 proteins changed. It does not apply to this accession.

## Deviations
- None executed.
- Recorded discrepancy: the paper ran DESeq2 on STAR counts, but GEO holds only TPM and the authors' DESeq2 result table. This was not evaluated further because of the refusal.

## Tool problems
- `tools.case_runner inspect`: the authors' result table `GSE216094_PSAPvGFP.deseq_star.csv.gz` is listed under `matrices`. Its "sample_columns" are `baseMean, log2FoldChange, lfcSE, stat, pvalue, padj`, and `candidates` is empty. It is not flagged as a DE-result table rather than a sample matrix. This is minor and did not affect the decision.
- Harness, not repository: backslashes in Bash heredocs were mangled when the spec was written (`\\d` arrived as `\d`, which is invalid JSON). The fix was to use `[0-9]` in the regexes.
