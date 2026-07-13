# STATUS0630 
---

## 1. LLM 数据类型判断与 DA 方法选择



| 环节 | 代码 | 作用 |
|---|---|---|
| Python 初筛 | [`_classify_matrix`](tools/batch_tools.py) | 读取矩阵前 2000 行,按数值分布判断 raw / log / FPKM-TPM / ambiguous |
| LLM 结构化 schema | [`MatrixTypeClassification`](tools/llm_helpers.py) | 约束 LLM 只能返回固定 `matrix_type`、`already_log_scale`、`confidence`、`reasoning` |
| LLM 判断入口 | [`_llm_datatype_decision`](tools/batch_tools.py) | 只在 decimal/ambiguous 或 proteomics/methylation hint 时调用 LLM |
| LLM 结果映射 | [`_apply_llm_matrix_type`](tools/batch_tools.py) | 把 LLM 类型映射回 pipeline 可执行的 raw / log / fpkm 分支 |
| batch 调用位置 | [`run_batch_geo_pipeline`](tools/batch_tools.py) | 写入 `summary.csv.matrix_type`、`matrix_type_source`、`da_method`、`da_method_reason` |

### 1.1 Python heuristic 先判断矩阵类型

先读取表达矩阵前 2000 行,只看 numeric columns,并排除 `log2FC`、`pvalue`、`padj`、score 等 derived statistics columns,避免把 DEG 结果表误当表达矩阵。

判断规则:

| 数据类型 | 判断来源 | DA 方法 |
|---|---|---|
| raw integer counts | 非零值无小数,最大值 > 100 | DESeq2;在 all 模式下可并跑 edgeR / limma-voom |
| log-transformed expression | 有负数,或有小数且最大值 < 30 | limma |
| FPKM/TPM | 有小数、非负、最大值较大 | 先 `log2(x+1)`,再 limma |
| 不可分析/无 raw matrix | pipeline skip,但保留 text-mined findings | `analysis.da_method = text-mining` |



### 1.2 LLM 什么时候介入

默认 `llm_datatype=True`,但有 gate,不是每个矩阵都调用:

| 触发情况 | 是否调用 LLM | 原因 |
|---|---|---|
| heuristic 判为可靠 `raw_counts` | 通常跳过 | 整数 raw counts 特征强,省 token 成本 |
| `fpkm_or_tpm` / `log_transformed` / `ambiguous_decimal` | 调用 | 小数矩阵最容易在 linear normalized 和 log-scale 之间混淆 |
| 文件名或 platform hint 含 proteomics / LFQ / TMT / DIA / MaxQuant | 调用 | 数值分布可能像表达矩阵,但实际是蛋白质强度 |
| 文件名或 platform hint 含 methylation / RRBS / WGBS / 450K / EPIC | 调用 | β value 可能像 small-range log matrix,需要识别后转 M-value |
| heuristic 找不到 analyzable matrix,但有候选大文件 | LLM rescue | 尝试从被 heuristic 放弃的 top candidate 中救回真实矩阵 |

### 1.3 LLM 看到什么信息

LLM 不读整篇文章,只看一个紧凑的 matrix profile:

- 文件名。
- GEO metadata 里的 platform / assay hint。
- Python heuristic 的初步标签。
- sampled numeric stats,例如整数比例、小数比例、最大值、是否有负数、是否大多在 `[0,1]`。
- 矩阵前几行/前几列 preview。
- organism hint。

LLM 被要求用结构化输出返回:

```text
matrix_type:
  raw_counts
  fpkm_or_tpm
  log_transformed
  proteomics_intensity
  methylation_beta
  ambiguous

already_log_scale: true/false
confidence: high / medium / low
reasoning: 引用 value range、integer-ness、sign、filename、platform 等证据
```

只有 `confidence=high` 或 `medium` 的结果会被 pipeline 采纳

### 1.4 LLM 类型如何变成 DA 方法

LLM 返回的类型会被 `_apply_llm_matrix_type` 映射回现有 pipeline 分支:

