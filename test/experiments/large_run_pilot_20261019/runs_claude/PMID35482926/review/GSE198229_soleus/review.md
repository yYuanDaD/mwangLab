# 复核：GSE198229_soleus

**总体结论：pass**（无 blocking / major 项）

## unsure 项
- **direction（minor）**：设计为 SED 为对照、EX 为处理，stat 与 log2FC 符号一致，没有发现反号的证据。但论文称 ND5 比目鱼肌 OxPhos 基因上调（S1.2.2.p1），而本结果 ND5 在 P<0.05 下 3147 下调 / 153 上调，54 个 OXPHOS 家族基因的平均 log2FC 约 +0.02，Hallmark OXPHOS 不显著。这是定性差异，不能证明方向反了。建议在 HANDBACK 中注明未复现，或用论文 Fig. S8 的基因列表核对。

## 待人工确认
- B6 对照组未运行：矩阵第 25–36 列只有数字编号，需向作者索取与 N-ID 的映射。
- ND5 OxPhos 上调未复现：对照补充数据集 S1–S11，判断是数据处理差异（无 TMM、取整、基因集不同）还是方向问题。

说明：阈值采用论文所述 nominal P<0.05（无倍数变化限制），padj<0.05 作为审计（0 个 DEG）；各突变株内独立拟合，每组 6 vs 6。
