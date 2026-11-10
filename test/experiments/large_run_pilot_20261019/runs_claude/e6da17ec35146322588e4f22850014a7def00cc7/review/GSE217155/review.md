# GSE217155 复核结果

总体结论:**pass**(无 blocking / major 项)

没有 disagree 或 unsure 项。

说明:
- 主要比较 EXE vs NASH(同为 Ath 饮食,仅运动不同),方向正确(Dio1 上调 log2FC +1.95)。
- 阈值与论文 S2.6.p1 一致(padj<0.05 且 |log2FC|>1,严格不等号);结果 188 对论文 204,已记录,GEO 每组 3 只 vs 论文 8 只。
- 机器标记 unused_subject_like_column 为误报:该列就是分组列本身,样本为独立个体,无重复测量。
- 开放策略问题:论文未说明联合模型还是两两拟合(当前为联合 ~grp 模型),留给人工决定,不影响通过。
