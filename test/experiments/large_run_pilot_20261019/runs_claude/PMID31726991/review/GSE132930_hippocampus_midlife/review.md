# 复核:GSE132930_hippocampus_midlife

**总体结论:fix**

设计与论文一致,方向无误;结果 8/3 vs 论文 271/172。HANDBACK 将差距完全归因于检验类型,缺乏直接证据(midlife p 值秩相关仅 0.83-0.88),建议改写为假设并补 exactTest/LRT 敏感性。

## 需关注项
- **paper_match**(不同意,major):HANDBACK says the count gap 'comes from the statistical test alone' and that LRT/exactTest explains the near-zero midlife counts (ours 8/3 vs paper 271/172). Not demonstrated: no exactTest/LRT fit was run; midlife p-value Spearman vs deposited tables is only 0.83-0.88 (young 0.99) while log2FC r=0.999, and DESeq2 ~pool+grp changes counts. The seven ECM genes the paper names all go down but none reaches FDR<0.05 (padj 0.29-0.65).
  - 修正建议:Reword HANDBACK and the study record: the gap is unexplained and the test-type difference is a hypothesis. Add an R exactTest (and glmLRT) execution on the same two-group subsets as a labelled sensitivity, or record it as an open discrepancy.

## 待人工决定
- Which test to report when the paper states QL F-test but the deposit looks like exactTest/LRT (open policy question).
