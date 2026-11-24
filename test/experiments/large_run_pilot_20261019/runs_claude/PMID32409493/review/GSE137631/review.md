# GSE137631 审查结果

**总体结论：pass**（无 blocking / major 项）

没有 `disagree` 或 `unsure` 项。

- 运动臂（RYGB+ET，6 人 × PRE/POST9）存在，随机对照为单纯 RYGB；分组 6/6/6/6/6 与 GEO 设计一致，30/30 样本精确对齐。
- 同一女性 PRE/POST9 重复取样，已用 subject 区组（`~ subject + grp`）；交互项用 limma paired_change，已声明为偏差。
- 论文仅有摘要，无阈值和 DEG 数：已记录为 `workflow_default`（padj<0.05），HANDBACK 未过度声称。
- 次要提示：lean 对比可能存在按臂的处理批次（"WD." 前缀），已作为 caveat 记录。

待人工决定（开放政策）：论文沉默时联合拟合与成对拟合的选择（此处为成对）。
