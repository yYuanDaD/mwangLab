# GSE256152 复核结论

**总体: human**（需人工确认方向约定）

## 有分歧 / 不确定的项目

### direction（unsure, major）
- 我们的 treatment/Tnm 上调/下调数: swim 73/138, cur 110/54, union 286/237。
- 论文 (S3.2.p3): swim 79/55, cur 28/79, union 154/291。
- 三个对比中主导方向都与论文相反；整体翻转符号（Tnm 对 treatment）后为 swim 138/73, cur 54/110, union 237/286，主导方向三者全部吻合。因此研究 caveat 中“没有单一符号翻转能同时对上三个对比”的说法不成立。
- 论文未写符号约定，Fig 3C 的基因方向文本中也没有。
- 建议: 查 Fig 2C / Fig 3C（WNT5A、IL6、CAMK1G 的方向）或询问作者；在确认前，把上调/下调标注为“约定未确认”，并更正 caveat。若论文为 Tnm 对 treatment，则把符号反过来报告。

## 其余检查
pairing 的候选键（标题后缀）只是重复编号，表达相关性检验不支持，论文说每只小鼠一个肿瘤，因此 pairing 标记为误报，不需要分块。run_or_refuse、grouping、model_fit、confounding、matrix_method、threshold（raw p<0.05 且 |log2FC|>1，严格不等号）、paper_match 均一致；stop_reason 不适用。
