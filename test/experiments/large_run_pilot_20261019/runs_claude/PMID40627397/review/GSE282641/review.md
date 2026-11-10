# GSE282641 复核结论

**总体结论：pass**（没有 blocking 或 major 项，无 disagree / unsure 项）

两个机械标记 `pvalues_piled_near_1`（KO vs WT ZT15 运动组；KO 的 ZT15 vs ZT3 久坐组）已核对：它们出现在 DEG 最少的对比中，而差异基因数与论文基本一致（101=101，191=191，89 vs 91，479 vs 516），说明归一化和模型没有问题，只是 pydeseq2 Wald 检验下低表达基因的离散 p 值靠近 1。判为 minor（matrix_method），无需改动。

其余检查（run_or_refuse、grouping、direction、pairing、model_fit、confounding、threshold、paper_match）均与论文一致；stop_reason 不适用（案例已完成，没有停止或拒绝）。

备注：整体 KO vs fl/fl 的对比论文未说明，已按“声明的偏差”处理（1305 vs 1473）；GEO 中没有笼位信息，无法检查笼位混杂。