| LLM `matrix_type` | pipeline `matrix_type` | 后续处理 | DA 方法 |
|---|---|---|---|
| `raw_counts` | `raw_counts` | 保留原矩阵 | 默认 DESeq2;可指定 edgeR / limma-voom / all |
| `fpkm_or_tpm` | `fpkm_or_tpm` | `log2(x+1)` | limma |
| `log_transformed` | `log_transformed` | 不再 log | limma |
| `proteomics_intensity` 且已 log | `log_transformed` | 不再 log | limma |
| `proteomics_intensity` 且未 log | `fpkm_or_tpm` 等价分支 | `log2(x+1)` | limma |
| `methylation_beta` | `log_transformed` | β value 转 M-value | limma |
| `ambiguous` | 不采纳 | 保留 heuristic 或 skip | 不变 |

---

## 2. result 同时保存原文结论与数据可推出的新结论



| 结论类型 | SEA-CDM 写法 | 说明 |
|---|---|---|
| 原文结论 A | `analysis.da_method = text-mining`;`results.file_access = reported_findings.csv` | 代表论文作者正文中明确报告的 gene/pathway/phenotype finding |
| 数据支持 A | `agreement.csv` / reconciliation result | 记录 A 在我们的 DEG/GSEA/DA 结果中是 confirmed,而不是只保存"冲突" |
| 数据额外推出 B | `analysis.da_method = deseq2/limma/...`;`results.file_access = DEG/GSEA CSV` | 代表 Agent A 从同一表达矩阵重新分析出的更显著/更完整结果 |
| A 与 B 的关系 | `results` + reconciliation summary | A 是 paper-reported conclusion;B 是 data-derived conclusion;两者可以同时成立 |

这样做的好处:

- 不因为数据能推出更强的 B,就覆盖或丢掉原文明确说出的 A。
- 不因为原文只讨论 A,就忽略数据里更显然的 B。
- 不只记录 contradicted / not_detected,也记录 confirmed 和 additional data-derived findings。
- 后续可以查询三类 case:原文说 A 且数据支持 A、原文说 A 但数据不支持 A、原文没说但数据强烈支持 B。


---

## 3. exercise + gene 入库



| exercise 字段 | 含义 |
|---|---|
| `exercise_id` | `{experiment_id}_exercise{n}` |
| `study_id` | FK → `study.study_id` |
| `experiment_id` | FK → `experiment.experiment_id` |
| `intervention_id` | FK → `interventions.intervention_id`,说明 exercise 节点从哪个 protocol intervention 派生 |
| `exercise_name` / `exercise_type` | 如 treadmill running / endurance training / voluntary wheel running |
| `exercise_parameters` | duration/dosage 等参数的合并描述 |

`gene.csv` 当前字段:

| 字段 | 含义 |
|---|---|
| `gene_id` | `{study_id}_gene{n}` |
| `study_id` | FK → `study.study_id` |
| `experiment_id` | FK → `experiment.experiment_id` |
| `intervention_id` | FK → `interventions.intervention_id`,优先指向 exercise/training/running 干预 |
| `exercise_id` | FK → `exercise.exercise_id`,直接表达 `Gene --is_regulated_by--> Exercise` |
| `group_id` | 可选 FK,当前多数为空 |
| `pathway_id` | 可选 FK,当前不强连,避免误把描述性 pathway 当标准 pathway |
| `gene_symbol` + source | 论文中写出的 gene 名及原文证据 |
| `comparison` + source | 该 gene 的比较关系 |
| `regulation_direction` | up / down / changed / unchanged / n/a |
| `relationship_to_exercise` | 当前默认 `is_regulated_by` |

关键决策:

- `gene` 是**文本证据表**,不等于全量 DEG matrix。
- 每条 gene row 必须能回到 `study` / `experiment` / `exercise`;若无 intervention/exercise,自动补一个 exercise scaffold。
- `pathway_id` 暂时 nullable,只在未来有明确 gene-pathway 关系时再连。

---

## 4. 一次性多抓取结果填入 schema

改成 chunked findings 后,可以一次 cohort 中抓取多条 reported findings,再批量填入 schema:

```text
paper chunks
  -> reported_findings.csv
  -> gene.csv
  -> pathway.csv
  -> results.csv(text-mining)
```

真实 cohort 中已经看到多 study 批量产出:

- top5 cohort:4 篇成功抽全文,`gene=167`,`pathway=20`。
- top8 cohort:4 篇成功抽全文,`gene=166`,`pathway=18`。
- 单篇 GSE208615 chunked A/B:两次均 `findings=50`,`gene=16`,`pathway=3`。

