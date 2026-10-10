# BO benchmark 新结论（2026-09-23）

会议后的执行清单见 [BO_MEETING_TODO_20260923.md](BO_MEETING_TODO_20260923.md)。其中已补充 MH vs MC 的 88-gene 诊断表和 pairwise/joint-design、Kang donor-paired、Meng/Bo 沟通事项。

本结论以桌面上的 [上次 BO benchmark 结论](C:/Users/34198/Desktop/Bo_Benchmark_Report_20260911/BO_BENCHMARK_CASES_MERGED_20260910.md) 为结构参考，并加入当前版本 agent 对 Kang scRNA-seq 样例的重新分析。

## 一、结论先说

1. **当前 agent 已经能够正确完成 Kang 样例的基础 single-cell pseudobulk 流程。**  
   它使用 donor/replicate 作为生物学重复，把每个 donor × cell type × condition 的细胞计数汇总成 pseudobulk，再运行 DESeq2 和 Hallmark GSEA；没有把单个细胞错误地当作独立生物学重复。

2. **这证明的是“single-cell 数据处理和安全门控能力”，还不是 Kang 论文级别的正式复现。**  
   Kang 的核心是同一 donor 的 ctrl/stim 配对设计。当前 DESeq2 实际使用的是单因素 `~ condition`，没有把 donor 作为 blocking factor 纳入模型，因此结果可以作为工程 benchmark 和方向性检查，暂时不能直接作为最终生物学结论。

3. **当前样例的输入计数层面是合适的。**  
   `kang_2018.h5ad` 的 `.X` 是稀疏矩阵；非零值为整数，细胞行和与 `nCount_RNA` 一致，没有额外 layer 或 `raw` 对象。这支持将 `.X` 作为 raw counts 进行 pseudobulk+DESeq2。

4. **正式验收建议定为“条件通过”。**  
   工程流程通过；paired design、CD8 不平衡样本和 BO gold concordance 仍需确认后，才能把 DEG 数量和通路结果升级为正式 benchmark 结论。

5. **F 盘 ZIP bulk benchmark 的基因级结果与 BO gold 高度一致。** 统一使用 BO 的 `padj < 0.05 且 abs(log2FC) > 0.5` 阈值后，6 个 contrast 的显著集合 Jaccard 为 0.904–0.987，交集方向一致率均为 100%；此前较大的 DEG 数主要来自 Agent 汇总未应用绝对 fold-change 阈值。

## 二、最新 agent 重分析

**输入：** `data/scrna_demo/kang_2018.h5ad`  
**输出：** [`output/scrna_kang_latest_20260923/`](../../output/scrna_kang_latest_20260923/)  
**参数：**

- biological sample/donor：`replicate`
- cell type：`cell_type`
- condition：`label`
- control：`ctrl`
- treatment：`stim`
- species：Human
- DA：DESeq2
- enrichment：每个可分析 cell type 运行 MSigDB Hallmark preranked GSEA

首次从 `main.py` 命令行入口调用时，外层流式输出遇到 `KeyError: 'messages'`；这属于 CLI 状态打印层问题。随后使用同一个最新版 agent executor 直接调用，完整分析成功并写出以下结果。该入口问题应单独修复，不能与 scRNA 分析结果混为一谈。

## 三、Kang scRNA-seq 最新结果

Kang 数据包含 24,673 个细胞、15,706 个基因、8 个 donor；总体 ctrl/stim 细胞数为 12,315/12,358。显著 DEG 数为 `padj < 0.05` 的基因数；GSEA 显著标准为 FDR q < 0.25。

