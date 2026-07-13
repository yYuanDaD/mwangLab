# STATUS2 —— Agent A 阶段项目状态


> 记录 **Agent A(文献→数据→13 表 SEA-CDM)** + **DA 方法矩阵** + **蛋白组** + **验证/防幻觉** 全部新工作。

---

## 一、项目目标(Agent A 阶段)

 **从一篇科学文献自动抽出可入库的 SEA-CDM 结构化记录**,并在能拿到数据时跑完差异表达分析:

```
关键词  →  检索论文  →  取全文  →  判定"自有 vs 引用"GSE  →  抽取 13 张 FK 互联的 SEA-CDM 表  →  对自有 GSE 跑 DA  →  回填 analysis/results
```



---

## 二、技术栈

| 项 | 选择 | 备注 |
|---|---|---|
| 文献检索 | **Semantic Scholar API**(`S2_API_KEY`) | 关键词→排序论文列表 |
| 全文获取 | **Europe PMC**(handle / search_index 制) | 句柄式抓取 + bogus-PMCID 拒绝(防幻觉) |
| 结构化抽取 | `with_structured_output(Pydantic)` + `mode='before'` 强制类型矫正 | Sonnet 偶发把 list/对象序列化成 JSON 字符串,靠 coercion validator 兜 |
| DA 后端矩阵 | DESeq2 / edgeR / limma-voom / limma-trend | 见 §六 |
| limma-voom | **R `limma::voom` via Rscript** | inmoose 无 voom;装了 R 4.6 + limma |
| 蛋白组 | inmoose.limma(纯 Python) | matrix-in,见 §六 |
| 验证 | concordance(logFC 相关性)对 MoTrPAC / 参考 DEG | 见 §七 |

---

## 三、Agent A 工具层

### 1. 文献检索 + 取全文(`paper_tools.py`)
- `search_papers(keyword, require_pdf, max_results, ...)` —— Semantic Scholar 检索,返回排序论文 + `openAccessPdf`,存 `papers.csv`
- `fetch_paper_text(search_index)` —— **句柄式**抓全文(Europe PMC + PDF 兜底 + guards);直接传 bogus PMCID 会被防幻觉守卫拒绝
- `choose_own_gse(text)` —— 扫正文里的 GSE 编号,判 **own / cited / ambiguous**,返回 `(chosen_gse, ownership, classes)`
- `verify_provenance` —— 逐字段核验 LLM 抽取的 `*_source` 引文是否在原文**逐字出现**;非逐字标 `[UNVERIFIED]`

### 2. Cohort 编排(`cohort_tools.py`)
- `run_agent_a_cohort(keyword, max_papers, search_pool, with_analysis, raw_da_method, ...)` —— 三阶段:
  - `[1/3]` `search_papers(max_results=search_pool)` → 取前 `max_papers` 篇
  - `[2/3]` 逐篇:`fetch_paper_text` → `choose_own_gse` → `extract_tables_from_text`(3 次分组结构化抽取)→ `verify_provenance` → `append_tables_to_csvs`
  - `[3/3]` `with_analysis=True` 时,对**严格自有(own)**的 GSE 调 `run_batch_geo_pipeline` 跑 DA,回填 `analysis`/`results` 行
- 产出 `cohort.log`(逐篇决策追溯)+ `papers.csv`(每篇 manifest,含 `prov_verified/prov_unverified`)

### 3. 13 表 SEA-CDM 抽取(`seacdm_tools.py` v1)
- `extract_tables_from_text(study_id, text, organism)` —— 用 3 个**扁平分组** Pydantic schema(StudyLevel / Design / Methods)强制结构化输出 → 拆成 13 张表
- **确定性 ID/FK**:study_id、experiment_id、group_id 等由代码按规则生成,**LLM 从不发明 ID**
- `Sourced(value, source)` → 落盘为 `<field>` + `<field>_source` 两列


### 4. DA 方法矩阵(`deseq2_tools.py` / `edger_tools.py` / `limma_voom_tools.py` / `limma_tools.py`)
- 见 §六

