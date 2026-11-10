# 复核 GSE320360

**总体结论：fix**（paper_match：major）

## 不一致项

### paper_match（major）
- 证据：同一对比、同一规则（padj<=0.05）下，我们 45/72/28，论文 15/33/4（3到7倍）；padj 系统性更小（miR-3618：0.0015 对 0.0055）；miR-137-3p、miR-329-5p 的 log2FC 与论文不同；75 min 方向为 18 上调/10 下调，论文全部上调。
- HANDBACK 称“排除约2%未收敛基因”最可能导致计数偏多，但去掉基因只会让论文的 BH padj 更小，无法解释我们 padj 更小，该解释未被支持。“reproduced_with_deviations”说法偏强。
- 修复：改写 HANDBACK 与方法记录，说明论文差异基因被全部复现但我们的集合大 3-7 倍，原因未确定；增加敏感性分析（R DESeq2 ~ID+Treatment，未过滤矩阵估计 size factor，标准化计数过滤），同时报告两种计数。

其余检查（run_or_refuse、grouping、direction、pairing、model_fit、confounding、matrix_method、threshold）均同意；stop_reason 不适用。
轻微：图3图注提到 log2FC 截断线但未给数值，记录中 effect_cutoff 为 null。
