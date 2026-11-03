# 复核结论 GSE302867

**总体判定：human（需人工判断）**

九项检查中无 disagree，一项 unsure，一项 na（stop_reason）。

## unsure
### paper_match（major）
- 论文无 DEG 数量，无法比较（已如实说明）。
- 通路层面：KO_Ex vs KO_Sed 的 OXPHOS NES -3.54，方向与论文（-10.22）一致；但 WT_Ex vs WT_Sed 的 OXPHOS NES -2.64，与论文 Fig 2e 的 +5.14 方向相反。
- HANDBACK 已披露并称原因未解决（FPKM+limma 与 DESeq2 计数、preranked 与表型置换 GSEA、或样本本身差异）；Ppargc1a 在 KO 中反而 +0.86 也值得注意。study 记录的 caveats 没有列出这一点。
- 建议：把该方向不一致写入 study 记录的 caveats；可选做敏感性分析（WT 两组单独拟合，或基于 logFC 的排序 GSEA）。

## 人工事项
1. 上述 WT 运动 OXPHOS 方向不一致是否可作为已声明的偏离接受。
2. 开放策略：论文未说明时联合模型与逐对拟合的取舍。
3. 开放策略：阈值取论文规则（偏离路线上）并附无倍数变化阈值的审计结果。
