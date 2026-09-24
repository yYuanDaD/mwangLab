# Meng 邮件后续：单细胞与其他组学

这份说明把 Meng 邮件中的两个技术问题落实到当前 agent 的输入约束和输出路径中，方便会前 review 或转发给 Meng/Chunyu。它不替代对具体实验设计、样本配对和 feature annotation 的确认。

## 单细胞差异表达参考

- [Squair et al., *Confronting false discoveries in single-cell differential expression*, Nature Communications (2021)](https://doi.org/10.1038/s41467-021-25960-2)：说明把细胞当作独立生物学重复会造成 pseudoreplication 和假阳性；当前 agent 因此按 donor/sample × cell type 聚合 pseudobulk。
- [Crowell et al., *muscat detects subpopulation-specific state transitions from multi-sample multi-condition single-cell transcriptomics data*, Nature Communications (2020)](https://doi.org/10.1038/s41467-020-19894-4)：多样本、多条件、按 cell type 分析的设计参考；当前 agent 的每个 cell type 独立输出与这个分析单位一致。
- [Zimmerman et al., *A practical solution to pseudoreplication bias in single-cell studies*, Nature Communications (2021)](https://doi.org/10.1038/s41467-021-21038-1)：强调个体/样本层面的重复结构；当一个 donor 同时有 control 和 treatment 时，当前分支支持 donor-blocked limma (`~ C(sample) + Treatment`)。

代码仍把 cell-type annotation 视为上游输入，不自动替代 clustering、cell calling 或 annotation。`paired=true` 时只保留同时有两个条件的完整 donor，结果中写出 `n_complete_pairs`，不完整配对会明确跳过。

## 蛋白组与表观组的最小路线

| 模态 | 最小输入 | 推荐统计单位/方法 | 禁止路由 |
| --- | --- | --- | --- |
| 蛋白组（protein-level） | protein ID × sample abundance + 样本 metadata | 线性强度先 log2、缺失值策略、median centering，再 limma | 把 raw intensity 送进 DESeq2；把 score/q-value 当样本列 |
| 蛋白组（peptide-level） | peptide sequence、protein mapping、sample abundance | `aggregate_peptide_to_protein`；线性值默认 sum，log2 值用 mean/median/top-N mean；默认排除 shared peptides 和 decoys | 直接把 peptide 行当独立蛋白；对 log2 值求和 |
| DNA methylation | CpG/probe/region × sample β 值 + metadata | β→M (`log2(β/(1-β))`)、过滤 invariant sites、limma | 把 β 值送进 DESeq2；忽略 bounded/heteroscedastic 结构 |

蛋白组的 peptide roll-up 会同时保存 `<base>_protein_abundance.csv` 和 JSON manifest，记录映射列、汇总方法、shared peptide 策略、过滤数量和输出蛋白数。后续仍需样本 metadata 才能运行 limma。

## 相关方法参考

- [Choi et al., *MSstats*, Bioinformatics (2014)](https://doi.org/10.1093/bioinformatics/btu305)：蛋白和 peptide 的定量、汇总及线性混合模型路线。
- [Ritchie et al., *limma powers differential expression analyses for RNA-sequencing and microarray studies*, Nucleic Acids Research (2015)](https://doi.org/10.1093/nar/gkv007)：当前 log-scale RNA/蛋白表达差异分析所用 moderated linear model 的方法依据。
- [Du et al., *Comparison of Beta-value and M-value methods for quantifying methylation levels by microarray analysis*, BMC Bioinformatics (2010)](https://doi.org/10.1186/1471-2105-11-587)：β 值和 M 值的尺度选择依据。

## 需要 Meng/Bo 确认的实验信息

1. 单细胞主分析是否固定为“每个 cell type 内、donor-level pseudobulk”，全细胞 pooled 结果只作为补充？
2. 蛋白组是 protein-level 结果还是 peptide-level 结果；如果是 peptide-level，protein mapping 是否包含 shared peptide、razor peptide 和 decoy 标记？
3. 每种模态的最小生物学重复数、paired donor、batch/plex、feature annotation，以及期望输出是差异 feature、通路还是跨模态整合结论？