| Cell type | 细胞数 | pseudobulk | ctrl/stim | 显著 DEG | 显著 Hallmark | 运行状态 | 最高 NES 的通路 |
|---|---:|---:|---:|---:|---:|---|---|
| CD4 T cells | 11,238 | 16 | 8/8 | 973 | 18 | 完成 | IFN-γ 2.84；IFN-α 2.74 |
| CD14+ Monocytes | 5,697 | 16 | 8/8 | 3,428 | 27 | 完成 | IFN-γ 2.61；IFN-α 2.61 |
| B cells | 2,651 | 16 | 8/8 | 760 | 16 | 完成 | IFN-γ 2.84；IFN-α 2.77 |
| NK cells | 1,716 | 16 | 8/8 | 459 | 20 | 完成 | IFN-γ 3.02；IFN-α 2.85 |
| CD8 T cells | 1,621 | 14 | 6/8 | 164 | 25 | 完成，但 ctrl 少 2 个 donor | IFN-γ 3.25；IFN-α 3.19 |
| FCGR3A+ Monocytes | 1,089 | 16 | 8/8 | 1,162 | 24 | 完成 | IFN-γ 2.80；IFN-α 2.71 |
| Dendritic cells | 529 | 16 | 8/8 | 879 | 22 | 完成 | IFN-γ 2.69；IFN-α 2.69 |
| Megakaryocytes | 132 | 2 | 1/1 | — | — | 正确跳过 | 样本数不足 |

最新一轮的完整机器可读汇总见 [scrna_pseudobulk_summary.csv](../../output/scrna_kang_latest_20260923/scrna_pseudobulk_summary.csv)。各 cell type 的 DEG 和 GSEA 表均在对应子目录中。

### 与上次 Kang 输出的比较

新一轮与旧输出的 pseudobulk 数量、样本数和 DEG 数完全一致；Dendritic cells 的 GSEA 从上次的空值变为 **22 个显著 Hallmark 集合**。因此当前流程具有稳定性，同时修复或避免了上次 Dendritic GSEA 未完成的情况。

## 四、对 single-cell 能力的判断

### 已经可以确认的能力

- **分析单位正确：** 先按 donor × cell type × condition 汇总，避免把单细胞数当成生物学重复数。
- **分组和低样本门控正确：** Megakaryocytes 只有 1 ctrl/1 stim，agent 没有强行运行 DE。
- **GSEA 链路完整：** 7 个可分析 cell type 全部完成 Hallmark GSEA，IFN-γ/IFN-α 在各细胞类型中均排在最高 NES 附近，方向符合 IFN-β 刺激的预期。
- **输入计数兼容：** `.X` 的非零计数为整数，且行和对应 `nCount_RNA`，适合当前 raw-count pseudobulk 路由。
- **结果可追溯：** 输出包含 pseudobulk count、pseudobulk metadata、DEG、GSEA、`decisions.json` 和 `evidence.json`。

### 尚不能宣称的能力

- **没有拟合 donor-paired design。** 当前调用的是 `~ condition`，不是 `~ donor + condition`；同一 donor 的配对信息只体现在 pseudobulk 样本名和 metadata 中，没有进入 DESeq2 模型。
- **没有做 cell-level QC、doublet 检测、聚类或细胞类型注释。** 这些标签直接使用 H5AD 中已提供的 `cell_type`；因此测试的是“已注释 scRNA 数据的 pseudobulk DA”，不是从原始单细胞数据独立完成完整 scRNA pipeline。
- **CD8 T cells 的 donor 覆盖不平衡。** `patient_107` 和 `patient_1039` 的 ctrl 细胞数分别为 8 和 9，低于 min_cells=10，被丢弃；stim 仍保留，最终是 6 ctrl/8 stim。
- **显著 DEG 数不能直接与论文数字比较。** 需要先冻结 donor-paired 模型、过滤、阈值、基因 ID 和 BO reference，再比较 logFC correlation、方向一致率、显著集合 overlap 和 GSEA NES。

## 五、需要 Bo 讨论并冻结的事项

