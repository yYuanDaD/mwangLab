# `dev/ds` 近期成果总览

> 整理日期：2026-08-18  
> 目标分支：`dev/ds`  
> 当前提交：`246abf979dfb027f2e476f1bde0a690cf1e494fe`  
> 对比基线：`main`（`1451ec6`）  
> 覆盖周期：2026-08-05 至 2026-08-18

## 1. 执行摘要

这一阶段的工作把项目从“已有较完整的多组学生物信息学 Agent”推进到了“有模型选型证据、有运行时工作流知识、有统一审计口径、能够分模式部署 DeepSeek 的可评估系统”。最重要的成果不是单纯替换模型，而是建立了从 provider 兼容性、Agent 路由、真实差异分析、长文 SEA-CDM 抽取、GEO 范围约束、未见案例盲测到高成本 fallback 的逐级证据链。

当前可以支持的结论如下。

1. **DeepSeek V4 Pro 可以作为主 ReAct Agent 和差异分析路由模型。**
   - provider/tool/structured-output 兼容性探针通过；
   - 7 类科学路由案例 × 3 次重复全部通过；
   - 3 个 cached-GEO 差异分析案例 × 3 次重复全部通过；
   - 未出现循环、重复工具调用或科学安全阻断；
   - 相对 Sonnet 4.6，Agent 路由实验的单次成功成本约为 1.95%，cached-GEO 端到端实验约为 2.06%。

2. **DeepSeek 不适合继续使用原来的单次超长 SEA-CDM 大 schema 路径。**
   - 在 GSE208615 的原始 100k 字符、单次 structured-output 路径上 0/3 通过；
   - 主要问题是输出虽然可解析，但材料和论文 findings 等必需内容为空，属于“结构合法但语义不完整”。

3. **分阶段、GEO metadata 支持的 accession-scope SEA-CDM 路径已经达到候选可用水平。**
   - 单次 4K 路径 0/3，通过 staged 16K 路径提升为 3/3；
   - GSE208615、GSE270703、修正范围后的 GSE250122 均 3/3；
   - 冻结的未见 multi-accession 案例 GSE197045 也达到 3/3，无 GSE198652/RNA-seq 跨 accession 污染；
   - staged、泛化和盲测目录的独立审计均为 100/100，但适用覆盖率为 65.2%，因为这些是结构化抽取实验，不包含 DA 的矩阵、contrast 和 DEG 检查。

4. **生产路由仍然采取分模式策略，而不是全量切换。**
   - 主 Agent/DA：评测部署使用 DeepSeek V4 Pro；
   - GEO metadata 支持、明确 target accession 的 staged SEA-CDM：DeepSeek 已有支持证据；
   - paper-wide 或无 metadata 的 SEA-CDM：继续保留 Sonnet 4.6；
   - Opus 5 已完成有限的 stage-only fallback 资格测试，但确定性路由和重复稳定性尚未完成，不能描述为已经正式接入生产。

5. **评测基础设施本身成为了可复用产品能力。**
   - 新增运行时 skill 渐进加载机制；
   - 新增 bioinformatics-agent 审计 skill、rubric 和自动审计脚本；
   - 强制分开报告分数、覆盖率、阻断项、成本和延迟；
   - 对 prompt/model/routing 改动采用相同案例、相同 scorer、至少 3 次重复的配对 A/B；
   - 关键运行产物具备 evidence、哈希、decision trace 和 run status。

## 2. Git 范围与交付规模

### 2.1 提交关系

```text
1451ec6  main
   └─ 8903e67  dev-base / codex/agent-evaluation-skill
         └─ 246abf9  dev/ds
```

`dev/ds` 与其他工作分支不是相互冲突的多条历史，而是一条线性提交链。`main`、`dev-base` 和 `codex/agent-evaluation-skill` 都已包含在 `dev/ds` 中。

### 2.2 两次增量提交

| 提交 | 日期 | 主题 | 主要规模 |
|---|---|---|---:|
| `8903e67` | 2026-08-05 | Runtime skills 与 A/B 安全评测 | 17 个文件，+1,054 / -29 |
| `246abf9` | 2026-08-18 | DeepSeek、SEA-CDM staged/scope 与 fallback 评测 | 29 个文件，+5,907 / -63 |

相对 `main`，`dev/ds` 总计改动 **45 个文件，新增约 6,961 行、删除 92 行**。新增内容以评测脚本、回归测试、模型工厂和 SEA-CDM 稳健化为主，没有把大体积运行产物、密钥或 `.env` 提交到 Git。

## 3. 最新分支继承的系统能力

`dev/ds` 继承了 `main` 已建立的完整 Agent 基础，新增工作是在这套基础上完成模型迁移与验证。

### 3.1 Agent 与路由

- LangChain `create_agent` / LangGraph ReAct 循环；
- 每个请求先经过确定性 `tool_router`，只暴露匹配的 bulk、single-cell、methylation、proteomics、paper 或 evaluation 工具；
- 模糊请求安全回退完整工具注册表；
- 每个请求创建独立的 guarded tool set；
- `guard_tools` 对相同参数调用去重、复用缓存或进行中的结果，并限制每个工具最多 3 组不同参数；
- `recursion_limit=25` 与工具层 cap 共同限制最坏情况调用成本。

### 3.2 独立运行状态

