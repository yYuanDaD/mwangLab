# 大规模运行审阅表（全部完成，2026-10-26，45 篇）

每篇一行。"我们 vs 原文" 是相同阈值下的 DEG 数。原始记录在同目录的 `progress.csv`（每篇一行）和 `PROBLEMS.md`（每篇的工具问题）。每行背后的证据（原文的估计目标、阈值和报告的数字及其在原文中的位置，我们的矩阵、设计、方法、阈值、DEG 数、结果文件、原文与数据的出入）见 `EVIDENCE.md`，同一编号。

## 总览

| 结论 | 篇数 | 文章 |
|---|---:|---|
| 吻合 | 11 | GSE308674、GSE164798（联合模型重跑后）、GSE156724、GSE243060、GSE270400、GSE275818、GSE267763、GSE276889、GSE304653、GSE308252、GSE164890 |
| 部分吻合（方向对，数量有偏差） | 17 | GSE140089、GSE283493、GSE208639、GSE273041、GSE255280、GSE153100、GSE159861、GSE297318、GSE283250、GSE298775、GSE151066（人部分）、GSE301564、GSE292369、GSE312780、GSE129962、GSE196147、GSE293221 |
| 效应一致，但显著性对不上 | 2 | GSE134698、GSE183150 |
| 未复现 | 3 | GSE179302、GSE232510、GSE328094 |
| 正确拒绝（不是运动对照） | 6 | GSE152133、GSE188236、GSE245048、GSE295777、GSE263103–6、GSE331495 |
| 原文没给数，无法比对 | 6 | GSE294230、GSE308626、GSE282942、GSE263186、GSE326247、GSE124819 |

所有 45 篇的决策记录都通过了校验（VALID）。

## 逐篇

