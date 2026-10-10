# mwangLab 近期工作交接给 Claude

更新时间：2026-10-09

仓库：`E:/agent/mwangLab`

当前分支：`main`

当前提交：`ed706f0`（本地 `main` 与 `origin/main` 已同步）

这份交接总结覆盖 2026-09-18 至 2026-10-09 的主线实现和已有实验产物。`data/`、`output/`、`archive/` 等运行数据不在 Git 提交中；需要复核实验时请直接使用本机路径，并以每个 run 的 `run_status.json`、`evidence.json`、`integrity_report.json` 和最终报告为准。

## 先读哪些文件

1. `AGENTS.md`：项目架构、工具边界、矩阵与方法政策、历史工程决策。
2. `agent_skills/bioinformatics-workflow/SKILL.md`：当前 paper-first 工作流和决策门；它要求把科学决策和执行状态分开，并在不兼容或不确定时 fail closed。
3. `agent_skills/bioinformatics-workflow/references/decision-contract.md`、`decision-gates.md`、`paper-reconstruction.md`、`multifactor-design.md`、`multigroup-longitudinal.md`、`matrix-method-policy.md`：决策记录、论文重构、复杂设计和矩阵方法的详细约束。
4. `main.py`、`tools/batch_tools.py`、`tools/model_factory.py`、`tools/multifactor_design.py`、`tools/multigroup_tools.py`、`tools/scrna_tools.py`、`tools/proteomics_tools.py`：生产实现。
5. `output/skill_forward_test_20261008/`、`output/paper_first_forward_test_20261009/`、`output/native_codex_exercise_corrected_processing_20261003T194153Z/`：最新的决策门、论文优先和 exercise cohort 证据。

## 近期主线提交

从 `main` 的共同基线 `a3cc3e2` 到当前 `ed706f0`，主要成果如下：

- `aee7b2d`：限制 GSEA 的 MyGene 注释请求，降低重复查询成本。
- `1df611d`、`5e6edd2`：冻结 RNA-seq ZIP gold/reference benchmark，并记录 ZIP 与远端数据范围。
- `df659cd`、`e45a614`：加入带来源和 provenance 的矩阵语义路由与分类器，避免只看数值分布就把 FPKM/TPM、estimated counts 或 raw counts 混用。
- `33730d5`：加入 peptide→protein 汇总，以及 paired single-cell pseudobulk/limma 路径。
- `ed706f0`：加入显式 multifactor、多组和 paired-change 执行器；加强 semantic contrast gate、决策证据记录、paper-first workflow skill、审计/复核脚本和相关测试。

主线还保留更早的多因素 limma/count semantics、claim evidence、20×3 稳定性、production preflight、SEA-CDM gate 和运行 guard/router 工作。

## 当前生产架构和已实现能力

### LLM、路由和运行控制

- `tools/model_factory.py` 统一 Anthropic Claude Sonnet 和 DeepSeek V4 Pro 配置。DeepSeek 使用 Anthropic-compatible endpoint；普通 ReAct agent 可启用 thinking，结构化输出会关闭 thinking 以兼容强制 schema/tool choice。
- `main.py` 根据请求做 deterministic tool routing；歧义请求才暴露完整工具集。`guard_tools` 对每次请求隔离，重复参数复用结果，单工具有唯一执行上限，避免模型循环和重复计费。
- `run_status.py`、`agent_state.py`、`evidence.py` 保存阶段状态、warnings/failures、输入来源、决策、artifacts 和 hash。批处理同时生成 `summary.csv`、`workflow.log`、`failures.log`、`run_status.json` 与每个 accession 的证据包。
- `llm_helpers.py` 的两个可选 fallback：
  - 结构化 contrast validation：Python proposal 不明确时复核 design column/control/treatment；strict 模式下 validator 不可用会阻止未验证 contrast。
  - 样本名语义对齐：exact、substring、token overlap 都失败时，才让结构化 LLM 解读缩写；结果会校验未知 ID、重复映射和覆盖率。
- 当前 Codex native paper-first workflow 应自行读论文、作决策、保存 decision contract，再调用 Python 工具。不要把原 LangChain agent 或隐藏外部 validator 当作科学判定替代品，除非用户明确要求。

### 矩阵、方法和安全门