运行状态没有作为重复的 assistant message 写入 ReAct 历史，而是保存在 `BioinformaticsAgentState` 中：

```text
BioinformaticsAgentState
├── messages
├── analysis_request
├── run_status
├── artifacts
├── evidence_ids
└── execution_budget
```

`RuntimeStateMiddleware` 在每次模型调用前同步 tracker，只把会影响下一步决策的状态临时投影到 system context。阶段计数、耗时、warning/failure、artifact 和 evidence 指针仍持续写入 `run_status.json`，但不会污染消息历史。

### 3.3 生物信息学安全策略

- raw integer counts 进入 DESeq2/edgeR/voom 类路径；
- FPKM/TPM、已 log 转换矩阵、microarray intensity 和 processed proteomics 使用 plain limma；
- 样本对齐使用 exact → substring（带 used 集合）→ token overlap → 经验证的 LLM fallback；
- 明确拒绝按行位置对齐；
- metadata 文件不会被当作 counts 候选；
- 二组设计、最小重复数和每组对齐覆盖率由 Python 验证；
- implausible DEG fraction 和过小样本量会产生显式 sanity finding；
- 单细胞差异分析使用 biological sample × cell type pseudobulk，不把细胞当生物学重复；
- batch 单 study 失败会隔离并记录，不中断整个 cohort。

## 4. 运行时 Skill 与 Agent 审计体系

### 4.1 渐进式运行时 Skill

新增 [`tools/runtime_skills.py`](../../tools/runtime_skills.py)，其设计重点是“先暴露元数据、相关时再加载正文”。

- Agent 初始只看到 `agent_skills/*/SKILL.md` 的 name 和 description；
- 仅当请求明显相关时调用 `load_runtime_skill`；
- loader 只读取仓库内受控的 Markdown、TXT、JSON references；
- 不执行 skill 脚本；
- 不接受任意文件路径；
- 重名 skill、非法名称、未知 skill 和超过 60,000 字符的 bundle 都会显式失败；
- 可用 `BIOAGENT_RUNTIME_SKILLS=0` 关闭，便于建立无 skill 基线。

首个项目 skill 为 [`paper-workflow-safety`](../../agent_skills/paper-workflow-safety/SKILL.md)，它约束：

- 先建立 paper dataset inventory；
- 区分论文自有 accession 与仅引用 accession；
- 不混合不同模态；
- single-cell 必须有 biological subject/sample ID 才能 pseudobulk；
- observational、clustering、prognostic 或 validation 设计不得虚构 treatment-control contrast；
- 矩阵类型决定统计方法；
- 论文报告结论与本项目计算结论必须分层记录；
- 不得复制示例中的 accession、分组、方法或结论。

### 4.2 Runtime skill 配对 A/B

固定 Sonnet 4.6、temperature 0、同一篇未见 AML 多数据集论文、同一 schema/gold/scorer，进行了 3 组配对试验。

第一版虽然平均分略升，但 2/3 skill 输出把 normalized/log-scale 数据错误路由到 limma-voom，因此被拒绝。随后将 matrix/method compatibility 加入硬门并强化 skill，第二版结果为：

| 指标 | 无 skill | Runtime skill |
|---|---:|---:|
| 平均总分 | 89.99 | 92.25 |
| Workflow safety | 0.833 | 0.944 |
| 配对胜/平/负 | — | 2 / 1 / 0 |
| Matrix/method gate | — | 3/3 通过 |
| 总成本 | $0.220284 | $0.212367 |

结论是**只接受这一 paper-planning 用例**，没有外推到所有 GEO、single-cell、methylation 或 proteomics 工作流。完整记录见 [`RUNTIME_SKILL_AB_20260805.md`](../reviews/RUNTIME_SKILL_AB_20260805.md)。

### 4.3 可复用的 bioinformatics-agent 审计 Skill

新增：

- [审计说明](../../.agents/skills/evaluate-bioinformatics-agent/SKILL.md)
- [审计 rubric](../../.agents/skills/evaluate-bioinformatics-agent/references/rubric.md)
- [自动审计脚本](../../.agents/skills/evaluate-bioinformatics-agent/scripts/audit_run.py)

审计分为六层：任务完成、科学有效性、结果稳定性、provenance、Agent 行为和效率。关键规则包括：

- **score 与 coverage 必须分开报告**；
- 加权覆盖率低于 60% 时，即使已测项目得分很高，也标为 `insufficient_evidence`；
- 非终态、失败 study、矩阵/方法不兼容、无效 contrast/alignment、异常 DEG、dangling reference 和 artifact hash mismatch 都是阻断项；
- schema、文件、哈希、阈值和路由尽量使用确定性检查；
- LLM judge 仅用于无法编码的语义问题，并与被测 Agent 独立；
- prompt/model/skill 变化采用配对 A/B，至少 3 次重复。

这一机制纠正了早期“流程退出码为 0 就算成功”或“平均分提高就接受改动”的问题。

## 5. 统一模型工厂与 DeepSeek V4 Pro 接入

新增 [`tools/model_factory.py`](../../tools/model_factory.py)，统一 Anthropic 与 DeepSeek Anthropic-compatible API 的模型构造。

### 5.1 配置与默认值

