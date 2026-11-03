# 评审：interaction_lrt（GSE283493 / PMC11810837）

**总体结论：fix**（pass / fix / human 中的 fix）。存在 2 个 major 项，没有 blocking 项。

## 不同意的项目

### pairing（major）：不同意
- 论文说明 SAT 与 VAT 取自同一只大鼠（S2.5.p1、S2.9.p1，两种组织每组均 n=6），因此 44 个文库是每只大鼠 2 个。
- 分析记录只检验了单独的重复字母 a-f（n_subjects 6, n_complete 0）。字母在 4 个组里重复，单独用当然无法配对。
- 用“组别+字母”（如 EAC|a，或去掉组织的 title）时：24 个键、48/48 文库被连接、每个组织各一次、无重复；表达相关性检查支持（同键 r=0.345，其它 -0.01，置换 p=0.0005）。
- 论文自己的 LRT 公式没有动物项。
- 修改建议：
  1. 把 covariance 记录改为：animal = grp + rep_letter（24 只），作为有依据的假设并明确标注。
  2. 主要复现：按论文原模型（无动物项）做 DESeq2 LRT，记录为“文库按独立处理，同论文”。
  3. 敏感性分析：动物嵌套在 Phase×Training 内，DESeq2 里加动物固定效应会与 Phase、Training 和交互项完全共线，不可行。应使用 limma-voom 加 duplicateCorrelation(block = animal)，对同一公式检验交互系数；或者按组织分别拟合（每只大鼠每个组织只有一个文库，无需配对）。与 632 并列报告。

### stop_reason（major）：不同意
- “GEO 没有动物 ID”是一个“缺失”类断言，检查范围过窄（只看字母）。
- 更正后的停止理由：动物键（组别+字母）合理且证据充分，但作者未文档化；剩下的真正阻碍是缺少 LRT/SVA 执行器（此项在本快照中可能属实，本次未核实）。
- 确认途径：补充材料 4D 或联系作者。

## 其余项目
run_or_refuse、grouping、direction、model_fit、confounding、matrix_method、threshold、paper_match 均同意。confounding 有一条 minor 备注：笼号（每笼 3 只，未存入 GEO）与采样时间/Phase 混合未被记录。

## 待人工决定
1. 论文自己的模型忽略了重复测量单位时，哪一个结果作为主结果：论文原样的非配对拟合，还是按动物区块化的拟合？评审倾向于原样拟合为主、区块化拟合并列。
2. 4 个离群文库（SAT_PM_Exp_d、SAT_PM_Exp_f、VAT_AM_Cont_e、VAT_AM_Exp_c）是按论文所述标准推断而非读自补充材料 4D；如能获得 4D，请核对。
