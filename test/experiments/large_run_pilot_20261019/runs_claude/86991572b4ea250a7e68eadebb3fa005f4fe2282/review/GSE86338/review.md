# 复核结果: GSE86338

总体结论: **pass**(无 blocking / major 项)

## 不同意或不确定的项

- `model_fit` (minor): 记录中的"论文的 Cuffdiff 把全部 iWAT 条件放在一起建模"论文并未说明(S4.3.1.p1 仅写使用 Cuffdiff)。未运行分析,无实际影响。建议改写为"论文未说明拟合结构"。

## 其他说明

- 机械标记 `unused_subject_like_column` 与 `pairing_key_candidate` 为误报: 候选键只是跨组织的重复序号,每个文库是4只动物混合(S4.2.p1),pairing_check 状态为 not_supported。
- 停止理由"n<3"成立: 每个 iWAT 组仅2个文库(适用性报告 0/6 比较达标),论文本身也是每条件2个混合样本。
- 待人工决定(开放政策问题): 是否允许在拒绝记录旁增加带标签的探索性敏感性分析(limma ~grp, SWIM vs CNT, n=2 vs 2)。
