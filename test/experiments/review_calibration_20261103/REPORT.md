# 复核员校准结果（2026-11-03 开始，2026-11-10 完成）

结论：**通过**。种入错误 + 真实案例检出 **6/6**（要求 ≥5/6）；干净案例经人工裁定后误报 **0/5**（要求 ≤1/5）。
复核员为只读子代理（请求模型 sonnet），每例约 9.9 万 tokens、约 1 分钟。

## 1. 种入错误与真实案例：6/6 检出

| 案例 | 种入/真实错误 | 期望检查项 | 复核员结论 | 严重度 | 判定 |
|---|---|---|---|---|---|
| s1 GSE267512 | 前后配对设计去掉了受试者项（~ time） | pairing | pairing 不同意：论文 `~ ID + timepoint`，已派生 subject 列却未用；79 vs 214 | blocking（另 model_fit、paper_match 为 major） | 检出 |
| s2 GSE178262 | DA vs CTRL 写反为 CTRL vs DA | direction | direction 不同意：执行的 log2FC 是 CTRL/DA，与计划相反，举例 Nr4a3 −3.88 | **major**（说明书规定符号反了是 blocking） | 检出，严重度偏低 |
| s3 GSE236613 | 论文 raw p<0.05 且 FC 1.2 写成 padj<0.05 | threshold | threshold 不同意：逐字引用 S2.8.p1，给出正确规则；另指出“已复现”说法夸大（5 vs 4423） | major | 检出 |
| s4 GSE174785 | 无运动组的系列被当作“运动预适应”比较硬跑 | run_or_refuse | run_or_refuse 不同意：无运动组，应标为基线纤维类型比较 | **major**（说明书规定“无运动组”是 blocking） | 检出，严重度偏低 |
| s5 GSE319603 | 运动效应取 HM vs C（饮食混杂），应为 HM vs H | grouping; run_or_refuse; paper_match | direction 与 paper_match 不同意：对照应为 H；563 是 HM vs H 的数，不能和 HM vs C 比 | blocking | 检出（归在 direction，不在 grouping） |
| r1 GSE283493（真实） | 以“无动物编号”停止；组别+字母可配 24 对 | stop_reason; pairing | 两项都不同意：只检验了单独字母；组别+字母 48/48 一一配对，表达检查支持（同键 r 0.345 vs −0.01，p=0.0005），论文写明 SAT/VAT 取自同一鼠 | major | 检出；修正建议与说明书一致（停止理由改正 + 以该键做敏感性分析） |

种入案例中复核员还发现了**种入时带进来的真实问题**，都属实：
- s4：矩阵是转录本水平（ENSMUST，96,971 行），1177 个“DEG”是转录本；论文 782 只是 RmEC 高表达一侧（另有 140 个）。属实，是种入 spec 时没做基因汇总。
- s3：次要对比 Sham vs NE 方向与论文相反（原运行已注明），列为 minor，合理。

## 2. 干净案例：误报 0/5

score.py：5 例中 blocking/major 的“不同意”为 0。下面逐条裁定所有 major 级“不确定”和较重的 minor 项。

| 案例 | 复核员结论 | 被提出的事项 | 人工裁定 |
|---|---|---|---|
| c1 GSE164890 | pass | 无 | — |
| c2 GSE344550 | pass | 无（拒绝理由成立） | — |
| c3 GSE324100 | pass | confounding 不确定/minor：运动鼠单笼、静息鼠群养，饲养方式与运动因素混叠，未记录 | **属实，非误报**：论文 S2.8.p1 和 GEO treatment_protocol 都写了静息鼠群养；严重度 minor 合适 |
| c4 GSE302867 | human | paper_match 不确定/major：WT_Ex vs WT_Sed 的 Hallmark OXPHOS NES −2.64，论文 Fig 2e 为 +5.14，方向相反 | **属实，非误报**：原运行 HANDBACK 写明了这一反向且原因未解决；study caveats 只写了 GSEA 方法偏离，没写反向结果。是记录不完整，不是分析错误；交人工判断合理 |
| c5 GSE230002 | pass | minor：论文 877 与 p<0.01（981）最接近，未写进差异记录 | 属实，minor 合适 |

政策性问题（联合/分组拟合、报告哪个阈值）都放进了 `human_items`，没有当成错误。

## 3. 成本

| 指标 | 均值 | 范围 |
|---|---|---|
| tokens / 例（harness 报告的 subagent_tokens，含缓存读取） | 98,917 | 86,464 – 110,899 |
| 分钟 / 例 | 1.0 | 0.4 – 1.5 |
| 工具调用 / 例 | 12 | 8 – 16 |

11 例合计约 109 万 tokens、11 分钟。模型：每次都请求 sonnet；11 份 review.json 都自报 Sonnet 5.5，且 11-03 两例因额度中断时的报错显示发给 API 的模型是 `claude-sonnet-5-5`。可以认为确实跑在 Sonnet 上（transcript 里没有逐条模型字段，无法再细查）。

## 4. 建议的改动

| # | 改哪里 | 改动 | 依据 |
|---|---|---|---|
| 1 | decision-review.md，Severity | 写明：主对比符号反了，**即使 DEG 数不变**也是 blocking | s2 判 major，理由是“DEG 集合和数量不变” |
| 2 | decision-review.md，Severity / run_or_refuse | 写明：没有运动组的系列被当作运动结果报告是 blocking，加 caveat 也不降级 | s4 判 major |
| 3 | decision-review.md，grouping / direction | 补一个典型错误：“运动组对照选错（换成另一条件的对照组，因素混杂）”，并说明归到 grouping 还是 direction | s5 检出了，但归在 direction；cases.csv 的期望写的是 grouping |
| 4 | cases.csv / score.py | s5 的期望加上 direction（或 score 接受同义的检查项） | 同上，避免以后漏判 |
| 5 | tools/case_review.py `pairing_search` | 也搜索已派生的设计列（design_metadata 里的 subject），并处理没有分隔符的名字（`ALORPRE` → 去掉 PRE/POST 后缀）；`subject` 有 33 个水平，超过 24 的上限后被跳过 | s1 的 packet A 候选键为“none”，复核员是从 packet B 和 alignment 记录里找到 subject 的 |
| 6 | case_review.py `flag_unused_subject` | 列名明确是 subject/ID 的列排在年龄等数值列前面 | s1 的第一条 flag 指向 `age of_donor` |
| 7 | 校准流程 | 以后的校准都用 blind.py 这类中性别名：本次的目录名（`s1_..._unpaired`、`c1_...`）和请求标签会直接泄露答案 | 本次已在复核前修正 |
| 8 | study 记录 | 结果与论文方向相反（如 c4 的 OXPHOS）要写进 study caveats，不能只写在 HANDBACK | c4 |

## 5. 过程说明

- 5 个种入 spec 都执行为 VALID，种入错误保留在 decisions 里（s2 的 log2FC 与原运行相关系数为 −1.0）。
- s4 执行时 `merge_raw_tar` 重写了 `E:\agent\mwangLab_pdf\data\GSE174785\GSE174785_merged_from_tar.csv`（数据缓存，不在 git 里）。已核对：基因、列和数值与原运行的合并结果完全一致，只是修改时间变了。
- 复核员看到的是 `.review_queue/case_NN/` 下随机排序的副本（映射见 `reviews/blind_map.json`），自身路径和种入标签已改写，blind.py 检查没有残留。复核员实际看到的 packet 存在 `reviews/<name>/seen/`。
- c2、c3 在 11-03 第一次复核时因额度中断，没有写出任何文件；11-10 用新的子代理重跑。
