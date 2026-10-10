# 论文主结论与 Agent 分析差异：Bo 讨论案例

核查日期：2026-09-09。分支：`codex/bo-multiomics-benchmark`。

**最值得讨论的是 GSE279359：Agent 未复现论文报告的表达变化，而且把转录本层面的结果当成了基因结果。** 在论文相同的时间点和显著性阈值下，作者报告 46 / 32 / 49 个差异基因，Agent 的 DESeq2 输出只有 1 / 4 / 0 个显著行。进一步核查发现，两者分析单位不同，因此这是明确的复现差异及流程问题，尚不能宣布论文的核心剪接结论被否定。

**本次未确认“同一研究范围、同一终点、可信结果显著反方向”的主结论冲突。** GSE282641 的氧化代谢和糖酵解方向实际上与论文相符，缺失的是运动与时间依赖性检验。不能为凑出反例，把分析缺失、未显著或不同终点解释成相反结论。

## 1. GSE279359：表达变化未复现，且分析单位错配

论文：*Impact of Acute Endurance Exercise on Alternative Splicing in Skeletal Muscle*。
仓库缓存为预印本 PMID40693573 / PMC12248044；本次另通过 Europe PMC 全文 XML 核对了[正式发表版本 PMID40746864 / PMC12312519](https://pmc.ncbi.nlm.nih.gov/articles/PMC12312519/)，以下表达数量与方法描述在正式版本中仍存在。不是版本差异造成的数字不一致。

### 论文支持的结论与 Agent 得到的结果

论文主要结论是急性耐力运动改变骨骼肌的可变剪接和异构体表达，24 小时恢复期尤其值得关注；有些变化可以发生在基因总表达未显著变化时。论文还报告同一小鼠 LRS 队列的基因表达变化。核查对象为小鼠腓肠肌，不混入文中的人类短读长队列。

最近汇报第 10 张幻灯片使用的是 **2026-06-22 三时间点、多方法运行**。本次直接重数该运行的 CSV，避免拿 8 月只分析立即时间点的运行去比较三个时间点。

共同筛选条件：`padj < 0.05` 且 `abs(log2FoldChange) > 1.0`；每组 5 个样本。

| 运动后 vs 运动前 | 论文基因数，Results 3.2 / Fig. 2F–H | Agent DESeq2 显著行 | Agent edgeR 显著行 | Agent limma-voom 显著行 |
|---|---:|---:|---:|---:|
| 立即 | 46 | 1 | 1 | 0 |
| 1 小时 | 32 | 4 | 16 | 5 |
| 24 小时 | 49 | 0 | 1 | 0 |

更严格的 `abs(log2FC) > 1.5` 下，论文为 **23 / 13 / 31**；Agent DESeq2 仍为 **1 / 4 / 0**。因此差异不能仅用“Agent 使用了更严格的 fold-change 阈值”解释。这里逐方法对照，没有额外施加两方法一致才显著的共识门槛。

### 发现的具体问题

源矩阵 `GSE279359_processed_counts.txt.gz` 有 **8,452 行、8,452 个不同 transcript_ID、5,029 个不同 gene_ID**。其中 **4,478 行**与别的行共享 gene_ID。三个时间点的三个 DA 方法输出均完整保留这 8,452 个源行 ID，未汇总成 gene_ID。

例如 Sirt2 的两个异构体是源行 `5358` 和 `5359`，同属 `gene_ID=20617`，但分别进入 DA。输入也包含 Known、Antisense 和 Intergenic gene-novelty 类别。论文 Methods 的 “Differential Gene Expression and Differential Alternative Splicing Analyses” 小节则描述使用 Swan v2.0 的**基因层面 DGE**，基于至少在一半样本中检测到的已知基因，并单独进行异构体/剪接分析。论文每个比较检测的基因数分别为 6,323 / 5,459 / 6,125，与 Agent 的 8,452 个转录本行不是同一检验集合。

因此，上表应读作“现有流程输出与论文的表达发现差距很大”，**不能把 1/46 等比例当作基因召回率**。分析单位、纳入特征集合、方法和过滤均未对齐。已证实单位错配；它对全部数量差异的贡献还没有通过重跑分离出来。

还有一个可以直接讨论的支持性发现：论文 Fig. 2 报告 Ube2d1 在立即时间点的 LRS `log2FC=0.75`、`padj=0.0002`，并做了 RT-ddPCR 验证；Agent 对其转录本行给出 `log2FC=0.946123`、`padj=0.999903`。**方向一致，显著性未复现**。论文验证的另外两个基因 Fbxo32、Fos 没有出现在当前选用矩阵的 `annot_gene_name` 中，不能将它们记为“测量后无变化”。

### 对主结论应如何表述

可用于会议：

> GSE279359 的现有分析没有复现论文报告的表达变化，也没有执行支撑其核心结论的剪接/异构体分析。尤其在 24 小时，论文报告 49 个差异基因，而 Agent 的 DESeq2 输出为零。核查发现 Agent 实际检验的是转录本行，说明 pipeline 尚未匹配论文的分析层级。

不应写成“运动没有生物学效应”或“论文的剪接结论错误”：零个显著结果不等于证明无效应；基因 DGE 也不检验 DAS/DIE。

**与 Bo 的具体讨论点：**确认当前 GEO 文件是否为完整分析输入；取得作者用于 Fig. 2 的基因汇总表、过滤规则和 Swan 输出；先复现同一基因层面 DGE，再单独比较 24 小时的异构体比例/剪接结果。固定数据及注释后比较方法，不能仅通过调阈值追求数字接近。

## 2. GSE282641：主要科学问题未被检验，不能列为相反结论

论文：[HIF1α mediates circadian regulation of skeletal muscle metabolism and substrate preference in response to time-of-day exercise](https://pmc.ncbi.nlm.nih.gov/articles/PMC12280960/)，PMID40627397。

论文的主张是 HIF1α 对运动后代谢的影响依赖昼夜时间。Fig. 5 对运动后的 KO 与对照进行分时段比较，ZT3 / ZT15 分别报告 516 / 91 个差异转录本；氧化代谢相关富集主要出现在 ZT3。Methods 使用 `~0 + group + sex`，FDR 阈值 0.1，并说明排除了一个低覆盖样本。

8 月 27 日汇报第 6–8 张及 8 月 25 日运行中，Agent 把 **64 个样本**合并为 `KO vs WT`，模型为单因子 `~ condition`，无协变量，报告 **394 个 padj<0.05 的差异结果、45 个 FDR<0.25 的 Hallmark 富集结果**。原始 metadata 明确包含 genotype、exercise/sedentary、ZT3/ZT15 和 sex，却未在模型中保留这些维度。运行使用全部 64 个样本；论文提及的低覆盖样本是否应从这份 GEO 矩阵排除，需要核对具体样本 ID，不能凭分组猜测。

从原始 GSEA 文件重读，正 NES 表示偏向 KO：

| Hallmark | NES | FDR q |
|---|---:|---:|
| Oxidative phosphorylation | +2.924709 | 0.001000 |
| Glycolysis | −1.523927 | 0.006270 |
| Fatty acid metabolism | +1.280008 | 0.064299 |

三个重复运行的这些数值一致。**KO 氧化代谢增强、糖酵解减弱的总体方向与论文相符**。直接把“论文 HIF1α 促进糖酵解”与“Agent KO 糖酵解下调”称为相反方向，是把基因功能存在与缺失两种干预混淆。

真正差异是：Agent 只给出平均基因型差异，不能回答“是否在 ZT3 更强、是否由运动诱发”。此外，论文 GO 与 Agent Hallmark、作者 FDR 0.1 与 Agent DEG FDR 0.05 也不一致；394 不能直接与 516 或 91 比大小来判定复现成败。

可用于会议：

> GSE282641 的 Agent 结果给出了方向一致的平均 KO–WT 代谢变化，但未检验论文核心的时间依赖运动反应。需要按论文样本范围、分组和 sex 校正复现，再检验预先定义的运动与时间比较。

## 3. 旧讨论材料中不应升级为主结论冲突的案例

| 案例 | 原材料实际证明的内容 | 本次处理 |
|---|---|---|
| GSE317978 | DEG 显著比例异常、每组 n=2，且作者 DESeq2 列与 Agent FPKM→limma 不一致 | 可作结果可靠性案例；未建立可信、同口径的论文主结论对照 |
| GSE270703 | 矩阵分类与方法 gate 冲突，DA 被阻止 | 没有可比较的生物学分析结论 |
| GSE302944 | transcript ID 导致 GSEA 失败 | 没有可比较的通路结论 |
| GSE308674 / GSE315678 | 注释列、分组或执行问题 | 工程回归案例，不是主结论反证 |

对这几例的说明来自 9 月 3 日讨论材料及既有运行审计；本次没有重跑 DA，也没有为这些失败案例新建论文主结论金标准。

## 4. 成果卡不能替代独立复现证据

重新统计 8 个 accession × 3 次的 24 张 machine-draft 成果卡，共 59 条 claim-evidence links：

- 54 条连接 `paper_reported`，3 条连接 `computed`，2 条连接 `descriptive`。
- 13 条 `direct_support`、31 条 `partial_support`、7 条 `secondary_finding`、8 条 `not_evaluable`，**0 条 `contradictory`**。

这些是现有机器标签的清点，不是“已证明没有矛盾”。卡片用论文自身的实验结果支持论文主张，可以是正确的文献整理，但不能据此宣布 Agent 复现了主结论。最近汇报已将 GSE282641 标为 secondary finding，也明确写了 GSE279359 “splicing not tested”；本报告把数值差异及分析单位问题进一步展开。

## 5. 证据、复核范围与后续验收

本次检索了 8 月 27 日汇报、9 月 3 日 Bo 材料、20×3 稳定性报告、24 张重复成果卡，以及 `output` 下的三份旧 agreement 表；深入重数了上述两个论文案例的现有结果。旧 agreement 表未发现 `contradicted` 行。本次不是所有 output 研究的逐篇全文审计，也未运行新的统计模型；不以一个总分表达主结论复现程度。

交付文件：

- [机器可读证据及源文件 SHA-256](paper_discrepancy_evidence_20260909.json)：51 个输入文件，包含精确结果路径、论文文本定位、逐方法计数、三个重复的 GSEA 数值和幻灯片文字。
- [离线重数脚本](../../test/reports/audit_paper_discrepancies.py)：从仓库外工作目录调用也可运行；不调用 LLM，不重新做 DA。依赖本地 `data/`、`output/` 归档，以及本次下载的正式发表全文 `output/paper_discrepancy_audit_20260909/PMC12312519.xml`。这些大文件按现有 `.gitignore` 不进入分支。

```powershell
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe test\reports\audit_paper_discrepancies.py
```

重要源文件：

- [GSE279359 三时间点运行决策](../../output/agentA_cohort_rerun_0622/cohort_analysis/GSE279359/decisions.json)
- [GSE279359 转录本计数源矩阵](../../data/GSE279359/GSE279359_processed_counts.txt.gz)
- [GSE282641 原始决策和模型参数](../../output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE282641/GSE282641/decisions.json)
- [GSE282641 原始 GSEA](../../output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE282641/GSE282641/DEG_results_ko_vs_wt_GSEA_Hallmark.csv)
- [8 月 27 日汇报](../../output/presentation_sample_20260826/bioinformatics_agent_report_short_20260827_final_title.pptx)
- [9 月 3 日旧讨论材料](../../output/bo_discussion_materials_20260903/BO_DISCUSSION_BRIEF.md)

Bo 讨论的首要决定应是：将 GSE279359 定为分析层级/表达复现案例，将 GSE282641 定为多因素主问题覆盖案例。只有样本、特征层级、时间点、比较方向和终点均对齐，且结果通过科学有效性检查后，才把显著反方向结果列入“主结论冲突”。本次两个候选都尚未达到这一条件。