| 事项 | 需要 Bo 确认的内容 |
|---|---|
| 正式统计模型 | Kang benchmark 是否必须使用 `~ donor + condition` 的 paired/blocking design？是否允许当前 `~ condition` 作为 smoke test？ |
| CD8 不平衡 | 6/8 ctrl、8/8 stim 是否可以作为正式结果？还是要求只保留成对 donor，或降低/修改 min_cells？ |
| 输入层 | 确认 `.X` 作为 raw counts 是 BO gold 的指定输入；如果 gold 使用其他 layer，需要冻结 layer 名称。 |
| 细胞类型标签 | benchmark 是否接受 H5AD 已提供的 `cell_type`，还是要求 agent 自己完成 annotation/QC？ |
| gold 结果 | 提供正式 DEG/GSEA reference、contrast 方向、阈值和 annotation 版本；否则只能判断流程是否完成，不能评定生物学复现度。 |
| 重复稳定性 | 是否要求 paired model 修复后重复运行 3 次，并报告 DEG/GSEA 稳定性？ |
| CLI 问题 | 修复 `main.py` 的 `KeyError: 'messages'` 状态打印问题，再把命令行端到端运行纳入验收。 |

## 六、审计记录

对本次输出运行了 evaluate-bioinformatics-agent 的离线审计：

- Observed score：**78.9/100**
- Evidence coverage：**20.7%**
- Verdict：**insufficient_evidence**
- Blocking findings：无

这个分数不能解释为“scRNA 结果只有 78.9 分”。审计未找到 `run_status.json`、root `summary.csv`、调用/耗时计数和重复稳定性摘要，因此执行、效率和科学有效性维度大多是 **not measured**；证据引用和 decision grounding 通过。审计文件见 [agent_evaluation.md](../../output/scrna_kang_latest_20260923/agent_evaluation.md)，运行决策见 [decisions.json](../../output/scrna_kang_latest_20260923/decisions.json)，证据包见 [evidence.json](../../output/scrna_kang_latest_20260923/evidence.json)。

## 七、最终判断

**对于 BO 想验证的“agent 能否正确处理 single-cell 数据”这一工程问题：本轮可以判定为通过。** Agent 使用正确的 pseudobulk 分析单位，能完成主要 cell types 的 DESeq2 和 GSEA，并对极小样本 cell type fail closed。

**对于“agent 是否已经复现 Kang 的正式 paired single-cell 结论”这一科学问题：当前只能判定为条件通过。** 在 donor blocking/paired model、CD8 donor 覆盖和 BO gold reference 冻结前，不能把当前 DEG 数和 GSEA 结果作为最终论文复现结论。



## 八、F 盘 RNA-seq ZIP 金标准 benchmark：逐案例比较

这一部分只使用冻结 ZIP 中的 BO 结果作为 gold，不纳入远程 GEO。BO 的 DEG 文件采用 `padj < 0.05` 且 `|log2FC| > 0.5`；Agent 的汇总表 `n_deg` 只按 `padj < 0.05` 统计。下面同时报告 Agent 原始汇总数和在 BO 阈值下重算的公平比较数。

### 总体基因级 concordance

| Case | BO gold DEG | Agent 汇总 DEG（仅 padj） | Agent 公平 DEG（padj + abs(log2FC)>0.5） | overlap | Jaccard | logFC Pearson | 结论 |
|---|---:|---:|---:|---:|---:|---:|---|
| GSE194151 FC vs MC | 6,847 | 10,776 | 6,808 | 6,781 | 0.9865 | 0.984 | 基本复现；汇总阈值不一致 |
| GSE194151 FH vs FC | 330 | 1,617 | 328 | 326 | 0.9819 | 1.000 | 基本复现；汇总阈值不一致 |
| GSE194151 FH vs MH | 7,092 | 11,035 | 7,011 | 6,992 | 0.9833 | 0.997 | 基本复现；汇总阈值不一致 |
| GSE194151 MH vs MC | 92 | 274 | 88 | 88 | 0.9565 | 0.790 | 方向一致，低 DEG 数导致相关性不稳定 |
| GSE195482 WMF vs WCF | 1,360 | 1,379 | 1,379 | 1,305 | 0.9100 | 1.000 | 基因级高度一致 |
| GSE195482 WMM vs WCM | 131 | 128 | 128 | 123 | 0.9044 | 1.000 | 基因级高度一致 |

`overlap/Jaccard/logFC Pearson` 是在 BO gold 的显著基因集合和 Agent 同一基因 ID 上重算的；不是把远程 GEO 输出当作 gold。GSEA 方面，BO ZIP 使用 KEGG/custom pathway，Agent 使用 MSigDB Hallmark，因此下列通路比较以方向和生物主题为主，不把 pathway 名称逐项相同作为硬性标准。

