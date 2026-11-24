# GSE126962 复核结果

**总体结论:pass**(无 blocking / major 项)

## 需要注意的项目(unsure)

- `model_fit`(minor):分析对全部137个样本使用单一 cell-means limma 模型。论文仅有摘要,未说明是联合拟合还是成对拟合,属于开放的政策问题,不算错误。

## 待人工确认

- 论文沉默时,联合拟合与成对拟合的选择(开放政策问题)。
- 论文的阈值与 DEG 数量需要全文才能做数值比对。

其余检查(run_or_refuse、grouping、direction、pairing、confounding、matrix_method、threshold、paper_match、stop_reason)均一致或不适用。
