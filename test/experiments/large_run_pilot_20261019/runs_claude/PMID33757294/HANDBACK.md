# HANDBACK — PMID33757294 / GSE161030

**Status: finished (paper_aligned).** The validator ran on 10 records and reported 0 errors.

## What ran
- `inspect` GSE161030 found two files. The first is a raw integer count matrix of StringTie transcripts: `GSE161030_lncRNA_EHP_vs_Sed.csv.gz`, 46,746 transcripts × 6 samples (Sed1–3, EHP1–3). The second is the authors' own DESeq2 table, with 27,884 transcripts.
- Paper (S2.3.p1, FIG4) compares 3 EHP hearts with 3 sedentary hearts. EHP means 21 days of swimming followed by 1 week of detraining. The method is DESeq2, and a transcript counts as differentially expressed at P < 0.05 and |log2FC| > 1 (raw P).
- Case spec: `case_spec.json`.
  - Samples were matched exactly on the metadata `description` column (6/6), and `grp` was derived from it (Sed / EHP).
  - Raw counts were analysed with pydeseq2 using the design `~ grp`.
  - Low-count transcripts were filtered at row sum >= 10, which reproduces the authors' 27,884 features exactly.
  - No enrichment was run. The paper only ran GO on cis-target genes of the lncRNAs, and the IDs here are transcript IDs.

## DEG counts vs paper
| Contrast | Rule | Ours (up/down) | Paper (up/down) |
|---|---|---|---|
| EHP vs Sed | P<0.05 & \|log2FC\|>1 (paper, S2.3.p1) | 2163 (1498/665) | 2162 (1482/680) |
| EHP vs Sed (audit) | padj<0.05 & \|log2FC\|>1 | 1521 | – |

Compared with the authors' deposited DESeq2 table:
- log2FC correlation is r = 0.99999999 across the 27,884 shared transcripts.
- 2,139 of the paper's 2,162 calls are also in our set.
- Applying the paper rule to the deposited table gives exactly 2162 (1482/680), which confirms the threshold is raw P.

## Deviations
- We used pydeseq2, not R DESeq2. This explains the small count differences: the deposited table splits 1482/680, ours 1498/665.
- The pre-filter (row sum >= 10) is not stated in the paper. It was inferred from the size of the deposited table.
- GEO `data_processing` states a different rule: RPKM > 500, |log2FC| > 1 and padj < 0.05. That rule does not reproduce the paper's count, and no RPKM values were deposited. We applied the paper's rule and report padj < 0.05 only as the audit rule.
- The paper calls all 2162 features "lncRNAs", but the table contains every StringTie transcript, not only lncRNAs. We counted them the same way the paper did.
- The paper's key gene, Mhrt779, cannot be looked up because it has no Ensembl transcript ID in this matrix.

## Tool problems
- No blocking problems.
- Minor: `filter_low_counts` has no rule for a total row-sum count. To get row sum >= 10 we had to pass a fractional `min_mean_count: 1.6666` (`tools/case_runner.py:777-778`).