| # | 文章 | 比较内容 | 我们 vs 原文 | 结论 | 需要你看的 |
|---|---|---|---|---|---|
| 1 | GSE283493 大鼠脂肪，运动时段 | 4 个运动 vs 对照（按组织 × 时段） | 0 / 497 / 2 / 37 vs 7 / 353 / 2 / 14 | 部分吻合：晚时段 > 早时段的规律成立 | 原文的 SVA 和 LRT 没有执行器，用了声明偏离 |
| 2 | GSE208639 DM1 力量训练 | 训练后 vs 训练前；患者 vs 对照 | 训练后 vs 前 20（ECM 上调，同原文）；训练前 vs 对照 475 vs 176 | 部分吻合 | 475 是加 TMM 之前跑的，现在重跑应更接近 |
| 3 | GSE308674 乳酸 / HIIT | 4 个处理 vs 对照 | 480 / 417 / 858 / 36 vs 474 / 414 / 857 / 40 | 吻合 | 原先分组单独拟合是 328 / 399 / 764 / 49，改成全样本联合模型后吻合 |
| 4 | GSE273041 超耐力运动员 | 4 个饮食内运动前后比较 | 311 / 299 / 287 / 399 vs 330 / 161 / 222 / 193 | 部分吻合 | "raw_counts" 文件实为 RPKM，用了 limma；原文是混合 ANOVA |
| 5 | GSE297318 830 nm 光照 | 2 个光照 vs 对照 | padj<0.05：2 / 59 vs 458 / ~1388；原始 p<0.05：300 / 578 vs 302 / ~586 | 部分吻合 | 原文写的是校正 p，但数字和原始 p 吻合：原文阈值可能写错 |
| 6 | GSE152133 老年小鼠 | — | — | 正确拒绝 | 衰老研究，没有运动干预；新筛选已排除 |
| 7 | GSE179302 类风湿关节炎，体力活动 | 活跃 vs 不活跃三分位（关联） | 0–5 vs 767 | 未复现 | 信号和种族混杂；没有 sva |
| 8 | GSE164798 5xFAD 小鼠跑轮 | 6 个活动比较 | WT 急性 vs 久坐 828 vs 835；急性 vs 慢性 1602 vs 1617 | 吻合 | 原先单独拟合是 3828 / 2028，联合模型后吻合 |
| 9 | GSE255280 BMAL1 敲除 | 各基因型内运动 vs 对照 | 溶剂组 200 vs 989；KO 5 vs 517 | 部分吻合：溶剂组 >> KO 的方向对 | 数量差距没找到原因（有一个未解释的 PC1） |
| 10 | GSE134698 心衰患者训练 | 训练后 vs 前（3 对） | 1 vs 28 | 效应一致，显著性不对 | 28 个基因方向 27/27 一致，log2FC r = 0.978 |
| 11 | GSE140089 帕金森力量训练 | 训练后 vs 前 | 279 vs 原文 706（其中 304 上调） | 部分吻合（数量偏少） | 原先误记为"原文无总数"，已更正；原文这组数字的阈值待核对；在适用性检查上线前跑完 |
| 12 | GSE153100 健康老龄 | 老年 vs 青年；老年运动 vs 青年（横断面） | 3353 / 311 vs "约 2500，运动后减弱" | 部分吻合：基因层面方向吻合 | 重复元件减弱没有复现 |
| 13 | GSE156724 大鼠高 / 低反应品系 | 功能性超负荷，各品系内 | 1608 / 2341 vs 1866 / 2460 | 吻合（略少） | 测序样本没有训练 vs 久坐，"运动"只体现在品系上 |
| 14 | GSE188236 TGF-β 肌管 | — | — | 正确拒绝 | 这个 series 只有体外实验；原文的运动数据在两个芯片 series 里 |
| 15 | GSE159861 大鼠品系 × 后肢制动 | 制动 vs 对照（2 肌肉 × 2 品系） | 519 / 126 / 186 / 203 vs 744 / 251 / 294 / 326 | 部分吻合 | atrogene 的 log2FC 与原文差 0.06 以内；原文用 voom，这里没有执行器 |
| 16 | GSE183150 Lynch 综合征训练 | 运动 vs 常规护理 × 12 个月变化 | 0 vs 46；原始 p<0.01 有 45 个 | 效应一致，显著性不对 | 原文的阈值在拿不到的补充材料里；原文头部基因排第 1–26 位，方向一致 |
| 17 | GSE232510 下丘脑，高脂 + 跑步 | 高脂 vs 正常；高脂跑步 vs 正常 | 2 / 15 vs 430 / 39 | 未复现 | GEO 少了一组（正常饮食跑步），另一组少 1 个样本 |
| 18 | GSE243060 RED-S 多器官图谱 | 能量不足 vs 对照（两组都跑轮），19 个组织 × 性别 | 雄性肾 5994 vs 6037；卵巢 2525 vs 2563；子宫 8018 vs 8785；肌肉、肌腱和全部组织总数差 1–7% | 吻合 | 对照不是久坐，是"运动换食物"范式；原文 Table S2 拿不到，32/35 个组织×性别没有原文数可比 |
| 19 | GSE270400 大鼠跟腱，跑步后 | 跑后 12 h vs 笼养对照（4 vs 4） | 按原文规则 31 vs 93；只用 padj<0.05 时 95 vs 93 | 吻合 | 原文的数漏用了自己写的 FC≥2；log2FC 和作者上传的表 r = 0.9999999 |
| 20 | GSE245048 ANP 信号缺失 | — | — | 正确拒绝 | 测序样本只有基因型对比（高脂饮食 Npr1+/- vs +/+）；训练实验的小鼠没有测序 |
| 21 | GSE275818 不同跑步距离 + 高脂 | 4 个跑步距离组 vs 高脂对照 | 两组单独拟合 1308 / 1783 / 1061 / 1070 vs 1347 / 1823 / 1103 / 1107；联合模型 1482 / 2397 / 1120 / 1166 | 吻合（单独拟合时） | 这篇用联合模型反而偏多：原文测序公司应是每两组单独拟合。见"请你决定"第 4 条 |
| 22 | GSE283250 应激易感小鼠 + 跑轮 | 应激 vs 对照；有效 / 无效运动 vs 应激（每组 3 只） | 应激 vs 对照 2911 vs 2305；运动比较原文只有火山图 | 部分吻合：OXPHOS 方向一致 | 原文用 FPKM 做 t 检验，GEO 只有计数；按原文的原始 p 规则计数，FDR 校正后几乎不剩 |
| 23 | GSE267763 大鼠运动训练，线粒体 RNA | 训练 vs 久坐，3 个组织部分 | 全肌肉 32 vs 34；线粒体 0 vs 0；左心室 0 vs 0 | 吻合 | 只有加 TMM 才对得上；现有 voom 执行器不加 TMM，线粒体部分会完全失效 |
| 24 | GSE294230 运动诱导的菌群代谢物 | 体外 CD8 T 细胞：甲酸盐 vs PBS（4 vs 4） | padj<0.2：32（原文数在拿不到的 Table S3） | 无法比对 | 这个 series 没有运动样本；子代理按"代谢物是运动的中介"跑了，和 GSE188236/GSE245048 的拒绝不一致，见"请你决定"第 2 条 |
| 25 | GSE298775 心源性恶病质大鼠 + 有氧训练 | 恶病质 vs 对照，在久坐组和训练组内分别比较 | 318 / 214 vs 145 / 18 | 部分吻合：训练后信号变小的结论成立 | 我们的数偏多，原因没找到；训练本身和交互作用都是 0 个基因，原文"训练减轻"的结论只靠两张列表对比 |
| 26 | GSE151066 + GSE279359 急性耐力运动与可变剪接 | 人：运动后 3 h vs 运动前（久坐 / 活跃两组）；小鼠长读长：3 个时间点 vs 运动前 | 人 259 / 194 vs 210 / 116；小鼠 1 / 1 / 1 vs 23 / 13 / 31 | 人部分吻合，小鼠未复现 | 小鼠的 GEO 文件是筛过的子集，缺原文验证的基因；原文主题"可变剪接"没有执行器 |
| 27 | GSE295777 YY1 与心脏代谢 | — | — | 正确拒绝 | 测序的 8 个心脏都是主动脉缩窄模型（YY1 敲除 vs 对照），游泳实验没测序；性别校验发现每组 2 雌 2 雄，原文写的是雄性 |
| 28 | GSE301564 老年雌鼠衰弱程度 + 下坡跑 | 低 / 高衰弱组内跑 vs 不跑，交互作用 | 联合模型 10 / 15，交互 0；两组单独拟合 6 / 54（原文总数在补充材料里） | 部分吻合：点名的 8 个基因方向全对，OXPHOS 规律一致 | 点名基因只在单独拟合时全部显著，又一篇说明原文是两组单独拟合 |
| 29 | GSE292369 运动后急性酮症 | 运动后 vs 运动前；酮 vs 安慰剂 | 2121 vs 1561；酮效应 2 / 4 vs 0 | 部分吻合：点名的 8 个基因方向全对，酮几乎无效应 | 多 36%：原文 Partek 的基因过滤规则没写；GEO 文件静默去掉了 2 个离群样本 |
| 30 | GSE308626 强制跑台训练，心脏肥大 | 训练 vs 久坐（5 vs 5） | FDR<0.1：1389（原文没给总数） | 无法比对，但方向一致 | 原文点名的 10 个基因方向一致且显著；OXPHOS 下降与原文一致 |
| 31 | GSE263103–6 过氧化物酶体 Pex5 敲除 | — | — | 正确拒绝 | 只比较敲除 vs 对照（3/9/18 月龄，均久坐）；跑台只是表型测试；性别校验全为雄性，原文说雌雄混合 |
| 32 | GSE312780 糖尿病患者血流限制训练 | 血流限制 / 常规训练各自 12 周 vs 0 周 | 415 / 48 vs 110 / 18 | 部分吻合：血流限制 >> 常规的规律成立 | 我们多 3–4 倍，可能因为联合模型没有 apeglm 收缩；剔除的受试者原文没写，按 PCA 推断 |
| 33 | GSE282942 鸢尾素与脂肪 IL-33 | 培养的脂肪基质细胞：鸢尾素 vs PBS（3 vs 3） | 562（原文只有火山图） | 无法比对，方向一致 | 又一篇没有运动样本、只有"运动因子"处理的体外实验（同 GSE294230）；Il33 上调 12.4 倍 vs 原文约 10 倍 |
| 34 | GSE276889 + GSE220280 运动前后的线粒体 miRNA | 运动后 / 3 h vs 运动前（mRNA 和 miRNA） | mRNA 上调 173 / 418 vs 178 / 465；miRNA FDR 下 0 vs 0，原始 p 15 / 11 / 22 vs 16 / 11 / 22 | 吻合 | 需要按受试者分区才对得上原文的 p 值 |
| 35 | GSE304653 运动抑制乳腺癌 | 跑轮 vs 久坐：肿瘤微环境、癌细胞两个分选部分 | 79 / 281 vs 87 / 293 | 吻合 | 点名基因和免疫通路都对得上；少的几个可能因为独立过滤的 alpha 固定在 0.05（已修） |
| 36 | GSE263186 运动与肝转移前微环境 | 训练 vs 久坐 × 肿瘤外泌体（肝脏） | 452 / 811 / 1709（原文只有火山图） | 无法比对 | 外泌体诱导 TNFα-NFκB 上升、运动使其下降与原文一致；原文 TREM-1 结论靠 IPA，无法复核 |
| 37 | GSE328094 有氧运动缓解肿瘤小鼠肌萎缩 | 肿瘤 vs 对照；带瘤小鼠运动 vs 不运动 | 按原文写的 FDR：106 / 4 vs 486 / 270；改用原始 p：464 / 296 | 未复现（按原文规则） | 和 GSE297318 一样，原文的数其实对应原始 p；见"请你决定"第 1 条 |
| 38 | GSE308252 运动强度与器官间通讯（人） | 脂肪组织运动后 vs 前；血浆换液实验（冲刺间歇 / 中等强度） | 2819 vs 2600；1960 vs 1677；26 vs 25 | 吻合 | 第一次跑时发现 DESeq2 工具把数字型受试者编号当成连续变量，配对失效，已修复并重跑 |
| 39 | GSE326247 运动肌肉外泌体促进再生 | 成肌细胞经久坐 / 向心 / 离心运动肌肉的外泌体处理 | 834 / 47（原文只有火山图） | 无法比对 | 又一篇体外"运动中介"实验；OXPHOS 基因在向心 vs 久坐中上调与原文一致，但离心并没有更高 |
| 40 | GSE331495 衰老与自噬通量 | — | — | 正确拒绝 | 测序的是年轻 / 年老供体的体外细胞；运动小试验只做了 Western blot |
| 41 | GSE129962 致心律失常性心肌病 + 跑台 | 野生型 / Dsp 小鼠各自运动 vs 常规活动；交互作用 | 1724 / 1409 vs 2529 / 2391；交互 8 vs 65 | 部分吻合：通路方向一致 | 6 月龄基因型对比对不上（64 vs 781），样本标签可疑；计数文件暗示运动组和非运动组是分批计数的 |
| 42 | GSE164890 速滑运动员高原高强度运动 | 运动后 vs 运动前（全血，7 人配对） | 4243 vs 4058 | 吻合 | 作者公开了分析脚本，取整方式、参考水平都能照搬 |
| 43 | GSE196147 大鼠每日抗阻训练 4 周 | 训练 2 / 10 / 20 / 30 天 vs 对侧未训练肢 | 1675 / 1550 / 1048 / 541 vs 2398 / 2218 / 1755 / 3312 | 部分吻合：log2FC 与作者结果 r = 0.92–0.96 | GEO 没有原始计数；按动物配对后，原文第 30 天的大量下调基因在未训练的对侧肢里也有，不是训练效应 |
| 44 | GSE124819 脊髓损伤大鼠肝脏与运动 | 游泳 / 游泳+跑轮 vs 损伤对照；大笼 vs 小笼 | 149 / 263；大笼 vs 小笼 0 | 无法比对 | 原文是数据描述论文，本身没做差异分析；GEO 里的 9 GB bigWig 压缩包把下载卡住了 |
| 45 | GSE293221 运动与黄柏提取物，前列腺癌小鼠 | 跑轮 / 黄柏提取物 vs 对照（每组 3 只） | 运动：联合模型 32 vs 32，两组单独拟合 385；提取物 2589 vs 176 | 部分吻合：运动部分完全对上，提取物对不上 | 这篇反而是联合模型对得上原文；运动组单笼饲养，其他组群养，饲养方式和运动混在一起 |

