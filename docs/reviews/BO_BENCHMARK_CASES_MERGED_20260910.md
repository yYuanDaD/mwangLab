

### GSE279359：表达变化未复现，且分析单位错配

**数据：** [GEO GSE279359](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE279359)；[本地输入矩阵](<E:/agent/mwangLab/data/GSE279359/GSE279359_processed_counts.txt.gz>)。

**原论文与 Agent 提取的结论：** [正式论文全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12312519/)。论文认为急性耐力运动会改变骨骼肌的可变剪接和异构体表达，24 小时恢复期尤其明显；部分变化可发生在基因总表达没有显著变化时。论文同时报告小鼠腓肠肌的基因表达变化，并把基因层面 DGE 与异构体/剪接分析分开。

**Agent 结果：** 在论文相同时间点和 `padj < 0.05`、`|log2FC| > 1` 条件下，论文报告立即/1 小时/24 小时分别有 46/32/49 个差异基因；Agent DESeq2 只有 1/4/0 个显著行，edgeR 为 1/16/1，limma-voom 为 0/5/0。输入有 8,452 个 transcript rows，但 Agent 没有先汇总到 gene level；其中 4,478 行与其他行共享 gene ID。

![GSE279359：不同方法和时间点的 DEG 数量](../../output/bo_figures_20260911/gse279359_method_comparison.png)

**复核判断：** 这是明确的复现差异和流程层级问题，但不能据此否定论文的剪接结论。下一步应取得作者 Fig. 2 的 gene-level 表、过滤规则和 Swan 输出，先复现 gene DGE，再单独比较异构体/剪接结果。

### GSE282641：总体方向相符，但没有检验论文核心设计

**数据：** [GEO GSE282641](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE282641)；[本地 Agent 决策目录](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE282641/GSE282641/decisions.json>)。

**原论文与 Agent 提取的结论：** [原论文全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12280960/)。论文认为 HIF1α 对运动后骨骼肌代谢的影响依赖昼夜时间；运动后 KO 与对照的差异在不同 ZT 时段不同，氧化代谢相关变化主要出现在 ZT3。

**Agent 结果：** Agent 将 64 个样本合并为单因素 `KO vs WT`，得到 394 个差异结果和 45 个 Hallmark 富集结果。氧化磷酸化 NES 为 +2.925，糖酵解 NES 为 −1.524，方向与论文的总体代谢方向一致。

![GSE282641：KO vs WT Hallmark NES](../../output/bo_figures_20260911/gse282641_gsea_nes.png)

**复核判断：** 不能称为论文结论冲突。Agent 没有纳入 exercise/sedentary、ZT3/ZT15 和 sex，也没有复现论文的时间依赖运动比较。应按论文设计重新建模。

### GSE317978：结果数量异常，contrast 方向未决

**数据：** [GEO GSE317978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317978)；[作者/Agent 比较表](<E:/agent/mwangLab/output/bo_discussion_materials_20260903/GSE317978_PRELIMINARY_COMPARISON.csv>)。

**原论文与 Agent 提取的结论：** 当前仓库没有经过核对的原论文正文或作者脚本，因此暂不补写论文主结论；应先向 Bo 索取论文链接、作者代码和 raw counts。

**Agent 结果：** 每组只有 2 个 pooled islet 样本。Agent 对 FPKM 做 `log2(x+1)` 后运行 limma，得到 11,339 个 `padj < 0.05` feature，占 66.5%。与作者结果列比较，Pearson 相关 0.665、Spearman 相关 0.789、同号率 73.9%，显著集合 Jaccard 为 0.306；但作者列名和 Agent 文件名的比较方向相反，机械翻转后相关变成 −0.789。

![GSE317978：Agent 与作者结果一致性指标](../../output/bo_figures_20260911/gse317978_agreement_metrics.png)

**复核判断：** Agent 结果触发 `implausible_sig_fraction` 和 `tiny_n_per_group`，应标记为 blocked / not trustworthy。必须先确认作者 fold-change 的定义、raw counts、pooled biological unit、过滤和统计模型。

