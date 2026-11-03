# 复核结果：GSE236613（PMC10470051）

**总体结论：fix**

## 不一致项

- **threshold（major）**：论文 S2.8.p1 写的是“p-value < 0.05 且 foldchange >1.2 或 <0.83”（原始 p，非 FDR）。记录写成 padj < 0.05、无倍数变化阈值，也没有登记差异。按论文规则在已有结果表上只读统计：联合模型 RE vs NE 749、Sham vs NE 2727；两两拟合 RE vs NE 874、NE vs Sham 2522；都远低于论文的 4423 / 6697。
  - 修改：paper_threshold 改为 pvalue < 0.05 且 |FC| 按 1.2/0.83（log2 约 +0.263/-0.269）；padj<0.05 作为更严格的次要规则；新增差异条目说明论文计数两种规则、联合或两两拟合都无法复现。
- **paper_match（major）**：study 与 method 中“主要运动对比按论文方法和阈值复现”的说法过强（我们 5 个 vs 论文 4423；规则也不是论文规则）。Stat1 在论文中 RE vs NE 上调，我们的 log2FC 为 -0.566。
  - 修改：用论文规则重做对比表；表述改为“方法复现，DEG 数量未复现”，并注明 Stat1 方向冲突。
- **direction（minor）**：论文报告 NE/Ovx vs Sham，设计里是 Sham vs NE（符号相反）。已在备注中说明，且两两敏感性分析为论文方向。修改：次要对比改为 control=Sham, treatment=NE。

## 其他检查
run_or_refuse、grouping、pairing（无重复测量；flags 里的 subject-like 列是分组列本身，属误报）、model_fit（联合和两两都已报告）、confounding、matrix_method 均同意；stop_reason 不适用。

## 待人工决定
论文原始 p + FC 1.2 规则仍无法得到论文的 4423 / 6697，应以何种阈值作为主报告需要人工决定。
