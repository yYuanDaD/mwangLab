# GSE213649 复核结论

**总体:pass**(无 blocking 或 major 项)

该案例按论文方法执行:每个组织单独拟合 DESeq2 `~group`,各组对 LPAEx,FDR<0.10 且 |LFC|>1(不含等号)。分组、方向、配对(同一动物只跨组织重复,每个模型内一只动物一个样本)、矩阵与方法均与论文一致。

## 需要注意的项(minor)

- **threshold / paper_match(minor)**:阈值转写正确。机械标记 `other_rule_matches_paper` 仅针对 PFC 的 LPAEx vs CONSed(论文 170,应用 59;padj<0.05 且 |lfc|>0.585 得 186)。该规则不能推广到其他对比(PFC vs LPASed 在该规则下为 581,论文为 317),所以不存在一致的替代规则。HANDBACK 已提到这个差距,但“已记录的论文数据差异”清单里没有。
  - 建议:把 PFC LPAEx vs CONSed(59 对 170)补入差异清单,处置为 executable_without_change。

## 待人工确认

- 论文没有说明排除了哪些样本。两个被标成肝脏但表达为结肠/肌肉的样本(L_AE7、L_PE4)被排除,是依据组织相关性和与论文计数吻合所作的推断,已在偏差中说明。
