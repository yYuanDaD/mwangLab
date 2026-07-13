# WORKFLOW.md 评审 + 当前代码演进思考

> 配套文档：`WORKFLOW.md`（导师转来的 ChatGPT 生成版本）
> 用途：明天会议讨论用。本文 **不实现任何代码**，只盘点现状 + 提改进点。

---

## 0. 术语速查（按软件视角）

- **SEA-CDM** —— 一份"运动研究的标准化字段表"。每个研究 → 一份结构化记录；字段涵盖运动协议、受试对象、检测结果等。本质就是 schema。
- **本体（ontology）** —— 受控词表 + is-a 关系。把研究里的自由文本（"endurance training"、"Type 2 diabetes"）映射成稳定 ID（`EXAO:xxx`、`MONDO:xxx`），方便跨研究查询。
- **三个 agent** —— 等价于一条 ETL：Curation = E（抽取）/ Mapping = T（规范化）/ Review = QA。

---

## A. 当前代码 ↔ WORKFLOW.md 映射（gap 分析）

| WORKFLOW.md 角色 | 当前 mwangLab 实现 | gap |
|---|---|---|
| Agent A Step 1 收集材料 | 无 | 全新（用户上传层 + 文件登记） |
| Agent A Step 2 在文档中识别 protocols/results | 无 | 全新（**PDF 解析 + section 分段**） |
| Agent A Step 3 抽取 SEA-A process | 无 | 全新（依赖 SEA-A 定义先落地） |
| Agent A Step 4 识别 protocol 里的 SEA-CDM 类 | 无 | 全新 |
| Agent A Step 5 刻画 results 里的 SEA-CDM 类 | `extract_sea_cdm_conditions` | **复用** Pydantic-structured-output 模式 |
| Agent B Phase 1 选本体 | 无 | 全新（也许不需要——见 §C 第 5 点） |
| Agent B Phase 2 term→ontology id | 无 | 全新（**需要本体索引基础设施**） |
| Agent C 评审 | 无（但 `validate_contrast_with_llm` 是同构的"LLM 复核"模式） | 全新但模式已有 |
| §6 Analysis sub-agent（出 plan） | 隐式藏在 system prompt + ReAct loop | 没拆出来 |
| §6 Coding sub-agent（执行 plan） | **几乎就是当前 batch_tools + tools/**（download → preprocess → QC → DESeq2 → GSEA） | **基本就绪** |
| 子循环上限 | `guard_tools(max_calls_per_tool=3)` | 模式同构 |
| Provenance | 部分（`workflow.log` + `summary.csv` 的 `llm_reasoning` 列） | 未结构化、未关联到字段 |
| 复现性 | 弱（无 prompt hash、无响应缓存、无 ontology 版本钉死） | 全新 |

**结论**：现在 90% 的代码量在 §6 Coding Agent；A/B/C 三层是全新工作。

---

## B. 演进路线（推荐"加壳"而非"重写"）

三个备选：

| 方案 | 工作量 | 风险 |
|---|---|---|
| (1) 按 WORKFLOW.md 全新重写 | 大（2-3 个月） | 现有代码作废、LLM 兜底经验丢失 |
| (2) **现有代码降级为 §6，外层加 A/B/C 三层 agent** | 中（按层增量） | 需要明确 Agent A ↔ §6 的接口契约 |
| (3) 暂不动代码，先把 WORKFLOW.md 的歧义/TODO 全部消干净 | 小 | 不出代码进展 |

**推荐：(2) + (3) 并行做。**

(2) 的增量顺序：
1. 把 `extract_sea_cdm_conditions` 提升为 Agent A Step 5 的实现
2. 在外层加 PDF → sections 抽取器（Step 2-4 的前提）
3. 加 Analysis Agent 的 plan schema，让现有 batch_tools 接受 `AnalysisPlan` 作为输入而不是裸 keyword
4. Agent B / Agent C 都靠 `with_structured_output` 一次性出，模式照搬 `validate_contrast_with_llm`

---

## C. WORKFLOW.md 可以改善的地方（按优先级三档）

### 🟥 必须开会确认才能动手的（doc 阻塞）

1. **§2.2 `SEACDMRecord` 全 TODO** —— 这是整个系统的合同。SEA-CDM 论文里的实际字段列表必须落到 doc 上，才能给 Agent A 出口、给 Agent B 入口、给入库定列。
2. **§12 `SEA-A` 定义 TODO** —— Step 3 抽取的对象本身没定义。
3. **§3 Step 2 → §6 子循环的触发条件没说** —— 写明"什么 missing field + 什么 repo accession → 触发"，否则要么全触发要么全不触发。

### 🟧 设计层歧义（应该 v2 文档修掉）

4. **§3 五个 step 粒度不齐**：Step 1 是数据装配不是 agent 工作；Step 3 vs Step 5 是不是同一次 LLM 调用没说。建议每个 step 显式说"一次 LLM call 一份 Pydantic 输出"。
5. **§4.1 Phase 1 鸡生蛋**：没看 term 前怎么选本体？三种解法选一：
   - (a) §2.2 schema 里就把字段绑定到本体（推荐）
   - (b) 合并进 Phase 2 按 term 决定
   - (c) 整条记录看完后路由
6. **§4 置信度 0.85 / 0.60 没说 metric**：embedding cosine 和 LLM 自评分的 0.85 分布完全不同，必须指明。
7. **§5 Agent C Step 7 "characterize remaining documentation" 是抽取不是评审**，应归并到 Agent A。Agent C 留给跨字段一致性。
8. **§6 子循环结果回灌路径缺失**：`SecondaryResults` 怎么进 `SEACDMRecord` 没说。

### 🟨 工程层决策（应该 v1 实现前选定）

9. **§9 "no LangGraph in v1" vs 现有 LangChain 代码冲突**：建议改成"外层 3-agent 用纯 SDK，§6 子循环允许复用现有 LangChain 代码"。
10. **§6 sandbox TODO 是大决策**：你当前是 in-process 跑；如果 Coding Agent 要执行 LLM 生成的代码必须沙箱化（推荐 Docker per-study）。如果 Coding Agent 只是 dispatch 到预定义工具（像现在 mwangLab 做的），就不需要沙箱。**这两条路线差异巨大，先选**。
11. **没提缓存 + 成本预算**：估算每研究 50-100 次 LLM 调用，必须加 prompt-hash 响应缓存 + per-study $$ 上限。
12. **"reproducibility seed where supported" 误导**：Claude 不暴露 seed，复现靠模型版本钉死 + prompt hash + 响应缓存。
13. **§8 "route back to A or B" 手挥**：需要一张 `issue.kind → re-entry 点` 的映射表。

---

## D. 明天会议建议的讨论顺序

1. **拿 SEA-CDM schema 实表**（解锁一切）
2. **定义 SEA-A 到底是什么**
3. **§4.1 ontology 选择时机选哪条路**（直接决定 Agent B 架构）
4. **§6 sandbox 路线选定**（直接决定要不要重做）
5. **现有 mwangLab 代码做 §6 的复用方案讨论**（节约 2-3 个月）

---

## E. 小问题清单（可不在会议讨论，doc 修订时一并处理）

- §10 "Out of Scope" 把 Web UI 排除，但 §7 又说 human reviewer 必须看 ReviewReport。CLI 看 JSON 太痛苦，至少要 markdown render。
- §1 没有定义如果 PDF 加密 / 扫描件（无 OCR 文本）怎么 fallback。
- §4.2 step 2 "synonym expansion" 没指明来源（手工词表？UMLS？OLS 同义词字段？）。
- §6 `AnalysisStep` 自己也是 TODO，没在 §2 定义。
- `download_supplementary_files` 当前每次都重下，做 cohort 大量浪费——演进新框架时顺手 fix。

---

## F. 当前代码现状速报（一句话版）

LangChain `create_agent` + Claude Sonnet 4.6 跑通的 GEO RNA-seq 全自动 pipeline：

- **单 study**：download → preprocess → QC（PCA / corr heatmap / sample QC）→ DESeq2 → GO/KEGG ORA + MSigDB Hallmark GSEA → SEA CDM 抽取
- **批量**：keyword 搜 GEO → 自动挑 cohort → 每个研究跑上述全流程 → 出 `summary.csv` + `workflow.log`
- **两条 LLM 兜底**：
  - A. Contrast validation（修关键词覆盖不到 / refuse off-topic study）
  - B. Sample alignment（解码 `HC_F1_TL_S54_L003` ↔ `HomeCage1_Female1_TotalLysate` 这种缩写）
- **结构性护栏**：`guard_tools` 限流；`align_samples` 拒绝位置 fallback；`_classify_matrix` 拒 FPKM/TPM；DEG 文件名 sanitize。

详细模块映射见 `CLAUDE.md`。
