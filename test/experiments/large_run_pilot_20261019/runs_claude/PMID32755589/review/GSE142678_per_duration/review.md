# 审查: GSE142678_per_duration

总体结论: **fix**

该案例在设计阶段因每组 n=2 而停止，理由属实，但技能规定仅凭小样本不应停止，论文的主要估计量（每个时长的 IP 和 IN 对比）因此完全没有执行。建议以探索性标注运行六个对比，并与论文的 460/544/124 对照。其余检查均一致。

## 不一致或不确定项

- `stop_reason` (disagree, major): The stop reason (all cells n=2, 0/22 comparisons reach n>=3) is true, but the skill states small n alone is not a stop, and the case itself notes that run_joint_limma can take planned small-n contrasts. The paper's own primary estimand (per-duration IP and IN, 544/460/124 DEGs) was therefore not run at all, while only the secondary pooled contrast was.
  - 修正: Execute the six per-duration contrasts with run_joint_limma (cell-means ~0+cell per fraction, 6 df) labelled exploratory n=2 per arm, and compare to paper counts 460/544/124 under the paper's rule; if the contract/suitability gate cannot allow it, record as policy item.

## 需人工判断

- Policy: can the decision contract accept a not_analyzable(sample_size) verdict as exploratory when the paper itself analysed n=2 per cell? Currently blocks the paper's primary estimand.
