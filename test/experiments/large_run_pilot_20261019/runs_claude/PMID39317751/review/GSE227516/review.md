# 复核结论: GSE227516

总体结论: pass(无 blocking / major 项)

没有 disagree 或 unsure 项。

说明: 该系列为小鼠胰岛 5 久坐 vs 5 跑台训练(10 天),与论文 Fig. 2j,k、Fig. 4c,d 的 n=5 一致;每只动物一个样本,无需配对;论文未给出 RNA-seq 方法与阈值,工作流使用 DESeq2(四舍五入的 tximport 估计计数)与 padj<0.05,已标注为 workflow_default / declared_deviation。仅有一条 minor 提示: SenMayo 基因集未检验,可用自定义基因集做 GSEA 补充。