```dotenv
BIOAGENT_LLM_PROVIDER=deepseek
BIOAGENT_SEACDM_LLM_PROVIDER=anthropic
BIOAGENT_STRUCTURED_MAX_TOKENS=16384
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

主要行为：

- 评测部署的主 Agent 默认选择 `deepseek-v4-pro`；
- 无环境配置时，library fallback 仍保持 Anthropic/Sonnet，避免隐式改变已有调用者；
- SEA-CDM 通过独立的 `BIOAGENT_SEACDM_LLM_PROVIDER` 控制，当前生产默认仍为 Anthropic；
- DeepSeek endpoint 被规范化到 `/anthropic`，自动移除旧 `/v4` 后缀并避免重复追加；
- 只允许明确支持的 `deepseek-v4-pro` / `deepseek-v4-flash`，防止 provider 将未知名称静默降级到错误模型；
- API key 只通过环境变量名解析，不进入配置对象、日志或提交。

### 5.2 Thinking 与 structured output 兼容性

- 主 ReAct Agent 保持 DeepSeek thinking enabled，默认 `effort=max`；
- `with_structured_output()` 会强制 `tool_choice`，而 DeepSeek thinking 模式不接受该组合；
- structured hooks 因此自动关闭 thinking，并省略 effort；
- structured output 默认提供 16K 输出预算，避免长 JSON 在 provider 较小默认上限处静默截断；
- 对 Claude 5/Opus 5 构造器移除不兼容的旧 `temperature` 参数。

相关行为由 13 个 model-factory 单测覆盖，包括 endpoint 规范化、模型白名单、可选 key 的 fail-soft、structured thinking、输出预算、SEA-CDM provider 隔离和 Opus 参数兼容。

## 6. DeepSeek provider/tool/schema 兼容性门

最新兼容性探针目录：[`model_compat_deepseek_20260817_195548`](../../output/model_compat_deepseek_20260817_195548/compatibility_report.md)。

结果：

- verdict：`pass`；
- gate score：100/100；
- gate coverage：100%；
- 模型：`deepseek:deepseek-v4-pro effort=max`；
- 估算成本：$0.001702；
- 阻断项：0。

探针实际覆盖：

- 基础文本调用；
- FPKM/TPM → limma 的 structured scientific routing，连续 10 次结果一致；
- 单次 tool call 参数生成；
- tool result 回传后的多轮回答；
- 完整小型 Agent loop，只有一次工具调用且正确停止。

该探针本身没有覆盖真实 GEO 文件、全量 SEA-CDM 或 DEG/GSEA 稳定性。因此其通用 Agent 审计只有 90.1/100、coverage 29.3%，被正确标记为 `insufficient_evidence`。后续 A/B 才补齐这些维度。

## 7. 主 Agent 科学路由 A/B

实验目录：[`model_agent_ab_20260817_200223`](../../output/model_agent_ab_20260817_200223/model_agent_ab.md)。

### 7.1 案例设计

7 类案例覆盖了：

1. raw counts；
2. log/FPKM；
3. single-cell；
4. methylation；
5. metadata-only；
6. unsafe multifactor；
7. repeated-results evaluation。

每个 provider 每个案例重复 3 次，即 Sonnet 21 次、DeepSeek 21 次。固定输入、tool registry、评分器和案例预期，交替执行顺序。

### 7.2 结果

| 指标 | Sonnet 4.6 | DeepSeek V4 Pro |
|---|---:|---:|
| Runs | 21 | 21 |
| 平均分 | 100 | 100 |
| 通过率 | 100% | 100% |
| 阻断 runs | 0 | 0 |
| 重复调用 runs | 0 | 0 |
| 中位延迟 | 9.773 s | 4.078 s |
| 总成本 | $0.329151 | $0.006408 |
| 每次成功成本 | $0.015674 | $0.000305 |

DeepSeek 每次成功成本约为 Sonnet 的 **1.95%**，中位延迟约降低 **58.3%**。质量非劣于 3 分、安全/循环和成本不超过 Sonnet 30% 三个接受门全部通过，结论为 `accept_pilot`。

该实验验证的是工具选择和 Agent 行为，不包含真实 GEO 计算，因此运行目录的通用审计仍只有 29.3% coverage；这也是下一项 cached-GEO E2E A/B 的必要性。

## 8. Cached-GEO 差异分析端到端 A/B

实验目录：[`model_e2e_ab_20260817_202739`](../../output/model_e2e_ab_20260817_202739/model_e2e_ab.md)。

### 8.1 三类真实案例

| 案例 | 数据类型 | 核心风险 | 正确路径 |
|---|---|---|---|
| GSE279359 | raw counts | 常规运动前后对比 | DESeq2 |
| GSE208615 | log/FPKM | 防止 normalized matrix 进入 raw-count 方法 | limma |
| GSE297707 | raw counts，64 样本 | `Sample_1` / `Sample_10` 前缀碰撞 | 安全样本对齐 + DESeq2 |

每个模型、每个案例重复 3 次，共 18 次完整 DA 运行。

### 8.2 结果与审计

| 指标 | Sonnet 4.6 | DeepSeek V4 Pro |
|---|---:|---:|
| 平均分 | 100 | 100 |
| 通过率 | 100% | 100% |
| 阻断 runs | 0 | 0 |
| 重复调用 runs | 0 | 0 |
| 中位延迟 | 14.330 s | 11.702 s |
| 总模型成本 | $0.280110 | $0.005778 |
| 每次成功成本 | $0.031123 | $0.000642 |

DeepSeek 每次成功成本约为 Sonnet 的 **2.06%**，中位延迟约降低 **18.3%**。

更重要的是，跨 provider 和 provider 内重复的以下指标在三个案例中全部为 1.000：

- full log2FC Pearson correlation；
- direction agreement；
- Top-50 Jaccard；
- significant DEG Jaccard。

这不是因为模型直接生成 DEG 数字，而是两者稳定选择了相同矩阵、设计、contrast 和统计工具，使确定性统计后端产生一致结果。

独立审计结果：

- verdict：`pass`；
- score：100/100；
- coverage：100%；
- 18/18 studies/runs 成功；
- 18 条矩阵/方法路由正确；
- 18 条 contrast 字段完整；
- DEG sanity 全部通过；
- 38/38 artifacts 哈希验证通过；
- 19/19 decisions/claims 有 grounding；
- 阻断项为 0。

因此该实验给出的结论强于“路由 pilot”：**DeepSeek V4 Pro 可以作为当前主 Agent/DA 的评测部署默认模型。**

未测范围包括联网 GSEA/ORA 和 SEA-CDM 长文抽取；后者被单独拆出评测。

## 9. SEA-CDM：从单次大 schema 到 staged accession-scope

### 9.1 原始单次路径的失败

实验目录：[`model_seacdm_ab_20260817_221240`](../../output/model_seacdm_ab_20260817_221240/model_seacdm_ab.md)。

在 GSE208615 的 100k 字符全文/大 schema 提取中：

| 指标 | Sonnet 4.6 | DeepSeek V4 Pro |
|---|---:|---:|
| 通过 | 3/3 | 0/3 |
| 平均分 | 100 | 75 |
| provenance | 97.1% | 100% |
| materials | 36–37 / run | 0 |
| findings | 12–13 / run | 0 |
| 中位延迟 | 133.232 s | 36.869 s |

DeepSeek 的 provenance 看起来是 100%，但分母来自它实际输出的有 source 项；materials/findings 为空导致核心任务未完成。因此“高 provenance”不能抵消 completion failure。该轮明确得出 `retain_sonnet_for_seacdm`，并触发 staged 重构。

### 9.2 Staged 方案的结构

新路径把原来的长输入/大输出拆成小 schema、聚焦文本区域和完成门：

```text
paper regions
├── study
├── documentation
├── experiment + interventions
├── materials chunks
└── findings chunks
        ↓
