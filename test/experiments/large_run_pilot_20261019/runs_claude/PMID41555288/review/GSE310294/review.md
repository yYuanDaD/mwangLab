# GSE310294 审查结果

总体结论: pass（无 blocking 或 major 项）

## 需要关注的项

- grouping (unsure, minor): 分组 CTRL 3 / EX 3 与论文 n = 3 一致，无排除样本。矩阵列 sampleN_FPKM 通过改名脚本对应到 "Library name: Sample N"，这是一个假设。论文点名的基因 Col1a1、Sp7、Bglap 方向与论文相反，Sample_6 是离群样本，因此不能从文件中排除列顺序错位。
- pairing: 无分歧。机器标志 pairing_key_candidate 为误报：每只大鼠一个左胫骨样本（S2.6.p1，Fig. 5），repN 只是组内重复编号，表达量检验为 not_supported。

## 待人工处理

- DESeq2 结果未复现论文（4459 对 2076 个 DEG，成骨基因方向相反）。文件无法确认补充文件的列顺序是否等于 GEO 的 Sample 1-6，必要时询问作者。
