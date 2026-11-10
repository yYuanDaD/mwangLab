# GSE229755 复核结果

**总体结论：pass**（无 blocking / major 问题，无 disagree 或 unsure 项）

- 数据为体内小鼠慢性跑台运动（6周）肝脏转录组，Exe 6 vs Con 6，分组、方向和阈值与论文（S2.1、S2.3、S2.4、S3.1）一致。
- 标记 pairing_key_candidate 只是标题后缀 L1-L6（组内重复编号），论文说每只小鼠一个肝脏样本，表达相关性检查 not_supported（permutation p=0.79），不是重复测量，无需配对。
- GEO 仅有 FPKM，DESeq（需原始计数）不可行；用 limma-trend（log2(FPKM+1)）并声明偏离，附未过滤敏感性分析。结果 0 个 DEG（论文 88），HANDBACK 未夸大，Cyp4a10/Cyp4a14 方向一致但 padj 不显著。
- 待人工决定（非错误）：是否从 SRA 获取计数以运行 DESeq 复现。
