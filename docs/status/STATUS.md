

## 一、项目目标

构建一个能自动跑 GEO RNA-seq 全流程的 bioinformatics agent，最终输出可入库的 SEA CDM 结构化记录。覆盖：

- **单 study 路径**：用户给一个 GSE 编号或自然语言需求 → agent 自动跑完
- **批量处理路径**：用户给一个生物学关键词（"Exercise"、"Diabetes"）→ 自动搜 GEO → 批量处理 top + random N 个研究 → 进行统计，得到批量级 summary

---

## 二、技术栈最终决定

| 项 | 选择 | 备注 |
|---|---|---|
| Agent 框架 | LangChain `create_agent`（ReAct loop） | 简单够用，比 LangGraph 轻 |
| LLM | 主 agent/DA 默认 **DeepSeek V4 Pro**；SEA-CDM 生产长文抽取仍用 **Claude Sonnet 4.6**（`tools/model_factory.py`, `seacdm_tools._get_llm`） | staged 候选加入 GEO accession 范围约束后，GSE208615、GSE270703、GSE250122 均 3/3；GSE250122 是同案修复验证，仍需未见 multi-cohort 论文后再考虑切生产 |
| 结构化输出 | `with_structured_output(PydanticSchema)` | 关键工具的输出全部走这条路 |
| 计算依赖 | pydeseq2 / gseapy / mygene / sklearn / pandas | 都在 `.venv` 里 |


---

## 三、工具层（`tools/*.py`）

### 1. 数据获取（`geo_tools.py`）
- `search_geo_studies(keyword)` —— NCBI E-utilities 搜 GEO series，每个 hit 标 `has_counts_like_supp`，存 `output/search_{keyword}.csv` 和 `output/geo_search_{keyword}.csv`
- `download_geo_data(accession)` —— GEOparse 拉 SOFT，输出 expression matrix CSV + metadata CSV 到 `data/{accession}/`
- `download_supplementary_files(accession)` —— 拉 supplementary，`.xlsx → .csv` 自动转，`_RAW.tar` 不在这里拆
- `fetch_geo_description(accession)` —— 拿 GEO 页面 title / summary

### 2. 元数据 & 设计推断（`deseq2_tools.py` + `batch_tools.py` 内部）
- `inspect_metadata(metadata_csv)` —— 列出潜在分组列 + unique values
- `_auto_detect_design`（批量内部）—— **评分式**挑设计列：+1 base、+1 列名含 treatment/condition、+1 两组 ≥3 样本；并且只有"匹配 ctrl 关键词且不匹配 treat 关键词"的值才算 control（避免"sedentary control"两边都中）
- `_find_raw_counts_file` —— 启发式挑 counts 文件，排除 `*_metadata.csv`，分类标签：raw_counts / fpkm_or_tpm / log_transformed / ambiguous_decimal
- `_unpack_and_merge_geo_tar` —— `_RAW.tar` → 每个 `GSM*_label.txt.gz` 解码 → 取最右侧数值列（跳 `#` 注释）→ 按 gene_id 合并成 `{accession}_merged_from_tar.csv` → 再次过 `_classify_matrix`

### 3. 预处理 + QC（`preprocess_tools.py` + `stats_tools.py`）
- `preprocess_counts` —— 删全 NaN 注释列 → 过滤低表达基因 → log2(CPM+1) 归一化。所有 read 点都用 `sep=None, engine="python"` 让 csv.Sniffer 自动判分隔符
- `sample_qc_summary` —— 每样本 library size / 检测到的基因数等
- `run_pca` —— 主成分散点图，可选按 metadata 某列着色
- `sample_correlation_heatmap` —— pearson/spearman 样本相关性热图
- 三个 QC 工具入口都有 `_reject_if_metadata`（防止用户把 metadata 当 counts 传入）

