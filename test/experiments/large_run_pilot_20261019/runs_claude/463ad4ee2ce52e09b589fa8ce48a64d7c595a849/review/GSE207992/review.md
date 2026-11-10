# GSE207992 审阅结果

总体结论：**pass**（无 blocking / major 项）

## 需要注意的项目

- **model_fit（unsure，minor）**：论文 S4.4.2.p1 未说明是一个四组联合模型还是逐对拟合，仅列出每个 pairwise 分析通过过滤的基因数，暗示可能逐对。联合模型（KO 运动 329、WT 772、KO 基因型 457、KO SVE vs WT nSVE 557）与逐对拟合（33、2047、326、594）均已报告，均不能同时复现论文的 223/795/307/557。
- **pairing（agree）**：机械标记 pairing_key_candidate 为误报。SVE 与 nSVE 为不同队列，每只动物一个样本（S4.4.p4）；表达相关检验不支持（same-key r=0.044，p=0.136）。

## 待人工判断

- 论文未说明时联合 vs 逐对拟合的开放策略问题。
- KO SVE vs KO nSVE 的通路方向（我们的结果中 OXPHOS/帕金森病下调）与 S2.5.p1 相反但与 S1.p4 一致，分析方已在 caveats 中披露。
