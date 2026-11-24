# 评审 GSE211204:OVERALL pass

所有检查均一致,无 blocking/major 项。

- 运动对比 AR vs ULLS,方向正确;模型 `~ subject + time` 与论文的 subject 配对分析一致;样本数 11/11/9 与论文一致;阈值 q<0.05 无 FC 阈值。
- 已声明的偏差:TMM 代替 voom quantile 归一化;论文只在 290 个 NMJ 基因内报告 DEG,本分析为全转录组,计数不可直接比较。
- 次要(paper_match):study 记录的 `paper_counts` 为空,可补 95/114/24(q<0.01:70/81/7)。