deterministic completion gate
        ↓ incomplete/error
targeted retry（最多 1 次）
        ↓
dedupe + deterministic repair + flatten + provenance verification
```

关键实现：

- `study`：必须得到 grounded `study_name`；
- `documentation`：必须恰好一条 paper record；
- 若 documentation title 已有可靠 source、study title 缺失，Python 复制同一 grounded fact，避免额外随机调用；
- `experiment_interventions`：必须恰好一个 accession-scope experiment，并包含至少一个 intervention；
- 当 GEO scope 包含 exercise/HIIT/MICT 时，intervention 中必须出现相应运动语义；
- materials 和 findings 对高相关 chunk map/reduce，随后按关键字段去重；
- 每次尝试记录 stage、attempt、输入字符数、输出行数、状态、错误和 usage 到 `decision_trace`；
- required-empty 不再作为“合法空对象”静默通过；
- shape normalization 兼容部分 provider 把 plain reference 字段错误包装为 `{value, source}` 的情况。

### 9.3 GSE208615 staged A/B

实验目录：[`deepseek_seacdm_staged_ab_20260818_135506`](../../output/deepseek_seacdm_staged_ab_20260818_135506/deepseek_seacdm_staged_ab.md)。

| 指标 | Single 4K | Staged 16K |
|---|---:|---:|
| 通过 | 0/3 | 3/3 |
| 平均分 | 65 | 100 |
| provenance | 100.0% | 99.0% |
| 中位延迟 | 35.717 s | 84.495 s |
| 每次成功成本 | 无成功 | $0.031671 |
| Material fuzzy reference recall | — | 89.2% |
| Finding fuzzy reference recall | — | 100.0% |

Staged 路径相对 Sonnet SEA-CDM 的每次成功成本约为 12.5%，通过全部预设门槛。独立 staged-only 审计为 100/100、coverage 65.2%、0 blocking；27/27 artifacts 哈希通过，6/6 decisions grounded。

低 exact-set Jaccard 没有被直接当作失败，因为整行文本的轻微措辞差异会使 exact tuple 完全不相等。评测同时使用了 fuzzy reference recall，并在后续盲测中进一步检查科学概念和 scope。

## 10. GEO accession scope 修正与泛化门

### 10.1 发现的评测口径错误

早期 prompt 要求模型抽取整篇论文中的所有实验，而当前 CDM 数据流实际以“一条目标 GEO accession”为单位。旧 evaluator 又用 Sonnet 的 paper-wide experiment count 作为 gold，导致：

- accession-scope 的正确单实验输出可能被错判为不完整；
- paper 中独立 qPCR、训练或 validation cohort 容易污染目标 GEO 的 experiment/intervention 关系；
- 评测奖励“抽得更多”，而不是“是否属于当前 accession”。

### 10.2 确定性 `[TARGET GEO SCOPE]`

新增 `summarize_geo_scope(metadata_csv)`：

- 只使用目标 GEO metadata，不做论文级科学推断；
- 汇总 sample count、title、source、species、molecule、platform、instrument、library strategy 和 characteristics；
- 对多值列均匀抽样，而不是只取前 N 个，避免 metadata 先列 control、后列 exercise 时把处理臂截掉；
- 作为明确的 `[TARGET GEO SCOPE]` block 注入 design stage。

新的硬规则要求：

- extraction unit 是 target accession，不是整篇论文；
- 恰好一个 experiment 表示该 GEO 样本；
- 只提取实际施加于这些样本的 intervention；
- 排除独立 validation、follow-up training 和 paper-only assay；
- 多时间点仍属于同一 experiment；
- 覆盖 metadata 中每个实验轴；
- evaluator 检查跨 cohort/accession 关系污染和目标 intervention recall，而不再硬编码 experiment count。

### 10.3 Routine + multifactor 泛化

实验目录：[`deepseek_seacdm_generalization_20260818_145725`](../../output/deepseek_seacdm_generalization_20260818_145725/deepseek_seacdm_generalization.md)。

| 指标 | Routine GSE270703 | Multifactor GSE250122 |
|---|---:|---:|
| 通过 | 3/3 | 3/3 |
| 平均分 | 100 | 100 |
| provenance | 99.4% | 95.8% |
| material reference recall | 100% | 100% |
| GEO scope pass | 3/3 | 3/3 |
| 结构一致 | 是 | 是 |
| 中位延迟 | 112.154 s | 86.824 s |
| 每次成本 | $0.032936 | $0.026733 |

GSE250122 修正后只保留目标 GEO 对应的 60 分钟急性骑行、baseline/+30 min/+3 h 和 microarray，不再把论文中的独立 8 周训练/qPCR cohort 合并到同一 accession。

保存结果的 zero-call rescore 对 6 次运行全部判定：scope consistent、target intervention recall 100%、无 excluded-term hit。独立审计为 100/100、coverage 65.2%、0 blocking；27/27 artifacts 哈希通过，6/6 decisions grounded。

### 10.4 Microarray assay 识别修正

部分 GEO 没有 `library_strategy`。旧代码可能把 Affymetrix/CEL/hybridization 信息误标成 `high-throughput sequencing`。现在 `_infer_assay_name` 会从 platform、sample type、label/hybridization/scan protocol、data processing 和 description 中寻找保守证据；出现 Affymetrix、CEL、GeneChip、BeadChip 等信息时标记为 `microarray gene expression profiling`。

## 11. 冻结的未见 multi-accession 盲测

实验目录：[`deepseek_seacdm_blind_multicohort_20260818_162736`](../../output/deepseek_seacdm_blind_multicohort_20260818_162736/blind_multicohort_report.md)。

在首次模型调用前冻结：

- target accession：GSE197045；
- paper-only sibling accession：GSE198652；
- 论文和 metadata SHA-256；
- 必须出现的设计术语组；
- 必须排除的 RNA-seq/sibling accession 内容；
- 结构计数和评分权重。

目标是老年雌性 C57BL/6N 小鼠 soleus myonuclei RRBS，PoWeR vs sedentary，6 个样本；同一论文另有 GSE198652 RNA-seq。

结果：

- 3/3 通过；
- 三轮均保持 3 vs 3 分组；
- 正确保留 8 周 PoWeR、2/3/4/5 g 递增负重、22–24 月龄、Bisulfite-Seq/HiSeq 2000；
- experiment/intervention/assay 关系中没有 GSE198652 或 RNA-seq 污染；
- 平均 provenance 97.9%；
- 结构完全一致；
- 中位延迟 103.48 s；
- 平均成本约 $0.03211/run；
- 独立审计 100/100、coverage 65.2%、0 blocking；
- 16/16 artifacts 哈希通过，3/3 decisions grounded。

报告中的 exact intervention Jaccard 为 0，来源是整行字符串的措辞/标点差异，不是关键科学事实缺失。该指标被保留作为警示，但不单独推翻冻结概念门和 scope gate。

这次盲测支持的范围是：**DeepSeek staged + GEO metadata + target accession scope**。它不证明 DeepSeek 已适合 paper-wide、无 metadata 或要求整篇论文多实验建模的场景。

## 12. Exercise cohort、阴性路由与确定性 Exercise 投影

实验目录：[`seacdm_exercise10_ab_20260818_1730`](../../output/seacdm_exercise10_ab_20260818_1730/comparison.md)。候选 manifest 为 10 篇，最终有 8 篇形成可比较的双模型 artifact。

### 12.1 “目标 GEO 无运动臂”概念修正

这里的“阴性”不是论文结果为阴性，而是论文标题或背景含 exercise，但 target GEO 样本没有真实运动干预。例如：

- GSE282166：AAV8-Irisin vs AAV8-GFP；
- GSE315575：NOX4 KO vs control。

正确处理是保留病毒、药物、基因型等真实 intervention，同时允许 `exercise` 表为空。不能因为搜索关键词是 exercise 就强制每条 accession 产生 Exercise node。

旧 evaluator 无条件要求 exercise，得到 Sonnet 6/8、DeepSeek 5/8；改为 scope-conditioned requirement 后，原始抽取为 Sonnet 7/8、DeepSeek 6/8；进一步修正确定性 Exercise projection 后，两者均为 7/8。

### 12.2 Exercise node 的确定性生成

LLM 只负责抽取 intervention；Python 再从明确的 exercise-like intervention 生成 ontology-level Exercise node。核心修复是：

- 只检查 intervention 的 `material` 和 `intervention_type`；
- 不再把 comments 当作正向语义证据；
- 防止 `control group; no exercise intervention` 之类备注因为含 exercise 字样而误建节点；
- 支持 treadmill、wheel running、endurance/resistance/aerobic/sprint training、HIIT、MICT 等术语；
- Exercise node 保留 experiment/intervention FK、名称、类型、剂量/时长、t0 和 source。

### 12.3 成本与一致性

8 篇可比案例中：

- 结构表一致：8/8；
- 平均描述 token overlap：92.1%；
- Sonnet 总成本：$3.8592；
- DeepSeek 总成本：$0.2736；
- DeepSeek 成本为 Sonnet 的 7.1%。

该轮每模型每 study 只有 1 次，不测随机稳定性；结构相等部分也受到 metadata-derived deterministic tables 的影响，不能解读为所有描述字段完全一致。

### 12.4 GSE319603 定向修复

全量比较中两模型都遗漏/错误表达了 high-fat diet + MICT 轴。修正 prompt 和确定性 grouping 后：

| 指标 | Sonnet | DeepSeek |
|---|---:|---:|
| 结果 | pass | pass |
| interventions | 2 | 2 |
| exercise rows | 1 | 1 |
| groups | 3 | 3 |
| 成本 | $0.4880 | $0.0310 |
| 延迟 | 242.2 s | 112.7 s |
| 审计 | 89.5/100 @ 65.2% | 89.5/100 @ 65.2% |

正确的三个组是 control、high-fat diet、high-fat diet with MICT。因为这里只重新运行了单个失败案例，没有重新执行完整 8-study cohort，所以不能把全量结果直接宣称为 8/8。

## 13. Opus 5 stage-only fallback 资格测试

实验目录：[`seacdm_fallback_qualification_final_20260818`](../../output/seacdm_fallback_qualification_final_20260818/qualification_summary.md)。

设计原则：

- DeepSeek 负责主提取；
- Python 确定性 validator 决定是否需要 fallback；
- Opus 只修复 experiment/interventions stage，不重跑全文；
- 保留 DeepSeek 已正确的表；
- 限制付费调用数量和范围；
- 独立 concept rubric 不泄漏到模型 prompt。

案例：

| Study | 模式 | 结果 | Opus 调用 | 成本 |
|---|---|---:|---:|---:|
| GSE319603 | 已知 design repair | success | 是 | $0.169365 |
| GSE318937 | complex-design shadow | success | 是 | $0.229250 |
| GSE282166 | negative-route control | success | 否 | $0 |

最终 3/3 通过、付费 fallback 2/2 成功、negative route 1/1 正确跳过。首次 GSE318937 调用产生费用但因 schema 解析失败，加入 provider-compatibility coercion 后重试成功；因此总 billable calls 为 3，总成本 $0.628215。独立运行审计为 100/100、coverage 65.2%、0 blocking，6/6 artifacts 哈希通过。

必须保留的限制：

- 两个付费案例都只有一次最终成功运行，未满足随机稳定性 3-repeat 门；
- GSE318937 是强制 shadow，不是自然路由触发；
- GSE319603 在 prompt 修正后 DeepSeek 自己也能通过，因此真实 fallback 触发率尚未测量；
- 该结果证明“Opus 能修复受限 stage”，不证明“当前系统已经稳定知道何时调用 Opus”；
- 当前尚未正式接入生产级 DeepSeek → retry → Opus router。

## 14. Provenance、运行状态和成本可观察性

近期所有主要实验不再只保存一段最终文本，而是形成机器可审计目录：

```text
run_status.json
summary.csv / experiment report
workflow.log
evidence.json
agent_evaluation.json
agent_evaluation.md
per-run trace.json
decision_trace.json
seacdm_tables.json
seacdm_provenance.json
```

主要改进：

- `run_status.json` 记录 terminal status、阶段、耗时、LLM calls、估算成本、warning/failure 和 evidence IDs；
- `evidence.json` 统一 source、claim、decision 和 artifact，引用可做 dangling-ID 检查；
- artifact 保存 SHA-256，审计器会检测缺失和哈希漂移；
- SEA-CDM 每个 sourced 字段保存原文证据，quote 进行 verbatim verification；
- 无法逐字验证的 source 标记 `[UNVERIFIED]`，而不是悄悄保留；
- staged extraction 的每次尝试写入 decision trace；
- A/B 报告分开统计质量、覆盖率、成本、延迟和 blocking；
- 定价使用实验时的 pricing snapshot，避免后续价格变化破坏历史可复现性。

## 15. 新增实验与回归测试

### 15.1 新增实验入口

- `test/scripts/probe_model_compatibility.py`
- `test/experiments/model_agent_ab/run_experiment.py`
- `test/experiments/model_e2e_ab/run_experiment.py`
- `test/experiments/model_seacdm_ab/run_experiment.py`
- `test/experiments/deepseek_seacdm_staged_ab/run_experiment.py`
- `test/experiments/deepseek_seacdm_generalization/run_experiment.py`
- `test/experiments/deepseek_seacdm_generalization/rescore_existing.py`
- `test/experiments/deepseek_seacdm_blind_multicohort/run_experiment.py`
- `test/experiments/seacdm_exercise10_ab/{prepare_manifest,worker,compare}.py`
- `test/experiments/seacdm_fallback_qualification/{run,summarize}.py`
- few-shot A/B 的 scorer 和 rescore 脚本也同步强化。

### 15.2 新增/增强单测重点

| 测试模块 | 覆盖内容 |
|---|---|
| `test_model_factory.py` | provider、endpoint、model whitelist、thinking、structured budget、SEA-CDM provider、Opus 参数 |
| `test_runtime_skills.py` | metadata-only discovery、受控 reference、未知路径、重复名称 |
| `test_agent_run_audit_skill.py` | 完整 grounded run、缺 evidence 不得虚高、hash mismatch 阻断、失败终态阻断 |
| `test_fewshot_ab_scoring.py` | gold-like 输出、复制 accession 惩罚、log-scale→voom 阻断、平均分不能覆盖安全退化 |
| `test_seacdm_staged.py` | required-empty retry、invalid strategy、shape coercion、grounded title repair、trace |
| `test_seacdm_scope_policy.py` | compact scope、microarray 识别、硬 scope prompt、跨 cohort 拒绝、exercise semantics、blind sibling accession gate |
| `test_metadata_structural.py` | metadata-derived 结构和 assay/design 行为 |
| `test_sea_extract.py` | 分阶段容错与 SEA-CDM 表生成 |

在本次汇总前，使用仓库现有 `.venv` 执行：

```powershell
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe -m unittest discover -s test\unit -p 'test*.py' -v
```

结果：**63 个 `unittest` 全部通过，退出码 0**。同时由 import 触发的本地脚本式回归检查也通过，包括成本缓存、GSEA symbol sidecar、methylation、pathway chain、reported/computed agreement、scRNA pseudobulk 和 SEA-CDM 分组容错。运行后工作区保持干净。

当前虚拟环境没有安装 `pytest`，因此尚不能把 `pytest` 作为统一入口。这与仓库仍缺少 `pyproject.toml`/lockfile/CI 的已知工程债一致。

## 16. 当前部署建议矩阵

| 场景 | 当前建议 | 证据强度 | 备注 |
|---|---|---|---|
| 主 ReAct Agent 工具路由 | DeepSeek V4 Pro | 强 | 7 case × 3 repeat，零循环/阻断 |
| Cached-GEO DA 设计与执行 | DeepSeek V4 Pro | 强 | 3 case × 3 repeat，独立审计 100/100 @ 100% |
| Structured helper | DeepSeek V4 Pro，thinking off | 中强 | provider gate + model factory tests |
| GEO metadata-backed staged SEA-CDM | 支持 DeepSeek 候选/受控路由 | 中强 | 3 个已知 accession + 1 个未见 accession，均 3/3 |
| Paper-wide 或无 metadata SEA-CDM | Sonnet 4.6 | 当前最稳妥 | DeepSeek 尚未通过此模式 |
| SEA-CDM 全量默认切 DeepSeek | 暂不建议 | 不足 | 模式边界和第二个盲测仍需补充 |
| Opus 5 stage-only repair | 已资格测试，未生产化 | 初步 | 付费案例各仅一次；路由稳定性未测 |
| “模型自报置信度”触发 fallback | 不建议 | 不可靠 | 应由 Python 确定性 hard gates 决定 |

## 17. 仍需谨慎解释的地方

1. **100 分不代表所有维度都测了。**  
   DA E2E 的 100/100 覆盖率也是 100%，证据较完整；SEA-CDM staged/盲测的 100/100 只有 65.2% applicable coverage，科学有效性中的矩阵/方法、contrast、DEG sanity 本来不适用于抽取任务。

2. **结构一致不等于描述字段完全一致。**  
   subject/sample/groups/assay 很多来自 metadata 的确定性生成，结构稳定是预期行为；LLM 负责的 materials/findings 仍要看 provenance、recall 和人工语义核验。

3. **Exact Jaccard 对长描述行过度敏感。**  
   一处标点或措辞变化会让整行 tuple 不相等，因此必须与字段级 concept gate、fuzzy recall、provenance 和 domain review 联合使用。

4. **Exercise 8-study 比较只有一次/模型。**  
   它可以比较成本和发现具体失败模式，不能证明 run-to-run stability。

5. **Fallback 尚未有完整路由稳定性实验。**  
   需要固定正确/错误输出做 100 次零调用确定性测试，再做正例、无运动臂、多因素和未见案例的 3-repeat live test。

6. **联网 GSEA/ORA 不在 cached E2E A/B 中。**  
   DEG 选择与稳定性已测，但 Enrichr/MSigDB/MyGene 的网络可用性和跨运行缓存需要独立集成测试。

7. **paper-wide/no-metadata 是明确未覆盖区。**  
   当前 staged 方案的优势来自 GEO metadata 提供 scope；缺少 metadata 时不能假设同样可靠。

8. **依赖与 CI 尚未标准化。**  
   没有 `requirements.txt`、`pyproject.toml` 或 lockfile，`pytest` 未安装；当前可复现性依赖本机 `.venv`。

9. **文档存在轻微漂移。**  
   README 的首段仍笼统写“与 Claude”，部分 TODO 已被当前实现部分覆盖；后续应统一 README、STATUS、AGENTS 和实际 routing policy。

## 18. 推荐的下一阶段工作

### P0：把已验证模式变成显式生产路由

1. 增加明确的 SEA-CDM mode classifier：
   - `geo_metadata_staged` → DeepSeek；
   - `paper_wide` / `no_metadata` → Sonnet；
   - 不允许默默跨模式降级。
2. 每个模式在 `run_status` 和 evidence 中记录 provider、model、prompt/schema version、scope policy 和 fallback reason。
3. 给 DeepSeek staged 设置调用数、token 和成本上限。

### P0：完成确定性 fallback router

建议只由以下硬门触发：

```text
parse/schema failure
FK failure
required stage empty
metadata/sample count inconsistency
foreign GEO accession contamination
required experimental axis missing
scope-required exercise semantics missing
```

相同冻结输入重复评估 100 次必须得到完全相同路由。不要依赖自然语言 confidence、一般性 provenance 小幅波动或论文标题是否含 exercise。

### P1：补充 SEA-CDM 泛化证据

- 第二篇未见 multi-accession 论文；
- 一篇 paper-wide、无可用 GEO metadata 的对抗案例；
- 一篇多 intervention、多时间点但仍属于单 accession 的复杂案例；
- 对 materials/interventions/findings 建立字段级人工 gold，而不是只比较整行文本；
- 对自然 fallback 触发执行每案例至少 3 次重复。

### P1：扩展端到端评测

- 联网 GSEA/ORA + symbol mapping；
- 缩写型样本 LLM alignment fallback；
- FPKM/TPM-only 正确拒绝 DESeq2；
- small-n + implausible DEG 阻断；
- multi-factor no-clean-contrast refusal；
- full Agent final-answer grounding。

### P2：工程化

- 添加 `pyproject.toml`、依赖锁定和 `pytest`；
- 划分 offline/unit、integration、network、expensive markers；
- 建立 CI；
- 统一 README/STATUS/AGENTS；
- 将长期运行 trace 标准化为 `agent_trace.jsonl`；
- 为实验报告加入版本化 scorer/config hash。

## 19. 汇报时可使用的一句话结论

> 本阶段不仅把主 Agent 从 Sonnet 迁移到了成本约 2% 的 DeepSeek V4 Pro，而且通过分阶段提取、GEO accession 范围约束、独立审计和未见 multi-accession 盲测，明确了 DeepSeek 在 SEA-CDM 中“可以安全使用的模式”和“仍必须保留 Sonnet fallback 的模式”；同时建立了可复用的 runtime skill 与证据化 A/B 评测体系，使后续模型、prompt 和 workflow 改动都能按质量、覆盖率、安全性、稳定性和成本进行可核验决策。

## 20. 主要证据索引

| 主题 | 机器可读/报告产物 |
|---|---|
| Runtime skill A/B | [`docs/reviews/RUNTIME_SKILL_AB_20260805.md`](../reviews/RUNTIME_SKILL_AB_20260805.md) |
| DeepSeek compatibility | [`compatibility_report.md`](../../output/model_compat_deepseek_20260817_195548/compatibility_report.md) |
| Agent routing A/B | [`model_agent_ab.md`](../../output/model_agent_ab_20260817_200223/model_agent_ab.md) |
| Cached-GEO DA A/B | [`model_e2e_ab.md`](../../output/model_e2e_ab_20260817_202739/model_e2e_ab.md) |
| DA 独立审计 | [`agent_evaluation.md`](../../output/model_e2e_ab_20260817_202739/agent_evaluation.md) |
| 原始 SEA-CDM A/B | [`model_seacdm_ab.md`](../../output/model_seacdm_ab_20260817_221240/model_seacdm_ab.md) |
| Staged SEA-CDM A/B | [`deepseek_seacdm_staged_ab.md`](../../output/deepseek_seacdm_staged_ab_20260818_135506/deepseek_seacdm_staged_ab.md) |
| Scope 泛化 | [`deepseek_seacdm_generalization.md`](../../output/deepseek_seacdm_generalization_20260818_145725/deepseek_seacdm_generalization.md) |
| Zero-call scope rescore | [`scope_rescore.md`](../../output/deepseek_seacdm_generalization_20260818_145725/scope_rescore.md) |
| 未见 multi-accession 盲测 | [`blind_multicohort_report.md`](../../output/deepseek_seacdm_blind_multicohort_20260818_162736/blind_multicohort_report.md) |
| Exercise cohort A/B | [`comparison.md`](../../output/seacdm_exercise10_ab_20260818_1730/comparison.md) |
| Opus fallback qualification | [`qualification_summary.md`](../../output/seacdm_fallback_qualification_final_20260818/qualification_summary.md) |

---

### 文档口径

- “通过”优先采用冻结 experiment report 的 acceptance gate，而不是仅依据程序退出码；
- “审计分数”必须与 coverage 一起引用；
- 成本均为对应实验保存的估算值，不代表未来 provider 定价；
- 输出目录是本地实验产物，通常不纳入 Git；实验脚本、scorer、rubric 和本报告纳入版本管理；
- 本报告描述的是 `dev/ds@246abf9` 的证据状态，不自动代表远端 `main` 或已部署生产环境。