- raw integer counts：可走 DESeq2、edgeR 或 limma-voom；批处理默认先产生 `log2(CPM+1)` sidecar，再按 raw-count route 做 DESeq2。
- FPKM/TPM、already-log、log2 FPKM/TPM、proteomics intensity：走 limma；不能把 normalized/log-scale 输入送进 DESeq2。
- estimated counts：数值为小数不足以直接决定 route。只有文件、脚本、论文或 provenance 明确说明是 estimated counts，并且处理配方允许显式 rounding 时，才可进入 count route；没有来源证据就停止，不能盲目 rounding 或把它当 FPKM/TPM。
- methylation β 值：先转 M-value，过滤 invariant sites，再走 limma；不能走 DESeq2。
- `analysis_policy.py`、`multifactor_design.py` 负责 numeric validation、两组复制数、缺失/完全混杂、full rank 和 residual df 等 hard gates。成功生成 p-value 不能覆盖失败的科学门。
- `batch_tools.py` 可执行 `multigroup`、`multilevel`、`factorial` 和 `paired_change` 计划；显式计划保存公式、rank、residual df、contrast 和 excluded/unresolved covariates。多组/重复测量不能被静默压成一个任意 two-arm contrast。实现会在拟合前处理重复 feature ID，不能把旧参考文档中“必然拒绝 duplicate feature ID”的表述当成当前实现行为。
- `limma_tools.py` 支持显式 formula、coefficient、additive covariates 和 interaction；`deseq2_tools.py` 支持 additive covariates，但没有明确 interaction contrast 时拒绝 DESeq2 interaction。

### 单细胞、蛋白组和其他组学

- `scrna_tools.py` 先按 sample/donor × cell type 聚合 pseudobulk，避免把 cell 当独立 biological replicate。`paired=True` 只保留同时有 control/treatment 的 complete donors，强制 limma 公式 `~ C(sample) + Treatment`，结果写出 `n_complete_pairs` 和 paired 状态；不完整配对或复制数不足会 stop。
- `proteomics_tools.py` 支持 peptide-level 到 protein-level 汇总；linear abundance 默认 sum，log2 abundance 用 mean/median/top-N mean；默认排除 shared peptides 和 decoys，并写 JSON provenance manifest。protein/intensity 需要先解决 log scale、缺失值、batch 和 metadata，再做 limma。
- `Methylation` 路径支持 β→M 和 probe/site 级结果，但真实分析仍需要明确 feature annotation、batch 和设计。
- `seacdm_tools.py` 当前使用结构化 Pydantic extraction，Python 分配 IDs/FKs 并写 evidence；旧 `extract_sea_cdm_conditions` 仅保留兼容性。

## 最新验证证据

### 1. Skill decision-gate forward test：2026-10-08

路径：`output/skill_forward_test_20261008/`

- 5 个冻结 case，3 次独立 blind pass，共 15 个 case-repeat observation。
- matrix/method、design/contrast、covariance、manual-review/stop 路由均为 15/15。
- GSE162307 和 GSE270703 正确停止；GSE308626、GSE132520、GSE217155 进入 execution smoke。
- execution smoke：
  - GSE308626：raw-count DESeq2，10 samples、32,200 features、10 个 `padj<0.05` 且 `|log2FC|>1` 的 DEG。
  - GSE132520：16 samples 的 factorial limma，公式 `~ C(genotype)*C(treatment)`，rank 4、residual df 12；三个 contrast 的 DEG 数为 7、33、0。
  - GSE217155：`EXE+Ath diet vs Ath diet` 的 exploratory limma，6 samples、rank 2、df 4、0 个 DEG，明确标记 small-n exploratory。
- `audit_run.py`：`verdict=pass`、score 90.0、coverage 100.0、blocking findings 0；execution 87.2、scientific validity 100、provenance 100、reproducibility 57.1。study completion 3/5 是有意 block 的 warning，不是漏跑。
- 证据链：19 个 artifacts 全部 hash verified，11/11 decisions grounded。
- 80% stratified subset stability 是 secondary numerical check，不是科学有效性证明：GSE308626 和 GSE132520 两个 exercise effect 多数为 mixed；GSE217155 null call 和 GSE132520 interaction 为 stable。不要把 mixed stability 解释为 invalid method，也不要把它当作稳健 gene-level discovery。
- 重要文件：`report.md`、`execution_summary.json`、`blind_repeat_summary.json/csv`、`stability/stability_summary.json`、`evidence.json`、`run_status.json`。