### GSE194151 FC vs MC：健康雌雄差异

**BO 正确结论：** FC 与 MC 的差异非常广泛。BO gold 有 6,847 个 DEG，其中 2,414 个上调、4,433 个下调；正向富集集中在呼吸链复合体 I/V（CI subunits、Complex V、CV subunits），负向富集集中在 complement/coagulation、血浆脂蛋白重塑和 steroid hormone biosynthesis。

**Agent 结论：** Agent 原始汇总报告 10,776 个 `padj < 0.05` 基因、33 个 Hallmark；在 BO 相同阈值下为 6,808 个 DEG。Hallmark 结果同样显示 oxidative phosphorylation 正向、coagulation 负向。

**差异与判断：** 公平阈值下与 BO gold 重叠 6,781 个，Jaccard 0.9865，logFC Pearson 0.984，方向一致率为 100%。Agent 的 10,776 不是生物学结果冲突，而是多报了低于 `|log2FC| > 0.5` 的显著基因。该案例可判定为**基因级和方向级复现**；需要修正报告层的 DEG 统计口径。

证据：[BO DEG](../../_rnaseq_benchmark_input/GSE194151/FC_vs_MC.DEGs_logfc0.5_padj0.05.txt)、[BO GSEA](../../_rnaseq_benchmark_input/GSE194151/FC_vs_MC.kegg.gsea.out)、[Agent DEG](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE194151_FC_vs_MC/GSE194151/DEG_results_FC_vs_MC.csv)、[Agent GSEA](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE194151_FC_vs_MC/GSE194151/DEG_results_FC_vs_MC_GSEA_Hallmark.csv)。

### GSE194151 FH vs FC：雌性 HFpEF 与雌性对照

**BO 正确结论：** 这是相对较小但明确的疾病相关 contrast。BO gold 有 330 个 DEG，其中 184 个上调、146 个下调；上调通路包括 G2/M cell-cycle events、ECM proteoglycans 和 ECM-receptor interaction，下调包括 capped-intron pre-mRNA processing 和 mRNA splicing。

**Agent 结论：** Agent 原始汇总为 1,617 个 `padj < 0.05` 基因、46 个 Hallmark；统一阈值后为 328 个 DEG。Hallmark 方向显示 EMT、mitotic spindle、adipogenesis 正向，cholesterol homeostasis、DNA repair 和 MYC targets 负向。

**差异与判断：** 公平阈值下重叠 326 个，Jaccard 0.9819，logFC Pearson 1.000，方向一致率为 100%。Agent 的基因级结论与 BO gold 基本相同；Hallmark 与 BO 的 ECM/cell-cycle 主题不完全同名，但没有证据表明主方向相反。该案例判定为**通过**，唯一明显问题仍是 Agent 汇总没有应用 BO 的绝对 fold-change 阈值。

证据：[BO DEG](../../_rnaseq_benchmark_input/GSE194151/FH_vs_FC.DEGs_logfc0.5_padj0.05.txt)、[BO GSEA](../../_rnaseq_benchmark_input/GSE194151/FH_vs_FC.kegg.gsea.out)、[Agent DEG](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE194151_FH_vs_FC/GSE194151/DEG_results_FH_vs_FC.csv)、[Agent GSEA](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE194151_FH_vs_FC/GSE194151/DEG_results_FH_vs_FC_GSEA_Hallmark.csv)。

### GSE194151 FH vs MH：HFpEF 状态下的雌雄差异

**BO 正确结论：** BO gold 有 7,092 个 DEG，其中 2,691 个上调、4,401 个下调；上调包括 respiratory-chain CI、CV 和 voltage-gated potassium channels，下调包括 complement/coagulation、steroid hormone biosynthesis 和 retinol metabolism。

**Agent 结论：** Agent 原始汇总为 11,035 个 `padj < 0.05` 基因、37 个 Hallmark；统一阈值后为 7,011 个 DEG。Hallmark 同样给出 oxidative phosphorylation、myogenesis 和 EMT 正向，xenobiotic/bile-acid metabolism 和 coagulation 负向。

