# 复核结果:GSE165110

**总体结论:pass**(没有 blocking 或 major 项,无 disagree / unsure 项)

- 拒绝运行(无运动臂)的理由成立:GSE165110 仅含 C2C12 肌管 4% STEM 分泌组 vs 4% 马血清(6 vs 6)。论文体内的卸载/恢复小鼠没有测序(S2.6.p2、S3.4.p1)。
- 机械标记 `refusal_vs_exercise_words` 是误报:命中的 `contact_department` 只是作者单位(Physical Therapy and Athletic Training)。
- 阈值记录正确:DESeq2、FDR 5%(adj. P ≤ 0.05)、无倍数变化截断(S2.7.p1)。论文没有给出总 DEG 数。
