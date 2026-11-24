# GSE99963 复核结果

**总体结论：pass**（无 blocking / major 项）

没有 `disagree` 项。以下为 `unsure` / 需关注的事项：

- **paper_match（minor）**：Ex-HFD 4256 vs 论文 2617，Sed-HFD 1487 vs 412，均为 FDR<0.1 同一规则，比较的对比也相同。但计数偏高 1.6 倍和 3.6 倍，Ex/Sed 比例也不同（2.9 vs 6.4）。点名基因的 logFC 与论文 Table 2 吻合。建议 HANDBACK 明确写出“DEG 数量未复现，原因未明（基因过滤近似、robust 设置、注释版本）”。
- **grouping（minor）**：为匹配论文 Sed n=6，排除了 S3（Pre_S3 仅 102,811 reads）。理由已写明并记录为假设，但论文未点名被剔除者。
- **matrix_method（minor）**：基因过滤用 CPM≥0.15（≥5 个样本）近似论文 RPKM>0.1，因为没有基因长度，已声明为偏差。

待人工处理：是否追加更严格过滤或 robust=FALSE 的敏感性分析。