### 2. Paper-first forward test：2026-10-09

路径：`output/paper_first_forward_test_20261009/`

这个 run 只做论文重构、决策 gate 和独立复核，没有新增 DE。5/5 paper source 的关键词和 SHA 检查通过；5/5 paper map、threshold、covariance、discrepancy 记录通过；exact reproduction safely allowed 为 0/5；safe declared validation route 为 1/5。

- GSE308626：论文报告 TPM/RSEM + DESeq2 + FDR<0.10；本地是 raw STAR counts。精确复现阻止；可以另做声明为 deviation 的 raw-count DESeq2 validation，不能称 exact reproduction。
- GSE132520：2×2 genotype×exercise；局部 log2 FPKM；论文未明确 primary RNA-seq DE method。允许 factorial limma validation，但必须标记 workflow fallback，不能称论文方法精确复现。
- GSE162307：single-nucleus、cell type/time-specific、loom 输入，animal-level covariance 和表达矩阵未解决。必须 manual review，不能做 bulk two-arm 替代。
- GSE217155：论文 DESeq2、n=8/group、`padj<0.05` 且 `|log2FC|>1`；本地 log2 FPKM、n=3/group。只能做 bounded exploratory limma，不是 exact reproduction。
- GSE270703：donor-paired Visium；本地文件是 tissue-position artifact。需要 spatial/data recovery review；paper threshold 也必须按 contrast 拆开，不能把 sample-level paired `p<0.05` 套到 spot-level FindMarkers。

独立 paper-first review 同意这 5 个 route，并特别确认 GSE270703 的阈值必须 contrast-specific。关键文件：`report.md`、`reproduction_summary.json`、`paper_first_decision_summary.csv`、`paper_first_independent_review.md`、`paper_data_discrepancies.json`、`paper_evidence_checks.json`。

### 3. Exercise article-first blind test：2026-10-03

主路径：`output/exercise_blind_article_first_20261003_182937/`；独立复核：`output/exercise_blind_article_first_20261003_182937_independent_review_20261003/`

- Europe PMC、OpenAlex、Crossref 搜索共 300 raw candidates，DOI/title deduplicate 后 295，保留 20 个 paper-owned experimental omics studies。
- primary pass：11 个 `ready_for_alignment_gate`，8 个 `manual_review_data_recovery`，1 个 QC-only 但因 paired/multilevel design 停在 DE 前；主 pass manual-review rate 40%。没有调用原 LangChain agent、DeepSeek/Anthropic 或隐藏 validator。
- P01/GSE97084 做到 102/103 metadata coverage 的 sample alignment、filtered counts 和 log2(CPM+1) normalization；由于论文是多 modality、paired pre/post、多层因素，停止在 DE 前。
- independent evidence review 20/20 source/evidence 完整，paths/hash 通过；verdict 为 justified 9、should-have-manual-review 6、false-positive-risk 5、valid-refusal 0。独立 hold/manual rate 55%。
- 主要风险：P03/P04/P14/P16 是 assay/accession/method mismatch；P05/P08/P09/P10/P11/P13 需要 genotype/time/sex/tumor/cell-fraction/patient-block design；P01 series metadata 与论文 46-subject/23-paired subset 不一致，必须先 subset。

### 4. Corrected native exercise processing：2026-10-03

路径：`output/native_codex_exercise_corrected_processing_20261003T194153Z/`；独立复核：`output/native_codex_exercise_independent_review_20261003T200108Z/`

- 16 个 paper-owned studies；9 个完成分析，其中 3 个标记 exploratory；2 个 manual review/data recovery；5 个 valid refusal；unsupported terminal labels 为 0。
- 关键纠正：
  - GSE162307 从 unsupported 改为 manual review：loom、cell QC、pseudobulk、animal mapping 和 crossed exercise×satellite-cell-depletion×time 需要明确计划。
  - GSE309619 改为 manual data recovery：论文有 10 个 paired baseline/12-month samples，但下载矩阵只有 4 features。
  - GSE66822 改为 valid refusal：只有 genotype，没有 exercise factor。
  - GSE128078 保留 subject-blocked disease×time interaction，但独立复核认为需要 full-rank reparameterization。
