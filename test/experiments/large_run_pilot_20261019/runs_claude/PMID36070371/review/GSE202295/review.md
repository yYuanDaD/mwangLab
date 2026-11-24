# GSE202295 复核结果

**总体结论：pass**（无 blocking / major 项）

没有 `disagree` 或 `unsure` 项。以下为次要说明和待人工确认项：

- model_fit（minor）：论文只说 edgeR "with pairing per individual"，没有说明联合拟合还是分组拟合。分析按诊断分层、按时间点两两拟合，并声明了与论文的偏差（DESeq2 代替 edgeR）。T2D 恢复期特有基因数为 2349，论文为 3185。可选：补一个联合配对模型作为敏感性分析。
- paper_match（minor）：对比的是同一对比、同一阈值（FDR<0.01），结论为定性一致，表述可接受。

人工确认项：
- 联合拟合与分对拟合的开放策略问题。
- 论文的 edgeR 配对路线被仓库执行器（不支持区组项）阻塞，DESeq2 为已声明偏差。
