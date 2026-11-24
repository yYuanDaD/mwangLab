# 复核结论：GSE208615 — 总体：pass

- 无阻断或重大分歧；所有检查项一致或仅为次要意见。

## 需关注项（unsure / 次要）
- **model_fit（unsure，minor）**：论文按每对组分别做 Cyber-T（S4.2.8.p1），本次为六组联合 limma-trend，已记录为 declared deviation。
- **threshold（minor）**：原始 p<0.05、无倍数变化阈值，转录正确；论文中 "both uncorrected p value" 的含义（可能 Cyber-T 与回归）有歧义，未注明。
- **paper_match（minor）**：HANDBACK 如实说明了 273 对 21 的共同上调基因差异，但该差异未列入 discrepancy 记录，可补一行。
- 机械标记 possible_reversed_contrast（RE2 vs SED）为误报：RE2 是 0-0-2 再激活运动组，SED 为对照。

## 人工事项
- 开放政策：论文为两两拟合时，联合模型是否可接受。
- 273 vs 21 基因交集差异原因无法从文件确定。