---

## 5. descriptive pathway 的处理策略



| 字段 | 写法 |
|---|---|
| `pathway_id` | `{study_id}_pathway_text{n}` |
| `pathway_name` | 文章里的描述性 pathway/process,如 `TGF-β signaling` |
| `library` | `paper_text` |
| `collection_version` | `study_id` |
| `n_genes` | 空 |

这样既不伪装成 MSigDB/KEGG/GO,又能把文章里的机制概念先落进表里,后续再做 ontology normalization。

---
## 6. 一致性与 ROUGE-L 量化



### 6.1 A/B row count

| 表 | A rows | B rows | 内容 |
|---|---:|---:|---|
| `exercise` | 1 | 1 | 显式 Exercise process 节点稳定 |
| `gene` | 16 | 16 | 行数一致,部分描述字段不同 |
| `pathway` | 3 | 3 | 内容完全一致 |
| `subject/sample/groups/interventions/assay` | 1/70/6/1/1 | 1/70/6/1/1 | metadata-derived 表稳定 |

### 6.2 ROUGE-L 汇总

| table | diff fields | mean ROUGE-L F1 | min ROUGE-L F1 |
|---|---:|---:|---:|
| `documentation` | 4 | 0.6655 | 0.0000 |
| `gene` | 12 | 0.7490 | 0.3000 |
| `results` | 1 | 0.9231 | 0.9231 |
| `study` | 3 | 0.8977 | 0.8000 |
| **total** | **20** | — | — |

### 6.3 gene 差异解读

高相似差异:

- `aging vs. young in C57BL6/J and 5xFAD mice`
- vs `aging vs. young in C57BL6/J and 5xFAD female and male mice`
- ROUGE-L F1 = 0.8571

低相似差异:

- `aging/AD hippocampus vs. young/wildtype`
- vs `aging/AD vs. control`
- ROUGE-L F1 = 0.6000

最低分来自 source quote 选择范围不同:

- 同样围绕 `Acvr1c is reduced in hippocampus...`
- 但两次截取的原文片段长度/范围不同
- ROUGE-L F1 = 0.3000

结论:

- 固定 chunked 后,row count 与 pathway 稳定。
- gene 的不一致集中在自由文本字段 `comparison` / `*_source`,不是 FK 或行数。
- 若要求 byte-identical,下一步要把 `comparison` 从 LLM 自由表述改为程序端 canonicalization,或只存 quote + deterministic parser。

### 6.4 新一族的比较


比较产物目录:[`agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/)

| 文件 | 内容 |
|---|---|
| [`row_count_summary.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/row_count_summary.csv) | top5/top8 各表 row count 对照 |
| [`gene_count_by_study.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/gene_count_by_study.csv) | 每个 study 的 gene row 数 |
| [`pathway_count_by_study.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/pathway_count_by_study.csv) | 每个 study 的 pathway row 数 |
| [`gene_top5_vs_top8_rouge_l.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/gene_top5_vs_top8_rouge_l.csv) | matched gene 字段级 ROUGE-L |
| [`pathway_top5_vs_top8_rouge_l.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/pathway_top5_vs_top8_rouge_l.csv) | matched pathway 字段级 ROUGE-L |

row count 结论:

| 表 | top5 | top8 | 解释 |
|---|---:|---:|---|
| `study` / `experiment` / `interventions` / `exercise` | 4 / 4 / 4 / 4 | 4 / 4 / 4 / 4 | 成功抽取的 study 集合一致,每个成功 study 有一个 exercise node |
| `sample` / `groups` | 80 / 13 | 80 / 13 | metadata-derived 结构稳定 |
| `gene` | 167 | 166 | gene 总量只差 1 行 |
| `pathway` | 20 | 18 | descriptive pathway 少 2 行 |
| `material` | 39 | 15 | metadata/material 自由抽取更漂移 |
| `documentation` | 10 | 11 | 文档/引用类表轻微漂移 |

ROUGE-L 结论:

| 对象 | matched | top5 only | top8 only | mean ROUGE-L F1 | min ROUGE-L F1 |
|---|---:|---:|---:|---:|---:|
| gene | 159 | 8 | 7 | 0.9532 | 0.2222 |
| pathway | 18 | 2 | 0 | 0.8897 | 0.2857 |

