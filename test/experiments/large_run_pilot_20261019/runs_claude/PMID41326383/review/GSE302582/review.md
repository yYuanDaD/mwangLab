# GSE302582 复核

**总体结论：pass**（无 blocking / major 项）。

## 需要关注的项目（均为 minor，verdict 仍为 agree）

- **model_fit**：论文未说明模型（S4.9.1.p1）。分析按组分别拟合 DESeq2（~subject+cell），并以 limma 变化量作为敏感性分析；组内 DEG 数为论文的 1.3-1.8 倍，未做联合模型。建议可选地补充联合拟合。
- **threshold**：padj<0.05（无 FC）与 S4.10.p1 原文一致。packet B 显示 padj<0.1 在 +3h 得 208（论文 207），+24h 用 p<0.05 且 |lfc|>1 得 17（论文 16）；研究记录只写了数量差异，未写这些替代规则吻合。建议补一句差异记录，不改变所用规则。

## 待人工决定（开放政策问题）
- 论文数字吻合另一规则时报告哪个阈值。
- 论文未说明时联合与成对拟合的选择。

其余检查（run_or_refuse、grouping、direction、pairing、confounding、matrix_method、paper_match）均 agree，stop_reason 不适用。