### 4. 差异表达（`deseq2_tools.py`）
- `run_deseq2_analysis(counts_csv, metadata_csv, design_column, control_group, treatment_group)`
- 内部流程：读 → 样本对齐（`align_samples_with_llm_fallback`）→ 转置成 rows=samples → intersection → 二组过滤 → 整数转换 → PyDESeq2 拟合 → 按 padj 排序保存
- 输出文件名经 `deg_filename(treat, ctrl)` sanitize（处理 `db/db`、空格、Windows 非法字符）

### 5. 富集分析（`enrichment_tools.py`）
- `run_enrichment_analysis` —— ORA against Enrichr（GO BP/MF/CC + KEGG），Ensembl ID 自动经 MyGene.info 转 symbol
- `run_gsea_analysis` —— preranked GSEA against MSigDB Hallmark；mouse 用 `mh.all @ 2024.1.Mm`，human 用 `h.all @ 2024.1.Hs`；依赖 `lxml`

### 6. SEA CDM 抽取（`seacdm_tools.py`）
- `extract_sea_cdm_conditions` —— 用 `SEACDM_Record` Pydantic schema 作 `args_schema`，强制 LLM 出结构化数据，存 `output/{study_id}/seacdm.json`

### 7. 共享工具
- `sample_align.py::align_samples` —— 三段 cascade：**exact → substring（带 `used` 集合防止双重指派）→ token-overlap（≥3-token Jaccard）**。**故意不做位置 fallback**（会静默产生生物学错误的 DEG）
- `guards.py::guard_tools(tools, max_calls_per_tool=3)` —— dedupe + per-tool cap，结构性阻止 LLM 循环

### 8. LLM 辅助（`llm_helpers.py`）
- **A. `validate_contrast_with_llm`** —— `_auto_detect_design` 之后调一次。三路径：confirm / override `(col, ctrl, treat)` / refuse；返回 `ContrastValidationResult`
- **B. `align_samples_with_llm_fallback`** —— `align_samples` 三策略全失败时调；LLM 解码缩写返回 mapping；mapping 经验证（剔除未知 ID/列/重复）后才采纳
- 两者失败都回退到 Python 启发式答案，**永不阻塞 pipeline**

### 9. Cohort 编排（`batch_tools.py`）
- `run_batch_geo_pipeline(accessions, treatment_keywords, control_keywords, run_label, source_search_csv?)`
- 每个 study 流程：download → 找 counts 文件 / 必要时拆 tar → preprocess → QC → `_auto_detect_design` → **LLM A 验证** → DESeq2 → GSEA
- 单 study 失败被 catch → `failures.log`，cohort 继续跑
- in-process Tee 把全部 stdout/stderr（含 pydeseq2、gseapy 日志）写到 `workflow.log`
- 给了 `source_search_csv` → workflow.log 顶部 snapshot 对应行做溯源
- 输出 `summary.csv`（含 status / n_deg / n_gsea_sig / `llm_validated` / `llm_overrode` / `llm_reasoning` 三新列）

---

## 四、单 study 端到端流程

```
用户自然语言 (e.g. "分析 GSE266241")
  ↓
Claude 解析 → 决定调哪个工具
  ↓
[guard_tools 拦截：dedupe + 调用次数检查]
  ↓
download_geo_data → data/{accession}/
  ↓
download_supplementary_files（如果需要 supplementary counts）
  ↓
preprocess_counts → *_filtered.csv + *_normalized.csv
  ↓
sample_qc_summary + run_pca + sample_correlation_heatmap → 图表 & 表格
  ↓
inspect_metadata → 让 LLM 看到候选 design 列
  ↓
run_deseq2_analysis (
  内部: align_samples_with_llm_fallback → DESeq2 → DEG_*.csv
)
  ↓
run_enrichment_analysis + run_gsea_analysis → 通路富集表
  ↓
extract_sea_cdm_conditions → seacdm.json
  ↓
Claude 用中文 summary 回复用户
```

---

## 五、Cohort 端到端流程

