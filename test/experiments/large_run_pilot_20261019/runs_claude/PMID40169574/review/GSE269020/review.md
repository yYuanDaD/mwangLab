# GSE269020 复核结论

**总体: pass**

没有 disagree 或 unsure 项。

- 拒绝理由(测序样本中无运动组)属实:GEO 元数据 treatment 恒为 HFD-fed,Fig 5a 图注为 "without exercise",DA.p1 与 S4.18.p1 一致。
- 机械标记 pairing_key_candidate 为误报:WT-1..4 / KO-1..4 是组内重复编号,论文为每组 4 只小鼠、单一组织与时间点,pairing_check 结果 not_supported(r 0.02,p 0.19)。
- 次要说明(minor):阈值已按 S4.18.p1 转录并记录与 Fig 5a 图注(仅 Padj < 0.05)的差异;矩阵仅有 FPKM,与论文 edgeR 计数路线不符,已记录且因拒绝而无影响。

待人工(开放策略问题,非错误):是否应把 KO vs WT 的基因型对比作为带标签的非运动结果给出。
