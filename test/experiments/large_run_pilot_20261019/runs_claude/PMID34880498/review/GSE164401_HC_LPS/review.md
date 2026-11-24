# 复核：GSE164401_HC_LPS

**总体结论：pass**

决定与论文一致：分组(8/8/7/8)、方向、阈值(Wald原始P<0.05)和原始计数矩阵均正确，LPS对照4709对4936基本吻合。L编号嵌套于组内，可能是笼，但论文同样按独立小鼠处理，仅列为次要提示。总体通过，开放的策略问题交人工。

## 需关注项
- `pairing` (unsure, minor): L1-L16 nested in group (L3,7,11,15=LPS+CP etc.); paper n=8 mice/group matches 4 L x 2, so _1/_2 are counted as separate mice; analysis tested expression neighbours and treated as independent. If L is a cage of two mice, cluster effect is ignored, but paper does the same. 建议：Optional sensitivity: cluster-robust or L-aware check, labelled assumption; not required.
- `model_fit` (unsure, minor): Paper does not state joint vs pairwise fits; S6.9.p1 only says 'DESeq2 ... using built-in algorithms'. Analysis used one joint ~grp model on all 31 samples (one dispersion fit) and recorded this as a deviation/assumption. 建议：Optionally report pairwise fits for LPSRP vs LPSCP as sensitivity.

## 待人工决定
- Open policy: plasma-transfer exercise-mediator series counted as exercise study.
- Open policy: joint vs pairwise fit when paper is silent; padj<0.05 gives only 3 DEGs for LPS+RP vs LPS+CP versus 1395 at raw P.