```
用户给关键词 (e.g. "Diabetes")
  ↓
search_geo_studies → output/geo_search_Diabetes.csv (含 has_counts_like_supp 等列)
  ↓
test/scripts/pick_cohort.py: top N (按样本数排序) + random M (seeded) → 10 个 accession
  ↓
run_batch_geo_pipeline.invoke({...})
  ↓
对每个 accession：
  download → _find_raw_counts_file
    ├─ 找到 raw counts → 继续
    ├─ 找到 FPKM/TPM/log → skipped_top_files_not_raw_counts(reason)
    └─ 只有 _RAW.tar → _unpack_and_merge_geo_tar → 再分类
  ↓
  preprocess_counts → 失败则记 failures.log，继续下一个
  ↓
  sample_qc_summary
  ↓
  _auto_detect_design (评分挑列)
  ↓
  validate_contrast_with_llm
    ├─ confirm → 用 Python 选的
    ├─ override → 用 LLM 选的
    └─ refuse → status=preprocess_ok_no_design，跳过 DEG
  ↓
  run_deseq2_analysis（内部含 LLM B 兜底）
  ↓
  run_gsea_analysis
  ↓
  写一行到 summary.csv
  ↓
全部完成 → 返回 cohort 路径
```

输出：

```
output/cohort_{run_label}/
├── summary.csv              # 一行一个 accession，含 LLM 决策列
├── failures.log             # 异常 traceback
├── workflow.log             # 全部 stdout/stderr（含 pydeseq2 输出）
└── {GSE_accession}/         # 每个研究的工件（与单 study 路径同布局）
```

---

## 六、输出工件清单

### 6.1 单 study 输出（位于 `output/{GSE_accession}/`）

以 `output/GSE266241/` 为例，**13 个工件**：

**表达矩阵（预处理产物）**
- `*_filtered.csv` —— 过滤低表达基因后的整数 counts 矩阵
- `*_normalized.csv` —— log2(CPM+1) 归一化矩阵，用于 PCA / 相关性

**QC 工件**
- `*_sample_qc.tsv` —— 每样本 library_size / n_detected_genes / n_zero_genes
- `*_pca.png` + `*_pca_scores.csv` —— PCA 图 + 坐标 + 解释方差
- `*_corr_pearson.png` + `*_corr_pearson.csv` —— 样本相关性热图 + 数值矩阵

**差异表达**
- `DEG_results_{treat}_vs_{ctrl}.csv` —— PyDESeq2 输出（每行一基因，列：`baseMean / log2FoldChange / lfcSE / stat / pvalue / padj`，按 padj 升序）

**通路富集（每个 DEG 文件对应 5 张表）**
- `*_GO_Biological_Process_2023.csv` / `*_GO_Cellular_Component_2023.csv` / `*_GO_Molecular_Function_2023.csv` —— GO 三大本体 ORA（Enrichr）
- `*_KEGG_2019_Mouse.csv` —— KEGG ORA
- `*_GSEA_Hallmark.csv` —— preranked GSEA against MSigDB Hallmark（含 `Term / ES / NES / NOM p-val / FDR q-val / Lead_genes`）

**结构化记录**
- `seacdm.json` —— Pydantic `SEACDM_Record` 强制结构化的 JSON

### 6.2 Cohort 输出（位于 `output/cohort_{run_label}/`）

**Cohort 级**
| 文件 | 内容 |
|---|---|
| `summary.csv` | **核心机器可读结果表**。每行一 accession，列：`accession / status / n_samples / design_col / control / treatment / n_deg / n_gsea_sig / counts_file / error / llm_validated / llm_overrode / llm_reasoning` |
| `workflow.log` | 全部 stdout/stderr 抓取（含 pydeseq2、gseapy 详细输出），in-process Tee 实现 |
| `failures.log` | 异常 traceback（仅 study 失败时有内容） |

**每 study 子目录**（与单 study 输出同构，但当前 cohort 模式只跑 GSEA 不跑 ORA）：
- 5 个文件 = `*_filtered.csv` + `*_normalized.csv` + `*_sample_qc.tsv` + `DEG_*.csv` + `DEG_*_GSEA_Hallmark.csv`

### 6.3 搜索阶段输出

