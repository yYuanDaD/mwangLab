# 复核结论：GSE122628（PMID31433691）

**总体：pass**（无 blocking / major 项）

没有 `disagree` 或 `unsure` 项。

- 分组：电刺激(S) 3 vs 假刺激(U) 3，与摘要、GEO 描述一致；对照为假刺激，方向为 STIM vs SHAM。
- 配对：每只小鼠一个样本，无重复测量。
- 方法：edgeR 准似然（GEO 所述）+ DESeq2 敏感性分析；估计计数取整已声明。
- 阈值：论文仅有摘要，未能获得阈值和 DEG 数，已按默认规则报告并注明，未声称与论文一致。
- 次要（minor）：未做低表达过滤（edgeR 检验 48759 基因，DESeq2 为 20359）；可选做 filterByExpr 敏感性分析。

待人工：若能取得全文，核对论文阈值与 DEG 数。
