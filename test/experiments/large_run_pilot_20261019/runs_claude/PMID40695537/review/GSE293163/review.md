# 复核结论：GSE293163

**总体：pass**（无 blocking / major 项）

## 无 disagree 项；以下为 minor 备注

- confounding（minor）：Young 为 2男5女，Old 为 4男4女（S2.2.p1），基线 Old vs Young 对比部分被性别混杂。研究 caveat 已说明为关联性对比且无性别协变量，但未提及性别比例差异。运动前后的组内对比不受影响。
- paper_match（minor）：HANDBACK 称论文计数与“均值 log2FC 子集”计数“匹配”，但 44 vs 53、1,301 vs 1,026、634 vs 665 并不匹配（Old 偏高 27%）。建议改为“更接近”。study caveat 中的“most likely”措辞是准确的。
- matrix_method / threshold（minor）：低表达过滤用 CPM 近似论文的 read 规则（Old 检测基因数 24,541 vs 19,101），阈值冲突（S2.8.p1 FDR<0.01 与 S2.7.p2 5% FDR）以及论文计数更符合后处理子集的情况均已记录，属于已披露的偏差/开放政策问题，不是错误。

## 待人工确认
- 当论文数字更符合后处理的均值 log2FC 子集而非其声明的 FDR 规则时，应报告哪个阈值（开放政策问题）。
