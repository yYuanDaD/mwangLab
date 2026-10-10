# Claim Card JSON 阅读指南

本文档用于阅读项目中的 `ArticleResultCard` JSON，示例以
`output/claim_evidence_repeat_v1/repeat_01/cards/GSE282641.json` 为准。

这类 JSON 不是单纯的论文摘要，也不是单纯的分析结果表，而是把三类信息放在一起：

1. 论文声称了什么（claim）；
2. 我们手里有哪些证据（evidence）；
3. 证据与 claim 的关系是什么（link）。

最重要的原则是：

> `trustworthy` 表示证据通过了当前的来源、文件和技术完整性检查；它不表示证据已经在生物学上证明了论文结论。

---

## 1. 推荐阅读顺序

不要从第一行开始逐字段孤立阅读。推荐按照下面的顺序：

```text
annotation_status / deliverable_level
        ↓
claims
        ↓
evidence
        ↓
links
        ↓
secondary_findings / limitations
```

具体做法：

1. 先确认这张卡是机器草稿、人工审核版还是 gold 版本；
2. 阅读 `claims`，确定论文的主要和次要结论；
3. 阅读 `evidence`，确认每条证据来自论文、计算分析还是描述性 QC；
4. 通过 `links` 判断证据对每条 claim 是直接支持、部分支持还是不可评估；
5. 最后检查次级发现和限制条件，防止把“有结果”误读成“验证了论文结论”。

---

## 2. 顶层字段

### `schema_version`

JSON 结构的版本号。

- 用途：判断字段定义属于哪个版本；
- 阅读方法：如果版本变化，不能直接假设旧 JSON 和新 JSON 的字段完全兼容；
- 它不是数据质量分数，也不是模型版本号。

### `article_id`

论文标识符，当前示例为 `PMID40627397`。

- 通常使用 PMID、DOI 或项目定义的文章 ID；
- 用于把 claim 的来源定位到具体论文；
- 它不等于 GEO accession。

### `accessions`

这张卡所针对的 GEO 或其他数据 accession 列表。

示例：

```json
"accessions": ["GSE282641"]
```

阅读时要特别注意：

- `article_id` 说明是哪篇论文；
- `accessions` 说明当前卡分析的是哪批数据；
- 论文可能包含多个 accession，但本卡可能只针对其中一个。

### `annotation_status`

标记卡片的审核状态：

- `machine_draft`：机器生成，尚未完成领域专家审核；
- `human_reviewed`：已经由人工检查；
- `gold`：可作为正式评测或金标准使用。

GSE282641 当前是 `machine_draft`。因此，即使其引用、文件和 ID 审计通过，也不能把它当成最终人工确认结论。

### `deliverable_level`

描述当前卡片能交付到什么程度，例如完整重分析、仅元数据、仅论文证据或不可评估等。

示例中的值为 `full_reanalysis`，表示该 accession 至少完成了主要分析流程，并生成了 QC、DEG、GSEA 等分析产物。

这个字段描述“完成了多少工作”，不直接表示“论文结论有多正确”。

---

## 3. `claims`：论文结论列表

`claims` 是一组 `PaperClaim` 对象。每个对象代表论文中一个可以单独检查的结论。

### `claim_id`

程序生成的稳定 claim ID，例如：

```text
CLM-1, CLM-2, CLM-3
```

- 只用于引用和关联；
- 不表示结论强弱；
- `CLM-1` 不一定比 `CLM-2` 更正确，只是排列顺序不同。

### `statement`

对论文结论的结构化表述。

阅读时应问：

- 这句话是否真的表达了论文的结论？
- 是否混入了模型自己的推断？
- 是否明确了对象、处理、比较组、时间点和终点？

GSE282641 的 `CLM-1` 涉及 HIF1α、骨骼肌、昼夜节律代谢、早期休息期运动和糖酵解等多个维度。后续判断需要检查这些维度是否都被当前 accession 的数据覆盖。

### `importance`

通常为：

- `primary`：论文的主要结论；
- `secondary`：次要结论、机制补充或附带结论。

阅读重点：主要 claim 应当有对应 link；如果主要 claim 没有足够证据，应该明确记录为 `not_evaluable`，不能用次要结果代替。

### `source_quote`

论文原文中的短引用。

- 应当是论文中的逐字内容；
- 用于人工快速核查；
- 不是模型的总结句。

如果引用无法在原文中找到，应降低对该 claim 的信任，并要求人工复核。

### `source_uri`