| 文件 | 内容 |
|---|---|
| `output/search_{keyword}.csv` | `search_geo_studies` 原始结果（title / summary / accession / n_samples / organism / has_counts_like_supp 等列） |
| `output/geo_search_{keyword}.csv` | 同上的 cohort 选样用版本 |

### 6.4 `summary.csv` 实样（Diabetes cohort 一行）

```
GSE291636, deg_failed, 73, characteristics_ch1.3.treatment,
Normal diet, High fat diet, , ,
GSE291636\GSE291636_merged_from_tar.csv, ,
True, False,
"The proposed contrast uses 'characteristics_ch1.3.treatment' with
 'Normal diet' as control and 'High fat diet' as treatment...
 Both groups have 5 samples each, meeting the minimum replicate
 requirement for DESeq2."
```

最后三列（`llm_validated / llm_overrode / llm_reasoning`）= LLM A 决策的完整可追溯记录。

### 6.5 中间产物（位于 `data/{GSE_accession}/`）

不算最终输出但落盘：
- `{accession}_metadata.csv` —— GEOparse 抽出的 phenotype 数据
- `{accession}_*.tsv.gz / .csv.gz / .txt.gz` —— 原始 counts 文件
- `{accession}_RAW.tar` + `_unpacked/` —— 按需解压
- `{accession}_merged_from_tar.csv` —— tar 拆开合并后的产物

### 6.6 当前**没有**的输出（盘点缺口）

1. **跨研究可视化总结**（cohort 级 PCA / cohort 级 DEG overlap / cohort 级 GSEA heatmap）—— 目前只有 summary.csv 表格
2. **HTML / markdown 形式的研究报告** —— 用户看结果要自己开 CSV
3. **本体映射后的结构化数据** —— SEA CDM 已抽，但 term → ontology ID 那步未做（参见 WORKFLOW.md Agent B）
4. **入库格式** —— 没有最终数据库 schema，所有 output 停在文件层

---

## 七、测试 / 验证基础设施（`test/`）

| 脚本 | 用途 |
|---|---|
| `test/unit/test.py` | 单工具调用测试 |
| `test/unit/test_seacdm.py` | SEA CDM 抽取测试 |
| `test/smoke/smoke_test_new_tools.py` | preprocess + stats + GSEA 在 GSE266241 上的烟雾测试 |
| `test/scripts/probe_search_quality.py` | 下载并分类几个搜索 hit |
| `test/unit/test_llm_contrast.py` | LLM A 三场景测试（confirm / override / refuse） |
| `test/unit/test_llm_align.py` | LLM B 三场景测试（exact / LLM 救回 / no_match） |
| `test/scripts/pick_cohort.py` | top + random 抽 cohort 工具 + CLI |
| `test/scripts/run_cohort_v2.py` | Exercise 5 study 真实运行 |
| `test/scripts/run_cohort_v3_diabetes.py` | Diabetes 5 top + 5 random 真实运行 |
| `test/validation/verify_llm_decisions.py` | 临时人工核验脚本（写死 3 个 GSE） |

所有 test 脚本都有 chdir prelude，能从任意 CWD 启动。

---

## 八、真实运行结果

### Cohort 1 —— Exercise 5 study（手挑）
- **4/5 端到端成功**，1 个 FPKM 数据正确跳过
- LLM A 触发 4 次：2 confirm + 2 override（GSE297515 改对更平衡的列；GSE282641 从 NO MATCH 救出 sed vs ex）
- LLM B 触发 1 次：GSE326587 缩写解码 28/28 全对
- **人工核验**：A 决定 4/5 完美 + 1/5 选对语义但 26 vs 3 不平衡（A 没主动 flag）；B 100% 准确

### Cohort 2 —— Diabetes 5 top + 5 random（随机扩展）
- **0/10 端到端成功**，但拆开看 8 个不是 pipeline 锅：
  - 4 个被正确判为数据质量问题（log_transformed / ambiguous_decimal）
  - 3 个被 LLM A 正确 refuse（off-topic：Pyridostigmine+TNF-α、MSNBA、ambiguous 3-treatment）
  - 1 个 metadata 没候选列（GSE319931）
  - **2 个真 bug**：filename sanitize（已修）、tar 静默丢样本（未修）

