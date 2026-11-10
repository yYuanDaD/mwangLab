# 评审结论 case_08 (GSE267512 / PMC12456396)

**总体: fix** (存在 1 个 blocking、2 个 major 问题,均可通过一次重跑解决)

## 不一致项

### pairing (blocking)
- 论文 S2.14.p6: `Genes ~ ID + timepoint`,ID 用于处理重复测量。
- 分析已把标题拆成 `subject`(24 名受试者有 PRE/POST 配对,7 人只有 PRE,2 人只有 POST),但执行公式为 `~ time`(covariance 记录为 `~ C(time)`,状态 `not_required`)。suitability.md 虽要求分块,却指向了错误的列(age of_donor)。
- 结果: 79 个 DEG,论文为 214 个;RPS6KC1 padj 0.0468(论文 FDR<0.01)。
- 修复: covariance 设为 required,分块项 `subject`(分类变量),公式 `~ subject + time`,保留 57 个样本(未配对样本也保留,与论文一致),重跑主分析(alpha 0.1)和 alpha 0.05 敏感性分析。

### model_fit (major)
- 论文是对全部样本拟合一个联合模型,但含 ID;执行的模型缺少 ID,而 `paper_route` 却标为 reproduced。
- 修复: 同上重跑;重跑前状态改为 reproduced_with_deviation。

### paper_match (major)
- 用不配对模型的 79/81 对比论文配对模型的 214,不是同一模型下的比较。
- 修复: 重跑后再与 214(上调 122 / 下调 92)及 RPS6KC1 FDR 比较,并在 caveats 中注明首次 `~ time` 结果已被替代。

## 其余检查
run_or_refuse、grouping、direction、confounding、matrix_method、threshold 均与论文一致(agree);stop_reason 不适用。样本数 31/26 与论文 35/27 的差异已记录为 GEO 缺失样本。
