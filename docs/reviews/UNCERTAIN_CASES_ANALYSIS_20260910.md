# 不确定案例离线分析报告（2026-09-10）

本报告只分析仓库已有的 `data/` 和 `output/`，没有重新调用模型或下载数据。重点是判断哪些结果可以相信、哪些结果必须先复核。

## 结论排序

1. **GSE317978 是最重要的复核案例。** Agent 与作者结果的数量差异很大，而且 fold-change 方向标签存在不确定性。
2. **GSE270703 是数据类型识别问题，不是生物学阴性结果。** 当前矩阵含负值，却被识别成整数型 log/normalized matrix，任何 DA 结果都不能使用。
3. **GSE302944 的 DEG 可以作为初步结果，但 GSEA 不能使用。** 输入是 transcript-level IDs，不能直接和 gene-symbol Hallmark 集合匹配。
4. **GSE315678 暴露了一个可复现的 metadata/design bug。** 26/26 样本已对齐、分组值也存在，但 design gate 仍报告组别缺失。
5. **Kang scRNA 和 PXD025560 proteomics 只证明流程能跑，不能证明生物学结论。**

## 1. GSE317978：数量差异 + contrast orientation 未决

数据：[GEO GSE317978](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE317978)。本地 metadata 记录的是小鼠胰岛、`flox/flox` 对 `BcBKO`、chow diet；目前仓库没有一份经过核对的原论文正文或 Bo 的分析脚本，因此不能可靠地补写论文主结论。该项目应先取得论文链接和作者代码，再做三方比较。

输入的 `GSE317978_core_table3.csv.gz` 有 17,549 行，其中作者差异结果列有 17,061 个非空值。Agent 输出保留 17,043 行，得到 11,339 个 `padj < 0.05`，占 66.5%；每组只有 2 个表达样本，而且每个样本本身是至少三只小鼠 islet 的 pooled sample。

与作者列逐行对齐（共同 17,013 行）后：

| 比较 | 结果 |
|---|---:|
| Agent log2FC vs 作者列的 Pearson | 0.665 |
| Agent log2FC vs 作者列的 Spearman | 0.789 |
| 共同行同号率 | 73.9% |
| Agent 显著集合 | 11,339 |
| 作者 q<0.05 集合 | 4,411 |
| q<0.05 集合交集 / Jaccard | 3,686 / 0.306 |
| 同时加 |log2FC|>1 的集合交集 / Jaccard | 205 / 0.137 |

但是作者列名是 `diffexp_log2fc_CTR_PBS-vs-KO_PBS`，Agent 文件名和模型对比是 `KO_PBS_vs_CTR_PBS`。如果机械地把作者列乘以 −1，相关性变为 −0.789，同号率降到 25.7%。因此目前不能说 Agent 与作者方向相反，也不能说方向一致。必须读取 Bo/作者脚本确认该列的实际定义，列名本身不足以确定方向。

另外，作者结果的统计单位、输入矩阵和 Agent 不完全相同：Agent 对 FPKM 进行了 `log2(x+1)` 后用 limma；作者提供的是 DESeq2 结果列；Agent 每组 n=2。当前 66.5% 显著比例已经触发 `implausible_sig_fraction` 和 `tiny_n_per_group`，所以 Agent 结果应标记为 **blocked / not trustworthy**，不能拿来支持论文结论。

**需要 Bo 先确认：**作者列的 contrast 正负方向；是否有 raw counts；pool 是否是 biological replicate；作者使用的 filter、normalization、design 和 q-value 阈值。

## 2. GSE270703：矩阵物理含义未确定

