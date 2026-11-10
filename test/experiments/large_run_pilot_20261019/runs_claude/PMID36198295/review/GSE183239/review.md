# GSE183239 审查结论

**总体: pass**(无 blocking / major 不一致项)

## 需要注意的项目(unsure / minor)
- `model_fit`(unsure, minor): 论文只说“每个组织用 DESeq2 做三个比较”,未说明联合拟合还是两两拟合。本案按组织做一次 `~ grp` 联合拟合;未并列报告两两拟合。
- `threshold`(minor): 阈值 padj<0.05、无倍数变化限制,转录正确。scWAT rescue 在 padj<0.1 时为 133(论文 132)的标记未单独记录,但 IHW→BH 偏差和过滤读法已记录,sum-filter 敏感性分析(139)可解释差距。
- `paper_match`(minor): 主分析采用“所有样本计数>10”的字面过滤,记录本身已显示它会剔除论文点名的 DEG(Dbp、Tef、Nr1d2、Per3、Thbs1、Cdkn1a);sum-filter 在 9 个格中多数更接近论文,但 SkM training 更差(24 对 92)。两者均已报告。

## 需要人工决定(human_items)
- 当论文数字更符合另一种读法时,以哪种过滤/阈值读法作为主结果。
- 论文未说明时,联合拟合与两两拟合如何取舍。
