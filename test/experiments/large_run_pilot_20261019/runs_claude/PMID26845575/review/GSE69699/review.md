# GSE69699 复核

总体结论: **fix**

## 分歧项
- **run_or_refuse (major)**: 论文的运动 vs 对照对比(mRNA-Seq 与 Ribo-Seq 各 2 个 3 只小鼠混合的重复)应当被分析。案例在 design 关口因 tools/suitability.py 的 MIN_GROUP=3 停下,但技能规则(decision-contract.md:78, SKILL.md:84)说小样本本身不是停止理由。修复: 增加运行器/规格选项,把 n=2 的计划对比作为探索性运行(edgeR TMM, 原始 P<0.01, >125 RPM 基因),并与论文的 26/37 对照。
- **stop_reason (major)**: 所述原因(每组 n=2)属实,但它是工具策略而非数据缺陷;应改标为工具策略阻塞,并补做上述探索性运行。

## 其他检查
分组、方向、配对(无重复测量,候选键只是标签巧合,表达检验 not_supported)、模型拟合、阈值、矩阵重建(RPM 还原为计数)均认同。

## 待人工决定
- 运行器是否应接受 n=2 的探索性对比(与 suitability 的 n<3 硬失败冲突)。
