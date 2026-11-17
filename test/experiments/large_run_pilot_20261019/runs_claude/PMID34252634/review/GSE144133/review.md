# 复核结论：GSE144133（PMID 34252634）

**总体：pass**（无 blocking / major 问题）

## 需关注项

- **threshold：unsure，minor。** 阈值转录正确（padj < 0.1，无倍数变化阈值，非包含）。但包 B 的机械标记显示：原始 p < 0.05 且 |log2FC| > 0.585 时得到 811 个基因，接近论文的 817（论文声明的规则为 FDR < 0.1，本案例该规则下为 16 个）。案例未把这一点记为差异。建议补一条差异记录，不改变已应用的规则。

## 待人工决定

- 论文数字符合另一规则（原始 p + 倍数变化）而非其声明的 FDR < 0.1 时，应报告哪一个：这是开放的政策问题。

## 其余检查
run_or_refuse、grouping、direction、pairing、model_fit、confounding、matrix_method、paper_match 均一致；stop_reason 不适用（无停止；sleuth 路线因 bootstraps 未上传而被阻断，理由属实）。