论文原文或本地论文文本的来源地址/路径。

- 用于追溯引用来自哪个文件；
- 与 `source_locator` 配合使用；
- 不是数据分析 artifact 的路径。

### `source_locator`

引用在论文中的位置，例如章节、页码、段落或经过验证的文本偏移位置。

当前程序会在标准化文本后追加类似“verified normalized-text offset”的定位信息。

阅读时，先看 `source_quote`，需要复核时再用 `source_uri + source_locator` 回到原文。

### `scope`

结论的生物学范围，由 `BiologicalScope` 表示。它是判断“证据是否真的对应这条 claim”的核心字段。

#### `scope.organism`

研究对象的物种，例如 mouse、human。

#### `scope.population_or_model`

实验模型、基因型、人群或细胞系，例如 HIF1α skeletal-muscle-specific knockout。

#### `scope.tissue_or_cell`

组织或细胞类型，例如 skeletal muscle。

#### `scope.intervention`

干预、刺激或处理，例如 exercise。

#### `scope.comparator`

比较组，例如 WT、vehicle 或 control。

#### `scope.timepoint`

时间点、昼夜节律时间或处理时长，例如 ZT3。

#### `scope.endpoint`

测量终点，例如 differential gene expression、glycolysis 或 fatty-acid oxidation。

#### `scope.mechanism`

论文声称的机制，例如 HIF1α regulation of circadian metabolism。

判断 link 时，不能只看“基因名是否相同”，还要比较这些 scope 维度是否一致。

---

## 4. `evidence`：证据列表

`evidence` 是一组 `AnalysisEvidence` 对象。证据可以来自计算分析、论文原文或描述性检查。

### `evidence_id`

程序生成的证据 ID，例如：

```text
E-QC
E-DEG
E-GSEA
E-PAPER-1
```

后面的 `links.evidence_id` 和 `secondary_findings.evidence_ids` 都通过这个 ID 引用证据。

### `accession`

该证据明确对应的数据 accession。

阅读时要区分：

- 有具体 accession：通常可以进行 accession-level 判断；
- 没有具体 accession：可能只是论文整体描述；
- 另一个 accession：不能拿来支持当前 accession 的结论。

GSE282641 中的论文证据带有 `paper_wide_scope_not_accession_specific` 标记，表示论文确实报告了该机制，但没有明确说它来自当前 GSE282641 的这一项重分析。

### `evidence_type`

证据类型。常见值包括：

- `deg`：差异表达结果；
- `gsea`：通路富集结果；
- `reported_result`：论文报告的结果；
- `phenotype`：表型证据；
- `qc`：质量控制结果；
- `metadata`：元数据或实验设计信息；
- `other`：其他证据。

类型只说明“是什么”，不说明“是否支持 claim”。支持关系要看 `links`。

### `origin`

证据来源层级：

- `computed`：由本项目代码计算得到，例如 DEG、GSEA；
- `paper_reported`：论文原文报告的结果；
- `descriptive`：描述性信息，例如 QC 或流程状态。

例如：

```text
E-DEG   → computed
E-GSEA  → computed
E-PAPER → paper_reported
E-QC    → descriptive
```

### `statement`

对证据内容的简短结构化描述。

例如：

```text
DESeq2 found 394 genes at padj<0.05 for ko vs wt
```

这句话只说明分析得到了什么，不自动说明它支持论文的哪条 claim。

### `contrast`

统计比较的两组，例如 `ko vs wt`。

它对 DEG 和 GSEA 尤其重要。阅读时要确认：

- treatment/control 是否方向正确；
- 是否与 claim 的比较组一致；
- 是否遗漏了时间点、组织或刺激条件。

### `trustworthy`

证据是否通过当前程序定义的技术和来源门槛。

对计算证据，主要检查：

- 分析流程状态是否正常；
- sanity check 是否通过；
- 结果 artifact 是否存在；
- 文件是否可以追溯和校验。

对论文证据，主要检查：

- quote 是否能在本地论文文本中找到；
- 来源定位是否完整；
- 论文文件 hash 是否记录。

重要：`trustworthy=true` 不是“已证明论文结论”，而是“可以进入 claim-evidence 关系判断”。如果 scope 不匹配，后续仍可能是 `partial_support` 或 `not_evaluable`。

### `sanity_flags`

程序检查得到的状态标签。

示例：

```text
deg_sanity:ok
pipeline_status:deg_gsea_ok
paper_wide_scope_not_accession_specific
reported_for_other_accession
```