**差异与判断：** 公平阈值下重叠 6,992 个，Jaccard 0.9833，logFC Pearson 0.997，方向一致率为 100%。因此 Agent 不是把 sex contrast 误判成完全不同的 treatment contrast；它复现了 BO gold 的主要基因方向。该案例可判定为**通过**，但应把 11,035 改写为统一阈值下的 7,011 再对外报告。

证据：[BO DEG](../../_rnaseq_benchmark_input/GSE194151/FH_vs_MH.DEGs_logfc0.5_padj0.05.txt)、[BO GSEA](../../_rnaseq_benchmark_input/GSE194151/FH_vs_MH.kegg.gsea.out)、[Agent DEG](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE194151_FH_vs_MH/GSE194151/DEG_results_FH_vs_MH.csv)、[Agent GSEA](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE194151_FH_vs_MH/GSE194151/DEG_results_FH_vs_MH_GSEA_Hallmark.csv)。

### GSE194151 MH vs MC：雄性 HFpEF 与雄性对照

**BO 正确结论：** 这是 GSE194151 中最小的疾病 contrast。BO gold 只有 92 个 DEG，其中 22 个上调、70 个下调；正向主题是 fatty-acid oxidation、mitochondrial fatty-acid beta-oxidation 和 peroxisomal protein import，负向主题包括 matrix-metalloproteinase activation 和 ECM degradation。

**Agent 结论：** Agent 原始汇总为 274 个 `padj < 0.05` 基因、26 个 Hallmark；统一阈值后为 88 个 DEG。Hallmark 结果的正向主题为 fatty-acid metabolism、adipogenesis 和 oxidative phosphorylation，负向主题主要为 allograft rejection 和 MYC targets。

**差异与判断：** 公平阈值下重叠 88 个，Jaccard 0.9565，方向一致率 100%；Pearson 为 0.790，主要因为 gold 只有 92 个基因，相关性容易受少数基因影响。Agent 捕获了 BO 的脂肪酸氧化/线粒体方向，但 GSEA 的负向主题没有直接复现 ECM/MMP 术语。该案例判定为**基因方向通过、通路解释部分一致**。

证据：[BO DEG](../../_rnaseq_benchmark_input/GSE194151/MH_vs_MC.DEGs_logfc0.5_padj0.05.txt)、[BO GSEA](../../_rnaseq_benchmark_input/GSE194151/MH_vs_MC.kegg.gsea.out)、[Agent DEG](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE194151_MH_vs_MC/GSE194151/DEG_results_MH_vs_MC.csv)、[Agent GSEA](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE194151_MH_vs_MC/GSE194151/DEG_results_MH_vs_MC_GSEA_Hallmark.csv)。

### GSE195482 WMF vs WCF：雌性 HFpEF 与雌性 WT

**BO 正确结论：** BO gold 有 1,360 个 DEG，其中 931 个上调、429 个下调；上调主要是 immune/hematopoietic/cell-adhesion 相关，负向最强的是 mitochondrial translation、aerobic respiration 和 mitochondrial ribosome，表示 HFpEF 中线粒体呼吸程序下降。

**Agent 结论：** Agent 报告 1,379 个 DEG、42 个 Hallmark；由于这个 contrast 的结果几乎都满足绝对 fold-change 阈值，公平重算仍为 1,379。Hallmark 显示 IFN-γ、IFN-α 和 allograft rejection 正向，oxidative phosphorylation、MYC targets 和 fatty-acid metabolism 负向。

**差异与判断：** 与 BO gold 重叠 1,305 个，Jaccard 0.9100，logFC Pearson 1.000。两边的正向免疫主题和负向线粒体主题一致；Hallmark 的 IFN 术语与 BO 的 immune/hematopoietic 术语不同，但方向一致。该案例判定为**基因级和主要生物学方向通过**。

