# GSE293221 复核结论

总体结论：**pass**（无 blocking / major 项，没有 disagree 或 unsure）。

## 需要人工确认的开放问题
- 主结果用联合模型 (~grp, 9 个样本) 还是两臂模型 (CON+EX)：联合模型 EX vs CON 为 32 个 DEG（与论文数量相同，但是巧合；Lipe、Plin1、Slc7a10 因 PHAM 臂引起的 Cook 标记而 padj 为 NA），两臂模型 385 个 DEG 且五个论文基因方向一致。论文只写 group-pairwise，未说明是否共用离散度，属于已列出的开放政策问题。
- PHAM vs CON 得到 3694 个 DEG（论文 176）：三个 PHAM 肿瘤中有两个与其余样本明显不同，已在 HANDBACK 中说明。

## 说明
其余十项检查均为 agree（stop_reason 不适用）：无重复测量，单笼饲养与运动臂完全混杂已记录，阈值转录正确，RPKM>1 预过滤缺失已作为偏离记录。