**结论**：A 的最大价值不是修正 override，而是**refuse off-topic 研究**——在 Diabetes 上 3/3 准确，关键词召回的污染被 A 干净拦下。

---

## 九、遇到的困难（按时间 / 主题）

### 1. LLM 选型困难
- **初版用 DeepSeek-chat**：multi-tool ReAct loop 中会反复调同一个工具，每次参数仅有 cosmetic 差异（多个空格、换大小写），直到撞 recursion limit。表现极不稳定
- **解决**：换 Claude Sonnet 4.6，本身就不循环；但同时构建 `guard_tools` 做程序化兜底，把最坏情况封死在 ~30 次调用以内
- **2026-08-18 更新**：统一模型工厂接入 DeepSeek **V4 Pro**；主 agent 使用 `effort=max`，结构化子调用因 DeepSeek 的 `tool_choice` 限制自动关闭 thinking。V4 Pro 在 7-case × 3-repeat 科学路由 pilot 与 3-case × 3-repeat 缓存 GEO DA A/B 中均为 100% 通过、零循环、零阻断；正式端到端运行成本/成功运行约为 Sonnet 的 2.06%，三例跨模型 DEG 的 log2FC 相关性、方向一致率及 Top-50 Jaccard 均为 1.000。原 100k 字符 GSE208615 SEA-CDM 单次大 schema 路径仍不可靠；新增按 study、documentation、experiment/intervention、materials、findings 分阶段的小 schema 路径，带 16K 输出预算、完成门、定向重试、形状归一化、确定性标题复用和 `decision_trace`。最终 A/B 中旧路径 0/3，新路径 3/3、平均 100 分、零阻断、99.0% provenance、material/finding 参考召回 89.2%/100%、约 $0.0317/pass；staged-only 独立审计 100/100（适用覆盖 65.2%）。该路径目前仍是候选，生产保持主 agent/DA 用 DeepSeek、SEA-CDM 用 Sonnet，直到额外常规和对抗论文通过。
- **2026-08-18 泛化门**：staged 路径在常规 GSE270703 为 3/3（98.1% provenance、100% material 参考召回、结构完全稳定、约 $0.0325/run），但多因素 GSE250122 为 0/3。失败不是格式或 FK：三轮均稳定输出一个 experiment 和两个 intervention，而论文/Sonnet 参考明确区分两个实验——ET/SED 急性运动 microarray 与独立 SED-T 8 周训练 qPCR。常规案例独立审计 100/100（适用覆盖 65.2%），多因素案例 86.7/100 且有 `study_completion` 阻断。生产 SEA-CDM 继续使用 Sonnet。
- **2026-08-18 GEO 范围修正与复测**：确认当前 CDM 路径本来就是“一条 GEO accession 对应一个 experiment”，旧 prompt 却让模型抽整篇论文，旧 evaluator 又把 Sonnet 论文级参考的 `experiment_count >= 2` 当硬门，二者口径冲突。现由 GEO metadata 生成确定性 `[TARGET GEO SCOPE]`，prompt 只允许 target accession 的 cohort/intervention，评测改为检查 experiment/intervention/assay 是否混入 paper-only 队列，不再用固定实验数。GSE250122 三次都只保留 60 min 急性骑行 + baseline/+30min/+3h + microarray，未混入 8 周训练/qPCR；GSE270703 同时保持 3/3。零调用重评分六次均为 scope pass、target intervention recall 100%；完整运行审计 100/100（适用覆盖 65.2%），平均成本约 $0.0267/$0.0329 per run。另修复了 GEO 无 `library_strategy` 时 Affymetrix/CEL 被误标为 high-throughput sequencing 的问题。因为 GSE250122 是同案修复，生产 SEA-CDM 暂仍保持 Sonnet，下一门槛是未见 multi-cohort 论文。
- **2026-08-18 未见 multi-accession 盲测**：在首次调用前冻结 GSE197045/PMC9233305 与全部门槛；目标是老年小鼠 soleus myonuclei RRBS（6 samples，PoWeR vs sedentary），同文另有 RNA-seq accession GSE198652。DeepSeek staged 3/3 通过，三轮均准确保留 8 周 PoWeR、2/3/4/5 g 递增负重、22–24 月龄雌性 C57BL/6N、Bisulfite-Seq/HiSeq 2000 和 3 vs 3 分组，且 design tables 无 GSE198652/RNA-seq 污染。平均 provenance 97.9%，成本 $0.0321/run，中位延迟 103.5 s，结构完全一致；独立审计 100/100、适用覆盖 65.2%、零阻断。旧 exact-set intervention Jaccard 为 0 是整行轻微措辞/标点差异造成，逐字段科学事实一致。结论：DeepSeek 已满足 staged + GEO metadata 的 accession-scope 候选门槛；生产默认仍保持 Sonnet，若切换应只路由该模式，并保留 paper-wide/no-metadata 的 Sonnet fallback。

