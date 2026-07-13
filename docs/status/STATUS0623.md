

## 一、本阶段目标

在 STATUS0605 的"关键词→论文→自有 GSE→SEA-CDM + DA"主干上,**逐条落实会议提出的 8 项需求**,并把整条管线在**多样真实数据**上压测,确认"够应对多数情况"且**失败时大声、报告时有解释**。

```
关键词 → 检索论文 → 取全文 → 判 own/cited GSE → 抽 15 张 FK 互联 SEA-CDM 表
        → 对 own-GSE 跑多方法 DA(共识)+ GSEA → 回填 analysis/results
        → 文本结论挖掘(#5)+ 计算↔文本一致性(#6)+ pathway↔exercise 机制链(#7/#7b)
```

---

## 二、技术栈增量(相对 0605)

| 新增/变化 | 说明 |
|---|---|
| `tools/metadata_structural.py` | subject/sample/groups/assay **从 GEO metadata CSV 确定性派生**(零 LLM)→ #3 |
| `seacdm_tools._extract_lean` | **1-call 合并抽取**(metadata 在场时自动启用)→ #4 |
| `tools/scrna_tools.py` | 单细胞 **pseudobulk** 聚合 → 复用 bulk DA 后端 → #2 |
| `tools/agreement_tools.py` | 计算 DEG ↔ 文本结论逐基因判定 + **note 解释** → #6 |
| `tools/pathway_chain_tools.py` + `tools/enrichment_loader.py` | 机制链 + **pathway/enrichment 关系表**(零 LLM JOIN)→ #7/#7b |
| `enrichment_tools` 整数 ID→符号 sidecar | TALON 整数基因 ID 经 `<base>_id2symbol.csv` 映射(本会话)|
| `batch_tools._deg_sanity_flags` | DA 后**结果合理性护栏**(本会话)|
| `tools/study_split.py` | 把多条件 GSE **拆成 N 条 per-condition study + 全配对比较**(本会话,#8 扩展)|
| `tools/methylation_tools.py` | **DNA 甲基化 DA**(β→M值→复用 limma;数据覆盖 P1,本会话)|
| 抽取 LLM | 仍为 **Claude Sonnet 4.6** + `with_structured_output(Pydantic)` |

**数据覆盖现状**(算法后端):RNA-seq 原始计数→DESeq2/edgeR/limma-voom;FPKM/TPM/log→limma-trend;蛋白组强度→limma;单细胞→pseudobulk 复用 bulk(#2);**DNA 甲基化→β→M值→limma(本会话新增,P1)**。仍未覆盖:ATAC(peak)/ 变异(VCF)/ 仅 SRA 原始 reads —— 一律 fail-loud 跳过带原因码,不造假结果。

---

## 三、8 项会议需求 —— 全部 SHIP(#1✅ #2✅ #3✅ #4✅ #5✅ #6✅ #7✅ #8✅)

| # | 需求 | 实现 | 报告位置(有解释) |
|---|---|---|---|
| **#1** | DA 方法选择**降成本**(去掉每研究 LLM picker) | `raw_da_method='auto'` → `choose_raw_da_method_rule()` 确定性返回 DESeq2;`'auto-llm'` 保留旧 LLM picker | `summary.csv` `da_method`+`da_method_reason`(散文理由);`decisions.json` `da_method_select` |
| **#2** | **单细胞** | `scrna_tools` pseudobulk(按 sample×celltype 求和)→ 每细胞类型跑 bulk DA + GSEA。验证于 Kang 2018(GSE96583,24673 细胞×15706 基因):CD14 单核 3428 DEG、IFN_GAMMA/ALPHA GSEA NES=2.61 | `scrna_demo_kang/`(8 细胞类型逐个工件)|
| **#3** | **确定性**(多次跑 JSON 一致) | 结构表从 metadata **确定性派生**(`metadata_structural`)→ subject/sample/groups/assay **字节一致**。字段稳定性 68%→**89.9%**,source 49%→**83.4%** | 各结构表 `<field>_source="GEO metadata: 列名"`;`_determinism_check/` |
| **#4** | **时间/成本剖析 + 抽取降本** | `_extract_lean` 1-call 合并抽取(metadata 在场自动启用)| `_extraction_profile/profile.json`:FULL vs LEAN **input −65.4% / $ −65.7% / wall −62%**(3→1 调用)|
| **#5** | **从正文挖结论**(无数据时也有 results) | `build_reported_findings` 1 次结构化抽取 → `reported_findings.csv` + text-mining 的 analysis/results 行;逐字率经 `_snap_to_verbatim` 收紧 **47%→0–2%** | `reported_findings.csv` 每条带**原文逐字** `source` |
| **#6** | **计算↔文本一致性标注** | `agreement_tools` 逐基因判定(confirmed/contradicted/direction_only/not_detected/not_checkable);基因 ID→符号桥 100% 覆盖 | `<study>_agreement.csv` `agreement`+**`note`(逐判定解释,本会话补全)** |
| **#7** | **pathway→exercise 机制链** | `pathway_chain_tools`(GSEA leading-edge × #5 文本结论)+ **#7b** `enrichment_loader` 把 GSEA 重置成 pathway/enrichment 关系表 → 链 = `enrichment⋈pathway⋈analysis⋈groups` | `chain_view.csv`(去规范化,自解释)+ `<study>_pathway_chain.csv`(带 `*_source`)|
| **#8** | **按 treatment/duration 拆 study** | `_auto_detect_contrasts` 返回**对比列表**(每个处理水平 vs 基线)→ 各对比独立 DEG+GSEA | `summary.csv` `n_contrasts`/`contrasts`/`n_deg_detail`(逐对比逐方法)+ `decisions.json` 逐对比步骤 |

---

## 四、SEA-CDM 13→15 表扩展(#7/#7b 的关系化)

为让"pathway↔exercise"成为**关系 JOIN** 而非文件解析,在原 13 表上扩展(`tools/sea_cdm_schema.py`):

| 新增 | 类型 | 来源 | 关键列 |
|---|---|---|---|
| `pathway` | NODE | MSigDB GMT(reference)| `pathway_id`(canonical,跨研究共享)、`n_genes` |
| `enrichment` | EDGE | GSEA CSV(pipeline)| `analysis_id`/`pathway_id` FK、`direction`/`nes`/`fdr`、`leading_edge_genes`、`gsea_source` |
| `analysis` +3 列 | — | — | `treatment_group_id`/`control_group_id`(FK→groups)、`contrast_label` |

- 链现在 = `enrichment ⋈ pathway ⋈ analysis ⋈ groups(×2 臂)`;跨研究聚合 = `GROUP BY pathway_id`。
- `chain_view.csv` = 物化的去规范化视图,一行一链,人可直读。
- `enrichment_loader.py` **零 LLM**,纯把已有 `*_GSEA_*.csv` 重塑成行。

---

## 五、本会话(0623)强化与修复

### 5.1 GSEA 基因符号修复(整数 ID → 符号)
- **问题**:GSE279359 是 TALON 输出,DEG 索引是**裸整数特征 ID**(符号在被丢弃的 `annot_gene_name` 列),GSEA 与符号化 Hallmark **零重叠** → 含糊失败。
- **修复**:`preprocess_counts` 在丢弃注释列前抢救符号列写 `<base>_id2symbol.csv`;`run_gsea_analysis` 检测裸整数索引 → 同目录自动发现 sidecar → 映射成符号(找不到则返回**明确可执行报错**)。
- **实测**:8452 整数 ID → 5029 鼠符号 → GSEA 跑通、**39 个 Hallmark 集显著**,信号合理(Myogenesis↓ NES−2.3、OXPHOS↓、mTORC1↑)。

### 5.2 机制链 FK 解析修复
- **问题**:`all` 多方法模式 GSEA 文件名带 `__deseq2` 后缀,泄漏进 control 臂(`pre-exercise  deseq2`)→ `control_group_id` 解析失败。
- **修复**:`_parse_gsea_contrast` 剥掉 `__<method>` 后缀 → 3 个对比两臂全解析(grp→grp),chain_view JOIN 39 行带两臂。

### 5.3 五项机械成本优化(零推理)
`download_supplementary_files`/`download_geo_data` skip-if-exists、MSigDB GMT 进程缓存、MyGene 缓存、**置信门控**(`_python_pick_is_confident`:仅当对比无歧义才跳过 LLM 校验)。

### 5.4 `deg_sanity` 结果合理性护栏(把"静默出错"变响亮)
- **根因(实测纠正两次)**:GSE317978 的 11339 DEG **不是** stat 列泄漏、**不是**低表达噪声,而是**正确对齐的 2v2** —— n=2/组导致大量基因组内方差为 0,eBayes 吹爆 t 统计量 → 66% 基因组判 DE,而 limma 只要求"≥4 总数",2v2 静默放行。
- **修复**:`_deg_sanity_flags` 两个有原则的信号 —— `implausible_sig_fraction`(>50% 显著)、`tiny_n_per_group`(<3)。接进单方法 + `all` 两条路径,在**三处**报警(控制台 / `summary.csv` 新列 `deg_sanity` / `failures.log`)。**不阻断**,只标"不可信"。

### 5.5 报告解释补全(8 项审计的 gap 2/3)
- **Gap 2**:`agreement_tools._verdict_note` —— 每个匹配基因判定都带解释(如 *"SIRT2 IS in our DEG matrix but not significant (padj=0.89 ≥ 0.05); the paper reports it 'changed'"*)。
- **Gap 3**:`batch_tools` 四处 DA/GSEA `dlog.record(...,"ok")` 全补散文 `reason`(deseq2/edger/limma-voom/gsea/da_method_comparison)。
- **Gap 1(顶层 manifest 漏上浮 #8 的 `n_contrasts`/LLM 校验)= 仍 OPEN**(本会话用户暂缓)。

---

## 六、鲁棒性验证("够应对多数情况")

两轮压测,合计 **16 个关键词跑 + 13 个缓存研究,0 硬崩溃**:

- **矩阵类型全覆盖**:raw_counts×6 → DESeq2+edgeR+limma-voom('all');fpkm_or_tpm×4 / log_transformed×2 → limma —— 分类路由全部正确。
- **路径全覆盖**:own-GSE 分析 / 无-own-GSE text-only / 无设计优雅跳过 / tar 合并 / 整数 ID 符号映射 / 对比门控(skip vs LLM 校验)。
- **`deg_sanity` 在真实数据上抓住** GSE317978(2v2 → 66% DEG 标红)。

**3 个真实边界**(精确读自 `failures.log`):
1. GSE132520 样本对齐四策略全失败 → 致命(**大声、不出错误结果**);
2. GSE302944 GSEA 基因 ID 既非符号又非 Ensembl 又非裸整数 → 落回老的含糊报错(残留缺口);
3. GSE317978 混合列 2v2 → **已由 #5.4 护栏从"静默"变"响亮"**。

汇总:`output/_robustness_summaries/`(3 张 CSV)。

---

## 七、确定性验证(同关键词 3 次复现)

同关键词跑 3 遍(归一化路径后字节比对):
- **字节一致**:subject / sample(20)/ groups(4)/ assay(#3 结构表)+ analysis(5)/ results(16)/ pathway(27)/ enrichment(39),以及**机制链核心**(contrast/pathway/dir/NES/FDR,对称差=0)。
- **预期浮动**:study/experiment/interventions/material(LLM 措辞)+ 链字符串里的 `exercise` 描述符(继承 interventions 文本)。
- 结论:**计算层(DA+GSEA+富集+链核心)完全可复现**;只有自由文本表 + 文本描述符浮动。

---

## 八、真实运行结果

### 8.1 旗舰:`acute/treadmill exercise` → GSE279359(`output/agentA_cohort_rerun_0622/`)
- own raw_counts;**3 个对比**(immediately/1h/24h post vs pre);多方法共识 n_deg=1/5/0(per-method deseq2/edger/voom);**GSEA 39 集 + 39 链**;agreement 5 not_detected(与"剪接变、表达不变"的论文结论一致);`deg_sanity=ok`。

### 8.2 整夜跑(老关键词,`max_papers=25`)
- **25 篇处理 | 17 抽取 | 8 抓取失败 | 4 分析 | 0 崩溃**。仅 GSE279359 完整跑通 DA+GSEA+链(39);其余 own-GSE 命中 `skipped_no_matrix_file` / `preprocess_ok_no_design`(优雅跳过)。
- **诚实标注**:此跑**昨晚撞到 API 额度**,部分 `text_ok_partial`/失败可能是 LLM 调用被掐断而非管线问题 —— **结果待额度恢复后复核**,不作为定论。
- 顺带暴露两点:Semantic Scholar `/paper/search` 偶发 **500**(已加重试)、长关键词把饮食摘要排成 top 命中(**搜索相关性** backlog)。

---

## 九、输出工件 + 展出清单

- **展出汇集**:根目录 `0623/`(原件保留在 output/):
  ```
  0623/
  ├── 00_deliverables_report/        # 书面报告 + 一致性表 + 散点图 + runbook
  ├── 01_flagship_cohort_GSE279359/  # 完整端到端跑(15 表 + decisions + GSEA + 链)
  ├── 02_by_requirement/             # 8 项需求逐一举证(req1–req8)
  └── 03_robustness/                 # 3 张压测汇总
  ```
- **output/ 已整理**:顶层只留 current(`agentA_cohort_rerun_0622`)+ 测试引用/基准 + `archive`(历史 tar);本会话压测 scratch 已删(回收 ~488MB)。data/ 14GB→1.14GB。

---

## 十、Bug 修复(本阶段)

| # | Bug | 修复 | 回归测试 |
|---|---|---|---|
| G1 | GSEA 整数特征 ID 零重叠静默失败 | preprocess 抢救符号 sidecar + GSEA 自动映射 | `test_gsea_symbol_fix.py` |
| G2 | `__method` 后缀泄漏 → enrichment→groups FK 失败 | `_parse_gsea_contrast` 剥后缀 | `test_enrichment_loader.py [5][6]` |
| G3 | n=2/组 DA **静默**出 66% DEG | `_deg_sanity_flags` 三处响亮报警 | `test_deg_sanity_guard.py` |
| G4 | agreement 判定无解释 | `_verdict_note` 逐判定 note | `test_report_explanations.py` |
| G5 | decisions.json DA 步骤无散文 reason | 四处 `record` 补 `reason=` | `test_report_explanations.py` |
| 成本 | 重复下载/网络/LLM | 5 项 skip/cache/gate | `test_cost_caches.py` / `test_cost_gate_45.py` |

---

## 十一、已知限制 / Backlog

1. **搜索相关性排序**(未解,backlog)—— 运动关键词偶尔召回饮食/无关研究排在 top。
2. **`max_papers=1` 对单次抓取失败脆弱** —— 已为整夜跑加 S2-500 重试;单篇路径仍无"换下一篇"兜底。
3. **GSEA 非符号·非 Ensembl·非整数基因 ID**(GSE302944)—— 落回老报错(fail-loud,不出错误结果)。
4. **样本对齐四策略全失败**(GSE132520)—— 致命跳过(安全),罕见命名约定的覆盖缺口。
5. **顶层 manifest 漏上浮 #8/LLM 校验解释**(报告 gap 1)—— 用户暂缓。
6. **多因子设计**(genotype×stimulus×time×tissue)—— 无单一干净 2-group。
7. **API 额度/429** —— 套餐层,代码层无解(整夜跑已实测撞到)。
8. **n=2/组研究** —— 护栏标红但仍产出 n_deg(用户需自行判不可信);非阻断。

---

## 十二、关键工程决策(本阶段新增,延续 STATUS0605)

1. **确定性优先于 LLM**:结构表能从 metadata 确定性派生就不让 LLM 抽 → #3 字节一致的根本。
2. **关系化机制链**:把 pathway/enrichment 做成**表**而非文件,让 #7 成为 JOIN、可跨研究 `GROUP BY` —— 而非每次解析文件。
3. **静默出错 → 大声**:`deg_sanity` 把"数值合法但统计垃圾"(n=2 的 66% DEG)从无信号变三处报警 —— 延续 fail-loud 原则到**结果合理性**层。
4. **报告处处带解释**:每个判定/每步决策都附 reason/note/`*_source`,审计时不留裸标签或裸数字。
5. **诚实标注污染**:整夜跑撞额度 → 明确标"待复核",不把可能被掐断的结果当定论。
6. **移动而非删除、抢救后再清**:整理 output 时先把展出件抢救出来再删归档,回收空间不丢证据。
