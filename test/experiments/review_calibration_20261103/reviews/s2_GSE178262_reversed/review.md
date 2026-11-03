# 复核结论:GSE178262_wheel

**总体结论:fix(需要修改后重跑一次)**

分组(CTRL 8 / DA 8,每个 ZT 每组 n=4)、矩阵与方法(tximport 伪计数取整后用 DESeq2)、阈值(FDR <= 0.05)、与论文计数的对比(ZT4:2257 vs 2094;ZT16:369 vs 368)均成立。小鼠单笼饲养、每只一块肌肉,无重复测量,配对检查不支持任何候选键。

## 不同意的项目

### direction(对比方向)——major

- 论文与 paper_reconstruction 的规划对比是 DA vs CTRL(S3.8.p1,日间训练的效应)。
- 实际执行的 design.contrasts 把 control 设为 "DA at ZT4/ZT16",treatment 设为 "CTRL at ZT4/ZT16",即结果是 CTRL/DA,符号与规划相反。机械标记 possible_reversed_contrast 也指出了这一点。
- 例:Nr4a3 log2FC = -3.88、Klf15 = -0.87、Klf4 = -1.04(这些基因在 DA 中更高,却显示为负)。
- DEG 的集合与数量不受影响,只有符号以及上调/下调的拆分(ZT4:1121 上调 / 1136 下调)与论文读法相反。
- 修改建议:把 control 改为 CTRL(ZT4 与 ZT16),treatment 改为 DA,改名为 act_DA_vs_CTRL_zt-Z04 / -Z16,用 run_joint_deseq2 重新执行,并重新生成上调/下调计数与 paper_gene_check;探索性对比也让 DA 位于处理一侧。

## 不确定的项目

### model_fit(拟合结构)——minor

- 论文没有说明是对全部样本拟合一个模型还是逐对拟合(S2.8.p2 只写了 DESeq2 1.26.0 和收缩的 log2FC)。
- 本案例对 16 个样本拟合一个 cell-means 联合模型。ZT16 与论文几乎一致(369 vs 368),ZT4 多 7.8%(2257 vs 2094)。
- 建议(可选):再做每个 ZT 单独拟合的敏感性分析,与联合模型并列报告。

## 其他说明(非分歧)

- threshold:阈值取自跑台实验一节 S3.3.p2,转轮实验一节 S3.8 没有重述,属于沿用;其他规则(如 padj<0.05 且 |lfc|>=0.585 得 537/60)都不比 padj<=0.05 更贴近论文计数。
- paper_match:Klf5 在 ZT4 的 padj 为 0.10,而论文把它列入重叠基因,属于基因层面的小差异。

## 待人工决定的开放问题

- 论文未说明时,联合拟合与逐对拟合哪个作为主结果。
- 是否把 S3.3.p2 的 FDR <= 0.05 规则沿用到湿轮实验。
