# 审查结论: GSE281849 (PMID39609254)

总体: **pass** (无 blocking 或 major 项)

没有 `disagree` 或 `unsure` 项。说明:

- 机械标记 `possible_reversed_contrast` (ACT vs SED, AR vs SED) 为误报: SED 是不运动对照, ACT 是运动组, 方向与论文图3一致; 命名基因 (Igfbp5, Ostn, Ak4, Zfhx4 下调, Smyd2, En1 上调) 方向均与论文相同。
- `pairing_key_candidate` 只是组内重复编号 (replicate k), 不是动物ID; 论文为三组独立随机分组, 表达相关性检验为 not_supported, 不需要分块。
- 阈值 (minor): 按论文方法 padj<0.05 且 |log2FC|>0.25 得到 76/45/134; 作者代码规则 (>=0.27) 得到 71/41/126, 更贴近论文的 71/40/124。两者均已记录, 属于开放的政策问题, 交给人决定哪个作为主报告。
- 可选: 联合模型 AR vs SED 只检验了 1990 个基因 (15 个 DEG), 可看一下是否为独立过滤的结果; 仅影响敏感性分析。