- corrected run 所有 evidence、decision、paper text、GEO metadata 和 declared artifacts 都存在且 hash 可核对；external LLM calls 为 0。
- independent review：6 justified、2 false-positive-risk、3 should-have-manual-review、5 valid-refusal；其中 GSE124676、GSE128078、GSE97718 被升级为需要人工关注。GSE97718 尚未体现论文所需 diet×time interaction。

### 5. RNA-seq ZIP gold benchmark

报告：`test/experiments/rnaseq_zip_remote_ab/REPORT.md`；本地产物：`output/rnaseq_zip_remote_ab/output_local/`

6/6 pairwise contrasts 完成 `deg_gsea_ok`：

| Contrast | DEG | GSEA significant |
|---|---:|---:|
| GSE194151 FC vs MC | 10,776 | 33 |
| GSE194151 FH vs FC | 1,617 | 46 |
| GSE194151 FH vs MH | 11,035 | 37 |
| GSE194151 MH vs MC | 274 | 26 |
| GSE195482 WMF vs WCF | 1,379 | 42 |
| GSE195482 WMM vs WCM | 128 | 37 |

GSE194151 的四个矩阵被 provenance 识别为 kallisto estimated counts，并依据 ZIP 内明确的处理配方显式 rounding 后走 DESeq2；GSE195482 两个矩阵是 raw counts。FC/MC 和 FH/MH 触发 DEG-sanity warning（约 51% 和 53% features significant），这是科学复核项，不是执行或 provenance 失败。formal acceptance 仍取决于确认 fractional-count interpretation 和两个 sanity warning。

### 6. 较早的 20×3 稳定性和多组 smoke

这些结果可以作为历史工程证据，不能当作当前 paper-fidelity 最终验收：

- DeepSeek `codex_skill_20x3` vs `current_agent_20x3`：60/60 trials executed，45/60 completed，15/20 repeat-stable；输入 SHA、claims grounding 和 artifact hashes 通过，但总体 audit verdict `fail`（score 82.9、coverage 89.1），主要阻塞为 study completion、DEG-sanity 和复杂矩阵语义。失败/阻塞案例包括 GSE270703 spatial、GSE302944 estimated-count provenance、GSE308674 non-finite matrix、GSE315678 fractional estimated counts、GSE317978 n=2/group。
- Native Codex 20-case migration：20/20 reviewed，2 个完整 workflow，18 个 manual review/refusal；旧 audit coverage 20.7%，因为缺 run_status/root summary/call-time/repeat evidence，不能当作质量分数。
- `output/cohort_main_multigroup_batch_20261002/integration_report.json`：6/6 study success、13 contrasts，能证明 explicit formula/rank/df 的 executor smoke；但该早期 summary 将部分 raw_counts 用 limma explicit plan，故不能当作当前 matrix-method compatibility 已通过的证据。对应 audit verdict fail 81.6/100，blocking matrix-method compatibility 和 contrast fields。

## BO/Kang 方向的历史结论和当前边界

- BO ZIP 的公平阈值是 `padj<0.05 && |log2FC|>0.5`；旧 agent 的 `n_deg` 只统计 `padj<0.05`，因此 DEG 数不可直接比较。统一阈值后六个 bulk contrast 的 Jaccard 为 0.904–0.987。
- MH vs MC 的全 92 个显著基因 Pearson 约 0.79，去掉 4 个单样本稀疏/高杠杆基因 `Try4`、`Ctrb1`、`Cpa1`、`Prss2` 后，88 个共同显著基因 Pearson/Spearman=1、方向一致率=100%。不要直接删除这 4 个基因；应保留主结果并报告 sensitivity analysis。
- Kang/GSE96583 的工程路径以前是未 donor-blocked 的 `~ condition` pseudobulk，历史结果只能算工程通过/方向性支持；代码现在已经支持 paired=True 的 donor-blocked scRNA executor，但仓库里还没有正式 Kang paired rerun、gold comparison 和独立 audit。因此不能把“代码已支持”写成“论文级 Kang 复现已完成”。
- 历史会议材料仍把 Kang donor blocking 列为待办；实际需要补的是正式 paired rerun、冻结 complete-pair/min-cell/CD8 sensitivity/composition 规则，以及独立审计和 Meng 对统计单位的确认。

