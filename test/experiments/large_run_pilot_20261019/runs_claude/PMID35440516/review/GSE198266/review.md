# 复核结论：GSE198266

总体：**pass**（无 blocking 或 major 项）

没有 `disagree` 或 `unsure` 项。次要说明：

- model_fit：论文逐对做 t 检验，主分析是每个组织 12 样本的联合 limma；已同时报告 6 样本的两组敏感性分析，并声明为偏差。
- threshold / paper_match：采用论文规则（原始 p<0.05 且 FC>1.5），我们的 DEG 数是论文的 1.5 至 3 倍，其他规则都不吻合；已在记录中说明方法差异。
- pairing：mouse 键只连接 SOL 与 GAS，组织分开拟合，无需区组；表达检查为 not_supported。

待人决定的开放问题：论文规则下计数与论文差异较大时，以哪个计数作为主结果。
