# GSE280656_synovium 审查结果

总体结论:**pass**

滑膜(synovium)病例每组 n=3,分组、对比方向、基质类型(RSEM 期望计数取整后 DESeq2)和阈值(FDR<0.1,FC>2,严格不等号)均与论文一致,无重复测量或混杂问题。论文的 DEG 数只在 Fig 2b 图中,所以只做了定性比较,没有夸大。结论:通过,仅有一个可选的次要比较(5,114 个筛选基因)。

## model_fit (unsure, none)

证据:Paper silent on joint vs pairwise (S4.4.p2); joint ~grp fit follows the iDEP default and is recorded as an approximation. Open policy item, not an error.

修改建议:无

## paper_match (agree, minor)

证据:Paper counts are only in Fig 2b, so paper_counts is empty and no count comparison is claimed; HANDBACK claims only the qualitative pattern (S24 fewest, R24 >> S24; S2.2.p1, S2.5.p1) and gene directions. S4.4.p3 gives 5,114 selected synovium genes that could be compared.

修改建议:Optional: compute genes with padj<0.1 and FC>1.5 or <0.67 vs control (protein-coding) and compare with 5,114.

## 待人工决定
- Joint versus pairwise fits when the paper is silent (open policy question); the joint fit follows the iDEP default.