## 仍需 Claude 接手的工作

### 优先级 1：正式 Kang donor-paired 复现

1. 明确 Meng 的统计单位：每个 cell type 内 donor-level pseudobulk/paired model 是否为主分析；全细胞 pooled 是否仅作补充。
2. 冻结 donor complete-pair、每 donor 最低 cell 数、CD8 不平衡（6/8 ctrl、8/8 stim）和 Megakaryocytes 1/1 的规则。
3. 用 `scrna_tools.run_scrna_pseudobulk_da(..., paired=True)` 对 GSE96583 做每 cell type 分析，记录 `n_complete_pairs`、公式、过滤和 GSEA。
4. 对比论文/BO reference 的 logFC、方向、DEG、GSEA；另行报告 composition change，不能把 composition 当 DE。
5. 运行 `evaluate-bioinformatics-agent` audit，补足 root summary、run_status、call-time、repeat evidence，使 coverage 可判定。

### 优先级 2：更新 workflow references

`agent_skills/bioinformatics-workflow/references/multifactor-design.md` 和 `multigroup-longitudinal.md` 仍有旧表述，像是 batch 只支持 two-arm/sibling。当前 `batch_tools.py` 已接入 `multigroup_tools.py`，应同步文档，准确写出支持的 analysis_type 和仍然不能自动推断的范围。

### 优先级 3：修复已知复核项

- GSE128078：重参数化 disease×time，确保 subject blocking 与 interaction 不冗余、design full rank。
- GSE97718：按论文要求显式加入 diet×time interaction，而不是只跑 diet/time 的简化路线。
- GSE124676：复核 donor/arm 结构，确认跨 arm donor 是否允许当前 exploratory route。
- GSE309619：恢复完整表达矩阵或 raw reads，再执行 10 个 paired subject 的方案。
- GSE162307/GSE270703：分别准备 single-nucleus pseudobulk/cell-level 和 spatial data recovery 方案；在输入与 covariance 未解决前保持 stop。

### 优先级 4：完善 benchmark 口径

统一报告 `n_padj05`、`n_padj05_lfc05`、全 tested genes Pearson/Spearman、显著集合 Jaccard、方向一致率和 GSEA NES overlap；异常稀疏基因做 sensitivity analysis。pairwise 和 joint 2×2 分析要明确区分 estimand，不能把 BO 的 R 脚本当成 agent 实现。

## 运行和验证命令

```powershell
$env:PYTHONIOENCODING = "utf-8"
.\.venv\Scripts\python.exe -m unittest `
  test.unit.test_multifactor_design `
  test.unit.test_multigroup_tools `
  test.unit.test_decision_log_llm `
  test.unit.test_strict_semantic_routing

.\.venv\Scripts\python.exe -m compileall -q main.py tools scripts agent_skills/bioinformatics-workflow test/unit test/reports test/experiments

.\.venv\Scripts\python.exe agent_skills/bioinformatics-workflow/scripts/validate_decision_contract.py <decision-json-files>
```

最近验证：上述 4 组 targeted unittest 共 15 tests passed；相关 Python 文件 compileall passed。系统 Python 没有 `pytest`/全部项目依赖，测试应使用仓库 `.venv`。

## 给 Claude 的交接要求

请把本文件当作事实边界和工作入口：

1. 先读 `AGENTS.md` 和 `agent_skills/bioinformatics-workflow/SKILL.md`，再读最新 run 的 JSON/CSV，而不是只看旧 prose。
2. 把 `decision_status`、`execution_status`、`paper_threshold`、`audit_threshold` 分开保存。
3. 论文和 GEO/matrix 有冲突时记录 discrepancy；不能用 p-value、DEG 数或成功运行掩盖 matrix/method/design/covariance 不兼容。
4. 先完成 Kang paired formal rerun 和 audit，再决定是否扩大到 joint bulk 或更多模态。
5. 所有新的结论必须附输入路径、run status、evidence/artifact hash 和明确的 exploratory/manual-review 标签。

不要把以下内容误报为已完成：正式 Kang donor-paired paper reproduction、当前 20×3 全部研究的最终 acceptance、GSE128078/GSE97718 的独立复核项、protein/methylation 的真实用户数据分析。