## 请你决定

1. **GSE297318、GSE328094**：按原文写的"校正 p<0.05"报告（2 / 59），还是按和原文数字吻合的"原始 p<0.05"？现在两个都记了，主结果用的是原文写的规则。
2. **GSE188236 / GSE245048 / GSE295777 / GSE263103 / GSE331495 / GSE152133** 这类"文章里有运动，但这个 series 没有运动样本"的情况，要不要在筛选时按 series 再过滤一次？现在只按文章判断。另外 GSE294230、GSE282942、GSE326247 只有"运动诱导的代谢物 / 肌肉因子"处理的体外样本，这次跑了，算不算运动研究？
3. **联合模型还是两组单独拟合**：GSE308674、GSE164798、GSE293221 用联合模型才对得上原文，GSE275818、GSE301564 却是单独拟合才对得上。默认按联合模型（统计上更合理），原文明显是单独拟合时加一份单独拟合的结果作对照，可以吗？
4. **voom + TMM + 协变量**的执行器缺失，影响了 GSE156724、GSE159861、GSE267763 三篇（GSE267763 的线粒体部分不加 TMM 时 p 值全挤在 1 附近）。建议补。

## 已修的工具问题（本轮）

联合模型（全样本拟合后逐个提取比较），适用性报告进 design 关口，raw count 按数值判断，运动设计检查，X/Y 性别校验，连续协变量，估计计数取整，无标题行的 HTSeq 合并，缺性别列时报错，组内 / 组间受试者因子。仍未修的见 `PROBLEMS.md`。