### 2. TSV 静默 NaN 灾难
- 原先 `pd.read_csv(path, index_col=0)` 没指定 `sep`，遇 `.tsv.gz` 直接把整行当一列读入；`pd.to_numeric` 把所有值 coerce 成 NaN；"drop all-NaN columns" 清理一步把所有样本删光；preprocess 报"N genes × 0 samples"但**没有任何错误**
- 影响 4 个 read 点：`preprocess_tools:29`、`stats_tools:31/44`、`deseq2_tools:32`
- **解决**：所有点改 `sep=None, engine="python"` 让 csv.Sniffer 自动判
- **教训**：silent failure 比 crash 更危险，宁可早 fail

### 3. 样本对齐困难
- **v1（旧）**：内联 greedy substring，对每个 metadata 行迭代 counts 列 break on first hit
- **失败案例**：GSE297707 (64 样本) 因 `Sample_1` 是 `Sample_10/11/...` 的子串，substring 过早匹配错的列，然后 `~duplicated(keep="first")` 把对的列丢掉。64 → 9 对齐 → 只剩 1 个 DEG
- **v2**：抽出 `align_samples` cascade（exact → substring with `used` set → token-overlap ≥3）
- **新失败案例**：GSE326587 counts 是 `HC_F1_TL_S54_L003`，metadata 是 `HomeCage1_Female1_TotalLysate` —— 三个策略全失败，因为词汇表不共享 token
- **v3**：加 LLM B 兜底（`align_samples_with_llm_fallback`），LLM 解码缩写返回 mapping
- **故意不做的事**：位置 fallback。silently align by row order 在 DESeq2 上会产生生物学错误的结论，比 fail 更糟

### 4. 设计列检测困难
- **v1**：first-match 太脆，多个 metadata 列都能切 2 组时随便选一个
- **v2**：评分式（+1 base, +1 列名关键词, +1 n≥3）+ control 候选必须"匹配 ctrl 关键词且不匹配 treat 关键词"
- **新失败案例**：关键词覆盖不到（PBS / Vehicle / AEX）、或者多个列都能合理切但选错了
- **v3**：加 LLM A（`validate_contrast_with_llm`），confirm / override / refuse 三路
- **未预料到的最大价值**：refuse off-topic studies（关键词召回带进来的污染研究），Diabetes cohort 3/3 准确识别

### 5. Tar 解包困难（**部分未解决**）
- GEO 经常把 per-sample counts 打包成 `{accession}_RAW.tar`，每个 sample 一个 `GSM*_label.txt.gz`（有时是 featureCounts 输出带 `#` 注释头）
- 写了 `_unpack_and_merge_geo_tar`：解压 → 自动判分隔符 → 跳 `#` 行 → 取最右侧数值列 → 按 gene_id 合并 → 输出 `*_merged_from_tar.csv` → 再次过 `_classify_matrix`
- **GSE291636 暴露了 bug**：metadata 列 73 个样本，tar 只解出 3 个 `.txt.gz` 文件，**没有任何 warning**。LLM A 基于完整 metadata 选了 "Normal diet vs HFD"，但残存的 3 个样本只剩 "high glocose"，DESeq2 阶段才报 "does not contain both"
- **未修**：需要在解出文件数与 metadata 样本数差太多时打 warning 或 fail

