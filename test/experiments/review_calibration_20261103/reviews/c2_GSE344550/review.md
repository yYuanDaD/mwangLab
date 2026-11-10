# 复核结论：GSE344550（pass）

总体：通过。该系列为人巨噬细胞体外感染 C. parapsilosis（BP vs LBP，3 h / 24 h），论文与 GEO 元数据均无运动、训练或活动因素，在 design 阶段拒绝分析的理由属实，且依据完整的 30 个样本元数据与论文全文检索，并非窄范围检索。

没有 disagree 或 unsure 项。
- 矩阵为 RPKM（文件名、data_processing、小数值一致），论文用原始计数 + edgeR，差异已记录。
- 阈值仅 |log2FC|>1，无 p/FDR，转录正确。
- 配对候选键（strain+标题后缀）表达检验不支持（p=0.40），论文也未提供供体信息，且已拒绝，故无影响。