## 211 篇运行：第一批（2026-10-28，按你的要求暂停在 16/211）

case spec 路线（`tools/case_runner.py`）。每篇一个独立子代理，最多 5 篇并行。16 篇全部通过决策记录校验（VALID）：12 篇跑完，4 篇在 design 门正确拒绝（数据里没有可用的运动对照）。工具补丁见 `../PATCHES_211.md`，续跑方法见 `../RESUME_211.md`。

| 队列号 | 文章 | 系列 | 状态 | 我们 vs 原文 | 用时（分钟） |
|---|---|---|---|---|---:|
| 4 | PMID40623475 | GSE302911 | finished | 6/6 contrasts (0h n=2, exploratory); DEGs U0/U6/U72/T0/T6/T72 351/386/0/372/303/9; paper gives no counts (Fig4A bars, myonuclear subset only) | 6.8 |
| 2 | PMID39393048 | GSE267512 | finished | 1/1 contrast (POST vs PRE, FDR<0.05): 211 DEGs (119 up/92 down) vs paper 214 (122/92); named-gene FDRs match the paper to about 0.01 | 6.8 |
| 3 | PMID42711121 | GSE324257 | finished | 4 planned + 1 exploratory contrasts; EPS-in-Ctrl 0 DEGs (paper: qPCR only); KO vs Ctrl basal 129 at padj<0.001 vs paper 1275 (6v6 sensitivity 927) | 7.6 |
| 8 | PMID34358431 | GSE174785 | refused | 0/2 contrasts run; GSE174785 has no exercise arm (soleus vs EDL ECs x WT vs Atf4-KO, sedentary). Paper: 782 WT RmEC vs WmEC DEGs (padj<0.05, LFC>1); not exercise | 3.1 |
| 6 | PMID35133080 | GSE186045 | finished | 2/2 contrasts (limma log2TPM deviation, no counts deposited); padj<0.05 DEGs CON 820 / EX 11 vs paper 1352 / 132; GO terms match | 7.0 |
| 5 | PMID37365374 | GSE230002 | finished | 2/2 contrasts (limma paired on log2CPM, edgeR blocked); DEGs 122/0 vs paper 877/1 at FDR<0.05,/log2FC/>0.3; 12/12 key genes up, 5 pass; OXPHOS enrichment matches | 7.2 |
| 9 | PMID40993371 | GSE302867 | finished | 4/4 contrasts (limma log2FPKM, paper DESeq2 blocked); DEGs WTEx/WTSed 24, KOEx/KOSed 164, KO/WT sed 111, ex 318; paper gives no counts; Gdf15 ok, WT OXPHOS sign opposite | 6.1 |
| 10 | 0f65e49e563e | GSE236613 | finished | 2/2 contrasts (DESeq2, p<0.05 & FC 1.2); RE vs NE 754 vs paper 4423; NE vs Sham 2737 vs 6697; qPCR gene directions match (Acp5/Fos/Fosb/Calcr) | 5.4 |
| 13 | PMID42679010 | GSE344550 | refused | 0/2 contrasts run; refused at design: GSE344550 is Candida-infected vs uninfected human macrophages (BP/LBP x time), no exercise arm; paper gives no DEG counts (/log2FC/>1) | 3.1 |
| 7 | 4a5659c6cb4a | GSE129694 | refused | 0/2 contrasts run; refused at design: exercise arms (13.5 wk) fully confounded with sacrifice time vs CONT SCI (11.5 wk); paper reports no DEGs/threshold | 18.6 |
| 16 | PMID42356398 | GSE319093 | refused | 0/0 exercise contrasts; RNA-seq is genotype/hypoxia/HFrD/AAV/C2C12 only; exercise (swim test S2.5) never sequenced; refused at design | 4.3 |
| 12 | PMID42241015 | GSE324100 | finished | 3/3 contrasts (limma deviation, FDR<0.05): PBS-ex 0 vs 42, C26-tumour 2165 vs 2740, C26-ex 255 vs 963; paper genes same direction, padj>0.05 | 17.2 |
| 11 | PMID31700184 | GSE124799 | finished | 2/2 contrasts; DESeq2 DEGs 28/14 (Ex/ExSed vs Sed, padj<0.05 default); paper no cutoff or count (Supp T2); edgeR 0/0; paper's cell-cycle GSEA drop not seen | 22.7 |
| 14 | 2dc6a81416a9 | GSE195585 | finished | 9 paper contrasts+3 pooled; PLA 1/4/24h DEGs 2101/4869/3185, CP 2117/5675/2628, CPvsPLA 0/0/0; paper gives no DEG counts (KEGG NES only); ANGPT1/TGFB1 ns | 18.7 |
| 15 | 87d00364413c | GSE244401 | finished | 3/3 exercise contrasts, P<0.01: SCA 1262 vs 524, CON 883 vs 623, interaction 114 vs 160 (exploratory); baseline 795 vs 2264 | 17.3 |
| 18 | PMID34142717 | GSE178262 | finished | 6/6 contrasts; wheel DA vs CTRL 2257/369 vs paper 2094/368 (FDR<=0.05); 4 treadmill tables 1457/2335/912/2904, paper counts only in Fig5 Venns | 10.6 |

