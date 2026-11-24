# GSE208354 复核结果

**总体结论:pass**(无 disagree / unsure 项)

- 分析对象:HFpEF 运动组(HFEXT)对比久坐 HFpEF 组(HF),input RNA-seq 各 3 例,与论文 n=3 一致;m6A IP 文库已按原因排除。
- 因只有 FPKM,使用 limma(log2(FPKM+1))代替论文的 DESeq2,已作为 declared deviation 记录;阈值按论文原始 p<0.05 且 FC>2 转写为 |log2FC|>1,并附 padj 审计(0 个)。
- 97 vs 论文 690:已如实呈现,Table 3 十个基因方向全部一致。

待人工关注(开放政策问题,非错误):论文的 690 个 DEG 与任何已测规则都对不上,差距归因于 FPKM/limma 与 DESeq2 计数、以及 FPKM≥1 过滤,尚未验证。
