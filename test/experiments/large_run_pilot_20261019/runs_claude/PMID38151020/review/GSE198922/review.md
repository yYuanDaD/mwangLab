# 评审 GSE198922

**总体结论：pass**（无 blocking / major 项）

## 需要注意的项
- **model_fit（unsure，minor）**：论文用一个合并模型（~0+group+sex，质量权重，duplicateCorrelation 按参与者分块）；本次按诊断分层各拟合一次，参与者作固定效应。偏离已记录，但 DEG 数是论文的 1.35–2 倍（如 T2D REC 8755 vs 4316），且未做合并模型的敏感性分析。可选：若执行器支持，补一个合并模型作敏感性分析。
- **paper_match（agree，minor）**：NGT REC 的“≥1088”是由 4316−3228 推断，不是论文给出的数字，HANDBACK 已标为“implied”。

## 其余检查
run_or_refuse、grouping（缺失 1_POST 已说明）、direction、pairing、confounding、matrix_method、threshold 均一致；stop_reason 不适用。

## 待人工确认
- 论文规则下计数偏高时，是否另报合并模型结果（开放政策问题）。