### 5. 蛋白组(`proteomics_tools.py`)
- `identify_proteomics_labeling` → `download_pride_project` → `preprocess_proteomics_matrix`,见 §六

---

## 四、Agent A 端到端流程

```
用户关键词 (e.g. "exercise RNA-seq")
  ↓
[1/3] search_papers → 排序候选 N 篇 (search_pool) → 取前 max_papers 篇
  ↓
[2/3] 对每篇 (top max_papers):
  fetch_paper_text(handle)  →  正文
    ↓
  choose_own_gse → (chosen_gse, ownership)   # own / cited / ambiguous
    ↓
  extract_tables_from_text → 13 张表 (3 次分组结构化抽取)
    ↓
  verify_provenance → 逐字段核验引文;非逐字标 [UNVERIFIED]
    ↓
  append_tables_to_csvs → 追加到 cohort 级 13 CSV + 写 per-study json
  ↓
[3/3] with_analysis: 对所有 own GSE 调 run_batch_geo_pipeline
  ↓ (复用 `docs/status/STATUS.md` 的 DESeq2/limma + GSEA 后端)
  回填 analysis.csv / results.csv
  ↓
返回文本报告 + cohort 目录
```

---

## 五、13 表 SEA-CDM 关系模型

一个**关系模型**,`study` 是父表,其余按一对多向下展开或按业务条件收敛。FK 串联:
`study → experiment → groups → sample → assay → analysis → results`,旁挂 `subject / material / interventions / occurence / documentation / ontology`。

| 表 | 粒度(一行=) | 备注 |
|---|---|---|
| study | 一篇论文 | 父表,行数 = 处理的论文数 |
| documentation | 一篇论文的文献条目 | 一对一 |
| experiment | 论文内一个子实验/设计 | 一篇可多个 |
| subject | 一类受试对象 | |
| groups | 一个实验分组 | 对照/处理 × 组织 × 性别 × 时间 展开 |
| sample | 一个样本 | |
| material | 一份生物材料 | 最细粒度 |
| assay | 一次测定 | |
| interventions | 一个干预手段 | |
| analysis | 一次差异表达分析 | **仅对 own-GSE + with_analysis 才有行** |
| results | 一条 DEG 结果 | **仅当 DA 真算出 DEG;失败留空(fail-loud)** |
| occurence | 一个表型/疾病事件 | 抽不到则空 |
| ontology | 本体映射 | **按要求交给 Agent B,A 不产行;`*_name_id` 列直接省略** |

**空表/空列的含义**(已实测确认):`results`/`occurence` 空 = fail-loud 或没抽到;`ontology` 空 + 无 `_name_id` 列 = 按规范跳过;部分 `*_id` 空 = 可选外键未接。**均非数据损坏。**

---

## 六、DA 方法矩阵 + 蛋白组

**矩阵类型 → 方法**(`batch_tools._classify_matrix` 分类 → matrix-type dispatch):

| 矩阵类型 | 方法 | 后端 | da_method_reason 记录 |
|---|---|---|---|
| 原始计数 raw_counts | DESeq2 / edgeR / limma-voom | pydeseq2 / inmoose / R limma::voom | `raw_da_method='auto'` 时 LLM 选 |
| FPKM/TPM(线性) | limma-trend | inmoose.limma(log2 后) | ✅ FPKM/TPM **可分析**,见下 |
| log_transformed | limma-trend | inmoose.limma(直接) | |
| 蛋白组强度 | limma | inmoose.limma | matrix-in,IRS for TMT 待办 |

- **FPKM/TPM 能分析**:`fpkm_or_tpm → _log2_transform_matrix → run_limma_analysis`(limma-trend)。"限制"仅指**不能对其跑 DESeq2**(模型要整数计数)。
- **edgeR / limma-voom** 均已 SHIP(2026-06-01)。limma-voom 走 Rscript 调真 R(inmoose 无 voom)。
- **蛋白组**:`identify_proteomics_labeling → download_pride_project → preprocess_proteomics_matrix`,端到端验证于 PXD025560(DIA-LFQ, 3286×208)。