### 6. Metadata 被当成 counts
- `_find_raw_counts_file` 在没找到别的文件时会拿 `{accession}_metadata.csv` 当 counts
- 某些 metadata 列（如 `data_row_count`）值是大整数，会通过"看起来像 raw counts"启发式
- **解决**：文件名含 `metadata` 直接从候选名单排除

### 7. 文件名 sanitize
- `db/db (leptin receptor mutant)` 作为 treatment 名 → `/` 被当目录分隔符 → `to_csv` 失败 "non-existent directory"
- DESeq2 跑完了（30103 行结果），但写文件那一步崩
- **解决**：`safe_for_filename` + `deg_filename` helper，writer (`deseq2_tools:106`) 和 reader (`batch_tools:414`) 共用，保证一致

### 8. Provenance / 可观察性困难
- 一开始没法回溯"为什么 LLM 选了 X 而不是 Y"
- **加了三个机制**：
  - `summary.csv` 三新列：`llm_validated` / `llm_overrode` / `llm_reasoning`
  - `workflow.log` 用 in-process Tee 抓全部 stdout/stderr（含 pydeseq2/gseapy）
  - `source_search_csv` 参数：workflow.log 顶部 snapshot 搜索 CSV 的对应行（来源溯源）

### 9. Cohort 选样策略困难
- 纯 top-N 选大样本研究，反复撞同类失败模式（都是大样本 → 都是同种数据格式）
- **解决**：`pick_cohort(n_top, n_random, seed)` 5 top + 5 random
- random 那一半在 Diabetes 上意外暴露了 A refuse 路径的价值

### 10. 跨平台 / 编码
- Windows GBK console 见 emoji 直接抛 `UnicodeEncodeError`


### 11. 未解决 / 已知限制
1. **Bug 1**：`_unpack_and_merge_geo_tar` 静默丢样本（GSE291636）—— 待加 sanity check
2. **小修**：`"[llm-validation] unavailable; using python result"` 在"metadata 无候选列"场景下措辞误导（GSE319931 case）—— 实际是没候选列而非 API 不可用
3. **FPKM/TPM-only 研究** —— 作者只上传归一化矩阵时 DESeq2 跑不了，pipeline 正确跳过但上游问题无法在本层修
4. **多因子设计**（genotype × stimulus × time × tissue 3-4 axis）—— 没有单一干净的 2-group split，当前 LLM A 只看关键词列表 + 列摘要，复杂 case 需要更长的 free-text intent
5. **元数据太稀疏的研究** —— 只有 GSM IDs + `data_processing` 列时，LLM B 没东西可 pattern-match
6. **`download_supplementary_files` 无 skip-if-exists** —— cohort 重跑时浪费带宽
7. **Priority C（keyword learning loop）** —— 评估 ROI 低（A 每次 ~$0.003，问题不大），主动搁置

---

## 十、关键工程决策（值得记下来的）

1. **结构性护栏 > prompt 约束**：`guard_tools` 把"不许循环"做成 Python 层强制，比 system prompt 写 "do not loop" 可靠得多
2. **Pydantic structured output > 后处理**：`@tool(args_schema=PydanticSchema)` 让 LLM 直接出验证过的对象，不靠"please return JSON"
3. **大声 fail > 静默猜测**：`align_samples` 拒绝位置 fallback、`_find_raw_counts_file` 用显式 reason code、`_classify_matrix` 拒 FPKM/TPM —— 全是同一条原则
4. **LLM 兜底永不阻塞**：A 和 B 失败都回退到 Python 启发式答案，LLM 不可用时 pipeline 仍能跑
5. **Writer 和 reader 共用 helper**：`deg_filename` 让两边的命名约定不会漂移
6. **每个 cohort run 隔离目录**：`output/cohort_{run_label}/`，两个 cohort 共享 GSE 也不会互相覆盖
