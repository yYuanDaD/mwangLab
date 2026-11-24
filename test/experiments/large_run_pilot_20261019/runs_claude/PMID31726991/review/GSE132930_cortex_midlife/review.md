# 复核:GSE132930_cortex_midlife

**总体结论:fix**

分组、方向、阈值均与论文一致,样本按标题精确对齐。但 ours=0 vs 论文 214/67,HANDBACK 把差距归因于检验类型,这只是未验证的假设;需改写或补做 exactTest/LRT 敏感性分析。

## 需关注项
- **paper_match**(不同意,major):HANDBACK says the count gap 'comes from the statistical test alone' and that LRT/exactTest explains the near-zero midlife counts (ours 0/0 vs paper 214/67). Not demonstrated: no exactTest/LRT fit was run; midlife p-value Spearman vs deposited tables is only 0.83-0.88 (young 0.99) while log2FC r=0.999, and DESeq2 ~pool+grp changes counts. padj<0.1 gives 879/593, so signal exists but QL is far more conservative than the paper's rule.
  - 修正建议:Reword HANDBACK and the study record: the gap is unexplained and the test-type difference is a hypothesis. Add an R exactTest (and glmLRT) execution on the same two-group subsets as a labelled sensitivity, or record it as an open discrepancy.

## 待人工决定
- Which test to report when the paper states QL F-test but the deposited tables look like exactTest/LRT (open policy question).
