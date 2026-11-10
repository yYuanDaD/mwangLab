# GSE222163 审查结果

**总体结论: pass**(无 blocking / major 项)

没有 `disagree` 或 `unsure` 项。

说明:
- pairing_key_candidate 标记的是 BAT 与 SkM 之间(同一小鼠两种组织)的可能配对。分析在每个组织内单独拟合(n 为 6-8),模型内没有同一动物重复,表达相关性检查也为 not_supported,因此不需要分块。
- paper_match(minor): SkM CREX vs CR 本分析 29 个 DEG,论文 15 个(各 3 个样本),HANDBACK 已如实说明不稳定;仅用 padj<0.05 也是 29,没有其他规则能复现 15。其余三项为 39/37、50/48、30/30,方向一致。
- 阈值 padj < 0.05 且 |log2FC| > log2(1.5) 与 S2.7.p1 一致,图注中的 raw p 写法已记录为差异。
