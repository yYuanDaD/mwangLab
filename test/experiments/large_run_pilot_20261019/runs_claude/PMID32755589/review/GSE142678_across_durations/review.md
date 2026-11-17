# 审查: GSE142678_across_durations

总体结论: **pass**

该案例的分组、方向、阈值转写和矩阵方法都与论文一致，TPM 上用 limma 属已声明的偏差。跨时长合并是对 Fig 3A 的推断，已在 caveat 中说明，仅记为 minor。没有需要阻断的问题。

## 不一致或不确定项

- `model_fit` (unsure, minor): Paper fits each running-vs-sedentary pair within a time point (S2.1.p3). This case pools durations with an additive duration term (6 vs 6) as the Fig 3A estimand; the case records that the pooling is inferred from 'across all three time points' (S2.3.p1). Fig 3E uses 18-day mice, so Fig 3A may be a single-duration volcano.
  - 修正: Keep the caveat; optionally also report the per-duration fits once the sibling case is unblocked.

## 需人工判断

- Whether Fig 3A pools the three durations or shows one duration is not stated; the paper's own estimand per time point is in the sibling case.