---

## 七、验证结果

**验证哲学 = concordance(不是 bit-exact)**:logFC Pearson/Spearman、符号一致率、ref-sig 召回;**headline = ref-sig 基因上的 logFC 相关性**


### 7.0 验证数据源(ground-truth 从哪来)

- **`new_deg3`(运动 DEG 真值库)** —— RNA-seq 的参考真值。limma 预先算好的**运动差异表达 ground-truth**,3 个数据框(**mouse / human / scRNA**),每条 DEG 带 `EGDB_ID`(Exercise Gene DataBase ID)+ `logFC`/`adj.P.Value`。覆盖 **43 个鼠 + 61 个人 series**(`data/_validation/new_{mouse,human}_series_manifest.csv`)。
  - 派生为 `data/_validation/ref_GSE*.csv` 共 **6 个**:`GSE132520 / GSE117161 / GSE151066 / GSE163356 / GSE164798 / GSE202295`。
  - **headline 用 2 个**(进下方 7.1 表):`GSE132520`(FPKM,limma-trend)、`GSE117161`(raw counts,DESeq2/edgeR/voom)。
  - 另外 **4 个(GSE151066/163356/164798/202295)已派生、做过探针,但未进 headline**(`master_concordance.csv` 不含 → **无 concordance 数字**,如实标注,非遗漏)。
- **MoTrPAC `PROT_DA`** —— 蛋白组的参考真值(`MotrpacRatTraining6moWATData` 的 PROT_EXP/PROT_DA),用于 MoTrPAC-WAT limma 那一行。
- **验证口径** = concordance(logFC 相关性)

### 7.1 跨方法 vs 参考/MoTrPAC ground-truth(`output/deliverables/master_concordance.csv`)

| 研究 | 模态 | 矩阵 | 方法 | headline logFC-corr (ref-sig) |
|---|---|---|---|---|
| GSE132520 | RNA-seq | FPKM | limma-trend | **0.951**(WT) / 0.937(pooled) |
| GSE117161 | RNA-seq | raw counts | DESeq2 | **0.977** |
| GSE117161 | RNA-seq | raw counts | edgeR | **0.977** |
| GSE117161 | RNA-seq | raw counts | limma-voom | **0.978** |
| MoTrPAC-WAT | proteomics | 强度 | limma | **0.997**(全 0.986) |

### 7.2 方法内部一致性(`internal_consistency.csv`,GSE117161 raw counts)

| 方法对 | logFC Pearson |
|---|---|
| DESeq2 vs edgeR | 0.989 |
| DESeq2 vs limma-voom | 0.953 |
| edgeR vs limma-voom | 0.937 |

**结论**:四种 DA 方法 + 蛋白组 limma 全部与 ground-truth 高度一致,方法间互相吻合。验证产物(报告 + 散点图)在 `output/deliverables/`。

---

## 八、防幻觉 / Provenance 栈

| 机制 | 作用 |
|---|---|
| 确定性 ID/FK | LLM 永不发明 ID,代码按规则赋值 |
| 句柄式取全文 + bogus-PMCID 拒绝 | 防止 LLM 编造文献来源 |
| GSE 字面交叉核对 | own/cited 判定基于正文实际出现的编号 |
| `verify_provenance` | 逐字段核验 `*_source` 引文逐字出现;非逐字标 `[UNVERIFIED]`|
| `_CoerceJSONContainer`(mode='before') | 矫正 Sonnet 偶发把 list/对象序列化成 JSON 字符串 |
| `guard_tools` | dedupe + per-tool cap,结构性阻止循环 |

| fail-loud align/classify | 拒绝位置 fallback、显式 reason code、拒非整数喂 DESeq2 |

---

## 九、输出工件清单