低分主要来自同义但表述不同的 comparison,例如 `endurance trained vs sedentary (baseline)` vs `ET vs SED (basal)`

---

## 7. 最近实跑成果汇总



### 7.1 Run-level 汇总

| run | 目的 | 输出目录 | 输入规模 | 成功抽取 | exercise | gene | pathway | LLM calls | cost/time | 关键结论 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| A/B chunked consistency A | 固定同一篇文章重复抽取,测试 gene/pathway 稳定性 | [`agentA_cohort_gene_consistency_chunked_a_0630`](output/agentA_cohort_gene_consistency_chunked_a_0630/) | 1 paper | 50 findings | 1 | 16 | 3 | 5 | ~$0.3107 | gene/exercise/pathway 行数稳定 |
| A/B chunked consistency B | 与 A 同设置复跑,用于 ROUGE-L 对照 | [`agentA_cohort_gene_consistency_chunked_b_0630`](output/agentA_cohort_gene_consistency_chunked_b_0630/) | 1 paper | 50 findings | 1 | 16 | 3 | 5 | ~$0.3099 | 行数一致,差异集中在自由文本字段 |
| keyword cohort top5 | `exercise skeletal muscle transcriptome`,扩大真实关键词 cohort | [`agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701/) | 5 papers | 4 full texts | 4 | 167 | 20 | 22 | $1.7232 / 776.57s | 4 篇成功入 SEA-CDM,1 篇 fetch failed |
| keyword cohort top8 | 同关键词扩大到前 8 篇,测试范围扩大后稳定性 | [`agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701/) | 8 papers | 4 full texts | 4 | 166 | 18 | 22 | $1.7087 / 851.62s | 新增 hit 多因 PDF/PMCID 问题未入库;成功 study 集合基本一致 |
| MoTrPAC big paper | 单篇大论文完整缓存全文 17 表抽取 | [`motrpac_big_paper_17table_0701`](output/motrpac_big_paper_17table_0701/) | 96,325 chars | 110 findings | 1 | 12 | 27 | 7 | $0.6383 / 236.21s | 大论文 chunked findings 跑通;12/12 gene 都连到 exercise |

### 7.2 关键产物链接

| run | gene | exercise | pathway | cost / comparison |
|---|---|---|---|---|
| A/B compare | [`rouge_l_differences.csv`](output/agentA_cohort_gene_consistency_chunked_compare_0630/rouge_l_differences.csv) | 同左 | 同左 | [`rouge_l_differences.csv`](output/agentA_cohort_gene_consistency_chunked_compare_0630/rouge_l_differences.csv) |
| top5 | [`gene.csv`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701/csv/gene.csv) | [`exercise.csv`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701/csv/exercise.csv) | [`pathway.csv`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701/csv/pathway.csv) | [`cost_timing.csv`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701/cost_timing.csv) |
| top8 | [`gene.csv`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701/csv/gene.csv) | [`exercise.csv`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701/csv/exercise.csv) | [`pathway.csv`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701/csv/pathway.csv) | [`cost_timing.csv`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701/cost_timing.csv) |
| top5 vs top8 compare | [`gene_top5_vs_top8_rouge_l.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/gene_top5_vs_top8_rouge_l.csv) | [`row_count_summary.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/row_count_summary.csv) | [`pathway_top5_vs_top8_rouge_l.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/pathway_top5_vs_top8_rouge_l.csv) | [`row_count_summary.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/row_count_summary.csv) |
| MoTrPAC big paper | [`gene.csv`](output/motrpac_big_paper_17table_0701/csv/gene.csv) | [`exercise.csv`](output/motrpac_big_paper_17table_0701/csv/exercise.csv) | [`pathway.csv`](output/motrpac_big_paper_17table_0701/csv/pathway.csv) | [`cost_timing.csv`](output/motrpac_big_paper_17table_0701/cost_timing.csv) |

---

## 8. top5 vs top8 的 gene/pathway 差异明细

比较对象:

- top5:[`agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_0701/)
- top8:[`agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701`](output/agentA_cohort_experiment_exercise_skeletal_muscle_gene_top8_0701/)
- 比较目录:[`agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/)

### 8.1 总体差异

| table | top5 | top8 | 差异 |
|---|---:|---:|---:|
| `gene` | 167 | 166 | -1 |
| `pathway` | 20 | 18 | -2 |

