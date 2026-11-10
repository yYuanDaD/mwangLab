# GSE327036 复核结论

**总体: pass**(无 blocking / major 项)

没有 `disagree` 或 `unsure` 项。

- 设计拒绝正确:RNA-seq 只比较 soleus 中 WT 与 mKO(各 3 个),运动只是另一批动物上的表型测试(S2.3, S2.4, FLT.p2)。
- `pairing_key_candidate` 标记为误报:候选键只是重复编号,FLT.p3 说明每个点是一只独立动物,表达相关性检验为 not_supported(p=0.18)。
- 阈值 FDR<0.05 且 |logFC|>1 转录正确;TPM 与 GEO 声称的 raw counts 不符已记录。
- 待人工(政策问题,非错误):仅基因型的系列若想作为基因型基线复现,需声明偏离(log2 TPM 上用 limma)。
