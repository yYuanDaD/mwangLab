# GSE128078 复核结果

**总体结论：pass**（无 blocking 或 major 问题）

## 需要说明的项目

- 机器标记 `unused_subject_like_column`（individual identifier）：误报。该列已别名为 `subject`，并作为固定区块项进入各组内的 day 对比模型（~0 + C(day) + C(subject)，秩 28，残差自由度 69）；变化量比较使用了配对文件 paired_change_pairs.json。
- threshold（minor，开放政策问题）：论文写 FDR < 0.1%，而表4中的 FDR 最高为 0.10。分析按 padj < 0.1 且 |log2FC| > log2(1.5) 运行，并以 padj < 0.001 作为审计规则，已记录为差异。原始 p < 0.05 未编码，但在此不起约束作用。
- stop_reason（minor）：低 VO2 / test-retest 子集因 GEO 无受试者标签而无法运行，成立。"全部时间点 ME/CFS vs 对照" 未运行的原因是运行器无法拟合受试者随机效应，这是工具限制而非数据缺失，可作为 duplicateCorrelation 敏感性分析补充。
- matrix_method（minor）：GEO 仅有 hg19 Cufflinks isoform FPKM，经基因符号求和后用 limma(log2(FPKM+1))，与论文 hg38 Partek 流程不同，已记录。

## 人工事项

- FDR 写法与表4不一致时应报告哪个阈值（开放政策问题）。
- 可选：补充全部时间点的敏感性分析。
