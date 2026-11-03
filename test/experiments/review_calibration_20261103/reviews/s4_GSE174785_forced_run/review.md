# 复核结论 case_07 / GSE174785

**总体: fix**

该系列没有运动组，只有比目鱼与趾长伸肌内皮细胞（及Atf4敲除）的基线比较，运行记录应明确不是运动对照分析。更重要的是矩阵仍是转录本水平（ENSMUST，9.7万行），1177个DEG是转录本数，并且论文的782只是RmEC高表达方向（另有140个WmEC高表达），因此与论文的比较口径不一致，需要汇总到基因水平后重跑并重新比较。分组、方向、阈值和联合模型与论文一致；配对信息无法确认，已被表达检查否定支持。

## 不一致项

### run_or_refuse (disagree, major)
- 证据: Series has no exercise arm (B1; packet A 'Values with exercise words: none'). Record runs it as primary with primary_estimand 'Exercise-primed vs non-primed ECs' and only a caveat 'exercise priming inferred from muscle type'.
- 修改: Label the case in the spec/HANDBACK as a baseline oxidative-vs-glycolytic EC (fibre-type) comparison from an exercise paper, not an exercise-vs-control analysis; do not describe it as an exercise result. Policy on whether such series count is for the person (human_items).

### pairing (unsure, minor)
- 证据: B3: paper silent on animal identity; key genotype + rep suffix links 20/20 once each but expression check not_supported (p 0.88). decisions.json never mentions the candidate key; covariance reasoning only says 'one sample per sorted EC pool'.
- 修改: Record in covariance/design reasoning that soleus-vs-EDL pairing by genotype+rep was considered, the expression check did not support it, and the animal identity is undocumented (confirm with authors/Data S1). No model change needed on current evidence.

### matrix_method (disagree, major)
- 证据: matrix decision: feature_level 'transcript (ENSMUST)', 129,439 features, integer_fraction 0.62, and its own reasoning says 'a gene-level summary would be needed before DESeq2'. DEG_results_...WT.csv has 96,971 ENSMUST transcript rows and 1177 'DEGs' are transcripts; no gene mapping, so Atf3/Atf4 cannot be checked. Paper counts are genes (kallisto counts processed for DESeq2).
- 修改: Summarise est_counts to gene level (tx2gene via Ensembl mouse annotation, sum per gene, round) and rerun DESeq2 for both contrasts; report DEGs per gene and confirm Atf3/Atf4 among top DEGs.

### paper_match (disagree, major)
- 证据: comparison pairs ours 1177 (up 945 + down 232, transcripts) with paper 782. B5: 782 is the count higher in RmEC (140 higher in WmEC), so total paper DEGs = 922 and the like-for-like pair is up 945 vs 782 / down 232 vs 140, at transcript not gene level. Also KO 'paper 211' is the number of WT DEGs still different after KO, not a KO DEG count, and no KO comparison is made against it.
- 修改: Record paper counts as 782 up / 140 down (922 total) and compare after gene-level rerun; compare 211/126 as overlap of KO DEGs with WT DEGs; restate HANDBACK so it does not claim reproduction on the 1177 vs 782 pair.

## 需要人工判断
- Whether a series comparing baseline oxidative vs glycolytic muscle ECs (no exercise-vs-sedentary arm) counts as an exercise study and should be run as primary.
- Whether the paper's DEG counts 782/140 were obtained at gene level with log2 FC; and whether SOL and EDL samples with the same rep number come from the same mouse (ask authors / Data S1).