```
output/agentA_cohort_{label}/
├── papers.csv              # 每篇 manifest:study_id/chosen_gse/ownership/n_experiments/
│                           #   analyzed/da_method/status/prov_verified/prov_unverified
├── cohort.log              # 逐篇决策追溯([1/3][2/3][3/3])
├── csv/                    # 13 张 cohort 级 SEA-CDM CSV(见 §五)
├── studies/{study_id}/     # per-study json
└── cohort_analysis/        # with_analysis 时:summary.csv / workflow.log / failures.log
                            #   + 每 own-GSE 的 DA 工件 + decisions.json

output/deliverables/        # 明细化交付物
├── DELIVERABLES_REPORT.md  # 主报告(5 组件 + 验证主表 + 散点图 + bug + 限制)
├── DEMO_RUNBOOK.md         # 演示脚本 + Q&A 速查
├── master_concordance.csv  # 验证主表
├── internal_consistency.csv
├── component_inventory.csv
└── plots/*.png             # our-vs-ref logFC 散点图 ×6
```

---

## 十、真实运行结果

### test2 —— "exercise RNA-seq",3 篇 + 含分析(2026-06-02)
- 检索 30 篇 → 处理前 3 篇。
- 3 篇:1 own(GSE242358)/ 2 引用或无 GSE。
- 抽取:13 表正常,出处核验 125/135、79/97、118/126 逐字通过,其余标 [UNVERIFIED]。
- 分析:GSE242358 `deg_failed` —— **根因实测**:它是 MoTrPAC 多组学 SuperSeries,GEO 上只有 RRBS 甲基化 cov 文件(416 个),RNA-seq 只在 SRA 是原始 reads,**无表达矩阵可分析**(数据可得性限制,非 bug)。

### test3 —— "exercise RNA-seq",**8 篇 + 含分析**(2026-06-05,本次)
- 参数:`max_papers=8`,`search_pool=50`,`with_analysis=True`,`raw_da_method='auto'`。检索 50 篇 → 处理前 8 篇。
- **归属判定**:8 篇里 **3 篇自有 GSE**(GSE208615 / GSE214284 / GSE242358),5 篇引用他人/无 GSE(按 PMCID 入库)。
- **抽取**:8 篇全出表,出处核验逐篇通过率见 `papers.csv`;**PDF-only 的 #7(无 PMCID)逐字率明显偏低 22/81**(PDF 抽文有空白/断行噪声,如实记录)。
- **13 表产出**:study=8,experiment=17,groups=63,material=213,**analysis=3,results=3(非空!)**。
- **分析(Phase 3,3 个 own GSE)**:
  - **GSE208615 → `deg_gsea_ok` ✅**(端到端跑通):FPKM 矩阵 → **limma-trend** → 2 DEG(padj<.05)+ 18 GSEA 显著。`da_method_reason` 已填(**Bug B 修复生效**);**LLM-A contrast 校验 override**:解码出 `exercise parameters` 列里 `0-0-0`(n=20)=久坐对照、`14-0-0`(n=10)=运动,启发式没提这列。
  - **GSE242358 → `skipped_no_matrix_file`**:**对比 test2 的误导性 `deg_failed`,本次正确以明确原因跳过**(`counts_detection: skip | no_matrix_file`)——**Bug 8 修复 + fail-loud 在真实数据上直接验证**。
  - **GSE214284 → `skipped_no_matrix_file`**:单细胞(scRNA,ME/CFS),无 bulk 表达矩阵,正确跳过。



---

## 十一、Bug 修复(verify_bugfixes.py 现 10/10,均带回归守护)

| # | Bug | 修复 |
|---|---|---|
| 1-6 | 早期健壮性(filename sanitize、TSV NaN、对齐 cascade、scoring design 等) | 见 `docs/status/STATUS.md` §九 |
| 7 | LLM 把 list 字段序列化成 JSON 字符串 → ValidationError | `_CoerceJSONContainer` mode='before' 矫正 |
| 8 | phenotype/viallabel 元数据文件被误当表达矩阵 | `_NONEXPRESSION_NAME_HINTS` 加 phenotype/viallabel/clinical/sdrf 等 |
| 9 | 出处核验对省略号拼接引文误判 | `_quote_is_verbatim` 拆片段核验 |
| 10 | tar 合并静默丢样本 | 记录跳过项 + 打印 `WARNING: skipped K/N` + `M/N merged` |
| B | limma-trend 分支缺 da_method_reason | 两个分支补 reason |



