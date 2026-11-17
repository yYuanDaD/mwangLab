# 复核结果：GSE230102_BAT

**总体结论：fix**

## 不一致项

- **confounding（major，disagree）**：论文 S4.2.2.p1 写明久坐小鼠每笼 1-4 只，运动小鼠单笼饲养，饲养方式与 TRN/SED 完全重叠，且分析记录和 HANDBACK 均未提及。修改建议：在 covariance/study 部分加入该混杂说明，结果应表述为"运动加饲养方式"效应。
- **paper_match（minor，disagree）**：论文没有给出各组织 DEG 数，只有"平均约 500"（S2.9.p3）。HANDBACK 称"liver 和 heart 在两种模型中 DEG 最少"，但未分块时 gWAT=15 少于 liver=60。未分块的五组织平均约 498，与论文的约 500 相符，而分块模型平均约 1734，此点未记录。

## 需要人工判断

- 论文未说明模型是否包含 strain，主分析应选分块还是未分块模型（见上，计数差异很大）。
- 能否取得论文图 S11A/S12A/S13A 中的各组织 DEG 数。
