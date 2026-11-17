# 审查：GSE286570

**总体结论：fix**

这个案例整体合理：运动对照 HFD 的两个主要对比、分组、n=3、DESeq2 原始计数、联合与成对拟合都符合论文。需要修正两点：HRE vs HFD 的论文数(171)更接近 padj<0.05 加倍数阈值，这一点未作为阈值差异记录；饮食对比以 NC vs HFD 运行，符号与论文的 HFD vs NC 相反，需要在结果中标明或重排。

## 不一致项

### direction（minor）
- 证据：Paper reports HFD vs NC (S2.6.p1, Fig 6B, 'HFD/NC'); run fitted NC vs HFD (treatment=NC, control=HFD), so log2FC signs are the reverse of the paper's. Recorded in discrepancies and HANDBACK gives up/down 'as HFD vs NC', and it is a non-exercise secondary contrast; exercise contrasts HAE/HRE vs HFD are correct.
- 修正：Add contrast HFD vs NC (control NC, treatment HFD) or relabel result columns so DEG tables carry the paper's direction.

### threshold（major）
- 证据：Paper S4.5.p1: 'log2FC < 1 and a p-value < 1E-2'; run reads it as raw p<0.01 and |log2FC|>1 and records the wording typo. But packet B flags the paper's HRE vs HFD count (171) fits padj<0.05 & |lfc|>0.585 (182) or padj<0.05 & |lfc|>1 (181 pairwise) far better than the applied rule (467/461); this is not recorded as a rule discrepancy, only attributed to n=3 instability. HAE vs HFD (1450) fits the applied rule (1488) best, so the evidence is mixed.
- 修正：Add to paper_data_discrepancies: HRE vs HFD paper 171 matches padj<0.05 with FC cutoff (182), not raw p<0.01 & |lfc|>1 (467); keep raw p as the primary rule per the paper's text, and report the closest-rule count next to it.

## 待人工决定
- Which threshold to report for HRE vs HFD when the paper's 171 fits padj<0.05 with FC cutoff rather than the stated raw p<0.01 (open policy question).
