# 复核：GSE198229_heart

**总体结论：pass**（无 blocking / major 项）

没有 `disagree` 或 `unsure` 项。

待人工确认（human_items）：
- B6 对照组（论文主要比较之一）未运行：矩阵第 37–48 列只有数字编号，无法对应 GEO 的 N-ID。需向作者索取编号映射，或用补充数据集 S1–S11 核对。
- 开放的策略问题：论文对心脏未给出阈值时，应报告 padj（0 个 DEG）还是 nominal P 的审计计数。当前两者都已列出。

说明：各突变株内 EX vs SED（每组 6 vs 6），limma-voom，方向、模型结构、矩阵类型与论文一致；每只小鼠只有一个心脏样本，无需配对。