### GSE270703：空间转录组被当作普通 bulk 矩阵

**数据：** [GEO GSE270703](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE270703)；[本地 workflow log](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE270703/workflow.log>)。

**原论文与 Agent 提取的结论：** [原论文记录](https://pubmed.ncbi.nlm.nih.gov/40894879/)。论文认为有氧和抗阻训练会改变年轻成人骨骼肌的空间转录组，包括肌纤维类型表达、间质细胞群和血管生成相关变化。

**Agent 结果：** 合并矩阵为 4,992 features × 10 samples，数值范围 −1,501 至 23,373，100% 整数型；pipeline 将其分类为 log-transformed，随后因 raw-count-like 特征阻止 limma。

**复核判断：** 这一轮没有可用的 DEG，但这是 guardrail 阻止了一个物理含义不一致的输入继续进入 limma，不能把它写成 exercise 没有表达影响。需要检查 `_unpacked` 中的原始表头和实际 abundance/count 列；如果目标是复现论文的空间结论，还需要空间转录组专用分析模块。

### GSE302944：DEG 初步可用，但 transcript ID 使 GSEA 失效

**数据：** [GEO GSE302944](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302944)；[本地 workflow log](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE302944/workflow.log>)。

**原论文与 Agent 提取的结论：** [原论文全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12330668/)。论文认为 Cebpa_ASKO 会损害 gWAT 发育，使脂肪组织在高脂饮食下不能正常扩增；iWAT 形态仍可形成，但脂肪细胞功能、脂质代谢和分化相关转录程序发生改变。

**Agent 结果：** 输入为 118,489 × 6 的 transcript-level FPKM/TPM 矩阵，`log2(x+1) + limma` 得到 201 个 transcript-level DEG。GSEA 失败，因为排序 ID 是 `ENSMUST...` transcript IDs，而 Hallmark 使用 gene symbols，overlap 为零。

**复核判断：** 201 个 DEG 只能算未完成注释的初步结果，不能据 GSEA 失败推导通路阴性结论。Agent 已有 Ensembl gene-ID→symbol 的 GSEA 映射能力，但当前输入是 transcript IDs（`ENSMUST...`），不满足现有识别规则；需要补充 transcript→gene 映射或在前处理阶段按 gene 汇总后重跑。

### GSE315678：样本已对齐，但 design gate 错误

**数据：** [GEO GSE315678](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE315678)；[本地 workflow log](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE315678/workflow.log>)。

**原论文与 Agent 提取的结论：** 当前仓库没有经过核对的论文全文，因此不补写论文主结论。metadata 说明使用 Salmon，并按 GENCODE M30/mm39 汇总到 gene level。

**Agent 结果：** 26 个样本中 `Control chow diet` 和 `CDAHFD` 各 13 个；日志记录了 26/26 substring alignment 和 26/26 exact alignment，但 design policy 仍报告组别缺失。

**复核判断：** 这是该历史运行中出现的 metadata/design gate 异常，不是“没有 contrast”。当前代码的设计校验本身使用精确的 metadata group 值和已对齐样本集合；应在当前分支用保存的 metadata 和 log2 矩阵重跑 `select_valid_two_group_design()`，确认这个问题是否已经修复后再把它计为现行缺陷。

## 其他需要标记的案例

### Kang scRNA-seq（GSE96583）

**数据：** [GEO GSE96583](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE96583)。

**原论文与 Agent 提取的结论：** [Kang 等，Nature Biotechnology](https://doi.org/10.1038/nbt.4042)。论文分析 8 名 lupus donor 的配对 PBMC，在 IFN-β 刺激 6 小时前后比较免疫细胞类型的转录反应；donor pairing 是设计核心。

**Agent 结果与判断：** 7 个 cell types 完成 pseudobulk，多数有 6–8 个 biological samples；Megakaryocytes 只有 1 vs 1，已正确跳过。其余 cell type 的 DEG 数不能直接作为复现结论，需重新确认 donor pairing、annotation 和 covariates。

![Kang scRNA-seq：各 cell type 的 DEG 数量](../../output/bo_figures_20260911/kang_scrna_deg_by_celltype.png)

### PXD025560 proteomics

**数据：** [PRIDE PXD025560](https://www.ebi.ac.uk/pride/archive/projects/PXD025560)。

**原论文与 Agent 提取的结论：** 当前验证没有使用原论文真实 case/control 设计，因此不引用任何原论文生物学结论解释这次输出。

**Agent 结果与判断：** DIA-LFQ 的 labeling、缺失值填补、log2 转换和 limma 可以运行，但测试脚本使用样本前半/后半的任意分组。它只能证明 proteomics plumbing 可运行，不能作为生物学 benchmark；需要 Bo 提供真实分组、批次和 protein-level gold table。

### GSE308674

**数据与运行记录：** [GEO GSE308674](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE308674)；[原始 count matrix](<E:/agent/mwangLab/data/GSE308674/GSE308674_gene_counts.csv.gz>)；[workflow log](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE308674/workflow.log>)；[Agent decisions.json](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE308674/GSE308674/decisions.json>)。

**Agent 结果：** metadata 中识别出 `PBS injection`、`HIIT` 和 `HIIT+MCT1/2 inhibitor` 三组，并生成了两个 contrast；但注释列混入表达矩阵且存在缺失/非有限值，两个 DESeq2 比较均被 policy 阻止。当前没有可比较的生物学结果，应作为工程回归案例处理，不能升级为论文主结论冲突。

## 总体判断与后续复核顺序

### 对“Agent 是否已经正确处理”的重新审查

对冻结的 20 个 bulk benchmark × 3 次重复运行执行了独立审计：`45/60` trials 完成，`15/20` datasets repeat-stable；矩阵/方法兼容性检查 60/60 通过，contrast 定义检查 51/51 通过，证据引用和 artifact hash 检查全部通过。剩余 15 个失败 trial 主要是 guardrail 阻止了可疑输入、极小样本的异常 DEG，或历史运行的设计异常，不能全部解释为 Agent 给出了错误生物学结果。

因此，GSE270703、GSE308674 应优先归为“安全检查正确阻止”；GSE302944 应归为“DEG 主流程完成、transcript-level GSEA 注释未覆盖”；GSE315678 应归为“冻结历史运行异常，需当前代码复核”；GSE317978 才是明显需要人工确认且结果不可信的极小样本案例。其余 15 个 benchmark accession 的正常 bulk 流程在本实验中完成，但“流程完成”仍不等于已经复现各自论文的主结论。

当前最适合与 Bo 讨论的顺序是：

1. 先确认 GSE317978 的 contrast 方向、raw counts 和 pooled biological unit。
2. 修复 GSE270703 的 tar 列识别、GSE315678 的 design gate，以及 GSE302944 的 transcript-to-gene 映射。
3. 将 GSE279359 定为“分析层级不一致导致表达复现失败”的主案例，将 GSE282641 定为“多因素设计未覆盖”的主案例。
4. 建立一个真实 proteomics benchmark、一个 microarray benchmark 和一个具有 biological replicates 的 scRNA benchmark。

20×3 bulk stability experiment 的总体结果是 45/60 trials 通过、15/20 datasets repeat-stable。当前 pipeline 仍处于可复核开发阶段，不能标记为已经 finalized。

## 证据文件

- [机器可读证据](<E:/agent/mwangLab/docs/reviews/paper_discrepancy_evidence_20260909.json>)
- [离线重数脚本](<E:/agent/mwangLab/test/reports/audit_paper_discrepancies.py>)
- [GSE279359 三时间点运行决策](<E:/agent/mwangLab/output/agentA_cohort_rerun_0622/cohort_analysis/GSE279359/decisions.json>)
- [GSE282641 原始决策](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE282641/GSE282641/decisions.json>)
- [Kang pseudobulk summary](<E:/agent/mwangLab/output/scrna_demo_kang/scrna_pseudobulk_summary.csv>)
- [Proteomics validation script](<E:/agent/mwangLab/test/validation/validate_proteomics_e2e.py>)

## 可直接查看的数据证据

以下文件是 Agent 实际生成的结果表，可用于重新计算显著基因数、相关性、富集方向和样本覆盖率：

- **GSE279359：** [立即时间点 DESeq2](<E:/agent/mwangLab/output/agentA_cohort_rerun_0622/cohort_analysis/GSE279359/DEG_results_immediately_post-exercise_vs_pre-exercise__deseq2.csv>)、[1 小时 DESeq2](<E:/agent/mwangLab/output/agentA_cohort_rerun_0622/cohort_analysis/GSE279359/DEG_results_1_hour_post-exercise_vs_pre-exercise__deseq2.csv>)、[24 小时 DESeq2](<E:/agent/mwangLab/output/agentA_cohort_rerun_0622/cohort_analysis/GSE279359/DEG_results_24_hours_post-exercise_vs_pre-exercise__deseq2.csv>)、[三方法比较表](<E:/agent/mwangLab/output/agentA_cohort_rerun_0622/cohort_analysis/GSE279359/DEG_results_24_hours_post-exercise_vs_pre-exercise__DA_compare.csv>)。
- **GSE282641：** [Agent GSEA 结果](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE282641/GSE282641/DEG_results_ko_vs_wt_GSEA_Hallmark.csv>)、[运行决策与设计信息](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE282641/GSE282641/decisions.json>)。
- **GSE317978：** [初步作者/Agent 比较表](<E:/agent/mwangLab/output/bo_discussion_materials_20260903/GSE317978_PRELIMINARY_COMPARISON.csv>)、[Agent 决策记录](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE317978/GSE317978/decisions.json>)。
- **Kang scRNA-seq：** [各 cell type 的 pseudobulk 汇总](<E:/agent/mwangLab/output/scrna_demo_kang/scrna_pseudobulk_summary.csv>)、[CD14+ Monocytes DEG](<E:/agent/mwangLab/output/scrna_demo_kang/CD14__Monocytes/DEG_results_stim_vs_ctrl.csv>)、[CD14+ Monocytes GSEA](<E:/agent/mwangLab/output/scrna_demo_kang/CD14__Monocytes/DEG_results_stim_vs_ctrl_GSEA_Hallmark.csv>)。
- **跨项目稳定性：** [20×3 总结表](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/summary.csv>)、[逐案例稳定性表](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/case_stability.csv>)、[完整实验报告](<E:/agent/mwangLab/output/full_pipeline_stability_20x3_20260825/large_experiment_report.md>)。

当前这些案例的主要证据是 CSV/TSV/JSON 和 workflow log；并非每个项目都已有可直接展示的 PNG。对 GSE279359、GSE282641 和 Kang scRNA，下一步可以根据上述结果表生成火山图、GSEA 条形图、方法间相关性散点图和 cell-type DEG 数量图；GSE270703、GSE315678 等失败案例应先修复输入/设计问题，再绘制生物学结论图。





## 展示图

- [GSE279359：不同方法和时间点的 DEG 数量](../../output/bo_figures_20260911/gse279359_method_comparison.png)
- [GSE282641：KO vs WT Hallmark NES](../../output/bo_figures_20260911/gse282641_gsea_nes.png)
- [GSE317978：Agent 与作者结果一致性指标](../../output/bo_figures_20260911/gse317978_agreement_metrics.png)
- [Kang scRNA：各 cell type 的 DEG 数量](../../output/bo_figures_20260911/kang_scrna_deg_by_celltype.png)
- [绘图脚本](<E:/agent/mwangLab/test/reports/generate_bo_figures.py>)

图片只展示 Agent 已有输出；它们不把失败的输入识别或未验证的比较转换成生物学结论。