阅读时优先查看是否有：

- `deg_sanity:ok`；
- pipeline failure 或 skip 标记；
- accession 范围不一致；
- 仅描述性、不能用于生物学推断的提示。

### `artifact_paths`

证据对应的本地文件路径，例如 DEG CSV、GSEA CSV、QC 表或论文文本。

阅读时可以沿此路径检查原始结果。路径存在不等于结果正确，但没有路径时通常无法完成审计。

### `artifact_sha256`

对应 artifact 的 SHA-256 校验值。

用途是确认：

- card 记录的文件没有被替换；
- 后续复核使用的文件和生成 card 时的文件一致。

hash 是文件完整性凭证，不是统计显著性或生物学可信度分数。

### `source_locator`

证据的来源定位。

- 对论文证据，通常指原文位置；
- 对计算证据，通常指结果文件、日志或对应分析记录；
- 对 QC/metadata，可用于定位输入或流程输出。

### `scope`

证据实际覆盖的生物学范围。它应当和 claim 的 `scope` 比较，而不是只看 statement 文本。

例如 `E-DEG` 的 scope 可能只有 `KO vs WT + differential gene expression`，但 claim 还要求 exercise + ZT3；这种情况下只能部分支持或无法评估。

---

## 5. `links`：claim 与 evidence 的关系

`links` 是理解整张 card 的核心。每个 `ClaimEvidenceLink` 回答：

> 这条证据能否支持这条具体论文结论？

### `link_id`

程序生成的关系 ID，例如 `LNK-1`。

只用于引用和审计，不代表关系强弱。

### `claim_id`

被评估的 claim，例如 `CLM-2`。

### `evidence_id`

用于支持或评估该 claim 的证据，例如 `E-GSEA`。

`not_evaluable` 关系可以没有 evidence，表示当前没有足够对应证据；即使带有 evidence，也表示该 evidence 不能用于支持该 claim。

### `relation`

关系类型：

- `direct_support`：证据在关键 scope 维度上与 claim 一致，可以直接支持；
- `partial_support`：只支持 claim 的一部分；
- `secondary_finding`：证据对应的是次级发现，不足以支持主要 claim；
- `contradictory`：证据与 claim 方向相反；
- `not_evaluable`：证据不足、范围不匹配或无法判断。

其中 `not_evaluable` 不是“分析失败”，而是“不能据此判断该 claim”。

### `rationale`

程序/LLM 对关系判断的解释。

阅读时重点找两类信息：

- 支持了哪些维度；
- 缺失或冲突了哪些维度。

例如 GSE282641 中，E-GSEA 可以支持 oxidative pathways，但没有明确覆盖 ZT3 exercise 条件，因此对 CLM-2 是 `partial_support`。

### `dimension_alignment`

记录 claim 和 evidence 在哪些 scope 维度上匹配，例如组织、基因型、比较组、时间点、终点或机制。

它比单纯的自然语言 rationale 更适合审计，因为可以明确看到“匹配了什么、没有匹配什么”。

### `confidence`

对这条关系判断的置信度，通常由关系提议模型给出，范围为 0 到 1。

注意：

- 它是关系置信度，不是 evidence 的 `trustworthy`；
- 当前规则对低置信度的 `direct_support` 会自动降级为 `partial_support`；
- 它不是经过 gold 数据校准的准确率。

---

## 6. `secondary_findings`：保留但不冒充主结论的结果

`secondary_findings` 用来保存有价值、但不能直接验证主要 claim 的结果。

### `finding_id`

次级发现 ID，例如 `SF-1`。

### `statement`

该次级发现的内容。

### `evidence_ids`

支撑该次级发现的证据 ID 列表。

例如，某个论文机制描述可以保留为 `SF-1`，但不把它升级成“当前 GEO 重分析已证明该机制”。

### `rationale`

解释为什么它被保留为次级发现，而不是 primary claim 的直接支持。

程序会自动把未被其他 link 使用、且本身通过技术门槛的 DEG/GSEA 结果加入 secondary finding，避免丢失分析结果，同时避免过度解读。

---

## 7. `limitations`：必须一起阅读的限制条件

`limitations` 是卡片级限制说明，通常合并了三类内容：

1. 论文文本摘录限制，例如只使用了 Significance、Abstract、Introduction；
2. 当前 accession 的分析范围限制，例如只做了 KO–WT，没有解析 ZT3 或 exercise 分层；
3. 证据关系限制，例如论文报告结果不能证明当前 accession 完整复现论文结论。

