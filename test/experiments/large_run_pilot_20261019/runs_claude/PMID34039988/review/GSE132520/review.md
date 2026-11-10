# 复核结果：GSE132520

**总体结论：pass**（无 blocking / major 项）

## 需要关注的项目
- **model_fit（unsure，minor）**：论文未说明拟合结构（S4.26.p1 指向补充表）；GEO 的 data_processing 写的是 Cuffdiff（成对比较）。本案例用一个 16 样本的联合模型 ~0+grp，已声明为偏离。DEG 数比论文少 4 倍（MM 137 vs 582）和 7 倍（VV 31 vs 216），更可能来自方法差异（FPKM 上的 limma-trend 对 Cuffdiff），而非拟合结构。建议（可选）补做每个基因型 8 个样本的单独拟合作为敏感性分析。
- **confounding（agree，minor）**：窝别与分组交叉，已记录。注意 L2161 只出现在运动组，L2032/L2127 只出现在 MM 久坐组，窝别与运动部分混杂；记录已说明不作为协变量的理由。

## 机械标志
- `unused_subject_like_column`（source_name_ch1）为误报：它是 基因型x处理 标签（4 个取值，每个 4 个样本），不是动物编号。每只小鼠只取一块股四头肌，无重复测量。

## 开放政策问题（human_items）
- 论文沉默时联合拟合与成对拟合的选择。
