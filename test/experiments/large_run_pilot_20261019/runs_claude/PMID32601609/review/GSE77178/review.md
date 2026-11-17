# GSE77178 复核结论

总体: pass（无 blocking / major 项）

## 需注意的项目
- model_fit (unsure, minor): 论文未说明联合还是分对拟合。本案例只做了联合 limma 细胞均值模型，DEG 数为论文的 4-12 倍（1064 vs 248；442 vs 35）。很可能因 RUVs k=6 因子未入模，已在 caveats 中记录。可选：增加分对 limma 作为敏感性分析。
- matrix_method (minor): 数据为 RUVs 标准化 FPKM，走 limma 正确；p 值分布右偏与计数偏高一致。推理文字中的中位数 5.8 与实际 6.04、11,332 与 11,337 基因数有小出入，均有解释。

## human_items
- 论文沉默时联合与分对拟合的取舍（开放政策问题）。
