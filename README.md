# mwangLab Bioinformatics Agent

一个基于 LangChain / LangGraph 与 Claude 的生物信息学智能体，面向 GEO
数据检索、RNA-seq 分析、多队列处理和 SEA-CDM 结构化结果提取。

## 核心特点

- **自然语言驱动分析**：用户可以直接用中文描述研究问题，由 Agent 选择并调用对应工具完成分析。
- **单研究与队列两种模式**：既支持输入一个 GEO accession，也支持按关键词搜索 GEO 并批量处理多个研究。
- **端到端 RNA-seq 工作流**：覆盖数据下载、预处理、样本 QC、PCA、相关性分析、差异表达、GO/KEGG ORA 和 MSigDB Hallmark GSEA。
- **按矩阵类型选择统计方法**：原始整数 counts 使用 DESeq2；log-scale、FPKM/TPM 和蛋白质组强度矩阵使用 limma；避免把不适合的数据错误送入 DESeq2。
- **多组学扩展**：包含 bulk RNA-seq、scRNA-seq pseudobulk、甲基化和蛋白质组数据的处理工具。
- **自动实验设计识别**：从 metadata 中推断 control/treatment；启发式结果不可靠时，可由 LLM 校验、覆盖或拒绝 contrast。
- **稳健的样本对齐**：依次尝试精确匹配、子串匹配和 token-overlap；仍失败时使用 LLM 解析实验室缩写，不使用可能造成生物学错误的位置对齐。
- **失败显式化**：无法识别矩阵、样本无法对齐、实验设计不明确或 GSEA 失败时明确记录原因，不用静默降级掩盖问题。
- **批处理故障隔离**：单个研究失败不会中断整个 cohort；每次运行生成统一 summary、完整 workflow log、failure log 和结构化 decision log。
- **程序化 Agent 护栏**：工具调用支持参数级去重、结果缓存和单工具调用次数上限，从代码层阻止重复调用循环。
- **结构化科研数据提取**：通过 Pydantic 约束 LLM 输出，并将论文、实验设计、分析结果与 provenance 整理为 SEA-CDM 风格记录。
- **论文优先的数据发现**：支持论文搜索、全文抓取、数据 accession 提取、论文自有数据与引用数据辨别，以及论文级交付记录组装。
- **可追溯与可复现**：记录数据来源、自动决策、LLM 判断、统计方法、contrast 和输出文件路径，并支持重复子集分析的一致性评估。

## TODO

- [ ] 将 SEA-CDM 提取器完整迁移到权威的 13 表关系模型，并补齐 ontology ID 与字段级 provenance。
- [ ] 实现 paper-first 批处理 orchestrator，一次处理多篇论文及其对应数据集。
- [ ] 加强 GEO 和论文候选的关键词相关性排序，减少无效下载与全文抓取。
- [ ] 建立 control/treatment 同义词学习回路，把 LLM 发现的新术语反馈给设计识别模块。
- [ ] 为多因素、多时间点和多 treatment arm 研究提供交互项、协变量和多 contrast 建模。
- [ ] 扩展基因标识符识别与转换，支持 numeric/internal IDs 以及更多非 Ensembl 标识符。
- [ ] 增加按性别或其他亚组分层的差异表达分析，并支持 `condition × subgroup` 交互模型。
- [ ] 完善蛋白质组矩阵路由、TMT/iTRAQ 跨批次归一化和真实 labeled 数据验证。
- [ ] 接入 MoTrPAC 公共数据与官方结果，验证差异基因和通路结果的一致性。
- [ ] 统一旧版 `seacdm.json` 与新版表结构输出路径，清理仍在使用的兼容层。
- [ ] 为核心模块补齐统一的自动化测试入口、依赖锁定和持续集成配置。