## 211 篇运行：第二批（2026-10-28，第 19–23 号，共 21/211）

这一轮按你的要求只跑 5 篇。5 篇全部跑完、全部 VALID。续跑前又修了 4 处工具（见 `../PATCHES_211.md`）：0 个 DEG 的 ORA 记为 not_run、多组正则键、输入路径、配对子集调用。第 24 号刚开始就停了，下次从它开始。

| 队列号 | 文章 | 系列 | 状态 | 我们 vs 原文 | 用时（分钟） |
|---|---|---|---|---|---:|
| 19 | PMID28273480 | GSE97084 | finished | 6/6 paired contrasts + baseline; Old HIIT up 983 vs paper 553 (paper's 6 named MT genes all up); old RT/CT ratio matches; baseline 2063 vs 433 not reproduced | 25.9 |
| 20 | PMID42310491 | GSE324036 | finished | 4/4 contrasts; DEGs WTex-vs-WTsed 61 vs paper 549, SCAsed-vs-WTsed 202 vs 76/79, SCAex-vs-SCAsed 1 (paper minimal); Calb1/Trpc3 log2FC match paper within 0.01 | 12.7 |
| 21 | PMID38232699 | GSE214282;GSE236402 | finished | GSE214282 refused (post-CPET only); GSE236402 3 contrasts: dRNA 0 DEGs vs paper GSEA-only; BL 82 vs not stated; PC 16 vs paper 0 (padj<0.05, workflow default) | 20.9 |
| 22 | 4671b217019c | GSE245594 | finished | 1/1 contrast (SW vs SED, limma on log2 FPKM, transcript level); 8 DE transcripts at padj<0.05 (audit P<0.05 & FC>2: 190); paper gives no count | 4.9 |
| 23 | 917d28883ad5 | GSE235174 | finished | 3 classes, p<.05&/LFC/>=1, unpaired: mRNA 110 vs 86, lncRNA 573 vs 570, circRNA 18 vs 2064; paired run 89/624/1; 15/16 paper genes pass in the paired run | 16.5 |
