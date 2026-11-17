# GSE166322 复核结果

**总体结论：pass**（无 blocking 或 major 项）

## 不一致项

- **direction（minor）**：机械标记 `possible_reversed_contrast` 来自次要对比 `grp_Ctrl_vs_MDZ`（treatment=Ctrl，control=MDZ），与论文 Fig. 3E 的 MDZ vs Ctrl 顺序相反。主要对比 `grp_RunMDZ_vs_MDZ` 方向正确（treatment=RunMDZ，control=MDZ）。该次要对比的设计说明已写明符号相反，HANDBACK 也已换算（MDZ 中 1671 上调、301 下调），所以没有方向相关的结论出错。建议（可选）把它改成 treatment=MDZ、control=Ctrl，使表格名称与论文一致，无需重跑主要对比。

## 留给人工

- 论文未说明联合拟合还是两两拟合（开放政策问题）。
- MDZ vs Ctrl 的上下调比例与论文相反（本次 1671 上 / 301 下，论文 604 上 / 873 下），Fig. 7B 的重叠数也不同（80 对 42，16 对 76）。原因（TPM+limma 与 counts+DESeq2 的差异，或 GEO 标题标注问题）无法从现有文件判断。
