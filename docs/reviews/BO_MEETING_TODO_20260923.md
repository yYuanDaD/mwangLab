# Bo 会议后续 TODO（2026-09-23）

这份清单把会议后的问题拆成可验收的分析、代码和沟通任务。F 盘 ZIP 只作为冻结 gold/reference；后续复跑由 agent 使用自己的 Python 方法完成，不执行 BO 的 R 脚本。

## 已完成的跟进

- [x] **MH vs MC 的低 Pearson 定位**：全体 92 个 BO 显著基因上的 logFC Pearson 为 0.7898，但 88 个共同显著基因上的 Pearson 为 1.0000、Spearman 为 1.0000、方向一致率为 100%。差异几乎全部来自 4 个极端稀疏基因：`Try4`、`Ctrb1`、`Cpa1`、`Prss2`（均为胰腺消化酶相关基因，表达主要由单个样本贡献）。诊断表见 [mh_vs_mc_88_gene_diagnostic.csv](../../output/rnaseq_zip_remote_ab/mh_vs_mc_88_gene_diagnostic.csv)。
- [x] **阈值口径核对**：BO 使用 `padj < 0.05 且 |log2FC| > 0.5`；旧 Agent 汇总的 `n_deg` 只使用 `padj < 0.05`。六个 bulk contrast 的公平 Jaccard 为 0.904–0.987，之前的大 DEG 数主要是报告口径差异。
- [x] **BO 与 agent 实现差异初步记录**：BO 是逐 contrast 的 R/DESeq2、先 `round()` estimated counts、`~ Group`；agent 是 Python/PyDESeq2，带矩阵语义、样本对齐、科学门控和证据记录，GSEA 使用 MSigDB Hallmark。BO 脚本只作为冻结 reference，不作为 agent 的运行方法。
- [x] **运行完整性审计**：Kang run `score=78.9, coverage=20.7%`，因覆盖不足只能判 `insufficient_evidence`；F 盘 MH vs MC run `score=99.3, coverage=89.1%`，无 blocking finding。

## P0：先冻结 benchmark 口径

- [ ] **统一结果表字段**：同时报告 `n_padj05`、`n_padj05_lfc05`、全 tested genes 的 Pearson/Spearman、显著集合 Jaccard、方向一致率；避免把两个 DEG 阈值混成一个数字。
  - 验收：每个 contrast 的报告都能复算，低 DEG 案例不能只用 Pearson 判失败。
- [ ] **确认 4 个极端基因的处理原则**：保留原始结果并标注“单样本稀疏/高杠杆”，同时给出排除这 4 个基因后的敏感性分析；不直接删除基因或修改 gold。
  - 验收：主结果、敏感性结果和排除理由都写入 comparison artifact。

## P1：pairwise 与 joint design 两种 agent 分析

- [ ] **Pairwise 分析**：agent 用 PyDESeq2 独立重跑冻结的 pairwise inputs。GSE194151 至少覆盖 `FH-FC`、`MH-MC`、`FC-MC`、`FH-MH`，并记录是否扩展到其余两组组合；GSE195482 覆盖两个性别内的 HFpEF-vs-chow contrast。
- [ ] **All-groups joint 分析**：把同一 accession 的所有组放进一个模型，不把 BO 的逐对脚本当作实现。优先使用 2×2 因子设计：
  - GSE194151：`Sex × Disease`，主效应为 sex/disease，交互项为 `(FH-FC) - (MH-MC)`。
  - GSE195482：按 metadata 冻结的 sex/status 因子定义对应的 2×2 模型；若 cell 不满或设计不满秩则明确 fail closed。
- [ ] **比较两种分析**：对每个可比 contrast 输出 logFC Pearson/Spearman、方向一致率、显著集合 overlap/Jaccard、GSEA NES 相关性和 DEG fraction sanity。
  - 验收：保存模型公式、reference level、样本数、矩阵取整/转换方式、失败原因和全部 CSV；报告清楚区分“pairwise estimand”和“joint-model estimand”。

## P1：Kang scRNA-seq donor 配对复现

- [ ] 将当前 `~ condition` smoke test 改为 donor blocking/paired model（目标形式 `~ donor + condition`，或等价的成对 donor-level pseudobulk 检验），按每个 cell type 单独分析。
- [ ] 冻结 donor 覆盖规则：优先只保留 ctrl/stim 都有合格细胞的 donor；对 CD8 的 6/8 ctrl、8/8 stim 不平衡单独报告；Megakaryocytes 的 1 vs 1 继续 fail closed。
- [ ] 用论文/BO reference 对比每个 cell type 的 logFC、方向、DEG、GSEA，并重新跑独立审计。目标是把 coverage 从 20.7% 提高到可判定范围，而不是只增加 prose。

## P1：向 Meng 确认 single-cell DE 的统计单位

- [x] 已向 Meng Wang（`mwmeng@med.umich.edu`）询问：差异表达应按每个 cell type 分析，还是所有细胞混合后分析？是否需要同时报告 cell-composition change？
- [ ] 建议问题表述：主分析是否采用“每个 cell type 内按 donor 聚合的 pseudobulk/paired model”；全细胞 pooled 结果是否只作为总体状态的补充分析。
- [ ] 把 Meng 的回答记录到 benchmark protocol，冻结后再跑正式 Kang 结果。

## P1：把 BO 结论和 Kang 原文发给 Bo

- [x] 已发送给 Bo：Kang 原文链接（PMID 29227470 / DOI 10.1038/nbt.4042 / PMC5784859）、GSE96583、当前结论、donor-paired 限制和 pairwise/joint 方案。
- [x] 已附上 [BO benchmark 结论](BO_BENCHMARK_CONCLUSION_20260923.md)；邮件主题为 `Kang 2018 paper and RNA-seq benchmark follow-up`。88-gene diagnostic 已保存在仓库并在邮件正文中说明。

## P2：扩展到蛋白组学和表观组学

- [ ] 分别问 Bo/Meng：已有数据类型、最小样本数、是否有 feature annotation、是否需要 paired donor/批次/多因素设计，以及期望输出是差异 feature、通路还是整合结论。
- [ ] 先做 modality feasibility audit，不直接把 RNA-seq 的 DESeq2 规则迁移过去：
  - 蛋白组学：protein/peptide level、缺失值、batch、log-intensity、limma/linear-model 路线。
  - 甲基化/表观组学：β/M value、probe/peak/region level、质量控制、批次和适合的线性模型。
- [ ] 验收：每种 modality 有一份最小输入 schema、推荐方法、禁止的错误路由、一个小型 frozen test case 和成本估计。

## 建议顺序

1. 完成 P0 的阈值和异常基因敏感性报告。
2. 冻结 Meng 对 single-cell 统计单位的回答，同时实现 Kang donor-paired 分析。
3. 在 agent 自己的方法下跑 pairwise 与 joint 2×2 两套 bulk 分析。
4. 将论文、结论、诊断表和 TODO 发给 Bo。
5. 根据反馈设计蛋白组学/表观组学 feasibility test。
