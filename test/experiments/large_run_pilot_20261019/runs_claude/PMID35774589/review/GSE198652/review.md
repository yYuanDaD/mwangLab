# GSE198652 审查结论

**总体：pass**（无 blocking / major 项）

没有 disagree 或 unsure 项。

- 机械标记 possible_reversed_contrast（4 个）为误报：对照 Sed、处理 PoW，方向正确。数据佐证：老龄比目鱼肌 Aldh1l1 log2FC +0.62、Lrrn1 +0.78（论文 S3.7.p1 称运动后升高），氧化代谢基因下调（S3.6.p1）。
- 分组与样本数（老龄 5 vs 4，年轻 4 vs 4）与 S2.8.p1 一致；"Aged Soleus" 标题错标的跖肌样本已按 source_name 纠正并记录。
- 每个肌肉、年龄单独拟合，与论文一致；同一小鼠的两块肌肉不在同一模型内，无需配对。
- 阈值 padj<0.10、无倍数变化条件，与 S2.10.p1 一致。
- 小问题（minor）：最大计数>50 的过滤在各层内进行，论文写"across all samples"，已作为偏差记录。