---

## 十二、数据覆盖架构(路线图)——"什么数据都能分析"

把"任意数据"重定义为有限的 **{模态 × 处理阶段}** 网格,用 **LLM 路由 → 有限后端注册表 → fail-loud 兜底** 的分发器逐格填绿。

| 模态 \ 阶段 | 原始 reads(SRA) | 处理后矩阵 | 现状 |
|---|---|---|---|
| Bulk RNA-seq | 需重定量 | 计数/FPKM/log | 🟢 矩阵已支持 |
| 微阵列 / 蛋白 / 代谢组 | — | 强度矩阵 | 🟢/🟡 可复用 limma |
| DNA 甲基化(RRBS) | 需重定量 | cov/β | 🔴→可低成本转🟢(β→M值→limma) |
| ATAC / scRNA / 变异 | 各异 | peak/稀疏/VCF | 🔴 路线图 |

**推进顺序**:P0 补全跳过原因码(`methylation_only`/`sra_only_no_matrix`)→ P1 甲基化 M值+limma → P2 "矩阵升级阶梯"(GEO series 级 / 作者门户,绕开 SRA)→ P3 SRA→matrix(salmon,慎重)。

### 真实佐证(test3 两个跳过的 GSE 各落在不同空白格)

test3 的 3 个 own-GSE 里,2 个被 `skipped_no_matrix_file`——**它们卡在网格的不同位置,正好佐证 P1 与 P3 各自的必要性**:

| GSE | 实际数据 | 卡在哪个格 | 性质 | 需要 |
|---|---|---|---|---|
| **GSE214284**(scRNA, ME/CFS) | `*_filtered_feature_bc_matrix.h5`(10x CellRanger 稀疏矩阵,在 RAW.tar 内) | **scRNA × 矩阵** | **"有数据,没工具"**——`.h5` 二进制读不了,且需 pseudobulk/scanpy 而非 bulk DESeq2/limma | **P1 新模态工具**:`.h5` reader + scRNA/pseudobulk 后端 |
| **GSE242358**(MoTrPAC 多组学) | RNA-seq 仅 SRA 原始 reads;附带 416 个 RRBS 甲基化 cov | **RNA-seq × 原始reads** + **甲基化 × 矩阵** | **"没矩阵数据"为主 + 甲基化"没工具"为辅**——加 reader 也没用,RNA-seq 得回 SRA 重定量 | **P3 SRA→矩阵**(RNA-seq)+ **P1 甲基化后端**(cov→M值→limma) |


---

## 十三、已知限制

1. **SRA-only / 仅甲基化的多组学 SuperSeries**(如 GSE242358)—— 无表达矩阵,正确跳过;需 P1-P3 扩展才能覆盖。

2. **FPKM/TPM-only** —— 能跑 limma,但跑不了 DESeq2(数据缺整数计数)。

3. **search 关键词相关性排序** —— 待加强(backlog)。
4. **429 API 限流** —— 套餐层级,代码层无解。

---

## 十四、关键工程决策

1. **确定性 ID + LLM 只填内容** —— 关系完整性由代码保证,LLM 不碰 ID/FK。
2. **逐字段出处可核验** —— `*_source` 列 + `verify_provenance` 逐字核对,非逐字即标记,不假装可信。
3. **矩阵进、不做 reads→矩阵** —— Agent A/蛋白组刻意定在 DA 层;SRA 重定量是单独的范围决策,不默认承担。
4. **concordance 而非 bit-exact** —— DA 方法验证用 logFC 相关性 + ref-sig 召回,符合生物学现实。
5. **fail-loud 贯穿** —— 分类/对齐/分析失败一律显式跳过 + 原因码,空表/空列有明确语义,绝不造数据。
6. **LLM 当兜底路由器** —— 分类/对齐/contrast 校验都用 LLM 兜底 Python 启发式,失败回退,永不阻塞。