阅读时不要把 limitations 当成附注。它们经常直接决定某个 link 为什么只能是 `partial_support` 或 `not_evaluable`。

---

## 8. GSE282641 的完整阅读示例

### 第一步：确认卡片状态

```text
annotation_status = machine_draft
deliverable_level = full_reanalysis
accessions = [GSE282641]
```

含义：该 accession 完成了较完整的重分析，但卡片仍是机器草稿。

### 第二步：看主要 claim

`CLM-1` 是主要 claim，涉及 HIF1α、骨骼肌、昼夜节律、运动和糖酵解。

这意味着后续证据不只要有“差异基因”，还要检查是否有对应的组织、处理和时间点。

### 第三步：看计算证据

```text
E-QC   → 64 个样本 QC
E-DEG  → KO vs WT，394 个差异基因
E-GSEA → KO vs WT，45 个 Hallmark sets
```

这些证据的 artifact 和 hash 都已记录，因此可以进入关系判断。

### 第四步：看关系，而不是只看 trustworthy

```text
CLM-2 ← E-GSEA → partial_support
CLM-3 ← E-DEG  → not_evaluable
```

解释：

- E-GSEA 的结果可以支持氧化代谢方向，但没有完整覆盖 ZT3 exercise 条件；
- E-DEG 虽然技术上可信，但 KO–WT 结果不足以判断“ZT3 时 HIF1α 驱动更强糖酵解响应”。

### 第五步：读限制条件

最终结论应写成：

> 当前重分析结果对部分代谢方向提供支持，但不足以直接验证论文关于特定运动时间点和条件的完整结论。

---

## 9. 机器阅读时的检查清单

### 先查结构

- `schema_version` 是否兼容；
- ID 是否唯一；
- 每个 link 的 claim/evidence ID 是否存在；
- 是否有 primary claim 没有 link；
- 是否有缺失的 source quote 或 source locator。

### 再查证据

- `trustworthy` 是否为 true；
- `artifact_paths` 是否存在；
- `artifact_sha256` 是否匹配；
- `sanity_flags` 是否有失败、跳过或范围冲突；
- accession 是否与当前 card 一致。

### 最后查科学关系

- claim 和 evidence 的 organism 是否一致；
- tissue/cell 是否一致；
- intervention 和 comparator 是否一致；
- timepoint 是否一致；
- endpoint 是否一致；
- 关系是否应为 direct、partial 或 not_evaluable；
- 是否把次级发现误当成主要结论验证。

---

## 10. 常见误读

### 误读一：`trustworthy=true` 就等于论文结论被验证

错误。它只表示证据来源和技术完整性通过门槛。

### 误读二：有 DEG 就一定支持论文 claim

错误。还必须匹配实验设计、组织、时间点、干预和终点。

### 误读三：`confidence=0.6` 是证据可信度 60%

错误。它是 claim-evidence 关系的模型置信度，不是统计概率，也不是 gold 评测准确率。

### 误读四：`not_evaluable` 等于没有数据

错误。可能有数据，但实验范围不足以判断该 claim。

### 误读五：论文报告的结果和当前 accession 的结果可以直接合并

错误。论文级证据需要检查 accession 是否明确对应；否则只能保留为 paper-wide finding 或 secondary finding。

---

## 11. 与 SEA-CDM 的关系

SEA-CDM 或 DEG/GSEA/QC 输出属于结构化研究数据和分析结果层；Claim Card 属于结论—证据关系和审核层。

```text
SEA-CDM / QC / DEG / GSEA
            ↓
      AnalysisEvidence
            ↓
PaperClaim ↔ ClaimEvidenceLink
            ↓
      ArticleResultCard
```

因此，Claim Card 不替代 SEA-CDM。它引用 SEA-CDM 或分析 artifact，并进一步回答：

> 这些结构化结果是否足以支持论文中的哪一个具体结论？

---

## 12. 一句话汇报版本

> Claim Card 是把论文 claim、计算证据和来源 provenance 放到同一张可审计记录中；`trustworthy` 负责判断证据能否入场，`link relation` 负责判断它是否真的支持某条结论。

相关实现文件：

- `tools/claim_evidence.py`：最终 Card schema、校验器和审计逻辑；
- `test/experiments/claim_evidence_alignment/prefill.py`：从论文提取 schema 到 Card 的组装流程；
- `output/claim_evidence_repeat_v1/repeat_01/cards/GSE282641.json`：实际示例。

