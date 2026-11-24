# 复核 GSE156174（PMID34836964）

**总体结论：pass**

该系列研究后肢卸载（HU，废用）及复负重（HUR），没有运动或训练组；每个分组（细胞类型 × 处理 × 时长）只有一个由 3-4 只小鼠合并的 RNA 文库（S4.7.p1、S2.4.p1），所有比较都是 1 vs 1。原分析的拒绝理由（无运动组、无重复）均成立，与盲审答案一致。

没有 `disagree` 或 `unsure` 项。

备注：
- 机械标记 `refusal_vs_exercise_words` 是误报（匹配到 "unloaded"）。
- 配对候选键 `grp` 只是标签组合（SSC 与 MSC 来自不同批小鼠），表达检验为 not_supported，不是动物 ID。
- 论文未给出 RNA-seq 的 DEG 阈值；记录采用 p<0.05 并标注 `stated_explicitly=false`，合理。