证据：[BO DEG](../../_rnaseq_benchmark_input/GSE195482/WMF_vs_WCF.DEGs_logfc0.5_padj0.05.txt)、[BO GSEA](../../_rnaseq_benchmark_input/GSE195482/WMF_vs_WCF.kegg.gsea.out)、[Agent DEG](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE195482_WMF_vs_WCF/GSE195482/DEG_results_WMF_vs_WCF.csv)、[Agent GSEA](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE195482_WMF_vs_WCF/GSE195482/DEG_results_WMF_vs_WCF_GSEA_Hallmark.csv)。

### GSE195482 WMM vs WCM：雄性 HFpEF 与雄性 WT

**BO 正确结论：** BO gold 有 131 个 DEG，其中 86 个上调、45 个下调；上调主题包括 cornified envelope、keratinization 和 complement triggering，下调主题包括 vascular smooth-muscle contraction 和 epigenetic regulation of gene expression。

**Agent 结论：** Agent 报告 128 个 DEG、37 个 Hallmark；统一阈值后仍为 128 个。Hallmark 正向为 mTORC1、androgen response 和 allograft rejection，负向为 myogenesis、mitotic spindle 和 WNT/β-catenin signaling。

**差异与判断：** 与 BO gold 重叠 123 个，Jaccard 0.9044，logFC Pearson 1.000。基因级结果高度一致，但 Hallmark 与 BO 的 cornification/vascular smooth-muscle 术语对应较弱，因此不能声称通路层面完全复现。该案例判定为**基因级通过、通路层面需要谨慎解释**。

证据：[BO DEG](../../_rnaseq_benchmark_input/GSE195482/WMM_vs_WCM.DEGs_logfc0.5_padj0.05.txt)、[BO GSEA](../../_rnaseq_benchmark_input/GSE195482/WMM_vs_WCM.kegg.gsea.out)、[Agent DEG](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE195482_WMM_vs_WCM/GSE195482/DEG_results_WMM_vs_WCM.csv)、[Agent GSEA](../../output/rnaseq_zip_remote_ab/output_local/cohort_GSE195482_WMM_vs_WCM/GSE195482/DEG_results_WMM_vs_WCM_GSEA_Hallmark.csv)。

### ZIP benchmark 的整体判断

- 6 个案例的**基因级方向和效应量与 BO gold 高度一致**；公平阈值下 Jaccard 为 0.904–0.987，显著交集的方向一致率均为 100%。
- GSE194151 FC vs MC、FH vs MH 的 Agent 原始 DEG 数偏大，原因是汇总表没有应用 BO 的 `|log2FC| > 0.5` 过滤，不是结果本身与 gold 冲突。
- GSE194151 MH vs MC 的 DEG 数较少，logFC Pearson 只有 0.790，但集合方向完全一致，不能只用 Pearson 将其判为失败。
- GSE195482 两个 contrast 的 gene-level concordance 很高；WMF vs WCF 的免疫上调/线粒体下调方向最清楚，WMM vs WCM 的 pathway terminology 差异较大。
- GSEA 不能做名称级一对一比较，因为 BO 使用 KEGG/custom pathway，Agent 使用 Hallmark；正式验收应增加统一数据库下的 NES correlation 和 pathway overlap。

详细运行记录见 [ZIP benchmark 原始报告](../../test/experiments/rnaseq_zip_remote_ab/REPORT.md)、[manifest](../../output/rnaseq_zip_remote_ab/manifest.json)、[comparison.csv](../../output/rnaseq_zip_remote_ab/comparison.csv) 和 [本地输出目录](../../output/rnaseq_zip_remote_ab/output_local/)。

## 九、合并后的结论

- **Bulk RNA-seq ZIP benchmark：基因级通过，整体条件通过。** Agent 已正确处理矩阵语义、样本对齐和 DESeq2；6 个案例的 gene-level 结果与 BO gold 高度一致。
- **需要修复的是报告口径和通路验收，而不是重新解释为普遍性分析失败。** 报告层应统一 `padj + |log2FC|` 阈值；正式 pathway benchmark 应统一数据库或使用 gold 的 pathway 集合重新计算。
- **Kang scRNA-seq：工程流程通过，正式 paired 生物学复现条件通过。** donor blocking model 尚未纳入，因此不能把当前 scRNA 结果直接当作最终论文复现。

