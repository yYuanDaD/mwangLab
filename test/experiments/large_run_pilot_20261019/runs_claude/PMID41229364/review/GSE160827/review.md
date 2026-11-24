# 复核 GSE160827

**总体结论: pass**

拒绝合理:该系列只有 Mybpc2 敲除与野生型的比较,没有运动组。机械标记的 'exercise words' 是 run/lane 编号造成的误报。未运行任何模型,因此分组、方向、阈值等不适用。

## 分歧 / 不确定项

无。

## 备注

- run_or_refuse (agree/none): Refusal matches B1: genotype-only series, no exercise arm (S2.11.p1, S3.5.p1). The mechanical 'exercise words' flag is a false positive: the matched strings are run/lane/index labels in `description`, not exercise terms.
- pairing (na/none): Not run. Stop-reason note that fibres need the donor mouse as block is right (3 WT/2 KO mice); no animal key exists in metadata. Would matter only for a KO-vs-WT run.
- stop_reason (agree/minor): 'Sedentary' is an inference: the paper does not state activity status of these mice. The claim 'no exercise arm' rests on metadata columns, the paper text and the paper's other methods; search is wide enough. 建议: Optionally reword 'sedentary' to 'untreated'.

## 待人工决定

- Whether knockout-only series with no exercise arm should be refused or run as a labelled non-exercise control (open policy).
