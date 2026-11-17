# GSE123879 审查结果

**总体结论：pass**（无 blocking / major 项）

摘要：运动组(EX)与久坐对照(SED)的比较方向、分组(每组 n=5)、阈值(padj<0.05)均与论文一致，小鼠相互独立无需配对。FPKM 上用 limma 属已声明的偏离，900 与论文 1562 的差异已如实记录。

无 disagree 项。需说明的 unsure/注意点：

- 机械标记 `possible_reversed_contrast`（MTG vs SED）为误报：MTG 是 Pgc1a 转基因组，SED 是对照，Ppargc1a log2FC 为 +2.75。
- model_fit（minor）：论文为直接两两比较，分析采用联合三组 limma 模型，已记为偏离。

待人工决定的开放政策问题：
1. 论文未说明联合模型时，联合与两两拟合如何选择。
2. 论文数字（1562）与另一规则（padj<0.1 得 1456）更接近时，报告哪条阈值。
