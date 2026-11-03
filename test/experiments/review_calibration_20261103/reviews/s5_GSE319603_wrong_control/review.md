# 复核结论：GSE319603（PMC12982024）

**总体：fix**（有 2 项 blocking，需要补跑运动对比）

## 不一致项

### direction — blocking
- 论文的运动对比是 HM vs H（对照为高脂组 H，S3.2.p1：563 个 DEG，213 上调/350 下调）。
- 分析把 HM 与普通饮食组 C 比较（`grp_HM_vs_C`，设计里写成"运动 vs 对照"），饮食与运动效应混在一起，HM vs H 没有执行。
- H vs C 方向正确（295 上调/163 下调，与论文完全一致）。study 的说明里"reference H"一句是过时的，与实际对比矛盾。
- 修正：主对比改为 `grp_HM_vs_H`（control=H, treatment=HM），`grp_H_vs_C` 保留为次要对比；`grp_HM_vs_C` 删除或标为探索性；重新 execute。

### paper_match — blocking
- study.comparison 把 `grp_HM_vs_C`（1182）与论文的 563 配对，而 563 是 HM vs H 的数字，对比不同，1182 对 563 的差异没有意义。只有 H vs C（458 对 458）是有效配对。
- 修正：补跑后用 HM vs H 与 563（213/350）比较，并对 Angptl7、Txnip、Fbxo32、Trim63 等基因重新做 paper_gene_check。

### model_fit — unsure（minor）
- 论文没说明是联合拟合还是两两拟合。联合拟合在 H vs C 上完全复现论文，支持联合模型，但方法记录中承诺的两组敏感性分析没有产出。HM vs H 补跑后，若数目与 563 差异大，再跑 H/HM 两组单独拟合；否则删去"pairwise sensitivity"的说法。

## 其余检查
run_or_refuse、grouping、pairing、confounding、matrix_method、threshold 均 agree；stop_reason 不适用。机械标记 `other_rule_matches_paper` 是错误对比造成的假象（HM vs C 与 HM vs H 的 563 比较），不是阈值问题。

## 待人决定
- 论文 Results 规则为 |log2FC| >= 0.5（含等号），运行器只支持单一 inclusive 标志，目前用 > 0.5，H vs C 已精确复现；仅当 HM vs H 的数目也出现偏差时才需要再看。