数据：[GEO GSE270703](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE270703)。原研究的主要结论是：结合有氧和抗阻训练会改变年轻成人骨骼肌的空间转录组；作者按肌纤维类型观察到运动诱导的表达变化，并报告间质细胞群变化与血管生成相关。原论文记录为 [PMID40894879](https://pubmed.ncbi.nlm.nih.gov/40894879/)。原研究使用的是 10x Visium spatial transcriptomics，10 个样本（5 名年轻供体的 sedentary/exercised 配对样本），所以当前把合并 tar 后的矩阵当普通 bulk 表达矩阵并运行 limma，不能检验论文的空间和细胞类型结论。

`GSE270703_merged_from_tar.csv` 为 4,992 features × 10 samples。数值范围是 **−1,501 到 23,373**，100% 整数型。它被 pipeline 分类为 `log_transformed`，但 limma policy 因 raw-count-like 特征而阻止分析。

这里不应简单把它改成 DESeq2：负的“counts”不可能是原始 read counts。更可能的情况是 tar 中取错了列、样本文件包含某种 signed/normalized quantity，或者合并逻辑把 annotation/统计列当成表达值。

**结论：**没有可用的 DEG；不能把这个案例描述成 exercise 对表达没有影响。应回到 `_unpacked` 的单样本文件，确认真正的 count/abundance 列和原始文件表头，再决定 DESeq2、limma 或跳过。

## 3. GSE302944：DEG 可运行，GSEA 不能解释

数据：[GEO GSE302944](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE302944)。该研究对应 C/EBPα 脂肪组织特异性敲除（Cebpa_ASKO）小鼠的 adipose RNA-seq。原论文结论包括：Cebpa_ASKO 小鼠的 gWAT 发育受损、在高脂饮食挑战下不能正常扩增脂肪库；iWAT 形态仍可形成，但脂肪细胞功能和脂质代谢/分化相关转录程序发生改变。可参考[原论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12330668/)。Agent 的 201 个 transcript-level DEG 只能部分触及这些分子变化，不能因为 GSEA 失败就判断脂肪代谢通路没有变化。

输入是 118,489 行 × 6 个样本，数值范围 0–56,329.4，只有约 43.3% 的值是整数型；pipeline 识别为 FPKM/TPM，运行 `log2(x+1) + limma`，得到 201 个 `padj<0.05` feature。

GSEA 失败的直接原因很清楚：排序 ID 是类似 `ENSMUST00000223520.1` 的 mouse transcript IDs，而 Hallmark 使用 gene symbols，overlap 为零。日志明确显示“first 5 genes”都是 transcript IDs。

**结论：**201 个 transcript-level DEG 只能算初步、未完成注释的结果；不能报告 Hallmark pathway。需要固定 Ensembl release，做 transcript→gene 汇总/映射，再重新决定是在 transcript 还是 gene level 做 DA 和 GSEA。

## 4. GSE315678：已对齐但设计 gate 失败

数据：[GEO GSE315678](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE315678)。metadata 的原始处理说明写明使用 Salmon，并已将 transcript estimates 汇总到 gene level（GENCODE M30 / mm39）；这是 Bo 复核时必须保留的输入信息。当前本地没有可核对的原论文全文，因此这里只能确认数据处理背景，不能把 Agent 失败解释成论文结论。

输入是 Salmon quant 文件，26 个样本，metadata 中明确有 `Control chow diet` 和 `CDAHFD`，各 13 个样本。pipeline 记录了 26/26 substring alignment，之后 limma 再次 exact alignment 26/26；但 policy 仍报告两个 group unavailable。

日志同时打印了 available values 正是 `['Control chow diet', 'CDAHFD']`。这说明不是论文设计不清楚，而是 metadata 在二次对齐/索引重建后，设计值检查存在实现问题。该案例不应被归类为“没有 contrast”。

**建议：**先做一个最小复现测试，直接用保存的 `GSE315678_metadata_aligned.csv` 和 log2 矩阵调用 `select_valid_two_group_design()`；检查 pandas dtype、index rename、sample column 的字符串/整数转换。修复后再运行 limma，并与作者 Salmon/tximeta gene-level 方法比较。

## 5. Kang scRNA-seq：一个 cell type 明显不具备 DA 条件

数据：[GEO GSE96583](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE96583)，本地对象是 `kang_2018.h5ad`。原论文是 Kang 等人的 [Nature Biotechnology 研究](https://doi.org/10.1038/nbt.4042)，研究 8 名 lupus donor 的 PBMC，在 IFN-β 刺激 6 小时前后比较不同免疫细胞类型的转录反应；原始设计是 donor-paired，而不是把每个 cell 当成独立 biological replicate。当前 pseudobulk 结果应按 donor 配对重新确认，Megakaryocytes 的 1 vs 1 已经不能形成可靠 DA。

7 个 cell types 完成 pseudobulk；多数 cell type 有 6–8 个 control 和 6–8 个 treatment biological samples。但 Megakaryocytes 只有 **1 vs 1** pseudobulk sample，因此被正确标记为 `skipped_too_few_samples`。

其余 cell types 的 DEG 数量（例如 CD14+ Monocytes 3,428 个）不能单独视为正确或错误，因为还没有 Bo/论文 gold result，也没有在本报告中检查 cell-type annotation、donor pairing 和 covariates。

## 6. PXD025560 proteomics：没有生物学结论

数据：[PRIDE PXD025560](https://www.ebi.ac.uk/pride/archive/projects/PXD025560)。当前验证没有使用原论文的 case/control 设计，而是任意前半/后半分组，因此不应引用任何原论文生物学结论来解释这次 limma 输出。需要 Bo 提供真实分组、批次和完整 protein-level gold table 后再比较。

真实 DIA-LFQ 数据完成了 labeling、missing-value imputation、log2 transform 和 limma，但测试脚本明确使用样本前半/后半的**任意分组**。它只能证明 proteomics plumbing 可运行，不能证明差异蛋白、通路或方向正确。该数据不适合作为 Bo benchmark，除非重新获得真实 case/control metadata。

## 建议的复核顺序

- **第一轮和 Bo 一起确认：** GSE317978 contrast orientation、raw counts 和 pooled biological unit。
- **第二轮修 pipeline：** GSE270703 tar 列识别、GSE315678 design gate、GSE302944 transcript-to-gene mapping。
- **第三轮建立真实 benchmark：** 一个 Bo 已分析的 proteomics 项目、一个真实 microarray 项目、一个有 biological replicates 的 scRNA 项目。
- **验收时禁止：** 用 failed GSEA 推导通路阴性结论，用 n=1 vs n=1 pseudobulk 推导 cell-type 结论，用任意蛋白组分组作为生物学 benchmark。

20×3 bulk stability experiment 的总体结果是 45/60 trials 通过、15/20 datasets repeat-stable；因此当前 pipeline 仍属于“可复核开发阶段”，不能标记为 finalized。

## 输入证据

- [GSE317978 decisions.json](../../output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE317978/GSE317978/decisions.json)
- [GSE270703 workflow.log](../../output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE270703/workflow.log)
- [GSE302944 workflow.log](../../output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE302944/workflow.log)
- [GSE315678 workflow.log](../../output/full_pipeline_stability_20x3_20260825/repeat_01/runs/cohort_GSE315678/workflow.log)
- [Kang pseudobulk summary](../../output/scrna_demo_kang/scrna_pseudobulk_summary.csv)
- [Proteomics validation script](../../test/validation/validate_proteomics_e2e.py)
- [20×3 stability report](../../output/full_pipeline_stability_20x3_20260825/large_experiment_report.md)
