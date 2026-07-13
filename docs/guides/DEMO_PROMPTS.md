# Demo Prompts —— 开会演示用

> 三档 prompt，从短到长。**推荐 V2 当主 demo**，`summary.csv` 当备胎。

---

## Demo 前准备（务必先做）

### 1. 环境
```powershell
$env:PYTHONIOENCODING="utf-8"   # 不设这个 Windows 控制台见 emoji 会崩
```

### 2. 预热 GEO 缓存（防止 demo 现场抽风）
demo 前 30 分钟跑一次，让 GSE266241 落到本地：

```powershell
.\.venv\Scripts\python.exe -c "from tools.geo_tools import download_geo_data; print(download_geo_data.invoke({'accession': 'GSE266241'}))"
```

### 3. 清掉旧 output（让 demo 看起来"新鲜生成"）
```powershell
.\.venv\Scripts\python.exe clean.py
```
⚠️ `clean.py` 会清 `data/` + `output/`。如果 data/ 也清了，记得**先**预热再清——或者把预热改成只在清空之后做。

### 4. 跑一次 V2 calibrate 时长
正式 demo 前用 V2 在本地跑一遍，确认实际耗时在 5 分钟内。**超过 8 分钟就砍掉 V2 第 2 步（QC 部分）**。

---

## 🟢 V1 —— 30 秒级"开胃菜"

**用途**：导师只想快速看一眼能力。
**触发工具**：`fetch_geo_description` + `inspect_metadata`
**用时**：~30 秒
**风险**：极低

```
分析 GSE266241：
1) 拿一下 GEO 的研究描述
2) 看 metadata，告诉我有哪些可能的实验分组
3) 推荐一个合理的差异表达对比（不用真跑 DESeq2）
```

**演示重点**：agent 能自己读 metadata 并推断分组——它不只是工具调用器，会理解结构。

---

## 🟡 V2 —— 5 分钟"主菜"（**推荐主轴**）

**用途**：核心 demo，展示端到端自动化。
**触发工具**：download → inspect_metadata → preprocess → QC(PCA + corr + sample_qc) → DESeq2 → GSEA → SEA CDM
**用时**：3-5 分钟
**风险**：低（GSE266241 是历史 ground truth）

```
请帮我端到端分析 GSE266241：

1) 下载数据（如本地已有请复用）
2) 跑 QC：PCA + 样本相关性热图
3) 看 metadata，按组织部位（Thoracic and Lumbar Spinal Cord vs Cervical Spinal Cord）跑 DESeq2
4) 用 GSEA 看富集到哪些 MSigDB Hallmark 通路（小鼠）
5) 抽取 SEA CDM 结构化记录

最后用 3-5 句话总结这个研究的主要发现。
```

**演示重点**：
- 工具自动串联（不用一步步指挥）
- 输出全套工件（图 + 表 + JSON）
- 中文最终总结

**如果时间紧，砍成 3 步版**：
```
分析 GSE266241：
1) 看 metadata 推断分组
2) 按组织部位（Thoracic and Lumbar Spinal Cord vs Cervical Spinal Cord）跑 DESeq2
3) GSEA 看 Hallmark 通路（小鼠）
用 3 句话总结。
```

---

## 🔴 V3 —— 10-20 分钟"全场展示"（时间充裕再上）

**用途**：展示 cohort 自动化 + LLM 兜底现场触发（项目最大亮点）。
**触发工具**：search → batch pipeline (10 个研究 × 完整流程)
**用时**：10-20 分钟
**风险**：高（依赖 NCBI + GEO 网络；可能召回 off-topic 研究）

```
请基于关键词 "Exercise" 搜 GEO，挑出前 3 个有 raw counts supplementary 的研究，
然后批量跑完整 pipeline：preprocess + QC + DESeq2 + GSEA。

跑完后告诉我：
- 哪些研究跑成功了
- LLM A 在哪些研究帮了忙（confirm / override / refuse）
- 哪个研究的运动响应信号最强
```

**演示重点**：
- 批量自动化（多个研究 1 条命令）
- **LLM A 现场触发**（refuse / override / confirm）
- 失败处理（FPKM 自动跳、tar 自动解包）
- `summary.csv` 审计列

---

## 🛟 Plan B —— 直接展示已跑完的 cohort summary（零风险备胎）

如果 V2/V3 任何一步翻车，**不要硬跑**——直接打开已跑完的 cohort summary 给导师看：

### Exercise cohort（4/5 成功 + LLM 帮忙）
```powershell
notepad output/cohort_Exercise_v2_llm_fallback/summary.csv
```

讲解台词模板：
> "这是之前跑的 Exercise cohort，5 个研究。注意最后三列 `llm_validated / llm_overrode / llm_reasoning`——agent 在 GSE297515 和 GSE282641 上**主动 override 了 Python 启发式的选择**，事后人工核验这两个都对。GSE326587 这一行更有意思：它的样本名是测序仪缩写（`HC_F1_TL_S54_L003`），跟 metadata 完全对不上，是 LLM B 现场解码成功的，28/28 全对。"

### Diabetes cohort（展示 LLM A refuse off-topic 的能力）
```powershell
notepad output/cohort_Diabetes_top5_random5/summary.csv
```

讲解台词模板：
> "这次随机抽 5 个 study 进来，3 个被 LLM A 主动 refuse：一个是 Pyridostigmine+TNF-α 研究（跟糖尿病无关）、一个是 MSNBA 化合物筛选（也无关）、一个是多臂 design 没法二选一。agent 自己把 search 召回的污染拦下来了——这正是有 LLM 兜底而不是纯脚本的价值。"

---

## 推荐演示顺序

| 时段 | 操作 | 内容 |
|---|---|---|
| 0-1 min | 口头 | 用 `docs/status/STATUS.md` §一+§三快速介绍架构 |
| 1-6 min | **V2 主菜** | GSE266241 端到端 |
| 6-8 min | **Plan B** | 打开 Exercise summary.csv 讲 LLM 兜底 |
| 8-10 min | **Plan B** | 打开 Diabetes summary.csv 讲 refuse off-topic |
| 10-15 min | 讨论 | 切到 `docs/reviews/REVIEW_NOTES.md` 谈 `docs/guides/WORKFLOW.md` 演进 |

→ 这个组合**网络 zero 依赖**（V2 用本地缓存数据；Plan B 读已有 CSV），导师能看到完整 capability，整个过程 15 分钟内。