按 study 拆开:

| study | top5 gene | top8 gene | gene 差异 |
|---|---:|---:|---:|
| `GSE250122` | 49 | 47 | -2 |
| `GSE270703` | 47 | 51 | +4 |
| `GSE279359` | 47 | 44 | -3 |
| `PMC12181168` | 24 | 24 | 0 |

| study | top5 pathway | top8 pathway | pathway 差异 |
|---|---:|---:|---:|
| `GSE270703` | 10 | 9 | -1 |
| `GSE279359` | 2 | 2 | 0 |
| `PMC12181168` | 8 | 7 | -1 |

### 8.2 Gene 差异:only rows

比较文件:[`gene_top5_vs_top8_rouge_l.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/gene_top5_vs_top8_rouge_l.csv)

| status | count |
|---|---:|
| matched | 159 |
| top5_only | 8 |
| top8_only | 7 |

top5 only:

| study | gene / phrase | direction | comparison |
|---|---|---|---|
| `GSE279359` | `RNA-binding proteins (RBPs)` | down | post-exercise vs pre-exercise (mmYS) |
| `GSE279359` | `RNA-binding proteins (RBPs)` | down | post-exercise vs pre-exercise (hsYS) |
| `GSE279359` | `RNA-binding proteins (RBPs)` | down | post-exercise vs pre-exercise (hsAS) |
| `GSE279359` | `RNA-binding proteins (RBPs)` | down | post-exercise vs pre-exercise (hsAA) |
| `GSE279359` | `RBP genes (61 genes)` | changed | mmYS-pre vs post-acute exercise time points |
| `GSE250122` | `PGK1` | up | sedentary vs endurance trained |
| `GSE250122` | `EGFR` | up | sedentary vs endurance trained |
| `GSE250122` | `EGF` | up | sedentary vs endurance trained |

top8 only:

| study | gene / phrase | direction | comparison |
|---|---|---|---|
| `GSE279359` | `RNA-binding proteins (RBPs)` | up | post-exercise vs pre-exercise (mmYS) |
| `GSE279359` | `RBP genes (61 genes without significant DGE)` | changed | mmYS pre vs post-acute exercise |
| `GSE250122` | `acute exercise-responsive genes` | unchanged | ET vs SED |
| `GSE270703` | `fast myofiber upregulated genes` | up | post-training vs pre-training, fast myofibers |
| `GSE270703` | `fast myofiber downregulated genes` | down | post-training vs pre-training, fast myofibers |
| `GSE270703` | `slow myofiber upregulated genes` | up | post-training vs pre-training, slow myofibers |
| `GSE270703` | `slow myofiber downregulated genes` | down | post-training vs pre-training, slow myofibers |

方向冲突补充:

| study | gene / phrase | comparison | top5 direction | top8 direction | source check | 判断 |
|---|---|---|---|---|---|---|
| `GSE279359` | `RNA-binding proteins (RBPs)` | post-exercise vs pre-exercise (mmYS) | down | up | 两次的 source 都指向 `significantly down-regulated`; top8 的 magnitude 又混入 `10 up-regulated, 7 down-regulated` | 这是 direction 抽取错误,不是普通 ROUGE-L 文本漂移 |

source 原文:

- top5 `gene_symbol_source` / `comparison_source` / `magnitude_source`: `The mmYS cohort had 3 RBPs that were significantly down-regulated with`
- top8 `gene_symbol_source` / `comparison_source` / `magnitude_source`: `The mmYS cohort had 3 RBPs that were significantly down-regulated with`
- top8 `magnitude`: `3 RBPs significantly down-regulated (p-adj < .05); 17 additional RBP genes (10 up-regulated, 7 down-regulated, raw p < .05)`

解读:

- `RNA-binding proteins (RBPs)`、`RBP genes`、`fast/slow myofiber genes`、`acute exercise-responsive genes` 都更像 gene set / 描述性 gene phrase,不是严格单 gene symbol。
- 真正 strict gene symbol 差异主要集中在 `PGK1`、`EGFR`、`EGF` 等少数行。
- 这说明 gene 行数差异主要来自 gene phrase 过滤和 canonicalization 不足,不是 `gene.exercise_id` 外键失败。
- 但 `GSE279359` 的 RBP 例子说明还存在更严重的 direction consistency 问题:当一句话同时出现显著 down 和额外 up/down 计数时,LLM 可能把同一 finding 合并成一行并选错 `regulation_direction`。后续需要 source-grounded direction validation:source 明确 down/up 时必须和字段一致;同一句包含 up/down 混合结果时应拆成多行,或将 direction 标成 `changed` 并加冲突标记。

### 8.3 Matched gene 中 ROUGE-L 低分例子

| study | gene | direction | ROUGE-L | top5 comparison | top8 comparison |
|---|---|---|---:|---|---|
| `GSE250122` | `TNFSF10` | up | 0.2222 | endurance trained vs sedentary (baseline) | ET vs SED (basal) |
| `GSE250122` | `IDO` | up | 0.2222 | endurance trained vs sedentary (baseline) | ET vs SED (basal) |
| `GSE279359` | `mFos` | changed | 0.4286 | mmYS-pre vs post-acute exercise time points | mmYS post-exercise vs mmYS-pre |
| `GSE279359` | `mFbxo32` | changed | 0.4286 | mmYS-pre vs post-acute exercise time points | mmYS post-exercise vs mmYS-pre |
| `GSE279359` | `mUbe2d1` | changed | 0.4286 | mmYS-pre vs post-acute exercise time points | mmYS post-exercise vs mmYS-pre |
| `GSE250122` | `SOD2` | up | 0.6000 | post acute exercise vs pre-exercise | acute exercise vs rest |
| `GSE250122` | `HMOX1` | up | 0.6000 | post acute exercise vs pre-exercise | acute exercise vs rest |

解读:

- `ET vs SED` 与 `endurance trained vs sedentary` 是同义缩写/全称差异。
- `baseline`、`basal`、`pre-training`、`pre-exercise` 这类词需要 canonicalize 成统一 control label。
- 所以 matched gene 的低分主要是 comparison 文本漂移,不是 gene identity 漂移。

### 8.4 Pathway exact diff

比较文件:[`pathway_top5_vs_top8_rouge_l.csv`](output/agentA_cohort_exercise_skeletal_muscle_top5_vs_top8_compare_0701/pathway_top5_vs_top8_rouge_l.csv)

top5 有、top8 没有:

| study | pathway |
|---|---|
| `PMC12181168` | `senescence-associated gene sets` |
| `PMC12181168` | `SASP` |
| `GSE270703` | `sarcoplasmic and sarcoplasmic reticulum genes pathway` |
| `GSE270703` | `angiogenesis` |
| `GSE270703` | `mitochondrial biogenesis` |

top8 有、top5 没有:

| study | pathway |
|---|---|
| `PMC12181168` | `senescence-associated gene sets (including SASP)` |
| `GSE270703` | `myofibril genes (cellular components pathway)` |
| `GSE270703` | `sarcoplasmic and sarcoplasmic reticulum genes` |

### 8.5 Pathway ROUGE-L 对齐

| study | top5 pathway | top8 pathway | ROUGE-L |
|---|---|---|---:|
| `PMC12181168` | `SASP` | `senescence-associated gene sets (including SASP)` | 0.2857 |
| `GSE270703` | `angiogenesis` | `regulation of angiogenesis pathway` | 0.4000 |
| `GSE270703` | `mitochondrial biogenesis` | `mitochondrial matrix pathway` | 0.4000 |
| `PMC12181168` | `senescence-associated gene sets` | `senescence-associated gene sets (including SASP)` | 0.8000 |
| `GSE270703` | `sarcoplasmic and sarcoplasmic reticulum genes pathway` | `sarcoplasmic and sarcoplasmic reticulum genes` | 0.9091 |

解读:

- `senescence-associated gene sets` 和 `SASP` 在 top8 被合并成 `senescence-associated gene sets (including SASP)`。
- `angiogenesis` 和 `regulation of angiogenesis pathway` 是同一概念不同粒度。
- `mitochondrial biogenesis` 被对齐到 `mitochondrial matrix pathway` 的 ROUGE-L 只有 0.4,这个可能不只是措辞差异,而是 pathway concept 选择漂移。
- 因此 pathway 差异比 gene 更需要 ontology/canonical label:至少要把 descriptive pathway 映射到 GO/KEGG/MSigDB 或内部 canonical pathway key。


